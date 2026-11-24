# Create and maintain formal verification

Use formal methods for consequential invariants, difficult event ordering or a
proof request. Routine changes need no proof or new skill. Keep the owner and scope.

## Select the claim and method

Start with the named area or inspect where a broken promise would harm users and
ordinary tests provide weak evidence. Prefer a valuable property over an easy one.
Derive it from requirements or an independent contract, not current output. State
the property and the harm of violating it in plain language.

| Question | Method to consider |
| --- | --- |
| Can a bad sequence or interleaving occur? | A small transition model and model checker; TLA+ is one suitable option. |
| Does implementation code preserve a property across inputs? | A verifier supporting the actual language and relevant semantics. |
| Must the property hold beyond any explored finite bound? | A proof with the required assumptions and obligations. |
| Is a suitable verifier unavailable? | Generated-input checks of real code; read [testing](testing.md) and [generated-input methods](methods.md#generated-input-checks), and state the fallback and unmet proof request explicitly. |

Prefer existing tooling and a reproducible, practical runtime. Explain the choice.
A hand-written duplicate of a function does not verify the implementation.

## Connect the check to the code

Map each property, model action and important assumption to concrete source paths
and functions. Inspect all relevant writers and failure paths. A model's atomic
step must match actual atomicity: examine transactions, locks, awaits and separate
reads/writes. Check important assumptions at the implementation boundary and name
behaviour the abstraction omits.

State input domains, bounds, environmental assumptions and fairness assumptions
where relevant. Confirm valid starting states and useful cases exist, filters do
not remove difficult cases, and the property can distinguish valid from invalid
behaviour. A law that repeats its premise is insufficient. Verify that the intended
obligations are selected, registered and complete. Keep errors, timeouts, skipped
obligations and incomplete exploration separate from a pass.

## Establish sensitivity and reuse

For each property claimed as verified, demonstrate that it rejects a representative
broken implementation variant in an isolated copy. Check the intended failure,
not an import or setup error. For an abstract model, follow the correspondence
procedure against the changed code before rerunning; changing only the model does
not demonstrate detection of a real-code regression. Preserve valid controls and
existing findings. Never weaken a property, domain or model to manufacture success.

For durable verification, prefer the project's existing runbook and verification
commands. Create or update a discoverable project `SKILL.md` when requested or
when it materially improves discovery, following the host's supported authoring
process and repository conventions. Keep instructions usable by the next agent
and identify the area and change triggers. Include, directly or through an
existing coverage record:

- Each property, purpose, source paths/functions, model mapping, assumptions and
  bounds; include relevant shared-state writers rather than only file names.
- Actual setup and rerun commands, reproducible tool version, runtime budget,
  output interpretation, evidence location and owned-resource cleanup.
- The commit where correspondence was confirmed and the identity of checked dirty
  or new content, using content hashes or an equivalent snapshot. A commit alone
  cannot identify uncommitted code. Keep this record per check where coverage differs.
- How to recognize a relevant change, inspect correspondence, interpret a failure
  and update verification for an authorised requirement change. Leave no placeholders.

Rehearse those instructions as a cold reader on a scratch change that breaks the
property in real code. A fresh agent, when useful, receives the instructions and
task without the expected answer. The procedure must detect the break.
Restore the exact original code and confirm the baseline result returns, including
any known failures. Preserve evidence and clean temporary resources. If the
rehearsal misses the defect or cannot run, repair the procedure or report it as an
unvalidated draft; do not substitute an easier defect to obtain a pass.

## Keep correspondence current

Run existing checks first and record the baseline; an old model's pass is not
evidence about new code. Compare the recorded revision with current dirty content,
following moved/split functions and new writers to protected state. If the record
is missing, reconstruct a provisional baseline from history and state uncertainty.

Classify changes as irrelevant to the check, model/harness drift, an intended
contract change, or a possible product bug. Update from source semantics. Change
a property only with evidence of changed intent, preserving the old/new meaning
and rationale. Explain any changed bounds or assumptions.

Rerun, refresh sensitivity for affected properties and replay counterexamples
against the implementation where possible. An impossible step indicates a model
error; unavailable replay limits the production-bug claim. Explain realizable
failures as steps in the code's terms. Preserve genuine bugs and return product
fixes outside the assignment to the lead.

Record correspondence separately from the result: current or updated verification
can expose a failing property. Advance its synchronization record only after
confirming the actual covered content and completing the relevant checks. Never
advance a blocked check's record. Refresh commands and coverage, then follow the
updated project instructions once to confirm they remain usable.

## Report the evidence

Report each property's method, checked content, result, assumptions, bounds,
counterexample or sensitivity evidence, rerun command and exclusions. Distinguish
sampled testing, exhaustive exploration within a stated finite scope and proof.
Optionally use an available statechart skill for TLA+; otherwise retain checker output
and explain paths plainly. Charts are projections; unshown or unchecked rules are not passes.
