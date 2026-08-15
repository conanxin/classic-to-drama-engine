# R4 Gate B Versioned Recovery 001 Plan

## Authority and identities

This Plan is authorized by `CTDE-GOAL-COMPLETION-20260815-001`, recovery `R4X-20260815-002`, successor suite `R4PS-20260815-002`, materialization phase `Phase 2-G-R4FRESH-M2`, and execution phase `Phase 2-G-R4FRESH-E2`.

The predecessor partial execution remains immutable. The successor never overwrites or resumes its create-once paths.

The authoritative materialization scope is 3,928 canonical bytes with SHA-256 `8b30132ddd1c2c819adcb73269c3dd65601a94d5a80839bbec313059a82acdba`. It binds exactly six mutable existing implementation files, five governance files, the successor recovery prefix/evidence/results, and preservation of all 16 predecessor failure files.

## Exact successor Gate B scope

Canonical scope identity: `db661411179360060acec24dd540fdbb29099b68551fb48bd1379ead5c3668ed` over 2,386 bytes.

Creatable directories are exactly:

```text
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-002/fixtures/
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-002/registry/
runtime_capability_prototype/r4_portable_suites/R4PS-20260815-002/aggregate/
```

Creatable files are exactly the three control files, three fixtures/catalog files, three registry files, nine evidence files, one aggregate file under `R4PS-20260815-002`, and `PORTABLE_RUNTIME_SYNTHETIC_E2E_RESULT_002.md`, matching the predecessor relative layout without reusing its namespace.

## Execution strategy

1. Preserve and hash the predecessor failure prefix.
2. Establish process-inception bytecode protection, then inspect UID/GID maps. If the process is not already inner UID/GID zero with one mapping each and `setgroups=deny`, re-exec through fixed `/usr/bin/unshare --user --map-root-user` before project imports.
3. Accept any nonnegative outer UID/GID only when the inner mapping is exactly zero and length exactly one. Persist the actual maps and capabilities.
4. Execute the unchanged temporary verified probe copy. Require chroot, complete capability drop, seccomp, NoNewPrivs, FD/path/network denial, parser/gateway boundaries and cleanup.
5. In a fresh OS-temporary clone, run targeted positive, direct-path, Greek, write-escape, unsafe-parser and second-channel regressions.
6. Build a successor implementation manifest and transitive closure from the repaired closure. Rebuild independently at least twice and require byte identity.
7. Run one full temporary 37-group qualification over actual N leaves and require runner and independent verifier PASS with zero failed/skipped/unknown/timeout/duplicate/reuse/cache/unauthorized-output/action counts.
8. Materialize the byte-identical qualified candidate and recovery governance in the authoritative repository. Persist the predecessor failure prefix and a versioned failure result without changing predecessor bytes.
9. Generate a standing-authorization execution artifact bound to the actual recovery prefix, independently verify it, and execute successor Gate B once.
10. Require `PASS_PORTABLE_RUNTIME_SYNTHETIC_E2E`, independent verifier PASS, exact 20-file scope, commit, normal push, equal local/remote HEAD and CLEAN tree.

Any implementation failure returns to a new OS-temporary clone and a new qualification identity. Formal successor failures are preserved and use a new namespace; no automatic overwrite or identity reuse is permitted.
