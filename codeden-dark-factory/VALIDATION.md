# Validation record

Validated on **19 November 2026** against the source revisions in
[pack.json](pack.json). This record distinguishes structural checks, executed
local tests, instruction review, and offline agent trials. No live CodeDen
instance or provider session was started.

## Executed structural and installation checks

| Check | Result | What it establishes |
| --- | --- | --- |
| Skill creator's quick validator, seven folders | 7 passed | Required metadata and naming are well formed. |
| `python3 -B scripts/validate.py` | Passed | Pack metadata, seven skill names, simple frontmatter, UI metadata, license preservation, and provider routing are consistent. |
| Actual distribution installation smoke | Passed | Both native layouts receive real directories and byte-identical complete files; existing project instructions survive; rerunning changes nothing. |
| `python3 -B scripts/test_install.py` | 15 tests passed | Installer behavior under normal use and meaningful conflict/failure cases. |
| Independent source/implementation review | Complete; findings corrected and rechecked | Native-stage boundaries and specific recovery exceptions were compared with pinned CodeDen code. |

The installer regression suite checks:

1. Complete real copies for both providers and preservation of existing instructions.
2. Default dry-run behavior with no target mutations.
3. Refusal of a Codex install shadowed by root `AGENTS.override.md`.
4. A second-provider collision causing no partial installation.
5. Destination symlink escape refusal.
6. Refusal when target state changes after preview.
7. Preservation/refusal of edited installed skill content.
8. Preservation/refusal of edited managed routing content.
9. Invalid or unowned routing markers.
10. Manifest paths outside provider roots.
11. Idempotence including manifest and file modification times.
12. Explicit handling of removed source files without deleting installed work.
13. Source skill symlink refusal.
14. Upgrading unmodified files while preserving an unselected provider and outside prose.
15. Rollback after a simulated I/O failure.

These checks use disposable directories and do not change user projects, global
provider settings, GitHub state, or CodeDen settings. The installer is designed
for a quiescent instruction tree; it does not claim a transaction against a
hostile concurrent filesystem writer or a process/machine crash.

## Fresh offline agent task trials

Each trial used a fresh agent context, the relevant skill, and a task-local raw
artifact. The agent did not receive the intended answer or the prior source
analysis. Native CodeDen MCP tools were deliberately absent; an accurate
capability limitation was part of the observed result.

### Investigation: reproduce without implementing early

Task: reproduce an order coupon being applied more than once across line items.
The public API was `cart.total(items, coupon_percent=0)`; the issue specified
that 1,000 + 2,000 pennies with a 10% order coupon must produce 2,700 pennies.

Observed:

- A regression test called the public function and failed with `2400 != 2700`.
- The agent ran control cases: no coupon produced 3,000; a single 3,000-penny
  line with the coupon produced 2,700.
- The production file's before/after hash matched.
- The agent preserved the failing test and evidence, reported the missing
  `factory_report_reproduction` capability, and did not claim a native
  transition or proceed to implement a fix.

This supports the investigation boundary, independent expected value, meaningful
failure signal, and truthful unavailable-tool handling. It does not test the
actual server's reproduction endpoint.

### Independent review: reject an authorization defect despite green CI

Task: review an invoice lookup against two criteria: an owner can read their
invoice, and a viewer cannot read another account's invoice. The supplied green
current-head CI ran a single owner-success test.

Observed:

- The included test passed.
- A direct in-memory probe exercised the candidate function and showed Alice
  reading Bob's invoice and Bob reading Alice's.
- The agent recommended `request_changes` with `blockers: "pr"`, marked the
  isolation criterion false, marked vision alignment false, identified
  inadequate tests, and listed the blocking security concern.
- It separated green CI's narrow coverage from the untested isolation claim.
- It did not edit target files or claim a recorded native verdict.
- It used the source hash to identify the snapshot and disclosed absent
  head/base identifiers instead of inventing them.

The observed candidate file SHA-256 was
`b705e4447f4ee2d6d1c4d15bc005a003aceeb2968deced019b69d4f017a45955`.

This supports read-only review, criterion coverage, independent behavioral
evidence, and consistency of the proposed verdict. It does not demonstrate
model behavior in every review or harden CodeDen's merge checks.

### Measurement: reject a faster incorrect candidate

Task: assess supplied export benchmark records. Required behavior aggregates
all invoice lines by account; the acceptance threshold requires preserved output
and at least 20% faster operation. Both variants had three recorded measurements.

Observed:

| Property | Baseline | Candidate |
| --- | --- | --- |
| Recorded durations, milliseconds | 12.2, 11.8, 12.1 | 6.0, 6.2, 6.1 |
| Mean recorded duration | 12.033 | 6.100 |
| Correct outputs | 3 of 3 | 0 of 3 |
| Alice total, pennies | 1,500 | 300 |

The agent rejected replacement. It described the 49.3% lower mean duration
without treating it as an acceptable speedup, because outputs were wrong.
It disclosed the small sample and missing environment/timing details, treated
overwrite behavior as a hypothesis rather than a proven implementation cause,
and required fresh evidence after correction. It ran no additional workload.

This supports correctness-first measurement and scope-accurate claims. The
numbers belong to the offline trial fixture; they are not performance results
for CodeDen or this skill pack.

## Independent findings and corrections

The source reviewer identified three concrete compatibility details:

- Ordinary offline PR reviews prohibit fetch, but a specific later-commit
  recheck may explicitly permit fetching a missing new head. Review now
  permits exactly that bounded exception.
- Exact factory reverts use a special CI/test evidence contract. Integrate
  no longer imposes ordinary feature screenshots or independent review on
  that path.
- `factory_submit_review` can return `recorded: false` for distinct reasons.
  Review now distinguishes input rejection, environment reassessment,
  replacement/end instructions, and a recorded verdict; it forbids retries
  merely to force `recorded: true`.

A narrow independent recheck confirmed all three corrections. No material
installer defect was identified in that review. The broader instruction review
did not establish a guarantee that an agent will follow every rule.

## Limits and first live use

The following were **not** performed:

- A live CodeDen run or real factory MCP submission.
- Actual Codex/Claude skill-body invocation inside a user's installed provider.
- Installation into any user's project, or changes to personal/global skills.
- Project CI, automatic merging, deployment, or a full factory stop/restart drill.
- A statistical evaluation of model reliability or comparative token/cost savings.

Before unattended use, install into a small project and observe native skill
discovery, actual body reads, stage reporting, PR evidence, and independent
review with automatic merging off. Recheck provider settings, overriding
instructions, CI, audit commands, budgets, and the selected CodeDen version.
The [README](README.md) describes setup; the [analysis](ANALYSIS.md) explains
which controls are enforced by CodeDen and which remain agent judgment.
