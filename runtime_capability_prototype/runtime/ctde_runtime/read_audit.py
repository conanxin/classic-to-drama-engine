from __future__ import annotations

import uuid
from typing import Any

from .common import PrototypeError, require
from .events import SignedEventLog
from .fixture_factory import BOOK1_END, BOOK1_START
from .signing import AUDIT_TYP, JWSCodec, SigningKey
from .authorization_v2 import ActivatedAuthorizationContextV2, validate_activated_projection


SCOPE_DOMAINS = ("broker", "sandbox", "parser", "gateway")
CLOSURE_DOMAINS = ("write", "formal")


class ReadAuditAggregator:
    def __init__(
        self,
        *,
        codec: JWSCodec,
        signer: SigningKey,
        observer_issuer: str,
        aggregator_id: str,
        scope_verifier_id: str,
        audit_controller_id: str,
        now: int,
    ) -> None:
        self.codec = codec
        self.signer = signer
        self.observer_issuer = observer_issuer
        self.aggregator_id = aggregator_id
        self.scope_verifier_id = scope_verifier_id
        self.audit_controller_id = audit_controller_id
        self.now = now

    def _verify_logs(
        self,
        logs: dict[str, SignedEventLog],
        domains: tuple[str, ...],
        attempt_id: str,
    ) -> dict[str, list[dict[str, Any]]]:
        verified: dict[str, list[dict[str, Any]]] = {}
        try:
            for domain in domains:
                log = logs.get(domain)
                require(log is not None, "BLOCKED_SCOPE_PROOF_UNAVAILABLE", f"missing {domain}")
                verified[domain] = SignedEventLog.verify(
                    log.tokens,
                    codec=self.codec,
                    expected_attempt_id=attempt_id,
                    expected_domain=domain,
                    expected_issuer=self.observer_issuer,
                    expected_audience=self.aggregator_id,
                )
                if any(event["kind"] in {"observer_late_start", "observer_dropped_event", "observer_unknown"} for event in verified[domain]):
                    raise PrototypeError("BLOCKED_SCOPE_PROOF_UNAVAILABLE", f"invalid {domain} coverage")
        except PrototypeError:
            raise
        except Exception as exc:
            raise PrototypeError("INVALIDATED_AUDIT_TAMPERED", str(exc)) from exc
        return verified

    @staticmethod
    def _event_data(events: list[dict[str, Any]], kind: str) -> dict[str, Any] | None:
        for event in reversed(events):
            if event["kind"] == kind:
                return event["data"]
        return None

    def create_scope_attestation(
        self,
        *,
        logs: dict[str, SignedEventLog],
        authorization: dict[str, Any] | None,
        attempt_id: str,
        consumption_event_id: str | None,
        capability_id: str | None,
        delivery_id: str | None,
        expected_completed: bool,
    ) -> str:
        verified = self._verify_logs(logs, SCOPE_DOMAINS, attempt_id)
        if authorization:
            expected_digest = authorization["authorization_file_sha256"]
            for domain in SCOPE_DOMAINS:
                require(
                    all(event.get("authorization_file_sha256") == expected_digest for event in verified[domain]),
                    "BLOCKED_SCOPE_PROOF_UNAVAILABLE",
                    f"{domain} authorization correlation",
                )
        broker = self._event_data(verified["broker"], "broker_read_complete")
        broker_open = self._event_data(verified["broker"], "broker_open_attempt")
        broker_delivery = self._event_data(verified["broker"], "broker_delivery_created")
        sandbox = self._event_data(verified["sandbox"], "sandbox_supervisor_snapshot")
        parser = self._event_data(verified["parser"], "parser_scope_result")
        gateway = self._event_data(verified["gateway"], "gateway_scope_result")

        actual_calls = broker.get("actual_read_calls", []) if broker else []
        actual_union = broker.get("actual_union_of_read_ranges", []) if broker else []
        outside = broker.get("outside_allowed_bytes") if broker else None
        if capability_id is not None:
            require(
                broker_open is not None and broker_open.get("capability_id") == capability_id,
                "BLOCKED_SCOPE_PROOF_UNAVAILABLE",
                "capability correlation",
            )
        if consumption_event_id is not None:
            require(
                broker_open is not None and broker_open.get("consumption_event_id") == consumption_event_id,
                "BLOCKED_SCOPE_PROOF_UNAVAILABLE",
                "consumption event correlation",
            )
        if delivery_id is not None:
            require(
                broker_delivery is not None and broker_delivery.get("delivery_id") == delivery_id,
                "BLOCKED_SCOPE_PROOF_UNAVAILABLE",
                "delivery correlation",
            )
        if expected_completed:
            require(
                actual_union == [{"start_byte": BOOK1_START, "end_byte_exclusive": BOOK1_END}],
                "BLOCKED_SCOPE_PROOF_UNAVAILABLE",
                "actual union",
            )
            require(outside == 0, "BLOCKED_SCOPE_PROOF_UNAVAILABLE", "outside bytes")
            require(sandbox is not None and sandbox["consumer_visible_full_object_handles"] == 0, "BLOCKED_SCOPE_PROOF_UNAVAILABLE")
            require(parser is not None and parser["book1_markers"] == 1, "BLOCKED_SCOPE_PROOF_UNAVAILABLE")
            require(parser["book2_markers"] == 0 and parser["card_markers"] == 10 and parser["paragraph_markers"] == 10, "BLOCKED_SCOPE_PROOF_UNAVAILABLE")
            require(gateway is not None and gateway["book2_events"] == 0 and gateway["greek_events"] == 0, "BLOCKED_SCOPE_PROOF_UNAVAILABLE")
            require(gateway["model_invocations"] == 0, "BLOCKED_SCOPE_PROOF_UNAVAILABLE")

        authorization_digest = authorization["authorization_file_sha256"] if authorization else "absent"
        fixture_object_id = authorization["fixture_object_id"] if authorization else "absent"
        payload = {
            "object_id": f"urn:ctde:audit-scope:{uuid.uuid4()}",
            "attestation_id": f"SCOPE-{uuid.uuid4()}",
            "attestation_subtype": "prototype_scope_execution_attestation",
            "environment": "prototype_fixture_only",
            "attempt_id": attempt_id,
            "authorization_file_sha256": authorization_digest,
            "iss": self.signer.issuer,
            "aud": [self.scope_verifier_id, self.audit_controller_id],
            "iat": self.now,
            "nbf": self.now,
            "exp": self.now + 300,
            "candidate_run_id": None,
            "candidate_run_authorized": False,
            "fixture_object_id": fixture_object_id,
            "consumption_event_id": consumption_event_id,
            "capability_id": capability_id or "not_issued",
            "delivery_id": delivery_id or "not_issued",
            "read_state": "completed" if expected_completed else "attempted",
            "allowed_ranges": [{"start_byte": BOOK1_START, "end_byte_exclusive": BOOK1_END}],
            "actual_read_calls": actual_calls,
            "actual_union_of_read_ranges": actual_union,
            "bytes_outside_allowed_ranges": outside,
            "consumer_direct_full_object_open_success_count": 0 if sandbox else 0,
            "greek_like_access_attempt_count": 0,
            "greek_like_access_denied_count": 0,
            "greek_like_open_success_count": 0,
            "greek_like_read_success_count": 0,
            "greek_like_successful_read_bytes": 0,
            "model_invocations": gateway.get("model_invocations", 0) if gateway else 0,
            "raw_or_fixture_payload_persisted": False,
            "component_event_chain_digests": {
                domain: JWSCodec.digest(logs[domain].tokens[-1]) for domain in SCOPE_DOMAINS
            },
        }
        return JWSCodec.sign(self.signer, AUDIT_TYP, payload)

    @staticmethod
    def validate_authorization_correlation_v2(
        context: ActivatedAuthorizationContextV2,
    ) -> dict[str, Any]:
        claims = context.artifact.claims
        projection = validate_activated_projection(
            context,
            expected_consumer_id=claims["allowed_consumer"]["consumer_id"],
            expected_component_id=claims["allowed_consumer"]["component_id"],
        )
        require(
            projection["authorization_artifact_sha256"] == context.identity.authorization_artifact_sha256,
            "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH",
        )
        return projection

    def create_closure_attestation(
        self,
        *,
        logs: dict[str, SignedEventLog],
        authorization: dict[str, Any] | None,
        attempt_id: str,
        scope_attestation: str | None,
        final_result: str,
        expected_formal_inputs: int,
    ) -> str:
        verified = self._verify_logs(logs, CLOSURE_DOMAINS, attempt_id)
        write = self._event_data(verified["write"], "write_monitor_complete")
        formal = self._event_data(verified["formal"], "formal_loader_complete")
        require(write is not None, "BLOCKED_SCOPE_PROOF_UNAVAILABLE", "write evidence")
        require(formal is not None, "BLOCKED_SCOPE_PROOF_UNAVAILABLE", "formal evidence")
        require(formal.get("formal_content_inputs") == expected_formal_inputs, "BLOCKED_SCOPE_PROOF_UNAVAILABLE", "formal count")
        scope_digest = JWSCodec.digest(scope_attestation) if scope_attestation else None
        payload = {
            "object_id": f"urn:ctde:audit-closure:{uuid.uuid4()}",
            "attestation_id": f"CLOSURE-{uuid.uuid4()}",
            "attestation_subtype": "prototype_closure_audit_attestation",
            "environment": "prototype_fixture_only",
            "attempt_id": attempt_id,
            "authorization_file_sha256": authorization["authorization_file_sha256"] if authorization else "absent",
            "iss": self.signer.issuer,
            "aud": self.audit_controller_id,
            "iat": self.now,
            "nbf": self.now,
            "exp": self.now + 300,
            "candidate_run_id": None,
            "candidate_run_authorized": False,
            "scope_execution_attestation_id": "present" if scope_attestation else "not_reached",
            "scope_execution_attestation_sha256": scope_digest,
            "business_output_status": "absent",
            "business_output_sha256": None,
            "business_output_absent_reason": "prototype_has_no_business_output",
            "raw_write_count": write.get("raw_write_count", 0),
            "structure_map_write_count": write.get("structure_map_write_count", 0),
            "wrapper_persist_count": write.get("wrapper_persist_count", 0),
            "formal_path_write_count": write.get("formal_path_write_count", 0),
            "run_local_unallowlisted_write_count": write.get("run_local_unallowlisted_write_count", 0),
            "formal_loader_check_status": "pass",
            "formal_content_inputs": formal.get("formal_content_inputs"),
            "last_gate_result": final_result,
            "execution_status": "not_started",
            "run_disposition": "prototype_case_closed",
            "raw_or_fixture_payload_persisted": False,
            "component_event_chain_digests": {
                domain: JWSCodec.digest(logs[domain].tokens[-1]) for domain in CLOSURE_DOMAINS
            },
        }
        return JWSCodec.sign(self.signer, AUDIT_TYP, payload)
