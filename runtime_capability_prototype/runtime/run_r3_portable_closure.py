from __future__ import annotations

import hashlib
import importlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from build_r3_portable_closure import (
    AUDIT_PATH,
    AUDIT_SHA256,
    PHASE_ID,
    PHASE_KIND,
    PLAN_PATH,
    PLAN_SHA256,
    PROFILE_ID,
    PROTOTYPE_ROOT,
    PUBLIC_TRUST_FREEZE,
    SUITE_ID,
    WORKSPACE_ROOT,
    WRITE_SCOPE_SHA256,
    build_component_freeze,
    build_snapshot_binding,
    canonical_bytes,
    load_canonical_json,
    sha256_file,
    validate_manifest,
)
from build_r3_portable_test_manifest import build_fixture_catalog, build_test_manifest, validate_test_manifest
from verify_r3_portable_closure import build_verification_evidence, execute_leaves, parse_attempts


SUITE_ROOT = PROTOTYPE_ROOT / "r3_portable_suites" / SUITE_ID
CONTROL_ROOT = SUITE_ROOT / "control"
FIXTURE_ROOT = SUITE_ROOT / "fixtures"
ATTEMPTS_PATH = SUITE_ROOT / "attempts" / "r3_attempts.jsonl"
START_PATH = SUITE_ROOT / "evidence" / "start" / "closure_start_verification.json"
DYNAMIC_PATH = SUITE_ROOT / "evidence" / "dynamic" / "dynamic_dependency_observation.json"
END_PATH = SUITE_ROOT / "evidence" / "end" / "closure_end_verification.json"
TERMINALS_PATH = SUITE_ROOT / "evidence" / "controller_terminal" / "controller_terminals.jsonl"
EVIDENCE_MANIFEST_PATH = SUITE_ROOT / "evidence" / "evidence_manifest.json"
AGGREGATE_PATH = SUITE_ROOT / "aggregate" / "r3_portable_closure_results.json"
REPORT_PATH = WORKSPACE_ROOT / "PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md"

IMPLEMENTATION_MANIFEST_PATH = CONTROL_ROOT / "r3_implementation_manifest.json"
EXECUTION_PLAN_PATH = CONTROL_ROOT / "r3_execution_plan.json"
CLOSURE_MANIFEST_PATH = CONTROL_ROOT / "runtime_transitive_closure_manifest.json"
TEST_MANIFEST_PATH = CONTROL_ROOT / "r3_synthetic_test_manifest.json"
COMPONENT_FREEZE_PATH = CONTROL_ROOT / "component_freeze.json"
SNAPSHOT_BINDING_PATH = CONTROL_ROOT / "execution_snapshot_closure_binding.json"
REGISTRY_PATH = CONTROL_ROOT / "closure_snapshot_registry_record.json"
FIXTURE_PATH = FIXTURE_ROOT / "r3_synthetic_fixtures.json"

AUTHORIZATION_ATTACHMENT_PATH = Path("/mnt/c/Users/haili/.codex/attachments/c2534e67-aa28-47d1-86e8-ae75f340b8a5/goal-objective.md")
AUTHORIZATION_SHA256 = "b94334431a39db41db5d2b6e066c9391187908487e1df0ce8bc9e753904699f9"
AUTHORIZATION_BYTES = 19018
BASELINE_HEAD = "bb27268271fd4d5a4c70ef411a37cbae7955672a"
HANDOFF_TAG_OBJECT = "211d98fd6308f7d3c1da4184089d6c6499e54915"
BASELINE_TAG_TARGET = "063fa0eb9d74a4da4e15dec29164eb78fde33655"

IMPLEMENTATION_FILES = [
    "runtime_capability_prototype/contracts/r3_portable_closure_policy_v1.yaml",
    "runtime_capability_prototype/contracts/runtime_transitive_closure_manifest_schema_v1.yaml",
    "runtime_capability_prototype/contracts/component_freeze_schema_v1.yaml",
    "runtime_capability_prototype/contracts/execution_snapshot_closure_binding_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r3_portable_closure_test_requirements.yaml",
    "runtime_capability_prototype/contracts/r3_portable_test_manifest_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r3_portable_controller_terminal_schema_v1.yaml",
    "runtime_capability_prototype/contracts/native_component_build_policy_v1.yaml",
    "runtime_capability_prototype/contracts/closure_snapshot_registry_record_schema_v1.yaml",
    "runtime_capability_prototype/contracts/r3_portable_closure_control_artifact_schema_v1.yaml",
    "runtime_capability_prototype/runtime/build_r3_portable_closure.py",
    "runtime_capability_prototype/runtime/build_r3_portable_test_manifest.py",
    "runtime_capability_prototype/runtime/verify_r3_portable_closure.py",
    "runtime_capability_prototype/runtime/run_r3_portable_closure.py",
    "runtime_capability_prototype/runtime/build_r3_portable_result.py",
]
CREATABLE_FILES = IMPLEMENTATION_FILES + [
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/r3_implementation_manifest.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/r3_execution_plan.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/runtime_transitive_closure_manifest.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/r3_synthetic_test_manifest.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/component_freeze.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/execution_snapshot_closure_binding.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/closure_snapshot_registry_record.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/fixtures/r3_synthetic_fixtures.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/attempts/r3_attempts.jsonl",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/start/closure_start_verification.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/dynamic/dynamic_dependency_observation.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/end/closure_end_verification.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/controller_terminal/controller_terminals.jsonl",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/evidence_manifest.json",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/aggregate/r3_portable_closure_results.json",
    "PORTABLE_RUNTIME_TRANSITIVE_CLOSURE_RESULT.md",
]
CREATABLE_DIRECTORIES = [
    "runtime_capability_prototype/r3_portable_suites/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/control/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/fixtures/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/attempts/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/start/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/dynamic/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/end/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/evidence/controller_terminal/",
    "runtime_capability_prototype/r3_portable_suites/R3PS-20260814-001/aggregate/",
]
WRITE_ALLOWLIST = {WORKSPACE_ROOT / path for path in CREATABLE_FILES}


class ControllerFailure(RuntimeError):
    pass


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=WORKSPACE_ROOT, check=True, capture_output=True, text=True).stdout.strip()


def _exclusive_write(path: Path, raw: bytes) -> None:
    if path not in WRITE_ALLOWLIST:
        raise ControllerFailure(f"write outside allowlist: {path}")
    if path.exists() or path.is_symlink() or not path.parent.is_dir():
        raise ControllerFailure(f"create-once state invalid: {path}")
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    if path.read_bytes() != raw:
        raise ControllerFailure(f"persisted bytes mismatch: {path}")


def _append_bytes(path: Path, raw: bytes) -> None:
    if path not in WRITE_ALLOWLIST or path.is_symlink() or not path.parent.is_dir():
        raise ControllerFailure(f"append path invalid: {path}")
    mode = "ab" if path.exists() else "xb"
    with path.open(mode) as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())


def _fixed_environment() -> dict[str, str]:
    return {
        "HOME": str(Path.home()),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "PYTHONPATH": str(PROTOTYPE_ROOT / "runtime"),
        "TMPDIR": "/tmp",
        "TZ": "UTC",
    }


def _validate_authorization_and_checkpoint() -> dict[str, str]:
    if not AUTHORIZATION_ATTACHMENT_PATH.is_file() or AUTHORIZATION_ATTACHMENT_PATH.is_symlink():
        raise ControllerFailure("authorization attachment unavailable")
    if AUTHORIZATION_ATTACHMENT_PATH.stat().st_size != AUTHORIZATION_BYTES or sha256_file(AUTHORIZATION_ATTACHMENT_PATH) != AUTHORIZATION_SHA256:
        raise ControllerFailure("authorization attachment identity mismatch")
    if sha256_file(PLAN_PATH) != PLAN_SHA256 or sha256_file(AUDIT_PATH) != AUDIT_SHA256:
        raise ControllerFailure("Plan/audit digest drift")
    local_head = _git("rev-parse", "HEAD")
    remote_main = _git("ls-remote", "origin", "refs/heads/main").split()[0]
    handoff_type = _git("cat-file", "-t", "machine-handoff-20260815")
    handoff_object = _git("rev-parse", "machine-handoff-20260815")
    handoff_target = _git("rev-parse", "machine-handoff-20260815^{}")
    baseline_target = _git("rev-parse", "work-handoff-pre-r3g03-20260813^{}")
    if (local_head, remote_main, handoff_type, handoff_object, handoff_target, baseline_target) != (BASELINE_HEAD, BASELINE_HEAD, "tag", HANDOFF_TAG_OBJECT, BASELINE_HEAD, BASELINE_TAG_TARGET):
        raise ControllerFailure("Git checkpoint identity mismatch")
    if _git("diff", "--name-only", "HEAD"):
        raise ControllerFailure("tracked working tree not clean")
    return {"git_head": local_head, "remote_main": remote_main, "machine_handoff_tag_target": handoff_target, "baseline_tag_target": baseline_target}


def _validate_implementation_manifest() -> tuple[dict[str, Any], bytes]:
    implementation, raw = load_canonical_json(IMPLEMENTATION_MANIFEST_PATH)
    required = {
        "artifact_class", "schema_version", "suite_id", "phase_id", "plan_sha256", "audit_sha256",
        "write_scope_sha256", "authorization_sha256", "baseline_head", "bundle_file_count", "files",
        "mutable_existing_files", "creatable_files", "creatable_directories", "missing_paths",
        "unexpected_paths", "materialization_status",
    }
    if set(implementation) != required:
        raise ControllerFailure("implementation manifest closed fields")
    exact = {
        "artifact_class": "ctde_r3_portable_implementation_manifest",
        "schema_version": "1.0.0", "suite_id": SUITE_ID, "phase_id": PHASE_ID,
        "plan_sha256": PLAN_SHA256, "audit_sha256": AUDIT_SHA256,
        "write_scope_sha256": WRITE_SCOPE_SHA256, "authorization_sha256": AUTHORIZATION_SHA256,
        "baseline_head": BASELINE_HEAD, "bundle_file_count": 15,
        "mutable_existing_files": [], "creatable_files": CREATABLE_FILES,
        "creatable_directories": CREATABLE_DIRECTORIES, "missing_paths": [], "unexpected_paths": [],
        "materialization_status": "complete_create_once_bundle",
    }
    for field, expected in exact.items():
        if implementation.get(field) != expected:
            raise ControllerFailure(f"implementation manifest mismatch: {field}")
    if [item["path"] for item in implementation["files"]] != IMPLEMENTATION_FILES:
        raise ControllerFailure("implementation file order")
    for item in implementation["files"]:
        if set(item) != {"path", "sha256", "bytes", "classification"}:
            raise ControllerFailure("implementation record closed fields")
        path = WORKSPACE_ROOT / item["path"]
        if not path.is_file() or path.is_symlink() or sha256_file(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
            raise ControllerFailure(f"implementation file mismatch: {item['path']}")
    return implementation, raw


def _validate_materialized_prefix() -> None:
    expected_present = set(IMPLEMENTATION_FILES + [str(IMPLEMENTATION_MANIFEST_PATH.relative_to(WORKSPACE_ROOT))])
    for relative in expected_present:
        if not (WORKSPACE_ROOT / relative).is_file():
            raise ControllerFailure(f"partial implementation bundle: {relative}")
    for relative in set(CREATABLE_FILES) - expected_present:
        path = WORKSPACE_ROOT / relative
        if path.exists() or path.is_symlink():
            raise ControllerFailure(f"non-prefix artifact present: {relative}")
    status_paths = [line[3:] for line in _git("status", "--porcelain=v1", "--untracked-files=all").splitlines() if line]
    if set(status_paths) != expected_present:
        raise ControllerFailure("implementation prefix working-tree mismatch")


def _make_remaining_directories() -> None:
    for relative in CREATABLE_DIRECTORIES:
        path = WORKSPACE_ROOT / relative
        if path.is_dir():
            continue
        if path.exists() or path.is_symlink():
            raise ControllerFailure(f"directory create state invalid: {relative}")
        path.mkdir()


def _append_terminal(sequence: int, stage_id: str, artifact_path: Path, fixed_epoch: int) -> str:
    previous = "0" * 64
    if TERMINALS_PATH.exists():
        raw = TERMINALS_PATH.read_bytes()
        if raw:
            previous = hashlib.sha256(raw.splitlines(keepends=True)[-1]).hexdigest()
    row = {
        "sequence": sequence,
        "stage_id": stage_id,
        "terminal_status": "PASS",
        "artifact_path": str(artifact_path.relative_to(WORKSPACE_ROOT)),
        "artifact_sha256": sha256_file(artifact_path),
        "previous_row_sha256": previous,
        "fixed_utc_epoch_seconds": fixed_epoch,
    }
    raw = canonical_bytes(row)
    _append_bytes(TERMINALS_PATH, raw)
    return hashlib.sha256(raw).hexdigest()


def _builder_pass(execution_plan_path: Path) -> bytes:
    command = [
        sys.executable,
        str(PROTOTYPE_ROOT / "runtime" / "build_r3_portable_closure.py"),
        "--implementation-manifest", str(IMPLEMENTATION_MANIFEST_PATH),
        "--execution-plan", str(execution_plan_path),
    ]
    completed = subprocess.run(command, cwd=WORKSPACE_ROOT, env=_fixed_environment(), capture_output=True, check=False)
    if completed.returncode != 0:
        raise ControllerFailure(f"closure builder failed: {completed.stderr.decode('utf-8', 'replace')}")
    value = json.loads(completed.stdout.decode("utf-8"))
    if completed.stdout != canonical_bytes(value):
        raise ControllerFailure("closure builder noncanonical output")
    validate_manifest(value, completed.stdout)
    return completed.stdout


def _verifier_snapshot(stage: str, control_paths: list[str], start_path: Path | None = None) -> bytes:
    command = [
        sys.executable,
        str(PROTOTYPE_ROOT / "runtime" / "verify_r3_portable_closure.py"),
        "--stage", stage,
        "--closure-manifest", str(CLOSURE_MANIFEST_PATH),
        "--implementation-manifest", str(IMPLEMENTATION_MANIFEST_PATH),
        "--execution-plan", str(EXECUTION_PLAN_PATH),
    ]
    for relative in control_paths:
        command.extend(["--control-path", relative])
    if start_path is not None:
        command.extend(["--start-snapshot", str(start_path)])
    completed = subprocess.run(command, cwd=WORKSPACE_ROOT, env=_fixed_environment(), capture_output=True, check=False)
    if completed.returncode != 0:
        raise ControllerFailure(f"{stage} verifier failed: {completed.stderr.decode('utf-8', 'replace')}")
    value = json.loads(completed.stdout.decode("utf-8"))
    if completed.stdout != canonical_bytes(value) or value.get("overall_result") != "PASS":
        raise ControllerFailure(f"{stage} verification blocked")
    return completed.stdout


def _dynamic_observation(manifest: dict[str, Any], execution: dict[str, Any]) -> dict[str, Any]:
    modules = sorted({root["module"] for root in manifest["callable_roots"]})
    child_payload = {
        "modules": modules,
        "workspace": str(WORKSPACE_ROOT),
        "forbidden": [str(WORKSPACE_ROOT / "source"), str(WORKSPACE_ROOT / "book_structure_map.yaml")],
    }
    child_code = r'''
import importlib, json, os, sys
payload=json.loads(sys.argv[1])
workspace=os.path.realpath(payload["workspace"])
forbidden=[os.path.realpath(p) for p in payload["forbidden"]]
opens=set()
forbidden_hits=[]
def hook(event,args):
    if event != "open" or not args:
        return
    value=args[0]
    if not isinstance(value,(str,bytes,os.PathLike)):
        return
    path=os.path.realpath(os.fsdecode(value))
    if any(path == item or path.startswith(item+os.sep) for item in forbidden):
        forbidden_hits.append(path)
        raise RuntimeError("forbidden source-content path")
    if (path == workspace or path.startswith(workspace+os.sep)) and os.path.isfile(path):
        opens.add(os.path.relpath(path,workspace).replace(os.sep,"/"))
sys.addaudithook(hook)
origins=[]
for name in payload["modules"]:
    module=importlib.import_module(name)
    origins.append({"module":name,"origin":getattr(module,"__file__",None)})
from ctde_runtime.public_trust import load_portable_public_trust
loaded=load_portable_public_trust()
print(json.dumps({"module_origins":origins,"project_file_opens":sorted(opens),"forbidden_hits":forbidden_hits,"public_trust_freeze_identity":loaded.public_trust_freeze_identity},sort_keys=True,separators=(",",":")))
'''
    code_sha = hashlib.sha256(child_code.encode("utf-8")).hexdigest()
    completed = subprocess.run(
        [sys.executable, "-c", child_code, json.dumps(child_payload, sort_keys=True, separators=(",", ":"))],
        cwd="/tmp", env=execution["fixed_environment"], capture_output=True, text=True, timeout=120, check=False,
    )
    if completed.returncode != 0:
        raise ControllerFailure(f"dynamic child failed: {completed.stderr}")
    observed = json.loads(completed.stdout)
    closure_paths = {node["identity"] for node in manifest["nodes"] if (WORKSPACE_ROOT / node["identity"]).is_file()}
    unknown = sorted(path for path in observed["project_file_opens"] if path not in closure_paths)
    passed = not observed["forbidden_hits"] and not unknown and observed["public_trust_freeze_identity"] == PUBLIC_TRUST_FREEZE
    return {
        "artifact_class": "ctde_r3_portable_dynamic_dependency_observation",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "overall_result": "PASS" if passed else "BLOCKED",
        "child_process": {
            "executable": sys.executable,
            "code_sha256": code_sha,
            "arguments_count": 4,
            "returncode": completed.returncode,
            "fixed_environment": execution["fixed_environment"],
            "inherited_descriptor_policy": "subprocess_capture_only_close_fds_default",
        },
        "module_origins": observed["module_origins"],
        "observed_project_file_opens": observed["project_file_opens"],
        "unknown_project_owned_files": unknown,
        "forbidden_path_hits": observed["forbidden_hits"],
        "public_trust_freeze_identity": observed["public_trust_freeze_identity"],
        "counts": {
            "modules_imported": len(observed["module_origins"]),
            "project_file_opens": len(observed["project_file_opens"]),
            "unknown_project_owned_loaded_bytes": len(unknown),
            "forbidden_path_accesses": len(observed["forbidden_hits"]),
            "model_calls": 0,
            "source_content_reads": 0,
            "project_tree_writes": 0,
        },
    }


def _registry_record(implementation_raw: bytes, execution_raw: bytes, closure: dict[str, Any], closure_raw: bytes, test_raw: bytes, fixture_raw: bytes, freeze_raw: bytes, binding_raw: bytes) -> dict[str, Any]:
    return {
        "artifact_class": "ctde_closure_snapshot_registry_record",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "registry_pass": "independent_controller_rehash",
        "implementation_manifest_sha256": hashlib.sha256(implementation_raw).hexdigest(),
        "execution_plan_sha256": hashlib.sha256(execution_raw).hexdigest(),
        "closure_manifest_sha256": hashlib.sha256(closure_raw).hexdigest(),
        "closure_payload_sha256": closure["closure_payload_sha256"],
        "test_manifest_sha256": hashlib.sha256(test_raw).hexdigest(),
        "fixture_catalog_sha256": hashlib.sha256(fixture_raw).hexdigest(),
        "component_freeze_sha256": hashlib.sha256(freeze_raw).hexdigest(),
        "execution_snapshot_binding_sha256": hashlib.sha256(binding_raw).hexdigest(),
    }


def run() -> int:
    _validate_materialized_prefix()
    checkpoint = _validate_authorization_and_checkpoint()
    implementation, implementation_raw = _validate_implementation_manifest()
    fixed_epoch = int(time.time())
    fixed_environment = _fixed_environment()
    _make_remaining_directories()
    execution = {
        "artifact_class": "ctde_r3_portable_execution_plan",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "phase_id": PHASE_ID,
        "phase_kind": PHASE_KIND,
        "assurance_profile_id": PROFILE_ID,
        "execution_authorized": True,
        "authorization_attachment_sha256": AUTHORIZATION_SHA256,
        "authorization_attachment_bytes": AUTHORIZATION_BYTES,
        "plan_sha256": PLAN_SHA256,
        "audit_sha256": AUDIT_SHA256,
        "write_scope_sha256": WRITE_SCOPE_SHA256,
        "implementation_manifest_sha256": hashlib.sha256(implementation_raw).hexdigest(),
        "git_head": checkpoint["git_head"],
        "remote_main": checkpoint["remote_main"],
        "machine_handoff_tag_target": checkpoint["machine_handoff_tag_target"],
        "baseline_tag_target": checkpoint["baseline_tag_target"],
        "fixed_utc_epoch_seconds": fixed_epoch,
        "fixed_environment": fixed_environment,
        "mutable_existing_files": [],
        "creatable_files": CREATABLE_FILES,
        "creatable_directories": CREATABLE_DIRECTORIES,
        "resume_policy": "same_authorization_exact_valid_prefix_only",
    }
    execution_raw = canonical_bytes(execution)
    _exclusive_write(EXECUTION_PLAN_PATH, execution_raw)
    _append_terminal(1, "R3-S0-AUTH", PLAN_PATH, fixed_epoch)
    _append_terminal(2, "R3-S1-IMPLEMENTATION", IMPLEMENTATION_MANIFEST_PATH, fixed_epoch)
    _append_terminal(3, "R3-S2-BOOTSTRAP", EXECUTION_PLAN_PATH, fixed_epoch)

    first = _builder_pass(EXECUTION_PLAN_PATH)
    second = _builder_pass(EXECUTION_PLAN_PATH)
    if first != second:
        raise ControllerFailure("two-pass closure manifest mismatch")
    _exclusive_write(CLOSURE_MANIFEST_PATH, first)
    closure = json.loads(first.decode("utf-8"))
    _append_terminal(4, "R3-S3-MANIFEST", CLOSURE_MANIFEST_PATH, fixed_epoch)

    fixture = build_fixture_catalog(closure, first)
    fixture_raw = canonical_bytes(fixture)
    test = build_test_manifest(closure, first, fixture_raw, implementation)
    test_raw = canonical_bytes(test)
    _exclusive_write(FIXTURE_PATH, fixture_raw)
    _exclusive_write(TEST_MANIFEST_PATH, test_raw)
    _append_terminal(5, "R3-S4-TEST-CONTROL", TEST_MANIFEST_PATH, fixed_epoch)

    freeze = build_component_freeze(closure, first, implementation_raw)
    freeze_raw = canonical_bytes(freeze)
    binding = build_snapshot_binding(closure, first, implementation_raw, execution, execution_raw, test_raw, fixture_raw, freeze_raw)
    binding_raw = canonical_bytes(binding)
    _exclusive_write(COMPONENT_FREEZE_PATH, freeze_raw)
    _exclusive_write(SNAPSHOT_BINDING_PATH, binding_raw)
    registry = _registry_record(implementation_raw, execution_raw, closure, first, test_raw, fixture_raw, freeze_raw, binding_raw)
    registry_raw = canonical_bytes(registry)
    _exclusive_write(REGISTRY_PATH, registry_raw)
    _append_terminal(6, "R3-S5-FREEZE", REGISTRY_PATH, fixed_epoch)

    control_paths = [
        str(path.relative_to(WORKSPACE_ROOT))
        for path in (IMPLEMENTATION_MANIFEST_PATH, EXECUTION_PLAN_PATH, CLOSURE_MANIFEST_PATH, TEST_MANIFEST_PATH, FIXTURE_PATH, COMPONENT_FREEZE_PATH, SNAPSHOT_BINDING_PATH, REGISTRY_PATH)
    ]
    start_raw = _verifier_snapshot("start", control_paths)
    _exclusive_write(START_PATH, start_raw)
    start = json.loads(start_raw.decode("utf-8"))
    _append_terminal(7, "R3-S6-START", START_PATH, fixed_epoch)

    dynamic = _dynamic_observation(closure, execution)
    dynamic_raw = canonical_bytes(dynamic)
    _exclusive_write(DYNAMIC_PATH, dynamic_raw)
    if dynamic["overall_result"] != "PASS":
        raise ControllerFailure("dynamic observation blocked")
    post = {
        "fixed_utc_epoch_seconds": fixed_epoch,
        "two_pass_manifest_identical": True,
    }
    attempts_first, rows_first, previous = execute_leaves(test, test_raw, closure, implementation, post, "R3-S7-OBSERVE", 1, "0" * 64)
    _append_bytes(ATTEMPTS_PATH, attempts_first)
    _append_terminal(8, "R3-S7-OBSERVE", DYNAMIC_PATH, fixed_epoch)

    end_control_paths = control_paths + [str(START_PATH.relative_to(WORKSPACE_ROOT)), str(DYNAMIC_PATH.relative_to(WORKSPACE_ROOT)), str(ATTEMPTS_PATH.relative_to(WORKSPACE_ROOT)), str(TERMINALS_PATH.relative_to(WORKSPACE_ROOT))]
    end_raw = _verifier_snapshot("end", end_control_paths, START_PATH)
    _exclusive_write(END_PATH, end_raw)
    end = json.loads(end_raw.decode("utf-8"))
    _append_terminal(9, "R3-S8-END", END_PATH, fixed_epoch)

    post.update({
        "start_verified": start["overall_result"] == "PASS",
        "dynamic_observation_complete": dynamic["overall_result"] == "PASS",
        "end_verified": end["overall_result"] == "PASS",
        "closure_delta_count": end["counts"]["closure_delta_count"],
        "unknown_project_owned_loaded_bytes": dynamic["counts"]["unknown_project_owned_loaded_bytes"],
        "existing_project_file_modifications": end["counts"]["tracked_changes"],
        "scope_violations": end["counts"]["scope_violations"],
        "forbidden_path_accesses": dynamic["counts"]["forbidden_path_accesses"],
        "assurance_profile_id": PROFILE_ID,
        "highest_claimed_evidence_level": "A1",
        "certified": False,
        "hardened": False,
        "candidate_ready": False,
        "result_generator_present": (PROTOTYPE_ROOT / "runtime" / "build_r3_portable_result.py").is_file(),
    })
    attempts_second, rows_second, _ = execute_leaves(test, test_raw, closure, implementation, post, "R3-S8-END", len(rows_first) + 1, previous)
    _append_bytes(ATTEMPTS_PATH, attempts_second)
    attempts_raw = ATTEMPTS_PATH.read_bytes()
    if len(parse_attempts(attempts_raw)) != test["leaf_count"]:
        raise ControllerFailure("attempt leaf coverage")

    evidence_inputs = control_paths + [
        str(ATTEMPTS_PATH.relative_to(WORKSPACE_ROOT)), str(START_PATH.relative_to(WORKSPACE_ROOT)),
        str(DYNAMIC_PATH.relative_to(WORKSPACE_ROOT)), str(END_PATH.relative_to(WORKSPACE_ROOT)),
        str(TERMINALS_PATH.relative_to(WORKSPACE_ROOT)),
    ]
    evidence = build_verification_evidence(test, test_raw, attempts_raw, start, start_raw, dynamic, dynamic_raw, end, end_raw, evidence_inputs)
    evidence_raw = canonical_bytes(evidence)
    _exclusive_write(EVIDENCE_MANIFEST_PATH, evidence_raw)
    if evidence["overall_result"] != "PASS":
        raise ControllerFailure("evidence manifest blocked")

    result_builder = importlib.import_module("build_r3_portable_result")
    aggregate_raw = result_builder.build_aggregate_bytes()
    aggregate = json.loads(aggregate_raw.decode("utf-8"))
    if aggregate["formal_status"] != "PASS_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE":
        raise ControllerFailure("aggregate blocked")
    _exclusive_write(AGGREGATE_PATH, aggregate_raw)
    report_raw = result_builder.build_report_bytes(aggregate)
    _exclusive_write(REPORT_PATH, report_raw)
    _append_terminal(10, "R3-S9-RESULT", REPORT_PATH, fixed_epoch)

    changed = [line[3:] for line in _git("status", "--porcelain=v1", "--untracked-files=all").splitlines() if line]
    if set(changed) != set(CREATABLE_FILES) or _git("diff", "--name-only", "HEAD"):
        raise ControllerFailure("final write scope mismatch")
    return 0


def main() -> int:
    try:
        return run()
    except Exception as exc:
        print(f"BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
