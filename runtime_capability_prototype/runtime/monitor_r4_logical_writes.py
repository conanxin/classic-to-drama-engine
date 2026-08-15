from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "1.0.0"
ARTIFACT_CLASS = "ctde_r4_portable_logical_write_event"
PRODUCER_ID = "ctde-r4-portable-logical-write-monitor"


class LogicalWriteViolation(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8") + b"\n"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _normal_relative(path: str) -> str:
    candidate = Path(path)
    if candidate.is_absolute() or path.startswith(("/", "\\")):
        raise LogicalWriteViolation("absolute project path is forbidden")
    normalized = Path(os.path.normpath(path)).as_posix()
    if normalized in {"", ".", ".."} or normalized.startswith("../"):
        raise LogicalWriteViolation("path traversal is forbidden")
    return normalized


class LogicalWriteMonitor:
    """Portable A1 logical write policy and in-memory evidence chain.

    The controller remains the sole persistent writer.  This monitor decides
    and records each logical attempt before the controller performs it.  It
    intentionally does not claim syscall-complete A2 observation.
    """

    def __init__(
        self,
        *,
        project_root: Path,
        create_once_paths: Iterable[str],
        append_only_paths: Iterable[str],
        temporary_root: Path,
        snapshot_identity: str,
        fixed_time: int,
    ) -> None:
        self.project_root = project_root.resolve(strict=True)
        self.temporary_root = temporary_root.resolve(strict=True)
        self.create_once_paths = frozenset(_normal_relative(item) for item in create_once_paths)
        self.append_only_paths = frozenset(_normal_relative(item) for item in append_only_paths)
        if self.create_once_paths & self.append_only_paths:
            raise LogicalWriteViolation("write classes overlap")
        self.snapshot_identity = snapshot_identity
        self.fixed_time = fixed_time
        self._events: list[dict[str, Any]] = []
        self._created: set[str] = set()

    @property
    def events(self) -> tuple[dict[str, Any], ...]:
        return tuple(dict(item) for item in self._events)

    def _project_relative(self, requested: Path) -> tuple[str | None, Path]:
        resolved = requested.resolve(strict=False)
        try:
            relative = resolved.relative_to(self.project_root).as_posix()
        except ValueError:
            relative = None
        return relative, resolved

    def _classify(self, requested: Path, operation: str) -> tuple[str, bool, str | None, str | None, Path]:
        relative, resolved = self._project_relative(requested)
        if relative is not None:
            if relative.startswith("source/") or relative == "book_structure_map.yaml":
                return "source_layer", False, "BLOCKED_R4_SOURCE_WRITE", relative, resolved
            if relative.startswith("analysis_candidate/"):
                return "candidate", False, "BLOCKED_R4_CANDIDATE_WRITE", relative, resolved
            if relative in self.create_once_paths:
                allowed = operation == "create" and relative not in self._created and not resolved.exists()
                blocker = None if allowed else "BLOCKED_R4_CREATE_ONCE_VIOLATION"
                return "gate_b_create_once", allowed, blocker, relative, resolved
            if relative in self.append_only_paths:
                allowed = operation == "append"
                blocker = None if allowed else "BLOCKED_R4_APPEND_ONLY_VIOLATION"
                return "gate_b_append_only", allowed, blocker, relative, resolved
            return "existing_project" if resolved.exists() else "outside_allowlist", False, "BLOCKED_R4_WRITE_SCOPE", relative, resolved
        try:
            resolved.relative_to(self.temporary_root)
            allowed = operation in {"create", "append"}
            return "os_temporary_leaf", allowed, None if allowed else "BLOCKED_R4_TEMP_OPERATION", None, resolved
        except ValueError:
            return "outside_allowlist", False, "BLOCKED_R4_WRITE_SCOPE", None, resolved

    def attempt(
        self,
        *,
        attempt_id: str,
        operation: str,
        requested_path: Path,
        bytes_requested: int,
        bytes_written: int = 0,
    ) -> dict[str, Any]:
        if operation not in {"create", "append", "replace", "delete", "rename"}:
            raise LogicalWriteViolation("unknown logical operation")
        if type(bytes_requested) is not int or bytes_requested < 0:
            raise LogicalWriteViolation("invalid requested byte count")
        if type(bytes_written) is not int or bytes_written < 0 or bytes_written > bytes_requested:
            raise LogicalWriteViolation("invalid written byte count")
        path_class, allowed, blocker, relative, resolved = self._classify(requested_path, operation)
        if not allowed and bytes_written != 0:
            raise LogicalWriteViolation("denied write reports nonzero bytes")
        if allowed and operation == "create" and relative is not None:
            self._created.add(relative)
        previous = sha256_bytes(canonical_bytes(self._events[-1])) if self._events else None
        event = {
            "artifact_class": ARTIFACT_CLASS,
            "schema_version": SCHEMA_VERSION,
            "sequence": len(self._events) + 1,
            "attempt_id": attempt_id,
            "operation": operation,
            "requested_path_class": path_class,
            "resolved_path": str(resolved),
            "allowed": allowed,
            "blocker": blocker,
            "bytes_requested": bytes_requested,
            "bytes_written": bytes_written,
            "producer_id": PRODUCER_ID,
            "previous_event_sha256": previous,
            "fixed_time": self.fixed_time,
            "snapshot_identity": self.snapshot_identity,
        }
        self._events.append(event)
        return dict(event)

    def jsonl_bytes(self) -> bytes:
        return b"".join(canonical_bytes(event) for event in self._events)

    def verify_chain(self) -> None:
        previous: str | None = None
        for sequence, event in enumerate(self._events, start=1):
            if event.get("sequence") != sequence or event.get("previous_event_sha256") != previous:
                raise LogicalWriteViolation("logical write chain mismatch")
            if event.get("allowed") is False and event.get("bytes_written") != 0:
                raise LogicalWriteViolation("denied write side effect")
            previous = sha256_bytes(canonical_bytes(event))


def denied_probe_event(
    project_root: Path,
    temporary_root: Path,
    snapshot_identity: str,
    fixed_time: int,
) -> dict[str, Any]:
    monitor = LogicalWriteMonitor(
        project_root=project_root,
        create_once_paths=(),
        append_only_paths=(),
        temporary_root=temporary_root,
        snapshot_identity=snapshot_identity,
        fixed_time=fixed_time,
    )
    event = monitor.attempt(
        attempt_id="RCPT-R4-WRITE-PROBE",
        operation="create",
        requested_path=project_root / "forbidden-r4-write-probe",
        bytes_requested=1,
        bytes_written=0,
    )
    monitor.verify_chain()
    return event
