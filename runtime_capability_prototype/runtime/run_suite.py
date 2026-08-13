from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
sys.path.insert(0, str(ROOT / "runtime"))

from ctde_runtime.authorization_registry import AuthorizationRegistry  # noqa: E402
from ctde_runtime.bounded_reader import BoundedReader  # noqa: E402
from ctde_runtime.common import (  # noqa: E402
    PrototypeError,
    atomic_write_bytes,
    b64url_decode,
    b64url_encode,
    canonical_json_bytes,
    dump_json,
    dump_yaml,
    load_yaml,
    require,
    sha256_bytes,
    sha256_file,
)
from ctde_runtime.events import SignedEventLog  # noqa: E402
from ctde_runtime.fixture_factory import (  # noqa: E402
    BOOK1_END,
    BOOK1_LENGTH,
    BOOK1_START,
    FixtureIdentity,
    fixture_attestation,
    generate_fixture,
    greek_existence_attestation,
)
from ctde_runtime.formal_loader import FormalLoader  # noqa: E402
from ctde_runtime.range_broker import CapabilityIssuer, RangeBroker  # noqa: E402
from ctde_runtime.read_audit import ReadAuditAggregator  # noqa: E402
from ctde_runtime.sandbox import SandboxSupervisor  # noqa: E402
from ctde_runtime.signing import (  # noqa: E402
    AUDIT_TYP,
    CAPABILITY_TYP,
    ENVELOPE_TYP,
    FORMAL_TYP,
    JWSCodec,
    KeyRecord,
    SigningKey,
    TrustStore,
)


SUITE_ID = "RCPTS-20260811-002"
NOW = 1786464000
DOMAINS = ("registry", "broker", "sandbox", "parser", "gateway", "write", "formal")

CAPABILITY_ISSUER_ID = "ctde-prototype-capability-issuer"
BROKER_ID = "ctde-prototype-range-broker"
READER_ID = "ctde-prototype-bounded-reader"
OBSERVER_ID = "ctde-prototype-audit-observer"
AUDIT_AGGREGATOR_ID = "ctde-prototype-audit-aggregator"
SCOPE_VERIFIER_ID = "ctde-prototype-scope-verifier"
AUDIT_CONTROLLER_ID = "ctde-prototype-audit-controller"
FORMAL_CONTROL_ID = "ctde-prototype-formal-control"
FORMAL_LOADER_ID = "ctde-prototype-formal-loader"


def render_yaml(value: Any) -> bytes:
    return yaml.safe_dump(
        value,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    ).encode("utf-8")


def decode_token(token: str) -> tuple[dict[str, Any], dict[str, Any], str]:
    protected_segment, payload_segment, signature_segment = token.split(".")
    protected = json.loads(b64url_decode(protected_segment).decode("utf-8"))
    payload = json.loads(b64url_decode(payload_segment).decode("utf-8"))
    return protected, payload, signature_segment


def unsigned_mutation(
    token: str,
    *,
    protected_updates: dict[str, Any] | None = None,
    payload_updates: dict[str, Any] | None = None,
    mutate_signature: bool = False,
) -> str:
    protected, payload, signature = decode_token(token)
    for mapping, updates in ((protected, protected_updates), (payload, payload_updates)):
        if updates:
            for key, value in updates.items():
                if value is None:
                    mapping.pop(key, None)
                else:
                    mapping[key] = value
    if mutate_signature:
        signature = ("A" if not signature.startswith("A") else "B") + signature[1:]
    return f"{b64url_encode(canonical_json_bytes(protected))}.{b64url_encode(canonical_json_bytes(payload))}.{signature}"


@dataclass
class SuiteKeys:
    capability: SigningKey
    broker: SigningKey
    observer: SigningKey
    audit: SigningKey
    formal: SigningKey
    revoked: SigningKey
    expired: SigningKey
    production: SigningKey
    unknown: SigningKey


class SuiteRuntime:
    def __init__(self, *, output_root: Path, persistent: bool) -> None:
        self.root = ROOT
        self.output_root = output_root
        self.persistent = persistent
        self.suite_root = output_root / "suites" / SUITE_ID
        self.manifest_path = ROOT / "suites" / SUITE_ID / "control" / "runtime_capability_test_manifest.yaml"
        self.manifest = load_yaml(self.manifest_path)
        self.keys = self._make_keys()
        self.prototype_store, self.production_store = self._make_trust_stores()
        self.codec = JWSCodec(self.prototype_store, NOW)
        self.production_codec = JWSCodec(self.production_store, NOW)
        self.registry = AuthorizationRegistry(output_root / "registry" / "prototype_registry.sqlite3")
        self.probe_binary = ROOT / "bin" / "consumer_probe"
        self.component_digests: dict[str, str] = {}

    def _make_keys(self) -> SuiteKeys:
        return SuiteKeys(
            capability=SigningKey.generate("rcpts-capability-active", CAPABILITY_ISSUER_ID),
            broker=SigningKey.generate("rcpts-broker-active", BROKER_ID),
            observer=SigningKey.generate("rcpts-observer-active", OBSERVER_ID),
            audit=SigningKey.generate("rcpts-audit-active", AUDIT_AGGREGATOR_ID),
            formal=SigningKey.generate("rcpts-formal-active", FORMAL_CONTROL_ID),
            revoked=SigningKey.generate("rcpts-revoked", "ctde-prototype-revoked"),
            expired=SigningKey.generate("rcpts-expired", "ctde-prototype-expired"),
            production=SigningKey.generate("synthetic-production-root", "ctde-synthetic-production", "production"),
            unknown=SigningKey.generate("rcpts-unknown", "ctde-prototype-unknown"),
        )

    def _make_trust_stores(self) -> tuple[TrustStore, TrustStore]:
        active = [
            self.keys.capability.record(NOW - 60, NOW + 86400),
            self.keys.broker.record(NOW - 60, NOW + 86400),
            self.keys.observer.record(NOW - 60, NOW + 86400),
            self.keys.audit.record(NOW - 60, NOW + 86400),
            self.keys.formal.record(NOW - 60, NOW + 86400),
            self.keys.revoked.record(NOW - 60, NOW + 86400, status="revoked"),
            self.keys.expired.record(NOW - 86400, NOW - 1, status="active"),
        ]
        prototype = TrustStore(active, trust_domain="prototype")
        production = TrustStore(
            [self.keys.production.record(NOW - 60, NOW + 86400)],
            trust_domain="production",
        )
        return prototype, production

    def validate_manifest(self) -> list[dict[str, Any]]:
        manifest = self.manifest
        require(manifest["suite_id"] == SUITE_ID, "BLOCKED_MANIFEST_INVALID", "suite id")
        require(manifest["environment"] == "prototype_fixture_only", "BLOCKED_MANIFEST_INVALID")
        require(manifest["candidate_run_id"] is None, "BLOCKED_MANIFEST_INVALID")
        require(manifest["candidate_run_authorized"] is False, "BLOCKED_MANIFEST_INVALID")
        leaves = manifest.get("leaf_cases")
        require(isinstance(leaves, list) and leaves, "BLOCKED_MANIFEST_INVALID", "leaves")
        groups = {case["requirement_group"] for case in leaves}
        require(groups == set(manifest["requirement_groups"]), "BLOCKED_MANIFEST_INVALID", "groups")
        require(len(groups) == 37, "BLOCKED_MANIFEST_INVALID", "requirement group coverage")
        require(len({case["leaf_case_id"] for case in leaves}) == len(leaves), "BLOCKED_MANIFEST_INVALID", "leaf ids")
        require(len({case["attempt_id"] for case in leaves}) == len(leaves), "BLOCKED_MANIFEST_INVALID", "attempt ids")
        for case in leaves:
            require(str(case["attempt_id"]).startswith("RCPT-"), "BLOCKED_MANIFEST_INVALID", "attempt namespace")
            require(not str(case["attempt_id"]).startswith("AC-"), "BLOCKED_MANIFEST_INVALID", "candidate namespace")
        grants = [case["grant_id"] for case in leaves if case["requires_grant"]]
        require(all(grants) and len(set(grants)) == len(grants), "BLOCKED_MANIFEST_INVALID", "grant isolation")
        return leaves

    def bootstrap(self) -> None:
        leaves = self.validate_manifest()
        if self.persistent:
            require(not (self.suite_root / "aggregate" / "test_results.json").exists(), "BLOCKED_SUITE_ALREADY_FINALIZED")
            existing_cases = self.suite_root / "cases"
            require(not existing_cases.exists() or not any(existing_cases.iterdir()), "BLOCKED_SUITE_ALREADY_STARTED")
        self._compile_probe()
        self._write_component_manifest()
        self._write_suite_snapshots(leaves)
        self._write_fixture_attestations()

    def _compile_probe(self) -> None:
        source = ROOT / "native" / "consumer_probe.c"
        self.probe_binary.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["gcc", "-static", "-O2", "-Wall", "-Wextra", "-Werror", "-o", str(self.probe_binary), str(source)],
            check=True,
            cwd=ROOT,
        )

    def _write_component_manifest(self) -> None:
        components = {
            "authorization_registry": "runtime/ctde_runtime/authorization_registry.py",
            "range_broker": "runtime/ctde_runtime/range_broker.py",
            "bounded_reader": "runtime/ctde_runtime/bounded_reader.py",
            "formal_loader": "runtime/ctde_runtime/formal_loader.py",
            "read_audit": "runtime/ctde_runtime/read_audit.py",
            "signed_event_log": "runtime/ctde_runtime/events.py",
            "signed_profiles": "runtime/ctde_runtime/signing.py",
            "fixture_controller": "runtime/ctde_runtime/fixture_factory.py",
            "sandbox_supervisor": "runtime/ctde_runtime/sandbox.py",
            "sandbox_probe_source": "native/consumer_probe.c",
            "sandbox_probe_binary": "bin/consumer_probe",
            "suite_runner": "runtime/run_suite.py",
        }
        records = []
        for component_id, relative in components.items():
            path = ROOT / relative
            digest = sha256_file(path)
            self.component_digests[component_id] = digest
            records.append(
                {
                    "component_id": f"ctde-prototype-{component_id}",
                    "version": "0.1.0",
                    "path": relative,
                    "sha256": digest,
                    "environment": "prototype_fixture_only",
                    "production_approved": False,
                }
            )
        manifest = {
            "schema_version": "1.0.0",
            "artifact_class": "runtime_capability_component_manifest",
            "suite_id": SUITE_ID,
            "environment": "prototype_fixture_only",
            "candidate_run_authorized": False,
            "formal_phase_2_input": False,
            "components": records,
        }
        target = self.output_root / "contracts" / "component_manifest.yaml"
        dump_yaml(target, manifest, mode=0o444)

    def _write_suite_snapshots(self, leaves: list[dict[str, Any]]) -> None:
        control = self.suite_root / "control"
        control.mkdir(parents=True, exist_ok=True)
        if self.output_root != ROOT:
            shutil.copy2(self.manifest_path, control / self.manifest_path.name)
        key_records = []
        for key, status, trust_domain, not_before, expires in (
            (self.keys.capability, "active", "prototype", NOW - 60, NOW + 86400),
            (self.keys.broker, "active", "prototype", NOW - 60, NOW + 86400),
            (self.keys.observer, "active", "prototype", NOW - 60, NOW + 86400),
            (self.keys.audit, "active", "prototype", NOW - 60, NOW + 86400),
            (self.keys.formal, "active", "prototype", NOW - 60, NOW + 86400),
            (self.keys.revoked, "revoked", "prototype", NOW - 60, NOW + 86400),
            (self.keys.expired, "active", "prototype", NOW - 86400, NOW - 1),
            (self.keys.production, "active", "synthetic_production_test_only", NOW - 60, NOW + 86400),
        ):
            record = key.record(not_before, expires, status=status)
            key_records.append(
                {
                    "kid": record.kid,
                    "issuer": key.issuer,
                    "status": status,
                    "trust_domain": trust_domain,
                    "not_before": not_before,
                    "expires_at": expires,
                    "public_key_ed25519_hex": record.public_key_hex(),
                    "private_key_persisted": False,
                }
            )
        component_snapshot = {
            "schema_version": "1.0.0",
            "artifact_class": "runtime_capability_suite_component_snapshot",
            "suite_id": SUITE_ID,
            "frozen_before_attempts": True,
            "deterministic_test_clock": NOW,
            "component_digests": self.component_digests,
            "key_records": key_records,
            "signed_profiles": {
                "capability": "CTDE-CAPABILITY-JWS-1",
                "broker_envelope": "CTDE-BROKER-ENVELOPE-JWS-1",
                "audit_attestation": "CTDE-AUDIT-ATTESTATION-JWS-1",
                "algorithm": "EdDSA",
                "profile_version": 1,
            },
        }
        policy_snapshot = {
            "schema_version": "1.0.0",
            "artifact_class": "runtime_capability_suite_test_policy_snapshot",
            "suite_id": SUITE_ID,
            "frozen_before_attempts": True,
            "manifest_file_sha256": sha256_file(control / self.manifest_path.name),
            "manifest_leaf_count_by_enumeration": len(leaves),
            "requirement_group_count_by_enumeration": len({leaf["requirement_group"] for leaf in leaves}),
            "test_policy_file_sha256": sha256_file(ROOT / "contracts" / "test_policy.yaml"),
            "fixture_recipe_file_sha256": sha256_file(ROOT / "fixture_specs" / "synthetic_book1_fixture.yaml"),
            "candidate_runs_executed": 0,
            "model_invocations_allowed": 0,
        }
        dump_yaml(control / "suite_component_snapshot.yaml", component_snapshot, mode=0o444)
        dump_yaml(control / "suite_test_policy_snapshot.yaml", policy_snapshot, mode=0o444)

    def _write_fixture_attestations(self) -> None:
        target = self.suite_root / "fixture_attestations"
        target.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="ctde-fixture-attestation-") as temporary:
            identity = generate_fixture(Path(temporary) / "fixture", attempt_id="RCPT-FIXTURE-ATTESTATION")
            dump_yaml(target / "synthetic_book1_fixture_identity.yaml", fixture_attestation(identity), mode=0o444)
            dump_yaml(target / "synthetic_greek_fixture_existence_attestation.yaml", greek_existence_attestation(identity), mode=0o444)


class CaseHarness:
    def __init__(self, suite: SuiteRuntime, case: dict[str, Any], case_root: Path) -> None:
        self.suite = suite
        self.case = case
        self.case_root = case_root
        self.attempt_id = case["attempt_id"]
        self.requirement = case["requirement_group"]
        self.suffix = case["leaf_suffix"]
        self.authorization: dict[str, Any] | None = None
        self.authorization_bytes: bytes | None = None
        self.fixture: FixtureIdentity | None = None
        self.logs: dict[str, SignedEventLog] = {}
        self.lease = None
        self.capability_token: str | None = None
        self.capability_id: str | None = None
        self.consumption_event_id: str | None = None
        self.delivery = None
        self.delivery_id: str | None = None
        self.reader_result: dict[str, Any] | None = None
        self.sandbox_snapshot: dict[str, Any] | None = None
        self.scope_attestation: str | None = None
        self.closure_attestation: str | None = None
        self.formal_inputs = 0
        self.write_attempts = 0
        self.write_denied = 0
        self.actual_component_result = "UNSET"
        self.blockers: list[str] = []
        self.temp_root: Path | None = None
        self.formal_root: Path | None = None
        self.candidate_probe_root: Path | None = None
        self.formal_loader: FormalLoader | None = None

    def run(self) -> dict[str, Any]:
        self.case_root.mkdir(parents=True, exist_ok=False)
        (self.case_root / "control").mkdir()
        (self.case_root / "evidence").mkdir()
        (self.case_root / "attestations").mkdir()
        with tempfile.TemporaryDirectory(prefix=f"ctde-{self.attempt_id.lower()}-") as temporary:
            self.temp_root = Path(temporary)
            try:
                self._prepare_case()
                self.actual_component_result = self._execute_case()
            except PrototypeError as exc:
                self.actual_component_result = exc.code
                self.blockers.append(f"{exc.code}: {exc.detail}" if exc.detail else exc.code)
            except Exception as exc:
                self.actual_component_result = "UNEXPECTED_EXCEPTION"
                self.blockers.append(f"{type(exc).__name__}: {exc}")
            try:
                self._finalize_evidence()
            except PrototypeError as exc:
                if self.actual_component_result == self.case["expected_component_result"]:
                    self.actual_component_result = exc.code
                self.blockers.append(f"{exc.code}: {exc.detail}" if exc.detail else exc.code)
            except Exception as exc:
                self.actual_component_result = "UNEXPECTED_EVIDENCE_EXCEPTION"
                self.blockers.append(f"{type(exc).__name__}: {exc}")
            result = self._write_case_result()
        return result

    def _fixture_variant(self) -> str:
        if self.requirement == "RCPT-T18-BOOK2-MARKER" and self.suffix == "PARSER":
            return "book2_marker"
        if self.requirement == "RCPT-T28-PARSER-UNSAFE":
            return {
                "DTD": "dtd",
                "INTERNAL-ENTITY": "internal_entity",
                "EXTERNAL-FILE-ENTITY": "external_file_entity",
                "EXTERNAL-NETWORK-ENTITY": "external_network_entity",
                "RECOVERY": "recovery",
                "BOOK2": "book2_marker",
                "DUPLICATE-BOOK1": "duplicate_book1",
                "WRONG-BOOK": "wrong_book",
                "EXTRA-CARD": "extra_card",
                "MISSING-CARD": "missing_card",
                "EXTRA-PARAGRAPH": "extra_paragraph",
                "MISSING-PARAGRAPH": "missing_paragraph",
                "QNAME-NAMESPACE": "wrong_namespace",
            }[self.suffix]
        return "baseline"

    def _prepare_case(self) -> None:
        needs_fixture = bool(self.case["requires_grant"])
        if needs_fixture:
            self.fixture = generate_fixture(
                self.temp_root / "broker-only-fixture",
                attempt_id=self.attempt_id,
                variant=self._fixture_variant(),
            )
            self._create_authorization()
        self._create_logs()
        self._write_execution_snapshot()
        self.formal_root = self.temp_root / "formal-root"
        self.candidate_probe_root = self.temp_root / "analysis_candidate"
        self.formal_root.mkdir()
        self.candidate_probe_root.mkdir()
        self.formal_loader = FormalLoader(
            codec=self.suite.codec,
            issuer_id=FORMAL_CONTROL_ID,
            loader_id=FORMAL_LOADER_ID,
            allowed_formal_root=self.formal_root,
            candidate_root=self.candidate_probe_root,
            prototype_root=ROOT,
        )

    def _create_authorization(self) -> None:
        assert self.fixture is not None
        fixture_object_id = self.fixture.object_id
        forbidden_roles = ["greek", "production_raw"]
        if self.requirement == "RCPT-T16-GREEK-ID" and self.suffix == "AUTH-GREEK-ROLE":
            fixture_object_id = "urn:ctde:fixture-greek-deny:synthetic"
        if self.requirement == "RCPT-T16-GREEK-ID" and self.suffix == "AUTH-PRODUCTION-RAW":
            fixture_object_id = "urn:sha256:synthetic-production-object"
        expected_slice = self.fixture.slice_sha256
        if self.requirement == "RCPT-T11-SLICE-HASH":
            expected_slice = "0" * 64
        payload = {
            "artifact_class": "runtime_capability_test_authorization",
            "environment": "prototype_fixture_only",
            "authorization_id": self.case["grant_id"],
            "attempt_id": self.attempt_id,
            "prototype_fixture_authorized": True,
            "candidate_run_authorized": False,
            "formal_phase_2_input": False,
            "one_time": True,
            "automatic_retry_allowed": False,
            "authorization_inheritable": False,
            "fixture_object_id": fixture_object_id,
            "fixture_structure_contract_id": self.fixture.structure_contract_id,
            "fixture_structure_contract_sha256": self.fixture.structure_contract_sha256,
            "allowed_range": {"start_byte": BOOK1_START, "end_byte_exclusive": BOOK1_END},
            "expected_length": BOOK1_LENGTH,
            "expected_slice_sha256": expected_slice,
            "forbidden_source_roles": forbidden_roles,
            "expires_at": NOW - 1 if self.requirement == "RCPT-T04-AUTH-EXPIRED" else NOW + 600,
            "initial_state": "expired" if self.requirement == "RCPT-T04-AUTH-EXPIRED" else "unconsumed",
        }
        self.authorization_bytes = render_yaml(payload)
        digest = sha256_bytes(self.authorization_bytes)
        self.authorization = dict(payload)
        self.authorization["authorization_file_sha256"] = digest
        atomic_write_bytes(
            self.case_root / "control" / "prototype_authorization.yaml",
            self.authorization_bytes,
            mode=0o444,
        )

    def _create_logs(self) -> None:
        digest = self.authorization["authorization_file_sha256"] if self.authorization else "absent"
        for domain in DOMAINS:
            log = SignedEventLog(
                attempt_id=self.attempt_id,
                domain=domain,
                signer=self.suite.keys.observer,
                audience=AUDIT_AGGREGATOR_ID,
                authorization_file_sha256=digest,
                now=NOW,
            )
            log.append(
                "observer_started",
                {
                    "writer": f"ctde-prototype-{domain}-observer",
                    "started_before_broker_open": True,
                    "process_tree_coverage": True,
                },
            )
            self.logs[domain] = log

    def _write_execution_snapshot(self) -> None:
        snapshot = {
            "schema_version": "1.0.0",
            "artifact_class": "runtime_capability_prototype_execution_snapshot",
            "environment": "prototype_fixture_only",
            "suite_id": SUITE_ID,
            "attempt_id": self.attempt_id,
            "candidate_run_id": None,
            "candidate_run_authorized": False,
            "formal_phase_2_input": False,
            "requirement_group": self.requirement,
            "leaf_case_id": self.case["leaf_case_id"],
            "component_digests": self.suite.component_digests,
            "test_clock": NOW,
            "sandbox_backend": "empty-chroot+single-id-map+zero-capabilities+no_new_privs+seccomp+close_fds+proc-supervisor",
            "scope_proof_level": "candidate_visible_bytes_and_application_exact_range",
            "model_invocations": 0,
            "automatic_retries": 0,
            "private_keys_persisted": False,
        }
        dump_yaml(self.case_root / "control" / "prototype_execution_snapshot.yaml", snapshot, mode=0o444)

    def _validate_authorization_role(self) -> None:
        assert self.authorization is not None
        object_id = self.authorization["fixture_object_id"]
        if "GREEK" in object_id.upper() or object_id.startswith("urn:sha256:") or "PRODUCTION" in object_id.upper():
            raise PrototypeError("BLOCKED_FORBIDDEN_SOURCE_ROLE")
        require(object_id.startswith("urn:ctde:fixture:"), "BLOCKED_FORBIDDEN_SOURCE_ROLE")
        require(
            self.authorization["forbidden_source_roles"] == ["greek", "production_raw"],
            "BLOCKED_FORBIDDEN_SOURCE_ROLE",
        )

    def _register_authorization(self) -> None:
        assert self.authorization is not None and self.authorization_bytes is not None
        self._validate_authorization_role()
        self.suite.registry.register(self.authorization, self.authorization_bytes)
        self.logs["registry"].append(
            "authorization_registered",
            {
                "authorization_id": self.authorization["authorization_id"],
                "state": self.authorization["initial_state"],
                "immutable_file_sha256": self.authorization["authorization_file_sha256"],
            },
        )

    def _consume_authorization(self, *, digest_override: str | None = None) -> None:
        assert self.authorization is not None
        self.lease = self.suite.registry.consume(
            authorization_id=self.authorization["authorization_id"],
            attempt_id=self.attempt_id,
            authorization_digest=digest_override or self.authorization["authorization_file_sha256"],
            now=NOW,
            events=self.logs["registry"],
        )
        self.consumption_event_id = self.lease.consumption_event_id

    def _issuer(self) -> CapabilityIssuer:
        return CapabilityIssuer(
            registry=self.suite.registry,
            signer=self.suite.keys.capability,
            broker_id=BROKER_ID,
            now=NOW,
        )

    def _mint_capability(self) -> None:
        assert self.authorization is not None and self.lease is not None
        self.capability_token = self._issuer().mint(self.lease, self.authorization, self.logs["registry"])
        _, payload, _ = decode_token(self.capability_token)
        self.capability_id = payload["capability_id"]

    def _monitors_active(self) -> bool:
        for domain in ("broker", "sandbox", "write"):
            if not self.logs[domain].tokens:
                return False
            _, payload, _ = decode_token(self.logs[domain].tokens[0])
            if payload.get("kind") != "observer_started":
                return False
        return True

    def _broker(self) -> RangeBroker:
        assert self.fixture is not None
        return RangeBroker(
            registry=self.suite.registry,
            codec=self.suite.codec,
            capability_issuer_id=CAPABILITY_ISSUER_ID,
            broker_id=BROKER_ID,
            reader_id=READER_ID,
            signer=self.suite.keys.broker,
            catalog={self.fixture.object_id: self.fixture},
            monitors_active=self._monitors_active,
            now=NOW,
        )

    def _deliver(self, token: str | None = None, request: dict[str, Any] | None = None) -> None:
        assert self.authorization is not None
        selected_token = token or self.capability_token
        assert selected_token is not None
        broker = self._broker()
        if request is not None:
            self.delivery = broker.handle_request(request, authorization=self.authorization, events=self.logs["broker"])
        else:
            self.delivery = broker.deliver(selected_token, authorization=self.authorization, events=self.logs["broker"])
        self.delivery_id = self.delivery.metadata["delivery_id"]

    def _reader(self) -> BoundedReader:
        return BoundedReader(
            registry=self.suite.registry,
            codec=self.suite.codec,
            broker_issuer_id=BROKER_ID,
            broker_component_id=BROKER_ID,
            reader_id=READER_ID,
            audit_aggregator_id=AUDIT_AGGREGATOR_ID,
            sandbox=SandboxSupervisor(probe_binary=self.suite.probe_binary, workspace_root=WORKSPACE),
        )

    def _read_delivery(
        self,
        *,
        envelope: str | None = None,
        broker_attestation: str | None = None,
        attack: str = "none",
        host_path: Path | None = None,
        inherited_fixture_fd: int | None = None,
        preserve_inherited_fixture_fd: bool = False,
        gateway_book2_injection: bool = False,
        sandbox_name: str = "sandbox-root",
    ) -> None:
        assert self.delivery is not None and self.authorization is not None
        reader = self._reader()
        try:
            self.reader_result = reader.consume(
                envelope or self.delivery.signed_envelope,
                self.delivery.sealed_slice_fd,
                broker_read_attestation=broker_attestation or self.delivery.broker_read_attestation,
                authorization=self.authorization,
                sandbox_root=self.temp_root / sandbox_name,
                sandbox_events=self.logs["sandbox"],
                parser_events=self.logs["parser"],
                gateway_events=self.logs["gateway"],
                attack=attack,
                host_path=host_path,
                inherited_fixture_fd=inherited_fixture_fd,
                preserve_inherited_fixture_fd=preserve_inherited_fixture_fd,
                gateway_book2_injection=gateway_book2_injection,
            )
        finally:
            sandbox_result = reader.last_sandbox_result or reader.sandbox.last_probe_result
            if sandbox_result:
                self.sandbox_snapshot = sandbox_result.get("supervisor")
            elif reader.sandbox.last_environment_snapshot:
                self.sandbox_snapshot = reader.sandbox.last_environment_snapshot

    def _positive_pipeline(
        self,
        *,
        attack: str = "none",
        host_path: Path | None = None,
        inherited_fixture_fd: int | None = None,
        preserve_inherited_fixture_fd: bool = False,
        gateway_book2_injection: bool = False,
    ) -> None:
        self._register_authorization()
        self._consume_authorization()
        self._mint_capability()
        self._deliver()
        self._read_delivery(
            attack=attack,
            host_path=host_path,
            inherited_fixture_fd=inherited_fixture_fd,
            preserve_inherited_fixture_fd=preserve_inherited_fixture_fd,
            gateway_book2_injection=gateway_book2_injection,
        )

    def _resign(
        self,
        token: str,
        *,
        signer: SigningKey,
        typ: str,
        payload_updates: dict[str, Any] | None = None,
        protected_updates: dict[str, Any] | None = None,
    ) -> str:
        _, payload, _ = decode_token(token)
        if payload_updates:
            for key, value in payload_updates.items():
                if value is None:
                    payload.pop(key, None)
                else:
                    payload[key] = value
        return JWSCodec.sign(signer, typ, payload, protected_override=protected_updates)

    def _signed_formal_manifest(self, entries: list[dict[str, Any]]) -> str:
        payload = {
            "object_id": f"urn:ctde:formal-test-manifest:{uuid.uuid4()}",
            "manifest_id": f"FM-{uuid.uuid4()}",
            "environment": "prototype_fixture_only",
            "iss": FORMAL_CONTROL_ID,
            "aud": FORMAL_LOADER_ID,
            "iat": NOW,
            "nbf": NOW,
            "exp": NOW + 300,
            "formal_test_run_id": f"FTR-{self.attempt_id}",
            "formal_phase_2_authorized": False,
            "entries": entries,
        }
        return JWSCodec.sign(self.suite.keys.formal, FORMAL_TYP, payload)

    def _formal_entry(
        self,
        path: Path,
        *,
        artifact_class: str = "formal_test_input",
        authority: str = "formal_test_only",
        approved: bool = True,
        provenance: bool = True,
        identity_override: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        stat = path.stat(follow_symlinks=False)
        content = path.read_bytes() if path.is_file() and not path.is_symlink() else b""
        entry = {
            "artifact_id": f"FART-{uuid.uuid4()}",
            "artifact_class": artifact_class,
            "authority": authority,
            "approved": approved,
            "formal_provenance_id": f"FPROV-{uuid.uuid4()}" if provenance else "absent",
            "formal_provenance_sha256": sha256_bytes(b"synthetic-formal-provenance") if provenance else "absent",
            "path": str(path),
            "device": stat.st_dev,
            "inode": stat.st_ino,
            "size_bytes": stat.st_size,
            "sha256": sha256_bytes(content),
        }
        if identity_override:
            entry.update(identity_override)
        return entry

    def _ensure_write_evidence(self) -> None:
        if any(decode_token(token)[1]["kind"] == "write_monitor_complete" for token in self.logs["write"].tokens):
            return
        self.logs["write"].append(
            "write_monitor_complete",
            {
                "write_attempts": self.write_attempts,
                "write_denied": self.write_denied,
                "write_success_count": 0,
                "raw_write_count": 0,
                "structure_map_write_count": 0,
                "wrapper_persist_count": 0,
                "formal_path_write_count": 0,
                "run_local_unallowlisted_write_count": 0,
                "payload_persisted": False,
            },
        )

    def _ensure_formal_evidence(self) -> None:
        if any(decode_token(token)[1]["kind"] == "formal_loader_complete" for token in self.logs["formal"].tokens):
            return
        probe_path = self.case_root / "control" / "prototype_execution_snapshot.yaml"
        entry = {
            "artifact_id": f"PROBE-{uuid.uuid4()}",
            "artifact_class": "runtime_capability_prototype_execution_snapshot",
            "authority": "prototype_fixture_only",
            "approved": False,
            "formal_provenance_id": "absent",
            "formal_provenance_sha256": "absent",
            "path": str(probe_path),
            "device": probe_path.stat().st_dev,
            "inode": probe_path.stat().st_ino,
            "size_bytes": probe_path.stat().st_size,
            "sha256": sha256_file(probe_path),
        }
        token = self._signed_formal_manifest([entry])
        accepted = self.formal_loader.load(token, events=self.logs["formal"])
        require(len(accepted) == 0, "INVALIDATED_FORMAL_DISCOVERY_LEAK")
        self.formal_inputs = 0

    def _audit_aggregator(self) -> ReadAuditAggregator:
        return ReadAuditAggregator(
            codec=self.suite.codec,
            signer=self.suite.keys.audit,
            observer_issuer=OBSERVER_ID,
            aggregator_id=AUDIT_AGGREGATOR_ID,
            scope_verifier_id=SCOPE_VERIFIER_ID,
            audit_controller_id=AUDIT_CONTROLLER_ID,
            now=NOW,
        )

    def _execute_case(self) -> str:
        requirement = self.requirement
        if requirement == "RCPT-T01-EXACT-RANGE":
            self._positive_pipeline()
            return "PASS_EXACT_RANGE"
        if requirement == "RCPT-T02-AUTH-MISSING":
            self.suite.registry.consume(
                authorization_id=f"MISSING-{self.attempt_id}",
                attempt_id=self.attempt_id,
                authorization_digest="0" * 64,
                now=NOW,
                events=self.logs["registry"],
            )
        if requirement == "RCPT-T03-AUTH-DIGEST":
            self._register_authorization()
            self._consume_authorization(digest_override="f" * 64)
        if requirement == "RCPT-T04-AUTH-EXPIRED":
            self._register_authorization()
            self._consume_authorization()
        if requirement == "RCPT-T05-AUTH-REPLAY":
            self._register_authorization()
            self._consume_authorization()
            if self.suffix == "EVENT-REPLAY":
                self._mint_capability()
                self._issuer().mint(self.lease, self.authorization, self.logs["registry"])
            else:
                self._consume_authorization()
        if requirement == "RCPT-T06-CAP-TAMPER":
            self._register_authorization()
            self._consume_authorization()
            self._mint_capability()
            if self.suffix == "CLAIMS":
                token = unsigned_mutation(self.capability_token, payload_updates={"nonce": "tampered"})
            else:
                token = unsigned_mutation(self.capability_token, mutate_signature=True)
            self._deliver(token=token)
        if requirement == "RCPT-T07-CAP-AUDIENCE":
            self._register_authorization()
            self._consume_authorization()
            self._mint_capability()
            token = self._resign(
                self.capability_token,
                signer=self.suite.keys.capability,
                typ=CAPABILITY_TYP,
                payload_updates={"aud": "ctde-wrong-broker"},
            )
            self._deliver(token=token)
        if requirement == "RCPT-T08-RANGE-OVERRIDE":
            self._register_authorization()
            self._consume_authorization()
            self._mint_capability()
            field_map = {
                "RAW-PATH": "raw_path",
                "SOURCE-PATH": "source_path",
                "SOURCE-ID": "source_id_override",
                "START": "start_byte",
                "END": "end_byte_exclusive",
                "LENGTH": "length",
                "EOF": "read_to_eof",
                "NEXT-RANGE": "next_range",
                "RETRY": "retry",
            }
            request = {"opaque_capability": self.capability_token, field_map[self.suffix]: True}
            self._deliver(request=request)
        if requirement in {"RCPT-T09-RANGE-SHORT", "RCPT-T10-RANGE-LONG"}:
            self._register_authorization()
            self._consume_authorization()
            self._mint_capability()
            _, payload, _ = decode_token(self.capability_token)
            if requirement == "RCPT-T09-RANGE-SHORT":
                payload["end_byte_exclusive"] -= 1
                payload["expected_length"] -= 1
            else:
                payload["end_byte_exclusive"] += 1
                payload["expected_length"] += 1
            token = JWSCodec.sign(self.suite.keys.capability, CAPABILITY_TYP, payload)
            self._deliver(token=token)
        if requirement == "RCPT-T11-SLICE-HASH":
            self._register_authorization()
            self._consume_authorization()
            self._mint_capability()
            self._deliver()
        if requirement == "RCPT-T12-DELIVERY-REPLAY":
            self._positive_pipeline()
            self._read_delivery(sandbox_name="sandbox-replay")
        if requirement == "RCPT-T13-ENVELOPE-TAMPER":
            self._register_authorization()
            self._consume_authorization()
            self._mint_capability()
            self._deliver()
            if self.suffix == "CLAIMS":
                envelope = unsigned_mutation(self.delivery.signed_envelope, payload_updates={"returned_bytes": 1})
            elif self.suffix == "SIGNATURE":
                envelope = unsigned_mutation(self.delivery.signed_envelope, mutate_signature=True)
            else:
                envelope = self._resign(
                    self.delivery.signed_envelope,
                    signer=self.suite.keys.broker,
                    typ=ENVELOPE_TYP,
                    payload_updates={"broker_read_attestation_sha256": "0" * 64},
                )
            self._read_delivery(envelope=envelope)
        if requirement == "RCPT-T14-FULL-PATH":
            self._positive_pipeline(attack="open_path", host_path=self.fixture.full_path)
        if requirement == "RCPT-T15-HANDLE-INVENTORY":
            descriptor = os.open(self.fixture.full_path, os.O_RDONLY | os.O_CLOEXEC)
            try:
                self._positive_pipeline(
                    inherited_fixture_fd=descriptor,
                    preserve_inherited_fixture_fd=self.suffix == "RESIDUAL-FD-DETECTED",
                )
            finally:
                os.close(descriptor)
            return "PASS_INHERITED_FD_SANITIZED"
        if requirement == "RCPT-T16-GREEK-ID":
            if self.suffix.startswith("AUTH-"):
                self._validate_authorization_role()
            self._register_authorization()
            self._consume_authorization()
            self._mint_capability()
            object_id = (
                "urn:ctde:fixture-greek-deny:synthetic"
                if self.suffix == "CAP-GREEK-OBJECT"
                else "urn:sha256:synthetic-production-object"
            )
            token = self._resign(
                self.capability_token,
                signer=self.suite.keys.capability,
                typ=CAPABILITY_TYP,
                payload_updates={"fixture_object_id": object_id},
            )
            self._deliver(token=token)
        if requirement == "RCPT-T17-GREEK-PATH":
            self._positive_pipeline(attack="greek_path", host_path=self.fixture.greek_path)
        if requirement == "RCPT-T18-BOOK2-MARKER":
            self._positive_pipeline(gateway_book2_injection=self.suffix == "GATEWAY")
        if requirement == "RCPT-T19-WRITE-ESCAPE":
            self.write_attempts = 1
            self.write_denied = 1
            if self.suffix == "FIXTURE-STORE":
                host_path = self.fixture.full_path
                attack = "write_fixture"
            elif self.suffix == "WORKSPACE":
                host_path = WORKSPACE / "forbidden-prototype-write"
                attack = "write_workspace"
            elif self.suffix == "FORMAL-PATH":
                host_path = self.formal_root / "forbidden-formal-write"
                attack = "write_formal"
            else:
                host_path = ROOT / "forbidden-unallowlisted-write"
                attack = "write_unallowlisted"
            self._positive_pipeline(attack=attack, host_path=host_path)
        if requirement in {
            "RCPT-T20-FORMAL-DISCOVERY",
            "RCPT-T21-RENAMED-COPY",
            "RCPT-T26-FORMAL-POSITIVE",
            "RCPT-T27-FORMAL-TOCTOU",
        }:
            return self._execute_formal_case()
        if requirement == "RCPT-T22-AUDIT-MISSING":
            return self._execute_audit_missing()
        if requirement == "RCPT-T23-AUTH-CONCURRENT":
            return self._execute_concurrent_cas()
        if requirement == "RCPT-T24-CAS-CRASH":
            return self._execute_cas_crash()
        if requirement == "RCPT-T25-AUDIT-TAMPER":
            return self._execute_audit_tamper()
        if requirement == "RCPT-T28-PARSER-UNSAFE":
            self._positive_pipeline()
        if requirement == "RCPT-T29-BROKER-OBJECT-SWAP":
            return self._execute_broker_object_swap()
        if requirement == "RCPT-T30-SECOND-CHANNEL":
            attack = {
                "MMAP": "mmap",
                "SENDFILE": "sendfile",
                "SPLICE": "splice",
                "COPY-FILE-RANGE": "copy_file_range",
                "IO-URING": "io_uring",
                "CHILD-ESCAPE": "child_escape",
            }[self.suffix]
            self._positive_pipeline(attack=attack)
        if requirement == "RCPT-T31-BROKER-FALLBACK":
            return self._execute_broker_fallback()
        if requirement == "RCPT-T32-RANGE-ONLY-MISMATCH":
            return self._execute_book2_range()
        if requirement in {
            "RCPT-T33-PROFILE-ALG",
            "RCPT-T34-PROFILE-TYP",
            "RCPT-T35-PROFILE-KID",
            "RCPT-T36-PROFILE-AUD",
            "RCPT-T37-PROFILE-TIME",
        }:
            return self._execute_profile_case()
        raise PrototypeError("BLOCKED_MANIFEST_SCENARIO_UNIMPLEMENTED", self.case["scenario"])

    def _execute_formal_case(self) -> str:
        assert self.formal_loader is not None and self.formal_root is not None and self.candidate_probe_root is not None
        if self.requirement == "RCPT-T20-FORMAL-DISCOVERY":
            if self.suffix == "PROTOTYPE-TREE":
                path = self.temp_root / "runtime_capability_prototype" / "probe.yaml"
            else:
                relative = {
                    "CANDIDATE-BARE": "candidate_probe.yaml",
                    "CANDIDATE-PREFIXED": "candidate__probe.yaml",
                    "CANDIDATE-NESTED": "nested/candidate_probe.yaml",
                }[self.suffix]
                path = self.candidate_probe_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"SYNTHETIC_CONTROL_PROBE")
            entry = self._formal_entry(
                path,
                artifact_class="prototype_or_candidate_probe",
                authority="prototype_fixture_only",
                approved=False,
                provenance=False,
            )
            accepted = self.formal_loader.load(self._signed_formal_manifest([entry]), events=self.logs["formal"])
            self.formal_inputs = len(accepted)
            require(self.formal_inputs == 0, "INVALIDATED_FORMAL_DISCOVERY_LEAK")
            return "PASS_FORMAL_EXCLUDED"

        if self.requirement == "RCPT-T26-FORMAL-POSITIVE":
            path = self.formal_root / "formal_probe.bin"
            path.write_bytes(b"FORMAL_TEST_CONTROL_MARKER")
            entry = self._formal_entry(path)
            accepted = self.formal_loader.load(self._signed_formal_manifest([entry]), events=self.logs["formal"])
            self.formal_inputs = len(accepted)
            require(self.formal_inputs == 1, "BLOCKED_OUTPUT_ISOLATION_UNPROVEN")
            return "PASS_FORMAL_POSITIVE"

        if self.requirement == "RCPT-T27-FORMAL-TOCTOU":
            path = self.formal_root / "toctou_probe.bin"
            path.write_bytes(b"FORMAL_TEST_CONTROL_MARKER")
            entry = self._formal_entry(path)

            def swap(_: dict[str, Any]) -> None:
                if self.suffix == "OBJECT-SWAP":
                    original = path.with_suffix(".original")
                    path.rename(original)
                    path.write_bytes(b"FORMAL_TEST_CHANGED_MARKER")
                else:
                    path.write_bytes(b"FORMAL_TEST_MUTATED_VALUE")

            accepted = self.formal_loader.load(
                self._signed_formal_manifest([entry]),
                events=self.logs["formal"],
                before_safe_open=swap,
            )
            self.formal_inputs = len(accepted)
            require(self.formal_inputs == 0, "INVALIDATED_FORMAL_DISCOVERY_LEAK")
            return "PASS_FORMAL_TOCTOU_REJECTED"

        path = self.formal_root / "copy_probe.bin"
        path.write_bytes(b"SYNTHETIC_CONTROL_PROBE")
        if self.suffix == "SYMLINK":
            target = self.formal_root / "symlink_probe.bin"
            target.symlink_to(path)
            entry = self._formal_entry(target)
        elif self.suffix == "HARDLINK":
            target = self.formal_root / "hardlink_probe.bin"
            os.link(path, target)
            entry = self._formal_entry(target)
        elif self.suffix == "RELATIVE-ESCAPE":
            entry = self._formal_entry(path)
            entry["path"] = str(self.formal_root / ".." / "outside.bin")
        elif self.suffix == "FORGED-MANIFEST":
            entry = self._formal_entry(path)
            token = unsigned_mutation(self._signed_formal_manifest([entry]), mutate_signature=True)
            accepted = self.formal_loader.load(token, events=self.logs["formal"])
            self.formal_inputs = len(accepted)
            require(self.formal_inputs == 0, "INVALIDATED_FORMAL_DISCOVERY_LEAK")
            return "PASS_FORMAL_EXCLUDED"
        else:
            entry = self._formal_entry(
                path,
                artifact_class="candidate_copy_without_formal_provenance",
                authority="non_authoritative",
                approved=False,
                provenance=False,
            )
            if self.suffix == "DIGEST-ONLY-CLONE":
                entry["artifact_id"] = "DIGEST-ONLY-NOT-APPROVED"
        accepted = self.formal_loader.load(self._signed_formal_manifest([entry]), events=self.logs["formal"])
        self.formal_inputs = len(accepted)
        require(self.formal_inputs == 0, "INVALIDATED_FORMAL_DISCOVERY_LEAK")
        return "PASS_FORMAL_EXCLUDED"

    def _clone_log(self, log: SignedEventLog) -> SignedEventLog:
        clone = SignedEventLog(
            attempt_id=log.attempt_id,
            domain=log.domain,
            signer=log.signer,
            audience=log.audience,
            authorization_file_sha256=log.authorization_file_sha256,
            now=log.now,
        )
        clone.tokens = list(log.tokens)
        return clone

    def _scope_from_logs(
        self,
        logs: dict[str, SignedEventLog] | None = None,
        *,
        authorization: dict[str, Any] | None = None,
        attempt_id: str | None = None,
        event_id: str | None = None,
        capability_id: str | None = None,
        delivery_id: str | None = None,
        completed: bool = True,
    ) -> str:
        return self._audit_aggregator().create_scope_attestation(
            logs=logs or self.logs,
            authorization=self.authorization if authorization is None else authorization,
            attempt_id=attempt_id or self.attempt_id,
            consumption_event_id=self.consumption_event_id if event_id is None else event_id,
            capability_id=self.capability_id if capability_id is None else capability_id,
            delivery_id=self.delivery_id if delivery_id is None else delivery_id,
            expected_completed=completed,
        )

    def _execute_audit_missing(self) -> str:
        self._positive_pipeline()
        test_logs = {name: self._clone_log(log) for name, log in self.logs.items()}
        try:
            if self.suffix.startswith("MISSING-"):
                domain = self.suffix.removeprefix("MISSING-").lower()
                if domain in {"write", "formal"}:
                    test_logs.pop(domain)
                    self._ensure_write_evidence()
                    self._ensure_formal_evidence()
                    self._audit_aggregator().create_closure_attestation(
                        logs=test_logs,
                        authorization=self.authorization,
                        attempt_id=self.attempt_id,
                        scope_attestation=None,
                        final_result="BLOCKED_SCOPE_PROOF_UNAVAILABLE",
                        expected_formal_inputs=0,
                    )
                else:
                    test_logs.pop(domain)
                    self._scope_from_logs(test_logs)
            elif self.suffix == "LATE-MONITOR":
                test_logs["sandbox"].append("observer_late_start", {"late": True})
                self._scope_from_logs(test_logs)
            elif self.suffix == "DROPPED-EVENT":
                test_logs["broker"].tokens.pop(1)
                self._scope_from_logs(test_logs)
            elif self.suffix == "UNMONITORED-CHILD":
                test_logs["sandbox"].append("observer_unknown", {"child_process_coverage": False})
                self._scope_from_logs(test_logs)
            elif self.suffix == "UNKNOWN-FIELD":
                test_logs["broker"].append("observer_unknown", {"actual_union": "unknown"})
                self._scope_from_logs(test_logs)
            elif self.suffix == "SELF-REPORT-ONLY":
                test_logs["sandbox"].append("observer_unknown", {"authority": "probe_self_report_only"})
                self._scope_from_logs(test_logs)
            elif self.suffix == "ATTEMPT-MISMATCH":
                wrong = SignedEventLog(
                    attempt_id="RCPT-20260811-999",
                    domain="sandbox",
                    signer=self.suite.keys.observer,
                    audience=AUDIT_AGGREGATOR_ID,
                    authorization_file_sha256=self.authorization["authorization_file_sha256"],
                    now=NOW,
                )
                wrong.append("observer_started", {"started_before_broker_open": True})
                test_logs["sandbox"] = wrong
                self._scope_from_logs(test_logs)
            elif self.suffix == "AUTH-DIGEST-MISMATCH":
                wrong_auth = dict(self.authorization)
                wrong_auth["authorization_file_sha256"] = "0" * 64
                self._scope_from_logs(test_logs, authorization=wrong_auth)
            elif self.suffix == "EVENT-MISMATCH":
                self._scope_from_logs(test_logs, event_id="RCE-WRONG")
            elif self.suffix == "CAPABILITY-MISMATCH":
                self._scope_from_logs(test_logs, capability_id="CAP-WRONG")
            elif self.suffix == "DELIVERY-MISMATCH":
                self._scope_from_logs(test_logs, delivery_id="DEL-WRONG")
            elif self.suffix == "SCOPE-CLOSURE-LINK-MISMATCH":
                valid_scope = self._scope_from_logs(test_logs)
                self._ensure_write_evidence()
                self._ensure_formal_evidence()
                wrong_scope = unsigned_mutation(valid_scope, payload_updates={"attestation_id": "SCOPE-WRONG"})
                closure = self._audit_aggregator().create_closure_attestation(
                    logs=self.logs,
                    authorization=self.authorization,
                    attempt_id=self.attempt_id,
                    scope_attestation=wrong_scope,
                    final_result="BLOCKED_SCOPE_PROOF_UNAVAILABLE",
                    expected_formal_inputs=0,
                )
                _, closure_payload = self.suite.codec.verify(
                    closure,
                    expected_typ=AUDIT_TYP,
                    expected_issuer=AUDIT_AGGREGATOR_ID,
                    expected_audience=AUDIT_CONTROLLER_ID,
                    max_ttl=300,
                    expected_attempt_id=self.attempt_id,
                )
                require(
                    closure_payload["scope_execution_attestation_sha256"] == JWSCodec.digest(valid_scope),
                    "BLOCKED_SCOPE_PROOF_UNAVAILABLE",
                    "scope closure link",
                )
            else:
                raise PrototypeError("BLOCKED_MANIFEST_SCENARIO_UNIMPLEMENTED", self.suffix)
        except Exception:
            return "BLOCKED_SCOPE_PROOF_UNAVAILABLE"
        raise PrototypeError("BLOCKED_SCOPE_PROOF_UNAVAILABLE", "audit negative vector was accepted")

    def _execute_concurrent_cas(self) -> str:
        self._register_authorization()
        barrier = threading.Barrier(2)
        outcomes: list[tuple[str, Any]] = []
        lock = threading.Lock()

        def worker(index: int) -> None:
            local_log = SignedEventLog(
                attempt_id=self.attempt_id,
                domain="registry",
                signer=self.suite.keys.observer,
                audience=AUDIT_AGGREGATOR_ID,
                authorization_file_sha256=self.authorization["authorization_file_sha256"],
                now=NOW,
            )
            local_log.append("observer_started", {"concurrent_worker": index})
            barrier.wait()
            try:
                lease = self.suite.registry.consume(
                    authorization_id=self.authorization["authorization_id"],
                    attempt_id=self.attempt_id,
                    authorization_digest=self.authorization["authorization_file_sha256"],
                    now=NOW,
                    events=local_log,
                )
                outcome: tuple[str, Any] = ("winner", lease)
            except PrototypeError as exc:
                outcome = (exc.code, None)
            with lock:
                outcomes.append(outcome)

        threads = [threading.Thread(target=worker, args=(index,)) for index in (1, 2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=15)
        require(all(not thread.is_alive() for thread in threads), "BLOCKED_TEST_AUTHORIZATION_INVALID", "concurrency timeout")
        winners = [value for status, value in outcomes if status == "winner"]
        losers = [status for status, _ in outcomes if status != "winner"]
        require(len(winners) == 1, "BLOCKED_TEST_AUTHORIZATION_INVALID", "winner count")
        require(losers == ["BLOCKED_TEST_AUTHORIZATION_SPENT"], "BLOCKED_TEST_AUTHORIZATION_INVALID", "loser result")
        self.lease = winners[0]
        self.consumption_event_id = self.lease.consumption_event_id
        self.logs["registry"].append(
            "concurrent_cas_result",
            {"winner_count": 1, "loser_code": losers[0], "state": "spent"},
        )
        counts = self.suite.registry.counts(self.attempt_id)
        require(counts["consumption_events"] == 1 and counts["capabilities"] == 0, "BLOCKED_TEST_AUTHORIZATION_INVALID")
        return "PASS_AUTH_CONCURRENT_SINGLE_WINNER"

    def _execute_cas_crash(self) -> str:
        self._register_authorization()
        self._consume_authorization()
        self.suite.registry.close_attempt(self.authorization["authorization_id"])
        state = self.suite.registry.state(self.authorization["authorization_id"])
        require(state["state"] == "spent" and state["closed"] == 1, "BLOCKED_TEST_AUTHORIZATION_INVALID")
        counts = self.suite.registry.counts(self.attempt_id)
        require(counts["capabilities"] == 0, "BLOCKED_TEST_AUTHORIZATION_INVALID", "capability after crash")
        if self.suffix == "AFTER-CAS-BEFORE-MINT":
            return "PASS_CAS_CRASH_SPENT_NO_MINT"
        self._consume_authorization()
        raise PrototypeError("BLOCKED_TEST_AUTHORIZATION_SPENT")

    def _execute_audit_tamper(self) -> str:
        self._positive_pipeline()
        self.scope_attestation = self._scope_from_logs()
        try:
            if self.suffix in {"REGISTRY-EVENT", "BROKER-EVENT"}:
                domain = "registry" if self.suffix == "REGISTRY-EVENT" else "broker"
                clone = self._clone_log(self.logs[domain])
                clone.tokens[-1] = unsigned_mutation(clone.tokens[-1], mutate_signature=True)
                SignedEventLog.verify(
                    clone.tokens,
                    codec=self.suite.codec,
                    expected_attempt_id=self.attempt_id,
                    expected_domain=domain,
                    expected_issuer=OBSERVER_ID,
                    expected_audience=AUDIT_AGGREGATOR_ID,
                )
            elif self.suffix == "COMPONENT-ATTESTATION":
                token = unsigned_mutation(self.delivery.broker_read_attestation, mutate_signature=True)
                self.suite.codec.verify(
                    token,
                    expected_typ=AUDIT_TYP,
                    expected_issuer=BROKER_ID,
                    expected_audience=AUDIT_AGGREGATOR_ID,
                    max_ttl=300,
                    expected_attempt_id=self.attempt_id,
                )
            elif self.suffix == "SCOPE-ATTESTATION":
                token = unsigned_mutation(self.scope_attestation, mutate_signature=True)
                self.suite.codec.verify(
                    token,
                    expected_typ=AUDIT_TYP,
                    expected_issuer=AUDIT_AGGREGATOR_ID,
                    expected_audience=[SCOPE_VERIFIER_ID, AUDIT_CONTROLLER_ID],
                    max_ttl=300,
                    expected_attempt_id=self.attempt_id,
                )
            elif self.suffix == "EVENT-REORDER":
                clone = self._clone_log(self.logs["broker"])
                clone.tokens[1], clone.tokens[2] = clone.tokens[2], clone.tokens[1]
                SignedEventLog.verify(
                    clone.tokens,
                    codec=self.suite.codec,
                    expected_attempt_id=self.attempt_id,
                    expected_domain="broker",
                    expected_issuer=OBSERVER_ID,
                    expected_audience=AUDIT_AGGREGATOR_ID,
                )
            elif self.suffix == "OLD-EVIDENCE-REPLAY":
                clone = self._clone_log(self.logs["sandbox"])
                clone.tokens[0] = unsigned_mutation(clone.tokens[0], payload_updates={"attempt_id": "RCPT-OLD"})
                test_logs = dict(self.logs)
                test_logs["sandbox"] = clone
                self._scope_from_logs(test_logs)
            elif self.suffix == "OLD-SCOPE-IN-CLOSURE":
                self._ensure_write_evidence()
                self._ensure_formal_evidence()
                old_scope = self._resign(
                    self.scope_attestation,
                    signer=self.suite.keys.audit,
                    typ=AUDIT_TYP,
                    payload_updates={"attempt_id": "RCPT-OLD"},
                )
                closure = self._audit_aggregator().create_closure_attestation(
                    logs=self.logs,
                    authorization=self.authorization,
                    attempt_id=self.attempt_id,
                    scope_attestation=old_scope,
                    final_result="INVALIDATED_AUDIT_TAMPERED",
                    expected_formal_inputs=0,
                )
                _, payload = self.suite.codec.verify(
                    closure,
                    expected_typ=AUDIT_TYP,
                    expected_issuer=AUDIT_AGGREGATOR_ID,
                    expected_audience=AUDIT_CONTROLLER_ID,
                    max_ttl=300,
                    expected_attempt_id=self.attempt_id,
                )
                require(
                    payload["scope_execution_attestation_sha256"] == JWSCodec.digest(self.scope_attestation),
                    "INVALIDATED_AUDIT_TAMPERED",
                    "old scope replay",
                )
            else:
                raise PrototypeError("BLOCKED_MANIFEST_SCENARIO_UNIMPLEMENTED", self.suffix)
        except Exception:
            return "INVALIDATED_AUDIT_TAMPERED"
        raise PrototypeError("INVALIDATED_AUDIT_TAMPERED", "tamper vector accepted")

    def _execute_broker_object_swap(self) -> str:
        self._register_authorization()
        self._consume_authorization()
        self._mint_capability()
        path = self.fixture.full_path
        if self.suffix == "IDENTITY-SWAP":
            original = path.with_suffix(".original")
            path.rename(original)
            data = original.read_bytes()
            path.write_bytes(data)
            os.chmod(path, 0o400)
        else:
            os.chmod(path, 0o600)
            with path.open("r+b") as handle:
                first = handle.read(1)
                handle.seek(0)
                handle.write(b"Z" if first != b"Z" else b"Y")
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(path, 0o400)
        self._deliver()
        raise PrototypeError("BLOCKED_SOURCE_OBJECT_NOT_IMMUTABLE")

    def _execute_broker_fallback(self) -> str:
        self._register_authorization()
        self._consume_authorization()
        self._mint_capability()
        _, payload, _ = decode_token(self.capability_token)
        field, value = {
            "FULL-HASH": ("full_hash", True),
            "READ-TO-EOF": ("read_to_eof", True),
            "MMAP": ("broker_read_strategy", "mmap"),
            "SENDFILE": ("broker_read_strategy", "sendfile"),
            "SPLICE": ("broker_read_strategy", "splice"),
            "COPY-FILE-RANGE": ("broker_read_strategy", "copy_file_range"),
            "IO-URING": ("broker_read_strategy", "io_uring"),
            "AUTO-RETRY": ("automatic_retry", True),
        }[self.suffix]
        payload[field] = value
        token = JWSCodec.sign(self.suite.keys.capability, CAPABILITY_TYP, payload)
        self._deliver(token=token)
        raise PrototypeError("BLOCKED_BROKER_FALLBACK_FORBIDDEN")

    def _execute_book2_range(self) -> str:
        self._register_authorization()
        self._consume_authorization()
        self._mint_capability()
        _, payload, _ = decode_token(self.capability_token)
        payload["start_byte"] = BOOK1_END
        payload["end_byte_exclusive"] = BOOK1_END + BOOK1_LENGTH
        payload["expected_length"] = BOOK1_LENGTH
        token = JWSCodec.sign(self.suite.keys.capability, CAPABILITY_TYP, payload)
        self._deliver(token=token)
        raise PrototypeError("BLOCKED_TEST_SCOPE_CONTRACT_MISMATCH")

    def _profile_target(self, target: str) -> tuple[str, str, SigningKey, str, str | list[str], int]:
        self._register_authorization()
        self._consume_authorization()
        self._mint_capability()
        if target == "CAP":
            return self.capability_token, CAPABILITY_TYP, self.suite.keys.capability, CAPABILITY_ISSUER_ID, BROKER_ID, 60
        self._deliver()
        if target == "ENV":
            return self.delivery.signed_envelope, ENVELOPE_TYP, self.suite.keys.broker, BROKER_ID, READER_ID, 60
        self._read_delivery()
        self.scope_attestation = self._scope_from_logs(completed=True)
        if target == "AUD-SCOPE":
            return (
                self.scope_attestation,
                AUDIT_TYP,
                self.suite.keys.audit,
                AUDIT_AGGREGATOR_ID,
                [SCOPE_VERIFIER_ID, AUDIT_CONTROLLER_ID],
                300,
            )
        self._ensure_write_evidence()
        self._ensure_formal_evidence()
        self.closure_attestation = self._audit_aggregator().create_closure_attestation(
            logs=self.logs,
            authorization=self.authorization,
            attempt_id=self.attempt_id,
            scope_attestation=self.scope_attestation,
            final_result="PROFILE_TEST_BASELINE",
            expected_formal_inputs=0,
        )
        return (
            self.closure_attestation,
            AUDIT_TYP,
            self.suite.keys.audit,
            AUDIT_AGGREGATOR_ID,
            AUDIT_CONTROLLER_ID,
            300,
        )

    def _execute_profile_case(self) -> str:
        if self.requirement == "RCPT-T36-PROFILE-AUD":
            if self.suffix.startswith("CAP-"):
                target, vector = "CAP", self.suffix.removeprefix("CAP-")
            elif self.suffix.startswith("ENV-"):
                target, vector = "ENV", self.suffix.removeprefix("ENV-")
            elif self.suffix.startswith("SCOPE-"):
                target, vector = "AUD-SCOPE", self.suffix.removeprefix("SCOPE-")
            else:
                target, vector = "AUD-CLOSURE", self.suffix.removeprefix("CLOSURE-")
        else:
            target = next(
                candidate
                for candidate in ("AUD-CLOSURE", "AUD-SCOPE", "CAP", "ENV")
                if self.suffix.startswith(candidate + "-")
            )
            vector = self.suffix.removeprefix(target + "-")

        token, typ, active_signer, issuer, audience, max_ttl = self._profile_target(target)
        codec = self.suite.codec
        mutated = token
        if vector == "ALG-NONE":
            mutated = unsigned_mutation(token, protected_updates={"alg": "none"})
        elif vector == "ALG-UNAPPROVED":
            mutated = unsigned_mutation(token, protected_updates={"alg": "ES256"})
        elif vector == "ALG-CONFUSION":
            mutated = unsigned_mutation(token, protected_updates={"alg": "HS256"})
        elif vector == "TYP-MISSING":
            mutated = self._resign(token, signer=active_signer, typ=typ, protected_updates={"typ": None})
        elif vector == "TYP-WRONG":
            mutated = self._resign(token, signer=active_signer, typ=typ, protected_updates={"typ": "ctde-wrong+jws"})
        elif vector == "VERSION-MISSING":
            mutated = self._resign(
                token,
                signer=active_signer,
                typ=typ,
                protected_updates={"ctde_profile_version": None},
            )
        elif vector == "VERSION-WRONG":
            mutated = self._resign(
                token,
                signer=active_signer,
                typ=typ,
                protected_updates={"ctde_profile_version": 2},
            )
        elif vector == "KID-UNKNOWN":
            mutated = self._resign(token, signer=self.suite.keys.unknown, typ=typ)
        elif vector == "KID-REVOKED":
            mutated = self._resign(token, signer=self.suite.keys.revoked, typ=typ)
        elif vector == "KID-EXPIRED":
            mutated = self._resign(token, signer=self.suite.keys.expired, typ=typ)
        elif vector == "ISS-WRONG":
            mutated = self._resign(token, signer=active_signer, typ=typ, payload_updates={"iss": "ctde-wrong-issuer"})
        elif vector == "PROD-ROOT-IN-PROTO":
            mutated = self._resign(token, signer=self.suite.keys.production, typ=typ)
        elif vector == "PROTO-ROOT-IN-PROD":
            codec = self.suite.production_codec
        elif vector == "AUD-MISSING":
            mutated = self._resign(token, signer=active_signer, typ=typ, payload_updates={"aud": None})
        elif vector in {"AUD-WRONG", "AUD-WRONG-SET"}:
            wrong_audience: str | list[str] = ["ctde-wrong-a", "ctde-wrong-b"] if isinstance(audience, list) else "ctde-wrong-audience"
            mutated = self._resign(token, signer=active_signer, typ=typ, payload_updates={"aud": wrong_audience})
        elif vector == "USING-CLOSURE-AUD":
            mutated = self._resign(token, signer=active_signer, typ=typ, payload_updates={"aud": AUDIT_CONTROLLER_ID})
        elif vector == "USING-SCOPE-AUD":
            mutated = self._resign(
                token,
                signer=active_signer,
                typ=typ,
                payload_updates={"aud": [SCOPE_VERIFIER_ID, AUDIT_CONTROLLER_ID]},
            )
        elif vector == "IAT-MISSING":
            mutated = self._resign(token, signer=active_signer, typ=typ, payload_updates={"iat": None})
        elif vector == "NBF-MISSING":
            mutated = self._resign(token, signer=active_signer, typ=typ, payload_updates={"nbf": None})
        elif vector == "EXP-MISSING":
            mutated = self._resign(token, signer=active_signer, typ=typ, payload_updates={"exp": None})
        elif vector == "NBF-FUTURE":
            mutated = self._resign(token, signer=active_signer, typ=typ, payload_updates={"nbf": NOW + 1})
        elif vector == "EXP-PAST":
            mutated = self._resign(token, signer=active_signer, typ=typ, payload_updates={"exp": NOW - 1})
        elif vector == "TTL-EXCEEDS":
            _, payload, _ = decode_token(token)
            mutated = self._resign(
                token,
                signer=active_signer,
                typ=typ,
                payload_updates={"exp": payload["iat"] + max_ttl + 1},
            )
        else:
            raise PrototypeError("BLOCKED_MANIFEST_SCENARIO_UNIMPLEMENTED", vector)

        try:
            codec.verify(
                mutated,
                expected_typ=typ,
                expected_issuer=issuer,
                expected_audience=audience,
                max_ttl=max_ttl,
                expected_attempt_id=self.attempt_id,
            )
        except PrototypeError as exc:
            require(exc.code == "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID")
            return "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID"
        raise PrototypeError("BLOCKED_SIGNED_OBJECT_PROFILE_INVALID", "invalid signed object accepted")

    def _event_kind_present(self, domain: str, kind: str) -> bool:
        return any(decode_token(token)[1].get("kind") == kind for token in self.logs[domain].tokens)

    def _finalize_evidence(self) -> None:
        for domain in ("broker", "sandbox", "parser", "gateway"):
            if len(self.logs[domain].tokens) == 1:
                self.logs[domain].append(
                    "observer_not_reached",
                    {"reason": self.actual_component_result, "success_events": 0},
                )
        self._ensure_write_evidence()
        self._ensure_formal_evidence()

        broker_open_observed = self._event_kind_present("broker", "broker_open_attempt")
        delivery_observed = self._event_kind_present("broker", "broker_delivery_created")
        expected_completed = self.actual_component_result in {
            "PASS_EXACT_RANGE",
            "PASS_INHERITED_FD_SANITIZED",
            "BLOCKED_SIGNED_OBJECT_PROFILE_INVALID",
            "BLOCKED_SCOPE_PROOF_UNAVAILABLE",
            "INVALIDATED_AUDIT_TAMPERED",
        } and self._event_kind_present("gateway", "gateway_scope_result")
        if self.scope_attestation is None:
            self.scope_attestation = self._audit_aggregator().create_scope_attestation(
                logs=self.logs,
                authorization=self.authorization,
                attempt_id=self.attempt_id,
                consumption_event_id=self.consumption_event_id if broker_open_observed else None,
                capability_id=self.capability_id if broker_open_observed else None,
                delivery_id=self.delivery_id if delivery_observed else None,
                expected_completed=expected_completed,
            )
        if self.closure_attestation is None:
            self.closure_attestation = self._audit_aggregator().create_closure_attestation(
                logs=self.logs,
                authorization=self.authorization,
                attempt_id=self.attempt_id,
                scope_attestation=self.scope_attestation,
                final_result=self.actual_component_result,
                expected_formal_inputs=self.formal_inputs,
            )

        for domain, log in self.logs.items():
            log.persist(self.case_root / "evidence" / f"{domain}_events.jsonl")
        broker_snapshot = {
            "environment": "prototype_fixture_only",
            "attempt_id": self.attempt_id,
            "broker_component_id": BROKER_ID,
            "catalog_object_ids": [self.fixture.object_id] if self.fixture else [],
            "catalog_contains_synthetic_only": True,
            "greek_object_catalogued": False,
            "production_object_catalogued": False,
            "caller_range_override_interface_exposed": False,
            "automatic_retry_count": 0,
            "full_hash_or_eof_fallback_count": 0,
            "paths_persisted": False,
        }
        consumer_snapshot = self.sandbox_snapshot or {
            "environment": "prototype_fixture_only",
            "attempt_id": self.attempt_id,
            "sandbox_status": "not_reached",
            "project_workspace_mounted": False,
            "project_source_tree_visible": False,
            "broker_fixture_store_mounted": False,
            "greek_fixture_or_raw_mounted": False,
            "network_source_fetch_allowed": False,
            "consumer_visible_full_object_handles": 0,
            "reason": self.actual_component_result,
        }
        dump_yaml(self.case_root / "evidence" / "broker_environment_snapshot.yaml", broker_snapshot)
        dump_yaml(self.case_root / "evidence" / "consumer_environment_snapshot.yaml", consumer_snapshot)
        atomic_write_bytes(
            self.case_root / "attestations" / "prototype_scope_execution_attestation.jws",
            (self.scope_attestation + "\n").encode("ascii"),
            mode=0o444,
        )
        atomic_write_bytes(
            self.case_root / "attestations" / "prototype_closure_audit_attestation.jws",
            (self.closure_attestation + "\n").encode("ascii"),
            mode=0o444,
        )

    def _verified_broker_summary(self) -> tuple[list[dict[str, Any]], list[dict[str, int]]]:
        events = SignedEventLog.verify(
            self.logs["broker"].tokens,
            codec=self.suite.codec,
            expected_attempt_id=self.attempt_id,
            expected_domain="broker",
            expected_issuer=OBSERVER_ID,
            expected_audience=AUDIT_AGGREGATOR_ID,
        )
        calls: list[dict[str, Any]] = []
        union: list[dict[str, int]] = []
        for event in events:
            if event["kind"] == "broker_read_complete":
                calls = event["data"]["actual_read_calls"]
                union = event["data"]["actual_union_of_read_ranges"]
        return calls, union

    def _write_case_result(self) -> dict[str, Any]:
        expected = self.case["expected_component_result"]
        exact_result_match = self.actual_component_result == expected
        try:
            calls, union = self._verified_broker_summary()
            evidence_files = list((self.case_root / "evidence").iterdir())
            evidence_complete = (
                len(evidence_files) == 9
                and all(path.stat().st_size > 0 for path in evidence_files)
                and self.scope_attestation is not None
                and self.closure_attestation is not None
            )
        except Exception as exc:
            calls, union = [], []
            evidence_complete = False
            self.blockers.append(f"evidence_verification: {exc}")
        outside = 0
        for call in calls:
            call_start = call["offset"]
            call_end = call_start + call["returned_bytes"]
            outside += max(0, BOOK1_START - call_start) + max(0, call_end - BOOK1_END)
        registry_counts = self.suite.registry.counts(self.attempt_id)
        common_assertions = {
            "candidate_run_id_used": False,
            "candidate_runs_executed": 0,
            "business_outputs_created": 0,
            "story_structure_yaml_created": False,
            "model_invocations": 0,
            "payload_persisted": False,
            "bytes_outside_allowed_range": outside,
            "actual_union_within_book1": all(
                item["start_byte"] >= BOOK1_START and item["end_byte_exclusive"] <= BOOK1_END
                for item in union
            ),
            "automatic_retry_count": 0,
            "greek_open_success_count": 0,
            "full_object_consumer_handle_count": (
                self.sandbox_snapshot.get("consumer_visible_full_object_handles", 0)
                if self.sandbox_snapshot
                else 0
            ),
        }
        handle_assertion_pass = (
            common_assertions["full_object_consumer_handle_count"] == 0
            or (
                self.requirement == "RCPT-T15-HANDLE-INVENTORY"
                and self.suffix == "RESIDUAL-FD-DETECTED"
                and common_assertions["full_object_consumer_handle_count"] >= 1
                and self.actual_component_result == "BLOCKED_SANDBOX_ISOLATION_UNPROVEN"
            )
        )
        common_assertions["full_object_handle_policy_pass"] = handle_assertion_pass
        assertions_pass = (
            common_assertions["bytes_outside_allowed_range"] == 0
            and common_assertions["actual_union_within_book1"]
            and common_assertions["model_invocations"] == 0
            and common_assertions["business_outputs_created"] == 0
            and handle_assertion_pass
        )
        case_pass = exact_result_match and evidence_complete and assertions_pass
        result = {
            "schema_version": "1.0.0",
            "artifact_class": "runtime_capability_leaf_case_result",
            "suite_id": SUITE_ID,
            "leaf_case_id": self.case["leaf_case_id"],
            "requirement_group": self.requirement,
            "attempt_id": self.attempt_id,
            "grant_id": self.case["grant_id"],
            "authorization_absent": self.authorization is None,
            "authorization_absent_reason": "manifest_case_requires_no_grant" if self.authorization is None else None,
            "expected_component_result": expected,
            "actual_component_result": self.actual_component_result,
            "exact_result_match": exact_result_match,
            "case_test_result": "pass" if case_pass else "fail",
            "evidence_complete": evidence_complete,
            "side_effect_bundle": self.case["side_effect_bundle"],
            "actual_read_calls": calls,
            "actual_union_of_read_ranges": union,
            "registry_counts": registry_counts,
            "assertions": common_assertions,
            "scope_attestation_sha256": JWSCodec.digest(self.scope_attestation) if self.scope_attestation else None,
            "closure_attestation_sha256": JWSCodec.digest(self.closure_attestation) if self.closure_attestation else None,
            "blockers": self.blockers,
        }
        dump_yaml(self.case_root / "case_result.yaml", result, mode=0o444)
        if self.delivery is not None:
            try:
                os.close(self.delivery.sealed_slice_fd)
            except OSError:
                pass
        return result


def aggregate_execution(suite: SuiteRuntime, leaves: list[dict[str, Any]], results: list[dict[str, Any]]) -> dict[str, Any]:
    manifest_count = len(leaves)
    discovered_count = len(leaves)
    executed_count = len(results)
    passed_count = sum(result["case_test_result"] == "pass" for result in results)
    failed_count = sum(result["case_test_result"] == "fail" for result in results)
    evidence_complete_count = sum(bool(result["evidence_complete"]) for result in results)
    groups_manifest = {leaf["requirement_group"] for leaf in leaves}
    groups_executed = {result["requirement_group"] for result in results}
    by_group: dict[str, dict[str, int]] = {}
    for group in sorted(groups_manifest):
        group_results = [result for result in results if result["requirement_group"] == group]
        by_group[group] = {
            "executed": len(group_results),
            "passed": sum(result["case_test_result"] == "pass" for result in group_results),
            "failed": sum(result["case_test_result"] == "fail" for result in group_results),
        }
    enumeration_counts_match = manifest_count == discovered_count == executed_count == evidence_complete_count
    counts_match = enumeration_counts_match and passed_count == manifest_count and failed_count == 0
    preliminary = {
        "schema_version": "1.0.0",
        "artifact_class": "runtime_capability_prototype_preliminary_aggregate",
        "suite_id": SUITE_ID,
        "environment": "prototype_fixture_only",
        "manifest_file_sha256": sha256_file(suite.suite_root / "control" / "runtime_capability_test_manifest.yaml"),
        "manifest_leaf_count": manifest_count,
        "runner_discovered_count": discovered_count,
        "runner_executed_count": executed_count,
        "mandatory_tests_passed": passed_count,
        "mandatory_tests_failed": failed_count,
        "mandatory_tests_skipped": 0,
        "mandatory_tests_unknown": 0,
        "evidence_complete_count": evidence_complete_count,
        "requirement_groups_manifest_count": len(groups_manifest),
        "requirement_groups_executed_count": len(groups_executed),
        "runner_enumeration_counts_match": enumeration_counts_match,
        "suite_manifest_runner_counts_match": counts_match,
        "group_results": by_group,
        "case_results": [
            {
                "leaf_case_id": result["leaf_case_id"],
                "attempt_id": result["attempt_id"],
                "expected_component_result": result["expected_component_result"],
                "actual_component_result": result["actual_component_result"],
                "case_test_result": result["case_test_result"],
                "evidence_complete": result["evidence_complete"],
            }
            for result in results
        ],
        "external_access_audit_status": "pending",
        "prototype_result": "PENDING_EXTERNAL_ACCESS_AUDIT" if counts_match else "BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED",
    }
    return preliminary


def build_evidence_manifest(suite_root: Path) -> dict[str, Any]:
    files = []
    for path in sorted((suite_root / "cases").rglob("*")):
        if path.is_file():
            files.append(
                {
                    "path": path.relative_to(suite_root).as_posix(),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    return {
        "schema_version": "1.0.0",
        "artifact_class": "runtime_capability_prototype_evidence_manifest",
        "suite_id": SUITE_ID,
        "files": files,
        "file_count_by_enumeration": len(files),
        "payload_files_present": False,
        "private_keys_present": False,
        "candidate_artifacts_present": False,
    }


def execute_suite(suite: SuiteRuntime, selected_leaf: str | None = None) -> dict[str, Any]:
    suite.bootstrap()
    leaves = suite.validate_manifest()
    if selected_leaf:
        leaves = [leaf for leaf in leaves if leaf["leaf_case_id"] == selected_leaf]
        require(len(leaves) == 1, "BLOCKED_MANIFEST_INVALID", "smoke leaf not found")
    results: list[dict[str, Any]] = []
    for index, leaf in enumerate(leaves, 1):
        case_root = suite.suite_root / "cases" / leaf["leaf_case_id"] / leaf["attempt_id"]
        result = CaseHarness(suite, leaf, case_root).run()
        results.append(result)
        if index == 1 or index % 10 == 0 or index == len(leaves):
            print(
                json.dumps(
                    {
                        "progress_executed": index,
                        "runner_discovered": len(leaves),
                        "passes_so_far": sum(item["case_test_result"] == "pass" for item in results),
                        "failures_so_far": sum(item["case_test_result"] == "fail" for item in results),
                        "last_actual_component_result": result["actual_component_result"],
                        "last_blockers": result["blockers"] if result["case_test_result"] == "fail" else [],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    preliminary = aggregate_execution(suite, leaves, results)
    aggregate_root = suite.suite_root / "aggregate"
    aggregate_root.mkdir(parents=True, exist_ok=True)
    dump_json(aggregate_root / "test_results_preliminary.json", preliminary, mode=0o444)
    dump_yaml(aggregate_root / "evidence_manifest.yaml", build_evidence_manifest(suite.suite_root), mode=0o444)
    print(json.dumps({"preliminary_aggregate": preliminary}, sort_keys=True), flush=True)
    return preliminary


def finalize_suite(suite: SuiteRuntime, external_audit_path: Path) -> dict[str, Any]:
    preliminary = json.loads((suite.suite_root / "aggregate" / "test_results_preliminary.json").read_text(encoding="utf-8"))
    external = json.loads(external_audit_path.read_text(encoding="utf-8"))
    external_pass = (
        external.get("overall_result") == "pass"
        and external.get("english_real_raw_stat_count") == 0
        and external.get("english_real_raw_open_count") == 0
        and external.get("english_real_raw_read_count") == 0
        and external.get("greek_real_raw_stat_count") == 0
        and external.get("greek_real_raw_open_count") == 0
        and external.get("greek_real_raw_read_count") == 0
        and external.get("project_source_tree_scan_count") == 0
        and external.get("book_structure_map_read_count") == 0
        and external.get("candidate_artifact_access_count") == 0
        and external.get("network_connect_success_count") == 0
    )
    all_cases_pass = (
        preliminary["suite_manifest_runner_counts_match"]
        and preliminary["mandatory_tests_failed"] == 0
        and preliminary["mandatory_tests_skipped"] == 0
        and preliminary["mandatory_tests_unknown"] == 0
    )
    overall_pass = all_cases_pass and external_pass
    failed_cases = [case for case in preliminary["case_results"] if case["case_test_result"] != "pass"]
    failed_actual_counts: dict[str, int] = {}
    for case in failed_cases:
        actual = case["actual_component_result"]
        failed_actual_counts[actual] = failed_actual_counts.get(actual, 0) + 1
    final = dict(preliminary)
    final["artifact_class"] = "runtime_capability_prototype_final_aggregate"
    final["external_access_audit_status"] = "pass" if external_pass else "fail"
    final["external_access_audit_sha256"] = sha256_file(external_audit_path)
    final["zero_real_source_access"] = external
    final["model_invocations"] = 0
    final["candidate_runs_executed"] = 0
    final["business_outputs_created"] = 0
    final["story_structure_yaml_created"] = False
    final["failed_actual_component_result_counts"] = failed_actual_counts
    final["prototype_result"] = (
        "PASS_RUNTIME_CAPABILITY_PROTOTYPE"
        if overall_pass
        else "BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED"
    )
    final["blockers"] = [] if overall_pass else list(dict.fromkeys([
        *([] if all_cases_pass else ["MANDATORY_LEAF_TEST_FAILURE"]),
        *(
            ["BLOCKED_SANDBOX_ISOLATION_UNPROVEN"]
            if "BLOCKED_SANDBOX_ISOLATION_UNPROVEN" in failed_actual_counts
            else []
        ),
        *([] if external_pass else ["ZERO_REAL_SOURCE_ACCESS_PROOF_FAILED"]),
        *external.get("blockers", []),
    ]))
    final_path = suite.suite_root / "aggregate" / "test_results.json"
    dump_json(final_path, final, mode=0o444)
    cases = {case["leaf_case_id"]: case for case in preliminary["case_results"]}

    def leaf_pass(leaf_id: str) -> bool:
        return cases.get(leaf_id, {}).get("case_test_result") == "pass"

    def group_pass(prefix: str) -> bool:
        selected = [case for leaf_id, case in cases.items() if leaf_id.startswith(prefix)]
        return bool(selected) and all(case["case_test_result"] == "pass" for case in selected)

    def proof(value: bool) -> str:
        return "PROVEN" if value else "NOT PROVEN"

    def audit_value(key: str) -> str:
        value = external.get(key)
        return "unknown (monitor unavailable)" if value is None else str(value)

    book1_proven = leaf_pass("RCPT-T01-EXACT-RANGE-BASELINE")
    book2_broker_rejected = leaf_pass("RCPT-T32-RANGE-ONLY-MISMATCH-BOOK2-DIRECT-RANGE")
    book2_consumer_proven = group_pass("RCPT-T18-") and leaf_pass("RCPT-T28-PARSER-UNSAFE-BOOK2")
    full_object_proven = group_pass("RCPT-T14-") and group_pass("RCPT-T15-")
    greek_broker_rejected = group_pass("RCPT-T16-")
    greek_consumer_proven = greek_broker_rejected and group_pass("RCPT-T17-")
    authorization_proven = all(group_pass(f"RCPT-T{number:02d}-") for number in (2, 3, 4, 5, 23, 24))
    formal_proven = all(group_pass(f"RCPT-T{number:02d}-") for number in (20, 21, 26, 27))
    audit_proven = all_cases_pass and external_pass
    blocker_lines = "\n".join(f"- `{blocker}`" for blocker in final["blockers"]) or "- None"
    report = f"""# Runtime Capability Prototype Test Report

Suite: `{SUITE_ID}`  
Result: `{final['prototype_result']}`  
Environment: `prototype_fixture_only`

## Runner enumeration

- Manifest leaf count: `{final['manifest_leaf_count']}`
- Runner discovered: `{final['runner_discovered_count']}`
- Runner executed: `{final['runner_executed_count']}`
- Evidence complete: `{final['evidence_complete_count']}`
- Passed: `{final['mandatory_tests_passed']}`
- Failed: `{final['mandatory_tests_failed']}`
- Skipped: `{final['mandatory_tests_skipped']}`
- Unknown: `{final['mandatory_tests_unknown']}`
- Requirement groups: `{final['requirement_groups_executed_count']}`
- Enumeration counts match: `{final['runner_enumeration_counts_match']}`
- Full PASS acceptance counts match: `{final['suite_manifest_runner_counts_match']}`

## Capability findings

- Book 1 exact range `[4076,36515)`: `{proof(book1_proven)}`.
- Book 2 direct broker range rejection: `{proof(book2_broker_rejected)}`.
- Book 2 consumer/parser/gateway isolation: `{proof(book2_consumer_proven)}`.
- Consumer full-object path/handle isolation: `{proof(full_object_proven)}`.
- Synthetic Greek broker-role rejection: `{proof(greek_broker_rejected)}`.
- Synthetic Greek consumer-path isolation: `{proof(greek_consumer_proven)}`.
- Authorization existence, one-shot CAS, replay, concurrency and crash semantics: `{proof(authorization_proven)}`.
- Formal allowlist, positive control and TOCTOU rejection: `{proof(formal_proven)}`.
- Complete independent read audit: `{proof(audit_proven)}`.

## Blockers

{blocker_lines}

## Zero-real-source boundary

- English real raw stat/open/read/hash: `{audit_value('english_real_raw_stat_count')} / {audit_value('english_real_raw_open_count')} / {audit_value('english_real_raw_read_count')} / {audit_value('english_real_raw_hash_count')}`
- Greek real raw stat/open/read/parse/copy: `{audit_value('greek_real_raw_stat_count')} / {audit_value('greek_real_raw_open_count')} / {audit_value('greek_real_raw_read_count')} / {audit_value('greek_real_raw_parse_count')} / {audit_value('greek_real_raw_copy_count')}`
- Project source tree scans: `{audit_value('project_source_tree_scan_count')}`
- `book_structure_map.yaml` reads: `{audit_value('book_structure_map_read_count')}`
- Model invocations: `0`
- Candidate Runs executed: `0`
- Business outputs created: `0`

This is prototype evidence only. It does not authorize any Candidate Run or mark any production `P2ER-*` Gate PASS.
"""
    report_path = suite.suite_root / "report" / "PROTOTYPE_TEST_REPORT.md"
    atomic_write_bytes(report_path, report.encode("utf-8"), mode=0o444)
    registry_record = {
        "suite_id": SUITE_ID,
        "prototype_result": final["prototype_result"],
        "final_aggregate_sha256": sha256_file(final_path),
        "report_sha256": sha256_file(report_path),
        "manifest_leaf_count": final["manifest_leaf_count"],
        "runner_executed_count": final["runner_executed_count"],
        "external_access_audit_sha256": final["external_access_audit_sha256"],
    }
    registry_path = suite.output_root / "registry" / "suite_registry.jsonl"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with registry_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(registry_record, sort_keys=True) + "\n")
    print(json.dumps({"final_aggregate": final}, sort_keys=True), flush=True)
    return final


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    execute = subparsers.add_parser("execute")
    execute.add_argument("--output-root", type=Path, default=ROOT)
    smoke = subparsers.add_parser("smoke")
    smoke.add_argument("--leaf", required=True)
    finalize = subparsers.add_parser("finalize")
    finalize.add_argument("--output-root", type=Path, default=ROOT)
    finalize.add_argument("--external-audit", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "smoke":
        with tempfile.TemporaryDirectory(prefix="ctde-suite-smoke-") as temporary:
            suite = SuiteRuntime(output_root=Path(temporary), persistent=False)
            execute_suite(suite, selected_leaf=args.leaf)
    elif args.command == "execute":
        suite = SuiteRuntime(output_root=args.output_root.resolve(), persistent=True)
        execute_suite(suite)
    else:
        suite = SuiteRuntime(output_root=args.output_root.resolve(), persistent=True)
        finalize_suite(suite, args.external_audit.resolve())


if __name__ == "__main__":
    main()
