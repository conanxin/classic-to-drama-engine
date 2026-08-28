# P10 Kindle Compatibility Report

status: `READY_WITH_PLATFORM_SPECIFIC_ACTION`

P9 EPUB files are valid EPUB 3 fixed-layout books and remain useful source inputs, but P10B does **not** equate that with Kindle acceptance. Amazon's current official guidance treats graphic novels as fixed-layout comic books and requires Kindle-specific metadata and panel behavior. MOBI is no longer an accepted fixed-layout submission format.

## Mapping

- five EPUB sources: identity-bound and under 100 MB each
- separate store covers: prepared; KDP-specific 1600 × 2560 derivative remains an upload-time choice
- fixed layout: present in P9 EPUB
- exact Kindle comic metadata/Panel View: requires conversion or package inspection
- Kindle Previewer/Kindle Create: external manual validation required
- ISBN: not required for Kindle ebook; Amazon assigns ASIN

## Required manual action

1. Open each volume in the current Kindle Previewer or import through Kindle Create's comic/fixed-layout workflow.
2. Confirm reading order, synthetic spreads, Panel View/Virtual Panels, cover and Chinese glyphs on representative phone, tablet and e-ink profiles.
3. Export the current accepted KPF/EPUB package if conversion is required.
4. Recompute the submitted-file digest and append it to the platform receipt before upload.

STORE_SUBMISSION: `NOT_EXECUTED`  
STORE_ACCEPTANCE: `NOT_CLAIMED`
