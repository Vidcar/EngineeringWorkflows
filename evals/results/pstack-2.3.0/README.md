# Pstack adaptation evidence

Start with the [evaluation report](../../../docs/EVALUATION.md) for interpretation
and the [component review](../../../docs/PSTACK_REVIEW.md) for recommendations.
These files retain the evaluated artifacts and evidence as data; they do not
register additional active skills or replace manual acceptance review.

## Contents

| File | Contents |
| --- | --- |
| [manifest.json](manifest.json) | Pinned baseline/upstream, the 52-file candidate identity, both evaluator versions, conditions, test counts, independent review findings and trial decisions. |
| [pstack-inventory.json](pstack-inventory.json) | All 553 upstream paths and Git blob identities, including 58 top-level and three embedded skill instructions. |
| [formal-create.json](formal-create.json) | Submitted skill, real-code checker, mutation/recovery evidence, preserved v1 evaluator report and separate fixed-v2 product observation. |
| [formal-maintain.json](formal-maintain.json) | Stale baseline, updated correspondence, current failing property, real replay, authored assets and independent parent reruns. |
| [formal-reuse.json](formal-reuse.json) | Fresh project-only discovery/reuse, real-code mutation, exact restoration and protected-file checks. |
| [application-create.json](application-create.json) | Generated skill/helper, feature map, eleven-step evidence, rejected persistence mutant and independent product probe. |
| [application-reuse.json](application-reuse.json) | Fresh project-only discovery/reuse, eleven real CLI steps, retained effects evidence and preservation/cleanup checks. |
| [measured-comparison.json](measured-comparison.json) | Read-only submission, independently observed missing output and the runner's rejection of the misleading timing result. |
| [refactor-contract.json](refactor-contract.json) | Shared serializer/public bridge, unchanged saved routes and independent compatibility probe. |
| [check-discovery.json](check-discovery.json) | Read-only review variant, project-skill discovery report, real-code counterexample and eight-file preservation check. |
| [minimal.json](minimal.json) | Small variable rename without extra machinery. |
| [evaluator-v1.json](evaluator-v1.json) | Exact historical evaluator snapshot for the already-started creation trial; the fixed version is in `evals/`. |

The JSON `acceptance` fields are the lead reviewer's decisions, with provenance
and scope. Standard helper reports retain `needs_review`: objective product
checks do not establish authored-check quality or agent success. The workflow
trial may be accepted while its product property fails, as in formal maintenance.

## Artifact format and reproduction

Each trial's `workspace_files` maps a relative path to its UTF-8 `content` and
SHA-256. These are the submitted bytes, including retained command evidence.
The standard-case `reports` contain independently executed probes, file-change
checks and captured artifact hashes. Parent reruns are separate `parent_checks`.
Some runner conclusions and guidance-read observations come from its final
report; they are labeled accordingly. Complete tool transcripts are not bundled.

Absolute paths in command logs and old report metadata identify the original
execution workspace; those paths are historical, not promised to exist on
another host. Materialize a trial into a **new disposable directory outside the
checkout**, inspect its project instructions and use the documented relative
commands. For example, from the repository root:

```sh
python3 -B - evals/results/pstack-2.3.0/formal-create.json /tmp/lease-review-copy <<'PY'
from pathlib import Path
import hashlib
import json
import sys

bundle = json.loads(Path(sys.argv[1]).read_text())
destination = Path(sys.argv[2]).resolve()
destination.mkdir(parents=True, exist_ok=False)
for name, record in bundle['workspace_files'].items():
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Invalid artifact path: ' + name)
    data = record['content'].encode('utf-8')
    if hashlib.sha256(data).hexdigest() != record['sha256']:
        raise ValueError('Artifact hash mismatch: ' + name)
    path = destination / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
print(destination)
PY
```

Review the materialized scripts before running them. Run commands in a restricted
disposable environment; the fixture helper is not a hostile-code sandbox. Keep
new outputs separate from the archived evidence. For example, the formal checker
accepts a new `--output` path, and the application helper's default `run` allocates
a new evidence directory. Do not rewrite original identities to make a changed
fixture scoreable. A formal maintenance primary check is expected to exit 1
because it exposes the preserved product bug; inspect the recorded result rather
than equating every nonzero exit with evaluation failure.

The v1 creation trial is not relabeled as v2. Its five original evaluator hashes
remain in `prepared_fixture_record`, and `evaluator-v1.json` retains matching
source. The fixed-v2 independent observation and fresh procedure reuse supply
additional evidence without changing that history. Only the fixed evaluator
source is part of the supported evaluation helper.

For new agents, prepare fresh task workspaces with [the evaluation guide](../../README.md).
Do not supply these result bundles, evaluator expectations or preferred answers
to a trial runner. The evidence supports these nine scoped trials on one host,
not an aggregate model-improvement claim or execution of all pstack integrations.
