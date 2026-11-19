---
name: codeden-measure
description: "Measure a quantitative performance, resource, reliability, or model-quality claim within an assigned CodeDen factory task. Use only when a numeric comparison matters to a decision. Preserve the current role and output contract; do not launch a benchmark campaign or alter factory budgets."
---

# Make a defensible measurement

Treat measurement as bounded support for the current assignment. Keep its
permissions, workspace, native report, budget, and endpoint. Do not start
agents, change provider settings, spend outside the assigned budget, or create
a new scheduling loop. If measurements require unavailable resources, report
that limit rather than inventing results.

## Freeze the comparison

Before collecting results, state the decision, metric and unit, success
threshold, representative workload, correctness oracle, baseline and candidate
revisions, environment, and resource/time limit. Define what observation would
change the decision. Avoid metrics selected after seeing favorable results.

Use the same meaningful inputs, configuration, dependencies, hardware/resource
allocation, concurrency, and relevant operating conditions for both variants.
Explain unavoidable differences. Include startup versus steady-state behavior,
cache/warmup effects, and measurement overhead when they matter.

## Measure behavior before speed

Check correctness before ranking performance. A faster candidate that loses
data, returns the wrong result, or violates the required behavior is not a
winner. Preserve correctness/error observations and failed runs alongside
timings. Do not quietly omit unfavorable samples or change assertions to make
a benchmark complete.

Choose bounded warmup, repetitions, and representative cases appropriate to
noise and cost. Record sample counts and variability, not just one best run.
Distinguish directly observed values, derived calculations, estimates, and
hypotheses. Prefer a cheap discriminating experiment to a broad benchmark
without a decision consequence.

For model or agent evaluation, keep prompts, tools, data access, time/token
allowances, and scoring comparable. Hold evaluation answers out of candidate
context. Separate task performance from grader agreement. Disclose reused
context, model identity uncertainty, small samples, and subjective judgments.

For competing designs, fix the rubric before evaluating candidates. Use
independently supplied candidates and a nonauthor judge if the factory has
assigned them. Otherwise label the comparison as a single-agent analysis;
do not claim independence or start an Arena. Verify a chosen synthesis as a
new artifact rather than inheriting the candidates' passing results.

## Return a bounded claim

Report baseline/candidate identities, conditions and workload, metric/unit,
sample size, result and variability, correctness/failures, and limitations.
State whether the evidence meets the predefined threshold and what decision
it supports. Avoid broad claims from a microbenchmark or small evaluation.

Keep raw results in the task's permitted evidence location, with enough detail
to reproduce the calculation. Use the current stage's native output fields:
a builder's PR/test results and evidence attachment, an investigator's analysis,
an area reviewer's finding, or an independent review verdict. Do not invent a
`factory_submit_benchmark` tool or claim the factory automatically gates on
your metric.

If the target, workload, or relevant environment changes, refresh the affected
measurement before making a final claim. Stop when the decision is supported
or the budget/limitation is reached; do not change factory limits to finish.
