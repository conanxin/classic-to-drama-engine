from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent.resolve()


def digest_files(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.name.encode("utf-8"))
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace-root", type=Path)
    parser.add_argument("--probe-unavailable", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--delete-trace", action="store_true")
    args = parser.parse_args()
    if args.probe_unavailable:
        with tempfile.TemporaryDirectory(prefix="ctde-monitor-probe-") as temporary:
            probe = subprocess.run(
                ["strace", "-ff", "-qq", "-o", str(Path(temporary) / "trace"), "/bin/true"],
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                check=False,
            )
        monitor_denied = probe.returncode != 0 and "Operation not permitted" in probe.stderr
        result = {
            "schema_version": "1.0.0",
            "artifact_class": "runtime_capability_external_access_audit",
            "suite_id": "RCPTS-20260811-002",
            "audit_authority": "external_strace_process_tree_verifier",
            "trace_scope": "runner and all child processes",
            "trace_raw_persisted": False,
            "monitor_probe_returncode": probe.returncode,
            "monitor_probe_denied_by_environment": monitor_denied,
            "monitor_probe_stderr_sha256": hashlib.sha256(probe.stderr.encode("utf-8")).hexdigest(),
            "coverage": {
                "process_tree_followed": False,
                "sandbox_syscalls_observed": False,
                "second_channels_observed": False,
            },
            "coverage_complete": False,
            "english_real_raw_stat_count": None,
            "english_real_raw_open_count": None,
            "english_real_raw_read_count": None,
            "english_real_raw_hash_count": None,
            "greek_real_raw_stat_count": None,
            "greek_real_raw_open_count": None,
            "greek_real_raw_read_count": None,
            "greek_real_raw_parse_count": None,
            "greek_real_raw_copy_count": None,
            "project_source_tree_scan_count": None,
            "book_structure_map_read_count": None,
            "candidate_artifact_access_count": None,
            "network_connect_success_count": None,
            "model_invocations": 0,
            "candidate_runs_executed": 0,
            "business_outputs_created": 0,
            "overall_result": "fail",
            "blockers": [
                "TRACE_MONITOR_UNAVAILABLE_PTRACE_DENIED"
                if monitor_denied
                else "TRACE_MONITOR_UNAVAILABLE_UNCLASSIFIED"
            ],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, sort_keys=True))
        return
    if args.trace_root is None:
        parser.error("--trace-root is required unless --probe-unavailable is used")
    trace_files = sorted(path for path in args.trace_root.rglob("*") if path.is_file())
    if not trace_files:
        raise SystemExit("no trace files")
    aggregate_digest = digest_files(trace_files)
    lines: list[str] = []
    for path in trace_files:
        lines.extend(path.read_text(encoding="utf-8", errors="replace").splitlines())

    workspace_source = str(WORKSPACE / "source")
    english_basename = "ody-eng-murray1919__raw__full.xml"
    book_map_name = "book_structure_map.yaml"
    candidate_markers = ("analysis_candidate/runs/", "story_structure.yaml", "execution_report.md")
    source_lines = [line for line in lines if workspace_source in line or english_basename in line]
    book_map_lines = [line for line in lines if book_map_name in line]
    candidate_lines = [line for line in lines if any(marker in line for marker in candidate_markers)]
    source_stat_lines = [
        line for line in source_lines
        if re.search(r"\b(stat|lstat|statx|newfstatat|access|faccessat)\(", line)
    ]
    source_open_lines = [line for line in source_lines if re.search(r"\b(open|openat|openat2)\(", line)]
    source_scan_lines = [line for line in source_lines if "getdents" in line]
    successful_connects = [line for line in lines if "connect(" in line and re.search(r"= 0(?:\s|$)", line)]
    runtime_uid_map = Path("/proc/self/uid_map").read_text(encoding="utf-8").split()
    runtime_gid_map = Path("/proc/self/gid_map").read_text(encoding="utf-8").split()
    runtime_setgroups_policy = Path("/proc/self/setgroups").read_text(encoding="utf-8").strip()

    coverage = {
        "trace_files": len(trace_files),
        "trace_lines": len(lines),
        "process_tree_followed": len(trace_files) > 1,
        "fixed_range_pread_observed": any("pread64(" in line and "32439" in line for line in lines),
        "sandbox_chroot_observed": any("chroot(" in line and "= 0" in line for line in lines),
        "single_uid_namespace_runtime": runtime_uid_map == ["0", "0", "1"],
        "single_gid_namespace_runtime": runtime_gid_map == ["0", "0", "1"],
        "setgroups_denied_by_namespace": runtime_setgroups_policy == "deny",
        "root_capability_drop_observed": any("capset(" in line and "= 0" in line for line in lines),
        "seccomp_filter_observed": any("PR_SET_SECCOMP" in line and "= 0" in line for line in lines),
        "sealed_memfd_observed": any("memfd_create(\"ctde-book1-slice\"" in line for line in lines),
        "synthetic_fixture_open_observed": any("synthetic_full_fixture.bin" in line and "openat(" in line for line in lines),
        "second_channel_denials_observed": any(
            syscall in line and "EPERM" in line
            for line in lines
            for syscall in ("mmap(", "sendfile(", "splice(", "copy_file_range(", "io_uring_setup(")
        ),
    }
    required_coverage = all(coverage[key] for key in (
        "process_tree_followed",
        "fixed_range_pread_observed",
        "sandbox_chroot_observed",
        "single_uid_namespace_runtime",
        "single_gid_namespace_runtime",
        "setgroups_denied_by_namespace",
        "root_capability_drop_observed",
        "seccomp_filter_observed",
        "sealed_memfd_observed",
        "synthetic_fixture_open_observed",
        "second_channel_denials_observed",
    ))
    zero_forbidden = not source_lines and not book_map_lines and not candidate_lines and not successful_connects
    result = {
        "schema_version": "1.0.0",
        "artifact_class": "runtime_capability_external_access_audit",
        "suite_id": "RCPTS-20260811-002",
        "audit_authority": "external_strace_process_tree_verifier",
        "trace_scope": "runner and all child processes",
        "trace_sha256": aggregate_digest,
        "trace_raw_persisted": False,
        "coverage": coverage,
        "coverage_complete": required_coverage,
        "english_real_raw_stat_count": len(source_stat_lines),
        "english_real_raw_open_count": len(source_open_lines),
        "english_real_raw_read_count": 0 if not source_open_lines else None,
        "english_real_raw_hash_count": 0 if not source_open_lines else None,
        "greek_real_raw_stat_count": len(source_stat_lines),
        "greek_real_raw_open_count": len(source_open_lines),
        "greek_real_raw_read_count": 0 if not source_open_lines else None,
        "greek_real_raw_parse_count": 0 if not source_open_lines else None,
        "greek_real_raw_copy_count": 0 if not source_open_lines else None,
        "project_source_tree_scan_count": len(source_scan_lines),
        "book_structure_map_read_count": len(book_map_lines),
        "candidate_artifact_access_count": len(candidate_lines),
        "network_connect_success_count": len(successful_connects),
        "model_invocations": 0,
        "candidate_runs_executed": 0,
        "business_outputs_created": 0,
        "overall_result": "pass" if required_coverage and zero_forbidden else "fail",
        "blockers": [
            *([] if required_coverage else ["TRACE_MONITOR_COVERAGE_INCOMPLETE"]),
            *([] if zero_forbidden else ["FORBIDDEN_REAL_SOURCE_OR_CANDIDATE_ACCESS_OBSERVED"]),
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if args.delete_trace:
        shutil.rmtree(args.trace_root)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
