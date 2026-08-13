# Runtime Capability Prototype Test Report

Suite: `RCPTS-20260811-002`  
Result: `BLOCKED_RUNTIME_CAPABILITY_PROTOTYPE_FAILED`  
Environment: `prototype_fixture_only`

## Runner enumeration

- Manifest leaf count: `197`
- Runner discovered: `197`
- Runner executed: `197`
- Evidence complete: `197`
- Passed: `99`
- Failed: `98`
- Skipped: `0`
- Unknown: `0`
- Requirement groups: `37`
- Enumeration counts match: `True`
- Full PASS acceptance counts match: `False`

## Capability findings

- Book 1 exact range `[4076,36515)`: `NOT PROVEN`.
- Book 2 direct broker range rejection: `PROVEN`.
- Book 2 consumer/parser/gateway isolation: `NOT PROVEN`.
- Consumer full-object path/handle isolation: `NOT PROVEN`.
- Synthetic Greek broker-role rejection: `PROVEN`.
- Synthetic Greek consumer-path isolation: `NOT PROVEN`.
- Authorization existence, one-shot CAS, replay, concurrency and crash semantics: `PROVEN`.
- Formal allowlist, positive control and TOCTOU rejection: `PROVEN`.
- Complete independent read audit: `NOT PROVEN`.

## Blockers

- `MANDATORY_LEAF_TEST_FAILURE`
- `BLOCKED_SANDBOX_ISOLATION_UNPROVEN`
- `ZERO_REAL_SOURCE_ACCESS_PROOF_FAILED`
- `TRACE_MONITOR_UNAVAILABLE_PTRACE_DENIED`

## Zero-real-source boundary

- English real raw stat/open/read/hash: `unknown (monitor unavailable) / unknown (monitor unavailable) / unknown (monitor unavailable) / unknown (monitor unavailable)`
- Greek real raw stat/open/read/parse/copy: `unknown (monitor unavailable) / unknown (monitor unavailable) / unknown (monitor unavailable) / unknown (monitor unavailable) / unknown (monitor unavailable)`
- Project source tree scans: `unknown (monitor unavailable)`
- `book_structure_map.yaml` reads: `unknown (monitor unavailable)`
- Model invocations: `0`
- Candidate Runs executed: `0`
- Business outputs created: `0`

This is prototype evidence only. It does not authorize any Candidate Run or mark any production `P2ER-*` Gate PASS.
