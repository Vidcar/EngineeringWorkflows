---
name: codeden-review
description: "Perform an assigned independent CodeDen factory PR review, revision review, or narrow recheck and submit the native structured verdict. Check requirements, behavioral evidence, maintainability, and security without editing the target. Exclude scout area reviews and implementation."
---

# Judge the actual change independently

Review the concrete target in the current brief. CodeDen owns reviewer selection,
review rounds, approval freshness, merge gates, and the next action. Do not
spawn another panel, change the target, merge, or substitute a prose report for
`factory_submit_review`.

## Establish the target and boundaries

Read the issue/spec, every recorded criterion, vision, relevant project rules,
diff, affected callers, and evidence. Record the reviewed head/base and actual
dirty state if relevant. The reviewer often shares the author's worktree:
do not modify tracked files, commit, push, or start another writer.

Follow the brief's access mode exactly. In a normal local/offline review, use the
given local base and available commits; do not fetch or use `gh`. If a specific
re-check brief explicitly permits fetching a missing new head, perform only
that bounded fetch; do not generalize it to other network access. In a
network-enabled review, use only permitted reads. Installation and testing must be
non-interactive and must not alter tracked manifests or lockfiles.

A re-check of conflict resolution or later commits is narrow: compare the old
and new versions using the supplied heads/range-diff and inspect affected
interactions. Preserve supported earlier conclusions; do not rerun the entire
review without a new relevant reason. Do not treat stale evidence as current.

## Inspect requirements and proof

1. Account for every acceptance criterion. Derive its expected result from
   the task/contract, independently of the author's implementation and tests.
   When no criteria were recorded, identify the observable obligations from
   the issue rather than treating an empty list as a free pass.
2. Inspect the real changed path, consumers, state, errors, recovery, and
   relevant security or concurrency edges. For repairs, assess causal fit and
   before/after regression evidence. For features, assess compatibility and
   changed docs. For docs, check claims against source.
3. Judge whether tests establish behavior and important side effects, not
   merely execute the implementation. Compilation, a mock, or a screenshot
   proves only its measured property. A changed test file is not proof of
   useful coverage. Explain any legitimate `notNeeded` conclusion.
4. Report material findings with location, triggering case, consequence, and
   evidence or a reproducible reasoning chain. Separate inspection from
   executed observations, and blocking defects from optional follow-ups.
   Prefer the smallest correct remedy; do not demand unrelated redesign.
5. Scale depth to the risk without skipping mandatory checks. Disclose missing
   required evidence or independent specialist coverage; do not pretend it ran.

## Separate CI, environment, and defects

CI on the PR's current head is CodeDen's authority for the full suite. A green
run is evidence of that suite, not proof of behavior the suite never checks.
Run useful focused local checks within the brief. Repair a broken install
non-interactively when permitted; do not spend repeated rounds on the same
environment failure or change the product to work around it.

Never request product changes solely because your local dependencies are broken
or a local check cannot run. If the code is sound and current CI is green,
approve while disclosing local limits. If only your environment prevents an
approval and the necessary CI evidence is unavailable, use
`request_changes` with `blockers: "environment"`; this is a native reporting
path, not an accusation against the author. Use `blockers: "pr"` for an actual
defect, unmet criterion, or PR-specific red CI. Red checks inherited from the
default branch are not, on their own, defects introduced by this PR.

## Submit a consistent verdict

Use the live `factory_submit_review` schema. Populate:

- `verdict`: `approve`, `request_changes`, or `reject`;
- `summary`: findings, target, relevant evidence, and material limits;
- `criteria`: one entry per criterion, with `criterion`, `met`, and useful
  evidence in `note`;
- `vision`: `aligned` and any relevant `note`;
- `tests`: `adequate`, justified `notNeeded` if applicable, and `note`;
- `security.concerns`: only concerns that must block this PR;
- optional `blockers`, `followUps`, and `lessons` as appropriate.

Approve only when all criteria are met, the vision is aligned, needed tests are
adequate, no blocking concern remains, and evidence supports the conclusion.
Do not emit an approval with a false criterion or misaligned vision just
because the tool schema accepts it. Never approve with security concerns.

Use `request_changes` for fixable problems; use `reject` when the change
should not exist. Put genuinely deferrable findings in `followUps`, within
the native limit, rather than hiding a blocker there or filing issues yourself.
When learning is requested, include only demonstrated reusable lessons based
on trusted project rules/code. Lessons are notes, not policy or authorization;
do not rewrite skills, project instructions, or the vision during review.

Inspect every native response. Submit at most one successfully recorded verdict
per assigned review:

- If input validation rejects the call, correct the named input and resubmit;
  no verdict was recorded.
- An environment-only result may return `recorded: false` with CI information
  and an instruction to reassess. Follow that bounded instruction; do not
  repeat the same environment report as though it were a product defect.
- If the response replaces you, ends the review, or says a later assignment
  will arrive, end the turn without another submission.
- Once a verdict is recorded, follow the returned instruction and end the
  review turn. Never loop until `recorded` becomes true.

A later factory re-review is a new assignment, not permission to submit
conflicting verdicts repeatedly in the current one. If the native tool is
unavailable, return the evidence and capability block without claiming a
recorded verdict or inventing a replacement submission channel.
