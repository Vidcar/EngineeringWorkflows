---
name: codeden-verify
description: "Produce behavioral evidence within an existing CodeDen factory assignment. Use for regression checks, real application paths, UI behavior, interfaces, state, and scoped formal reasoning. This is a bounded method, not a new factory stage, reviewer, or lifecycle."
---

# Prove the relevant behavior

Retain the current factory role, scope, permissions, budget, and native output
contract. Verification does not grant writes to a reviewer or scout, create a
new agent, or authorize merging. Return evidence to the calling stage; that
stage still submits its required native report, verdict, or finish.

## Define the claim and oracle

Identify the observable requirement, preserved behavior, target head/base and
dirty/new content, relevant environment, and expected result. Derive the
expectation from the issue/spec, public contract, known invariant, independent
calculation, or validated baseline. Do not let the implementation under test
define its own correct answer.

Choose checks for the actual remaining risk. Use existing useful tests and
required project commands. Add a regression test for a meaningful repair when
the writing assignment permits it; for reversible mechanical work, a relevant
check can be sufficient. A host-required gate or stricter project condition
still applies.

## Exercise the real relevant path

- For a defect, demonstrate the original failing case and the repaired case
  where practical. Ensure the original failure is the reported symptom, not
  setup failure. Retain the broader user scenario after minimizing a probe.
- For APIs, include input/output, errors, important boundaries, compatibility,
  and externally visible side effects.
- For persisted state, verify write, subsequent read/reload, and isolation or
  recovery behavior where relevant. A rendered success message is insufficient.
- For UI, use the actual route, interaction, responsive/state/error cases
  relevant to the change, and confirm requests/state behind the visible result.
  Capture genuine screenshots when the factory requires them. Do not substitute
  generated images or snapshots for observed behavior.
- For security/concurrency/data changes, exercise representative forbidden and
  valid cases, authorization boundaries, races, idempotency, or rollback as
  implicated by the change. Do not launch unrelated exhaustive suites.
- For a formal model, state assumptions and its mapping to actual code. Treat
  model success as evidence about that model until the real mapping is checked.

Run commands non-interactively. Wait for the commands you start in the same
turn; do not leave a check running while declaring the stage complete.
Respect offline/read-only review restrictions. Do not fetch, change tracked
files, or create persistent fixtures in a role that forbids those effects.

## Interpret evidence honestly

Distinguish:
- **Pass:** the claimed check ran on the identified target and met its oracle.
- **Fail:** the check ran and observed the contrary result; identify whether
  it is introduced by the change or already present in the baseline.
- **Blocked:** setup, access, dependencies, or environment prevented the check.
- **Untested:** the claimed behavior was not exercised.

These are evidence labels, not new CodeDen tool verdicts or stage states.
In review, current-head CI is authoritative for the full suite; map a solely
local environment block through the reviewer's native `blockers` field.
Never report compilation as a user-flow test, a mocked service as an exercised
real integration, or a screenshot as proof of unobserved side effects.

Record the command/steps, target, expected result, actual result, and meaningful
raw output or artifact. Avoid storing secrets. Do not manufacture output,
hide failed attempts, delete useful tests, or weaken assertions for green.

## Refresh only what changed

After an edit, integration, relevant base/dependency change, or environment
change, identify which claims became stale and recheck those. Passing separate
branches/candidates does not prove a combined result. Check important
interactions on the actual combined artifact.

Stop when the assignment's claims have sufficient current evidence or a
specific block is established. Extra repetition needs a remaining risk.
Return the concise evidence and material limits to the current stage; builders
attach results through `attach_evidence`, reviewers use their structured
verdict, and investigation/scout sessions use their assigned native reports.
