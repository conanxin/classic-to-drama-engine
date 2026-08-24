# P7C Success Criteria

status: `PRE_REGISTERED_BEFORE_REAL_READER_DATA`

## Primary thresholds

| metric | ready-to-rollout threshold | interpretation |
|---|---:|---|
| character recognition accuracy | ≥75% overall | Graphic condition should be directionally ≥10 percentage points above Script when comparable sample exists |
| relationship / identity comprehension | ≥75% | EP19 reader knowledge and scene knowledge must both be understood |
| EP27 action / prop comprehension | ≥70% | who, where, arrow count and armory consequence remain trackable |
| task completion | ≥80% | stop/abandonment is reported, never silently excluded |
| desire to continue | median ≥4/5 or ≥70% positive | not inferred from button presence |
| visual overload | median ≤3/5 | higher is a product warning even when comprehension passes |
| major mode confusion | ≤20% of participants | participant understands Script and Graphic are two reading layers |

## Diagnostic metrics

Help-open rate has no simple “higher is better” target. A healthy exploratory range is 15–65%. More than 80% combined with low comprehension suggests default orientation is insufficient; near-zero use with low comprehension suggests the help is undiscoverable. Mode-switch rate, time to complete and source-layer use are diagnostics, not standalone success measures.

Graphic Mode may be slower if comprehension, orientation and retention are deeper. A time increase up to 25% is acceptable when a primary comprehension metric improves by at least 10 percentage points and overload remains within threshold.

## Decision rules

- **GO:** at least six valid external participants, all primary comprehension thresholds met, no recurring major confusion, and no accessibility blocker.
- **GO_WITH_CHANGES:** comprehension thresholds met but overload, help discoverability, completion or mode clarity requires bounded design changes before scale-up.
- **NO_GO_YET:** any primary comprehension metric below 60%, repeated inability to identify scene actors/relationships, or a major interaction barrier.
- **AWAIT_REAL_READER_EVIDENCE:** fewer than six valid external results or no imported real data. This is the P7C closeout state unless evidence appears.

These thresholds are fixed before real data and must not be moved after seeing results without a new versioned protocol.
