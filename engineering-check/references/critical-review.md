# Review independently

Identify the exact artifact and relevant context. Give a fresh reviewer the
requirements, constraints and known evidence without steering them toward the
author's conclusion.

Focus on risks relevant to the work: missing requirements, unsupported
assumptions, failure and recovery, interfaces, migration, security, concurrency,
accessibility and maintenance. Review a plan as a plan; a predicted failure is
different from an observed runtime defect.

## Follow the change's effects

Trace more than direct callers. Check affected wire formats, serialized fields,
saved data, other languages, flags, teardown ordering and consumers several steps
away. For library behaviour that matters to safety, inspect the pinned version
and local patches rather than assuming the latest documentation applies.

Identify the one or two assumptions that clear the most consequential risks.
Follow a failure through the actual code and use a small executable probe when it
can distinguish the competing explanations. Verify can supply that bounded check
within the assignment's allowed effects. Record supported risks, cleared risks
and unresolved assumptions with locations and evidence; do not invent likelihood
numbers or callers.

Read rationale before removing an unusual workaround, comment or suppression.
It may encode a supported compatibility or ordering constraint. Challenge the
constraint with evidence; replacing it with enforcement can be useful, but the
review alone does not authorize that edit.

## Judge the evidence

Inspect assertions and their independent requirement basis. Ask whether a
plausible wrong implementation would pass or a harmless internal refactor would
fail. Preserve useful characterization and interaction tests. For application
procedures or formal checks, read the corresponding Verify reference before
judging coverage, implementation correspondence and reuse.

Confirm what actually ran on the reviewed content and environment. Distinguish
sampled cases, bounded exploration and proof, and a model violation from a bug
reproduced in the application. A static or design finding can remain useful when
execution is unavailable; state the evidence and the unresolved step instead of
presenting it as an observed failure.

## Resolve and report

Keep supported findings even when other reviewers disagree. Resolve material
disagreements with the code, an independent example or a safe check that
distinguishes the competing explanations. Explain accepted tradeoffs. Refresh
affected review and evidence when the artifact changes.

Describe the independence actually achieved. A fresh reviewer can use the same
model family; agreement or model reputation does not establish correctness.
Report missing required review coverage instead of implying it happened.
