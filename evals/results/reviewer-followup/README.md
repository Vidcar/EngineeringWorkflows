# Reviewer follow-up evidence

Start with the [follow-up report](../../../docs/REVIEW_FOLLOWUP.md) for the changes,
results and limits. This bundle records the two revised-instruction transitions,
a successful pre-clarification baseline and an incomplete measurement attempt.
The [original adaptation evidence](../pstack-2.3.0/README.md) remains separate.

## Contents and decisions

| File | Contents and decision |
| --- | --- |
| [manifest.json](manifest.json) | Frozen 52-file pack identity, exact evaluator versions, controls, independent review findings, CI definition and scoped decisions. |
| [baseline-review-to-fix.json](baseline-review-to-fix.json) | Accepted pre-clarification baseline on the original PR instructions and evaluator v2. This shows that the earlier wording could already succeed; it is not a run of the clarification. |
| [review-to-fix.json](review-to-fix.json) | Accepted two-turn trial of the revised instructions, checked with its preserved v3 evaluator. Clean review checkpoint; four passing tests, three original-defect failures and independent contract checks after the fix. |
| [measurement-incomplete-v3.json](measurement-incomplete-v3.json) | Incomplete first-turn-only attempt before fixture corrections. No second prompt was sent. The inaccurate account-count description and original identities are retained; this attempt is not accepted. |
| [measure-to-improve.json](measure-to-improve.json) | Accepted fresh two-turn trial on the corrected v4 fixture: Measure-only baseline, explicit Workflows transition, useful optimization, preserved frozen inputs, eight independent cases per implementation, four authored tests and an independent benchmark replay. |
| [evaluator-v3.json](evaluator-v3.json) | Exact historical Python sources and README for already-prepared v3 trials; this is not the current supported evaluator. |
| [local-controls.json](local-controls.json) | Original validator/57-pack-test/23-control output and the separate corrected 23-control run, with source identities and stdout/stderr. |

The `manual_acceptance` fields are the lead's scoped decisions. Original helper
reports retain `needs_review`: objective checks alone cannot establish that an
agent used the right guidance, respected scope throughout or made a useful
optimization. The incomplete attempt retains `incomplete_fixture_corrected`.

## Identity and provenance

The revised skill-content manifest digest is
`1ff13510b6d19bef82b48f18ee27a0b6d4c7598a7adfb7bcc1c9331bedcde9c3`.
It is SHA-256 of the UTF-8 encoding of
`json.dumps(files, sort_keys=True, separators=(',', ':'))`, where `files` maps
each skill-relative path to its SHA-256. All 52 delivered skill files were
checked against it. Documentation, evaluator source, evidence and CI have
separate identities.

Each trial retains its original parsed `run` and `checkpoint`, plus exact
UTF-8 metadata files and hashes. `workspace_files` contains the final submitted
files as `{sha256, content}`. `check_files` preserves independent reports and
logs. The measurement trial also contains `independent_replay` logs and a
supplementary schema check. `runner_report` labels selected reported guidance
reads and before/after observations; these are distinct from independently
captured replay output. No complete tool transcript is bundled.

Two fixture defects were discovered after the first 23-control run: the workload
populated 56 accounts rather than 160, and checks could accept cross-call output
buffer reuse. The corrected control run and fresh measurement trial use v4.
The existing review trial uses unchanged billing inputs/checks from preserved
v3. No prepared run's hashes were edited to make a changed fixture scoreable.

A later source review found no regression in the optimized candidate and a
nonblocking validation limit: equality checks can accept mapping wrappers rather
than dictionaries. The candidate constructs dictionary literals; independent
parent checks confirmed its exact output types and keys. This limit is retained
in the measurement review and is a reason the evaluator requires manual review.

## Reproduction

The artifact format matches the original bundle's
[materialization example](../pstack-2.3.0/README.md#artifact-format-and-reproduction).
Use a **new directory outside the checkout**, verify each record's content hash,
and keep new outputs separate from historical evidence. For example, materialize
`measure-to-improve.json`, then run from that new directory:

```sh
python -B -m unittest -v test_candidate
python -B benchmark.py
```

The archived optimized implementation should preserve the contract. Timing
ratios will vary by host. To inspect the original correct baseline, its exact
candidate bytes match the archived `reference.py`; do any baseline replay in a
separate copy. The recorded before/after runner measurements used the same frozen
workload/harness, six alternating pairs and equal completed output.

For the review trial, materialize `review-to-fix.json` and run:

```sh
python -B -m unittest discover -s tests -v
```

Its archived countercheck logs show how the retained tests fail on the original
bug. The original fixture source and helper hashes remain available in v2's
pinned PR commit or the historical v3 snapshot, as recorded in the manifest.
Absolute paths in logs identify the original execution workspace; they are not
promised to exist on a different host.

For new behavioral trials use the [evaluation guide](../../README.md) and a fresh
workspace/conversation. Do not supply these result bundles, evaluator criteria
or preferred answers to the runner. CI runs structural and helper controls;
[the current PR checks](https://github.com/Vidcar/EngineeringWorkflows/pull/2/checks)
are the hosted execution record. CI does not run these AI-agent conversations.

The evidence supports these bounded transitions and their fixture contracts on
one host. It does not establish an aggregate effectiveness rate or a universal
performance gain. Fresh conversations shared a filesystem with instruction
boundaries, and checkpoints cannot reveal transient reverted edits.
