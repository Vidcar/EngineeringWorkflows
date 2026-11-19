---
name: codeden-build
description: "Implement an assigned CodeDen factory feature, reproduced bug, docs change, revision, or explicitly requested rebuild. Produce a focused change and current evidence through CodeDen's PR and finish tools. Exclude initial analysis/reproduction, independent review, and integration-only tasks."
---

# Deliver the assigned change

Own the assigned implementation and its evidence. CodeDen owns work allocation,
worktrees, independent review, retry counters, merge policy, and cleanup.
Do not start another workflow owner, campaign, review panel, merge loop, or
self-directed deployment.

## Recover the actual assignment

Read the current step, issue, spec/reproduction, acceptance criteria, latest
review/check failures, vision, and project instructions. Inspect branch, base,
dirty/new files, and any existing PR. Preserve work you do not own. On resume,
reconcile what actually completed before repeating remote effects.

Stay in the assigned worktree and branch. A revision normally updates the same
PR. A rebuild or post-revert repair may require a fresh branch/PR; follow that
explicit brief instead of imposing a universal same-branch rule. Never replace
a writer or clean a worktree because a timeout suggests it might be idle.

If still at Analyze or Reproduce, return to that native step. Do not skip its
reporting tool. If a protected change, missing/contradictory vision, or an
irreversible external action blocks the work, record the decision with
`needsHuman: true` when available, leave dependent actions undone, and use
`finish` with outcome `blocked` if the assigned result cannot be completed.
Routine reversible choices should follow the vision and be stated in the PR.

## Implement coherently

- Fix the responsible path rather than masking a symptom. Keep a reproduced
  bug's failing test and show it passing after the repair.
- Meet the recorded criteria and preserve established callers, compatibility,
  state ownership, and error/recovery behavior. Trace consumers when changing
  an interface. Add an abstraction only when current needs justify it.
- Keep unrelated cleanup, speculative features, policy changes, and external
  actions outside this assignment. Do not weaken tests or gates to obtain green.
- For a revision, address the actual confirmed defects and check failures.
  Test a disputed premise before repeating a failing fix. Distinguish an
  environment problem or inherited baseline failure from a new code defect.
- For docs, verify commands, paths, options, examples, and API claims against
  current source. Disclose any necessary non-docs change; never label code or
  instruction changes as docs-only to avoid review.
- Preserve meaningful tests and rationale. Remove only your own temporary
  probes/resources once their useful evidence is retained.

Scale scrutiny to the risk inside the required factory stages. A trivial edit
does not waive a host-mandated gate. A consequential change warrants explicit
checks of its failure, security, migration, or concurrency risks. Do not claim
self-review is the factory's independent review.

## Prove the current result

Use `codeden-verify` as a bounded method when useful, or apply its essentials:
derive expectations independently, exercise the real relevant entrypoint and
side effects, check important negative paths, and run required project checks.
Record commands, outcomes, target revision/dirty state, and relevant environment.
Separate pass, fail, blocked, and untested in the evidence without inventing a
new native outcome.

Run commands non-interactively and wait for installs, builds, and tests in the
same turn. Do not end the turn while a check you started is still running.
If visible UI changed, exercise the relevant flow and capture actual screenshots;
an image alone does not prove persistence, requests, or accessibility behavior.
If no new test is warranted, explain why; do not add meaningless tests merely
to satisfy a file-pattern check.

Refresh affected evidence after fixes, dependency changes, or rebases.
Do not reuse evidence from older bytes as proof of the final change.
Use `codeden-measure` only for a required quantitative claim.

## Complete the native handoff

1. Inspect the complete intended diff, including new files. Commit the intended
   result in the assigned branch.
2. Use `create_pull_request` to create or update the assigned PR, following the
   brief. Include the concrete problem, resulting behavior, assumptions, and a
   `## Test results` section with real commands and outcomes. For bugs, include
   the before/after reproduction.
3. Attach current raw output through `attach_evidence` using `testOutput`;
   attach actual UI screenshots through its `files` input when required.
4. Read the tool responses and confirm the resulting PR and evidence. If a
   request timed out or its effect is uncertain, reconcile native state before
   retrying. Do not open a duplicate PR to bypass a failure.
5. Call `finish` with the native schema's outcome, summary, tests, and changed
   files. Report any material limits accurately.

Do not merge, approve your own PR, release, edit factory settings, or declare
the factory run finished. Your endpoint is the handed-off change; CodeDen
decides its next stage.
