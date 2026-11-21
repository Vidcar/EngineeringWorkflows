# Review independently

Identify the exact artifact and relevant context. Give a fresh reviewer the
requirements, constraints and known evidence without steering them toward the
author's conclusion.

Focus on risks relevant to the work: missing requirements, unsupported
assumptions, failure and recovery, interfaces, migration, security, concurrency,
accessibility and maintenance. Review a plan as a plan; a predicted failure is
different from an observed runtime defect.

Keep supported findings even when other reviewers disagree. Resolve material
disagreements with the code, an independent example or a safe check that
distinguishes the competing explanations. Explain accepted tradeoffs. Refresh
affected review and evidence when the artifact changes.

Describe the independence actually achieved. A fresh reviewer can use the same
model family; agreement or model reputation does not establish correctness.
Report missing required review coverage instead of implying it happened.
