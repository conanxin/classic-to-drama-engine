# P9 Typography Specification

status: `FROZEN_P9_TYPOGRAPHY`

## Font policy

The build uses the installed open-source Noto Sans CJK SC family and embeds/subsets it in PDF output where the renderer permits. No font binaries are added to the repository. Fallbacks are Source Han Sans SC, Droid Sans Fallback, then a generic sans-serif. The chosen Noto CJK family is distributed under the SIL Open Font License 1.1.

## Print sizes

| Role | Size | Line height | Treatment |
|---|---:|---:|---|
| Series title | 25–31 pt | 1.05 | restrained display, no synthetic Greek ornament |
| Chapter title | 20–25 pt | 1.1 | paired with episode number |
| Speech | 10.2 pt minimum | 1.42 | white/near-white bubble; speaker in 7.6 pt small caps treatment |
| Caption | 9.4 pt minimum | 1.5 | warm paper strip; never shaped like a missing panel |
| Character guide | 8.8 pt minimum | 1.45 | spoiler-safe short identity only |
| Note / provenance | 7.8 pt minimum | 1.45 | reserved for front/back matter |
| Folio | 7.5 pt | 1 | outside lower corner; hidden on chapter openers |

Chinese punctuation uses normal CJK line-breaking. Widows/orphans and lone punctuation are avoided where the renderer supports it. Speech and caption text remain searchable vector text in PDF and semantic XHTML in EPUB. Rasterized CBZ text is generated deterministically from this same typography master.
