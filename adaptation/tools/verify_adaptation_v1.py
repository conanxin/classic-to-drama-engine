from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "adaptation/odyssey_m1_v1"
CORPUS = ROOT / "analysis/formal/odyssey_v1/corpus_manifest.json"
EVENTS = ROOT / "analysis/formal/odyssey_v1/indexes/events.json"
EXPECTED_CORPUS_SHA256 = "0999249a0a25e804dbaa4a393145a7e18d40fe4d1759743cd008a8ab47c1379b"
FIXED_TIME = "2026-08-15T10:10:00Z"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


checks: list[dict[str, object]] = []


def check(name: str, condition: bool, detail: object) -> None:
    checks.append({"check": name, "status": "PASS" if condition else "FAIL", "detail": detail})


manifest = load(OUT / "manifest.json")
architecture = load(OUT / "episode_architecture.json")
ledger = load(OUT / "decision_ledger.json")
continuity = load(OUT / "continuity_bible.json")
event_index = load(EVENTS)

check("corpus_manifest_identity", sha256(CORPUS) == EXPECTED_CORPUS_SHA256, sha256(CORPUS))
check(
    "manifest_status",
    manifest.get("status") == "PASS_ADAPTATION_BIBLE_AND_30_EPISODE_ARCHITECTURE",
    manifest.get("status"),
)

inventory = manifest.get("artifacts", [])
inventory_results = []
for entry in inventory:
    path = ROOT / entry["path"]
    ok = path.is_file() and len(path.read_bytes()) == entry["bytes"] and sha256(path) == entry["sha256"]
    inventory_results.append({"path": entry["path"], "status": "PASS" if ok else "FAIL"})
check(
    "manifest_inventory_exact",
    len(inventory) == manifest.get("artifact_count") == 35 and all(x["status"] == "PASS" for x in inventory_results),
    {"declared": manifest.get("artifact_count"), "verified": len(inventory_results)},
)

cards = [load(OUT / "episode_cards" / f"EP{number:02d}.json") for number in range(1, 31)]
episode_ids = [card.get("episode_id") for card in cards]
episode_numbers = [card.get("episode_number") for card in cards]
check("episode_sequence", episode_ids == [f"EP{i:02d}" for i in range(1, 31)] and episode_numbers == list(range(1, 31)), episode_ids)
check("episode_count", len(cards) == manifest.get("episode_count") == architecture.get("episode_count") == 30, len(cards))

event_records = {event["event_id"]: event for event in event_index["events"]}
decision_records = {item["decision_id"]: item for item in ledger["decisions"]}
card_results = []
covered_books: set[int] = set()
for card in cards:
    source_books = set(card.get("source_books", []))
    covered_books.update(source_books)
    source_events = card.get("source_event_ids", [])
    decision_ids = card.get("adaptation_decision_ids", [])
    event_books = {
        event_records[event_id]["source_span"]["book"]
        for event_id in source_events
        if event_id in event_records
    }
    scene_cards = card.get("scene_cards", [])
    scene_ids = [scene.get("scene_id") for scene in scene_cards]
    functions = [scene.get("function") for scene in scene_cards]
    required_text = [
        card.get("opening_pressure"),
        card.get("midpoint_reversal"),
        card.get("irreversible_turn"),
        card.get("ending_cliffhanger"),
    ]
    ok = all(
        [
            card.get("status") == "locked",
            card.get("target_minutes") == 7,
            len(scene_cards) == 5,
            len(set(scene_ids)) == 5,
            functions == ["opening_pressure", "escalation", "midpoint_reversal", "irreversible_turn", "cliffhanger"],
            all(isinstance(text, str) and text.strip() for text in required_text),
            bool(source_events) and all(event_id in event_records for event_id in source_events),
            event_books.issubset(source_books),
            bool(decision_ids) and all(decision_id in decision_records for decision_id in decision_ids),
            all(decision_records[decision_id].get("status") == "locked" for decision_id in decision_ids),
            bool(card.get("continuity_requirements")),
        ]
    )
    card_results.append({"episode_id": card["episode_id"], "status": "PASS" if ok else "FAIL"})
check("episode_cards_independently_valid", all(x["status"] == "PASS" for x in card_results), card_results)
check("source_books_complete", covered_books == set(range(1, 25)), sorted(covered_books))

embedded = cards[8:15]
check(
    "embedded_books_9_12_frame",
    set(range(9, 13)).issubset({book for card in embedded for book in card["source_books"]})
    and "Phaeacian court" in ledger["decisions"][2]["decision"],
    {"episodes": [card["episode_id"] for card in embedded], "books": sorted({book for card in embedded for book in card["source_books"]})},
)

knowledge_locks = continuity.get("knowledge_locks", [])
through_values = [item.get("through_episode") for item in knowledge_locks]
check(
    "knowledge_continuity_locks",
    len(knowledge_locks) >= 4 and all(isinstance(value, int) and 1 <= value <= 30 for value in through_values),
    knowledge_locks,
)
check(
    "recognition_chain_locked",
    {"Odysseus' scar", "Odysseus' bow", "twelve axes", "olive-tree bed"}.issubset(set(continuity.get("prop_registry", []))),
    continuity.get("prop_registry", []),
)
check(
    "architecture_embeds_exact_cards",
    architecture.get("episodes") == cards,
    {"architecture_cards": len(architecture.get("episodes", [])), "disk_cards": len(cards)},
)

failures = [item for item in checks if item["status"] != "PASS"]
result = {
    "artifact_class": "ctde_adaptation_v1_independent_verification",
    "schema_version": "1.0.0",
    "status": "PASS_ADAPTATION_BIBLE_AND_30_EPISODE_ARCHITECTURE_VERIFIED" if not failures else "BLOCKED_ADAPTATION_VERIFICATION",
    "generated_at": FIXED_TIME,
    "independent_from_builder": True,
    "corpus_manifest_sha256": sha256(CORPUS),
    "adaptation_manifest_sha256": sha256(OUT / "manifest.json"),
    "episode_count": len(cards),
    "source_book_count": len(covered_books),
    "decision_count": len(decision_records),
    "checks": checks,
    "failure_count": len(failures),
}
(OUT / "ADAPTATION_V1_VERIFICATION.json").write_text(
    json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n",
    encoding="utf-8",
)
print(result["status"])
if failures:
    raise SystemExit(1)
