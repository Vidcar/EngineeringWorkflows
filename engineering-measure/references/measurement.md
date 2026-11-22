# Measurement details

## Performance

State the decision and the result that would change it before measuring. Inspect
the script's timing boundaries, counts and omissions. Ensure lazy work is consumed,
asynchronous work is awaited, and required writes or responses complete inside the
measured interval. Count errors, timeouts, retries and successful work separately;
fast rejected requests are not improved successful throughput. Inspect correctness,
not just the existence of output.

Choose workloads and concurrency that match the decision. Record relevant
hardware, runtime, versions, tuning and data. Use comparable production-relevant
builds and settings, or state that the result compares configurations. Confirm
that the load generator can sustain the intended load. Preserve the baseline
before tuning and define what one sample contains.

Choose repetitions and warmup for the decision. Interleave or randomize comparison
order when drift could favour one side. Include variation or uncertainty; one best
run is insufficient. Label a requested single-run estimate as exploratory. A gap
smaller than the observed uncertainty does not establish a winner; another run
needs a specific uncertainty to resolve and sufficient budget.

Compare normal runs separately from profiling, which can add overhead. Use a
profile or counters to investigate the resource or code path limiting the result.
Compare claimed savings with the changed portion's original cost, and throughput
with relevant capacity. Investigate impossible-looking results for skipped work,
caching, errors or inconsistent units before reporting them. Pair a microbenchmark
with its contribution to the actual user path when the decision concerns that path.

A measured difference and its cause are separate claims. Report unexplained
results honestly; a plausible profile does not replace the comparison and a
repeatable comparison does not by itself identify the cause.

For a requested improvement, give the implementation lead a bottleneck hypothesis
and a checkable expected effect. Change one causal factor when practical, preserve
correctness and rerun the same valid workload. Keep or revert the task-owned change
based on the result and relevant regressions. Freeze the harness during a comparison;
if it must change, rerun both sides. Stop when the requested target is supported or
the next experiment cannot resolve a worthwhile uncertainty within the budget.
Measurement-only assignments return findings rather than starting implementation.

## Models and agents

Fix the task inputs, acceptance criteria and scoring before comparing candidates.
Freeze baseline and candidate instructions with their dependent references. Use
equivalent resources and tool access. Identify the actual loaded catalog, exposed
model identities and fixture versions. Keep attempts isolated and expected answers
out of runner context and accessible runner files.

Inspect completed outputs, errors and incomplete attempts as well as aggregate
scores. Preserve failures and explain missing data. Score observed behaviour and
effects; a proposed plan, judge agreement or structural validator does not show
that the task succeeded. Keep per-case outcomes beside aggregate results so a
success cannot hide a required missing case. Report the conditions needed to
interpret or repeat the comparison, including unavailable tools or untested hosts.
