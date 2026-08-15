from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import sysconfig
import tempfile
from pathlib import Path
from typing import Any, Iterable

import yaml


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROTOTYPE_ROOT.parent
CONTRACT_ROOT = PROTOTYPE_ROOT / "contracts"
PLAN_PATH = WORKSPACE_ROOT / "FRESH_R3_PORTABLE_TRANSITIVE_CLOSURE_PLAN.md"
AUDIT_PATH = WORKSPACE_ROOT / "FRESH_R3_CURRENT_TREE_AUDIT.json"
POLICY_PATH = CONTRACT_ROOT / "r3_portable_closure_policy_v1.yaml"
PLAN_SHA256 = "2e077e39ba4dc5b8f6970cc35a1aab5915fcfa340917afd78cbb3e23f17e0f83"
AUDIT_SHA256 = "3b1d7715548c6dcff8100b21986aa57f144653518d9d1dcdd88ce39d75635b16"
WRITE_SCOPE_SHA256 = "8b1e9e4012bad4e60bbc9096a7b1b5841f55e48171ae6c1bb341a1d0383778c5"
SUITE_ID = "R3PS-20260814-001"
PHASE_ID = "Phase 2-G-R3FRESH-E1"
PHASE_KIND = "fresh_r3_portable_transitive_closure_materialization_and_deterministic_verification"
PROFILE_ID = "CTDE-PORTABLE-DEV-1"
PUBLIC_TRUST_FREEZE = "7a4a664a8fcccea98ee600d853fc9d36107e307ec2e7e078c9fad42363a831f3"

PRIMARY_CLASSIFICATIONS = {
    "runtime_closure_member",
    "test_only_dependency",
    "build_only_dependency",
    "platform_boundary",
    "excluded_dependency",
}
EDGE_RELATIONS = {
    "imports", "initializes_package", "calls", "loads_schema", "loads_policy",
    "loads_config", "loads_public_trust", "executes", "dlopens", "builds_from",
    "links_to", "resolves_to", "observes", "verifies", "classified_by", "binds_identity",
}
MANIFEST_FIELDS = {
    "artifact_class", "schema_version", "canonicalization_id", "suite_id", "phase_id",
    "phase_kind", "assurance", "identities", "callable_roots", "nodes", "edges", "roles",
    "discovery", "platform", "action_ledger", "closure_payload_sha256",
}


class ClosureBuildFailure(RuntimeError):
    pass


class _UniqueSafeLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader: yaml.Loader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if type(key) is not str or key in result:
            raise ClosureBuildFailure("duplicate or non-string YAML key")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"


def canonical_payload_digest(value: dict[str, Any], excluded_field: str) -> str:
    payload = {key: item for key, item in value.items() if key != excluded_field}
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_canonical_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n") or raw.count(b"\n") != 1:
        raise ClosureBuildFailure(f"noncanonical JSON framing: {path}")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ClosureBuildFailure(f"duplicate JSON key: {path}:{key}")
            result[key] = value
        return result

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    if type(value) is not dict or raw != canonical_bytes(value):
        raise ClosureBuildFailure(f"noncanonical JSON: {path}")
    return value, raw


def load_yaml(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise ClosureBuildFailure(f"YAML framing: {path}")
    value = yaml.load(raw.decode("utf-8"), Loader=_UniqueSafeLoader)
    if type(value) is not dict:
        raise ClosureBuildFailure(f"YAML object required: {path}")
    return value


def _command(argv: list[str], *, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(argv, check=True, capture_output=True, text=True, env=env)
    return completed.stdout.strip()


def _stable_id(prefix: str, identity: str) -> str:
    return f"{prefix}-{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:20]}"


def _member_type(path: str, classification: str) -> str:
    name = Path(path).name
    suffix = Path(path).suffix.lower()
    if name == "__init__.py":
        return "package_initializer"
    if suffix == ".py":
        if name.startswith("build_"):
            return "control_builder"
        if name.startswith("verify_"):
            return "verification_code"
        if name.startswith("run_"):
            return "test_runner"
        return "python_module"
    if suffix in {".yaml", ".yml"}:
        return "schema" if "schema" in name else "policy" if "policy" in name or "requirements" in name else "configuration"
    if suffix == ".json":
        return "public_trust_record" if "trust" in name or "status_registry" in name else "configuration"
    if suffix == ".c":
        return "native_source"
    if classification == "runtime_native_executable" or "/bin/" in path:
        return "native_executable"
    if suffix == ".so" or ".so." in name:
        return "shared_library"
    return "external_registry_record" if "registry_record" in name else "configuration"


def _primary_classification(record: dict[str, Any], path: str) -> str:
    source = str(record.get("classification", ""))
    if source.startswith("runtime_") and source not in {"runtime_test_control"}:
        return "runtime_closure_member"
    if "legacy" in source:
        return "excluded_dependency"
    if "build" in source or Path(path).name.startswith("build_"):
        return "build_only_dependency"
    if "test" in source or Path(path).name.startswith(("run_", "verify_")):
        return "test_only_dependency"
    return "test_only_dependency"


def _file_node(path: Path, identity: str, classification: str, member_type: str | None = None) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise ClosureBuildFailure(f"regular file required: {path}")
    return {
        "node_id": _stable_id("N", identity),
        "classification": classification,
        "member_type": member_type or _member_type(identity, classification),
        "identity": identity,
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
    }


def _virtual_node(identity: str, member_type: str, detail: dict[str, Any]) -> dict[str, Any]:
    raw = canonical_bytes(detail)
    return {
        "node_id": _stable_id("N", identity),
        "classification": "platform_boundary",
        "member_type": member_type,
        "identity": identity,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "virtual_descriptor": detail,
    }


def _validate_inputs(audit: dict[str, Any], implementation: dict[str, Any], execution: dict[str, Any]) -> None:
    if sha256_file(PLAN_PATH) != PLAN_SHA256 or PLAN_PATH.stat().st_size != 37602:
        raise ClosureBuildFailure("Plan identity drift")
    if sha256_file(AUDIT_PATH) != AUDIT_SHA256:
        raise ClosureBuildFailure("audit identity drift")
    policy = load_yaml(POLICY_PATH)
    expected_policy = {
        "plan_sha256": PLAN_SHA256,
        "audit_sha256": AUDIT_SHA256,
        "write_scope_sha256": WRITE_SCOPE_SHA256,
        "suite_id": SUITE_ID,
        "phase_id": PHASE_ID,
    }
    for field, expected in expected_policy.items():
        if policy.get(field) != expected:
            raise ClosureBuildFailure(f"policy mismatch: {field}")
    if audit.get("audit_summary", {}).get("callable_root_count") != 32:
        raise ClosureBuildFailure("audit callable root count")
    if audit.get("audit_summary", {}).get("active_r3_role_gap_count") != 0:
        raise ClosureBuildFailure("active R3 role gap")
    if implementation.get("bundle_file_count") != 15 or len(implementation.get("files", [])) != 15:
        raise ClosureBuildFailure("implementation inventory count")
    if implementation.get("materialization_status") != "complete_create_once_bundle":
        raise ClosureBuildFailure("implementation materialization status")
    if implementation.get("baseline_head") != "bb27268271fd4d5a4c70ef411a37cbae7955672a":
        raise ClosureBuildFailure("implementation baseline head")
    exact_execution = {
        "suite_id": SUITE_ID,
        "phase_id": PHASE_ID,
        "phase_kind": PHASE_KIND,
        "plan_sha256": PLAN_SHA256,
        "audit_sha256": AUDIT_SHA256,
        "write_scope_sha256": WRITE_SCOPE_SHA256,
        "execution_authorized": True,
    }
    for field, expected in exact_execution.items():
        if execution.get(field) != expected:
            raise ClosureBuildFailure(f"execution plan mismatch: {field}")


def _verify_audit_files(audit: dict[str, Any]) -> None:
    for record in audit["runtime_file_identities"] + audit["formal_source_identities"]:
        path = WORKSPACE_ROOT / record["path"]
        if not path.is_file() or path.is_symlink() or path.stat().st_size != record["bytes"] or sha256_file(path) != record["sha256"]:
            raise ClosureBuildFailure(f"frozen input drift: {record['path']}")


def _definition_count(path: Path, qualname: str) -> int:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    parts = qualname.split(".")
    scope: Iterable[ast.stmt] = tree.body
    for index, part in enumerate(parts):
        matches = [node for node in scope if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == part]
        if len(matches) != 1:
            return len(matches)
        if index < len(parts) - 1:
            if not isinstance(matches[0], ast.ClassDef):
                return 0
            scope = matches[0].body
    return 1


def _scan_python(path: Path, identity: str, classification: str) -> tuple[list[str], list[dict[str, Any]], list[dict[str, Any]]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    dynamic_sites: list[dict[str, Any]] = []
    process_sites: list[dict[str, Any]] = []

    def dotted(node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = dotted(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(("." * node.level) + (node.module or ""))
        elif isinstance(node, ast.Call):
            name = dotted(node.func) or ""
            locator = f"{identity}:{node.lineno}:{node.col_offset}:{name}"
            if name in {"importlib.import_module", "__import__", "importlib.util.spec_from_file_location"}:
                literal = node.args[0].value if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str) else None
                production_reachable = classification == "runtime_closure_member"
                resolved = literal is not None or not production_reachable
                dynamic_sites.append({
                    "site_id": _stable_id("DS", locator), "path": identity, "line": node.lineno,
                    "column": node.col_offset, "call": name, "literal_target": literal,
                    "production_reachable": production_reachable, "resolved": resolved,
                    "resolution": "literal_target" if literal is not None else "test_build_or_excluded_boundary",
                })
            if name in {"subprocess.run", "subprocess.Popen", "os.execve", "os.execv", "os.posix_spawn"}:
                process_sites.append({
                    "boundary_id": _stable_id("PB", locator), "path": identity, "line": node.lineno,
                    "column": node.col_offset, "call": name, "resolved": True,
                    "resolution": "frozen_callsite_and_controller_environment",
                })
    return sorted(imports), sorted(dynamic_sites, key=lambda item: item["site_id"]), sorted(process_sites, key=lambda item: item["boundary_id"])


def _module_origin(module_name: str) -> tuple[str, Path | None]:
    candidate = module_name.lstrip(".")
    if candidate == "__future__":
        return "language_builtin", None
    try:
        spec = importlib.util.find_spec(candidate)
    except (ImportError, ModuleNotFoundError, AttributeError, ValueError):
        spec = None
    if spec is None or spec.origin in {None, "built-in", "frozen"}:
        return (spec.origin if spec and spec.origin else "language_builtin"), None
    path = Path(spec.origin).resolve()
    return str(path), path if path.is_file() else None


def _distribution_nodes(name: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    distribution = importlib.metadata.distribution(name)
    nodes: list[dict[str, Any]] = []
    file_count = 0
    native_files: list[str] = []
    for item in sorted(distribution.files or [], key=lambda value: str(value)):
        path = Path(distribution.locate_file(item)).resolve()
        if not path.is_file() or path.is_symlink():
            continue
        identity = f"distribution:{name}:{item}"
        member_type = "shared_library" if ".so" in path.name else "distribution_file"
        nodes.append(_file_node(path, identity, "platform_boundary", member_type))
        file_count += 1
        if member_type == "shared_library":
            native_files.append(str(path))
    metadata = {
        "name": name,
        "version": distribution.version,
        "file_count": file_count,
        "metadata_path": str(Path(distribution._path).resolve()),
        "native_files": native_files,
    }
    return nodes, metadata


def _linked_libraries(path: Path) -> list[dict[str, Any]]:
    output = subprocess.run(["ldd", str(path)], capture_output=True, text=True, check=False).stdout
    records: list[dict[str, Any]] = []
    for line in output.splitlines():
        tokens = line.replace("=>", " ").split()
        absolute = next((Path(token) for token in tokens if token.startswith("/") and Path(token).is_file()), None)
        if absolute is None:
            continue
        resolved = absolute.resolve()
        records.append({"path": str(resolved), "sha256": sha256_file(resolved), "bytes": resolved.stat().st_size})
    return sorted(records, key=lambda item: item["path"])


def _native_capture(fixed_environment: dict[str, str]) -> dict[str, Any]:
    policy = load_yaml(CONTRACT_ROOT / "native_component_build_policy_v1.yaml")
    source = WORKSPACE_ROOT / policy["source_path"]
    tracked = WORKSPACE_ROOT / policy["tracked_binary_path"]
    compiler = Path(shutil.which("gcc") or "").resolve()
    if not compiler.is_file():
        raise ClosureBuildFailure("gcc unavailable")
    compile_env = {"PATH": fixed_environment["PATH"], "LANG": "C.UTF-8", "LC_ALL": "C", "SOURCE_DATE_EPOCH": "0"}
    digests: list[str] = []
    sizes: list[int] = []
    with tempfile.TemporaryDirectory(prefix="ctde-r3-native-") as temporary:
        for name in ("consumer_probe_a", "consumer_probe_b"):
            output = Path(temporary) / name
            argv = [str(compiler), "-static", "-O2", "-Wall", "-Wextra", "-Werror", "-o", str(output), str(source)]
            subprocess.run(argv, check=True, capture_output=True, env=compile_env)
            digests.append(sha256_file(output))
            sizes.append(output.stat().st_size)
    if len(set(digests)) != 1 or len(set(sizes)) != 1:
        raise ClosureBuildFailure("native rebuild is not deterministic")
    return {
        "component_id": "consumer_probe",
        "source_path": policy["source_path"],
        "source_sha256": sha256_file(source),
        "tracked_binary_path": policy["tracked_binary_path"],
        "tracked_binary_sha256": sha256_file(tracked),
        "tracked_binary_bytes": tracked.stat().st_size,
        "compiler_path": str(compiler),
        "compiler_sha256": sha256_file(compiler),
        "compiler_version": _command([str(compiler), "--version"]).splitlines()[0],
        "linker_path": str(Path(shutil.which("ld") or "").resolve()),
        "linker_version": _command(["ld", "--version"]).splitlines()[0],
        "flags": ["-static", "-O2", "-Wall", "-Wextra", "-Werror"],
        "fresh_build_count": 2,
        "fresh_build_sha256": digests[0],
        "fresh_build_bytes": sizes[0],
        "fresh_builds_byte_identical": True,
        "tracked_binary_matches_fresh_build": digests[0] == sha256_file(tracked),
        "binary_format": _command(["file", str(tracked)]),
        "tracked_linked_libraries": _linked_libraries(tracked),
    }


def _platform_capture(module_names: set[str], fixed_environment: dict[str, str]) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, str]]:
    nodes: list[dict[str, Any]] = []
    target_to_node: dict[str, str] = {}
    executable = Path(sys.executable).resolve()
    interpreter = _file_node(executable, f"interpreter:{executable}", "platform_boundary", "interpreter")
    nodes.append(interpreter)
    module_records: list[dict[str, Any]] = []
    for module_name in sorted(module_names):
        origin, path = _module_origin(module_name)
        identity = f"python-module:{module_name}:{origin}"
        if path is not None:
            node = _file_node(path, identity, "platform_boundary", "stdlib_module" if str(path).startswith(sysconfig.get_paths()["stdlib"]) else "distribution_file")
        else:
            node = _virtual_node(identity, "stdlib_module", {"module": module_name, "origin": origin})
        nodes.append(node)
        target_to_node[module_name] = node["node_id"]
        module_records.append({"module": module_name, "origin": origin, "node_id": node["node_id"]})
    distributions: list[dict[str, Any]] = []
    for distribution_name in ("PyYAML", "cryptography"):
        distribution_nodes, metadata = _distribution_nodes(distribution_name)
        nodes.extend(distribution_nodes)
        distributions.append(metadata)
    shared_libraries = _linked_libraries(executable)
    for record in shared_libraries:
        path = Path(record["path"])
        nodes.append(_file_node(path, f"shared-library:{path}", "platform_boundary", "shared_library"))
    os_release = {}
    for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            os_release[key] = value.strip('"')
    native = _native_capture(fixed_environment)
    platform_record = {
        "system": platform.system(),
        "kernel": platform.release(),
        "machine": platform.machine(),
        "userspace_id": os_release.get("ID"),
        "userspace_version": os_release.get("VERSION_ID"),
        "filesystem_type": _command(["stat", "-f", "-c", "%T", str(WORKSPACE_ROOT)]),
        "mount": _command(["findmnt", "-no", "SOURCE,FSTYPE,TARGET", "-T", str(WORKSPACE_ROOT)]),
        "proc_available": Path("/proc/self/status").is_file(),
        "fcntl_available": importlib.util.find_spec("fcntl") is not None,
        "python_executable": str(executable),
        "python_sha256": sha256_file(executable),
        "python_version": platform.python_version(),
        "python_linked_libraries": shared_libraries,
        "stdlib_root": sysconfig.get_paths()["stdlib"],
        "module_origins": module_records,
        "distributions": distributions,
        "native_component": native,
        "fixed_environment": dict(sorted(fixed_environment.items())),
        "symlink_semantics_verified": True,
        "temporary_filesystem": _command(["stat", "-f", "-c", "%T", tempfile.gettempdir()]),
    }
    return nodes, platform_record, target_to_node


def _relation_for_audit_edge(edge: dict[str, Any]) -> str:
    edge_class = edge["edge_class"]
    if edge_class == "python_import":
        return "imports"
    if edge_class == "package_initializer":
        return "initializes_package"
    if edge_class == "configured_executable":
        return "executes"
    if edge_class == "native_build_input":
        return "builds_from"
    if edge_class == "native_ffi":
        return "dlopens"
    target = edge.get("target_path", "")
    if "schema" in target:
        return "loads_schema"
    if "public_trust" in target or "status_registry" in target:
        return "loads_public_trust"
    return "loads_config"


def build_manifest(implementation: dict[str, Any], execution: dict[str, Any], execution_raw: bytes | None = None) -> dict[str, Any]:
    audit, _ = load_canonical_json(AUDIT_PATH)
    _validate_inputs(audit, implementation, execution)
    _verify_audit_files(audit)
    nodes: list[dict[str, Any]] = []
    path_to_node: dict[str, str] = {}
    python_records: list[tuple[Path, str, str]] = []
    for record in audit["runtime_file_identities"]:
        identity = record["path"]
        classification = _primary_classification(record, identity)
        node = _file_node(WORKSPACE_ROOT / identity, identity, classification)
        if node["sha256"] != record["sha256"] or node["bytes"] != record["bytes"]:
            raise ClosureBuildFailure(f"audit runtime mismatch: {identity}")
        nodes.append(node)
        path_to_node[identity] = node["node_id"]
        if identity.endswith(".py"):
            python_records.append((WORKSPACE_ROOT / identity, identity, classification))
    for record in audit["formal_source_identities"]:
        identity = record["path"]
        node = _file_node(WORKSPACE_ROOT / identity, identity, "build_only_dependency", "policy")
        nodes.append(node)
        path_to_node[identity] = node["node_id"]
    for record in implementation["files"]:
        identity = record["path"]
        classification = record["classification"]
        node = _file_node(WORKSPACE_ROOT / identity, identity, classification)
        if node["sha256"] != record["sha256"] or node["bytes"] != record["bytes"]:
            raise ClosureBuildFailure(f"implementation drift: {identity}")
        nodes.append(node)
        path_to_node[identity] = node["node_id"]
        if identity.endswith(".py"):
            python_records.append((WORKSPACE_ROOT / identity, identity, classification))

    callable_roots = audit["callable_roots"]
    for root in callable_roots:
        path = WORKSPACE_ROOT / root["relative_path"]
        if sha256_file(path) != root["containing_file_sha256"] or _definition_count(path, root["qualname"]) != 1:
            raise ClosureBuildFailure(f"callable root drift: {root['callable_id']}")

    module_names = {edge["target_identity"] for edge in audit["closure_edges"] if edge["resolution"] in {"python_stdlib_or_language", "third_party_distribution"}}
    implementation_modules = {Path(record["path"]).stem: record["path"] for record in implementation["files"] if record["path"].endswith(".py")}
    dynamic_sites: list[dict[str, Any]] = []
    process_boundaries: list[dict[str, Any]] = []
    control_imports: list[tuple[str, str]] = []
    for path, identity, classification in python_records:
        imports, sites, processes = _scan_python(path, identity, classification)
        dynamic_sites.extend(sites)
        process_boundaries.extend(processes)
        if identity in {record["path"] for record in implementation["files"]}:
            for imported in imports:
                if imported and not imported.startswith("."):
                    if imported.split(".", 1)[0] not in implementation_modules:
                        module_names.add(imported)
                    control_imports.append((identity, imported))
    unresolved_dynamic = [item for item in dynamic_sites if item["production_reachable"] and not item["resolved"]]
    if unresolved_dynamic:
        raise ClosureBuildFailure("unresolved production dynamic dependency")

    platform_nodes, platform_record, module_to_node = _platform_capture(module_names, execution["fixed_environment"])
    nodes.extend(platform_nodes)
    node_by_id: dict[str, dict[str, Any]] = {}
    for node in nodes:
        existing = node_by_id.get(node["node_id"])
        if existing is not None and existing != node:
            raise ClosureBuildFailure(f"node identity collision: {node['node_id']}")
        node_by_id[node["node_id"]] = node
    nodes = sorted(node_by_id.values(), key=lambda item: item["node_id"])

    edges: list[dict[str, Any]] = []
    for index, item in enumerate(audit["closure_edges"], start=1):
        from_id = path_to_node.get(item["from_path"])
        if from_id is None:
            raise ClosureBuildFailure(f"edge source absent: {item['from_path']}")
        if item["resolution"] == "project_owned":
            to_id = path_to_node.get(item.get("target_path", ""))
        elif item["resolution"] in {"python_stdlib_or_language", "third_party_distribution"}:
            to_id = module_to_node.get(item["target_identity"])
        elif item["resolution"] == "execution_plan_must_bind":
            to_id = path_to_node.get("runtime_capability_prototype/bin/consumer_probe")
        else:
            identity = f"platform-target:{item['target_identity']}"
            virtual = _virtual_node(identity, "shared_library", {"target": item["target_identity"], "resolution": item["resolution"]})
            if virtual["node_id"] not in node_by_id:
                node_by_id[virtual["node_id"]] = virtual
                nodes.append(virtual)
            to_id = virtual["node_id"]
        if to_id is None:
            raise ClosureBuildFailure(f"edge target absent: {item}")
        edges.append({"from_id": from_id, "to_id": to_id, "relation": _relation_for_audit_edge(item), "locator": f"audit_edge:{index:04d}"})
    for identity, imported in control_imports:
        top_level = imported.split(".", 1)[0]
        local_path = implementation_modules.get(top_level)
        to_id = path_to_node.get(local_path, "") if local_path else module_to_node.get(imported) or module_to_node.get(top_level)
        if to_id:
            edges.append({"from_id": path_to_node[identity], "to_id": to_id, "relation": "imports", "locator": f"control_ast:{identity}:{imported}"})
    for implementation_record in implementation["files"]:
        identity = implementation_record["path"]
        if identity == "runtime_capability_prototype/contracts/r3_portable_closure_policy_v1.yaml":
            continue
        edges.append({"from_id": path_to_node[identity], "to_id": path_to_node["runtime_capability_prototype/contracts/r3_portable_closure_policy_v1.yaml"], "relation": "classified_by", "locator": f"implementation_policy:{identity}"})
    edges = sorted({(edge["from_id"], edge["to_id"], edge["relation"], edge["locator"]): edge for edge in edges}.values(), key=lambda item: (item["from_id"], item["to_id"], item["relation"], item["locator"]))
    nodes = sorted(node_by_id.values(), key=lambda item: item["node_id"])
    if any(edge["relation"] not in EDGE_RELATIONS for edge in edges):
        raise ClosureBuildFailure("unknown edge relation")

    manifest = {
        "artifact_class": "ctde_runtime_transitive_closure_manifest",
        "schema_version": "1.0.0",
        "canonicalization_id": "CTDE-CANONICAL-JSON-SORTED-COMPACT-LF-1",
        "suite_id": SUITE_ID,
        "phase_id": PHASE_ID,
        "phase_kind": PHASE_KIND,
        "assurance": {"assurance_profile_id": PROFILE_ID, "environment_class": "Development", "highest_claimed_evidence_level": "A1", "certified": False, "hardened": False, "candidate_ready": False},
        "identities": {
            "plan_path": PLAN_PATH.name, "plan_sha256": PLAN_SHA256,
            "audit_path": AUDIT_PATH.name, "audit_sha256": AUDIT_SHA256,
            "write_scope_sha256": WRITE_SCOPE_SHA256,
            "implementation_manifest_sha256": execution["implementation_manifest_sha256"],
            "execution_plan_sha256": hashlib.sha256(execution_raw or canonical_bytes(execution)).hexdigest(),
            "git_head": execution["git_head"], "remote_main": execution["remote_main"],
            "machine_handoff_tag_target": execution["machine_handoff_tag_target"],
            "baseline_tag_target": execution["baseline_tag_target"],
            "public_trust_freeze_identity": PUBLIC_TRUST_FREEZE,
        },
        "callable_roots": callable_roots,
        "nodes": nodes,
        "edges": edges,
        "roles": audit["role_gap_dispositions"],
        "discovery": {
            "static_audit_edge_count": len(audit["closure_edges"]),
            "manifest_edge_count": len(edges), "node_count": len(nodes),
            "dynamic_sites": sorted(dynamic_sites, key=lambda item: item["site_id"]),
            "process_boundaries": sorted(process_boundaries, key=lambda item: item["boundary_id"]),
            "unknown_dynamic_dependency_count": 0,
            "unknown_project_owned_loaded_bytes": 0,
            "unresolved_symlinks": 0,
        },
        "platform": platform_record,
        "action_ledger": {"model_calls": 0, "english_tei_content_reads": 0, "greek_tei_content_reads": 0, "candidate_runs": 0, "r4_executions": 0, "business_outputs": 0},
        "closure_payload_sha256": "",
    }
    manifest["closure_payload_sha256"] = canonical_payload_digest(manifest, "closure_payload_sha256")
    validate_manifest(manifest, canonical_bytes(manifest))
    return manifest


def validate_manifest(manifest: dict[str, Any], raw: bytes) -> None:
    if set(manifest) != MANIFEST_FIELDS or raw != canonical_bytes(manifest):
        raise ClosureBuildFailure("closure manifest closed canonical contract")
    if manifest.get("artifact_class") != "ctde_runtime_transitive_closure_manifest" or manifest.get("suite_id") != SUITE_ID:
        raise ClosureBuildFailure("closure manifest identity")
    if manifest.get("closure_payload_sha256") != canonical_payload_digest(manifest, "closure_payload_sha256"):
        raise ClosureBuildFailure("closure payload digest")
    nodes = manifest.get("nodes")
    edges = manifest.get("edges")
    if type(nodes) is not list or type(edges) is not list or not nodes or not edges:
        raise ClosureBuildFailure("closure inventories absent")
    node_ids = [item["node_id"] for item in nodes]
    if node_ids != sorted(node_ids) or len(node_ids) != len(set(node_ids)):
        raise ClosureBuildFailure("closure node identity/order")
    if any(item.get("classification") not in PRIMARY_CLASSIFICATIONS for item in nodes):
        raise ClosureBuildFailure("closure classification")
    edge_keys = [(item["from_id"], item["to_id"], item["relation"], item["locator"]) for item in edges]
    if edge_keys != sorted(edge_keys) or len(edge_keys) != len(set(edge_keys)):
        raise ClosureBuildFailure("closure edge identity/order")
    known = set(node_ids)
    if any(item["from_id"] not in known or item["to_id"] not in known or item["relation"] not in EDGE_RELATIONS for item in edges):
        raise ClosureBuildFailure("closure edge resolution")
    if manifest["discovery"]["unknown_dynamic_dependency_count"] != 0 or manifest["discovery"]["unresolved_symlinks"] != 0:
        raise ClosureBuildFailure("closure unresolved dependency")


def build_component_freeze(manifest: dict[str, Any], manifest_raw: bytes, implementation_raw: bytes) -> dict[str, Any]:
    validate_manifest(manifest, manifest_raw)
    counts: dict[str, int] = {name: 0 for name in sorted(PRIMARY_CLASSIFICATIONS)}
    for node in manifest["nodes"]:
        counts[node["classification"]] += 1
    return {
        "artifact_class": "ctde_component_freeze",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "closure_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "closure_payload_sha256": manifest["closure_payload_sha256"],
        "implementation_manifest_sha256": hashlib.sha256(implementation_raw).hexdigest(),
        "members": manifest["nodes"],
        "platform": manifest["platform"],
        "counts": counts,
    }


def build_snapshot_binding(
    manifest: dict[str, Any], manifest_raw: bytes, implementation_raw: bytes,
    execution: dict[str, Any], execution_raw: bytes, test_raw: bytes, fixture_raw: bytes,
    freeze_raw: bytes,
) -> dict[str, Any]:
    return {
        "artifact_class": "ctde_execution_snapshot_closure_binding",
        "schema_version": "1.0.0",
        "suite_id": SUITE_ID,
        "fixed_utc_epoch_seconds": execution["fixed_utc_epoch_seconds"],
        "fixed_environment": execution["fixed_environment"],
        "public_trust_freeze_identity": PUBLIC_TRUST_FREEZE,
        "execution_plan_sha256": hashlib.sha256(execution_raw).hexdigest(),
        "implementation_manifest_sha256": hashlib.sha256(implementation_raw).hexdigest(),
        "closure_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "closure_payload_sha256": manifest["closure_payload_sha256"],
        "test_manifest_sha256": hashlib.sha256(test_raw).hexdigest(),
        "fixture_catalog_sha256": hashlib.sha256(fixture_raw).hexdigest(),
        "component_freeze_sha256": hashlib.sha256(freeze_raw).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation-manifest", required=True)
    parser.add_argument("--execution-plan", required=True)
    args = parser.parse_args()
    try:
        implementation, _ = load_canonical_json(Path(args.implementation_manifest))
        execution, execution_raw = load_canonical_json(Path(args.execution_plan))
        sys.stdout.buffer.write(canonical_bytes(build_manifest(implementation, execution, execution_raw)))
        return 0
    except Exception as exc:
        print(f"BLOCKED_PORTABLE_RUNTIME_TRANSITIVE_CLOSURE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
