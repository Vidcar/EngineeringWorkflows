# Try the skills on real tasks

These seven small Python cases test how an agent handles requirements, mocks,
retries, empty test selections, review scope and a later request to fix a finding.
They use the standard library. Keep this directory with the pack's source; agents
using an installed skill do not need to load it.

## Run a case

```bash
python evals/run.py list
python evals/run.py prepare mock-regression /tmp/engineering-trial-01
```

Give a fresh agent **only** the resulting `work/` directory, its `TASK.md` request,
and the candidate skill catalog. Mount only that workspace when the host allows it.
Keep `cases.py`, this guide, `run.json` and evaluator expectations out of the runner's
context and filesystem. A path convention alone does not enforce that isolation.
Use the same ordinary task request for baseline and candidate runs.

Save the agent's response and tool trace beside `work/`. Also record the pack
revision or content digest, actual loaded catalog, host, exposed model identity,
tool access and any limits in `conditions.json`. The helper records fixture hashes.
It refuses to score a run if the fixture or evaluator files have since changed;
prepare a fresh run rather than updating its recorded hashes. Preserve failed and
incomplete attempts.

After the agent finishes:

```bash
python evals/run.py check /tmp/engineering-trial-01
python evals/run.py check /tmp/engineering-trial-01 --execute
```

The first command compares files. The second also runs the repair or test-authoring
probes: independent contract examples and a temporary copy with the original defect
or reference repair. It checks that tests execute, pass where appropriate, and fail
on the relevant wrong behaviour. It leaves the submitted workspace's production
code intact. Each invocation writes to a new `checks/check-*/` directory beside
`work/`. The command output includes `report_path`. Any probe results and logs for
that check are stored next to its report, so rechecking preserves earlier evidence.

`--execute` runs candidate Python code. Use a disposable environment with no secrets,
no network and no access to production resources. The helper provides a timeout,
not an operating-system sandbox. Read-only cases are judged from file changes,
the trace and the response; the helper does not rerun their task commands.

## Judge the result

Open the report at `report_path`. Inspect the relevant case in `cases.py`, the
actual changes and the agent's trace. A report of `needs_review` means objective
checks passed or were not applicable. Confirm that the agent executed the checks
it claims, used the right expectations, stayed within scope and reported limits.
Do not score policy keywords, skill counts or a confident final answer.

The review case includes both an unjustified field removal and a requested name
change. Credit a reviewer for distinguishing them. For the empty-selection case,
zero discovered tests provide no passing evidence; additional correctly selected
checks are useful if reported accurately. Its local runner deliberately returns
zero when the selection is empty, so the case works across Python versions.

For `review-to-fix`, finish and save the first turn before running:

```bash
python evals/run.py checkpoint /tmp/engineering-trial-01
```

This records the first-turn file changes and prints the second user request.
Send that request to the same conversation, then check the final result. File
snapshots cannot detect a temporary edit that was reverted; use the trace too.

Compare baseline and candidate under equivalent conditions. Run affected cases
after instruction changes and add a case when a real failure reveals a gap.
Repeat a trial to resolve a specific uncertainty; do not discard unsuccessful runs.

## Check the fixture helper

```bash
python -m unittest discover -s evals -p 'test_*.py' -v
```

These tests use known good and bad artifacts to check preparation and scoring.
They do not run agents or establish that the skill pack improves agent behaviour.
