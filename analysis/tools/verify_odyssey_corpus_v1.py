from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis/formal/odyssey_v1"
SOURCE = ROOT / "source/translations/en/ody-eng-murray1919/raw/ody-eng-murray1919__raw__full.xml"
SOURCE_SHA256 = "dda5b206e332e56c570c1d92ea41e9a510339a454bc2ea90491788e34174a7e7"


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load(path: Path) -> dict:
    raw = path.read_bytes()
    value = json.loads(raw)
    if raw != json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8") + b"\n":
        raise SystemExit(f"BLOCKED_NONCANONICAL:{path}")
    return value


source_raw = SOURCE.read_bytes()
if len(source_raw) != 870905 or digest(source_raw) != SOURCE_SHA256:
    raise SystemExit("BLOCKED_SOURCE_IDENTITY")
manifest = load(OUT / "corpus_manifest.json")
if manifest["status"] != "PASS_24_BOOK_CORPUS_AND_GRAPHS" or manifest["book_count"] != 24 or manifest["card_count"] != 288:
    raise SystemExit("BLOCKED_MANIFEST_COUNTS")
for item in manifest["artifacts"]:
    path = ROOT / item["path"]
    raw = path.read_bytes()
    if len(raw) != item["bytes"] or digest(raw) != item["sha256"]:
        raise SystemExit(f"BLOCKED_ARTIFACT_DRIFT:{item['path']}")

namespace = "{http://www.tei-c.org/ns/1.0}"
root = ET.fromstring(source_raw)
source_books = [
    element
    for element in root.iter(namespace + "div")
    if element.get("type") == "textpart" and element.get("subtype") == "book"
]
verified_cards = 0
for number, element in enumerate(source_books, start=1):
    record = load(OUT / f"corpus/books/B{number:02d}.json")
    cards = [child for child in element if child.tag == namespace + "div" and child.get("subtype") == "card"]
    locators = [int(card.get("n", "0")) for card in cards]
    if record["book_number"] != number or record["card_locators"] != locators or record["card_count"] != len(cards):
        raise SystemExit(f"BLOCKED_BOOK_LOCATORS:{number}")
    for card, evidence in zip(cards, record["card_evidence"], strict=True):
        text = re.sub(r"\s+", " ", " ".join("".join(card.itertext()).split())).strip().encode("utf-8")
        if evidence["normalized_text_bytes"] != len(text) or evidence["normalized_text_sha256"] != digest(text):
            raise SystemExit(f"BLOCKED_CARD_EVIDENCE:{evidence['native_locator']}")
        verified_cards += 1
    if len(record["key_events"]) != 3 or not record["major_characters"] or not record["locations"] or not record["objects_and_motifs"]:
        raise SystemExit(f"BLOCKED_BOOK_ANALYSIS:{number}")

events = load(OUT / "indexes/events.json")
characters = load(OUT / "indexes/characters.json")
relationships = load(OUT / "graphs/relationships.json")
causal = load(OUT / "graphs/causal.json")
dna = load(OUT / "narrative_dna.json")
if events["event_count"] != 72 or characters["character_count"] != 52 or len(relationships["edges"]) != 14 or len(causal["edges"]) != 34:
    raise SystemExit("BLOCKED_INDEX_GRAPH_COUNTS")
if dna["status"] != "locked" or dna["source_book_coverage"] != list(range(1, 25)) or dna["greek_content_used"] is not False:
    raise SystemExit("BLOCKED_NARRATIVE_DNA")

result = {
    "artifact_class": "ctde_odyssey_corpus_independent_verification",
    "schema_version": "1.0.0",
    "status": "PASS_24_BOOK_CORPUS_INDEPENDENT_VERIFICATION",
    "source_identity_exact": True,
    "books_verified": len(source_books),
    "cards_verified": verified_cards,
    "events_verified": events["event_count"],
    "characters_verified": characters["character_count"],
    "relationship_edges_verified": len(relationships["edges"]),
    "causal_edges_verified": len(causal["edges"]),
    "artifact_count_verified": len(manifest["artifacts"]),
    "book1_formal_analysis_status": "PASS",
    "greek_tei_content_reads": 0,
    "external_model_calls": 0,
}
print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
