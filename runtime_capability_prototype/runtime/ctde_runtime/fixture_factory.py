from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .common import canonical_json_bytes, sha256_bytes, sha256_file


BOOK1_START = 4076
BOOK1_END = 36515
BOOK1_LENGTH = BOOK1_END - BOOK1_START
SUFFIX_LENGTH = 4096
GENERATOR_ID = "ctde-synthetic-structure-fixture"
GENERATOR_VERSION = "1.0.0"
GENERATOR_SEED = "RCPTS-20260811-001"

PREFIX_SENTINEL = b"PREFIX_DENY_SENTINEL"
BOOK2_SENTINEL = b"BOOK_02_DENY_SENTINEL"
GREEK_SENTINEL = b"FIXTURE_GREEK_DENY"


@dataclass(frozen=True)
class FixtureIdentity:
    object_id: str
    structure_contract_id: str
    structure_contract_sha256: str
    full_path: Path
    greek_path: Path
    full_size: int
    full_sha256: str
    slice_sha256: str
    start_byte: int
    end_byte_exclusive: int
    device: int
    inode: int
    mtime_ns: int
    variant: str


def _repeat_to_length(seed: bytes, length: int) -> bytes:
    return (seed * ((length // len(seed)) + 1))[:length]


def _structural_core(variant: str) -> bytes:
    namespace = "urn:ctde:synthetic"
    book_open = '<BOOK_01 xmlns="urn:ctde:synthetic">'
    book_close = "</BOOK_01>"
    card_count = 10
    paragraph_count = 10
    preamble = ""
    trailer = ""

    if variant == "dtd":
        preamble = "<!DOCTYPE BOOK_01 []>"
    elif variant == "internal_entity":
        preamble = '<!DOCTYPE BOOK_01 [<!ENTITY x "X">]>'
        trailer = "&x;"
    elif variant == "external_file_entity":
        preamble = '<!DOCTYPE BOOK_01 [<!ENTITY x SYSTEM "file:///etc/passwd">]>'
        trailer = "&x;"
    elif variant == "external_network_entity":
        preamble = '<!DOCTYPE BOOK_01 [<!ENTITY x SYSTEM "http://127.0.0.1/x">]>'
        trailer = "&x;"
    elif variant == "wrong_book":
        book_open = '<BOOK_03 xmlns="urn:ctde:synthetic">'
        book_close = "</BOOK_03>"
    elif variant == "wrong_namespace":
        namespace = "urn:ctde:wrong"
        book_open = f'<BOOK_01 xmlns="{namespace}">'
    elif variant == "extra_card":
        card_count = 11
        paragraph_count = 11
    elif variant == "missing_card":
        card_count = 9
        paragraph_count = 9
    elif variant == "extra_paragraph":
        paragraph_count = 11
    elif variant == "missing_paragraph":
        paragraph_count = 9

    pieces = [preamble, book_open, "<UTF8_MARKER>多字节</UTF8_MARKER>"]
    for index in range(1, card_count + 1):
        pieces.append(f"<CARD_{index:02d}>")
        if index <= paragraph_count:
            pieces.append(f"<PARA_{index:02d}/>")
        if variant == "extra_paragraph" and index == card_count:
            pieces.append("<PARA_11/>")
        pieces.append(f"</CARD_{index:02d}>")
    if variant == "duplicate_book1":
        pieces.append("<BOOK_01/>")
    if variant == "book2_marker":
        pieces.append("<BOOK_02/>")
    pieces.append(trailer)
    if variant != "recovery":
        pieces.append(book_close)
    return "".join(pieces).encode("utf-8")


def _allowed_zone(variant: str) -> bytes:
    core = _structural_core(variant)
    pad_open = b"<PAD>"
    pad_close = b"</PAD>"
    insertion = core.rfind(b"</BOOK_")
    if insertion < 0:
        insertion = len(core)
    room = BOOK1_LENGTH - len(core) - len(pad_open) - len(pad_close)
    if room < 0:
        raise ValueError("synthetic structural core exceeds Book 1 range")
    padding = _repeat_to_length(b"SYNTHETIC_PAD_0123456789_", room)
    return core[:insertion] + pad_open + padding + pad_close + core[insertion:]


def recipe() -> dict[str, Any]:
    return {
        "generator_id": GENERATOR_ID,
        "generator_version": GENERATOR_VERSION,
        "seed": GENERATOR_SEED,
        "literary_content_present": False,
        "prefix_range": {"start_byte": 0, "end_byte_exclusive": BOOK1_START},
        "book1_range": {"start_byte": BOOK1_START, "end_byte_exclusive": BOOK1_END},
        "book1_length": BOOK1_LENGTH,
        "book1_card_markers": 10,
        "book1_paragraph_markers": 10,
        "suffix_range": {"start_byte": BOOK1_END, "length": SUFFIX_LENGTH},
        "greek_deny_object": "host_only_synthetic_non_literary",
        "offset_unit": "raw_utf8_bytes",
        "interval_kind": "zero_based_half_open",
        "supported_variants": [
            "baseline",
            "dtd",
            "internal_entity",
            "external_file_entity",
            "external_network_entity",
            "recovery",
            "book2_marker",
            "duplicate_book1",
            "wrong_book",
            "extra_card",
            "missing_card",
            "extra_paragraph",
            "missing_paragraph",
            "wrong_namespace",
        ],
    }


def generate_fixture(root: Path, *, attempt_id: str, variant: str = "baseline") -> FixtureIdentity:
    root.mkdir(parents=True, exist_ok=False)
    os.chmod(root, 0o700)
    prefix = _repeat_to_length(PREFIX_SENTINEL + b"|", BOOK1_START)
    allowed = _allowed_zone(variant)
    suffix = _repeat_to_length(BOOK2_SENTINEL + b"|", SUFFIX_LENGTH)
    full_bytes = prefix + allowed + suffix
    full_path = root / "synthetic_full_fixture.bin"
    greek_path = root / "synthetic_greek_deny.bin"
    with full_path.open("xb") as handle:
        handle.write(full_bytes)
        handle.flush()
        os.fsync(handle.fileno())
    with greek_path.open("xb") as handle:
        handle.write(GREEK_SENTINEL + b"|" + _repeat_to_length(b"GREEK_DENY_PAD|", 1024))
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(full_path, 0o400)
    os.chmod(greek_path, 0o400)
    stat = full_path.stat()
    contract_bytes = canonical_json_bytes(recipe())
    contract_digest = sha256_bytes(contract_bytes)
    full_digest = sha256_bytes(full_bytes)
    return FixtureIdentity(
        object_id=f"urn:ctde:fixture:{full_digest}",
        structure_contract_id=f"urn:ctde:fixture-structure:{contract_digest}",
        structure_contract_sha256=contract_digest,
        full_path=full_path,
        greek_path=greek_path,
        full_size=len(full_bytes),
        full_sha256=full_digest,
        slice_sha256=sha256_bytes(allowed),
        start_byte=BOOK1_START,
        end_byte_exclusive=BOOK1_END,
        device=stat.st_dev,
        inode=stat.st_ino,
        mtime_ns=stat.st_mtime_ns,
        variant=variant,
    )


def fixture_attestation(identity: FixtureIdentity) -> dict[str, Any]:
    return {
        "artifact_class": "synthetic_fixture_identity_attestation",
        "environment": "prototype_fixture_only",
        "fixture_object_id": identity.object_id,
        "fixture_structure_contract_id": identity.structure_contract_id,
        "fixture_structure_contract_sha256": identity.structure_contract_sha256,
        "variant": identity.variant,
        "size_bytes": identity.full_size,
        "full_sha256": identity.full_sha256,
        "book1_range": {
            "start_byte": identity.start_byte,
            "end_byte_exclusive": identity.end_byte_exclusive,
        },
        "book1_slice_sha256": identity.slice_sha256,
        "contains_literary_content": False,
        "path_persisted": False,
        "payload_persisted": False,
    }


def greek_existence_attestation(identity: FixtureIdentity) -> dict[str, Any]:
    stat = identity.greek_path.stat()
    return {
        "artifact_class": "synthetic_greek_fixture_existence_attestation",
        "environment": "prototype_fixture_only",
        "object_id": f"urn:ctde:fixture-greek-deny:{sha256_file(identity.greek_path)}",
        "size_bytes": stat.st_size,
        "sha256": sha256_file(identity.greek_path),
        "exists_at_fixture_controller": stat.st_size > 0,
        "broker_catalogued": False,
        "consumer_mounted": False,
        "path_persisted": False,
        "payload_persisted": False,
    }

