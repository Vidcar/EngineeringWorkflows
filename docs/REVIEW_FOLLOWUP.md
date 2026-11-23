# Reviewer follow-up: outcome changes and CI

This follow-up builds on PR #2's initial candidate at
[`8b34e17e18a4c87b523e64338b10539415b71a34`](https://github.com/Vidcar/EngineeringWorkflows/commit/8b34e17e18a4c87b523e64338b10539415b71a34).
It addresses the review-to-fix ownership ambiguity and the smaller description,
routing, fallback-reference and CI comments. The seven skill roles and 17
automatic support edges remain unchanged.

## Changes and rationale

| Comment | Change |
| --- | --- |
| Review/verification/measurement becomes implementation | The [shared contract](../engineering-workflows/references/contract.md#when-the-user-changes-the-outcome) now distinguishes the accountable agent from its active owning skill. An explicit user request for production changes selects Workflows, reads its entrypoint and applicable references, and preserves prior findings. Helpers continue to return beyond-scope requests to their existing lead. |
| Specialist restrictions conflict with that transition | Check, Verify and Measure point to the shared rule. Measure's retention/no-call restriction now explicitly applies when supporting another lead. User-directed reselection is distinct from an automatic helper call, so no reverse graph edge is added. |
| Check's impact-analysis description can obscure ownership | Check's description explicitly owns review-only assessments and supports Workflows when implementation is included. Standalone impact assessment remains a useful Check capability. |
| Missing feature-build route | [Routing](../engineering-workflows/references/routing.md) now includes implementing a new feature or extending behavior, with applicable Verify/project guidance and acceptance/preservation evidence. |
| Formal fallback lacks testing pointers | The [fallback row](../engineering-verify/references/formal.md) links to testing and generated-input methods while preserving the unmet-proof limitation. |
| No automated PR checks | [Validate](../.github/workflows/validate.yml) runs the pack validator and both unit/control suites on push and pull-request events. |

Independent instruction/CI review found no remaining material issue in these
changes. The reviewer checked top-level versus delegated scope, reference
resolution, graph consistency and the workflow's actual repository commands.
That source review was separate from the agent trials and hosted execution.

## Candidate and evaluator identities

The revised 52-file skill pack was frozen before the follow-up agent trials.
Its content-manifest digest is
`1ff13510b6d19bef82b48f18ee27a0b6d4c7598a7adfb7bcc1c9331bedcde9c3`.
The [follow-up evidence](../evals/results/reviewer-followup/README.md) records the
digest encoding, file hashes, evaluator versions, checkpoints, submitted
artifacts, independent observations and acceptance decisions.

The initial nine pstack-adaptation trials remain in [EVALUATION.md](EVALUATION.md)
and their original bundle. They are not relabeled as executions of the revised
instructions. A pre-clarification review-to-fix trial, run while assessing the
reviewer's comment, also succeeded and is retained as baseline evidence. This
follow-up improves an explicit instruction boundary; it does not claim to have
converted a demonstrated agent failure into success.

## Two-turn trials

Each runner started in a fresh conversation with the ordinary first task,
project files and revised pack. The evaluator's rubric and second user request
were excluded from that initial task workspace. The lead recorded a first-turn
checkpoint before sending the explicit second request to the same conversation.
The measurement fixture was corrected during independent review; its earlier
incomplete attempt is preserved separately below.

### Review to fix — accepted

The first request asked for a read-only invoice-total review. The agent found
the unconditional extra unit, ran the existing failing test and additional
contract examples, and made no file changes at the checkpoint. It initially
tried a nonexistent Check-local contract path, then read the correct shared
contract; that recovered read error is retained in the evidence summary.

The second user request authorized a local fix and retained regression test.
The same agent selected Workflows and reported loading routing, methods,
coordination and delivery guidance. It removed the extra unit and retained or
added checks for positive amounts, empty invoices, credits and input preservation.

Independent execution confirmed:

- Only `billing.py` and `tests/test_billing.py` changed.
- The task and specification were preserved; the first-turn checkpoint was clean.
- All four tests ran and passed, with zero skips.
- The same tests failed three times against the original defective implementation.
- A separate contract probe passed against the submitted repair.

The review trial retains its original evaluator-v3 identity. The later corrections
affected only the separate aggregation fixture and probe; the review task,
billing probe and helper were unchanged. It was checked with the preserved exact
v3 evaluator, not by rewriting its recorded hashes.

### Measure to improvement — accepted

The first request asked for measurements and output checks without file changes.
The fresh agent selected Measure, found the project measurement skill and ran the
supplied benchmark. It reported equal correct work and the unchanged candidate's
timings without claiming an improvement. The first-turn checkpoint was clean.

After the second request authorized an implementation improvement, the same agent
selected Workflows and reported reading its entrypoint, routing, methods,
coordination and delivery references, plus Verify's testing guidance. It retained
the original baseline and project measurement contract. Only `candidate.py` and
a new `test_candidate.py` changed.

The implementation replaces a full row scan per requested account with one row
pass and private accumulators, then emits fresh dictionaries in request order.
Repeated and missing requests, zero and negative deltas, Unicode names, large
integers, input preservation and fresh results across changed-input calls remain
covered. The tradeoff is temporary storage proportional to distinct requested
accounts; the change does not introduce a cross-call cache.

| Observation | Result |
| --- | --- |
| Runner's baseline candidate median | 23.5672 ms/call; candidate and reference had identical source |
| Runner's changed candidate median | 0.6227 ms/call |
| Runner's changed paired reference/candidate ratio | Median 34.13×; range 32.58–34.75× |
| Independent replay of the submitted candidate | Four authored tests passed; median 0.6395 ms/call; paired ratio median 34.00×, range 32.38–36.71× |
| Separate contract probe | Eight cases passed for each implementation, including preservation and freshness |

Both runner measurements and the independent replay used the unchanged workload
of 6,000 rows, 160 populated accounts and 173 requested summaries. The harness
warms each implementation once, alternates six pairs of two calls per
implementation, and checks every completed output outside the timed interval.
Every run completed 12 timed calls and 2,076 summaries per implementation; no
failed, incomplete or excluded timing sample was reported. The frozen reference,
workload, harness, task, specification and project skill hashes were preserved.

The contemporaneous paired ratios are the relevant comparison: the reference
also varied between processes, so a raw before/after ratio alone would overstate
precision. These observations establish a useful optimization on this fixture,
not a production-wide speedup. Memory, concurrency, tail latency and other data
distributions were not benchmarked. Independent source review and the parent
acceptance decision are recorded in the bundle; raw independent replay output is
retained separately from runner-reported before/after measurements.

The final source reviewer found no regression in the submitted implementation
and one nonblocking validation limit: equality-based benchmark checks can accept
mapping wrappers instead of dictionaries. The submitted implementation visibly
constructs dictionary literals, and a supplementary parent check confirmed exact
list/dictionary types and keys on three cases. This coverage limit is recorded;
the frozen fixture was not silently changed after the trial, and its objective
report still requires manual contract review.

## Fixture review found and fixed two defects

Independent review of the new aggregation case found two concrete issues that
the first 23-control run did not expose:

1. The initial deterministic generator populated only 56 accounts while the
   project instructions described 160. The corrected generator covers all 160;
   the benchmark reports actual populated cardinality and a control checks the
   complete expected account set.
2. A defective implementation could reuse its output list/dictionaries between
   calls and still pass the original checks. Both the benchmark and independent
   probe now check cross-call dictionary identity and preservation of previously
   returned values, including after changed-input calls. The reviewer's exact
   reusable-buffer implementation is retained as a negative control.

The reviewer reproduced the corrections: the final workload has 6,000 rows,
160 populated accounts and 173 requests; the valid implementations still pass;
the original defective buffer now fails both check paths for the intended reason.
No other material findings remained in that bounded review.

One measurement runner had completed its read-only first turn before these
findings arrived. Its files were unchanged, but it repeated the incorrect
160-account description. That attempt is **incomplete and not accepted as
transition evidence**. Its original workspace, checkpoint and evaluator-v3
identity are preserved. No second request was sent to that conversation.
A new workspace and fresh agent ran the corrected final fixture. No prepared
trial hash was rewritten and no failed/incomplete attempt was discarded.

## Automated checks and CI

| Check | Observed local result |
| --- | --- |
| Pack validator | Pass: seven skills, 17 automatic edges, no errors |
| Pack and helper tests | **57 passed** |
| Evaluation-helper controls | **23 passed** on the corrected evaluator |
| Evaluation cases | 13 available, including the new genuine two-turn `measure-to-improve` case |

The five added controls cover the aggregation workload and paired counts,
valid/defective implementations, the first-turn checkpoint, allowed second-turn
changes and frozen inputs. They impose no speed threshold and leave process,
routing and performance acceptance to manual review. The correct unchanged
implementation can pass the correctness probe without completing the optimization
task; the guide explicitly requires judging that distinction.

Local execution used CPython 3.12.14 and PyYAML 6.0.3 on Linux x86_64, with an
explicit external `TMPDIR`. An initial CI-author run encountered the previously
documented host fallback into the checkout; the external temporary directory
resolved it without changing tests. The final workflow applies `${{ runner.temp }}`
at the two unittest steps, where that context is available.

The workflow uses Python 3.12, a ten-minute job timeout, `contents: read` and
checkout with credential persistence disabled. The action commits were verified
against official release tags:

- [actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1): `3d3c42e5aac5ba805825da76410c181273ba90b1`.
- [actions/setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0): `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`.

The three commands are the validator, `unittest discover` in
`engineering-workflows/scripts`, and `unittest discover` in `evals`. Packaged
logs are local execution evidence. Use [PR #2's current checks](https://github.com/Vidcar/EngineeringWorkflows/pull/2/checks)
for the hosted result associated with the delivered revision. CI runs these
automated controls; it does not execute fresh AI-agent trials.

## Interpretation and limits

These are scoped observations on one host with inherited model settings and no
model override. Task conversations were fresh, but filesystem isolation was by
instruction rather than an operating-system boundary. The bundle contains
submitted artifacts, selected retained outputs, runner reports of guidance reads
and independent checks; it does not contain a complete export of every tool call.
Checkpoints cannot detect a transient edit reverted before the checkpoint.

The evidence supports the two requested transitions and the stated fixture
contracts. It does not establish an aggregate success-rate, cost or latency
improvement for the skill pack, nor universal application performance. The PR
updates repository source and evidence; installation, merge and deployment remain
separate endpoints.
