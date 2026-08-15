# R4 Gate B Versioned Recovery 001 Contract

```yaml
standing_authorization_id: CTDE-GOAL-COMPLETION-20260815-001
recovery_id: R4X-20260815-002
predecessor_suite_id: R4PS-20260815-001
successor_suite_id: R4PS-20260815-002
materialization_phase_id: Phase 2-G-R4FRESH-M2
execution_phase_id: Phase 2-G-R4FRESH-E2
materialization_scope_sha256: 8b30132ddd1c2c819adcb73269c3dd65601a94d5a80839bbec313059a82acdba
materialization_scope_bytes: 3928
gate_b_write_scope_sha256: db661411179360060acec24dd540fdbb29099b68551fb48bd1379ead5c3668ed
gate_b_write_scope_bytes: 2386
```

The predecessor formal attempt is consumed and immutable. Its 16 create-once files, 75 case results, 22 failed dispositions, common `BLOCKED_SANDBOX_ISOLATION_UNPROVEN` terminal, and case-results SHA-256 `6122439e551b57fc2eb393567eadd0f05584d726f3aa40ef6095fce2b9e0e260` are preserved as failure evidence. No successor path may overwrite them or reuse their suite, attempt, authorization, registry, fixture, or case identities.

The lowest-level root cause is jointly classified as `IMPLEMENTATION_ENVIRONMENT_BOOTSTRAP_DEFECT` and `FORMAL_CONTRACT_ENVIRONMENT_BINDING_GAP`. The runner described a chroot plus single-ID user-namespace backend but did not establish that namespace. Formal execution began as UID 1000 with no effective capabilities, broad host UID/GID maps, and `setgroups=allow`; the probe therefore failed its pre-handshake `chroot`. The prior qualification did not bind controller UID, capabilities, maps, or setgroups policy.

The minimal security-preserving successor bootstraps itself before any project import through `/usr/bin/unshare --user --map-root-user`. PASS requires inner UID/GID zero, one UID and one GID mapping of length one, `setgroups=deny`, namespace-local chroot capability, subsequent complete capability drop in the probe, empty chroot, no directory or full-object handles, seccomp mode 2, `NoNewPrivs=1`, no workspace/host/Greek visibility, no network fetch, and unchanged negative-case terminals. The outer mapped UID/GID are evidence, not required to be host root. No sudo, setuid binary, global policy change, sandbox relaxation, skipped leaf, or expected-for-actual substitution is allowed.

The successor implementation must be qualified in a fresh OS-temporary clone before authoritative materialization. Qualification covers targeted positive/path/write/parser/second-channel cases and a complete 37-group actual-N run with independent verification. Only after PASS may the authoritative recovery prefix, closure, freeze, registry and execution authorization be persisted. The closure is a versioned successor to repaired closure `70b48a10b04ff3a31cae8dd2e3224a7d89278031ed95d2b56957618ea3d0326a`; changed predecessor nodes are permitted only for the explicitly inventoried successor implementation paths, while all other predecessor nodes remain byte-exact.

The authoritative recovery materialization scope is the canonical 3,928-byte object with SHA-256 `8b30132ddd1c2c819adcb73269c3dd65601a94d5a80839bbec313059a82acdba`. It binds the six mutable implementation paths, five governance artifacts, successor prefix/evidence/result paths, and the exact 16 predecessor failure files that must be preserved byte-for-byte.

The successor Gate B scope contains exactly 20 create-once files under `R4PS-20260815-002` plus `PORTABLE_RUNTIME_SYNTHETIC_E2E_RESULT_002.md`, with three new directories and no mutable existing Gate B output. Its canonical scope is independently recoverable from the Plan. Python bytecode, model calls, source semantic reads, Candidate runs, and business outputs remain zero throughout R4 recovery.
