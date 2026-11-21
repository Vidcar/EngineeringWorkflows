---
name: engineering-check
description: Review a change, design, issue or readiness claim and report supported findings. Use for triage, design review or an independent assessment. Running checks and maintaining test assets belong to engineering-verify.
---

# Review the change

Resolve `engineering-workflows` by exact catalog name and read its
`references/contract.md` once per task. If it is unavailable, report the gap and
continue useful review within the agreed scope.

Keep a review-only target unchanged. Workflows leads requests that also require
implementation. Keep the same accountable lead when the user changes the
requested outcome, following the shared contract. A supporting reviewer stays
within the assignment and does not delegate further unless allowed.

1. Establish the decision to be made, acceptance conditions, comparison base,
   actual changed and relevant untracked files, and environment.
2. Inspect the change and its callers. Consider relevant failure paths,
   compatibility and maintenance costs. Separate inherited failures from
   regressions, and suspected defects from reproduced ones.
3. Review material changes to tests, snapshots, fixtures, mocks, generators,
   selected checks and gates against the requirements. Distinguish a justified
   expectation update from reduced coverage or an expected result changed to
   match a defect. For test quality, resolve `engineering-verify` by exact name
   and read `references/testing.md`; reading it does not transfer ownership.
4. Gather evidence that can settle material questions. Use Verify or Measure for
   a specific check when needed. Respect the assignment's allowed effects;
   review alone does not authorise fixes, publication or deployment.
5. Report actionable findings with the location, trigger, consequence and
   evidence. State uncertainty, checks not run and remaining risk. A review with
   no findings applies only to the inspected scope. Settle disagreements with
   evidence or an explained tradeoff.

For design or adversarial review, read
[critical-review.md](references/critical-review.md).
