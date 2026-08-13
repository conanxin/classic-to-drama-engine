from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
import threading
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .common import PrototypeError, canonical_json_bytes, require, sha256_bytes
from .events import SignedEventLog
from .authorization_v2 import (
    ActivatedAuthorizationContextV2,
    AuthorizationArtifactV2,
    AuthorizationRegistryIdentityV2,
    AuthorizationRegistryStateV2,
    PostConsumeMintContextV2,
    PostMintLeaseContextV2,
    PreConsumeAuthorizationContextV2,
    PreparedCapabilityContextV2,
    PORTABLE_PROFILE,
    SCHEMA_ID,
    SCHEMA_VERSION,
    compare_handle,
    handle_digest,
    load_authorization_v2,
    parse_rfc3339_utc,
    validate_request_binding,
)


@dataclass(frozen=True)
class MintLease:
    authorization_id: str
    attempt_id: str
    consumption_event_id: str
    authorization_digest: str
    secret: bytes


class AuthorizationRegistry:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path, timeout=30, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=FULL")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS authorizations (
                    authorization_id TEXT PRIMARY KEY,
                    attempt_id TEXT NOT NULL UNIQUE,
                    authorization_digest TEXT NOT NULL UNIQUE,
                    fixture_object_id TEXT NOT NULL,
                    expires_at INTEGER NOT NULL,
                    immutable_bytes_sha256 TEXT NOT NULL,
                    state TEXT NOT NULL CHECK(state IN ('unconsumed','spent','revoked','expired')),
                    consumption_event_id TEXT,
                    lease_hash TEXT,
                    mint_claimed INTEGER NOT NULL DEFAULT 0,
                    closed INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS registry_events (
                    event_id TEXT PRIMARY KEY,
                    authorization_id TEXT NOT NULL,
                    attempt_id TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    created_at INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS capabilities (
                    capability_id TEXT PRIMARY KEY,
                    consumption_event_id TEXT NOT NULL UNIQUE,
                    attempt_id TEXT NOT NULL,
                    consumed INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS deliveries (
                    delivery_id TEXT PRIMARY KEY,
                    attempt_id TEXT NOT NULL,
                    consumed INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS authorization_v2_identity (
                    registry_record_id TEXT PRIMARY KEY,
                    authorization_id TEXT NOT NULL UNIQUE,
                    schema_id TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    assurance_profile_id TEXT NOT NULL,
                    run_id TEXT NOT NULL UNIQUE,
                    source_id TEXT NOT NULL,
                    source_snapshot_id TEXT NOT NULL,
                    structure_map_id TEXT NOT NULL,
                    nonce TEXT NOT NULL UNIQUE,
                    authorization_artifact_bytes BLOB NOT NULL,
                    authorization_artifact_sha256 TEXT NOT NULL UNIQUE,
                    authorization_artifact_size_bytes INTEGER NOT NULL,
                    registered_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS authorization_v2_state (
                    registry_record_id TEXT PRIMARY KEY REFERENCES authorization_v2_identity(registry_record_id),
                    consumption_state TEXT NOT NULL CHECK(consumption_state IN ('unconsumed','spent','revoked','expired')),
                    state_version INTEGER NOT NULL,
                    consumption_event_id TEXT,
                    last_state_event_id TEXT,
                    state_changed_at TEXT NOT NULL,
                    terminal_reason TEXT,
                    mint_eligibility_state TEXT NOT NULL CHECK(mint_eligibility_state IN ('unavailable','available','claimed','aborted')),
                    mint_eligibility_handle_sha256 TEXT UNIQUE,
                    mint_eligibility_event_id TEXT,
                    mint_claimed INTEGER NOT NULL DEFAULT 0,
                    mint_claim_event_id TEXT,
                    capability_preparation_state TEXT NOT NULL CHECK(capability_preparation_state IN ('not_claimed','unprepared','prepared','aborted')),
                    preparation_handle_sha256 TEXT UNIQUE,
                    pending_capability_id TEXT UNIQUE,
                    pending_capability_artifact_sha256 TEXT,
                    capability_preparation_event_id TEXT,
                    capability_activation_state TEXT NOT NULL CHECK(capability_activation_state IN ('not_ready','eligible','activated','aborted')),
                    activation_handle_sha256 TEXT UNIQUE,
                    active_capability_id TEXT UNIQUE,
                    capability_activation_event_id TEXT,
                    activation_commit_a1_event_sha256 TEXT
                );
                CREATE TABLE IF NOT EXISTS authorization_v2_events (
                    registry_event_id TEXT PRIMARY KEY,
                    registry_record_id TEXT,
                    registry_operation_id TEXT NOT NULL UNIQUE,
                    consume_operation_id TEXT,
                    event_type TEXT NOT NULL,
                    event_json TEXT NOT NULL,
                    authoritative_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS pending_capabilities_v2 (
                    pending_capability_id TEXT PRIMARY KEY,
                    registry_record_id TEXT NOT NULL UNIQUE REFERENCES authorization_v2_identity(registry_record_id),
                    mint_claim_event_id TEXT NOT NULL UNIQUE,
                    capability_bytes BLOB NOT NULL,
                    capability_sha256 TEXT NOT NULL UNIQUE,
                    callable INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS active_capabilities_v2 (
                    active_capability_id TEXT PRIMARY KEY,
                    registry_record_id TEXT NOT NULL UNIQUE REFERENCES authorization_v2_identity(registry_record_id),
                    capability_preparation_event_id TEXT NOT NULL UNIQUE,
                    activated_at TEXT NOT NULL
                );
                """
            )

    def register(self, authorization: dict[str, Any], immutable_bytes: bytes) -> str:
        authorization_id = authorization["authorization_id"]
        digest = sha256_bytes(immutable_bytes)
        require(
            digest == authorization["authorization_file_sha256"],
            "BLOCKED_TEST_AUTHORIZATION_INVALID",
            "authorization digest",
        )
        with self._connect() as connection:
            connection.execute(
                """INSERT INTO authorizations
                   (authorization_id, attempt_id, authorization_digest, fixture_object_id,
                    expires_at, immutable_bytes_sha256, state)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    authorization_id,
                    authorization["attempt_id"],
                    digest,
                    authorization["fixture_object_id"],
                    authorization["expires_at"],
                    digest,
                    "expired" if authorization.get("initial_state") == "expired" else "unconsumed",
                ),
            )
        return digest

    def consume(
        self,
        *,
        authorization_id: str,
        attempt_id: str,
        authorization_digest: str,
        now: int,
        events: SignedEventLog,
    ) -> MintLease:
        secret = secrets.token_bytes(32)
        lease_hash = hashlib.sha256(secret).hexdigest()
        event_id = f"RCE-{uuid.uuid4()}"
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM authorizations WHERE authorization_id=?",
                (authorization_id,),
            ).fetchone()
            if row is None:
                raise PrototypeError("BLOCKED_TEST_AUTHORIZATION_MISSING")
            if row["attempt_id"] != attempt_id or row["authorization_digest"] != authorization_digest:
                raise PrototypeError("BLOCKED_TEST_AUTHORIZATION_INVALID")
            if row["expires_at"] < now or row["state"] == "expired":
                connection.execute(
                    "UPDATE authorizations SET state='expired' WHERE authorization_id=?",
                    (authorization_id,),
                )
                connection.commit()
                raise PrototypeError("BLOCKED_TEST_AUTHORIZATION_EXPIRED")
            if row["state"] != "unconsumed":
                raise PrototypeError("BLOCKED_TEST_AUTHORIZATION_SPENT")
            changed = connection.execute(
                """UPDATE authorizations
                   SET state='spent', consumption_event_id=?, lease_hash=?
                   WHERE authorization_id=? AND state='unconsumed'""",
                (event_id, lease_hash, authorization_id),
            ).rowcount
            if changed != 1:
                raise PrototypeError("BLOCKED_TEST_AUTHORIZATION_SPENT")
            connection.execute(
                "INSERT INTO registry_events VALUES (?, ?, ?, 'authorization_spent', ?)",
                (event_id, authorization_id, attempt_id, now),
            )
            connection.commit()
        except Exception:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()
        events.append(
            "authorization_spent",
            {
                "authorization_id": authorization_id,
                "consumption_event_id": event_id,
                "state": "spent",
            },
        )
        return MintLease(authorization_id, attempt_id, event_id, authorization_digest, secret)

    def claim_mint_lease(self, lease: MintLease) -> None:
        lease_hash = hashlib.sha256(lease.secret).hexdigest()
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM authorizations WHERE authorization_id=?",
                (lease.authorization_id,),
            ).fetchone()
            require(row is not None, "BLOCKED_TEST_AUTHORIZATION_MISSING")
            require(row["state"] == "spent", "BLOCKED_TEST_AUTHORIZATION_SPENT")
            require(not row["closed"], "BLOCKED_TEST_AUTHORIZATION_SPENT", "attempt closed")
            require(row["attempt_id"] == lease.attempt_id, "BLOCKED_TEST_AUTHORIZATION_INVALID")
            require(row["consumption_event_id"] == lease.consumption_event_id, "BLOCKED_TEST_AUTHORIZATION_INVALID")
            require(row["lease_hash"] == lease_hash, "BLOCKED_TEST_AUTHORIZATION_INVALID", "lease")
            changed = connection.execute(
                "UPDATE authorizations SET mint_claimed=1 WHERE authorization_id=? AND mint_claimed=0",
                (lease.authorization_id,),
            ).rowcount
            require(changed == 1, "BLOCKED_TEST_AUTHORIZATION_SPENT", "mint lease replay")
            connection.commit()

    def close_attempt(self, authorization_id: str) -> None:
        with self._connect() as connection:
            connection.execute(
                "UPDATE authorizations SET closed=1 WHERE authorization_id=?",
                (authorization_id,),
            )

    def register_capability(self, capability_id: str, event_id: str, attempt_id: str) -> None:
        with self._connect() as connection:
            try:
                connection.execute(
                    "INSERT INTO capabilities VALUES (?, ?, ?, 0)",
                    (capability_id, event_id, attempt_id),
                )
            except sqlite3.IntegrityError as exc:
                raise PrototypeError("BLOCKED_RANGE_CAPABILITY_INVALID", "event replay") from exc

    def consume_capability(self, capability_id: str, attempt_id: str) -> None:
        with self._connect() as connection:
            changed = connection.execute(
                "UPDATE capabilities SET consumed=1 WHERE capability_id=? AND attempt_id=? AND consumed=0",
                (capability_id, attempt_id),
            ).rowcount
            require(changed == 1, "BLOCKED_RANGE_CAPABILITY_INVALID", "capability replay")

    def register_delivery(self, delivery_id: str, attempt_id: str) -> None:
        with self._connect() as connection:
            connection.execute(
                "INSERT INTO deliveries VALUES (?, ?, 0)",
                (delivery_id, attempt_id),
            )

    def consume_delivery(self, delivery_id: str, attempt_id: str) -> None:
        with self._connect() as connection:
            changed = connection.execute(
                "UPDATE deliveries SET consumed=1 WHERE delivery_id=? AND attempt_id=? AND consumed=0",
                (delivery_id, attempt_id),
            ).rowcount
            require(changed == 1, "BLOCKED_BOUNDED_READER_REPLAY")

    def state(self, authorization_id: str) -> dict[str, Any]:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM authorizations WHERE authorization_id=?",
                (authorization_id,),
            ).fetchone()
            if row is None:
                return {"state": "unknown"}
            return dict(row)

    def counts(self, attempt_id: str) -> dict[str, int]:
        with self._connect() as connection:
            return {
                "consumption_events": connection.execute(
                    "SELECT COUNT(*) FROM registry_events WHERE attempt_id=?",
                    (attempt_id,),
                ).fetchone()[0],
                "capabilities": connection.execute(
                    "SELECT COUNT(*) FROM capabilities WHERE attempt_id=?",
                    (attempt_id,),
                ).fetchone()[0],
                "deliveries": connection.execute(
                    "SELECT COUNT(*) FROM deliveries WHERE attempt_id=?",
                    (attempt_id,),
                ).fetchone()[0],
            }

    # Authorization Schema V2 is deliberately routed through separate tables and
    # typed contexts.  The historical V1 API above remains byte-for-byte compatible
    # for frozen suites, but is never a fallback for V2.

    @staticmethod
    def _v2_identity(row: sqlite3.Row) -> AuthorizationRegistryIdentityV2:
        return AuthorizationRegistryIdentityV2(
            registry_record_id=row["registry_record_id"],
            authorization_id=row["authorization_id"],
            schema_id=row["schema_id"],
            schema_version=row["schema_version"],
            assurance_profile_id=row["assurance_profile_id"],
            run_id=row["run_id"],
            source_id=row["source_id"],
            source_snapshot_id=row["source_snapshot_id"],
            structure_map_id=row["structure_map_id"],
            nonce=row["nonce"],
            authorization_artifact_sha256=row["authorization_artifact_sha256"],
            authorization_artifact_size_bytes=row["authorization_artifact_size_bytes"],
            registered_at=row["registered_at"],
        )

    @staticmethod
    def _v2_state(row: sqlite3.Row) -> AuthorizationRegistryStateV2:
        return AuthorizationRegistryStateV2(
            registry_record_id=row["registry_record_id"],
            consumption_state=row["consumption_state"],
            state_version=row["state_version"],
            consumption_event_id=row["consumption_event_id"],
            last_state_event_id=row["last_state_event_id"],
            state_changed_at=row["state_changed_at"],
            terminal_reason=row["terminal_reason"],
            mint_eligibility_state=row["mint_eligibility_state"],
            mint_eligibility_handle_sha256=row["mint_eligibility_handle_sha256"],
            mint_eligibility_event_id=row["mint_eligibility_event_id"],
            mint_claimed=bool(row["mint_claimed"]),
            mint_claim_event_id=row["mint_claim_event_id"],
            capability_preparation_state=row["capability_preparation_state"],
            preparation_handle_sha256=row["preparation_handle_sha256"],
            pending_capability_id=row["pending_capability_id"],
            pending_capability_artifact_sha256=row["pending_capability_artifact_sha256"],
            capability_preparation_event_id=row["capability_preparation_event_id"],
            capability_activation_state=row["capability_activation_state"],
            activation_handle_sha256=row["activation_handle_sha256"],
            active_capability_id=row["active_capability_id"],
            capability_activation_event_id=row["capability_activation_event_id"],
            activation_commit_a1_event_sha256=row["activation_commit_a1_event_sha256"],
        )

    def _load_v2(
        self,
        connection: sqlite3.Connection,
        authorization_id: str,
        schema_path: Path,
    ) -> tuple[AuthorizationArtifactV2, AuthorizationRegistryIdentityV2, AuthorizationRegistryStateV2]:
        identity_row = connection.execute(
            "SELECT * FROM authorization_v2_identity WHERE authorization_id=?",
            (authorization_id,),
        ).fetchone()
        if identity_row is None:
            raise PrototypeError("BLOCKED_AUTHORIZATION_MISSING")
        exact_bytes = bytes(identity_row["authorization_artifact_bytes"])
        digest = sha256_bytes(exact_bytes)
        if (
            digest != identity_row["authorization_artifact_sha256"]
            or len(exact_bytes) != identity_row["authorization_artifact_size_bytes"]
        ):
            raise PrototypeError("BLOCKED_AUTHORIZATION_REGISTRY_DIGEST_MISMATCH")
        artifact = load_authorization_v2(exact_bytes, schema_path)
        claims = artifact.claims
        comparisons = {
            "authorization_id": claims["authorization_id"],
            "schema_version": claims["schema_version"],
            "assurance_profile_id": claims["assurance_profile_id"],
            "run_id": claims["run_id"],
            "source_id": claims["source_id"],
            "source_snapshot_id": claims["source_snapshot_id"],
            "structure_map_id": claims["structure_map_id"],
            "nonce": claims["nonce"],
        }
        for field, expected in comparisons.items():
            if identity_row[field] != expected:
                raise PrototypeError("BLOCKED_AUTHORIZATION_REGISTRY_DIGEST_MISMATCH", field)
        if identity_row["schema_id"] != SCHEMA_ID:
            raise PrototypeError("BLOCKED_AUTHORIZATION_REGISTRY_DIGEST_MISMATCH", "schema_id")
        state_row = connection.execute(
            "SELECT * FROM authorization_v2_state WHERE registry_record_id=?",
            (identity_row["registry_record_id"],),
        ).fetchone()
        require(state_row is not None, "BLOCKED_AUTHORIZATION_REGISTRY_DIGEST_MISMATCH", "missing state")
        return artifact, self._v2_identity(identity_row), self._v2_state(state_row)

    @staticmethod
    def _v2_event_payload(
        *,
        event_id: str,
        event_type: str,
        identity: AuthorizationRegistryIdentityV2,
        before: AuthorizationRegistryStateV2 | None,
        after: AuthorizationRegistryStateV2 | None,
        registry_operation_id: str,
        consume_operation_id: str | None,
        cas_outcome: str,
        blocker: str | None,
        authoritative_at: str,
    ) -> dict[str, Any]:
        state = after or before
        return {
            "registry_event_id": event_id,
            "event_type": event_type,
            "registry_record_id": identity.registry_record_id,
            "authorization_id": identity.authorization_id,
            "run_id": identity.run_id,
            "assurance_profile_id": identity.assurance_profile_id,
            "nonce": identity.nonce,
            "authorization_artifact_sha256": identity.authorization_artifact_sha256,
            "registry_operation_id": registry_operation_id,
            "consume_operation_id": consume_operation_id,
            "from_consumption_state": before.consumption_state if before else None,
            "to_consumption_state": after.consumption_state if after else None,
            "from_mint_eligibility_state": before.mint_eligibility_state if before else None,
            "to_mint_eligibility_state": after.mint_eligibility_state if after else None,
            "from_capability_preparation_state": before.capability_preparation_state if before else None,
            "to_capability_preparation_state": after.capability_preparation_state if after else None,
            "from_capability_activation_state": before.capability_activation_state if before else None,
            "to_capability_activation_state": after.capability_activation_state if after else None,
            "mint_eligibility_handle_sha256": state.mint_eligibility_handle_sha256 if state else None,
            "preparation_handle_sha256": state.preparation_handle_sha256 if state else None,
            "activation_handle_sha256": state.activation_handle_sha256 if state else None,
            "mint_claim_event_id": state.mint_claim_event_id if state else None,
            "pending_capability_id": state.pending_capability_id if state else None,
            "active_capability_id": state.active_capability_id if state else None,
            "pending_capability_artifact_sha256": state.pending_capability_artifact_sha256 if state else None,
            "capability_preparation_event_id": state.capability_preparation_event_id if state else None,
            "activation_commit_a1_event_sha256": state.activation_commit_a1_event_sha256 if state else None,
            "expected_state_version": before.state_version if before else None,
            "result_state_version": after.state_version if after else None,
            "cas_outcome": cas_outcome,
            "blocker": blocker,
            "authoritative_at": authoritative_at,
        }

    def _insert_v2_event(
        self,
        connection: sqlite3.Connection,
        *,
        event_type: str,
        identity: AuthorizationRegistryIdentityV2,
        before: AuthorizationRegistryStateV2 | None,
        after: AuthorizationRegistryStateV2 | None,
        registry_operation_id: str,
        consume_operation_id: str | None,
        cas_outcome: str,
        blocker: str | None,
        authoritative_at: str,
        event_id: str | None = None,
    ) -> str:
        selected_event_id = event_id or f"R2EV-{uuid.uuid4()}"
        payload = self._v2_event_payload(
            event_id=selected_event_id,
            event_type=event_type,
            identity=identity,
            before=before,
            after=after,
            registry_operation_id=registry_operation_id,
            consume_operation_id=consume_operation_id,
            cas_outcome=cas_outcome,
            blocker=blocker,
            authoritative_at=authoritative_at,
        )
        connection.execute(
            "INSERT INTO authorization_v2_events VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                selected_event_id,
                identity.registry_record_id,
                registry_operation_id,
                consume_operation_id,
                event_type,
                json.dumps(payload, sort_keys=True, separators=(",", ":")),
                authoritative_at,
            ),
        )
        return selected_event_id

    def register_authorization_v2(
        self,
        *,
        exact_bytes: bytes,
        schema_path: Path,
        registered_at: str,
        registry_operation_id: str,
        required_profile: str = PORTABLE_PROFILE,
    ) -> PreConsumeAuthorizationContextV2:
        artifact = load_authorization_v2(exact_bytes, schema_path)
        claims = artifact.claims
        require(claims["assurance_profile_id"] == required_profile, "BLOCKED_AUTHORIZATION_PROFILE_MISMATCH")
        parse_rfc3339_utc(registered_at, "registered_at")
        registry_record_id = f"R2REG-{uuid.uuid4()}"
        identity = AuthorizationRegistryIdentityV2(
            registry_record_id=registry_record_id,
            authorization_id=claims["authorization_id"],
            schema_id=SCHEMA_ID,
            schema_version=SCHEMA_VERSION,
            assurance_profile_id=claims["assurance_profile_id"],
            run_id=claims["run_id"],
            source_id=claims["source_id"],
            source_snapshot_id=claims["source_snapshot_id"],
            structure_map_id=claims["structure_map_id"],
            nonce=claims["nonce"],
            authorization_artifact_sha256=artifact.artifact_sha256,
            authorization_artifact_size_bytes=artifact.size_bytes,
            registered_at=registered_at,
        )
        event_id = f"R2EV-{uuid.uuid4()}"
        state = AuthorizationRegistryStateV2(
            registry_record_id=registry_record_id,
            consumption_state="unconsumed",
            state_version=0,
            consumption_event_id=None,
            last_state_event_id=event_id,
            state_changed_at=registered_at,
            terminal_reason=None,
            mint_eligibility_state="unavailable",
            mint_eligibility_handle_sha256=None,
            mint_eligibility_event_id=None,
            mint_claimed=False,
            mint_claim_event_id=None,
            capability_preparation_state="not_claimed",
            preparation_handle_sha256=None,
            pending_capability_id=None,
            pending_capability_artifact_sha256=None,
            capability_preparation_event_id=None,
            capability_activation_state="not_ready",
            activation_handle_sha256=None,
            active_capability_id=None,
            capability_activation_event_id=None,
            activation_commit_a1_event_sha256=None,
        )
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """INSERT INTO authorization_v2_identity VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    identity.registry_record_id,
                    identity.authorization_id,
                    identity.schema_id,
                    identity.schema_version,
                    identity.assurance_profile_id,
                    identity.run_id,
                    identity.source_id,
                    identity.source_snapshot_id,
                    identity.structure_map_id,
                    identity.nonce,
                    sqlite3.Binary(artifact.exact_bytes),
                    identity.authorization_artifact_sha256,
                    identity.authorization_artifact_size_bytes,
                    identity.registered_at,
                ),
            )
            connection.execute(
                """INSERT INTO authorization_v2_state
                   (registry_record_id, consumption_state, state_version, consumption_event_id,
                    last_state_event_id, state_changed_at, terminal_reason, mint_eligibility_state,
                    mint_eligibility_handle_sha256, mint_eligibility_event_id, mint_claimed,
                    mint_claim_event_id, capability_preparation_state, preparation_handle_sha256,
                    pending_capability_id, pending_capability_artifact_sha256,
                    capability_preparation_event_id, capability_activation_state,
                    activation_handle_sha256, active_capability_id,
                    capability_activation_event_id, activation_commit_a1_event_sha256)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    state.registry_record_id,
                    state.consumption_state,
                    state.state_version,
                    state.consumption_event_id,
                    state.last_state_event_id,
                    state.state_changed_at,
                    state.terminal_reason,
                    state.mint_eligibility_state,
                    state.mint_eligibility_handle_sha256,
                    state.mint_eligibility_event_id,
                    int(state.mint_claimed),
                    state.mint_claim_event_id,
                    state.capability_preparation_state,
                    state.preparation_handle_sha256,
                    state.pending_capability_id,
                    state.pending_capability_artifact_sha256,
                    state.capability_preparation_event_id,
                    state.capability_activation_state,
                    state.activation_handle_sha256,
                    state.active_capability_id,
                    state.capability_activation_event_id,
                    state.activation_commit_a1_event_sha256,
                ),
            )
            self._insert_v2_event(
                connection,
                event_type="authorization_registered",
                identity=identity,
                before=None,
                after=state,
                registry_operation_id=registry_operation_id,
                consume_operation_id=None,
                cas_outcome="not_applicable",
                blocker=None,
                authoritative_at=registered_at,
                event_id=event_id,
            )
            connection.commit()
        except sqlite3.IntegrityError as exc:
            if connection.in_transaction:
                connection.rollback()
            detail = str(exc).lower()
            code = "BLOCKED_AUTHORIZATION_NONCE_CONFLICT" if "nonce" in detail else "BLOCKED_AUTHORIZATION_IDENTITY_CONFLICT"
            raise PrototypeError(code, str(exc)) from exc
        except Exception:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()
        return PreConsumeAuthorizationContextV2(artifact, identity, state)

    def resolve_preconsume_v2(self, authorization_id: str, schema_path: Path) -> PreConsumeAuthorizationContextV2:
        with self._connect() as connection:
            artifact, identity, state = self._load_v2(connection, authorization_id, schema_path)
        if state.consumption_state == "spent":
            raise PrototypeError("BLOCKED_AUTHORIZATION_REPLAY")
        if state.consumption_state == "revoked":
            raise PrototypeError("BLOCKED_AUTHORIZATION_REVOKED")
        if state.consumption_state == "expired":
            raise PrototypeError("BLOCKED_AUTHORIZATION_EXPIRED")
        require(state.consumption_state == "unconsumed", "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
        return PreConsumeAuthorizationContextV2(artifact, identity, state)

    def _record_rejection_v2(
        self,
        *,
        authorization_id: str,
        schema_path: Path,
        registry_operation_id: str,
        consume_operation_id: str | None,
        blocker: str,
        authoritative_at: str,
        event_type: str = "authorization_request_rejected",
    ) -> None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            _, identity, state = self._load_v2(connection, authorization_id, schema_path)
            self._insert_v2_event(
                connection,
                event_type=event_type,
                identity=identity,
                before=state,
                after=state,
                registry_operation_id=registry_operation_id,
                consume_operation_id=consume_operation_id,
                cas_outcome="rejected",
                blocker=blocker,
                authoritative_at=authoritative_at,
            )
            connection.commit()
        except Exception:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()

    def _require_current_v2(
        self,
        connection: sqlite3.Connection,
        context: Any,
        schema_path: Path,
    ) -> tuple[AuthorizationArtifactV2, AuthorizationRegistryIdentityV2, AuthorizationRegistryStateV2]:
        artifact, identity, state = self._load_v2(connection, context.identity.authorization_id, schema_path)
        if (
            identity != context.identity
            or artifact.artifact_sha256 != context.artifact.artifact_sha256
            or artifact.exact_bytes != context.artifact.exact_bytes
            or artifact.claims != context.artifact.claims
        ):
            raise PrototypeError("BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
        if state.state_version != context.state.state_version:
            raise PrototypeError("BLOCKED_AUTHORIZATION_CONTEXT_STALE")
        return artifact, identity, state

    def _v2_operation_exists(self, registry_operation_id: str) -> bool:
        with self._connect() as connection:
            return connection.execute(
                "SELECT 1 FROM authorization_v2_events WHERE registry_operation_id=?",
                (registry_operation_id,),
            ).fetchone() is not None

    def consume_authorization_v2(
        self,
        *,
        context: PreConsumeAuthorizationContextV2,
        request: dict[str, Any],
        schema_path: Path,
        now: str,
        registry_operation_id: str,
        consume_operation_id: str,
        signed_writer_ready: bool = True,
    ) -> PostConsumeMintContextV2:
        require(isinstance(context, PreConsumeAuthorizationContextV2), "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        parse_rfc3339_utc(now, "now")
        try:
            validate_request_binding(context.artifact.claims, request)
            require(signed_writer_ready, "BLOCKED_A1_AUDIT_WRITER_UNAVAILABLE")
        except PrototypeError as exc:
            self._record_rejection_v2(
                authorization_id=context.identity.authorization_id,
                schema_path=schema_path,
                registry_operation_id=registry_operation_id,
                consume_operation_id=consume_operation_id,
                blocker=exc.code,
                authoritative_at=now,
            )
            raise
        secret = secrets.token_bytes(32)
        digest = handle_digest("CTDE-R2P-MINT-ELIGIBILITY-V1", secret)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            artifact, identity, state = self._require_current_v2(connection, context, schema_path)
            if state.consumption_state != "unconsumed":
                code = {
                    "spent": "BLOCKED_AUTHORIZATION_REPLAY",
                    "revoked": "BLOCKED_AUTHORIZATION_REVOKED",
                    "expired": "BLOCKED_AUTHORIZATION_EXPIRED",
                }.get(state.consumption_state, "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH")
                self._insert_v2_event(
                    connection,
                    event_type="authorization_request_rejected",
                    identity=identity,
                    before=state,
                    after=state,
                    registry_operation_id=registry_operation_id,
                    consume_operation_id=consume_operation_id,
                    cas_outcome="rejected",
                    blocker=code,
                    authoritative_at=now,
                )
                connection.commit()
                raise PrototypeError(code)
            if parse_rfc3339_utc(now, "now") >= parse_rfc3339_utc(artifact.claims["expires_at"], "expires_at"):
                event_id = f"R2EV-{uuid.uuid4()}"
                changed = connection.execute(
                    """UPDATE authorization_v2_state SET consumption_state='expired', state_version=state_version+1,
                       last_state_event_id=?, state_changed_at=?, terminal_reason='expired'
                       WHERE registry_record_id=? AND consumption_state='unconsumed' AND state_version=?""",
                    (event_id, now, identity.registry_record_id, state.state_version),
                ).rowcount
                require(changed == 1, "BLOCKED_AUTHORIZATION_CONTEXT_STALE")
                _, _, after = self._load_v2(connection, identity.authorization_id, schema_path)
                self._insert_v2_event(
                    connection,
                    event_type="authorization_expired",
                    identity=identity,
                    before=state,
                    after=after,
                    registry_operation_id=registry_operation_id,
                    consume_operation_id=consume_operation_id,
                    cas_outcome="accepted",
                    blocker="BLOCKED_AUTHORIZATION_EXPIRED",
                    authoritative_at=now,
                    event_id=event_id,
                )
                connection.commit()
                raise PrototypeError("BLOCKED_AUTHORIZATION_EXPIRED")
            event_id = f"R2EV-{uuid.uuid4()}"
            changed = connection.execute(
                """UPDATE authorization_v2_state SET consumption_state='spent', state_version=state_version+1,
                   consumption_event_id=?, last_state_event_id=?, state_changed_at=?, terminal_reason='consumed',
                   mint_eligibility_state='available', mint_eligibility_handle_sha256=?, mint_eligibility_event_id=?
                   WHERE registry_record_id=? AND consumption_state='unconsumed' AND state_version=?""",
                (event_id, event_id, now, digest, event_id, identity.registry_record_id, state.state_version),
            ).rowcount
            if changed != 1:
                raise PrototypeError("BLOCKED_AUTHORIZATION_REPLAY")
            _, _, after = self._load_v2(connection, identity.authorization_id, schema_path)
            self._insert_v2_event(
                connection,
                event_type="authorization_spent",
                identity=identity,
                before=state,
                after=after,
                registry_operation_id=registry_operation_id,
                consume_operation_id=consume_operation_id,
                cas_outcome="accepted",
                blocker=None,
                authoritative_at=now,
                event_id=event_id,
            )
            connection.commit()
        except PrototypeError as exc:
            if connection.in_transaction:
                connection.rollback()
            if not self._v2_operation_exists(registry_operation_id):
                blocker = "BLOCKED_AUTHORIZATION_REPLAY" if exc.code == "BLOCKED_AUTHORIZATION_CONTEXT_STALE" else exc.code
                self._record_rejection_v2(
                    authorization_id=context.identity.authorization_id,
                    schema_path=schema_path,
                    registry_operation_id=registry_operation_id,
                    consume_operation_id=consume_operation_id,
                    blocker=blocker,
                    authoritative_at=now,
                )
                if exc.code == "BLOCKED_AUTHORIZATION_CONTEXT_STALE":
                    raise PrototypeError(blocker) from exc
            raise
        except Exception:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()
        return PostConsumeMintContextV2(artifact, identity, after, consume_operation_id, secret)

    def revoke_authorization_v2(
        self,
        *,
        authorization_id: str,
        schema_path: Path,
        now: str,
        registry_operation_id: str,
    ) -> None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            _, identity, state = self._load_v2(connection, authorization_id, schema_path)
            require(state.consumption_state == "unconsumed", "BLOCKED_AUTHORIZATION_REPLAY")
            event_id = f"R2EV-{uuid.uuid4()}"
            changed = connection.execute(
                """UPDATE authorization_v2_state SET consumption_state='revoked', state_version=state_version+1,
                   last_state_event_id=?, state_changed_at=?, terminal_reason='revoked'
                   WHERE registry_record_id=? AND consumption_state='unconsumed' AND state_version=?""",
                (event_id, now, identity.registry_record_id, state.state_version),
            ).rowcount
            require(changed == 1, "BLOCKED_AUTHORIZATION_CONTEXT_STALE")
            _, _, after = self._load_v2(connection, authorization_id, schema_path)
            self._insert_v2_event(
                connection,
                event_type="authorization_revoked",
                identity=identity,
                before=state,
                after=after,
                registry_operation_id=registry_operation_id,
                consume_operation_id=None,
                cas_outcome="accepted",
                blocker=None,
                authoritative_at=now,
                event_id=event_id,
            )
            connection.commit()
        except Exception:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()

    def claim_mint_lease_v2(
        self,
        *,
        context: PostConsumeMintContextV2,
        pending_capability_id: str,
        schema_path: Path,
        now: str,
        registry_operation_id: str,
    ) -> PostMintLeaseContextV2:
        require(isinstance(context, PostConsumeMintContextV2), "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        preparation_secret = secrets.token_bytes(32)
        preparation_digest = handle_digest("CTDE-R2P-CAPABILITY-PREPARATION-V1", preparation_secret)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            artifact, identity, state = self._require_current_v2(connection, context, schema_path)
            if not compare_handle("CTDE-R2P-MINT-ELIGIBILITY-V1", context.eligibility_handle, state.mint_eligibility_handle_sha256):
                raise PrototypeError("BLOCKED_AUTHORIZATION_MINT_ELIGIBILITY_HANDLE_INVALID")
            if state.mint_claimed or state.mint_eligibility_state != "available":
                raise PrototypeError("BLOCKED_AUTHORIZATION_MINT_LEASE_ALREADY_CLAIMED")
            event_id = f"R2EV-{uuid.uuid4()}"
            changed = connection.execute(
                """UPDATE authorization_v2_state SET state_version=state_version+1,
                   mint_eligibility_state='claimed', mint_claimed=1, mint_claim_event_id=?,
                   preparation_handle_sha256=?, pending_capability_id=?, capability_preparation_state='unprepared',
                   capability_activation_state='not_ready', last_state_event_id=?, state_changed_at=?
                   WHERE registry_record_id=? AND state_version=? AND consumption_state='spent'
                   AND mint_eligibility_state='available' AND mint_claimed=0""",
                (event_id, preparation_digest, pending_capability_id, event_id, now, identity.registry_record_id, state.state_version),
            ).rowcount
            require(changed == 1, "BLOCKED_AUTHORIZATION_MINT_LEASE_ALREADY_CLAIMED")
            _, _, after = self._load_v2(connection, identity.authorization_id, schema_path)
            self._insert_v2_event(
                connection,
                event_type="authorization_mint_lease_claimed",
                identity=identity,
                before=state,
                after=after,
                registry_operation_id=registry_operation_id,
                consume_operation_id=context.consume_operation_id,
                cas_outcome="accepted",
                blocker=None,
                authoritative_at=now,
                event_id=event_id,
            )
            connection.commit()
        except PrototypeError as exc:
            if connection.in_transaction:
                connection.rollback()
            if exc.code in {"BLOCKED_AUTHORIZATION_MINT_LEASE_ALREADY_CLAIMED", "BLOCKED_AUTHORIZATION_CONTEXT_STALE", "BLOCKED_AUTHORIZATION_MINT_ELIGIBILITY_HANDLE_INVALID"}:
                self._record_rejection_v2(
                    authorization_id=context.identity.authorization_id,
                    schema_path=schema_path,
                    registry_operation_id=registry_operation_id,
                    consume_operation_id=context.consume_operation_id,
                    blocker=exc.code,
                    authoritative_at=now,
                    event_type="authorization_mint_lease_claim_rejected",
                )
            raise
        finally:
            connection.close()
        return PostMintLeaseContextV2(artifact, identity, after, context.consume_operation_id, preparation_secret)

    def prepare_capability_v2(
        self,
        *,
        context: PostMintLeaseContextV2,
        pending_capability_bytes: bytes,
        schema_path: Path,
        now: str,
        registry_operation_id: str,
    ) -> PreparedCapabilityContextV2:
        require(isinstance(context, PostMintLeaseContextV2), "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        activation_secret = secrets.token_bytes(32)
        activation_digest = handle_digest("CTDE-R2P-CAPABILITY-ACTIVATION-V1", activation_secret)
        pending_digest = sha256_bytes(pending_capability_bytes)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            artifact, identity, state = self._require_current_v2(connection, context, schema_path)
            if not compare_handle("CTDE-R2P-CAPABILITY-PREPARATION-V1", context.preparation_handle, state.preparation_handle_sha256):
                raise PrototypeError("BLOCKED_AUTHORIZATION_PREPARATION_HANDLE_UNAVAILABLE")
            if state.capability_preparation_state != "unprepared":
                raise PrototypeError("BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_PREPARED")
            event_id = f"R2EV-{uuid.uuid4()}"
            connection.execute(
                "INSERT INTO pending_capabilities_v2 VALUES (?, ?, ?, ?, ?, 0)",
                (
                    state.pending_capability_id,
                    identity.registry_record_id,
                    state.mint_claim_event_id,
                    sqlite3.Binary(pending_capability_bytes),
                    pending_digest,
                ),
            )
            changed = connection.execute(
                """UPDATE authorization_v2_state SET state_version=state_version+1,
                   capability_preparation_state='prepared', pending_capability_artifact_sha256=?,
                   capability_preparation_event_id=?, capability_activation_state='eligible',
                   activation_handle_sha256=?, last_state_event_id=?, state_changed_at=?
                   WHERE registry_record_id=? AND state_version=? AND capability_preparation_state='unprepared'""",
                (pending_digest, event_id, activation_digest, event_id, now, identity.registry_record_id, state.state_version),
            ).rowcount
            require(changed == 1, "BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_PREPARED")
            _, _, after = self._load_v2(connection, identity.authorization_id, schema_path)
            self._insert_v2_event(
                connection,
                event_type="authorization_capability_prepared",
                identity=identity,
                before=state,
                after=after,
                registry_operation_id=registry_operation_id,
                consume_operation_id=context.consume_operation_id,
                cas_outcome="accepted",
                blocker=None,
                authoritative_at=now,
                event_id=event_id,
            )
            connection.commit()
        except (PrototypeError, sqlite3.IntegrityError) as exc:
            if connection.in_transaction:
                connection.rollback()
            code = exc.code if isinstance(exc, PrototypeError) else "BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_PREPARED"
            self._record_rejection_v2(
                authorization_id=context.identity.authorization_id,
                schema_path=schema_path,
                registry_operation_id=registry_operation_id,
                consume_operation_id=context.consume_operation_id,
                blocker=code,
                authoritative_at=now,
                event_type="authorization_capability_preparation_rejected",
            )
            raise PrototypeError(code) from exc
        finally:
            connection.close()
        return PreparedCapabilityContextV2(artifact, identity, after, context.consume_operation_id, activation_secret)

    def activate_capability_v2(
        self,
        *,
        context: PreparedCapabilityContextV2,
        activation_commit_a1_event_sha256: str,
        schema_path: Path,
        now: str,
        registry_operation_id: str,
    ) -> ActivatedAuthorizationContextV2:
        require(isinstance(context, PreparedCapabilityContextV2), "BLOCKED_AUTHORIZATION_CONTEXT_STAGE_MISMATCH")
        require(len(activation_commit_a1_event_sha256) == 64, "BLOCKED_AUTHORIZATION_CONTEXT_MISMATCH", "commit digest")
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            artifact, identity, state = self._require_current_v2(connection, context, schema_path)
            if not compare_handle("CTDE-R2P-CAPABILITY-ACTIVATION-V1", context.activation_handle, state.activation_handle_sha256):
                raise PrototypeError("BLOCKED_AUTHORIZATION_ACTIVATION_HANDLE_UNAVAILABLE")
            if state.capability_activation_state != "eligible":
                raise PrototypeError("BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_ACTIVATED")
            event_id = f"R2EV-{uuid.uuid4()}"
            connection.execute(
                "INSERT INTO active_capabilities_v2 VALUES (?, ?, ?, ?)",
                (state.pending_capability_id, identity.registry_record_id, state.capability_preparation_event_id, now),
            )
            connection.execute(
                "UPDATE pending_capabilities_v2 SET callable=1 WHERE pending_capability_id=?",
                (state.pending_capability_id,),
            )
            changed = connection.execute(
                """UPDATE authorization_v2_state SET state_version=state_version+1,
                   capability_activation_state='activated', active_capability_id=pending_capability_id,
                   capability_activation_event_id=?, activation_commit_a1_event_sha256=?,
                   last_state_event_id=?, state_changed_at=?
                   WHERE registry_record_id=? AND state_version=? AND capability_activation_state='eligible'""",
                (event_id, activation_commit_a1_event_sha256, event_id, now, identity.registry_record_id, state.state_version),
            ).rowcount
            require(changed == 1, "BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_ACTIVATED")
            _, _, after = self._load_v2(connection, identity.authorization_id, schema_path)
            self._insert_v2_event(
                connection,
                event_type="authorization_capability_activated",
                identity=identity,
                before=state,
                after=after,
                registry_operation_id=registry_operation_id,
                consume_operation_id=context.consume_operation_id,
                cas_outcome="accepted",
                blocker=None,
                authoritative_at=now,
                event_id=event_id,
            )
            connection.commit()
        except (PrototypeError, sqlite3.IntegrityError) as exc:
            if connection.in_transaction:
                connection.rollback()
            code = exc.code if isinstance(exc, PrototypeError) else "BLOCKED_AUTHORIZATION_CAPABILITY_ALREADY_ACTIVATED"
            self._record_rejection_v2(
                authorization_id=context.identity.authorization_id,
                schema_path=schema_path,
                registry_operation_id=registry_operation_id,
                consume_operation_id=context.consume_operation_id,
                blocker=code,
                authoritative_at=now,
                event_type="authorization_capability_activation_rejected",
            )
            raise PrototypeError(code) from exc
        finally:
            connection.close()
        return ActivatedAuthorizationContextV2(artifact, identity, after, context.consume_operation_id)

    def abort_mint_eligibility_v2(
        self,
        *,
        context: PostConsumeMintContextV2,
        schema_path: Path,
        now: str,
        registry_operation_id: str,
        blocker: str,
    ) -> None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            _, identity, state = self._require_current_v2(connection, context, schema_path)
            require(state.mint_eligibility_state == "available", "BLOCKED_AUTHORIZATION_CONTEXT_STALE")
            event_id = f"R2EV-{uuid.uuid4()}"
            connection.execute(
                """UPDATE authorization_v2_state SET state_version=state_version+1,
                   mint_eligibility_state='aborted', last_state_event_id=?, state_changed_at=?, terminal_reason=?
                   WHERE registry_record_id=? AND state_version=? AND mint_eligibility_state='available'""",
                (event_id, now, blocker, identity.registry_record_id, state.state_version),
            )
            _, _, after = self._load_v2(connection, identity.authorization_id, schema_path)
            self._insert_v2_event(
                connection,
                event_type="authorization_mint_eligibility_aborted",
                identity=identity,
                before=state,
                after=after,
                registry_operation_id=registry_operation_id,
                consume_operation_id=context.consume_operation_id,
                cas_outcome="accepted",
                blocker=blocker,
                authoritative_at=now,
                event_id=event_id,
            )
            connection.commit()
        except Exception:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()

    def abort_preparation_v2(
        self,
        *,
        context: PostMintLeaseContextV2,
        schema_path: Path,
        now: str,
        registry_operation_id: str,
        blocker: str,
    ) -> None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            _, identity, state = self._require_current_v2(connection, context, schema_path)
            require(state.capability_preparation_state == "unprepared", "BLOCKED_AUTHORIZATION_CONTEXT_STALE")
            event_id = f"R2EV-{uuid.uuid4()}"
            connection.execute(
                """UPDATE authorization_v2_state SET state_version=state_version+1,
                   capability_preparation_state='aborted', last_state_event_id=?, state_changed_at=?, terminal_reason=?
                   WHERE registry_record_id=? AND state_version=? AND capability_preparation_state='unprepared'""",
                (event_id, now, blocker, identity.registry_record_id, state.state_version),
            )
            _, _, after = self._load_v2(connection, identity.authorization_id, schema_path)
            self._insert_v2_event(
                connection,
                event_type="authorization_capability_preparation_aborted",
                identity=identity,
                before=state,
                after=after,
                registry_operation_id=registry_operation_id,
                consume_operation_id=context.consume_operation_id,
                cas_outcome="accepted",
                blocker=blocker,
                authoritative_at=now,
                event_id=event_id,
            )
            connection.commit()
        except Exception:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()

    def abort_activation_v2(
        self,
        *,
        context: PreparedCapabilityContextV2,
        schema_path: Path,
        now: str,
        registry_operation_id: str,
        blocker: str,
    ) -> None:
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            _, identity, state = self._require_current_v2(connection, context, schema_path)
            require(state.capability_activation_state == "eligible", "BLOCKED_AUTHORIZATION_CONTEXT_STALE")
            event_id = f"R2EV-{uuid.uuid4()}"
            connection.execute(
                "UPDATE pending_capabilities_v2 SET callable=0 WHERE pending_capability_id=?",
                (state.pending_capability_id,),
            )
            connection.execute(
                """UPDATE authorization_v2_state SET state_version=state_version+1,
                   capability_activation_state='aborted', last_state_event_id=?, state_changed_at=?, terminal_reason=?
                   WHERE registry_record_id=? AND state_version=? AND capability_activation_state='eligible'""",
                (event_id, now, blocker, identity.registry_record_id, state.state_version),
            )
            _, _, after = self._load_v2(connection, identity.authorization_id, schema_path)
            self._insert_v2_event(
                connection,
                event_type="authorization_capability_activation_aborted",
                identity=identity,
                before=state,
                after=after,
                registry_operation_id=registry_operation_id,
                consume_operation_id=context.consume_operation_id,
                cas_outcome="accepted",
                blocker=blocker,
                authoritative_at=now,
                event_id=event_id,
            )
            connection.commit()
        except Exception:
            if connection.in_transaction:
                connection.rollback()
            raise
        finally:
            connection.close()

    def validate_context_v2(self, context: Any, schema_path: Path) -> AuthorizationRegistryStateV2:
        with self._connect() as connection:
            _, identity, state = self._load_v2(connection, context.identity.authorization_id, schema_path)
        if identity != context.identity or state.state_version != context.state.state_version:
            raise PrototypeError("BLOCKED_AUTHORIZATION_CONTEXT_STALE")
        return state

    def state_v2(self, authorization_id: str, schema_path: Path) -> dict[str, Any]:
        with self._connect() as connection:
            artifact, identity, state = self._load_v2(connection, authorization_id, schema_path)
            events = [json.loads(row[0]) for row in connection.execute(
                "SELECT event_json FROM authorization_v2_events WHERE registry_record_id=? ORDER BY rowid",
                (identity.registry_record_id,),
            )]
            pending_count = connection.execute(
                "SELECT COUNT(*) FROM pending_capabilities_v2 WHERE registry_record_id=?",
                (identity.registry_record_id,),
            ).fetchone()[0]
            active_count = connection.execute(
                "SELECT COUNT(*) FROM active_capabilities_v2 WHERE registry_record_id=?",
                (identity.registry_record_id,),
            ).fetchone()[0]
        return {
            "identity": identity.__dict__,
            "state": state.__dict__,
            "events": events,
            "pending_capability_count": pending_count,
            "active_capability_count": active_count,
            "artifact_sha256_recomputed": artifact.artifact_sha256,
        }

    def v2_counts(self) -> dict[str, int]:
        with self._connect() as connection:
            return {
                "identity_rows": connection.execute("SELECT COUNT(*) FROM authorization_v2_identity").fetchone()[0],
                "state_rows": connection.execute("SELECT COUNT(*) FROM authorization_v2_state").fetchone()[0],
                "registry_events": connection.execute("SELECT COUNT(*) FROM authorization_v2_events").fetchone()[0],
                "pending_capabilities": connection.execute("SELECT COUNT(*) FROM pending_capabilities_v2").fetchone()[0],
                "active_capabilities": connection.execute("SELECT COUNT(*) FROM active_capabilities_v2").fetchone()[0],
            }

    def corrupt_authoritative_blob_v2_test_only(self, authorization_id: str, replacement: bytes) -> None:
        with self._connect() as connection:
            changed = connection.execute(
                "UPDATE authorization_v2_identity SET authorization_artifact_bytes=? WHERE authorization_id=?",
                (sqlite3.Binary(replacement), authorization_id),
            ).rowcount
            require(changed == 1, "BLOCKED_AUTHORIZATION_MISSING")
