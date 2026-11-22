---
name: engineering-measure
description: Design or assess benchmarks, performance comparisons and quantitative engineering or model evaluations. Use for measured results. When the request also includes improving software, engineering-workflows owns the change and Measure supplies measurements.
---

# Measure the result

Own measurement-only requests. When a new request includes implementation or
improvement, Workflows owns the result. For an existing assignment, keep the lead,
question, scope, review requirements and budget. Return measurements and limits
without calling other engineering skills.

Resolve `engineering-workflows` by exact catalog name and read its
`references/contract.md` once per task. Reading it does not call that skill. Report
missing guidance and continue useful measurement within the agreed scope.
Measurement adds no permission for production effects or spending.

1. Define the decision, metrics, units, workload, correctness criteria, baseline,
   candidate and environment before running comparisons. Read
   [measurement.md](references/measurement.md) for performance or agent evaluation.
2. Confirm the actual revisions and configuration. Inspect what the measurement
   includes. Check that intended work completes inside the measured interval,
   outputs are correct, and errors are counted. Check that the load generator
   can supply the intended load.
3. Compare under equivalent, realistic conditions. Choose appropriate warmup,
   repetitions and representative inputs. Control or disclose caching, contention
   and changes between runs. Isolate mutable resources and inspect what a claimed
   dry run actually does.
4. Check surprising results against plausible resource and end-to-end limits.
   Keep failures and invalid runs visible. Explain exclusions. Report observations
   or useful summaries, sample size, variability, conditions and material limits.

Separate measured results from explanations of their cause. Limit speedup or
winner claims to the workloads and conditions actually measured. Return enough
evidence for the lead or user to assess the comparison.
