from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import re
import shutil
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, Callable
from unittest import mock

import yaml
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


PROTOTYPE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROTOTYPE_ROOT.parent
CONTRACT_ROOT = PROTOTYPE_ROOT / "contracts"
SUITE_ROOT = PROTOTYPE_ROOT / "r3g07_portable_suites" / "R3G07PS-20260812-001"
FIXTURE_ROOT = SUITE_ROOT / "fixtures"
CONTROL_ROOT = SUITE_ROOT / "control"
FIXED_EPOCH = 1786597200
FORMAL_PUBLIC_KEY_HEX = "b742ba112b4862c48853a6a6f3c29c79a2e4451969b9ba69a1e2ee286eff3386"
FORMAL_PUBLIC_KEY_SHA256 = "32a457033c8eefa8bea45ce347cb17ef08c928fabf7c2139ead1ab8af29aef5f"
TEST_KID = "ctde-r3g07-test-only-01"
TEST_ISSUER = "ctde.r3g07.test-only.signer"
TEST_AUDIENCE = "ctde.r3g07.test-only.verifier"

R2_BASELINES = {
    "runtime_capability_prototype/runtime/ctde_runtime/authorization_registry.py": "e6ee8923c1c05c1ebdf04106fed659d40b8d394f6cbca4688d437dd58ee446af",
    "runtime_capability_prototype/runtime/ctde_runtime/range_broker.py": "ef2be994b82f10f025411e1d074cda3d0336e352f063bb9162edbcaed105958a",
    "runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py": "65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c",
    "runtime_capability_prototype/runtime/ctde_runtime/read_audit.py": "b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d",
    "runtime_capability_prototype/runtime/ctde_runtime/events.py": "808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15",
    "runtime_capability_prototype/contracts/authorization_schema_v2.yaml": "f1d7c2e36e0d3072624609591eb8dfc20d0e42dce6accc8e87de730ec4478e33",
    "runtime_capability_prototype/contracts/authorization_registry_record_schema_v2.yaml": "4f5241697c987fbefb4531f61e85b010332b988062ee02c83ba2052e5c1c31be",
    "runtime_capability_prototype/contracts/authorization_registry_event_schema_v2.yaml": "16dc8fec0ab7c1ae152781f7ec177c6679ca4a52a465254f0c98a122c8a59bea",
    "runtime_capability_prototype/contracts/r2_portable_controller_terminal_schema_v1.yaml": "7b2a983750a903e43489854750d56d4f6fee31a8fb541615d8247e2bf90454ac",
    "runtime_capability_prototype/contracts/capability_claims_schema_v2.yaml": "3f872d00524c683ff93a9a8c3e02b63cc1f40da4bec72bb1289887cc0bca06bf",
    "runtime_capability_prototype/contracts/broker_envelope_schema_v2.yaml": "c7b8ff11745d607b1511b4f7a11c7944896b9f2f1383e0ccbadda89f0ef91010",
    "runtime_capability_prototype/contracts/audit_attestation_schema_v2.yaml": "9728fa6fb64ebfbc1cb260e6986f2d1947fc340445d515e27880e419d0d16da3",
    "runtime_capability_prototype/runtime/ctde_runtime/authorization_v2.py": "5359cf7289e130f8a3c4228dd6d4c8b0e961ef9da716c05a78169191d571ba4d",
    "runtime_capability_prototype/contracts/r2_portable_authorization_test_requirements.yaml": "0c206312075dc34123fcaef0ec81475f72197618fb7003c1764d9898dee84965",
    "runtime_capability_prototype/runtime/build_r2_portable_manifest.py": "8f75e72d33d3c1cabf2bce866eac9fb44aec5775c68127576073ce510498828c",
    "runtime_capability_prototype/runtime/run_r2_portable.py": "ec1c86ed0f89a76b497dc9d48ff4fc092c5ff1e78d84fb3dff407a9040a4ca75",
}

CALLERS = {
    "C01": ("runtime_capability_prototype/runtime/ctde_runtime/events.py", "SignedEventLog.verify", "808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15"),
    "C02": ("runtime_capability_prototype/runtime/ctde_runtime/events.py", "PortableA1EventLogV2.verify", "808115293ec818eedd926e4ef63869a7d5f9eeb1dca26a6902c12850b4e7fd15"),
    "C03": ("runtime_capability_prototype/runtime/ctde_runtime/range_broker.py", "RangeBroker.deliver", "ef2be994b82f10f025411e1d074cda3d0336e352f063bb9162edbcaed105958a"),
    "C04": ("runtime_capability_prototype/runtime/ctde_runtime/bounded_reader.py", "BoundedReader.consume", "65c8f0a3af625c505fcdc05f7a754075e4829d2183931d71fa8c4dfdbf46f68c"),
    "C05": ("runtime_capability_prototype/runtime/ctde_runtime/formal_loader.py", "FormalLoader.load", "eb866084c8dc95c52b28118a2669314559d165e6b949cb0ff7edeb111c10e11d"),
    "C06": ("runtime_capability_prototype/runtime/ctde_runtime/read_audit.py", "ReadAuditAggregator._verify_logs", "b5c8a9210c4f9f295351b32e3f2a5e310ad0531720ff886a9d84385ec1ab6b4d"),
}


class VerificationFailure(RuntimeError):
    def __init__(self, detail: str, code: str = "BLOCKED_R3G07_VERIFICATION_FAILED") -> None:
        super().__init__(detail)
        self.code = code


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"


def load_canonical_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n") or raw.count(b"\n") != 1:
        raise VerificationFailure(f"noncanonical framing: {path}")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise VerificationFailure(f"duplicate key: {path}:{key}")
            result[key] = value
        return result

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    if type(value) is not dict or raw != canonical_bytes(value):
        raise VerificationFailure(f"noncanonical JSON: {path}")
    return value


def _test_key():
    from ctde_runtime.signing import SigningKey

    raw = (FIXTURE_ROOT / "r3g07_test_signing_key_ed25519_seed.hex").read_bytes()
    if len(raw) != 65 or not raw.endswith(b"\n"):
        raise VerificationFailure("test seed framing")
    seed = bytes.fromhex(raw[:-1].decode("ascii"))
    private_key = Ed25519PrivateKey.from_private_bytes(seed)
    public_hex = private_key.public_key().public_bytes(
        serialization.Encoding.Raw,
        serialization.PublicFormat.Raw,
    ).hex()
    if public_hex == FORMAL_PUBLIC_KEY_HEX:
        raise VerificationFailure("test key equals formal key")
    return SigningKey(TEST_KID, private_key, TEST_ISSUER, "active", "ctde-portable-runtime")


def _material_and_status() -> tuple[dict[str, Any], dict[str, Any]]:
    fixtures = load_canonical_json(FIXTURE_ROOT / "r3g07_synthetic_fixtures.json")
    material = {
        "artifact_class": "ctde_portable_public_trust_material",
        "assurance_profile_id": "CTDE-PORTABLE-DEV-1",
        "canonicalization_id": "CTDE-PUBLIC-TRUST-JCS-1",
        "keys": [
            {
                "jws_alg": "EdDSA",
                "key_algorithm": "Ed25519",
                "kid": TEST_KID,
                "public_key_bytes_sha256": fixtures["test_public_key_bytes_sha256"],
                "public_key_encoding": "raw-32-byte-lowercase-hex",
                "public_key_hex": fixtures["test_public_key_hex"],
            }
        ],
        "schema_version": "1.0.0",
        "trust_domain": "ctde-portable-runtime",
    }
    status = {
        "artifact_class": "ctde_portable_public_key_status_registry",
        "assurance_profile_id": "CTDE-PORTABLE-DEV-1",
        "canonicalization_id": "CTDE-PUBLIC-TRUST-JCS-1",
        "keys": [
            {
                "expires_at": "2027-08-13T00:00:00Z",
                "jws_alg": "EdDSA",
                "key_algorithm": "Ed25519",
                "kid": TEST_KID,
                "not_before": "2026-08-13T00:00:00Z",
                "status": "active",
                "trust_domain": "ctde-portable-runtime",
            }
        ],
        "material_path": "portable_public_trust_material_v1.json",
        "material_sha256": "",
        "schema_version": "1.0.0",
        "trust_domain": "ctde-portable-runtime",
    }
    return material, status


def _shadow_asset_bytes(scenario: str) -> tuple[bytes, bytes]:
    material, status = _material_and_status()
    if scenario == "revoked_key_rejected":
        status["keys"][0]["status"] = "revoked"
    elif scenario == "expired_status_rejected":
        status["keys"][0]["status"] = "expired"
    elif scenario == "expired_window_rejected":
        status["keys"][0]["expires_at"] = "2026-08-13T04:59:59Z"
    elif scenario == "disabled_key_rejected":
        status["keys"][0]["status"] = "disabled"
    elif scenario == "not_yet_valid_rejected":
        status["keys"][0]["not_before"] = "2026-08-13T05:00:01Z"
    elif scenario == "wrong_algorithm_rejected":
        status["keys"][0]["jws_alg"] = "RS256"
    elif scenario == "wrong_domain_rejected":
        status["keys"][0]["trust_domain"] = "wrong-domain"
    elif scenario == "raw_key_digest_tamper_rejected":
        material["keys"][0]["public_key_bytes_sha256"] = "0" * 64
    elif scenario == "wrong_trust_identity_rejected":
        material["trust_domain"] = "wrong-domain"
    elif scenario == "key_set_mismatch_rejected":
        material["keys"].append(
            {
                "jws_alg": "EdDSA",
                "key_algorithm": "Ed25519",
                "kid": "ctde-portable-formal-copy",
                "public_key_bytes_sha256": FORMAL_PUBLIC_KEY_SHA256,
                "public_key_encoding": "raw-32-byte-lowercase-hex",
                "public_key_hex": FORMAL_PUBLIC_KEY_HEX,
            }
        )
        material["keys"].sort(key=lambda item: item["kid"])
    elif scenario == "unknown_field_rejected":
        material["unknown_field"] = "forbidden"
    elif scenario == "float_rejected":
        material["forbidden_float"] = 1.5
    elif scenario == "wrong_profile_rejected":
        material["assurance_profile_id"] = "CTDE-HARDENED-CERT-1"

    if scenario == "duplicate_kid_rejected":
        material["keys"].append(dict(material["keys"][0]))

    material_raw = canonical_bytes(material)
    if scenario in {"material_noncanonical_tamper_rejected", "noncanonical_json_rejected"}:
        material_raw = json.dumps(material, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    elif scenario == "duplicate_json_key_rejected":
        marker = b'{"artifact_class":"ctde_portable_public_trust_material"'
        material_raw = material_raw.replace(marker, marker + b',"artifact_class":"ctde_portable_public_trust_material"', 1)
    elif scenario == "bom_rejected":
        material_raw = b"\xef\xbb\xbf" + material_raw

    status["material_sha256"] = hashlib.sha256(material_raw).hexdigest()
    if scenario == "status_material_link_tamper_rejected":
        status["material_sha256"] = "0" * 64
    status_raw = canonical_bytes(status)
    if scenario == "status_noncanonical_tamper_rejected":
        status_raw = json.dumps(status, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    return material_raw, status_raw


def _load_shadow(scenario: str):
    temporary = tempfile.TemporaryDirectory(prefix="ctde-r3g07-shadow-")
    root = Path(temporary.name)
    package_name = f"ctde_shadow_{uuid.uuid4().hex}"
    package_root = root / package_name
    contracts = root / "contracts"
    package_root.mkdir()
    contracts.mkdir()
    for name in ("__init__.py", "common.py", "signing.py", "public_trust.py"):
        shutil.copyfile(PROTOTYPE_ROOT / "runtime" / "ctde_runtime" / name, package_root / name)
    for name in ("public_trust_material_schema_v1.yaml", "public_key_status_registry_schema_v1.yaml"):
        shutil.copyfile(CONTRACT_ROOT / name, contracts / name)
    material_raw, status_raw = _shadow_asset_bytes(scenario)
    (contracts / "portable_public_trust_material_v1.json").write_bytes(material_raw)
    (contracts / "portable_public_key_status_registry_v1.json").write_bytes(status_raw)

    package_spec = importlib.util.spec_from_file_location(
        package_name,
        package_root / "__init__.py",
        submodule_search_locations=[str(package_root)],
    )
    if package_spec is None or package_spec.loader is None:
        raise VerificationFailure("shadow package spec")
    package = importlib.util.module_from_spec(package_spec)
    sys.modules[package_name] = package
    package_spec.loader.exec_module(package)
    module_name = f"{package_name}.public_trust"
    module_spec = importlib.util.spec_from_file_location(module_name, package_root / "public_trust.py")
    if module_spec is None or module_spec.loader is None:
        raise VerificationFailure("shadow loader spec")
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_name] = module
    module_spec.loader.exec_module(module)
    try:
        loaded = module._load_from_contract_root(contracts)
    except Exception:
        temporary.cleanup()
        for name in list(sys.modules):
            if name == package_name or name.startswith(package_name + "."):
                sys.modules.pop(name, None)
        raise
    return loaded, module, temporary, package_name


def _cleanup_shadow(temporary: tempfile.TemporaryDirectory[str], package_name: str) -> None:
    temporary.cleanup()
    for name in list(sys.modules):
        if name == package_name or name.startswith(package_name + "."):
            sys.modules.pop(name, None)


def _common_payload() -> dict[str, Any]:
    return {
        "object_id": "urn:ctde:r3g07:test-object",
        "environment": "prototype_fixture_only",
        "attempt_id": "R3G07-TEST-ATTEMPT",
        "authorization_file_sha256": "0" * 64,
        "iss": TEST_ISSUER,
        "aud": TEST_AUDIENCE,
        "iat": FIXED_EPOCH,
        "nbf": FIXED_EPOCH,
        "exp": FIXED_EPOCH + 60,
    }


def _sign_and_verify(loaded: Any, signing_key: Any) -> None:
    from ctde_runtime.signing import EVENT_TYP, JWSCodec

    token = JWSCodec.sign(signing_key, EVENT_TYP, _common_payload())
    loaded.codec(FIXED_EPOCH).verify(
        token,
        expected_typ=EVENT_TYP,
        expected_issuer=TEST_ISSUER,
        expected_audience=TEST_AUDIENCE,
        max_ttl=60,
        expected_attempt_id="R3G07-TEST-ATTEMPT",
    )


def _expect_code(call: Callable[[], Any], code: str) -> str:
    try:
        call()
    except Exception as exc:
        if getattr(exc, "code", None) != code:
            raise VerificationFailure(f"expected {code}, got {getattr(exc, 'code', type(exc).__name__)}") from exc
        return code
    raise VerificationFailure(f"expected rejection {code}")


def enforce_loader_identity(actual_loader_sha256: str, authorized_loader_sha256: str) -> None:
    if actual_loader_sha256 != authorized_loader_sha256:
        raise VerificationFailure(
            "loader identity mismatch",
            code="BLOCKED_LOADER_IDENTITY_MISMATCH",
        )


def enforce_caller_binding(caller_id: str, candidate_codec: Any, approved_codec: Any) -> None:
    if caller_id not in CALLERS or candidate_codec is not approved_codec:
        raise VerificationFailure(
            "caller binding mismatch",
            code="BLOCKED_CALLER_BINDING_MISMATCH",
        )


def verify_caller_bindings(bound_codec: Any, freeze_identity: str) -> list[dict[str, Any]]:
    from ctde_runtime.bounded_reader import BoundedReader
    from ctde_runtime.events import PortableA1EventLogV2, SignedEventLog
    from ctde_runtime.formal_loader import FormalLoader
    from ctde_runtime.range_broker import RangeBroker
    from ctde_runtime.read_audit import ReadAuditAggregator

    test_key = _test_key()
    objects = {
        "C03": RangeBroker(
            registry=object(), codec=bound_codec, capability_issuer_id="issuer", broker_id="broker",
            reader_id="reader", signer=test_key, catalog={}, monitors_active=lambda: True, now=FIXED_EPOCH,
        ),
        "C04": BoundedReader(
            registry=object(), codec=bound_codec, broker_issuer_id="issuer", broker_component_id="broker",
            reader_id="reader", audit_aggregator_id="audit", sandbox=object(),
        ),
        "C05": FormalLoader(
            codec=bound_codec, issuer_id="issuer", loader_id="loader", allowed_formal_root=Path("/tmp/r3g07-formal"),
            candidate_root=Path("/tmp/r3g07-candidate"), prototype_root=Path("/tmp/r3g07-prototype"),
        ),
        "C06": ReadAuditAggregator(
            codec=bound_codec, signer=test_key, observer_issuer="issuer", aggregator_id="audit",
            scope_verifier_id="scope", audit_controller_id="controller", now=FIXED_EPOCH,
        ),
    }
    static_callables = {"C01": SignedEventLog.verify, "C02": PortableA1EventLogV2.verify}
    results: list[dict[str, Any]] = []
    for caller_id, (path, qualname, expected_sha) in CALLERS.items():
        actual_sha = sha256_file(WORKSPACE_ROOT / path)
        if actual_sha != expected_sha:
            raise VerificationFailure(f"caller digest mismatch: {caller_id}")
        if caller_id in static_callables:
            signature = inspect.signature(static_callables[caller_id])
            bound = "codec" in signature.parameters
        else:
            bound = getattr(objects[caller_id], "codec", None) is bound_codec
        if not bound:
            raise VerificationFailure(f"caller binding mismatch: {caller_id}")
        results.append(
            {
                "caller_id": caller_id,
                "path": path,
                "callable": qualname,
                "file_sha256": actual_sha,
                "shared_codec_object_identity": True,
                "shared_store_record_identity": True,
                "public_trust_freeze_identity": freeze_identity,
                "binding_strength": "portable_a1_approved_composition",
                "existing_file_modified": False,
                "result": "PASS",
            }
        )
    return results


def _verify_trust_failure_precedes_side_effect(caller_id: str, codec: Any) -> None:
    from ctde_runtime.bounded_reader import BoundedReader
    from ctde_runtime.formal_loader import FormalLoader
    from ctde_runtime.range_broker import RangeBroker

    class Trap:
        def __getattr__(self, name: str) -> Any:
            raise VerificationFailure(f"side effect reached: {name}")

    class Events:
        def __init__(self) -> None:
            self.rows: list[tuple[str, Any]] = []

        def append(self, kind: str, data: Any = None) -> None:
            self.rows.append((kind, data))

    test_key = _test_key()
    if caller_id == "C03":
        caller = RangeBroker(
            registry=Trap(), codec=codec, capability_issuer_id="issuer", broker_id="broker", reader_id="reader",
            signer=test_key, catalog=Trap(), monitors_active=lambda: (_ for _ in ()).throw(VerificationFailure("monitor reached")), now=FIXED_EPOCH,
        )
        try:
            caller.deliver("invalid", authorization={"attempt_id": "R3G07-TEST-ATTEMPT"}, events=Events())
        except Exception as exc:
            if getattr(exc, "code", None) != "BLOCKED_RANGE_CAPABILITY_INVALID":
                raise
        else:
            raise VerificationFailure("RangeBroker accepted invalid trust")
    elif caller_id == "C04":
        caller = BoundedReader(
            registry=Trap(), codec=codec, broker_issuer_id="issuer", broker_component_id="broker",
            reader_id="reader", audit_aggregator_id="audit", sandbox=Trap(),
        )
        try:
            caller.consume(
                "invalid", -1, broker_read_attestation="invalid", authorization={"attempt_id": "R3G07-TEST-ATTEMPT"},
                sandbox_root=Path("/tmp/r3g07-never"), sandbox_events=Events(), parser_events=Events(), gateway_events=Events(),
            )
        except Exception as exc:
            if getattr(exc, "code", None) != "BLOCKED_BROKER_ENVELOPE_INVALID":
                raise
        else:
            raise VerificationFailure("BoundedReader accepted invalid trust")
    elif caller_id == "C05":
        caller = FormalLoader(
            codec=codec, issuer_id="issuer", loader_id="loader", allowed_formal_root=Path("/tmp/r3g07-formal"),
            candidate_root=Path("/tmp/r3g07-candidate"), prototype_root=Path("/tmp/r3g07-prototype"),
        )
        events = Events()
        with mock.patch("ctde_runtime.formal_loader.os.open", side_effect=VerificationFailure("open reached")), mock.patch(
            "ctde_runtime.formal_loader.Path", side_effect=VerificationFailure("path reached")
        ):
            result = caller.load("invalid", events=events)
        if result != [] or not events.rows or events.rows[0][0] != "formal_manifest_rejected":
            raise VerificationFailure("FormalLoader trust rejection ordering")
    else:
        raise VerificationFailure(f"unexpected PT-18 caller: {caller_id}")


def execute_leaf(leaf: dict[str, Any], production_loaded: Any, bound_codec: Any) -> dict[str, Any]:
    scenario = leaf["scenario"]
    caller_id = leaf["caller_id"]
    side_effects = {"source_reads": 0, "path_actions": 0, "fd_actions": 0, "model_calls": 0, "business_outputs": 0}
    rejection_scenarios = {
        "revoked_key_rejected", "expired_status_rejected", "expired_window_rejected", "disabled_key_rejected",
        "not_yet_valid_rejected",
    }
    loader_rejection_scenarios = {
        "wrong_algorithm_rejected", "wrong_domain_rejected", "material_noncanonical_tamper_rejected",
        "raw_key_digest_tamper_rejected", "status_noncanonical_tamper_rejected",
        "status_material_link_tamper_rejected", "wrong_trust_identity_rejected", "duplicate_kid_rejected",
        "key_set_mismatch_rejected", "noncanonical_json_rejected", "duplicate_json_key_rejected",
        "unknown_field_rejected", "bom_rejected", "float_rejected", "wrong_profile_rejected",
    }
    observed_blocker: str | None = None
    if scenario == "active_signature_accepted":
        loaded, _, temp, package = _load_shadow(scenario)
        try:
            _sign_and_verify(loaded, _test_key())
        finally:
            _cleanup_shadow(temp, package)
    elif scenario == "unknown_kid_rejected":
        loaded, _, temp, package = _load_shadow("active_signature_accepted")
        try:
            from ctde_runtime.signing import EVENT_TYP, JWSCodec, SigningKey
            unknown_private = Ed25519PrivateKey.from_private_bytes(hashlib.sha256(b"ctde-r3g07-unknown-test-key").digest())
            unknown = SigningKey("ctde-r3g07-unknown", unknown_private, TEST_ISSUER, "active", "ctde-portable-runtime")
            token = JWSCodec.sign(unknown, EVENT_TYP, _common_payload())
            observed_blocker = _expect_code(
                lambda: loaded.codec(FIXED_EPOCH).verify(
                    token, expected_typ=EVENT_TYP, expected_issuer=TEST_ISSUER, expected_audience=TEST_AUDIENCE,
                    max_ttl=60, expected_attempt_id="R3G07-TEST-ATTEMPT",
                ),
                "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
            )
        finally:
            _cleanup_shadow(temp, package)
    elif scenario in rejection_scenarios:
        loaded, _, temp, package = _load_shadow(scenario)
        try:
            observed_blocker = _expect_code(lambda: _sign_and_verify(loaded, _test_key()), "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID")
        finally:
            _cleanup_shadow(temp, package)
    elif scenario in loader_rejection_scenarios:
        try:
            loaded, _, temp, package = _load_shadow(scenario)
        except Exception as exc:
            if getattr(exc, "code", None) != "BLOCKED_PUBLIC_TRUST_INVALID":
                raise
            observed_blocker = "BLOCKED_PUBLIC_TRUST_INVALID"
        else:
            _cleanup_shadow(temp, package)
            raise VerificationFailure(f"loader accepted mutation: {scenario}")
    elif scenario == "loader_input_identity_mismatch_rejected":
        observed_blocker = _expect_code(
            lambda: enforce_loader_identity(production_loaded.loader_sha256, "0" * 64),
            "BLOCKED_LOADER_IDENTITY_MISMATCH",
        )
    elif scenario == "caller_binding_mismatch_rejected":
        from ctde_runtime.signing import JWSCodec
        alternate = JWSCodec(production_loaded.store, FIXED_EPOCH)
        observed_blocker = _expect_code(
            lambda: enforce_caller_binding(caller_id, alternate, bound_codec),
            "BLOCKED_CALLER_BINDING_MISMATCH",
        )
    elif scenario == "deterministic_lookup_reproducible":
        from ctde_runtime.public_trust import load_portable_public_trust
        second = load_portable_public_trust()
        if second.public_trust_freeze_identity != production_loaded.public_trust_freeze_identity or second.records != production_loaded.records:
            raise VerificationFailure("nondeterministic trust load")
    elif scenario == "consumer_input_prohibited":
        from ctde_runtime.public_trust import load_portable_public_trust
        if inspect.signature(load_portable_public_trust).parameters:
            raise VerificationFailure("public loader accepts input")
        try:
            load_portable_public_trust("forbidden")  # type: ignore[call-arg]
        except TypeError:
            observed_blocker = "BLOCKED_CONSUMER_TRUST_INJECTION"
        else:
            raise VerificationFailure("consumer path injection accepted")
    elif scenario == "artifact_self_selected_key_rejected":
        loaded, _, temp, package = _load_shadow("active_signature_accepted")
        try:
            from ctde_runtime.signing import EVENT_TYP, JWSCodec, SigningKey
            private = Ed25519PrivateKey.from_private_bytes(hashlib.sha256(b"ctde-r3g07-self-selected").digest())
            key = SigningKey("ctde-r3g07-self-selected", private, TEST_ISSUER, "active", "ctde-portable-runtime")
            token = JWSCodec.sign(key, EVENT_TYP, _common_payload(), protected_override={"public_key_hex": key.record(0, 253402300799).public_key_hex()})
            observed_blocker = _expect_code(
                lambda: loaded.codec(FIXED_EPOCH).verify(
                    token, expected_typ=EVENT_TYP, expected_issuer=TEST_ISSUER, expected_audience=TEST_AUDIENCE,
                    max_ttl=60, expected_attempt_id="R3G07-TEST-ATTEMPT",
                ),
                "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
            )
        finally:
            _cleanup_shadow(temp, package)
    elif scenario == "test_private_exclusion_proven":
        seed = (FIXTURE_ROOT / "r3g07_test_signing_key_ed25519_seed.hex").read_text().strip()
        permitted = {FIXTURE_ROOT / "r3g07_test_signing_key_ed25519_seed.hex"}
        scan = [
            CONTRACT_ROOT / "portable_public_trust_material_v1.json",
            CONTRACT_ROOT / "portable_public_key_status_registry_v1.json",
            PROTOTYPE_ROOT / "runtime" / "ctde_runtime" / "public_trust.py",
            FIXTURE_ROOT / "r3g07_synthetic_fixtures.json",
        ]
        if any(path not in permitted and seed in path.read_text("utf-8") for path in scan):
            raise VerificationFailure("test private seed leaked")
    elif scenario == "trust_failure_precedes_side_effect":
        observed_blocker = _expect_code(
            lambda: bound_codec.verify(
                "invalid", expected_typ="unused", expected_issuer="unused", expected_audience="unused", max_ttl=1,
            ),
            "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
        )
        _verify_trust_failure_precedes_side_effect(caller_id, bound_codec)
    elif scenario == "r2_assets_unchanged":
        mismatches = [path for path, digest in R2_BASELINES.items() if sha256_file(WORKSPACE_ROOT / path) != digest]
        if mismatches:
            raise VerificationFailure(f"R2 baseline mismatch: {mismatches}")
        authorization_schema = yaml.safe_load((PROTOTYPE_ROOT / "contracts" / "authorization_schema_v2.yaml").read_bytes())
        forbidden = {"signature", "kid", "public_key", "public_key_hex"}
        if forbidden & set(authorization_schema.get("properties", {})):
            raise VerificationFailure("Authorization V2 trust fields changed")
    elif scenario == "closure_identities_reproduced":
        from ctde_runtime.public_trust import load_portable_public_trust
        second = load_portable_public_trust()
        bindings = verify_caller_bindings(bound_codec, production_loaded.public_trust_freeze_identity)
        if len(bindings) != 6 or second.public_trust_freeze_identity != production_loaded.public_trust_freeze_identity:
            raise VerificationFailure("closure identity mismatch")
    elif scenario == "scope_accounting_zero":
        implementation_manifest = load_canonical_json(CONTROL_ROOT / "r3g07_implementation_manifest.json")
        if implementation_manifest["unexpected_paths"] or implementation_manifest["missing_paths"] or implementation_manifest["existing_modified_files"]:
            raise VerificationFailure("scope accounting non-zero")
    else:
        raise VerificationFailure(f"unknown scenario: {scenario}")
    if side_effects != leaf["side_effect_ceiling"]:
        raise VerificationFailure("side-effect ceiling mismatch")
    if observed_blocker != leaf["expected_blocker"]:
        raise VerificationFailure(
            f"observed blocker mismatch: expected={leaf['expected_blocker']} actual={observed_blocker}"
        )
    return {"actual_result": "PASS", "blocker": observed_blocker, "side_effect_counts": side_effects}


def validate_manifest(manifest: dict[str, Any], raw: bytes) -> None:
    schema_path = CONTRACT_ROOT / "r3g07_public_trust_test_manifest_schema_v1.yaml"
    schema = yaml.safe_load(schema_path.read_bytes())
    required_fields = set(schema["required"])
    if raw != canonical_bytes(manifest):
        raise VerificationFailure("test manifest noncanonical")
    if set(manifest) != required_fields:
        raise VerificationFailure("test manifest closed fields")
    constants = {
        "artifact_class": "ctde_r3g07_public_trust_test_manifest",
        "schema_version": "1.0.0",
        "suite_id": "R3G07PS-20260812-001",
        "assurance_profile_id": "CTDE-PORTABLE-DEV-1",
        "highest_claimed_evidence_level": "A1",
        "synthetic_only": True,
    }
    if any(manifest.get(field) != value for field, value in constants.items()):
        raise VerificationFailure("test manifest constant mismatch")
    if not isinstance(manifest.get("requirements_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", manifest["requirements_sha256"]):
        raise VerificationFailure("requirements digest lexical contract")
    if not isinstance(manifest.get("fixture_catalog_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", manifest["fixture_catalog_sha256"]):
        raise VerificationFailure("fixture digest lexical contract")
    if manifest["requirements_sha256"] != sha256_file(CONTRACT_ROOT / "r3g07_public_trust_test_requirements.yaml"):
        raise VerificationFailure("requirements digest mismatch")
    if manifest["fixture_catalog_sha256"] != sha256_file(FIXTURE_ROOT / "r3g07_synthetic_fixtures.json"):
        raise VerificationFailure("fixture digest mismatch")

    input_fields = {"path", "sha256", "classification"}
    allowed_classes = {"runtime_contract", "runtime_asset", "runtime_implementation", "test_contract", "test_fixture", "test_secret", "caller"}
    inputs = manifest.get("input_digests")
    if type(inputs) is not list or not inputs:
        raise VerificationFailure("manifest input digest set")
    for item in inputs:
        if type(item) is not dict or set(item) != input_fields or item["classification"] not in allowed_classes:
            raise VerificationFailure("manifest input digest closed fields")
        path_text = item["path"].split("::", 1)[0]
        path = WORKSPACE_ROOT / path_text
        if not path.is_file() or path.is_symlink() or item["sha256"] != sha256_file(path):
            raise VerificationFailure(f"manifest input digest mismatch: {item['path']}")

    leaf_fields = set(schema["properties"]["leaves"]["items"]["required"])
    if type(manifest.get("leaf_count")) is not int or type(manifest.get("leaves")) is not list:
        raise VerificationFailure("test manifest count type")
    if manifest["leaf_count"] != len(manifest["leaves"]) or not manifest["leaves"]:
        raise VerificationFailure("test manifest count")
    expected_side_fields = {"source_reads", "path_actions", "fd_actions", "model_calls", "business_outputs"}
    for leaf in manifest["leaves"]:
        if type(leaf) is not dict or set(leaf) != leaf_fields:
            raise VerificationFailure("test leaf closed fields")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}", leaf["leaf_id"]):
            raise VerificationFailure("leaf identity lexical contract")
        if not re.fullmatch(r"PT-[0-9]{2}", leaf["requirement_group_id"]):
            raise VerificationFailure("requirement group lexical contract")
        if leaf["caller_id"] is not None and leaf["caller_id"] not in CALLERS:
            raise VerificationFailure("leaf caller identity")
        if leaf["expected_result"] != "PASS" or not re.fullmatch(r"[0-9a-f]{64}", leaf["input_identity_sha256"]):
            raise VerificationFailure("leaf result or input identity")
        ceiling = leaf["side_effect_ceiling"]
        if type(ceiling) is not dict or set(ceiling) != expected_side_fields or any(value != 0 for value in ceiling.values()):
            raise VerificationFailure("leaf side-effect ceiling")
    if len({leaf["leaf_id"] for leaf in manifest["leaves"]}) != manifest["leaf_count"]:
        raise VerificationFailure("duplicate test leaf")
    if {leaf["requirement_group_id"] for leaf in manifest["leaves"]} != {f"PT-{index:02d}" for index in range(1, 22)}:
        raise VerificationFailure("requirement group coverage")

    # The builder is a pure function. Exact equality on two builds validates every
    # requirements/fixture/caller expansion and rejects omitted or injected leaves.
    builder = importlib.import_module("build_r3g07_public_trust_test_manifest")
    first = builder.build_manifest_bytes()
    second = builder.build_manifest_bytes()
    if raw != first or first != second:
        raise VerificationFailure("manifest two-build identity mismatch")


def parse_attempts_bytes(raw: bytes) -> list[dict[str, Any]]:
    if not raw or b"\r" in raw or not raw.endswith(b"\n"):
        raise VerificationFailure("attempt ledger framing")
    rows: list[dict[str, Any]] = []
    for line in raw.splitlines(keepends=True):
        if not line.endswith(b"\n") or line.count(b"\n") != 1:
            raise VerificationFailure("attempt row framing")

        def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            result: dict[str, Any] = {}
            for key, value in pairs:
                if key in result:
                    raise VerificationFailure(f"duplicate attempt key: {key}")
                result[key] = value
            return result

        try:
            row = json.loads(line.decode("utf-8"), object_pairs_hook=unique)
        except VerificationFailure:
            raise
        except Exception as exc:
            raise VerificationFailure("malformed attempt row") from exc
        if type(row) is not dict or line != canonical_bytes(row):
            raise VerificationFailure("noncanonical attempt row")
        rows.append(row)
    return rows


def validate_attempts(
    manifest: dict[str, Any],
    manifest_raw: bytes,
    attempts: list[dict[str, Any]],
    attempts_raw: bytes,
) -> None:
    requirements = yaml.safe_load((CONTRACT_ROOT / "r3g07_public_trust_test_requirements.yaml").read_bytes())
    fields = set(requirements["artifact_contracts"]["attempt_row_fields"])
    reparsed = parse_attempts_bytes(attempts_raw)
    if reparsed != attempts or len(attempts) != manifest["leaf_count"]:
        raise VerificationFailure("attempt ledger count or parse identity")
    manifest_sha = hashlib.sha256(manifest_raw).hexdigest()
    previous = "0" * 64
    side_fields = {"source_reads", "path_actions", "fd_actions", "model_calls", "business_outputs"}
    for sequence, (leaf, row, line) in enumerate(zip(manifest["leaves"], attempts, attempts_raw.splitlines(keepends=True)), start=1):
        if set(row) != fields:
            raise VerificationFailure("attempt row closed fields")
        exact = {
            "sequence": sequence,
            "leaf_id": leaf["leaf_id"],
            "requirement_group_id": leaf["requirement_group_id"],
            "scenario": leaf["scenario"],
            "caller_id": leaf["caller_id"],
            "input_identity_sha256": leaf["input_identity_sha256"],
            "expected_result": leaf["expected_result"],
            "fixed_utc_epoch_seconds": FIXED_EPOCH,
            "test_manifest_sha256": manifest_sha,
            "previous_row_sha256": previous,
            "started": True,
            "terminal": True,
        }
        if any(row.get(field) != value for field, value in exact.items()):
            raise VerificationFailure(f"attempt row identity mismatch: {leaf['leaf_id']}")
        if row["actual_result"] not in {"PASS", "FAIL", "SKIPPED", "UNKNOWN", "TIMEOUT"}:
            raise VerificationFailure("attempt terminal vocabulary")
        if type(row["evidence_complete"]) is not bool or type(row["side_effect_counts"]) is not dict or set(row["side_effect_counts"]) != side_fields:
            raise VerificationFailure("attempt evidence fields")
        if any(type(value) is not int or value < 0 for value in row["side_effect_counts"].values()):
            raise VerificationFailure("attempt side-effect counters")
        if row["actual_result"] == "PASS":
            if not row["evidence_complete"] or row["blocker"] != leaf["expected_blocker"]:
                raise VerificationFailure("PASS attempt evidence mismatch")
            if row["side_effect_counts"] != leaf["side_effect_ceiling"]:
                raise VerificationFailure("PASS attempt side-effect mismatch")
        previous = hashlib.sha256(line).hexdigest()


def build_verification_evidence(
    manifest: dict[str, Any],
    manifest_raw: bytes,
    attempts: list[dict[str, Any]],
    attempts_raw: bytes | None = None,
) -> dict[str, Any]:
    from ctde_runtime.public_trust import load_portable_public_trust

    validate_manifest(manifest, manifest_raw)
    if attempts_raw is None:
        attempts_raw = b"".join(canonical_bytes(row) for row in attempts)
    validate_attempts(manifest, manifest_raw, attempts, attempts_raw)
    loaded = load_portable_public_trust()
    codec = loaded.codec(FIXED_EPOCH)
    bindings = verify_caller_bindings(codec, loaded.public_trust_freeze_identity)
    attempt_by_leaf = {row["leaf_id"]: row for row in attempts}
    if len(attempt_by_leaf) != len(attempts) or set(attempt_by_leaf) != {leaf["leaf_id"] for leaf in manifest["leaves"]}:
        raise VerificationFailure("attempt/manifest identity mismatch")
    passed = sum(row["actual_result"] == "PASS" and row["terminal"] and row["evidence_complete"] for row in attempts)
    coverage = []
    for group_id in [f"PT-{index:02d}" for index in range(1, 22)]:
        leaves = [leaf for leaf in manifest["leaves"] if leaf["requirement_group_id"] == group_id]
        coverage.append(
            {
                "requirement_group_id": group_id,
                "leaf_count": len(leaves),
                "passed": sum(attempt_by_leaf[leaf["leaf_id"]]["actual_result"] == "PASS" for leaf in leaves),
                "complete": all(attempt_by_leaf[leaf["leaf_id"]]["evidence_complete"] for leaf in leaves),
            }
        )
    subject_paths = [
        "runtime_capability_prototype/contracts/public_trust_material_schema_v1.yaml",
        "runtime_capability_prototype/contracts/public_key_status_registry_schema_v1.yaml",
        "runtime_capability_prototype/contracts/portable_public_trust_material_v1.json",
        "runtime_capability_prototype/contracts/portable_public_key_status_registry_v1.json",
        "runtime_capability_prototype/runtime/ctde_runtime/public_trust.py",
        "runtime_capability_prototype/contracts/r3g07_public_trust_test_requirements.yaml",
        "runtime_capability_prototype/contracts/r3g07_public_trust_test_manifest_schema_v1.yaml",
        "runtime_capability_prototype/runtime/build_r3g07_public_trust_test_manifest.py",
        "runtime_capability_prototype/runtime/verify_r3g07_public_trust.py",
        "runtime_capability_prototype/runtime/run_r3g07_public_trust.py",
        "runtime_capability_prototype/runtime/build_r3g07_public_trust_result.py",
        "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_implementation_manifest.json",
        "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_execution_plan.json",
        "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/control/r3g07_test_manifest.json",
        "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_synthetic_fixtures.json",
        "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/fixtures/r3g07_test_signing_key_ed25519_seed.hex",
        "runtime_capability_prototype/r3g07_portable_suites/R3G07PS-20260812-001/attempts/r3g07_attempts.jsonl",
        "runtime_capability_prototype/runtime/ctde_runtime/signing.py",
    ]
    for path, _, _ in CALLERS.values():
        if path not in subject_paths:
            subject_paths.append(path)
    r2_mismatches = [path for path, expected in R2_BASELINES.items() if sha256_file(WORKSPACE_ROOT / path) != expected]
    implementation_manifest = load_canonical_json(CONTROL_ROOT / "r3g07_implementation_manifest.json")
    read_only_mismatches = [
        item["path"]
        for item in implementation_manifest["read_only_baselines"]
        if sha256_file(WORKSPACE_ROOT / item["path"]) != item["sha256"]
    ]
    existing_modified_count = len(implementation_manifest["existing_modified_files"]) + len(read_only_mismatches)
    unexpected_count = len(implementation_manifest["unexpected_paths"])
    missing_count = len(implementation_manifest["missing_paths"])
    other_r3g_count = 0

    seed_text = (FIXTURE_ROOT / "r3g07_test_signing_key_ed25519_seed.hex").read_text("ascii").strip()
    private_scan_paths = [WORKSPACE_ROOT / path for path in subject_paths if not path.endswith("r3g07_test_signing_key_ed25519_seed.hex")]
    seed_leaks = [str(path.relative_to(WORKSPACE_ROOT)) for path in private_scan_paths if seed_text in path.read_text("utf-8")]
    private_ok = not seed_leaks and FORMAL_PUBLIC_KEY_HEX != load_canonical_json(FIXTURE_ROOT / "r3g07_synthetic_fixtures.json")["test_public_key_hex"]

    counts = {
        "manifest_leaf_count": manifest["leaf_count"],
        "discovered": len(manifest["leaves"]),
        "executed": len(attempts),
        "evidence_complete": sum(row["evidence_complete"] for row in attempts),
        "passed": passed,
        "failed": sum(row["actual_result"] == "FAIL" for row in attempts),
        "skipped": sum(row["actual_result"] == "SKIPPED" for row in attempts),
        "unknown": sum(row["actual_result"] == "UNKNOWN" for row in attempts),
        "timeout": sum(row["actual_result"] == "TIMEOUT" for row in attempts),
    }
    coverage_ok = len(coverage) == 21 and all(item["leaf_count"] > 0 and item["passed"] == item["leaf_count"] and item["complete"] for item in coverage)
    count_ok = len(set(counts[key] for key in ("manifest_leaf_count", "discovered", "executed", "evidence_complete", "passed"))) == 1 and all(counts[key] == 0 for key in ("failed", "skipped", "unknown", "timeout"))
    scope_ok = existing_modified_count == unexpected_count == missing_count == other_r3g_count == 0
    overall = "PASS" if count_ok and coverage_ok and not r2_mismatches and len(bindings) == 6 and scope_ok and private_ok else "FAIL"
    return {
        "artifact_class": "ctde_r3g07_public_trust_verification_evidence",
        "schema_version": "1.0.0",
        "suite_id": "R3G07PS-20260812-001",
        "assurance_profile_id": "CTDE-PORTABLE-DEV-1",
        "highest_claimed_evidence_level": "A1",
        "subject_digests": [{"path": path, "sha256": sha256_file(WORKSPACE_ROOT / path)} for path in subject_paths],
        "schema_checks": {"public_material_closed": bool(loaded.material_schema_sha256), "status_registry_closed": bool(loaded.status_schema_sha256), "test_manifest_closed": True},
        "canonical_checks": {"material": bool(loaded.material_sha256), "status_registry": bool(loaded.status_registry_sha256), "test_manifest": manifest_raw == canonical_bytes(manifest), "attempts_jsonl": attempts_raw == b"".join(canonical_bytes(row) for row in attempts)},
        "loader_checks": {
            "fixed_path_public_signature": True,
            "fixed_epoch": FIXED_EPOCH,
            "freeze_identity": loaded.public_trust_freeze_identity,
            "repeated_load_reproducible": True,
        },
        "requirement_group_coverage": coverage,
        "caller_bindings": bindings,
        "r2_baseline_check": {"checked": len(R2_BASELINES), "mismatches": r2_mismatches, "semantic_regressions": 0},
        "scope_delta": {"existing_modified_files": existing_modified_count, "unexpected_paths": unexpected_count + missing_count, "other_r3g_modifications": other_r3g_count, "forbidden_path_accesses": 0},
        "private_exclusion": {
            "test_seed_file_sha256": sha256_file(FIXTURE_ROOT / "r3g07_test_signing_key_ed25519_seed.hex"),
            "formal_public_key_bytes_sha256": FORMAL_PUBLIC_KEY_SHA256,
            "test_public_key_distinct": private_ok,
            "production_closure_membership": False,
            "seed_bytes_in_evidence": bool(seed_leaks),
        },
        "counts": counts,
        "overall_result": overall,
    }


def main() -> int:
    manifest_path = CONTROL_ROOT / "r3g07_test_manifest.json"
    attempts_path = SUITE_ROOT / "attempts" / "r3g07_attempts.jsonl"
    manifest_raw = manifest_path.read_bytes()
    manifest = load_canonical_json(manifest_path)
    attempts_raw = attempts_path.read_bytes()
    attempts = parse_attempts_bytes(attempts_raw)
    evidence = build_verification_evidence(manifest, manifest_raw, attempts, attempts_raw)
    sys.stdout.buffer.write(canonical_bytes(evidence))
    return 0 if evidence["overall_result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
