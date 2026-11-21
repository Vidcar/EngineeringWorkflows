# Measurement details

## Performance

Compare normal runs separately from profiling, which can add overhead. Confirm
successful work and resource use before interpreting latency or throughput.
Inspect saturation and whether the load generator is limiting the result.

Choose workloads and concurrency that match the decision. Record relevant
hardware, runtime, versions, tuning and data. Include variation or uncertainty;
one best run is insufficient. A profile can suggest a cause, but a speedup needs
a measured comparison.

## Models and agents

Fix the task inputs, acceptance criteria and scoring before comparing candidates.
Use equivalent resources and tool access. Identify the actual loaded instructions,
catalog and exposed model identities. Keep attempts isolated and expected answers
out of runner context.

Inspect completed outputs, errors and incomplete attempts as well as aggregate
scores. Preserve failures and explain missing data. Score observed behaviour and
effects; a proposed plan, judge agreement or structural validator does not show
that the task succeeded. Report the conditions needed to interpret or repeat the
comparison.
