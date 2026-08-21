# Architecture

Astro 7 performs a static build. `scripts/build-content-data.mjs` reads only manifest-approved root artifacts, validates their frozen hashes, parses the thirty V2 screenplay files, and stages approved media. Pages import deterministic JSON from `src/generated/`.

The site has no database, server backend, authentication or CMS. Pagefind indexes rendered HTML after Astro builds. GitHub Pages serves the output below the repository base path.

## Layers

1. Frozen project artifacts: authoritative V2/P3/P4/P5 inputs.
2. Publication manifests: explicit document and media boundary.
3. Generated content: deterministic structured page data.
4. Astro routes: reading and archive presentation.
5. Pagefind and verification: static search plus independent build checks.
