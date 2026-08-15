from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = "AC-20260815-STORYSTRUCT-003"
RUN_ROOT = ROOT / "analysis_candidate/runs" / RUN_ID
SOURCE = ROOT / "source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml"
SOURCE_SHA256 = "dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7"
ALLOWED = {1, 44, 80, 125, 178, 230, 280, 325, 365, 421}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(relative: str) -> dict:
    path = RUN_ROOT / relative
    raw = path.read_bytes()
    value = json.loads(raw)
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n"
    if canonical != raw:
        raise SystemExit(f"BLOCKED_NONCANONICAL:{relative}")
    return value


manifest = load("run_manifest.json")
authorization = load("control/authorization.json")
snapshot = load("input/source_snapshot.json")
scope = load("input/task_scope.json")
execution = load("input/execution_snapshot.json")
story = load("output/story_structure.json")
acceptance = load("evaluation/acceptance_report.json")

if sha(SOURCE) != SOURCE_SHA256 or snapshot["source_sha256"] != SOURCE_SHA256:
    raise SystemExit("BLOCKED_SOURCE_IDENTITY")
if authorization["candidate_run_authorized"] is not True or authorization["one_time_authorization"] is not True:
    raise SystemExit("BLOCKED_AUTHORIZATION")
if authorization["greek_source_content_read_authorized"] is not False or scope["greek_content_allowed"] is not False:
    raise SystemExit("BLOCKED_GREEK_BOUNDARY")
if execution["external_model_calls"] != 0 or execution["automatic_retries"] != 0:
    raise SystemExit("BLOCKED_EXECUTION_CEILING")

records = story["records"]
ids = {record["record_id"] for record in records}
if story["status"] != "PASS_CANDIDATE_BOOK1_STORY_STRUCTURE" or len(records) != story["record_count"] or len(ids) != len(records):
    raise SystemExit("BLOCKED_STORY_INVENTORY")
for record in records:
    span = record["source_span"]
    if span["book"] != 1 or not set(span["evidence_cards"]).issubset(ALLOWED):
        raise SystemExit("BLOCKED_SOURCE_SPAN")
    if record["authority"] != "non_authoritative" or record["formal_phase_2_input"] is not False or record["downstream_consumption_allowed"] is not False:
        raise SystemExit("BLOCKED_AUTHORITY_BOUNDARY")
    parent = record["parent_record_id"]
    if parent is not None and parent not in ids:
        raise SystemExit("BLOCKED_PARENT_LINK")

for item in manifest["artifact_inventory"]:
    path = ROOT / item["path"]
    if not path.is_file() or path.stat().st_size != item["bytes"] or sha(path) != item["sha256"]:
        raise SystemExit(f"BLOCKED_ARTIFACT_DRIFT:{item['path']}")
if acceptance["status"] != "PASS_CANDIDATE_RUN" or not all(acceptance["checks"].values()):
    raise SystemExit("BLOCKED_ACCEPTANCE")

result = {
    "artifact_class": "ctde_candidate_independent_verification",
    "schema_version": "1.0.0",
    "run_id": RUN_ID,
    "status": "PASS_CANDIDATE_INDEPENDENT_VERIFICATION",
    "record_count": len(records),
    "book_count": 1,
    "card_count": len(ALLOWED),
    "artifact_count_verified": len(manifest["artifact_inventory"]),
    "source_identity_exact": True,
    "book1_scope_exact": True,
    "greek_content_reads": 0,
    "external_model_calls": 0,
    "automatic_retries": 0,
    "candidate_authority_preserved": True,
}
print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
