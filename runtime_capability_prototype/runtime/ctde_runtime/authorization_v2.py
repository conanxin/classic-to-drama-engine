from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import re
from dataclasses import dataclass, replace
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Mapping

import yaml

from .common import PrototypeError, load_yaml, require, sha256_bytes


SCHEMA_ID = "urn:ctde:schema:runtime-authorization:2"
SCHEMA_VERSION = "2.0.0"
PORTABLE_PROFILE = "CTDE-PORTABLE-DEV-1"
HARDENED_PROFILE = "CTDE-HARDENED-CERT-1"
DENIED_POLICY_VERSION = "CTDE-DENIED-CAPABILITIES-1"
DENIED_CAPABILITIES = (
    "direct_source_open",
    "raw_path_disclosure",
    "caller_supplied_range_override",
    "unbounded_read",
    "read_to_eof",
    "automatic_retry",
    "second_source",
    "network_source_fetch",
    "unapproved_output_write",
    "authorization_inheritance",
    "authorization_replay",
    "profile_promotion",
)
LEGACY_OR_SELF_DIGEST_FIELDS = frozenset(
    {
        "authorization_file_sha256",
        "authorization_artifact_sha256",
        "self_digest",
        "file_digest",
        "attempt_id",
        "fixture_object_id",
        "fixture_structure_contract_id",
        "allowed_range",
        "forbidden_source_roles",
        "initial_state",
    }
)
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RFC3339_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

TOP_FIELDS = frozenset(
    {
        "schema_version",
        "artifact_class",
        "assurance_profile_id",
        "authorization_id",
        "run_id",
        "source_id",
        "source_snapshot_id",
        "source_snapshot_sha256",
        "structure_map_id",
        "structure_map_file_sha256",
        "mapping_payload_canonicalization_id",
        "mapping_payload_sha256",
        "task_scope",
        "allowed_ranges",
        "allowed_consumer",
        "allowed_outputs",
        "denied_capability_policy_version",
        "denied_capabilities",
        "issuer",
        "issued_at",
        "expires_at",
        "nonce",
        "one_time",
        "automatic_retry_allowed",
        "authorization_inheritable",
        "authorization_state",
    }
)


class _UniqueKeySafeLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(loader: yaml.Loader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if type(key) is not str:
            raise PrototypeError("BLOCKED_AUTHORIZATION_SCHEMA_INVALID", "mapping key must be string")
        if key in mapping:
            raise PrototypeError("BLOCKED_AUTHORIZATION_SCHEMA_INVALID", f"duplicate key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _schema_invalid(detail: str) -> None:
    raise PrototypeError("BLOCKED_AUTHORIZATION_SCHEMA_INVALID", detail)


def _closed_object(value: Any, fields: set[str], name: str) -> dict[str, Any]:
    if type(value) is not dict:
        _schema_invalid(f"{name} must be object")
    if set(value) != fields:
        missing = sorted(fields - set(value))
        extra = sorted(set(value) - fields)
        _schema_invalid(f"{name} fields missing={missing} extra={extra}")
    return value


def _id(value: Any, name: str) -> str:
    if type(value) is not str or ID_RE.fullmatch(value) is None:
        _schema_invalid(f"{name} invalid id")
    return value


def _sha(value: Any, name: str) -> str:
    if type(value) is not str or SHA256_RE.fullmatch(value) is None:
        _schema_invalid(f"{name} invalid sha256")
    return value


def parse_rfc3339_utc(value: Any, name: str) -> dt.datetime:
    if type(value) is not str or RFC3339_RE.fullmatch(value) is None:
        raise PrototypeError("BLOCKED_AUTHORIZATION_TIME_INVALID", f"{name} must be quoted RFC3339 UTC")
    try:
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError as exc:
        raise PrototypeError("BLOCKED_AUTHORIZATION_TIME_INVALID", name) from exc


def _validate_json_compatible(value: Any, path: str = "$") -> None:
    if value is None or type(value) in {str, bool, int}:
        return
    if type(value) is float:
        _schema_invalid(f"float forbidden at {path}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_compatible(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if type(key) is not str:
                _schema_invalid(f"non-string key at {path}")
            _validate_json_compatible(item, f"{path}.{key}")
        return
    _schema_invalid(f"non JSON-compatible type at {path}: {type(value).__name__}")


def _reject_unsafe_yaml(exact_bytes: bytes) -> str:
    if exact_bytes.startswith(b"\xef\xbb\xbf"):
        _schema_invalid("BOM forbidden")
    try:
        text = exact_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PrototypeError("BLOCKED_AUTHORIZATION_SCHEMA_INVALID", "UTF-8 required") from exc
    try:
        tokens = list(yaml.scan(text, Loader=_UniqueKeySafeLoader))
    except PrototypeError:
        raise
    except Exception as exc:
        raise PrototypeError("BLOCKED_AUTHORIZATION_SCHEMA_INVALID", "malformed YAML") from exc
    forbidden_tokens = (yaml.tokens.AnchorToken, yaml.tokens.AliasToken, yaml.tokens.TagToken)
    if any(isinstance(token, forbidden_tokens) for token in tokens):
        _schema_invalid("anchors, aliases and custom tags forbidden")
    if "<<:" in text:
        _schema_invalid("merge key forbidden")
    return text


@dataclass(frozen=True)
class AuthorizationArtifactV2:
    claims: Mapping[str, Any]
    exact_bytes: bytes
    artifact_sha256: str
    size_bytes: int

    def plain_claims(self) -> dict[str, Any]:
        return _plain(self.claims)


@dataclass(frozen=True)
class AuthorizationRegistryIdentityV2:
    registry_record_id: str
    authorization_id: str
    schema_id: str
    schema_version: str
    assurance_profile_id: str
    run_id: str
    source_id: str
    source_snapshot_id: str
    structure_map_id: str
    nonce: str
    authorization_artifact_sha256: str
    authorization_artifact_size_bytes: int
    registered_at: str


@dataclass(frozen=True)
class AuthorizationRegistryStateV2:
    registry_record_id: str
    consumption_state: str
    state_version: int
    consumption_event_id: str | None
    last_state_event_id: str | None
    state_changed_at: str
    terminal_reason: str | None
    mint_eligibility_state: str
    mint_eligibility_handle_sha256: str | None
    mint_eligibility_event_id: str | None
    mint_claimed: bool
    mint_claim_event_id: str | None
    capability_preparation_state: str
    preparation_handle_sha256: str | None
    pending_capability_id: str | None
    pending_capability_artifact_sha256: str | None
    capability_preparation_event_id: str | None
    capability_activation_state: str
    activation_handle_sha256: str | None
    active_capability_id: str | None
    capability_activation_event_id: str | None
    activation_commit_a1_event_sha256: str | None


@dataclass(frozen=True)
class PreConsumeAuthorizationContextV2:
    artifact: AuthorizationArtifactV2
    identity: AuthorizationRegistryIdentityV2
    state: AuthorizationRegistryStateV2


@dataclass(frozen=True)
class PostConsumeMintContextV2:
    artifact: AuthorizationArtifactV2
    identity: AuthorizationRegistryIdentityV2
    state: AuthorizationRegistryStateV2
    consume_operation_id: str
    eligibility_handle: bytes


@dataclass(frozen=True)
class PostMintLeaseContextV2:
    artifact: AuthorizationArtifactV2
    identity: AuthorizationRegistryIdentityV2
    state: AuthorizationRegistryStateV2
    consume_operation_id: str
    preparation_handle: bytes


@dataclass(frozen=True)
class PreparedCapabilityContextV2:
    artifact: AuthorizationArtifactV2
    identity: AuthorizationRegistryIdentityV2
    state: AuthorizationRegistryStateV2
    consume_operation_id: str
    activation_handle: bytes


@dataclass(frozen=True)
class ActivatedAuthorizationContextV2:
    artifact: AuthorizationArtifactV2
    identity: AuthorizationRegistryIdentityV2
    state: AuthorizationRegistryStateV2
    consume_operation_id: str


def load_authorization_v2(exact_bytes: bytes, schema_path: Path) -> AuthorizationArtifactV2:
    schema = load_yaml(schema_path)
    require(isinstance(schema, dict), "BLOCKED_AUTHORIZATION_SCHEMA_INVALID", "schema artifact")
    require(schema.get("$id") == SCHEMA_ID, "BLOCKED_AUTHORIZATION_SCHEMA_INVALID", "schema id")
    require(set(schema.get("required", [])) == TOP_FIELDS, "BLOCKED_AUTHORIZATION_SCHEMA_INVALID", "schema required set")
    text = _reject_unsafe_yaml(exact_bytes)
    try:
        documents = list(yaml.load_all(text, Loader=_UniqueKeySafeLoader))
    except PrototypeError:
        raise
    except Exception as exc:
        raise PrototypeError("BLOCKED_AUTHORIZATION_SCHEMA_INVALID", "malformed YAML") from exc
    if len(documents) != 1 or type(documents[0]) is not dict:
        _schema_invalid("exactly one mapping document required")
    claims = documents[0]
    _validate_json_compatible(claims)
    version = claims.get("schema_version")
    if version != SCHEMA_VERSION:
        raise PrototypeError("BLOCKED_AUTHORIZATION_SCHEMA_VERSION_UNSUPPORTED", str(version))
    if "assurance_profile_id" not in claims:
        raise PrototypeError("BLOCKED_AUTHORIZATION_PROFILE_MISMATCH", "missing profile")
    legacy = sorted(set(claims) & LEGACY_OR_SELF_DIGEST_FIELDS)
    if legacy:
        _schema_invalid(f"legacy/self-digest fields forbidden: {legacy}")
    _closed_object(claims, set(TOP_FIELDS), "authorization")
    if claims["artifact_class"] != "ctde_runtime_authorization":
        _schema_invalid("artifact_class")
    if claims["assurance_profile_id"] not in {PORTABLE_PROFILE, HARDENED_PROFILE}:
        _schema_invalid("assurance_profile_id")
    for name in ("authorization_id", "run_id", "source_id", "source_snapshot_id", "structure_map_id"):
        _id(claims[name], name)
    for name in (
        "source_snapshot_sha256",
        "structure_map_file_sha256",
        "mapping_payload_sha256",
        "nonce",
    ):
        _sha(claims[name], name)
    if claims["mapping_payload_canonicalization_id"] != "CTDE-MAP-C14N-1":
        _schema_invalid("mapping canonicalization")

    task = _closed_object(
        claims["task_scope"],
        {"task_scope_id", "task_type", "task_scope_sha256", "selected_source_units", "max_invocations", "automatic_retries"},
        "task_scope",
    )
    _id(task["task_scope_id"], "task_scope_id")
    _id(task["task_type"], "task_type")
    _sha(task["task_scope_sha256"], "task_scope_sha256")
    units = task["selected_source_units"]
    if type(units) is not list or not units or len(units) != len(set(units)):
        _schema_invalid("selected_source_units")
    for unit in units:
        _id(unit, "selected_source_unit")
    if type(task["max_invocations"]) is not int or task["max_invocations"] < 0:
        _schema_invalid("max_invocations")
    if type(task["automatic_retries"]) is not int or task["automatic_retries"] != 0:
        _schema_invalid("automatic_retries")

    ranges = claims["allowed_ranges"]
    if type(ranges) is not list or len(ranges) != 1:
        _schema_invalid("allowed_ranges must contain exactly one range")
    item = _closed_object(
        ranges[0],
        {"range_id", "start_byte", "end_byte_exclusive", "expected_length", "expected_slice_sha256"},
        "allowed_ranges[0]",
    )
    _id(item["range_id"], "range_id")
    for name in ("start_byte", "end_byte_exclusive", "expected_length"):
        if type(item[name]) is not int:
            _schema_invalid(name)
    if item["start_byte"] < 0 or item["end_byte_exclusive"] <= item["start_byte"]:
        _schema_invalid("range ordering")
    if item["expected_length"] != item["end_byte_exclusive"] - item["start_byte"]:
        _schema_invalid("expected_length")
    _sha(item["expected_slice_sha256"], "expected_slice_sha256")

    consumer = _closed_object(
        claims["allowed_consumer"],
        {"consumer_id", "consumer_role", "component_id", "component_version", "component_identity_artifact_sha256"},
        "allowed_consumer",
    )
    for name in ("consumer_id", "consumer_role", "component_id", "component_version"):
        _id(consumer[name], name)
    _sha(consumer["component_identity_artifact_sha256"], "component_identity_artifact_sha256")

    outputs = claims["allowed_outputs"]
    if type(outputs) is not list:
        _schema_invalid("allowed_outputs")
    seen_outputs: set[tuple[str, str]] = set()
    for index, output in enumerate(outputs):
        output = _closed_object(output, {"artifact_class", "relative_path", "writer_component_id", "max_count"}, f"allowed_outputs[{index}]")
        _id(output["artifact_class"], "output artifact_class")
        _id(output["writer_component_id"], "writer_component_id")
        path = output["relative_path"]
        if type(path) is not str or path != path.strip() or not path or "\\" in path or "\x00" in path or any(ch in path for ch in "*?[]"):
            _schema_invalid("output relative_path")
        pure = PurePosixPath(path)
        if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts) or str(pure) != path:
            _schema_invalid("output relative_path canonicality")
        if type(output["max_count"]) is not int or output["max_count"] <= 0:
            _schema_invalid("output max_count")
        key = (output["artifact_class"], path)
        if key in seen_outputs:
            _schema_invalid("duplicate allowed output")
        seen_outputs.add(key)

    if claims["denied_capability_policy_version"] != DENIED_POLICY_VERSION:
        _schema_invalid("denied policy version")
    if claims["denied_capabilities"] != list(DENIED_CAPABILITIES):
        _schema_invalid("denied capability set/order")
    issuer = _closed_object(claims["issuer"], {"authority_id", "approval_evidence_ref", "approval_evidence_sha256"}, "issuer")
    _id(issuer["authority_id"], "authority_id")
    _id(issuer["approval_evidence_ref"], "approval_evidence_ref")
    _sha(issuer["approval_evidence_sha256"], "approval_evidence_sha256")

    issued = parse_rfc3339_utc(claims["issued_at"], "issued_at")
    expires = parse_rfc3339_utc(claims["expires_at"], "expires_at")
    if expires <= issued:
        raise PrototypeError("BLOCKED_AUTHORIZATION_TIME_INVALID", "expires_at must be after issued_at")
    if claims["one_time"] is not True or claims["automatic_retry_allowed"] is not False or claims["authorization_inheritable"] is not False:
        _schema_invalid("one-time/retry/inheritance flags")
    if claims["authorization_state"] != "approved":
        _schema_invalid("authorization_state")

    return AuthorizationArtifactV2(
        claims=_freeze(claims),
        exact_bytes=bytes(exact_bytes),
        artifact_sha256=sha256_bytes(exact_bytes),
        size_bytes=len(exact_bytes),
    )


def handle_digest(domain: str, secret: bytes) -> str:
    require(len(secret) == 32, "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH", "handle length")
    return hashlib.sha256(domain.encode("ascii") + b"\x00" + secret).hexdigest()


def compare_handle(domain: str, secret: bytes, expected: str | None) -> bool:
    if expected is None or len(secret) != 32:
        return False
    return hmac.compare_digest(handle_digest(domain, secret), expected)


def validate_request_binding(claims: Mapping[str, Any], request: Mapping[str, Any]) -> None:
    required = {
        "run_id",
        "source_id",
        "source_snapshot_id",
        "structure_map_id",
        "task_scope_id",
        "task_type",
        "requested_range",
        "consumer_id",
        "component_id",
        "requested_output",
        "requested_capability",
        "assurance_profile_id",
        "nonce",
    }
    require(set(request) == required, "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH", "request shape")
    require(request["run_id"] == claims["run_id"], "BLOCKED_AUTHORIZATION_RUN_MISMATCH")
    require(request["assurance_profile_id"] == claims["assurance_profile_id"], "BLOCKED_AUTHORIZATION_PROFILE_MISMATCH")
    require(request["nonce"] == claims["nonce"], "BLOCKED_AUTHORIZATION_NONCE_MISMATCH")
    if request["source_id"] != claims["source_id"] or request["source_snapshot_id"] != claims["source_snapshot_id"]:
        raise PrototypeError("BLOCKED_AUTHORIZATION_SOURCE_MISMATCH")
    require(request["structure_map_id"] == claims["structure_map_id"], "BLOCKED_AUTHORIZATION_STRUCTURE_MAP_MISMATCH")
    task = claims["task_scope"]
    if request["task_scope_id"] != task["task_scope_id"] or request["task_type"] != task["task_type"]:
        raise PrototypeError("BLOCKED_AUTHORIZATION_TASK_SCOPE_MISMATCH")
    expected_range = claims["allowed_ranges"][0]
    if dict(request["requested_range"]) != dict(expected_range):
        raise PrototypeError("BLOCKED_AUTHORIZATION_RANGE_EXCEEDED")
    consumer = claims["allowed_consumer"]
    if request["consumer_id"] != consumer["consumer_id"] or request["component_id"] != consumer["component_id"]:
        raise PrototypeError("BLOCKED_AUTHORIZATION_CONSUMER_MISMATCH")
    requested_output = request["requested_output"]
    allowed_outputs = [dict(item) for item in claims["allowed_outputs"]]
    if requested_output is not None and dict(requested_output) not in allowed_outputs:
        raise PrototypeError("BLOCKED_AUTHORIZATION_OUTPUT_NOT_ALLOWED")
    requested_capability = request["requested_capability"]
    if requested_capability is not None and requested_capability in claims["denied_capabilities"]:
        raise PrototypeError("BLOCKED_AUTHORIZATION_CAPABILITY_DENIED")


def validate_activated_projection(context: Any, *, expected_consumer_id: str, expected_component_id: str) -> dict[str, Any]:
    require(isinstance(context, ActivatedAuthorizationContextV2), "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
    claims = context.artifact.claims
    state = context.state
    require(context.identity.assurance_profile_id == claims["assurance_profile_id"], "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
    require(context.identity.run_id == claims["run_id"], "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
    require(context.identity.nonce == claims["nonce"], "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
    require(state.consumption_state == "spent", "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
    require(state.mint_eligibility_state == "claimed" and state.mint_claimed, "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
    require(state.capability_preparation_state == "prepared", "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
    require(state.capability_activation_state == "activated", "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
    require(state.consumption_event_id is not None and state.mint_claim_event_id is not None, "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
    require(state.capability_preparation_event_id is not None and state.capability_activation_event_id is not None, "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
    require(state.active_capability_id == state.pending_capability_id and state.active_capability_id is not None, "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
    consumer = claims["allowed_consumer"]
    require(consumer["consumer_id"] == expected_consumer_id and consumer["component_id"] == expected_component_id, "BLOCKED_AUTHORIZATION_CONSUMER_MISMATCH")
    return {
        "assurance_profile_id": claims["assurance_profile_id"],
        "run_id": claims["run_id"],
        "authorization_id": claims["authorization_id"],
        "authorization_artifact_sha256": context.identity.authorization_artifact_sha256,
        "authorization_nonce": claims["nonce"],
        "consumption_event_id": state.consumption_event_id,
        "mint_claim_event_id": state.mint_claim_event_id,
        "capability_preparation_event_id": state.capability_preparation_event_id,
        "capability_activation_event_id": state.capability_activation_event_id,
        "capability_id": state.active_capability_id,
    }
