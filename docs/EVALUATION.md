# Evaluation of the pstack adaptations

This record covers the initial PR candidate at
[`8b34e17e18a4c87b523e64338b10539415b71a34`](https://github.com/Vidcar/EngineeringWorkflows/commit/8b34e17e18a4c87b523e64338b10539415b71a34).
The [review follow-up](REVIEW_FOLLOWUP.md) records the later clarification,
updated candidate identity, two-turn trials and CI. Earlier trials and evaluator
identities below remain historical evidence; they are not relabeled as runs of
the changed instructions.

## Decision and scope

The candidate is suitable for a review PR. Keep the seven entrypoint skills and
add the targeted routing, application verification, formal verification,
measurement, impact-analysis and delivery improvements described in
[PSTACK_REVIEW.md](PSTACK_REVIEW.md). This evaluation supports the exercised
behaviors below; it does not establish a general improvement rate across models
or projects.

The source baseline is Engineering Workflows 2.2.0 at
[`6277fe359e25fd37e8c734a4627b3260d5245c78`](https://github.com/Vidcar/EngineeringWorkflows/tree/6277fe359e25fd37e8c734a4627b3260d5245c78).
The upstream comparison is pstack 0.15.46 at
[`7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9`](https://github.com/cursor/plugins/tree/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack).
The delivered candidate declares version 2.3.0.

The [evidence bundle](../evals/results/pstack-2.3.0/README.md) records exact
candidate and evaluator identities, submitted workspaces, independently executed
probe reports and selected command evidence. It includes unsuccessful controls
and the evaluator revision issue described below. Generated project skills are
stored as data in JSON, so the evidence does not add active skills to the pack.

## Conditions and evidence boundaries

Evaluation used CPython **3.12.14** on Linux x86_64. The fixtures and helpers use
the standard library. No external theorem prover, browser, service, account or
network dependency was needed by the task fixtures. Python 3.9 compatibility is
an implementation target, not a separately executed environment in this review.

The initial 52 candidate skill files were frozen before the behavioral trials. Their
sorted content-hash manifest has digest
`efab50e5047156e2a31ab7235b600afcd7dd85416fe3df28c86397890154af52`.
The skill files at that revision were compared with that manifest. Documentation and
evaluation evidence are outside this skill-content digest; the evaluator has its
own recorded file hashes.

Each task runner began in a fresh agent conversation with its ordinary `TASK.md`,
project files and the frozen candidate pack. Reuse agents received only the
produced project and its own instructions, without the pack, creation report or
creation transcript. No preferred finding or evaluator rubric was supplied to
the task runners. The model was inherited from the parent session without an
override; a separately verifiable provider/model revision was not exposed.

The workers shared a host filesystem. They were instructed not to inspect
sibling trials or evaluator materials; this was **not operating-system-enforced
isolation**. The evidence contains final artifacts, retained command outputs,
runner reports of guidance reads, and parent-executed checks. It is not a complete
export of every agent tool call. Discovery observations should be read with that
provenance limit. No baseline-versus-candidate agent experiment or statistical
effectiveness estimate is claimed.

## Structural and executable controls

| Check | Baseline | Candidate | What the result establishes |
| --- | --- | --- | --- |
| Pack validator | Pass: 2.2.0 | Pass: 2.3.0 | Seven unique skills, required files, metadata, policies, references and 17 declared automatic edges are structurally valid. |
| Pack/helper unit tests | 55 passed | **57 passed** | Existing resolver/snapshot/pack controls remain; missing phase routing and missing verification lifecycle guides are rejected. |
| Evaluation-helper controls | 8 passed | **18 passed** | The original eight controls remain, with ten new positive/negative workflow and evaluator-integrity controls. |
| Candidate identity | Frozen source baseline | 52 files match the trial manifest | The instructions under review are the ones used in the trials. |
| Diff and documentation checks | — | No whitespace errors; relative links and component inventory checked | Review artifacts connect to existing files and cover the inventoried semantic components. |

The first baseline pack-test run had 54 passes and one environment error:
`test_non_repository_fails` received a temporary directory inside the checkout
because this host set its default temporary location there. Repeating with an
explicit task-owned `TMPDIR` outside the checkout produced 55/55 passes. No test
expectation or implementation was weakened. Candidate tests used the same
explicit external temporary root.

The new evaluator controls reject a real lease race, recognize a stale abstract
model, detect missing persistence and duplicate notes, reject unequal conversion
work, preserve dynamic saved routes, keep failed artifacts, enforce read-only
scope, reject changed evaluator identities and prevent candidate-module
shadowing of the trusted probe. These are controls of the fixtures and helper.
They do not themselves demonstrate skill effectiveness.

Commands from the repository root:

```sh
python3 -B engineering-workflows/scripts/validate_pack.py --root .
python3 -B -m unittest discover -s engineering-workflows/scripts -p 'test_*.py' -v
python3 -B -m unittest discover -s evals -p 'test_*.py' -v
git diff --check
```

Set `TMPDIR` to a writable directory outside the checkout and
`PYTHONDONTWRITEBYTECODE=1` when reproducing on this host. The
[evaluation guide](../evals/README.md) explains fixture preparation, identity
checks and independent acceptance review.

## Behavioral trials

The standard helper intentionally returns `needs_review` for these workflow
cases. A passing product probe, a file named `SKILL.md`, or a confident final
answer cannot validate an authored verification procedure. Acceptance below
combines the submitted artifacts, runner reports, independent product probes,
inspection of the authored procedures and the specific replays described here.

| Trial | Observed result | Acceptance and boundary |
| --- | --- | --- |
| Small mechanical edit | Renamed one local accumulator, performed four direct behavior checks, and added no machinery or extra files. Parent independently checked the exact edit and results. | Accepted: proportional workflow for the deliberately small request. |
| Formal verification creation | Created a project skill and a checker that executes the real cooperative Python generators over all 256 schedules of eight selections. Original source passed; a real-code yield mutation produced 48 violating schedules. | Accepted for the stated finite scope; independent reuse is recorded separately. |
| Formal verification maintenance | Discovered the existing skill and old source record. The old model passed; the updated model and actual implementation both produced 48 unsafe schedules, with zero trace mismatches. Production and contract bytes were preserved. | Accepted: current correspondence and a real product failure are reported separately. |
| Application skill creation | Created a discoverable skill, feature map and helper. Eleven real CLI steps checked persistence, repetition, conflicting writes, removal and cleanup. A response-without-persistence mutation failed at the first add. | Accepted: the authored helper observes effects and preserves evidence; reuse is separate. |
| Application skill reuse | A fresh agent found `AGENTS.md`, followed its project-skill link, read the procedure and ran its commands. All eleven CLI steps passed. Six source/procedure files were unchanged; owned state was removed and evidence retained. | Accepted: the generated procedure worked without its creator's context or the engineering pack. |
| Direct measured comparison | Discovered the unnamed project benchmark skill. Rejected an apparent 9.195× throughput result because the candidate returned only 200 of 2,000 required outputs. All files remained unchanged. | Accepted: correctness and completed work governed the conclusion. Timings are illustrative, not a performance ranking. |
| Refactor with persisted contracts | Moved common serialization into `reports.py` while retaining public handler wrappers and saved route strings. The runner reported identical before/after output digests across 32 renders. Parent inspection and a separate ten-example probe passed. | Accepted: public imports, dynamic consumers, exact output bytes and input preservation were checked. |
| Direct review discovery | Found the existing formal project skill during a direct Check request. Ran the stale model, identified changed atomicity and reproduced a six-step failure against actual code using in-memory rebinding. All eight project files remained unchanged. | Accepted: relevant guidance was discovered and review-only scope was preserved. |
| Formal procedure reuse | A fresh agent discovered the generated skill from the specification's project location, read the actual checker and source, and ran both documented commands. Baseline passed all 256 schedules; the real-code mutation failed in 48 schedules and exact restoration passed. | Accepted: the procedure ran without prior evidence, its creation report or the engineering pack. |

### Formal creation: real code, finite claim and fault sensitivity

The fixture supplies two cooperative workers, one initially unowned lease and
exactly eight scheduler selections. The promise is at most one active worker.
The authored checker does not substitute a copied transition model: it compiles
and executes the identified implementation bytes, explores all 256 schedules,
makes 2,048 `next` calls and observes 2,304 states including initial states.
Selections of completed generators are explicitly exercised as no-ops.

The original implementation completed with zero violations and zero execution
errors. The rehearsal inserted a yield between the ownership guard and
assignment in an isolated copy of the real code. It detected 48 unsafe schedules;
the first witness was `ABAABBAA`, with both workers active after step six. Import
errors, missing witnesses and incomplete exploration do not count as sensitivity
success. The rehearsal accepted valid controls, restored exact original bytes,
reran both isolated and production baselines, and removed only owned scratch.

The documented scope excludes unbounded safety, arbitrary worker counts,
preemptive threads, fairness, liveness, clocks and distributed failures. The
source export had no meaningful Git history, so it recorded actual file hashes
and did not invent a commit. The generated procedure warns that later writers or
changed yield boundaries require renewed correspondence and observation review.

A separate fresh agent then discovered and ran that procedure from a source
export containing no prior evidence or creation report. It inspected the source
mapping, obtained the same completed baseline and real-code counterexample, and
confirmed all four valid/restoration controls. Parent inspection confirmed the
five supplied product/procedure files were unchanged and the owned scratch
directory was absent. The worker additionally checked its original task file.

### Formal maintenance: synchronize without hiding the bug

The supplied source had acquired a yield between its guard and assignment, but
the previous abstract model still represented acquisition as atomic. The worker
preserved the initial passing checker output and source synchronization record,
then updated the model and executed it alongside the real implementation.

Both sides completed all 256 schedules and 2,048 post-call observations. Each
reported 48 unsafe schedules, and their traces matched. Direct replay of
`A B A A B B` reached `active == {A, B}`. Parent execution of the authored checker
independently returned the expected safety-failure exit code, and a separate
product probe reproduced the real interleaving.

The maintenance rehearsal accepted the valid historical control, detected the
broken real source, rejected the stale model, accepted restored controls and
preserved the original failing production baseline. The parent reran that
rehearsal with separate output, checked cleanup and confirmed the protected
source/contract hashes. The updated synchronization record says the model is
current and the product property fails. That is successful verification
maintenance, not a product safety pass or authorization to repair production.

### Application creation and reuse: observe persisted effects

The project skill runs a read-only doctor before allocating a fresh owned store.
The actual CLI must list a missing store without creating it, add a note, expose
it to a different process, accept an identical retry without duplication, reject
a conflicting ID without changing bytes, remove one note while preserving
another, and tolerate repeated removal. Evidence contains exact arguments,
stdout, stderr and persisted JSON, outside the disposable state directory.

The creator also changed `save` to return without persisting in an isolated
project copy. The unchanged helper rejected the successful response because the
store was missing. Failing evidence survived cleanup. The independent product
probe used nine real processes and passed its separate contract checks.

A fresh reuse workspace contained only the application, specification, generated
instructions and helper. Its agent discovered the project pointer and reran the
documented doctor and all eleven steps. The parent independently compared all
six protected hashes, inspected the acceptance summary and confirmed that the
exact owned state directory no longer existed. This exercises a CLI; it does
not establish browser/desktop control or automatic host-catalog registration.

### Measurement and refactoring: preserve the actual contract

The benchmark trial's supplied timer credited every input row while discarding
conversion outputs. The candidate returned one tenth of a large input. The
worker found the project-specific instructions during a direct Measure request,
checked complete output and inputs, and refused to call unequal work an
improvement. The parent's independent probe confirmed the discrepancy on five
input sizes, and the evaluator confirmed that no files changed.

The direct Check trial used a read-only variant of the maintenance fixture. It
found the project skill, contrasted the old model's 256-schedule pass with a
real-code failure, and reproduced the interleaving without editing files by
rebinding the checker's implementation globals in memory. The parent compared
all eight project-file hashes with the pre-trial snapshot and independently
reproduced the failure. This variant is recorded as a separate manual trial,
not a standard maintenance-case completion.

The refactor trial retained the compatibility wrappers needed by persisted
dynamic route strings. Inspection confirmed a single shared serializer rather
than duplicate implementations. A separate parent-run probe exercised both
public imports and persisted dispatch on ten examples with exact JSON and
immutability assertions. The worker's reported broader before/after inline
probe is additional evidence; its full tool transcript is not archived here.

## Review findings and corrections

An independent instruction review found a material routing omission: direct
Check and Measure requests could bypass the project-skill discovery rule when
they never entered Workflows or Verify. The rule was moved into the shared
contract so it applies to every entrypoint, including direct specialists. The
reviewer reread that change and the measurement-loop clarification and found
the omission resolved. The frozen candidate and direct specialist trials include
that correction.

The evaluation helper also had a concrete import-order defect during preparation:
it added the candidate workspace to `sys.path` before loading `workflow_probe`.
A candidate file with that name could shadow the trusted evaluator module. The
helper now imports its trusted probe before adding the task path, with a
dedicated negative control. This closes that particular accidental shadowing
route; it does not turn execution of arbitrary Python into a security sandbox.

One formal-creation runner had already started against evaluator v1. Its recorded
hashes were preserved. An exact five-file v1 evaluator snapshot was reconstructed
and verified against that run's original identities; it was used to retain that
run's report. The submitted workspace contained no `workflow_probe.py`. A
separate fixed-v2 product probe also passed on the same submitted source.
Unstarted v1 workspaces were retained separately and freshly prepared with v2.
The formal reuse trial is a separate manual followup, not a relabeled v2
creation trial. All published evaluator source is the fixed version.

Creation workers could not spawn their own reviewers because the session's
concurrency slots were occupied. They reported that limitation. The parent
subsequently inspected the generated procedures, replayed maintenance, and
arranged independent application and formal reuse. No self-rehearsal is described
as an independent review.

A second independent reviewer inspected the evaluation helper, new cases,
probes, controls and README claims against the baseline and ran all 18 controls.
It reported no material findings. This review covered evaluator code and claims,
not hostile-code containment, trial transcripts or general skill effectiveness.

## Coverage that remains unexercised

The complete component disposition map is an instruction/architecture assessment,
not execution of every pstack tool. This review did not exercise TLC, Apalache,
Lean, another installed prover, a production distributed system, browser or
desktop verification, Windows registration, external queues or Slack, persistent
automation, remote merge/release, or pstack's runtime integrations.

Application-maintenance instructions, visual comparisons, multi-PR delivery
pagination, active issue-owner coordination, and optional statechart presentation
were inspected but did not receive their own end-to-end agent fixtures here.
The trials are deliberately small, one-off examples on one host. They establish
concrete behavior on those tasks and expose important failure controls. They do
not prove that every task will route correctly or that the pack improves aggregate
agent success, latency or cost.

The PR is the requested review artifact. Installing these changes in the user's
active skill catalog, merging the PR and releasing to other hosts are separate
endpoints that this review does not perform.
