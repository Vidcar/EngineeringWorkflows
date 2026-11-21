# Methods for the task at hand

## Investigate or plan

Trace callers, state and constraints. Separate observations from inferences and
hypotheses. Check primary sources for uncertain external facts. For historical
questions, distinguish evidence found, a search that found nothing and history
you could not access. Use a small probe to resolve the assumption most likely to
change the decision. Keep prototypes separate and state their limits.

Propose an approach with acceptance examples, key interfaces, dependency order
and verification. Record consequential accepted decisions in the project's
existing documentation. A planning-only task ends with the plan; a request that
includes implementation continues under the same lead.

## Diagnose and repair

Get evidence of the reported defect: a failing test, real invocation, trace or
small reproduction. A setup failure does not reproduce the defect. When the cause
is unclear, compare explanations and change one relevant variable at a time.
If reproduction is unavailable, explain the limit on your diagnosis.

Fix the responsible code, keep a useful regression check when practical, and
rerun the original scenario as well as any smaller reproduction. For intermittent
failures, retain seeds, timing and sample counts. When repeated fixes depend on
the same assumption, test that assumption before trying another fix. Remove
temporary instrumentation when finished.

## Refactor or migrate

State the problem being solved and behaviour to preserve. Read consumers before
changing an interface. Give mutable state one owner and keep related decisions
together. Complete the local improvement without speculative abstractions.

Plan changes to supported callers and saved data. Where compatibility requires
it, add the new path, migrate consumers and then remove the old path, with a clear
completion condition. If coupled changes cannot pass independently, isolate them
and verify the combined transition.

Before preserving a visual design, capture the original rendering and use Verify's
visual method. Use Measure for quantitative performance claims. Check a new
guardrail through the project's real check path: a valid case must pass and a
representative violation must fail.
