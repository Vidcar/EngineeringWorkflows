---
name: engineering-check
description: Assess a change, design, issue, or readiness and report evidence-backed findings. Use for review, triage, adversarial scrutiny, or a bounded independent view; execution and verification assets belong to engineering-verify.
---

# Engineering Check

Own a judgment, findings, or readiness request; keep the target read-only unless the user authorizes changes. For a mixed request whose final outcome requires implementation, use engineering-workflows as owner once and provide bounded review. An existing owner never changes. A support assignment inherits its owner, scope, authorized effects, review depth, and budget; return findings without restarting a lifecycle.

Resolve `engineering-workflows` by exact name in the active catalog and read its `references/contract.md` once per task. Reading is not invocation. If unavailable, continue safe useful review and report the precise limitation; do not expand authority or claim missing evidence.

Identify the requested decision, acceptance criteria, actual comparison base, changed and relevant untracked files, and environment. Examine the concrete artifact and callers, failure paths, compatibility, and maintainability. Distinguish inherited failures from regressions, and hypotheses from reproduced defects. Use a clean independent lens where appropriate, following the shared contract; a bounded reviewer does not redelegate unless its assignment explicitly permits it.

Gather discriminating evidence, using engineering-verify or engineering-measure as bounded support when needed. Standalone review does not authorize fixes, publication, or deployment. Report actionable findings with location, trigger, consequence, and supporting evidence; state uncertainty, remaining risk, and checks not run. A no-findings result is limited to the inspected scope. Resolve material disagreement using source evidence or a safe probe, not votes.

For design or adversarial review, read [critical-review.md](references/critical-review.md).
