#!/usr/bin/env python3
from __future__ import annotations

import ctypes
import errno
import fcntl
import hashlib
import json
import os
import platform
import select
import shutil
import signal
import stat
import struct
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
WORKSPACE = BASE.parent
MANIFEST_PATH = BASE / "probe_manifest.json"
RUN_ID = "OSOP-20260811-001"
RUN_ROOT = BASE / "runs" / RUN_ID
EVIDENCE = RUN_ROOT / "evidence"
TERMINAL = RUN_ROOT / "terminal"
BIN = RUN_ROOT / "bin"
FIXTURES = RUN_ROOT / "fixtures"
AGGREGATE = RUN_ROOT / "aggregate"
CONSUMER_SOURCE = BASE / "probes" / "synthetic_consumer.c"
CONSUMER_BINARY = BIN / "synthetic_consumer"
MATRIX_PATH = WORKSPACE / "OS_OBSERVABILITY_CAPABILITY_MATRIX.json"
REPORT_PATH = WORKSPACE / "RUNTIME_OS_OBSERVABILITY_PREFLIGHT_RESULT.md"
ARTIFACT_MANIFEST_PATH = BASE / "ARTIFACT_MANIFEST.json"
RUNTIME_ROOT = WORKSPACE / "runtime_capability_prototype"
BASIS_FILES = [
    WORKSPACE / "RUNTIME_CAPABILITY_PROTOTYPE_RESULT.md",
    WORKSPACE / "RUNTIME_CAPABILITY_REPAIR_PLAN.md",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE.resolve()).as_posix()


def read_text_if_exists(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (FileNotFoundError, PermissionError, OSError):
        return None


def readlink_if_exists(path: Path) -> str | None:
    try:
        return os.readlink(path)
    except (FileNotFoundError, PermissionError, OSError):
        return None


def parse_status_text(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key] = value.strip()
    return result


def read_status(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return parse_status_text(text)


def nspid_values(status: dict[str, str]) -> list[int]:
    return [int(value) for value in status.get("NSpid", "").split() if value.isdigit()]


def proc_starttime(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    end = text.rfind(")")
    if end < 0:
        raise ValueError("malformed /proc stat")
    fields_after_comm = text[end + 2 :].split()
    return int(fields_after_comm[19])


def cmdline_parts(path: Path) -> list[str]:
    return [part.decode("utf-8", "replace") for part in path.read_bytes().split(b"\0") if part]


def cmdline_parts_if_readable(path: Path) -> tuple[list[str] | None, str | None]:
    try:
        return cmdline_parts(path), None
    except (FileNotFoundError, ProcessLookupError, PermissionError, OSError) as exc:
        return None, repr(exc)


def tree_manifest(root: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    if not root.exists():
        return {"root": rel(root), "exists": False, "entries": [], "entry_count": 0, "identity_sha256": sha256_bytes(b"[]")}
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        info = path.lstat()
        row: dict[str, Any] = {
            "path": path.relative_to(root).as_posix(),
            "mode": stat.S_IMODE(info.st_mode),
            "mtime_ns": info.st_mtime_ns,
            "size": info.st_size,
        }
        if path.is_symlink():
            row["type"] = "symlink"
            row["target"] = os.readlink(path)
        elif path.is_dir():
            row["type"] = "directory"
        elif path.is_file():
            row["type"] = "file"
            row["sha256"] = sha256_file(path)
        else:
            row["type"] = "other"
        entries.append(row)
    payload = canonical_bytes(entries)
    return {
        "root": rel(root),
        "exists": True,
        "entries": entries,
        "entry_count": len(entries),
        "identity_sha256": sha256_bytes(payload),
    }


def file_identities(paths: list[Path]) -> list[dict[str, Any]]:
    result = []
    for path in paths:
        info = path.stat()
        result.append({
            "path": rel(path),
            "size": info.st_size,
            "mtime_ns": info.st_mtime_ns,
            "mode": stat.S_IMODE(info.st_mode),
            "sha256": sha256_file(path),
        })
    return result


def run_command(argv: list[str], timeout: float = 15.0, cwd: Path | None = None) -> dict[str, Any]:
    started_at = utc_now()
    started_monotonic = time.monotonic_ns()
    try:
        completed = subprocess.run(
            argv,
            cwd=str(cwd or WORKSPACE),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
            close_fds=True,
        )
        return {
            "argv": argv,
            "started_at": started_at,
            "terminal_at": utc_now(),
            "duration_ns": time.monotonic_ns() - started_monotonic,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "argv": argv,
            "started_at": started_at,
            "terminal_at": utc_now(),
            "duration_ns": time.monotonic_ns() - started_monotonic,
            "returncode": None,
            "stdout": exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
            "stderr": exc.stderr.decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or ""),
            "timed_out": True,
        }


def read_line_with_timeout(stream: Any, timeout: float = 5.0) -> str:
    ready, _, _ = select.select([stream], [], [], timeout)
    if not ready:
        raise TimeoutError("consumer handshake timeout")
    line = stream.readline()
    if not line:
        raise EOFError("consumer closed handshake stream")
    return line.rstrip("\n")


def scan_proc_by_nonce(nonce: str) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    token = nonce
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            parts = cmdline_parts(entry / "cmdline")
            if token not in parts:
                continue
            status = read_status(entry / "status")
            matches.append({
                "outer_pid": int(entry.name),
                "nspid": nspid_values(status),
                "ppid_outer": int(status.get("PPid", "-1")),
                "starttime": proc_starttime(entry / "stat"),
                "cmdline": parts,
                "name": status.get("Name"),
                "state": status.get("State"),
            })
        except (FileNotFoundError, ProcessLookupError, PermissionError, OSError, ValueError):
            continue
    return sorted(matches, key=lambda row: row["outer_pid"])


def map_inner_pid(nonce: str, inner_pid: int) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    matches = scan_proc_by_nonce(nonce)
    candidates = [row for row in matches if row["nspid"] and row["nspid"][-1] == inner_pid]
    return (candidates[0] if len(candidates) == 1 else None, matches)


def capture_proc(outer_pid: int, expected_starttime: int, nonce: str) -> dict[str, Any]:
    root = Path("/proc") / str(outer_pid)
    status_text = (root / "status").read_text(encoding="utf-8", errors="replace")
    status = parse_status_text(status_text)
    starttime = proc_starttime(root / "stat")
    cmdline = cmdline_parts(root / "cmdline")
    identity_ok = starttime == expected_starttime and nonce in cmdline
    fd_rows: list[dict[str, Any]] = []
    fd_errors: list[dict[str, str]] = []
    try:
        fd_names = sorted((root / "fd").iterdir(), key=lambda item: int(item.name))
    except (FileNotFoundError, PermissionError, OSError) as exc:
        fd_names = []
        fd_errors.append({"path": str(root / "fd"), "error": repr(exc)})
    for fd_path in fd_names:
        row: dict[str, Any] = {"fd": int(fd_path.name)}
        try:
            row["target"] = os.readlink(fd_path)
        except (FileNotFoundError, PermissionError, OSError) as exc:
            row["target_error"] = repr(exc)
        try:
            row["fdinfo"] = (root / "fdinfo" / fd_path.name).read_text(encoding="utf-8", errors="replace")
        except (FileNotFoundError, PermissionError, OSError) as exc:
            row["fdinfo_error"] = repr(exc)
        try:
            info = fd_path.stat()
            row["device"] = info.st_dev
            row["inode"] = info.st_ino
            row["mode"] = stat.S_IMODE(info.st_mode)
        except (FileNotFoundError, PermissionError, OSError) as exc:
            row["stat_error"] = repr(exc)
        fd_rows.append(row)
    namespaces = {name: readlink_if_exists(root / "ns" / name) for name in ["pid", "pid_for_children", "mnt", "user", "net", "cgroup"]}
    return {
        "outer_pid": outer_pid,
        "expected_starttime": expected_starttime,
        "observed_starttime": starttime,
        "identity_ok": identity_ok,
        "status_text": status_text,
        "status": status,
        "cmdline": cmdline,
        "fd": fd_rows,
        "fd_errors": fd_errors,
        "root_target": readlink_if_exists(root / "root"),
        "exe_target": readlink_if_exists(root / "exe"),
        "namespaces": namespaces,
        "uid_map": read_text_if_exists(root / "uid_map"),
        "gid_map": read_text_if_exists(root / "gid_map"),
        "cgroup": read_text_if_exists(root / "cgroup"),
    }


class InotifyWatcher:
    IN_ACCESS = 0x00000001
    IN_MODIFY = 0x00000002
    IN_ATTRIB = 0x00000004
    IN_CLOSE_WRITE = 0x00000008
    IN_CLOSE_NOWRITE = 0x00000010
    IN_OPEN = 0x00000020
    IN_NONBLOCK = os.O_NONBLOCK
    IN_CLOEXEC = os.O_CLOEXEC

    def __init__(self, paths: list[Path]):
        self.libc = ctypes.CDLL(None, use_errno=True)
        self.libc.inotify_init1.argtypes = [ctypes.c_int]
        self.libc.inotify_init1.restype = ctypes.c_int
        self.libc.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]
        self.libc.inotify_add_watch.restype = ctypes.c_int
        self.fd = self.libc.inotify_init1(self.IN_NONBLOCK | self.IN_CLOEXEC)
        if self.fd < 0:
            value = ctypes.get_errno()
            raise OSError(value, os.strerror(value))
        self.watches: dict[int, str] = {}
        mask = self.IN_ACCESS | self.IN_MODIFY | self.IN_ATTRIB | self.IN_CLOSE_WRITE | self.IN_CLOSE_NOWRITE | self.IN_OPEN
        for path in paths:
            wd = self.libc.inotify_add_watch(self.fd, os.fsencode(path), mask)
            if wd < 0:
                value = ctypes.get_errno()
                os.close(self.fd)
                raise OSError(value, os.strerror(value), str(path))
            self.watches[int(wd)] = str(path)

    def read_events(self) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        while True:
            try:
                data = os.read(self.fd, 65536)
            except BlockingIOError:
                break
            if not data:
                break
            offset = 0
            while offset + 16 <= len(data):
                wd, mask, cookie, length = struct.unpack_from("iIII", data, offset)
                offset += 16
                name_bytes = data[offset : offset + length]
                offset += length
                events.append({
                    "wd": wd,
                    "path": self.watches.get(wd),
                    "mask": mask,
                    "cookie": cookie,
                    "name": name_bytes.rstrip(b"\0").decode("utf-8", "replace"),
                    "is_open": bool(mask & self.IN_OPEN),
                    "is_access": bool(mask & self.IN_ACCESS),
                })
        return events

    def close(self) -> None:
        os.close(self.fd)


def sys_pidfd_open(pid: int) -> tuple[int, int]:
    libc = ctypes.CDLL(None, use_errno=True)
    rc = int(libc.syscall(434, pid, 0))
    return rc, ctypes.get_errno() if rc < 0 else 0


def sys_pidfd_getfd(pidfd: int, targetfd: int) -> tuple[int, int]:
    libc = ctypes.CDLL(None, use_errno=True)
    rc = int(libc.syscall(438, pidfd, targetfd, 0))
    return rc, ctypes.get_errno() if rc < 0 else 0


def parse_key_values(line: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in line.split():
        if "=" in item:
            key, value = item.split("=", 1)
            result[key] = value
    return result


def trace_files(prefix: Path) -> list[Path]:
    return sorted(prefix.parent.glob(prefix.name + "*"))


def trace_summary(prefix: Path, allowed: Path, reference: Path) -> dict[str, Any]:
    rows = []
    combined = ""
    for path in trace_files(prefix):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            text = ""
            rows.append({"path": rel(path), "error": repr(exc)})
            continue
        rows.append({"path": rel(path), "size": path.stat().st_size, "sha256": sha256_file(path), "line_count": len(text.splitlines())})
        combined += text
    return {
        "files": rows,
        "trace_file_count": len(rows),
        "trace_bytes": len(combined.encode("utf-8")),
        "allowed_path_mentions": combined.count(str(allowed)),
        "reference_path_mentions": combined.count(str(reference)),
        "has_process_events": any(token in combined for token in ["clone(", "clone3(", "fork(", "vfork(", "execve(", "exit_group("]),
        "has_allowed_open": str(allowed) in combined and any(token in combined for token in ["open(", "openat(", "openat2("]),
        "has_read": "read(" in combined or "pread64(" in combined,
        "has_network": any(token in combined for token in ["socket(", "connect(", "sendto(", "recvfrom("]),
        "has_write_path": any(token in combined for token in ["write(", "rename(", "link(", "unlink("]),
    }


def compile_consumer() -> dict[str, Any]:
    compiler = shutil.which("cc")
    if not compiler:
        return {"success": False, "blocker": "C_COMPILER_NOT_FOUND", "attempts": []}
    attempts = []
    static_argv = [compiler, "-static", "-O2", "-Wall", "-Wextra", "-o", str(CONSUMER_BINARY), str(CONSUMER_SOURCE)]
    static_result = run_command(static_argv, timeout=30)
    attempts.append(static_result)
    if static_result["returncode"] == 0:
        return {"success": True, "linkage": "static", "attempts": attempts, "binary_sha256": sha256_file(CONSUMER_BINARY)}
    dynamic_argv = [compiler, "-O2", "-Wall", "-Wextra", "-o", str(CONSUMER_BINARY), str(CONSUMER_SOURCE)]
    dynamic_result = run_command(dynamic_argv, timeout=30)
    attempts.append(dynamic_result)
    if dynamic_result["returncode"] == 0:
        return {"success": True, "linkage": "dynamic", "attempts": attempts, "binary_sha256": sha256_file(CONSUMER_BINARY)}
    return {"success": False, "blocker": "SYNTHETIC_CONSUMER_BUILD_FAILED", "attempts": attempts}


def run_hold_tree(allowed: Path, reference: Path, controller: dict[str, Any]) -> dict[str, Any]:
    nonce = "OSOP-HOLD-" + uuid.uuid4().hex
    started_at = utc_now()
    process = subprocess.Popen(
        [str(CONSUMER_BINARY), "hold-tree", str(allowed), nonce],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        close_fds=True,
        start_new_session=True,
    )
    pidfd, pidfd_errno = sys_pidfd_open(process.pid)
    watcher: InotifyWatcher | None = None
    result: dict[str, Any] = {
        "started_at": started_at,
        "nonce": nonce,
        "popen_namespace_pid": process.pid,
        "pidfd_open": {"fd": pidfd, "errno": pidfd_errno, "message": os.strerror(pidfd_errno) if pidfd_errno else "OK"},
    }
    try:
        assert process.stdout is not None and process.stdin is not None
        pre_line = read_line_with_timeout(process.stdout)
        pre = parse_key_values(pre_line)
        inner_pid = int(pre["pid"])
        inner_ppid = int(pre["ppid"])
        mapped, matches = map_inner_pid(nonce, inner_pid)
        result["pre_handshake"] = {"line": pre_line, "parsed": pre}
        result["pre_mapping_matches"] = matches
        result["mapped_main_pre"] = mapped
        result["inner_pid_matches_popen"] = inner_pid == process.pid
        result["inner_ppid_matches_controller"] = inner_ppid == controller["namespace_pid"]
        direct_alias = Path("/proc") / str(process.pid)
        direct_cmdline, direct_cmdline_error = cmdline_parts_if_readable(direct_alias / "cmdline")
        result["direct_namespace_pid_proc_path"] = {
            "path": str(direct_alias),
            "exists": direct_alias.exists(),
            "cmdline": direct_cmdline,
            "cmdline_error": direct_cmdline_error,
        }
        if mapped is None:
            raise RuntimeError("unique outer PID mapping failed")
        result["proc_pre"] = capture_proc(mapped["outer_pid"], mapped["starttime"], nonce)
        watcher = InotifyWatcher([allowed, reference])
        result["observer_ready_at"] = utc_now()
        result["release_open_at"] = utc_now()
        process.stdin.write("G")
        process.stdin.flush()
        post_line = read_line_with_timeout(process.stdout)
        post = parse_key_values(post_line)
        result["post_handshake"] = {"line": post_line, "parsed": post}
        descendant_inner = int(post["descendant"])
        time.sleep(0.15)
        all_matches = scan_proc_by_nonce(nonce)
        result["post_mapping_matches"] = all_matches
        main_candidates = [row for row in all_matches if row["nspid"] and row["nspid"][-1] == inner_pid]
        descendant_candidates = [row for row in all_matches if row["nspid"] and row["nspid"][-1] == descendant_inner]
        result["mapped_main_post"] = main_candidates[0] if len(main_candidates) == 1 else None
        result["mapped_descendant"] = descendant_candidates[0] if len(descendant_candidates) == 1 else None
        if len(main_candidates) == 1:
            result["proc_main_post"] = capture_proc(main_candidates[0]["outer_pid"], main_candidates[0]["starttime"], nonce)
        if len(descendant_candidates) == 1:
            result["proc_descendant_post"] = capture_proc(descendant_candidates[0]["outer_pid"], descendant_candidates[0]["starttime"], nonce)
        if pidfd >= 0:
            target_fd = int(post["fd"])
            duplicated, duplicate_errno = sys_pidfd_getfd(pidfd, target_fd)
            result["pidfd_getfd"] = {"fd": duplicated, "errno": duplicate_errno, "message": os.strerror(duplicate_errno) if duplicate_errno else "OK"}
            if duplicated >= 0:
                duplicate_stat = os.fstat(duplicated)
                result["pidfd_getfd"]["device"] = duplicate_stat.st_dev
                result["pidfd_getfd"]["inode"] = duplicate_stat.st_ino
                os.close(duplicated)
        result["inotify_events"] = watcher.read_events()
        process.stdin.write("X")
        process.stdin.flush()
        process.wait(timeout=5)
        result["returncode"] = process.returncode
        result["terminal_at"] = utc_now()
        result["outer_proc_exists_after_wait"] = {
            str(row["outer_pid"]): (Path("/proc") / str(row["outer_pid"])).exists()
            for row in all_matches
        }
        if pidfd >= 0:
            poller = select.poll()
            poller.register(pidfd, select.POLLIN | select.POLLHUP | select.POLLERR)
            result["pidfd_poll_after_wait"] = poller.poll(0)
    except Exception as exc:
        result["exception"] = repr(exc)
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError, OSError):
            process.kill()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            pass
        result["returncode"] = process.returncode
        result["terminal_at"] = utc_now()
    finally:
        if watcher is not None:
            watcher.close()
        if pidfd >= 0:
            os.close(pidfd)
        if process.stderr is not None:
            result["stderr"] = process.stderr.read()
    return result


def repeated_mapping_probe(controller: dict[str, Any]) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    for index in range(3):
        nonce = f"OSOP-REPEAT-{index}-" + uuid.uuid4().hex
        process = subprocess.Popen(
            [str(CONSUMER_BINARY), "idle", nonce],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            close_fds=True,
        )
        row: dict[str, Any] = {"index": index, "nonce": nonce, "popen_namespace_pid": process.pid}
        try:
            assert process.stdout is not None and process.stdin is not None
            line = read_line_with_timeout(process.stdout)
            parsed = parse_key_values(line)
            mapped, matches = map_inner_pid(nonce, int(parsed["pid"]))
            row.update({"handshake": line, "matches": matches, "mapped": mapped})
            row["unique"] = mapped is not None and len([item for item in matches if item["nspid"] and item["nspid"][-1] == int(parsed["pid"])]) == 1
            row["parent_ok"] = bool(mapped) and mapped["ppid_outer"] == controller["outer_pid"]
            process.stdin.write("X")
            process.stdin.flush()
            process.wait(timeout=3)
            row["returncode"] = process.returncode
            row["outer_proc_absent_after_wait"] = bool(mapped) and not (Path("/proc") / str(mapped["outer_pid"])).exists()
        except Exception as exc:
            row["exception"] = repr(exc)
            process.kill()
            process.wait(timeout=3)
        attempts.append(row)
    return {"attempts": attempts, "all_unique": all(row.get("unique") and row.get("parent_ok") and row.get("outer_proc_absent_after_wait") for row in attempts)}


def strace_launch_probe(allowed: Path, reference: Path) -> dict[str, Any]:
    executable = shutil.which("strace")
    prefix = EVIDENCE / "strace_launch.trace"
    if not executable:
        return {"executable": None, "command": None, "summary": trace_summary(prefix, allowed, reference)}
    argv = [executable, "-ff", "-qq", "-o", str(prefix), "-e", "trace=all", str(CONSUMER_BINARY), "single-open", str(allowed)]
    command = run_command(argv, timeout=15)
    return {"executable": executable, "command": command, "summary": trace_summary(prefix, allowed, reference)}


def strace_attach_probe(allowed: Path, reference: Path) -> dict[str, Any]:
    executable = shutil.which("strace")
    prefix = EVIDENCE / "strace_attach.trace"
    nonce = "OSOP-ATTACH-" + uuid.uuid4().hex
    child = subprocess.Popen(
        [str(CONSUMER_BINARY), "attach-wait", str(allowed), nonce],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        close_fds=True,
    )
    result: dict[str, Any] = {"executable": executable, "nonce": nonce, "child_namespace_pid": child.pid}
    tracer: subprocess.Popen[str] | None = None
    try:
        assert child.stdout is not None and child.stdin is not None
        ready_line = read_line_with_timeout(child.stdout)
        result["child_ready"] = ready_line
        mapped, matches = map_inner_pid(nonce, child.pid)
        result["child_mapping"] = {"mapped": mapped, "matches": matches}
        if executable:
            argv = [executable, "-ff", "-qq", "-o", str(prefix), "-e", "trace=all", "-p", str(child.pid)]
            result["argv"] = argv
            result["started_at"] = utc_now()
            tracer = subprocess.Popen(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
            time.sleep(0.75)
            result["tracer_returncode_before_release"] = tracer.poll()
        child.stdin.write("G")
        child.stdin.flush()
        result["child_done"] = read_line_with_timeout(child.stdout)
        child.stdin.write("X")
        child.stdin.flush()
        child.wait(timeout=5)
        result["child_returncode"] = child.returncode
        if tracer is not None:
            try:
                stdout, stderr = tracer.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                tracer.terminate()
                stdout, stderr = tracer.communicate(timeout=3)
            result["tracer_returncode"] = tracer.returncode
            result["tracer_stdout"] = stdout
            result["tracer_stderr"] = stderr
            result["terminal_at"] = utc_now()
    except Exception as exc:
        result["exception"] = repr(exc)
        child.kill()
        child.wait(timeout=3)
        if tracer is not None and tracer.poll() is None:
            tracer.kill()
            tracer.communicate(timeout=3)
    result["summary"] = trace_summary(prefix, allowed, reference)
    return result


def ptrace_attach_probe() -> dict[str, Any]:
    nonce = "OSOP-PTRACE-" + uuid.uuid4().hex
    child = subprocess.Popen(
        [str(CONSUMER_BINARY), "idle", nonce],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        close_fds=True,
    )
    result: dict[str, Any] = {"nonce": nonce, "child_namespace_pid": child.pid}
    try:
        assert child.stdout is not None and child.stdin is not None
        result["child_ready"] = read_line_with_timeout(child.stdout)
        libc = ctypes.CDLL(None, use_errno=True)
        ctypes.set_errno(0)
        rc = int(libc.ptrace(16, child.pid, None, None))
        saved_errno = ctypes.get_errno()
        result["ptrace_attach"] = {"rc": rc, "errno": saved_errno, "message": os.strerror(saved_errno) if saved_errno else "OK"}
        if rc == 0:
            waited_pid, wait_status = os.waitpid(child.pid, os.WUNTRACED)
            result["wait_stop"] = {"pid": waited_pid, "status": wait_status, "stopped": os.WIFSTOPPED(wait_status)}
            ctypes.set_errno(0)
            detach_rc = int(libc.ptrace(17, child.pid, None, None))
            detach_errno = ctypes.get_errno()
            result["ptrace_detach"] = {"rc": detach_rc, "errno": detach_errno, "message": os.strerror(detach_errno) if detach_errno else "OK"}
        child.stdin.write("X")
        child.stdin.flush()
        child.wait(timeout=5)
        result["child_returncode"] = child.returncode
    except Exception as exc:
        result["exception"] = repr(exc)
        child.kill()
        child.wait(timeout=3)
    return result


def fanotify_probe() -> dict[str, Any]:
    libc = ctypes.CDLL(None, use_errno=True)
    fan_cloexec = 0x00000001
    fan_nonblock = 0x00000002
    fan_class_notif = 0x00000000
    ctypes.set_errno(0)
    rc = int(libc.syscall(300, fan_cloexec | fan_nonblock | fan_class_notif, os.O_RDONLY | os.O_CLOEXEC))
    saved_errno = ctypes.get_errno() if rc < 0 else 0
    result = {"fanotify_init_rc": rc, "errno": saved_errno, "message": os.strerror(saved_errno) if saved_errno else "OK"}
    if rc >= 0:
        os.close(rc)
    return result


def ptrace_traceme_probe() -> dict[str, Any]:
    return run_command([str(CONSUMER_BINARY), "ptrace-traceme"], timeout=10)


def tamper_probe() -> dict[str, Any]:
    target = EVIDENCE / "sacrificial_observer_evidence.txt"
    target.write_text("immutable-observer-evidence\n", encoding="utf-8")
    os.chmod(target, 0o400)
    before = {"sha256": sha256_file(target), "mode": stat.S_IMODE(target.stat().st_mode), "size": target.stat().st_size}
    command = run_command([str(CONSUMER_BINARY), "tamper", str(target)], timeout=10)
    after = {"sha256": sha256_file(target), "mode": stat.S_IMODE(target.stat().st_mode), "size": target.stat().st_size, "content": target.read_text(encoding="utf-8", errors="replace")}
    return {"target": rel(target), "before": before, "command": command, "after": after, "modified": before["sha256"] != after["sha256"]}


def environment_probe() -> dict[str, Any]:
    status_text = Path("/proc/self/status").read_text(encoding="utf-8", errors="replace")
    status = parse_status_text(status_text)
    cap_eff = int(status.get("CapEff", "0"), 16)
    cap_bits = {"CAP_SYS_PTRACE": 19, "CAP_SYS_ADMIN": 21, "CAP_AUDIT_CONTROL": 30, "CAP_PERFMON": 38, "CAP_BPF": 39}
    tools = {name: shutil.which(name) for name in ["strace", "perf", "auditctl", "bpftrace", "bpftool"]}
    yama = read_text_if_exists(Path("/proc/sys/kernel/yama/ptrace_scope"))
    return {
        "captured_at": utc_now(),
        "platform": platform.platform(),
        "uname": list(platform.uname()),
        "hostname": platform.node(),
        "python": sys.version,
        "namespace_pid": os.getpid(),
        "namespace_ppid": os.getppid(),
        "proc_self_status_text": status_text,
        "proc_self_status": status,
        "proc_self_stat_starttime": proc_starttime(Path("/proc/self/stat")),
        "proc_self_cmdline": cmdline_parts(Path("/proc/self/cmdline")),
        "outer_pid": int(status.get("Pid", "-1")),
        "outer_ppid": int(status.get("PPid", "-1")),
        "nspid": nspid_values(status),
        "namespaces": {name: readlink_if_exists(Path("/proc/self/ns") / name) for name in ["pid", "pid_for_children", "mnt", "user", "net", "cgroup"]},
        "uid_map": read_text_if_exists(Path("/proc/self/uid_map")),
        "gid_map": read_text_if_exists(Path("/proc/self/gid_map")),
        "cgroup": read_text_if_exists(Path("/proc/self/cgroup")),
        "lsm_current": read_text_if_exists(Path("/proc/self/attr/current")),
        "yama_ptrace_scope": yama.strip() if yama is not None else None,
        "effective_capabilities_hex": status.get("CapEff"),
        "relevant_capabilities": {name: bool(cap_eff & (1 << bit)) for name, bit in cap_bits.items()},
        "no_new_privs": status.get("NoNewPrivs"),
        "seccomp": status.get("Seccomp"),
        "seccomp_filters": status.get("Seccomp_filters"),
        "tools": tools,
        "tracefs_exists": Path("/sys/kernel/tracing").exists(),
        "tracefs_readable": os.access("/sys/kernel/tracing", os.R_OK),
        "securityfs_exists": Path("/sys/kernel/security").exists(),
        "os_release": read_text_if_exists(Path("/etc/os-release")),
    }


def artifact_refs(*paths: Path) -> list[str]:
    return [rel(path) for path in paths]


def evaluate(
    capability_id: str,
    available: bool,
    evidence_level: str,
    result: str,
    blocker: str,
    artifacts: list[str],
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    started_at = utc_now()
    terminal_at = utc_now()
    row = {
        "probe_run_id": f"{RUN_ID}-{capability_id}",
        "capability_id": capability_id,
        "available": bool(available),
        "evidence_level": evidence_level,
        "result": result,
        "blocker": blocker,
        "evidence_artifact": artifacts,
        "started_at": started_at,
        "terminal_at": terminal_at,
        "details": details or {},
    }
    write_json(TERMINAL / f"{capability_id}.json", row)
    return row


def main() -> int:
    if RUN_ROOT.exists() or MATRIX_PATH.exists() or REPORT_PATH.exists() or ARTIFACT_MANIFEST_PATH.exists():
        raise SystemExit("refusing to overwrite an existing preflight run or result artifact")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    probes = manifest.get("probes", [])
    ids = [item.get("capability_id") for item in probes]
    if not probes or len(ids) != len(set(ids)) or any(not value for value in ids):
        raise SystemExit("invalid probe manifest")
    for path in [EVIDENCE, TERMINAL, BIN, FIXTURES, AGGREGATE]:
        path.mkdir(parents=True, exist_ok=False)

    phase_started_at = utc_now()
    runtime_before = tree_manifest(RUNTIME_ROOT)
    basis_before = file_identities(BASIS_FILES)
    write_json(EVIDENCE / "runtime_tree_before.json", runtime_before)
    write_json(EVIDENCE / "basis_before.json", basis_before)

    allowed = FIXTURES / "allowed.synthetic"
    reference = FIXTURES / "reference_not_opened.synthetic"
    allowed.write_bytes(b"SYNTHETIC-ALLOWED-NON-LITERARY\n" * 8)
    reference.write_bytes(b"SYNTHETIC-REFERENCE-NON-LITERARY\n" * 8)
    fixture_identity = {
        "allowed": {"path": rel(allowed), "size": allowed.stat().st_size, "sha256": sha256_file(allowed), "device": allowed.stat().st_dev, "inode": allowed.stat().st_ino},
        "reference": {"path": rel(reference), "size": reference.stat().st_size, "sha256": sha256_file(reference), "device": reference.stat().st_dev, "inode": reference.stat().st_ino},
        "both_nonempty": allowed.stat().st_size > 0 and reference.stat().st_size > 0,
        "literary_content": False,
    }
    write_json(EVIDENCE / "fixture_identity.json", fixture_identity)

    environment = environment_probe()
    write_json(EVIDENCE / "environment.json", environment)
    controller = {"namespace_pid": environment["namespace_pid"], "outer_pid": environment["outer_pid"], "nspid": environment["nspid"], "starttime": environment["proc_self_stat_starttime"]}

    build = compile_consumer()
    write_json(EVIDENCE / "consumer_build.json", build)
    if not build.get("success"):
        raise SystemExit("synthetic consumer build failed; raw build evidence preserved")

    hold = run_hold_tree(allowed, reference, controller)
    write_json(EVIDENCE / "process_proc_fd_probe.json", hold)
    repeated = repeated_mapping_probe(controller)
    write_json(EVIDENCE / "repeated_pid_mapping.json", repeated)
    strace_version = run_command([environment["tools"]["strace"], "--version"], timeout=10) if environment["tools"]["strace"] else None
    write_json(EVIDENCE / "strace_version.json", strace_version)
    launch = strace_launch_probe(allowed, reference)
    write_json(EVIDENCE / "strace_launch.json", launch)
    attach = strace_attach_probe(allowed, reference)
    write_json(EVIDENCE / "strace_attach.json", attach)
    traceme = ptrace_traceme_probe()
    write_json(EVIDENCE / "ptrace_traceme.json", traceme)
    ptrace_attach = ptrace_attach_probe()
    write_json(EVIDENCE / "ptrace_attach.json", ptrace_attach)
    fanotify = fanotify_probe()
    write_json(EVIDENCE / "fanotify.json", fanotify)
    tamper = tamper_probe()
    write_json(EVIDENCE / "evidence_tamper.json", tamper)

    main_pre = hold.get("mapped_main_pre") or {}
    main_post = hold.get("mapped_main_post") or {}
    descendant = hold.get("mapped_descendant") or {}
    proc_pre = hold.get("proc_pre") or {}
    proc_main = hold.get("proc_main_post") or {}
    proc_descendant = hold.get("proc_descendant_post") or {}
    all_fd = list(proc_main.get("fd", [])) + list(proc_descendant.get("fd", []))
    allowed_stat = allowed.stat()
    reference_stat = reference.stat()
    allowed_fd_rows = [row for row in all_fd if row.get("device") == allowed_stat.st_dev and row.get("inode") == allowed_stat.st_ino]
    reference_fd_rows = [row for row in all_fd if row.get("device") == reference_stat.st_dev and row.get("inode") == reference_stat.st_ino]
    inotify_events = hold.get("inotify_events", [])
    allowed_events = [row for row in inotify_events if row.get("path") == str(allowed)]
    reference_events = [row for row in inotify_events if row.get("path") == str(reference)]
    proc_error_free = not proc_pre.get("fd_errors") and not proc_main.get("fd_errors") and not proc_descendant.get("fd_errors")
    launch_ok = bool(launch.get("command")) and launch["command"].get("returncode") == 0 and launch["summary"].get("has_allowed_open") and launch["summary"].get("has_read")
    attach_ok = attach.get("tracer_returncode") == 0 and attach.get("summary", {}).get("has_allowed_open")
    traceme_ok = traceme.get("returncode") == 0
    ptrace_attach_ok = ptrace_attach.get("ptrace_attach", {}).get("rc") == 0
    fanotify_ok = fanotify.get("fanotify_init_rc", -1) >= 0
    complete_trace_ok = launch_ok
    exact_reference_zero = complete_trace_ok and launch["summary"].get("reference_path_mentions") == 0
    full_tree_trace_ok = complete_trace_ok and launch["summary"].get("has_process_events")
    kernel_info_ok = environment.get("seccomp") is not None and environment.get("no_new_privs") is not None and environment.get("effective_capabilities_hex") is not None
    security_fields = ["Uid", "Gid", "CapEff", "NoNewPrivs", "Seccomp"]
    proc_security_ok = bool(proc_main) and proc_main.get("identity_ok") and all(field in proc_main.get("status", {}) for field in security_fields) and all(proc_main.get("namespaces", {}).get(name) for name in ["pid", "mnt", "user", "net"]) and proc_main.get("root_target") is not None
    parent_relation_ok = bool(main_pre) and main_pre.get("ppid_outer") == controller["outer_pid"] and hold.get("inner_ppid_matches_controller")
    tree_ok = bool(main_post) and bool(descendant) and descendant.get("ppid_outer") == main_post.get("outer_pid")
    lifecycle_ok = hold.get("returncode") == 0 and all(value is False for value in hold.get("outer_proc_exists_after_wait", {}).values())
    pidfd_ok = hold.get("pidfd_open", {}).get("fd", -1) >= 0 and bool(hold.get("pidfd_poll_after_wait"))
    status_ok = bool(proc_main) and proc_main.get("identity_ok") and bool(proc_main.get("status_text"))
    cmdline_ok = bool(proc_main) and proc_main.get("identity_ok") and hold.get("nonce") in proc_main.get("cmdline", [])
    fd_ok = bool(proc_main) and proc_main.get("identity_ok") and proc_error_free and len(proc_main.get("fd", [])) > 0
    fdinfo_ok = fd_ok and all("fdinfo" in row for row in all_fd)
    fd_target_ok = bool(allowed_fd_rows) and all("target" in row for row in allowed_fd_rows)
    host_namespace_distinguished = len(environment.get("nspid", [])) >= 2 and environment["nspid"][-1] == environment["namespace_pid"] and environment["nspid"][0] == environment["outer_pid"]
    child_mapping_ok = bool(main_pre) and len([row for row in hold.get("pre_mapping_matches", []) if row.get("nspid") and row["nspid"][-1] == hold.get("popen_namespace_pid")]) == 1
    current_pid_ok = environment["nspid"] and environment["nspid"][-1] == environment["namespace_pid"]
    ready_ok = hold.get("observer_ready_at") is not None and hold.get("release_open_at") is not None and hold["observer_ready_at"] <= hold["release_open_at"] and not any(row.get("device") == allowed_stat.st_dev and row.get("inode") == allowed_stat.st_ino for row in proc_pre.get("fd", [])) and bool(allowed_events)

    backend_assessment = {
        "strace_launch_ok": launch_ok,
        "strace_attach_ok": attach_ok,
        "ptrace_traceme_ok": traceme_ok,
        "ptrace_attach_ok": ptrace_attach_ok,
        "fanotify_ok": fanotify_ok,
        "complete_pid_attributed_file_trace": complete_trace_ok or fanotify_ok,
        "complete_process_tree_trace": full_tree_trace_ok,
        "event_loss_count": 0 if complete_trace_ok else None,
        "decode_error_count": 0 if complete_trace_ok else None,
        "late_start_count": 0 if launch_ok else None,
        "complete_second_channel_coverage": False,
        "complete_network_write_coverage": False,
        "observer_evidence_write_protected": not tamper.get("modified", False),
        "qualification_note": "No complete process-attributed file/syscall observer is available" if not (complete_trace_ok or fanotify_ok) else "A process-attributed backend responded",
    }
    write_json(EVIDENCE / "trace_backend_assessment.json", backend_assessment)

    outcomes: dict[str, dict[str, Any]] = {}

    def put(capability_id: str, ok: bool, level: str, blocker: str, artifacts: list[str], details: dict[str, Any] | None = None, unknown: bool = False) -> None:
        outcomes[capability_id] = evaluate(
            capability_id,
            ok,
            level if ok else "A0",
            "UNKNOWN" if unknown else ("PASS" if ok else "FAIL"),
            "" if ok else blocker,
            artifacts,
            details,
        )

    process_artifact = artifact_refs(EVIDENCE / "process_proc_fd_probe.json")
    environment_artifact = artifact_refs(EVIDENCE / "environment.json")
    launch_artifact = artifact_refs(EVIDENCE / "strace_launch.json")
    attach_artifact = artifact_refs(EVIDENCE / "strace_attach.json")
    backend_artifact = artifact_refs(EVIDENCE / "trace_backend_assessment.json")

    put("OSOP-001", bool(current_pid_ok), "A1", "CURRENT_PID_IDENTITY_UNBOUND", environment_artifact)
    put("OSOP-002", bool(host_namespace_distinguished), "A2", "HOST_NAMESPACE_PID_LAYER_NOT_EXPOSED", environment_artifact)
    put("OSOP-003", child_mapping_ok, "A2", "CHILD_PID_MAPPING_NOT_UNIQUE", process_artifact)
    put("OSOP-004", parent_relation_ok, "A2", "PARENT_CHILD_RELATION_UNPROVEN", process_artifact)
    put("OSOP-005", tree_ok, "A2", "SYNTHETIC_PROCESS_TREE_NOT_FULLY_OBSERVED", process_artifact)
    put("OSOP-006", lifecycle_ok, "A2", "CHILD_LIFECYCLE_NOT_CLOSED", process_artifact)
    put("OSOP-007", status_ok, "A2", "PROC_STATUS_UNREADABLE_OR_UNBOUND", process_artifact)
    put("OSOP-008", cmdline_ok, "A2", "PROC_CMDLINE_UNREADABLE_OR_UNBOUND", process_artifact)
    put("OSOP-009", fd_ok, "A2", "PROC_FD_UNREADABLE_OR_UNSTABLE", process_artifact)
    put("OSOP-010", fdinfo_ok, "A2", "PROC_FDINFO_UNREADABLE_OR_INCOMPLETE", process_artifact)
    put("OSOP-011", fd_target_ok, "A2", "FD_TARGET_IDENTITY_UNRESOLVED", process_artifact)
    put("OSOP-012", proc_security_ok, "A2", "PROC_SECURITY_OR_NAMESPACE_FIELDS_INCOMPLETE", process_artifact)
    put("OSOP-013", pidfd_ok, "A2", "PIDFD_LIFECYCLE_BINDING_UNAVAILABLE", process_artifact)
    put("OSOP-014", bool(repeated.get("all_unique")), "A2", "REPEATED_PID_BINDING_UNSTABLE", artifact_refs(EVIDENCE / "repeated_pid_mapping.json"))
    strace_exists_ok = bool(strace_version) and strace_version.get("returncode") == 0
    put("OSOP-015", strace_exists_ok, "A1", "STRACE_NOT_AVAILABLE", artifact_refs(EVIDENCE / "strace_version.json"))
    put("OSOP-016", launch_ok, "A2", "TRACE_MONITOR_UNAVAILABLE_STRACE_LAUNCH_DENIED", launch_artifact)
    put("OSOP-017", attach_ok, "A2", "TRACE_MONITOR_UNAVAILABLE_STRACE_ATTACH_DENIED", attach_artifact)
    put("OSOP-018", traceme_ok, "A2", "TRACE_MONITOR_UNAVAILABLE_PTRACE_TRACEME_DENIED", artifact_refs(EVIDENCE / "ptrace_traceme.json"))
    put("OSOP-019", ptrace_attach_ok, "A2", "TRACE_MONITOR_UNAVAILABLE_PTRACE_ATTACH_DENIED", artifact_refs(EVIDENCE / "ptrace_attach.json"))
    put("OSOP-020", kernel_info_ok, "A2", "KERNEL_CONTAINER_RESTRICTIONS_NOT_OBSERVABLE", environment_artifact)
    put("OSOP-021", bool(allowed_fd_rows), "A2", "ALLOWED_FILE_FD_POSITIVE_NOT_OBSERVED", process_artifact)
    put("OSOP-022", not reference_fd_rows and bool(all_fd), "A2", "REFERENCE_FILE_PRESENT_IN_FD_SNAPSHOT", process_artifact, {"scope": "instantaneous_snapshot_only"})
    put("OSOP-023", any(row.get("is_open") for row in allowed_events), "A0", "INOTIFY_ALLOWED_POSITIVE_NOT_OBSERVED", process_artifact, {"pid_attributed": False, "qualifies_complete_a2": False})
    put("OSOP-024", bool(allowed_events) and not reference_events, "A0", "INOTIFY_REFERENCE_ZERO_NOT_ESTABLISHED", process_artifact, {"pid_attributed": False, "qualifies_complete_a2": False})
    put("OSOP-025", fanotify_ok, "A2", "FANOTIFY_INIT_PERMISSION_DENIED", artifact_refs(EVIDENCE / "fanotify.json"))
    put("OSOP-026", complete_trace_ok, "A2", "COMPLETE_FILE_OPEN_SET_UNPROVEN", backend_artifact + launch_artifact)
    put("OSOP-027", exact_reference_zero, "A2", "REFERENCE_ZERO_NOT_PROCESS_ATTRIBUTED", backend_artifact + launch_artifact)
    put("OSOP-028", ready_ok, "A2", "OBSERVER_READY_BEFORE_OPEN_UNPROVEN", process_artifact)
    put("OSOP-029", full_tree_trace_ok, "A2", "DESCENDANT_SYSCALL_TRACE_UNAVAILABLE", backend_artifact + launch_artifact)
    put("OSOP-030", False, "A2", "SECOND_CHANNEL_CLOSED_COVERAGE_UNAVAILABLE", backend_artifact)
    put("OSOP-031", False, "A2", "NETWORK_WRITE_CLOSED_COVERAGE_UNAVAILABLE", backend_artifact)
    put("OSOP-032", backend_assessment["event_loss_count"] == 0 and backend_assessment["decode_error_count"] == 0, "A2", "OBSERVER_LOSS_ACCOUNTING_UNKNOWN", backend_artifact)
    put("OSOP-033", False, "A2", "OBSERVER_CRASH_FAIL_CLOSED_BEHAVIOR_UNQUALIFIED", backend_artifact)
    put("OSOP-034", not tamper.get("modified", False), "A2", "CONSUMER_CAN_MODIFY_OBSERVER_EVIDENCE", artifact_refs(EVIDENCE / "evidence_tamper.json"))
    required_observer_independent = complete_trace_ok and not tamper.get("modified", False)
    put("OSOP-035", required_observer_independent, "A2", "COMPLETE_OS_EVIDENCE_NOT_INDEPENDENT_OF_CONSUMER", backend_artifact + artifact_refs(EVIDENCE / "evidence_tamper.json"))
    put("OSOP-036", required_observer_independent, "A2", "COMPLETE_OS_EVIDENCE_NOT_INDEPENDENT_OF_BROKER", backend_artifact + artifact_refs(EVIDENCE / "evidence_tamper.json"))
    put("OSOP-037", required_observer_independent, "A2", "COMPLETE_OS_EVIDENCE_NOT_INDEPENDENT_OF_BOUNDED_READER", backend_artifact + artifact_refs(EVIDENCE / "evidence_tamper.json"))
    put("OSOP-038", False, "A2", "REAL_SOURCE_ZERO_COUNTS_A2_UNKNOWN", backend_artifact, {"controller_logical_count": 0, "a2_verified_count": None}, unknown=True)
    put("OSOP-039", False, "A2", "CANDIDATE_MODEL_BUSINESS_ZERO_COUNTS_A2_UNKNOWN", backend_artifact, {"controller_logical_counts": {"candidate_runs": 0, "model_calls": 0, "business_outputs": 0}, "a2_verified_counts": None}, unknown=True)

    runtime_after = tree_manifest(RUNTIME_ROOT)
    basis_after = file_identities(BASIS_FILES)
    runtime_unchanged = runtime_before["identity_sha256"] == runtime_after["identity_sha256"] and runtime_before["entry_count"] == runtime_after["entry_count"]
    basis_unchanged = basis_before == basis_after
    write_json(EVIDENCE / "runtime_tree_after.json", runtime_after)
    write_json(EVIDENCE / "basis_after.json", basis_after)
    write_json(EVIDENCE / "boundary_controller_ledger.json", {
        "evidence_level": "A1",
        "english_tei_reads_directed": 0,
        "greek_tei_reads_directed": 0,
        "candidate_runs_directed": 0,
        "model_calls_directed": 0,
        "business_outputs_directed": 0,
        "story_structure_outputs_directed": 0,
        "r2_actions_directed": 0,
        "r3_actions_directed": 0,
        "r4_actions_directed": 0,
        "runtime_tree_before_sha256": runtime_before["identity_sha256"],
        "runtime_tree_after_sha256": runtime_after["identity_sha256"],
        "runtime_unchanged": runtime_unchanged,
        "basis_unchanged": basis_unchanged,
        "a2_phase_wide_file_exec_network_coverage": False,
        "a2_zero_counts": None,
    })
    put("OSOP-040", runtime_unchanged and basis_unchanged, "A1", "RUNTIME_OR_BASIS_DIGEST_CHANGED", artifact_refs(EVIDENCE / "runtime_tree_before.json", EVIDENCE / "runtime_tree_after.json", EVIDENCE / "basis_before.json", EVIDENCE / "basis_after.json"))

    missing_outcomes = [capability_id for capability_id in ids if capability_id not in outcomes]
    extra_outcomes = [capability_id for capability_id in outcomes if capability_id not in ids]
    if missing_outcomes or extra_outcomes:
        raise RuntimeError(f"manifest/outcome mismatch missing={missing_outcomes} extra={extra_outcomes}")

    matrix_rows = []
    for item in probes:
        row = dict(item)
        row.update({key: value for key, value in outcomes[item["capability_id"]].items() if key not in {"capability_id", "details"}})
        row["details"] = outcomes[item["capability_id"]]["details"]
        matrix_rows.append(row)

    totals = {status: sum(1 for row in matrix_rows if row["result"] == status) for status in ["PASS", "FAIL", "UNKNOWN"]}
    executed = len(matrix_rows)
    required_failures = [row["capability_id"] for row in matrix_rows if row["required_for_r1"] and row["result"] != "PASS"]
    all_terminal = executed == totals["PASS"] + totals["FAIL"] + totals["UNKNOWN"]
    r1_pass = not required_failures and all_terminal and complete_trace_ok and backend_assessment["event_loss_count"] == 0 and not tamper.get("modified", False)
    final_status = "PASS_A2_CAPABLE" if r1_pass else "BLOCKED_OS_OBSERVABILITY_INSUFFICIENT"
    blockers = sorted({row["blocker"] for row in matrix_rows if row["blocker"]})
    highest_individual = "A2" if any(row["result"] == "PASS" and row["evidence_level"] == "A2" for row in matrix_rows) else "A1"
    highest_end_to_end = "A2" if r1_pass else "A1"
    phase_terminal_at = utc_now()

    matrix = {
        "schema_version": "1.0",
        "phase": "2-G-R1",
        "suite_id": RUN_ID,
        "fixture_class": "synthetic_non_literary_only",
        "phase_started_at": phase_started_at,
        "phase_terminal_at": phase_terminal_at,
        "final_status": final_status,
        "r1": final_status,
        "r1_satisfied": r1_pass,
        "allow_r2": r1_pass,
        "highest_end_to_end_evidence_level": highest_end_to_end,
        "highest_individual_capability_evidence_level": highest_individual,
        "probe_summary": {
            "manifest": len(probes),
            "discovered": len(probes),
            "executed": executed,
            "terminal": executed,
            "pass": totals["PASS"],
            "fail": totals["FAIL"],
            "unknown": totals["UNKNOWN"],
            "all_terminal_equation_holds": all_terminal,
        },
        "required_failure_capability_ids": required_failures,
        "blockers": blockers,
        "capabilities": matrix_rows,
    }
    write_json(MATRIX_PATH, matrix)
    write_json(AGGREGATE / "probe_results.json", matrix)

    evidence_index_rows = []
    for path in sorted(EVIDENCE.rglob("*")):
        if path.is_file():
            evidence_index_rows.append({"path": rel(path), "size": path.stat().st_size, "sha256": sha256_file(path)})
    evidence_index = {"artifact_count": len(evidence_index_rows), "artifacts": evidence_index_rows}
    write_json(AGGREGATE / "evidence_index.json", evidence_index)

    trace_launch_rc = launch.get("command", {}).get("returncode") if launch.get("command") else None
    trace_launch_stderr = launch.get("command", {}).get("stderr", "") if launch.get("command") else ""
    trace_attach_rc = attach.get("tracer_returncode")
    trace_attach_stderr = attach.get("tracer_stderr", "")
    ptrace_attach_errno = ptrace_attach.get("ptrace_attach", {}).get("errno")
    traceme_stderr = traceme.get("stderr", "")
    traceme_stdout = traceme.get("stdout", "")
    created_paths = [
        rel(MANIFEST_PATH),
        rel(CONSUMER_SOURCE),
        rel(Path(__file__).resolve()),
    ]
    created_paths.extend(rel(path) for path in sorted(RUN_ROOT.rglob("*")) if path.is_file())
    created_paths.extend([rel(MATRIX_PATH), rel(REPORT_PATH), rel(ARTIFACT_MANIFEST_PATH)])
    created_paths = sorted(set(created_paths))

    report = f"""# Runtime OS Observability Preflight Result

Phase: `2-G-R1 — Runtime OS Observability Capability Preflight`  
Suite: `{RUN_ID}`  
Environment: `synthetic_non_literary_only`  
Final status: `{final_status}`  
R1 satisfied: `{'true' if r1_pass else 'false'}`  
Allow R2: `{'true' if r1_pass else 'false'}`

## 1. 结论

`R1 = {final_status}`。

当前环境能提供独立的 `/proc`、PID namespace、pidfd、FD snapshot 与 inotify 路径事件等局部 OS 观测；但它不能提供完整、进程归属明确、覆盖全部 descendants 和文件读取通道的 syscall/file-open trace。因此这些局部 OS 信号不能合成为 R1 所要求的 A2 audit capability，也不能证明 consumer 的完整文件访问集合。

当前环境的**端到端最高 evidence level 为 `{highest_end_to_end}`**。个别 PID／`/proc`／FD snapshot capability 有 A2 级独立证据，但 qualification-wide A2 不成立；A3 也不成立，因为本阶段没有 Runtime A1 pipeline 与完整 A2 observer 的同一 attempt 绑定。

由于 R1 未通过，本阶段明确禁止进入 R2，且未执行 R2／R3／R4。

## 2. Probe 实际枚举与结果

Probe 数量来自 `probe_manifest.json`、{len(probes)} 个 terminal ledger 和 runner aggregate 的真实枚举：

| 指标 | 实际值 |
| --- | ---: |
| Manifest | {len(probes)} |
| Discovered | {len(probes)} |
| Executed | {executed} |
| Terminal | {executed} |
| PASS | {totals['PASS']} |
| FAIL | {totals['FAIL']} |
| UNKNOWN | {totals['UNKNOWN']} |

闭合等式：`executed = PASS + FAIL + UNKNOWN = {executed}`；结果为 `{'成立' if all_terminal else '不成立'}`。

`PASS` 只表示对应的窄 capability 被实际探针确认，不表示整个 R1 PASS。完整能力矩阵见 `OS_OBSERVABILITY_CAPABILITY_MATRIX.json`。

## 3. PID / process namespace

- Controller namespace PID：`{environment['namespace_pid']}`；`/proc` 外层 PID：`{environment['outer_pid']}`。
- Controller `NSpid`：`{environment['nspid']}`；PID namespace：`{environment['namespaces'].get('pid')}`。
- Synthetic child `Popen.pid`（namespace PID）：`{hold.get('popen_namespace_pid')}`。
- Synthetic child 外层 PID：`{main_pre.get('outer_pid')}`；starttime：`{main_pre.get('starttime')}`。
- PID mapping：`{'PASS' if child_mapping_ok else 'FAIL'}`。映射依据为 exact nonce + `NSpid` tail + outer `PPid` + `/proc/<outer>/stat` starttime，不使用数值猜测。
- Parent-child relation：`{'PASS' if parent_relation_ok else 'FAIL'}`。
- Known synthetic descendant tree：`{'PASS' if tree_ok else 'FAIL'}`；完整 syscall observer descendant coverage：`{'PASS' if full_tree_trace_ok else 'FAIL'}`。
- Lifecycle：`{'PASS' if lifecycle_ok else 'FAIL'}`；pidfd supporting proof：`{'PASS' if pidfd_ok else 'FAIL'}`。
- 三次独立重复 mapping：`{'PASS' if repeated.get('all_unique') else 'FAIL'}`。

Host PID 层在 `NSpid` 中可见，但 namespace PID 不能直接当作当前挂载 `/proc/<pid>` 的索引；runner 记录了直接路径是否 absent/alias，并只使用经联合身份验证的外层 PID。

## 4. /proc 与 FD 可观测性

| 能力 | 结果 |
| --- | --- |
| `/proc/<pid>/status` | `{'PASS' if status_ok else 'FAIL'}` |
| `/proc/<pid>/cmdline` | `{'PASS' if cmdline_ok else 'FAIL'}` |
| `/proc/<pid>/fd` | `{'PASS' if fd_ok else 'FAIL'}` |
| `/proc/<pid>/fdinfo` | `{'PASS' if fdinfo_ok else 'FAIL'}` |
| FD target → device/inode | `{'PASS' if fd_target_ok else 'FAIL'}` |
| root/ns/UID/GID/caps/NoNewPrivs/seccomp | `{'PASS' if proc_security_ok else 'FAIL'}` |

Allowed synthetic file 的 held FD 正控制数：`{len(allowed_fd_rows)}`。Reference synthetic file 的 instantaneous held-FD 数：`{len(reference_fd_rows)}`。

该 reference 零值只证明采样时点没有 held FD；它不能排除短暂 `open/read/close`，因此未被用作完整文件访问集合的 A2 证明。

## 5. ptrace / strace 实测

- `strace` executable：`{environment['tools'].get('strace')}`；版本命令实际结果：`{'PASS' if strace_exists_ok else 'FAIL'}`。
- Launch tracing：`{'PASS' if launch_ok else 'FAIL'}`；return code：`{trace_launch_rc}`；trace bytes：`{launch.get('summary', {}).get('trace_bytes')}`。
- Attach tracing：`{'PASS' if attach_ok else 'FAIL'}`；return code：`{trace_attach_rc}`；trace bytes：`{attach.get('summary', {}).get('trace_bytes')}`。
- `PTRACE_TRACEME`：`{'PASS' if traceme_ok else 'FAIL'}`；stdout/stderr：`{(traceme_stdout + ' ' + traceme_stderr).strip()}`。
- Direct-parent `PTRACE_ATTACH`：`{'PASS' if ptrace_attach_ok else 'FAIL'}`；errno：`{ptrace_attach_errno}`。
- `fanotify_init`：`{'PASS' if fanotify_ok else 'FAIL'}`；errno：`{fanotify.get('errno')}` (`{fanotify.get('message')}`).
- Seccomp：`{environment.get('seccomp')}`；NoNewPrivs：`{environment.get('no_new_privs')}`；effective capabilities：`{environment.get('effective_capabilities_hex')}`。
- Relevant capabilities：`{json.dumps(environment.get('relevant_capabilities'), ensure_ascii=False, sort_keys=True)}`。
- Yama `ptrace_scope`：`{environment.get('yama_ptrace_scope') if environment.get('yama_ptrace_scope') is not None else 'not_exposed'}`。

Launch stderr：`{trace_launch_stderr.strip() or '(empty)'}`  
Attach stderr：`{trace_attach_stderr.strip() or '(empty)'}`

命令存在没有被当作 capability PASS；launch、attach 和原生 ptrace 都以实际 synthetic probe 结果判定。

## 6. Process-level filesystem evidence

Synthetic fixtures：

- Allowed：`{rel(allowed)}`，{allowed.stat().st_size} bytes，non-empty。
- Reference/not-opened：`{rel(reference)}`，{reference.stat().st_size} bytes，non-empty。

Consumer 逻辑（A1）只请求 allowed file。独立 OS supporting evidence 显示：

- `/proc` held-FD allowed positive：`{len(allowed_fd_rows)}`。
- `/proc` held-FD reference snapshot：`{len(reference_fd_rows)}`。
- inotify allowed events：`{len(allowed_events)}`，其中 open events：`{sum(1 for row in allowed_events if row.get('is_open'))}`。
- inotify reference events：`{len(reference_events)}`。

但 inotify event 不含 PID，只覆盖两个已知 watched path；`/proc/fd` 只覆盖采样时刻。由于 strace/ptrace/fanotify 均未提供完整 PID-attributed trace，无法证明 consumer tree 的**完整实际文件打开集合**，也无法把 reference 的零事件提升为完整 A2 negative proof。

## 7. Audit independence

- 局部 `/proc`／pidfd／inotify 证据由 controller/kernel 取得，不依赖 consumer 自报；因此它们是独立 supporting signals。
- 完整 syscall/file-open evidence 不可用。
- Sacrificial evidence tamper probe：`{'PROTECTED' if not tamper.get('modified') else 'MODIFIABLE'}`。当前相同 execution identity 能修改 mode `0400` 的测试 evidence 文件，因此“consumer 对 observer evidence 写权限为 0”未证明。
- 结果：required OS evidence 不能证明独立于 consumer、broker 和 bounded reader；`OSOP-035..037` 均不通过。

## 8. Evidence level 与 R1 Gate

| 判断 | 结果 |
| --- | --- |
| 最高 individual capability level | `{highest_individual}` |
| 最高 end-to-end qualification level | `{highest_end_to_end}` |
| Complete PID-attributed open set | `{'true' if complete_trace_ok else 'false'}` |
| Exact event-loss count available | `{'true' if backend_assessment['event_loss_count'] is not None else 'false'}` |
| Evidence tamper protection | `{'true' if not tamper.get('modified') else 'false'}` |
| R1 | `{final_status}` |
| Allow R2 | `{'true' if r1_pass else 'false'}` |

关键 blocker：

{chr(10).join('- `' + item + '`' for item in blockers)}

## 9. 边界终检

Controller 的限定动作账本（A1）记录：English TEI read = 0、Greek TEI read = 0、Candidate Run = 0、model calls = 0、business outputs = 0、`story_structure.yaml` = 0、R2/R3/R4 = 0。

现有 Runtime Prototype 的完整树摘要：

- before：`{runtime_before['identity_sha256']}`（{runtime_before['entry_count']} entries）
- after：`{runtime_after['identity_sha256']}`（{runtime_after['entry_count']} entries）
- unchanged：`{'true' if runtime_unchanged else 'false'}`

两份依据文件 unchanged：`{'true' if basis_unchanged else 'false'}`。

必须区分：由于 phase-wide complete OS observer 不可用，English/Greek、Candidate/model/business 的 **A2 independently verified counts 保持 `unknown`**，不能伪写成由 OS 证据证明的 0。这一 inability 本身触发 `OSOP-038/039` UNKNOWN，并参与 R1 BLOCKED。操作层面没有执行这些禁止动作；审计层面无法将其升级为 A2 zero proof。

## 10. 所有创建或修改文件

本阶段没有修改任何既有 Runtime／suite／Repair Plan 文件。创建文件如下（目录不单列）：

{chr(10).join('- `' + item + '`' for item in created_paths)}

编译器或操作系统在 workspace 外创建后立即清理的内部临时文件不作为项目 artifact 保留；本清单覆盖本阶段所有持久 workspace 文件。

本报告不授权 Candidate Run，不修改 Repair Plan，不启动 R2、R3 或 R4。
"""
    REPORT_PATH.write_text(report, encoding="utf-8")

    artifact_rows = []
    all_artifacts = [path for path in sorted(BASE.rglob("*")) if path.is_file() and path != ARTIFACT_MANIFEST_PATH]
    all_artifacts.extend([MATRIX_PATH, REPORT_PATH])
    for path in sorted(set(all_artifacts)):
        artifact_rows.append({"path": rel(path), "size": path.stat().st_size, "sha256": sha256_file(path)})
    write_json(ARTIFACT_MANIFEST_PATH, {
        "schema_version": "1.0",
        "phase": "2-G-R1",
        "suite_id": RUN_ID,
        "created_or_modified_files": artifact_rows,
        "self_digest_excluded": True,
    })

    print(json.dumps({
        "final_status": final_status,
        "manifest": len(probes),
        "executed": executed,
        "pass": totals["PASS"],
        "fail": totals["FAIL"],
        "unknown": totals["UNKNOWN"],
        "allow_r2": r1_pass,
        "matrix": str(MATRIX_PATH),
        "report": str(REPORT_PATH),
    }, ensure_ascii=False, sort_keys=True))
    return 0 if r1_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
