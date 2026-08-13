from __future__ import annotations

import datetime as dt
import hashlib
import inspect
import json
import re
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import yaml
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .common import PrototypeError, canonical_json_bytes, sha256_file
from .signing import JWSCodec, KeyRecord, TrustStore


ASSURANCE_PROFILE_ID = "CTDE-PORTABLE-DEV-1"
TRUST_DOMAIN = "ctde-portable-runtime"
CANONICALIZATION_ID = "CTDE-PUBLIC-TRUST-JCS-1"
AUTHORIZED_FIXED_UTC_EPOCH_SECONDS = 1786597200
BLOCKER = "BLOCKED_PUBLIC_TRUST_INVALID"

_PROTOTYPE_ROOT = Path(__file__).resolve().parents[2]
_CONTRACT_ROOT = _PROTOTYPE_ROOT / "contracts"
_MATERIAL_SCHEMA_NAME = "public_trust_material_schema_v1.yaml"
_STATUS_SCHEMA_NAME = "public_key_status_registry_schema_v1.yaml"
_MATERIAL_NAME = "portable_public_trust_material_v1.json"
_STATUS_NAME = "portable_public_key_status_registry_v1.json"

_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_HEX_KEY_RE = re.compile(r"^[0-9a-f]{64}$")
_UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

_MATERIAL_TOP_FIELDS = {
    "schema_version",
    "artifact_class",
    "assurance_profile_id",
    "trust_domain",
    "canonicalization_id",
    "keys",
}
_MATERIAL_KEY_FIELDS = {
    "kid",
    "jws_alg",
    "key_algorithm",
    "public_key_encoding",
    "public_key_hex",
    "public_key_bytes_sha256",
}
_STATUS_TOP_FIELDS = {
    "schema_version",
    "artifact_class",
    "assurance_profile_id",
    "trust_domain",
    "canonicalization_id",
    "material_path",
    "material_sha256",
    "keys",
}
_STATUS_KEY_FIELDS = {
    "kid",
    "jws_alg",
    "key_algorithm",
    "status",
    "trust_domain",
    "not_before",
    "expires_at",
}
_STATUS_VALUES = {"active", "revoked", "expired", "disabled"}


class _UniqueSafeLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader: yaml.Loader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if type(key) is not str or key in result:
            raise PrototypeError(BLOCKER, "schema duplicate or non-string key")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


def _fail(detail: str) -> None:
    raise PrototypeError(BLOCKER, detail)


def _closed(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != fields:
        _fail(f"{label} closed fields")
    return value


def _validate_json_types(value: Any, label: str = "$") -> None:
    if type(value) is str or type(value) is int:
        return
    if type(value) is list:
        for index, item in enumerate(value):
            _validate_json_types(item, f"{label}[{index}]")
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                _fail(f"non-string key at {label}")
            _validate_json_types(item, f"{label}.{key}")
        return
    _fail(f"forbidden JSON type at {label}")


def _parse_json_exact(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n") or raw.count(b"\n") != 1:
        _fail(f"{path.name} encoding")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PrototypeError(BLOCKER, f"{path.name} UTF-8") from exc

    def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                _fail(f"{path.name} duplicate key")
            result[key] = value
        return result

    try:
        value = json.loads(text, object_pairs_hook=unique_pairs)
    except PrototypeError:
        raise
    except Exception as exc:
        raise PrototypeError(BLOCKER, f"{path.name} malformed JSON") from exc
    if type(value) is not dict:
        _fail(f"{path.name} top-level object")
    _validate_json_types(value)
    expected = canonical_json_bytes(value) + b"\n"
    if raw != expected:
        _fail(f"{path.name} noncanonical bytes")
    return value, raw


def _parse_schema(path: Path, expected_id: str, expected_required: set[str]) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        _fail(f"{path.name} encoding")
    text = raw.decode("utf-8")
    try:
        tokens = list(yaml.scan(text, Loader=_UniqueSafeLoader))
        if any(isinstance(token, (yaml.tokens.AnchorToken, yaml.tokens.AliasToken, yaml.tokens.TagToken)) for token in tokens):
            _fail(f"{path.name} unsafe YAML")
        if "<<:" in text:
            _fail(f"{path.name} merge key")
        value = yaml.load(text, Loader=_UniqueSafeLoader)
    except PrototypeError:
        raise
    except Exception as exc:
        raise PrototypeError(BLOCKER, f"{path.name} malformed YAML") from exc
    if type(value) is not dict or value.get("$id") != expected_id:
        _fail(f"{path.name} schema identity")
    if value.get("type") != "object" or value.get("additionalProperties") is not False:
        _fail(f"{path.name} schema closure")
    if set(value.get("required", [])) != expected_required:
        _fail(f"{path.name} required fields")
    return value, hashlib.sha256(raw).hexdigest()


def _utc_epoch(value: Any, label: str) -> int:
    if type(value) is not str or _UTC_RE.fullmatch(value) is None:
        _fail(f"{label} UTC format")
    try:
        parsed = dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    except ValueError as exc:
        raise PrototypeError(BLOCKER, f"{label} UTC value") from exc
    return int(parsed.timestamp())


@dataclass(frozen=True)
class PublicTrustRecordIdentity:
    kid: str
    jws_alg: str
    key_algorithm: str
    public_key_bytes_sha256: str
    status: str
    trust_domain: str
    not_before: str
    expires_at: str


@dataclass(frozen=True)
class LoadedPublicTrust:
    store: TrustStore
    assurance_profile_id: str
    trust_domain: str
    material_schema_sha256: str
    status_schema_sha256: str
    material_sha256: str
    status_registry_sha256: str
    loader_sha256: str
    signing_sha256: str
    semantic_payload_sha256: str
    records: tuple[PublicTrustRecordIdentity, ...]
    public_trust_freeze_identity: str

    def codec(self, now: int) -> JWSCodec:
        if type(now) is not int or now != AUTHORIZED_FIXED_UTC_EPOCH_SECONDS:
            _fail("fixed UTC epoch mismatch")
        return JWSCodec(self.store, now)


def _load_from_contract_root(contract_root: Path) -> LoadedPublicTrust:
    material_schema_path = contract_root / _MATERIAL_SCHEMA_NAME
    status_schema_path = contract_root / _STATUS_SCHEMA_NAME
    material_path = contract_root / _MATERIAL_NAME
    status_path = contract_root / _STATUS_NAME
    for path in (material_schema_path, status_schema_path, material_path, status_path):
        if not path.is_file() or path.is_symlink():
            _fail(f"missing or non-regular input: {path.name}")

    _, material_schema_sha = _parse_schema(
        material_schema_path,
        "urn:ctde:schema:portable-public-trust-material:1",
        _MATERIAL_TOP_FIELDS,
    )
    _, status_schema_sha = _parse_schema(
        status_schema_path,
        "urn:ctde:schema:portable-public-key-status-registry:1",
        _STATUS_TOP_FIELDS,
    )
    material, material_raw = _parse_json_exact(material_path)
    status, status_raw = _parse_json_exact(status_path)
    _closed(material, _MATERIAL_TOP_FIELDS, "material")
    _closed(status, _STATUS_TOP_FIELDS, "status registry")

    if (
        material["schema_version"] != "1.0.0"
        or material["artifact_class"] != "ctde_portable_public_trust_material"
        or material["assurance_profile_id"] != ASSURANCE_PROFILE_ID
        or material["trust_domain"] != TRUST_DOMAIN
        or material["canonicalization_id"] != CANONICALIZATION_ID
    ):
        _fail("material identity")
    if (
        status["schema_version"] != "1.0.0"
        or status["artifact_class"] != "ctde_portable_public_key_status_registry"
        or status["assurance_profile_id"] != ASSURANCE_PROFILE_ID
        or status["trust_domain"] != TRUST_DOMAIN
        or status["canonicalization_id"] != CANONICALIZATION_ID
        or status["material_path"] != _MATERIAL_NAME
    ):
        _fail("status registry identity")
    material_sha = hashlib.sha256(material_raw).hexdigest()
    if status["material_sha256"] != material_sha:
        _fail("status-to-material digest")

    material_keys = material["keys"]
    status_keys = status["keys"]
    if type(material_keys) is not list or type(status_keys) is not list or not material_keys:
        _fail("non-empty key set")
    if len(material_keys) != len(status_keys):
        _fail("material/status key-set size")

    material_by_kid: dict[str, dict[str, Any]] = {}
    for item in material_keys:
        item = _closed(item, _MATERIAL_KEY_FIELDS, "material key")
        kid = item["kid"]
        if type(kid) is not str or _ID_RE.fullmatch(kid) is None or kid in material_by_kid:
            _fail("material kid")
        if item["jws_alg"] != "EdDSA" or item["key_algorithm"] != "Ed25519":
            _fail("material algorithm")
        if item["public_key_encoding"] != "raw-32-byte-lowercase-hex":
            _fail("material encoding")
        key_hex = item["public_key_hex"]
        digest = item["public_key_bytes_sha256"]
        if type(key_hex) is not str or _HEX_KEY_RE.fullmatch(key_hex) is None:
            _fail("public key hex")
        raw_key = bytes.fromhex(key_hex)
        if len(raw_key) != 32 or type(digest) is not str or _SHA_RE.fullmatch(digest) is None:
            _fail("public key length or digest")
        if hashlib.sha256(raw_key).hexdigest() != digest:
            _fail("raw public key digest")
        material_by_kid[kid] = item
    if list(material_by_kid) != sorted(material_by_kid):
        _fail("material kid order")

    status_by_kid: dict[str, dict[str, Any]] = {}
    records: list[KeyRecord] = []
    identities: list[PublicTrustRecordIdentity] = []
    for item in status_keys:
        item = _closed(item, _STATUS_KEY_FIELDS, "status key")
        kid = item["kid"]
        if type(kid) is not str or _ID_RE.fullmatch(kid) is None or kid in status_by_kid:
            _fail("status kid")
        if item["jws_alg"] != "EdDSA" or item["key_algorithm"] != "Ed25519":
            _fail("status algorithm")
        if item["status"] not in _STATUS_VALUES or item["trust_domain"] != TRUST_DOMAIN:
            _fail("status or trust domain")
        not_before = _utc_epoch(item["not_before"], "not_before")
        expires_at = _utc_epoch(item["expires_at"], "expires_at")
        if not_before > expires_at:
            _fail("status validity order")
        material_item = material_by_kid.get(kid)
        if material_item is None:
            _fail("status unknown kid")
        public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(material_item["public_key_hex"]))
        records.append(KeyRecord(kid, public_key, item["status"], not_before, expires_at, TRUST_DOMAIN))
        identities.append(
            PublicTrustRecordIdentity(
                kid=kid,
                jws_alg=item["jws_alg"],
                key_algorithm=item["key_algorithm"],
                public_key_bytes_sha256=material_item["public_key_bytes_sha256"],
                status=item["status"],
                trust_domain=item["trust_domain"],
                not_before=item["not_before"],
                expires_at=item["expires_at"],
            )
        )
        status_by_kid[kid] = item
    if list(status_by_kid) != sorted(status_by_kid) or set(status_by_kid) != set(material_by_kid):
        _fail("material/status key set")

    store = TrustStore(records, trust_domain=TRUST_DOMAIN)
    store.records = MappingProxyType(dict(store.records))
    semantic_payload = {
        "assurance_profile_id": ASSURANCE_PROFILE_ID,
        "fixed_utc_epoch_seconds": AUTHORIZED_FIXED_UTC_EPOCH_SECONDS,
        "records": [identity.__dict__ for identity in identities],
        "trust_domain": TRUST_DOMAIN,
    }
    semantic_sha = hashlib.sha256(canonical_json_bytes(semantic_payload) + b"\n").hexdigest()
    loader_path = Path(__file__).resolve()
    signing_path = loader_path.with_name("signing.py")
    loader_sha = sha256_file(loader_path)
    signing_sha = sha256_file(signing_path)
    status_sha = hashlib.sha256(status_raw).hexdigest()
    freeze_payload = {
        "assurance_profile_id": ASSURANCE_PROFILE_ID,
        "fixed_utc_epoch_seconds": AUTHORIZED_FIXED_UTC_EPOCH_SECONDS,
        "loader_callable": f"{__name__}.load_portable_public_trust",
        "loader_sha256": loader_sha,
        "material_schema_sha256": material_schema_sha,
        "material_sha256": material_sha,
        "semantic_payload_sha256": semantic_sha,
        "signing_sha256": signing_sha,
        "status_registry_sha256": status_sha,
        "status_schema_sha256": status_schema_sha,
        "trust_domain": TRUST_DOMAIN,
    }
    freeze_identity = hashlib.sha256(canonical_json_bytes(freeze_payload) + b"\n").hexdigest()
    return LoadedPublicTrust(
        store=store,
        assurance_profile_id=ASSURANCE_PROFILE_ID,
        trust_domain=TRUST_DOMAIN,
        material_schema_sha256=material_schema_sha,
        status_schema_sha256=status_schema_sha,
        material_sha256=material_sha,
        status_registry_sha256=status_sha,
        loader_sha256=loader_sha,
        signing_sha256=signing_sha,
        semantic_payload_sha256=semantic_sha,
        records=tuple(identities),
        public_trust_freeze_identity=freeze_identity,
    )


def load_portable_public_trust() -> LoadedPublicTrust:
    """Load the one module-relative Portable public-trust composition."""
    if inspect.signature(load_portable_public_trust).parameters:
        _fail("public loader signature")
    return _load_from_contract_root(_CONTRACT_ROOT)

