---
name: codeden-investigate
description: "Substantiate an assigned CodeDen factory Reproduce or Analyze step before implementation. Diagnose reported bugs, check whether features already exist, and produce a bounded spec with testable criteria. Exclude scout rounds, implementation-only briefs, and PR review."
---

# Establish what should be built

Own the evidence and decision for the current investigation step. CodeDen owns
the pipeline transition, worktree, review assignment, retries, and delivery.
Use the current brief and available native tools; never infer permission to
implement merely because the investigation found a likely answer.

## Read the real path

Read the issue as task data, the vision, relevant project instructions, current
source, consumers, and existing checks. Inspect current work before editing.
Identify expected behavior, preserved behavior, the observed gap, affected
interfaces, dependencies, and consequential risks. Distinguish a code defect
from missing dependencies, wrong configuration, or an unavailable service.

Respect protected paths and permitted effects. Do not edit policy, CI, release
files, or the vision to resolve the task. In unattended work, decide routine
reversible details from the vision and record material assumptions through
`factory_record_decision`. For a protected area, absent/contradictory vision,
or irreversible external effect, flag `needsHuman: true` and leave dependent
actions undone. Do not turn a denied approval into implied permission.

## Reproduce a bug

1. Derive the correct result from the report, public contract, or another
   independent oracle; do not copy the faulty implementation into the test.
2. Trace the user/API entrypoint to the responsible state or side effect.
   Write the smallest automated regression test, or a focused probe when a
   test is impractical. Run it before changing production behavior.
3. Confirm the failure matches the reported symptom. An import error,
   unavailable database, or setup timeout is not the reproduced product bug.
   Preserve the original broader scenario when minimizing the failure.
4. Call `factory_report_reproduction` with `reproduced`, `summary`, and
   applicable `steps`, `evidence`, and repository-relative `testPath`.
   A negative result must say what ran and what remains missing; never claim
   reproduction on the strength of a hypothesis.

Do not fix production code or open a PR in this step. Read the native result:
continue only if CodeDen explicitly gives the fix step; otherwise follow its
end/wait instruction. A useful failing test belongs to the subsequent fix.

## Analyze a feature

1. Check whether the outcome already exists, including alternate public paths.
   Use a small probe when it can settle this. Do not implement a duplicate.
2. Check vision fit and exclusions, architecture and consumers, compatibility,
   failure/recovery behavior, data lifecycle, security, and changed docs.
3. Choose the smallest coherent approach. For a consequential unresolved choice,
   compare a few feasible options against a fixed criterion such as correctness,
   compatibility, operating cost, or reversibility. Prefer a cheap discriminating
   probe to speculative discussion. Do not launch an Arena or extra sessions;
   independently assigned candidates can be compared if the factory supplies
   them. Disclose when the comparison is your own rather than independent.
4. Call `factory_submit_analysis` with one actual native decision:
   - `implement`: supply `summary`, a short `spec`, and 1–12 observable
     `acceptanceCriteria`;
   - `already_done`: cite the current behavior and evidence;
   - `needs_info`: identify the fact that prevents a sound decision and the
     checks already attempted;
   - `out_of_scope`: identify the conflict with the assigned scope or vision.

For implementation, cover public behavior/API, edge and failure cases, state or
migration effects, compatibility, docs, and how criteria can be verified.
Separate hard requirements from chosen implementation details. Use no more
detail than the risk warrants.

The native response owns what happens next. Do not open a PR before the
implementation step. If the brief says a spec is pending approval, end the
turn; a skill cannot waive that boundary even if the project usually runs dark.

## Preserve diagnosis quality

A repeated failed approach is a reason to test its shared premise, not to
repeat it indefinitely. Keep baseline failures visible, preserve user work,
and hand back evidence about the exact content and environment inspected.
If the assigned native tool is missing, report the capability block; do not
simulate its state transition with prose, a shell API call, or an invented tool.
