# Methods for the task at hand

## Investigate or plan

Trace callers, state and constraints. Separate observations from inferences and
hypotheses. Check primary sources for uncertain external facts. For historical
questions, distinguish evidence found, a search that found nothing and history
you could not access. Code shows behaviour, not necessarily why it was chosen.
Use a small probe to resolve the assumption most likely to change the decision.
Keep prototypes separate and state their limits.

Propose an approach with acceptance examples, key interfaces, dependency order
and verification. Record consequential accepted decisions in the project's
existing documentation. A planning-only task ends with the plan; a request that
includes implementation continues under the same lead.

## Shape interfaces and state

For a consequential interface or state change, trace consumers and invariants
before choosing types, signatures and module boundaries. Give mutable state one
owner. Derive related shapes from the authoritative schema instead of maintaining
parallel definitions. Represent valid states explicitly when that removes
contradictory flags or repeated assumptions. Use validated construction or runtime
checks for constraints the language's types cannot express.

Parse untrusted data at real trust boundaries. Keep transport concerns out of
domain interfaces where practical, and preserve internal checks justified by the
failure model. Use the project's conventions and dependencies. Avoid speculative
types, abstraction layers or blanket bans on guards and casts.

When competing shapes have consequential tradeoffs, give Arena the same caller
examples, constraints and decision criteria. Use a small experiment for an
empirical uncertainty; leave unresolved product preferences with the user.

For commands, jobs or migrations that can retry or stop halfway, derive the next
action from actual state. Check repeated execution and material interruption
points, including duplicated external effects and stale resources. Isolate
independent writers; give necessarily shared state a clear owner and enforced
synchronisation. A written instruction alone does not coordinate concurrent writes.

## Diagnose and repair

Get evidence of the reported defect: a failing test, real invocation, trace or
small reproduction. A setup failure does not reproduce the defect. When the cause
is unclear, compare explanations and change one relevant variable at a time.
If reproduction is unavailable, explain the limit on your diagnosis.

Read available report evidence and check relevant existing issues, active owners
and concrete proposed fixes before creating competing work. Similar symptoms are
not enough to declare a duplicate. When asked to verify an existing PR or commit,
assess that artifact first against the relevant baseline and patched behavior in
comparable environments. Report confirmed, insufficient or inconclusive evidence;
do not silently replace an assessment with a new repair.

Before interpreting logs, traces or profiles, identify the running revision,
process, configuration and relevant data. Correlate the actual request or operation
with the evidence. A nearby log or a matching source line does not establish that
the suspected path ran. Add focused instrumentation when competing explanations
would otherwise look the same, then rerun the discriminating case.

Fix the responsible code, keep a useful regression check when practical, and
rerun the original scenario as well as any smaller reproduction. For intermittent
failures, retain seeds, timing and sample counts. When repeated fixes depend on
the same assumption, test that assumption before trying another fix. Remove
temporary instrumentation when finished.

Decide whether the failing state is legitimate and needs handling, or whether an
earlier operation created an invalid state. Fix that cause. Check sibling paths
within scope; return unrelated repairs to the lead instead of widening the task.

## Refactor or migrate

State the problem being solved and behaviour to preserve. Read consumers before
changing an interface. Capture useful current behaviour before restructuring,
and distinguish intentional preservation from a defect the user wants repaired.
Keep related decisions together and complete the local improvement without
speculative abstractions.

Trace contracts beyond symbol references: saved data, serialized fields, other
languages, versioned dependencies and lifecycle ordering. Ask Check a focused
impact question when a consequential assumption needs independent scrutiny.
Where compatibility requires it, add the new path, migrate supported consumers
and then remove the old path, with a clear completion condition. If coupled changes
cannot pass independently, isolate them and verify the combined transition.

For repeated or error-prone transformations, prove a representative unit before
automating it. Prefer a small bounded tool that is safe to rerun and verifies its
result. Keep legitimate variations visible; do not spread an unverified pattern.

Before preserving a visual design, capture the original rendering and use Verify's
visual method. Use Measure for quantitative performance claims. Check a new
guardrail through the project's real check path: a valid case must pass and a
representative violation must fail.
