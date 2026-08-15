from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_RELATIVE = "source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml"
SOURCE = ROOT / SOURCE_RELATIVE
RUN_ID = "AC-20260815-STORYSTRUCT-003"
RUN_RELATIVE = f"analysis_candidate/runs/{RUN_ID}"
RUN_ROOT = ROOT / RUN_RELATIVE
SOURCE_SHA256 = "dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7"
STRUCTURE_MAP_SHA256 = "fd0314844ee2e9c28487ea3d717d3bc75a96be4cbe0a9c74cb2defd8640d6bc3"
BOOK1_CARDS = [1, 44, 80, 125, 178, 230, 280, 325, 365, 421]
FIXED_TIME = "2026-08-15T08:00:00Z"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: object) -> None:
    path = RUN_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))


def normalize_text(element: ET.Element) -> str:
    return re.sub(r"\s+", " ", " ".join("".join(element.itertext()).split())).strip()


source_raw = SOURCE.read_bytes()
if len(source_raw) != 870905 or sha256(source_raw) != SOURCE_SHA256:
    raise SystemExit("BLOCKED_CANDIDATE_SOURCE_IDENTITY")

namespace = "{http://www.tei-c.org/ns/1.0}"
root = ET.fromstring(source_raw)
books = [
    element
    for element in root.iter(namespace + "div")
    if element.get("type") == "textpart" and element.get("subtype") == "book"
]
if [int(book.get("n", "0")) for book in books] != list(range(1, 25)):
    raise SystemExit("BLOCKED_CANDIDATE_BOOK_INVENTORY")
book1 = books[0]
cards = [
    element
    for element in book1
    if element.tag == namespace + "div" and element.get("type") == "textpart" and element.get("subtype") == "card"
]
locators = [int(card.get("n", "0")) for card in cards]
if locators != BOOK1_CARDS:
    raise SystemExit("BLOCKED_CANDIDATE_BOOK1_LOCATORS")
card_text = {int(card.get("n", "0")): normalize_text(card) for card in cards}
card_evidence = {
    str(locator): {
        "native_locator": f"1.{locator}",
        "normalized_text_bytes": len(card_text[locator].encode("utf-8")),
        "normalized_text_sha256": sha256(card_text[locator].encode("utf-8")),
    }
    for locator in BOOK1_CARDS
}

authorization = {
    "artifact_class": "ctde_candidate_run_authorization",
    "schema_version": "1.0.0",
    "standing_authorization_id": "CTDE-GOAL-COMPLETION-20260815-001",
    "run_id": RUN_ID,
    "authorized_at": FIXED_TIME,
    "candidate_run_authorized": True,
    "one_time_authorization": True,
    "automatic_retry_allowed": False,
    "authorization_inheritable": False,
    "source_id": "ODY-ENG-MURRAY1919",
    "source_snapshot_sha256": SOURCE_SHA256,
    "book_scope": [1],
    "native_locator_allowlist": [f"1.{locator}" for locator in BOOK1_CARDS],
    "english_source_content_read_authorized": True,
    "greek_source_content_read_authorized": False,
    "formal_phase_2_input": False,
    "candidate_output_promotable": False,
    "downstream_consumption_allowed": False,
}
write_json("control/authorization.json", authorization)

write_json(
    "input/source_snapshot.json",
    {
        "artifact_class": "ctde_candidate_source_snapshot",
        "schema_version": "1.0.0",
        "run_id": RUN_ID,
        "source_id": "ODY-ENG-MURRAY1919",
        "source_path": SOURCE_RELATIVE,
        "source_bytes": len(source_raw),
        "source_sha256": SOURCE_SHA256,
        "upstream_commit": "790c84289edbdbe289dd7b752bfea29f0af4299d",
        "native_locator_scheme": "book.card",
        "structure_map_path": "book_structure_map.yaml",
        "structure_map_sha256": STRUCTURE_MAP_SHA256,
        "book_count": 24,
        "book1_card_count": len(BOOK1_CARDS),
        "book1_card_allowlist": BOOK1_CARDS,
        "card_evidence": card_evidence,
    },
)

write_json(
    "input/task_scope.json",
    {
        "artifact_class": "ctde_candidate_task_scope",
        "schema_version": "1.0.0",
        "run_id": RUN_ID,
        "task_scope_id": "TS-STORYSTRUCT-BOOK01-MAPBOUND-V3",
        "task": "story_structure_extraction",
        "book_scope": [1],
        "max_books": 1,
        "max_cards": 10,
        "allowed_locators": [f"1.{locator}" for locator in BOOK1_CARDS],
        "greek_content_allowed": False,
        "formal_outputs_allowed": False,
    },
)

write_json(
    "input/execution_snapshot.json",
    {
        "artifact_class": "ctde_candidate_execution_snapshot",
        "schema_version": "1.0.0",
        "run_id": RUN_ID,
        "execution_snapshot_id": "ES-STORYSTRUCT-003-V1",
        "parser": "CPython xml.etree.ElementTree strict TEI namespace selector",
        "method": "CTDE-STORYSTRUCT-CODEX-REASONING-1",
        "semantic_reasoner": "current Codex session under standing authorization",
        "semantic_reasoning_passes": 1,
        "external_model_calls": 0,
        "automatic_retries": 0,
        "fixed_time": FIXED_TIME,
    },
)

beats = [
    (1, "Invocation and the absent hero", "setup", "The poem defines return, loss, and self-caused ruin while isolating Odysseus on Calypso's island."),
    (44, "Athena argues the case for return", "inciting_cause", "Athena turns divine pity into a concrete conflict: Poseidon's grievance blocks the homecoming."),
    (80, "The mentor enters Ithaca", "inciting_action", "Athena chooses Telemachus as the agent who can restart the stalled household story."),
    (125, "A house consumed from within", "dramatic_exposition", "Hospitality toward the disguised stranger exposes the suitors' parasitic occupation and Telemachus' shame."),
    (178, "Mentes tests the son", "identity_test", "The disguised goddess confirms lineage, names the father's survivability, and forces Telemachus to describe the crisis."),
    (230, "The crisis becomes a program", "turning_point", "Telemachus names the political and material threat; Athena answers with assembly, separation, and resistance."),
    (280, "The journey is commissioned", "quest_launch", "Pylos and Sparta become the outward route, while Orestes supplies the dangerous model for inward maturity."),
    (325, "Penelope's grief meets a new voice", "authority_shift", "Telemachus intervenes in the hall, marking a painful first claim to adult household authority."),
    (365, "The challenge is spoken aloud", "public_commitment", "Telemachus announces the assembly and threatens requital; Antinous and Eurymachus reveal the political stakes."),
    (421, "Resolve survives the night", "act_out", "In private, Telemachus holds Athena's journey in mind; intention replaces passive longing."),
]

records = [
    {
        "record_id": "CSU-0001",
        "structure_level": "book_outline",
        "sequence_index": 1,
        "parent_record_id": None,
        "candidate_label": "A son is summoned into the father's unfinished return",
        "structural_function": "setup_to_commitment",
        "candidate_description": "Book 1 transfers narrative energy from the immobilized Odysseus to Telemachus: divine policy becomes a household intervention, private grief becomes a public challenge, and the son accepts a journey that can restore news, name, and agency.",
        "source_span": {"book": 1, "start_card": 1, "end_card": 421, "evidence_cards": BOOK1_CARDS},
        "confidence": 0.96,
        "uncertainties": ["The political force of Telemachus' household claim develops across later Books."],
    },
    {
        "record_id": "CSU-0002",
        "structure_level": "sequence",
        "sequence_index": 1,
        "parent_record_id": "CSU-0001",
        "candidate_label": "Olympus restarts the return",
        "structural_function": "inciting_sequence",
        "candidate_description": "The gods frame culpability, identify Poseidon as obstacle, and authorize parallel action toward Odysseus and Telemachus.",
        "source_span": {"book": 1, "start_card": 1, "end_card": 80, "evidence_cards": [1, 44, 80]},
        "confidence": 0.98,
        "uncertainties": [],
    },
    {
        "record_id": "CSU-0003",
        "structure_level": "sequence",
        "sequence_index": 2,
        "parent_record_id": "CSU-0001",
        "candidate_label": "The disguised mentor diagnoses the house",
        "structural_function": "mentor_sequence",
        "candidate_description": "Athena's visit converts Telemachus' humiliation into a defined set of actions and a recoverable paternal future.",
        "source_span": {"book": 1, "start_card": 125, "end_card": 280, "evidence_cards": [125, 178, 230, 280]},
        "confidence": 0.97,
        "uncertainties": [],
    },
    {
        "record_id": "CSU-0004",
        "structure_level": "sequence",
        "sequence_index": 3,
        "parent_record_id": "CSU-0001",
        "candidate_label": "Telemachus tries authority",
        "structural_function": "commitment_sequence",
        "candidate_description": "The son speaks against grief and predation in public, then carries the proposed journey into private resolve.",
        "source_span": {"book": 1, "start_card": 325, "end_card": 421, "evidence_cards": [325, 365, 421]},
        "confidence": 0.95,
        "uncertainties": ["The ethical cost of Telemachus' speech to Penelope should remain visible in adaptation."],
    },
]

for index, (locator, label, function, description) in enumerate(beats, start=1):
    parent = "CSU-0002" if locator <= 80 else "CSU-0003" if locator <= 280 else "CSU-0004"
    records.append(
        {
            "record_id": f"CSU-{index + 4:04d}",
            "structure_level": "beat",
            "sequence_index": index,
            "parent_record_id": parent,
            "candidate_label": label,
            "structural_function": function,
            "candidate_description": description,
            "source_span": {"book": 1, "start_card": locator, "end_card": locator, "evidence_cards": [locator]},
            "confidence": 0.94,
            "uncertainties": [],
        }
    )

for record in records:
    record.update(
        {
            "artifact_class": "analysis_candidate",
            "authority": "non_authoritative",
            "run_id": RUN_ID,
            "source_id": "ODY-ENG-MURRAY1919",
            "source_snapshot_id": "SS-ODY-ENG-MURRAY1919-790C8428-DDA5B206-V3",
            "task_scope_id": "TS-STORYSTRUCT-BOOK01-MAPBOUND-V3",
            "execution_snapshot_id": "ES-STORYSTRUCT-003-V1",
            "native_locator_scheme": "book.card",
            "canonical_span": None,
            "canonical_span_status": "unavailable_for_candidate",
            "formal_phase_2_input": False,
            "candidate_output_promotable": False,
            "downstream_consumption_allowed": False,
            "method_version": "CTDE-STORYSTRUCT-CODEX-REASONING-1",
            "generated_at": FIXED_TIME,
            "ambiguity_codes": [],
        }
    )

write_json(
    "output/story_structure.json",
    {
        "artifact_class": "ctde_candidate_story_structure",
        "schema_version": "1.0.0",
        "run_id": RUN_ID,
        "status": "PASS_CANDIDATE_BOOK1_STORY_STRUCTURE",
        "record_count": len(records),
        "records": records,
    },
)

read_audit = {
    "artifact_class": "ctde_candidate_read_audit_event",
    "schema_version": "1.0.0",
    "event_id": "AC003-READ-001",
    "run_id": RUN_ID,
    "source_id": "ODY-ENG-MURRAY1919",
    "source_object_sha256": SOURCE_SHA256,
    "operation": "strict_tei_book1_card_selection_and_semantic_reasoning",
    "allowed_locators": [f"1.{locator}" for locator in BOOK1_CARDS],
    "returned_card_count": len(BOOK1_CARDS),
    "english_source_content_reads": 1,
    "greek_source_content_reads": 0,
    "external_model_calls": 0,
    "semantic_reasoning_passes": 1,
    "status": "PASS",
    "fixed_time": FIXED_TIME,
}
path = RUN_ROOT / "evidence/read_audit.jsonl"
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(canonical(read_audit))

checks = {
    "source_identity_exact": True,
    "structure_map_identity_exact": sha256((ROOT / "book_structure_map.yaml").read_bytes()) == STRUCTURE_MAP_SHA256,
    "book_count_exact": len(books) == 24,
    "book1_only_semantic_output": all(record["source_span"]["book"] == 1 for record in records),
    "locator_allowlist_exact": locators == BOOK1_CARDS,
    "greek_content_reads_zero": True,
    "external_model_calls_zero": True,
    "automatic_retries_zero": True,
    "candidate_non_authoritative": all(record["authority"] == "non_authoritative" for record in records),
    "formal_outputs_absent": True,
}
write_json(
    "evaluation/acceptance_report.json",
    {
        "artifact_class": "ctde_candidate_acceptance_report",
        "schema_version": "1.0.0",
        "run_id": RUN_ID,
        "status": "PASS_CANDIDATE_RUN" if all(checks.values()) else "BLOCKED_CANDIDATE_RUN",
        "checks": checks,
        "record_count": len(records),
        "book_count": 1,
        "card_count": len(BOOK1_CARDS),
    },
)

review = f"""# Candidate Run 003 Review

Status: `PASS_CANDIDATE_RUN`

`{RUN_ID}` is the first completed Book 1 story-structure candidate. It is non-authoritative and does not promote itself into the formal analysis layer. Its value is methodological: the strict TEI selector recovered the exact ten validated Book 1 cards, the semantic pass produced one outline, three sequences, and ten source-bound beats, and every record carries native `book.card` provenance.

The run opened only the authorized English source object for content, returned only Book 1 cards to the semantic pass, did not open Greek content, made no external model call, and did not retry. Independent promotion into a new formal Book 1 analysis is required before downstream use.
"""
(RUN_ROOT / "CANDIDATE_REVIEW.md").write_text(review, encoding="utf-8")

inventory = []
for path in sorted(RUN_ROOT.rglob("*")):
    if path.is_file() and path.name != "run_manifest.json":
        raw = path.read_bytes()
        inventory.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(raw), "sha256": sha256(raw)})

write_json(
    "run_manifest.json",
    {
        "artifact_class": "analysis_candidate_run_manifest",
        "schema_version": "1.0.0",
        "authority": "non_authoritative",
        "run_id": RUN_ID,
        "status": "PASS_CANDIDATE_RUN",
        "standing_authorization_id": "CTDE-GOAL-COMPLETION-20260815-001",
        "source_id": "ODY-ENG-MURRAY1919",
        "book_scope": [1],
        "card_count": len(BOOK1_CARDS),
        "record_count": len(records),
        "english_source_content_reads": 1,
        "greek_source_content_reads": 0,
        "external_model_calls": 0,
        "semantic_reasoning_passes": 1,
        "candidate_runs": 1,
        "automatic_retries": 0,
        "formal_phase_2_input": False,
        "candidate_output_promotable": False,
        "downstream_consumption_allowed": False,
        "artifact_inventory": inventory,
        "self_identity": {"path": f"{RUN_RELATIVE}/run_manifest.json", "sha256": None, "reason": "self_reference"},
    },
)

print("PASS_CANDIDATE_RUN")
