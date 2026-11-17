# Conditional execution methods

## Investigate or plan

Trace the actual callers, state and constraints. Separate observation, inference
and hypothesis; use primary sources for uncertain external facts. For historical
claims distinguish evidence found, searched-empty and inaccessible history.
Resolve the assumption most likely to change the decision with a small probe.
Keep prototypes isolated and label what they do not prove.

Recommend an approach with acceptance examples, important interfaces, dependency
order and verification. Document consequential accepted decisions once in the
project's existing home. A decision-only request ends at that artifact; a mixed
request continues to implementation under the same owner.

## Diagnose and repair

Obtain a symptom-specific signal: failing test, real invocation, trace or minimal
reproduction. A setup failure is not the reported defect. For ambiguous failures,
compare causal predictions and change one explanatory variable per probe. If
reproduction is unavailable, preserve useful inspection and qualify the cause.

Fix the responsible path, retain a meaningful regression check when practical,
and rerun the original unminimised scenario. For flakes retain seeds/timing and
sample counts. Repeated failed fixes sharing a premise call for testing that
premise, not another blind retry. Remove temporary instrumentation after use.

## Refactor or migrate

Name the demonstrated problem and behaviour to preserve. Read consumers before
changing an interface; give mutable state one owner and related knowledge a
coherent home. Prefer a complete local improvement over speculative abstractions.
Migrate supported callers and saved data deliberately. Use expand/migrate/contract
when compatibility requires it, with an explicit completion condition. If a coupled
transition cannot stay green between steps, isolate it and verify the final boundary.

Capture the original rendering before an appearance-preserving change; use
engineering-verify's visual method. Use engineering-measure before quantitative
performance claims. A new guardrail must accept a valid case and reject the
representative violation through the project's real check path.
