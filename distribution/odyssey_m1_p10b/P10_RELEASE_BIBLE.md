# P10B Public Release Bible

status: `PASS_P10B_RELEASE_BIBLE`

P10B is a distribution and reader-facing layer over the frozen P9 Digital Graphic Novel Edition 1.0.0. It does not change story, art, pages, panel mapping or any of the 21 release binaries.

## Reader promise

一个关于归乡、身份与被重新认出的故事。 A reader can begin online, continue across 30 graphic episodes, understand the five-volume structure, select PDF/EPUB/CBZ by device, download from the canonical release and verify the exact bytes.

## Release architecture

- /read/: primary reader entry and volume/episode orientation
- /publication/: download center for ordinary reading formats; print masters remain advanced
- /publication/verify/: 21 SHA-256 identities and verification instructions
- /about/: reader-facing work and edition explanation
- /project/: deep technical archive, preserved but visually subordinate

## Boundaries

No store listing, price, territory, tax/bank setup, ISBN purchase, print order, outreach or payment is executed. Platform packages are preparation material and dated requirement mappings. P6 remains `PAUSED_BY_USER`.
