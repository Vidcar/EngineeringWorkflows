# Use Bend laws when they help

Read this when the project uses Bend, the user requests it, or a specific
consequential invariant makes formal checking worth considering. Keep ordinary
testing proportional to the same task. Do not introduce a language migration or
make proof a requirement for routine changes.

1. Identify the required rule and the mistake it should exclude. Derive it from
   the requirement, not from whatever the implementation currently does. Check
   that useful valid cases satisfy it and representative bad cases violate it.
   A property that merely repeats its premise gives little assurance.
2. State the input domain, assumptions and bounds. Confirm there are valid inputs
   and reachable states; restrictive assumptions must not remove the difficult
   cases the rule was meant to cover.
3. Connect the law to the shipped code. If it checks a separate model, explain the
   mapping and verify the important assumptions at the real application boundary.
   Identify behaviour outside the model that still needs testing.
4. Use the project's pinned tooling and inspect the actual registration and
   result. Consult primary documentation when syntax or result semantics are
   unclear. Confirm the intended check completed; errors, timeouts and missing
   properties remain unresolved.
5. Report what the tool actually established, for which code and assumptions.
   Distinguish examples, bounded checking and proof as applicable. Refresh the
   result when the relevant code, law, assumptions or tooling changes.
