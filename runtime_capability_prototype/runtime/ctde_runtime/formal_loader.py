from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

from .common import PrototypeError, require, sha256_bytes
from .events import SignedEventLog
from .signing import FORMAL_TYP, JWSCodec


class FormalLoader:
    def __init__(
        self,
        *,
        codec: JWSCodec,
        issuer_id: str,
        loader_id: str,
        allowed_formal_root: Path,
        candidate_root: Path,
        prototype_root: Path,
    ) -> None:
        self.codec = codec
        self.issuer_id = issuer_id
        self.loader_id = loader_id
        self.allowed_formal_root = allowed_formal_root.resolve()
        self.candidate_root = candidate_root.resolve()
        self.prototype_root = prototype_root.resolve()

    @staticmethod
    def _is_relative_to(path: Path, root: Path) -> bool:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            return False

    def load(
        self,
        signed_manifest: str,
        *,
        events: SignedEventLog,
        before_safe_open: Callable[[dict[str, Any]], None] | None = None,
    ) -> list[dict[str, Any]]:
        try:
            _, manifest = self.codec.verify(
                signed_manifest,
                expected_typ=FORMAL_TYP,
                expected_issuer=self.issuer_id,
                expected_audience=self.loader_id,
                max_ttl=300,
                expected_attempt_id=None,
                require_common=False,
            )
        except PrototypeError as exc:
            events.append("formal_manifest_rejected", {"reason": "signature_or_profile"})
            return []
        entries = manifest.get("entries")
        if (
            not isinstance(entries, list)
            or not isinstance(manifest.get("formal_test_run_id"), str)
            or not manifest["formal_test_run_id"].startswith("FTR-")
            or manifest.get("formal_phase_2_authorized") is not False
        ):
            events.append("formal_manifest_rejected", {"reason": "manifest_schema"})
            return []
        accepted: list[dict[str, Any]] = []
        for entry in entries:
            reason = self._validate_entry(entry)
            if reason:
                events.append("formal_entry_rejected", {"entry_id": entry.get("artifact_id"), "reason": reason})
                continue
            requested = Path(entry["path"])
            try:
                pre_stat = requested.lstat()
            except OSError:
                events.append("formal_entry_rejected", {"entry_id": entry.get("artifact_id"), "reason": "not_found"})
                continue
            if not requested.is_file() or requested.is_symlink() or pre_stat.st_nlink != 1:
                events.append("formal_entry_rejected", {"entry_id": entry.get("artifact_id"), "reason": "link_or_nonregular"})
                continue
            if before_safe_open:
                before_safe_open(entry)
            try:
                descriptor = os.open(requested, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
            except OSError:
                events.append("formal_entry_rejected", {"entry_id": entry.get("artifact_id"), "reason": "safe_open"})
                continue
            try:
                post_stat = os.fstat(descriptor)
                chunks: list[bytes] = []
                while True:
                    chunk = os.read(descriptor, 65536)
                    if not chunk:
                        break
                    chunks.append(chunk)
                content = b"".join(chunks)
            finally:
                os.close(descriptor)
            identity_matches = (
                pre_stat.st_dev == post_stat.st_dev
                and pre_stat.st_ino == post_stat.st_ino
                and pre_stat.st_size == post_stat.st_size
                and pre_stat.st_mtime_ns == post_stat.st_mtime_ns
                and entry.get("device") == post_stat.st_dev
                and entry.get("inode") == post_stat.st_ino
                and entry.get("size_bytes") == post_stat.st_size
                and entry.get("sha256") == sha256_bytes(content)
            )
            if not identity_matches:
                events.append("formal_entry_rejected", {"entry_id": entry.get("artifact_id"), "reason": "toctou_or_digest"})
                continue
            accepted.append(
                {
                    "artifact_id": entry["artifact_id"],
                    "sha256": entry["sha256"],
                    "size_bytes": entry["size_bytes"],
                    "content_input": True,
                    "payload_persisted": False,
                }
            )
            events.append("formal_entry_accepted", {"entry_id": entry["artifact_id"], "sha256": entry["sha256"]})
        events.append("formal_loader_complete", {"formal_content_inputs": len(accepted)})
        return accepted

    def _validate_entry(self, entry: Any) -> str | None:
        if not isinstance(entry, dict):
            return "entry_schema"
        required = {
            "artifact_id",
            "artifact_class",
            "authority",
            "approved",
            "formal_provenance_id",
            "formal_provenance_sha256",
            "path",
            "device",
            "inode",
            "size_bytes",
            "sha256",
        }
        if set(entry) != required:
            return "entry_schema"
        if (
            entry["artifact_class"] != "formal_test_input"
            or entry["authority"] != "formal_test_only"
            or entry["approved"] is not True
            or not str(entry["formal_provenance_id"]).startswith("FPROV-")
            or not isinstance(entry["formal_provenance_sha256"], str)
            or len(entry["formal_provenance_sha256"]) != 64
        ):
            return "formal_provenance"
        raw_path = Path(entry["path"])
        if not raw_path.is_absolute() or ".." in raw_path.parts:
            return "relative_escape"
        resolved = raw_path.resolve(strict=False)
        if self._is_relative_to(resolved, self.candidate_root):
            return "candidate_root"
        if self._is_relative_to(resolved, self.prototype_root):
            return "prototype_root"
        if not self._is_relative_to(resolved, self.allowed_formal_root):
            return "formal_root_or_provenance"
        return None

