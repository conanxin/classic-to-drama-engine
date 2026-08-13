from __future__ import annotations

import json
import os
import select
import shutil
import signal
import stat
import subprocess
import time
from pathlib import Path
from typing import Any

from .common import PrototypeError, require
from .events import SignedEventLog


class SandboxSupervisor:
    def __init__(self, *, probe_binary: Path, workspace_root: Path) -> None:
        self.probe_binary = probe_binary.resolve()
        self.workspace_root = workspace_root.resolve()
        self.last_environment_snapshot: dict[str, Any] | None = None
        self.last_probe_result: dict[str, Any] | None = None

    @staticmethod
    def _read_signal(fd: int, expected: bytes, timeout: float = 10.0) -> None:
        ready, _, _ = select.select([fd], [], [], timeout)
        if not ready:
            raise PrototypeError("BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "probe handshake timeout")
        value = os.read(fd, 1)
        require(value == expected, "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "probe handshake")

    @staticmethod
    def _status(pid: int) -> dict[str, str]:
        status: dict[str, str] = {}
        try:
            with Path(f"/proc/{pid}/status").open("r", encoding="utf-8") as handle:
                for line in handle:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        status[key] = value.strip()
        except FileNotFoundError as exc:
            raise PrototypeError(
                "BLOCKED_SANDBOX_ISOLATION_UNPROVEN",
                "supervisor cannot resolve child PID in the mounted /proc namespace",
            ) from exc
        return status

    @staticmethod
    def _fd_inventory(pid: int) -> dict[int, str]:
        result: dict[int, str] = {}
        directory = Path(f"/proc/{pid}/fd")
        for entry in directory.iterdir():
            try:
                result[int(entry.name)] = os.readlink(entry)
            except FileNotFoundError:
                continue
        return result

    @staticmethod
    def _directory_handles(pid: int, inventory: dict[int, str]) -> dict[int, str]:
        result: dict[int, str] = {}
        for fd, target in inventory.items():
            try:
                mode = os.stat(f"/proc/{pid}/fd/{fd}").st_mode
            except OSError:
                continue
            if stat.S_ISDIR(mode):
                result[fd] = target
        return result

    @staticmethod
    def _proc_text(pid: int, name: str) -> str:
        return Path(f"/proc/{pid}/{name}").read_text(encoding="utf-8").strip()

    def run(
        self,
        *,
        slice_fd: int,
        sandbox_root: Path,
        events: SignedEventLog,
        attack: str = "none",
        host_path: Path | None = None,
        inherited_fixture_fd: int | None = None,
        preserve_inherited_fixture_fd: bool = False,
    ) -> dict[str, Any]:
        sandbox_root.mkdir(parents=True, exist_ok=False)
        os.chmod(sandbox_root, 0o555)
        ready_read, ready_write = os.pipe2(os.O_CLOEXEC)
        go_read, go_write = os.pipe2(os.O_CLOEXEC)
        pass_fds = [slice_fd, ready_write, go_read]
        environment = {
            "CTDE_SLICE_FD": str(slice_fd),
            "CTDE_READY_FD": str(ready_write),
            "CTDE_GO_FD": str(go_read),
            "CTDE_SANDBOX_ROOT": str(sandbox_root),
            "CTDE_ATTACK": attack,
            "CTDE_HOST_PATH": str(host_path) if host_path else "/host-only-not-provided",
            "CTDE_WORKSPACE_PATH": str(self.workspace_root),
        }
        if inherited_fixture_fd is not None:
            pass_fds.append(inherited_fixture_fd)
            if preserve_inherited_fixture_fd:
                environment["CTDE_LEAK_FD"] = str(inherited_fixture_fd)

        events.append(
            "sandbox_launch",
            {
                "backend": "chroot+single-uid-map+capability-drop+seccomp",
                "attack": attack,
                "workspace_mount_supplied": False,
                "fixture_store_mount_supplied": False,
                "greek_mount_supplied": False,
                "network_namespace_required": False,
                "network_syscalls_seccomp_denied": True,
            },
        )
        process = subprocess.Popen(
            [str(self.probe_binary)],
            cwd="/tmp",
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            pass_fds=tuple(pass_fds),
            close_fds=True,
            text=True,
        )
        os.close(ready_write)
        os.close(go_read)
        try:
            try:
                self._read_signal(ready_read, b"R")
            except PrototypeError as exc:
                process.wait(timeout=5)
                stderr = process.stderr.read() if process.stderr else ""
                raise PrototypeError(
                    "BLOCKED_SANDBOX_ISOLATION_UNPROVEN",
                    f"initial handshake rc={process.returncode} stderr={stderr!r}",
                ) from exc
            pre_status = self._status(process.pid)
            pre_fds = self._fd_inventory(process.pid)
            uid_map = self._proc_text(process.pid, "uid_map")
            gid_map = self._proc_text(process.pid, "gid_map")
            setgroups_policy = self._proc_text(process.pid, "setgroups")
            try:
                process_root = os.readlink(f"/proc/{process.pid}/root")
            except OSError as exc:
                raise PrototypeError("BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "root inspection") from exc
            os.write(go_write, b"G")
            self._read_signal(ready_read, b"S")
            seccomp_status = self._status(process.pid)
            seccomp_fds = self._fd_inventory(process.pid)
            directory_handles = self._directory_handles(process.pid, seccomp_fds)

            fixture_links = {
                fd: target
                for fd, target in seccomp_fds.items()
                if "synthetic_full_fixture.bin" in target or "synthetic_greek_deny.bin" in target
            }
            environment_snapshot = {
                "sandbox_backend": "chroot+single-uid-map+capability-drop+seccomp",
                "process_root_matches_empty_sandbox": Path(process_root).resolve() == sandbox_root.resolve(),
                "uid_fields": pre_status.get("Uid"),
                "gid_fields": pre_status.get("Gid"),
                "groups_fields": pre_status.get("Groups"),
                "uid_map": uid_map,
                "gid_map": gid_map,
                "setgroups_policy": setgroups_policy,
                "single_uid_namespace_mapping": uid_map.split() == ["0", "0", "1"],
                "single_gid_namespace_mapping": gid_map.split() == ["0", "0", "1"],
                "effective_capabilities_zero": int(pre_status.get("CapEff", "1"), 16) == 0,
                "permitted_capabilities_zero": int(pre_status.get("CapPrm", "1"), 16) == 0,
                "bounding_capabilities_zero": int(pre_status.get("CapBnd", "1"), 16) == 0,
                "ambient_capabilities_zero": int(pre_status.get("CapAmb", "1"), 16) == 0,
                "no_new_privs": seccomp_status.get("NoNewPrivs"),
                "seccomp_mode": seccomp_status.get("Seccomp"),
                "consumer_visible_full_object_handles": len(fixture_links),
                "consumer_visible_full_object_handle_links": fixture_links,
                "consumer_fd_inventory_count": len(seccomp_fds),
                "consumer_visible_directory_handles": len(directory_handles),
                "consumer_visible_directory_handle_links": directory_handles,
                "project_workspace_mounted": False,
                "project_source_tree_visible": False,
                "broker_fixture_store_mounted": False,
                "greek_fixture_or_raw_mounted": False,
                "network_source_fetch_allowed": False,
                "generic_file_read_tools_available": False,
                "consumer_writable_project_paths": 0,
                "full_object_path_persisted": False,
            }
            self.last_environment_snapshot = environment_snapshot
            events.append("sandbox_supervisor_snapshot", environment_snapshot)
            if fixture_links:
                process.terminate()
                process.wait(timeout=5)
                raise PrototypeError("BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "full object fd visible")
            require(
                environment_snapshot["process_root_matches_empty_sandbox"],
                "BLOCKED_SANDBOX_ISOLATION_UNPROVEN",
                "chroot root",
            )
            require(
                environment_snapshot["single_uid_namespace_mapping"]
                and environment_snapshot["single_gid_namespace_mapping"]
                and setgroups_policy == "deny",
                "BLOCKED_SANDBOX_ISOLATION_UNPROVEN",
                "single-id namespace mapping",
            )
            require(
                environment_snapshot["effective_capabilities_zero"]
                and environment_snapshot["permitted_capabilities_zero"]
                and environment_snapshot["bounding_capabilities_zero"]
                and environment_snapshot["ambient_capabilities_zero"],
                "BLOCKED_SANDBOX_ISOLATION_UNPROVEN",
                "capability drop",
            )
            require(
                not directory_handles,
                "BLOCKED_SANDBOX_ISOLATION_UNPROVEN",
                "directory handle visible",
            )
            require(
                seccomp_status.get("Seccomp") == "2" and seccomp_status.get("NoNewPrivs") == "1",
                "BLOCKED_SANDBOX_ISOLATION_UNPROVEN",
                "seccomp status",
            )
            os.write(go_write, b"G")
            stdout, stderr = process.communicate(timeout=15)
            require(process.returncode == 0, "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", f"probe rc={process.returncode}")
            require(not stderr, "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "probe stderr")
            try:
                probe = json.loads(stdout)
            except Exception as exc:
                raise PrototypeError("BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "probe output") from exc
            probe["supervisor"] = environment_snapshot
            self.last_probe_result = probe
            events.append(
                "sandbox_probe_result",
                {
                    "sandbox_backend": probe["sandbox_backend"],
                    "uid": probe["uid"],
                    "gid": probe["gid"],
                    "seccomp_active": probe["seccomp_active"],
                    "slice_sealed": probe["slice_sealed"],
                    "slice_bytes": probe["slice_bytes"],
                    "workspace_visible": probe["workspace_visible"],
                    "host_path_visible": probe["host_path_visible"],
                    "network_source_fetch_allowed": probe["network_source_fetch_allowed"],
                    "attack": probe["attack"],
                    "attack_denied": probe["attack_denied"],
                    "attack_success_bytes": probe["attack_success_bytes"],
                    "parser_status": probe["parser_status"],
                },
            )
            require(
                probe["uid"] == 0 and probe["gid"] == 0 and not probe["uid_drop_supported"],
                "BLOCKED_SANDBOX_ISOLATION_UNPROVEN",
                "single-id namespace identity",
            )
            require(probe["slice_sealed"], "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "slice not sealed")
            require(not probe["workspace_visible"], "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "workspace visible")
            require(not probe["host_path_visible"], "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "host path visible")
            require(not probe["network_source_fetch_allowed"], "BLOCKED_SANDBOX_ISOLATION_UNPROVEN", "network")
            return probe
        finally:
            for fd in (ready_read, go_write):
                try:
                    os.close(fd)
                except OSError:
                    pass
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)
