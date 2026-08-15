# Portable Runtime R4 Formal Failure 001 Result

Status: `BLOCKED_SANDBOX_ISOLATION_UNPROVEN`

The consumed `R4PS-20260815-001` formal attempt is preserved as immutable failure evidence. The runner discovered and executed 75 leaves: 53 matched their expected result and 22 did not. All 22 failed dispositions were caused by the controller environment reaching the native probe without first establishing the required single-ID user namespace, so the probe failed before its baseline sandbox handshake.

The authoritative `case_results.jsonl` contains 75 records and has SHA-256 `6122439e551b57fc2eb393567eadd0f05584d726f3aa40ef6095fce2b9e0e260`. Its 16 create-once suite artifacts are committed byte-for-byte without repair, overwrite, retry, or identity reuse. Recovery proceeds only through the versioned successor `R4X-20260815-002` / `R4PS-20260815-002`.

Action ledger: model calls 0; Candidate runs 0; English source reads 0; Greek source reads 0; business outputs 0.
