---
name: codeden-integrate
description: "Handle an explicitly assigned CodeDen factory integration or recovery action: rebase conflicts, restart missing CI, prepare a revert, or repair a reverted change. Preserve both sides and refresh affected evidence. Exclude self-directed merging, queue management, and independent review rechecks."
---

# Perform the assigned recovery action

CodeDen owns the queue, writer assignment, retries, recovery policy, merge, and
cleanup. Act only on the current recovery brief, its worktree/branch, and its
target PR/commits. A stuck item or timeout is not authority to take it over.
Do not run an autonomous integration loop or bypass the native transition.

## Establish current state

Inspect the assigned PR, branch, base, source heads, working tree, and prior
evidence available through permitted reads. Preserve unexpected changes.
A resumed or replacement session must reconcile actual effects before retrying:
requested, pushed, PR-opened, and merged are different observations.
Do not reset/clean other work, kill unowned processes, or allocate new worktrees
to resolve uncertainty.

Classify the assignment by the brief, not by guessing from symptoms:

| Assignment | Permitted result |
| --- | --- |
| Rebase/conflicts | Resolve this PR against the named current base; update the same PR. |
| CI never started | Perform the specifically requested CI action, often an empty commit; change no product code. |
| Prepare revert | Revert the exact named commit and open the specified revert PR. |
| Repair after revert | Start the explicitly requested new branch from current default, restore the change as directed, fix the regression, and open a new PR. |
| Review a resolution | Use the independent review method instead; do not resolve it yourself. |

## Resolve conflicts semantically

Understand each side's intended behavior and shared interfaces before choosing
conflict hunks. Inspect consumers, invariants, schema/data compatibility,
generated files, and dependency state as relevant. Preserve the original change
and the newly merged base behavior; textual conflict removal is not sufficient.
Follow the project's generation commands for generated artifacts, preserving
already-shipped migration behavior.

Use the brief's permitted fetch/rebase operations in this assigned writer
worktree. Make only changes needed for the resolution. Check the resulting
diff and relevant range-diff. Run focused checks for both sides' interactions
and the required project checks. Refresh evidence for changed bytes and base.
Do not claim the old head's passing tests or approval prove the new head.

If correct resolution requires a consequential new product decision or goes
beyond the assignment, record the specific block and permitted alternatives.
In unattended mode, use `factory_record_decision` for material choices; flag
protected areas, conflicting/missing vision, or irreversible external effects
with `needsHuman: true`. Do not rewrite policy or waive a gate.

## Preserve recovery intent

For missing CI, perform only the instructed kick; do not edit workflow files,
weaken checks, or keep pushing empty commits until something changes. Return
the result and let the factory observe CI.

For a revert, use the exact commit and requested scope. Resolve conflicts
conservatively, check restored behavior, and record evidence honestly in
`## Test results`. Do not replace the revert with a speculative broader fix
or merge the revert yourself.

For a post-revert repair, inspect the actual failed checks and causal
interaction before restoring the change. Preserve a regression check where
practical. A new PR is appropriate only because the brief authorizes it.

## Return the native result

Run commands non-interactively and wait for started checks in the same turn.
Use `create_pull_request` to update the same PR or open the specifically
requested new/revert PR. Attach refreshed output with `attach_evidence` when
the brief requires it or affected checks were rerun. For ordinary integration,
include UI evidence when required by its brief and gates. A factory-designated
exact revert uses its special CI/test-evidence contract: do not add screenshot,
new-feature, or independent-review requirements that the revert brief omits.
Read the result, then call `finish` with the native outcome and accurate
summary/tests/changed files.

If blocked, use the native blocked outcome with the exact missing fact or
capability and preserved work. Do not report success based on a requested
operation alone. Leave review freshness, CI observation, merge ordering, and
resource cleanup to CodeDen.
