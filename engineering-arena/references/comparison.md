# Run a fair comparison

## Brief the candidates

Give each candidate the goal, behaviour to preserve, exact inputs, environment,
owned output, allowed writes, required evidence and stopping limit. Include the
requirements; withhold preferred conclusions and other candidates' reasoning.

For designs, ask for realistic caller examples, state ownership, success and
failure flows, recovery, compatibility, and a way to test the most consequential
assumption. For implementations, require evidence that the relevant behaviour
works.

## Keep work independent

Use separate worktrees or checkouts and separate mutable databases, ports,
profiles and outputs. In a shared folder, assign disjoint files and leave Git
operations to the coordinator. Read Workflows' `references/coordination.md` for
cross-host work or writer replacement. Confirm a writer has stopped before
replacing it; a timeout is insufficient. Preserve its unfinished output.

Prefer available model diversity. Fresh contexts on the same model, including
sequential runs, can still provide independent alternatives. Report what was
actually used. Variants and reviews produced by their own author are useful
fallbacks, but do not count as independent work. Honour stricter user requirements.

## Judge and combine

Separate requirements every candidate must meet from qualities used to compare
them. Consider user value, clear ownership, ease of use, recovery, compatibility,
testability and maintenance. Shorter code is not automatically better.

Give the judge fixed outputs and the full criteria. Withhold author/model labels
and the lead's preferred answer on the first pass. Ask for evidence, remaining
risks and a recommended starting point, rather than scores alone.

Replace one failed candidate only after it has stopped. If every candidate fails,
identify the shared cause before trying one focused revision. Further rounds need
an unresolved consequential question and sufficient resources; honour any greater
depth the user requested. Keep failed attempts visible.

Use one integrator. Check that adopted ideas fit the chosen state and error model,
then verify the exact combined result. Preserve useful alternatives and failure
evidence until the lead has inspected them. Resolve routine technical choices;
return unresolved product choices with options and a recommendation.
