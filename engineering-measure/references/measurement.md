# Measurement details

For performance, separate uninstrumented comparison from profiling, which can add overhead. Confirm successful work and resource use before interpreting latency or throughput; inspect saturation and the load generator. Choose a workload and concurrency that match the decision, record hardware, runtime, versions, tuning and dataset, and include variance or uncertainty rather than a single best run. A profile can suggest a cause but does not alone establish a speedup.

For model or agent evaluation, freeze task inputs, acceptance criteria and scoring before comparing; apply equivalent resources and tool access. Inspect completed outputs, errors and incomplete attempts, not just aggregate scores or agreement. Isolate candidate work, prevent leakage between attempts, and report actual exposed identities and missing data without guessing. Avoid treating a prompt, judge agreement, or a structural validator as proof of task success.
