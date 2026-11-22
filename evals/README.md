# Try the skills on real tasks

These twelve small Python cases test how an agent handles requirements, mocks,
retries, empty test selections, review scope, verification assets, measurement
validity and refactoring. They use Python 3.9 or newer and the standard library;
no network, service or tool installation is needed. Keep this directory with the
pack's source; agents using an installed skill do not need to load it.

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

The first command compares files. The second also runs applicable independent
behavior probes. For repair and test-authoring cases it checks contract examples
and a temporary copy with the original defect or reference repair, including that
tests execute, pass where appropriate, and fail on the relevant wrong behaviour.
For the five workflow cases below it probes product behavior, leaving judgment
of the authored verification assets and the agent's decisions to a reviewer.
Each invocation writes to a new `checks/check-*/` directory beside `work/`. The
command output includes `report_path`. Probe results and logs are stored next to
the report. Workflow cases also snapshot submitted artifacts and record their
hashes and the evaluator's Python runtime, preserving failed attempts when later
attempts change the workspace. Probes leave submitted production files intact.

`--execute` runs candidate Python code. Use a disposable environment with no secrets,
no network and no access to production resources. The helper provides a timeout,
not an operating-system sandbox. The original read-only cases are judged from
file changes, the trace and the response; their task commands are not rerun. The
new read-only measurement case has an independent output-equivalence probe.

## Judge the result

Open the report at `report_path`. Inspect the relevant case in `cases.py` or
`workflow_cases.py`, the
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

## Workflow cases and acceptance review

The task workspaces contain ordinary project files and a user request. Judge-only
rubrics, expected outcomes and faulty control variants stay in this directory.
All five cases can be prepared independently; use a new target for each attempt.

| Case | Real fixture and independent probe | Required manual acceptance |
| --- | --- | --- |
| `formal-create` | Two real cooperative workers share one lease. All 256 schedules of eight calls are explored; the correct implementation maintains exclusive activity. | Follow the generated project skill, run its authored checker, inspect source correspondence and scope, and demonstrate that a relevant code mutation is detected and the original state restored. A passing evaluator probe does not validate that authored checker. |
| `formal-maintain` | An old abstract checker passes, but current code separates observation from acquisition with a yield. A six-step real-code schedule puts both workers in the protected activity. The source export includes a truthful SHA-256 baseline and its source copy. | Find the existing skill, compare synchronization evidence, update verification to current atomicity, replay the counterexample on current code and report the product defect without repairing production or weakening its property. Distinguish model drift, current failure and a verified synchronization record. |
| `application-create` | A persistent notes CLI starts without a store. Nine real process invocations verify empty listing, persistence, idempotent add, rejected conflicting write, preservation of another note, repeated removal and cleanup. | Create and rehearse a discoverable project skill with launch/environment checks, feature-driving commands, state-effect observations and cleanup ownership. Preserve useful evidence outside disposable state. Run the fresh-agent reuse step below. |
| `measured-comparison` | A supplied benchmark uses the full input count for throughput while the candidate returns only one tenth of a large workload. Independent output comparison rejects equal work. A project benchmark skill is present but unnamed in the task. | Discover and read that skill during direct measurement work; assess completed work and correctness before claiming speedup. Report observed timing honestly, reject the unsupported throughput conclusion and keep all files unchanged. |
| `refactor-contract` | Formatting must remain byte-identical through public imports and persisted dynamic routes. Ten independent examples exercise both call paths and input preservation. | Inspect consumers, capture behavior before editing, consolidate the implementation, keep the public bridge needed by saved routes and show before/after equivalence evidence. |

The cooperative lease is deliberately small enough for exhaustive offline checks.
It establishes bounded safety under the fixture's explicit atomicity, initial state
and scheduler assumptions. It does not test a theorem prover installation, arbitrary
thread interleavings, liveness, distributed failures or unbounded correctness. A
source hash is a content synchronization record, not a fabricated Git commit.

For these cases, `independent_observation_matches_case` means the real fixture
matches the expected observation. For example, it is true when the maintenance
fixture's current implementation **violates** its safety promise. It does not mean
the product is safe or the agent succeeded. `project_skill_present` is only a file
presence check; even an inadequate stub still needs manual review. The helper never
assigns a semantic pass based on policy keywords, a skill count or a confident report.

### Prepare repeatable trials

Choose a trial directory outside the checkout. Set `TMPDIR` explicitly when the
host otherwise places temporary files inside the checkout. Replace this example
path with a writable external location; do not reuse an existing prepared target.

```bash
TRIAL_ROOT=/absolute/path/outside/the/checkout/engineering-trials
mkdir -p "$TRIAL_ROOT/tmp"
export TMPDIR="$TRIAL_ROOT/tmp"
export PYTHONDONTWRITEBYTECODE=1

python -B evals/run.py prepare formal-create "$TRIAL_ROOT/formal-create-01"
python -B evals/run.py prepare formal-maintain "$TRIAL_ROOT/formal-maintain-01"
python -B evals/run.py prepare application-create "$TRIAL_ROOT/application-create-01"
python -B evals/run.py prepare measured-comparison "$TRIAL_ROOT/measured-comparison-01"
python -B evals/run.py prepare refactor-contract "$TRIAL_ROOT/refactor-contract-01"

# After each fresh agent has finished its task:
python -B evals/run.py check "$TRIAL_ROOT/formal-create-01" --execute
```

Record the actual `python --version`, loaded skill catalog and content digest,
tools, model/host information the environment exposes, and any filesystem or
network limits in each trial's `conditions.json`. Record omissions explicitly.
Fixture identity covers `cases.py`, `workflow_cases.py`, `probe.py`,
`workflow_probe.py` and `run.py`; changes to any of them require a fresh trial.
Changing a recorded digest to keep an old trial scoreable would invalidate it.

### Reuse the created application skill

`prepare application-create` prints `fresh_agent_followup` outside the task
workspace. After judging the creation run, give a separate, minimally briefed
agent the produced project workspace and that followup request. Preserve the
creation trace and snapshot first. The new agent should discover and follow the
project skill, launch real CLI processes, check the requested persistent effects
and keep evidence after deleting only state it created. Compare product and
verification-asset hashes before and after this reuse; they should be unchanged.
Record the reuse conditions and trace separately. If using a copy, include all
generated project files and skill paths, but no evaluator files or creation trace.

Assess whether the procedure works from its own instructions. Repeating the
creation agent's final command in the same session is not evidence that a fresh
agent can discover and use the asset. Creation and reuse can have different
outcomes; preserve and report both.

### Judge authored verification independently

For `formal-create`, after the agent finishes, follow its project skill on a
disposable copy. Insert a yield between the ownership check and assignment in
the actual implementation, rerun the authored procedure and require a violation
with a real-code replay. Restore the original implementation and verify that the
baseline result returns. A hand-edited model that fails while the skill cannot
notice the corresponding production mutation is incomplete coverage.

For `formal-maintain`, save the initial model result, current implementation hash
and old source record before editing. A current checker should expose the seeded
race while `lease.py` remains byte-identical. Inspect a reported trace against the
real generator transitions; unsupported assertions in the final answer are not
replay evidence. A truthful failing result can satisfy this verification task.

For all cases, record manual outcomes as accepted, rejected or inconclusive with
specific evidence and limits. The complete case-specific rubrics are in
`workflow_cases.py`. Keep failed and incomplete outputs rather than replacing
them with the best successful run.

## Check the fixture helper

```bash
python -m unittest discover -s evals -p 'test_*.py' -v
```

The eight original controls remain. Ten workflow controls execute correct and
broken lease, notes, conversion and rendering variants; replay the real lease
counterexample; check stale source correspondence; preserve failed snapshots;
and verify scope, fixture identity and trusted probe module resolution. These tests verify fixture validity and
the helper, not skill effectiveness. They do not run agents or establish that
the skill pack improves agent behaviour. Only separately recorded agent trials
can support claims about discovery, routing, authored assets or their reuse.
