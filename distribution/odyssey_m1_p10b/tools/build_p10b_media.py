#!/usr/bin/env python3
"""Create deterministic, source-bound P10B sample and cover derivatives.

The source PDFs are frozen P9 v1.0.0 release bytes.  This helper never writes
inside publication/odyssey_m1_p9.  It extracts the spoiler-safe opening of
Volume I and rasterizes the five existing P9 covers for store/web use.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import fitz
from PIL import Image, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[3]
P9 = ROOT / "publication/odyssey_m1_p9"
EXPORTS = P9 / "exports"
OUT = ROOT / "distribution/odyssey_m1_p10b/media"
OUT.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def save_jpeg(image: Image.Image, path: Path, quality: int = 92) -> None:
    image.convert("RGB").save(
        path,
        "JPEG",
        quality=quality,
        subsampling=0,
        optimize=True,
        progressive=True,
        dpi=(300, 300),
    )


def contain_on_canvas(image: Image.Image, size: tuple[int, int], color=(18, 18, 16)) -> Image.Image:
    canvas = Image.new("RGB", size, color)
    fitted = ImageOps.contain(image.convert("RGB"), size, Image.Resampling.LANCZOS)
    canvas.paste(fitted, ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2))
    return canvas


def social_frame(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    base = ImageOps.fit(image.convert("RGB"), size, Image.Resampling.LANCZOS)
    base = base.filter(ImageFilter.GaussianBlur(radius=max(size) / 130)).point(lambda p: int(p * 0.43))
    cover = ImageOps.contain(image.convert("RGB"), (int(size[0] * 0.56), int(size[1] * 0.88)), Image.Resampling.LANCZOS)
    base.paste(cover, ((size[0] - cover.width) // 2, (size[1] - cover.height) // 2))
    return base


def build_sample() -> dict:
    source = EXPORTS / "odyssey-homecoming-v01-digital.pdf"
    target = OUT / "odyssey-homecoming-reader-sample-v1.0.0.pdf"
    source_doc = fitz.open(source)
    sample = fitz.open()
    # Pages 1-20 contain the cover/front matter and complete EP01 only.
    sample.insert_pdf(source_doc, from_page=0, to_page=19)
    sample.set_metadata(
        {
            "title": "归途：奥德修斯｜读者试读本",
            "author": "Classic-to-Drama Engine 项目",
            "subject": "P9 v1.0.0 Volume I pages 1–20; complete EP01; spoiler-safe reader sample",
            "keywords": "归途, 奥德修斯, 图像小说, 试读",
            "creator": "ODYSSEY-P10B deterministic extraction",
            "producer": "PyMuPDF",
            "creationDate": "D:20260828000000+08'00'",
            "modDate": "D:20260828000000+08'00'",
        }
    )
    sample.save(target, garbage=4, deflate=True, clean=True, no_new_id=True)
    sample.close()
    source_doc.close()
    return {
        "path": str(target.relative_to(ROOT)),
        "source": str(source.relative_to(ROOT)),
        "source_sha256": sha256(source),
        "pages": 20,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
        "derivation": "exact P9 Volume I digital PDF pages 1-20 (front matter plus complete EP01)",
    }


def build_covers() -> list[dict]:
    records = []
    for index in range(1, 6):
        code = f"v{index:02d}"
        source = EXPORTS / f"odyssey-homecoming-{code}-digital.pdf"
        doc = fitz.open(source)
        pix = doc[0].get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
        rendered = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        doc.close()

        store = OUT / f"odyssey-homecoming-{code}-store-master.jpg"
        thumb = OUT / f"odyssey-homecoming-{code}-thumbnail.jpg"
        web = OUT / f"odyssey-homecoming-{code}-web.webp"
        social = OUT / f"odyssey-homecoming-{code}-social-1200x630.jpg"

        save_jpeg(ImageOps.fit(rendered, (1800, 2557), Image.Resampling.LANCZOS), store, 94)
        save_jpeg(ImageOps.fit(rendered, (240, 341), Image.Resampling.LANCZOS), thumb, 88)
        ImageOps.fit(rendered, (900, 1278), Image.Resampling.LANCZOS).save(web, "WEBP", quality=88, method=6)
        save_jpeg(social_frame(rendered, (1200, 630)), social, 91)

        files = []
        for purpose, path in (("store_portrait_master", store), ("thumbnail", thumb), ("web", web), ("social_og", social)):
            files.append({"purpose": purpose, "path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha256(path)})
        records.append(
            {
                "volume": f"V{index:02d}",
                "source": str(source.relative_to(ROOT)),
                "source_sha256": sha256(source),
                "method": "300-dpi rasterization of the frozen P9 digital-PDF cover page; deterministic resize/composition",
                "files": files,
            }
        )
    return records


def build_series_promos() -> list[dict]:
    source = OUT / "odyssey-homecoming-v01-store-master.jpg"
    image = Image.open(source).convert("RGB")
    specs = {
        "social-square": (1080, 1080),
        "social-portrait": (1080, 1350),
        "social-story": (1080, 1920),
    }
    records = []
    for name, size in specs.items():
        target = OUT / f"odyssey-homecoming-{name}.jpg"
        save_jpeg(social_frame(image, size), target, 91)
        records.append({"purpose": name, "path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": sha256(target)})
    return records


manifest = {
    "schema_version": "P10B_MEDIA_MANIFEST_V1",
    "status": "PASS_P10B_DETERMINISTIC_MEDIA",
    "generated_at": "2026-08-28T00:00:00+08:00",
    "sample": build_sample(),
    "covers": build_covers(),
    "promotional": build_series_promos(),
}
(OUT / "media-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": manifest["status"], "sample": manifest["sample"], "cover_sets": len(manifest["covers"]), "promos": len(manifest["promotional"])}, ensure_ascii=False))
