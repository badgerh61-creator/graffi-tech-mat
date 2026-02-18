# Phase V — End-to-End Validation Scenarios (Journey Tests)

## Purpose (LOCKED)
Prove system-wide invariants across real user journeys:
- Phase U locks
- Phase T stations/tools/flows/modes
- Snapshot lifecycle (draft → child draft → finalize → immutable)
- Tier 4.4 metrics deterministic
- Tier 4.6 preview matches metrics endpoint post-apply
- Conflict detection deterministic (U.3)

These are confidence tests, not unit tests.

## Invariants (LOCKED)
1. Draft locks cannot be bypassed by any API entrypoint.
2. Tool execution must be rejected when station/flow/mode mismatch.
3. Assistant never mutates directly (proposal must go through tool executor + confirmation + hash).
4. Metrics preview is deterministic and must match post-apply computed metrics (within strict tolerance).
5. Conflict detection outcome is deterministic for the same input state.

## Scenario Packs (Minimum)
V.1 Single-user happy path
V.2 Multi-user lock contention + handoff
V.3 Deterministic conflict detection path
V.4 Assistant proposal preview → apply → metrics match
V.5 Failure/recovery (bounded retry + stable status)

## Pass Criteria
- No flakiness
- No sleeps required
- All rejections have explicit reason codes/messages
- Audit events exist for each major action (where applicable)

