# Use Bend laws when they help

Read this when the project uses Bend or the user requests it. Apply the formal
verification reference for property selection, implementation correspondence,
sensitivity, reusable instructions and maintenance. Do not introduce a language
migration or make Bend a requirement for routine changes.

Use the project's pinned tooling and inspect the actual law registration and
result. Consult primary documentation when syntax, language version or result
semantics are unclear; do not invent verifier commands. Inspect specification
helpers, types and imports that determine the law's meaning as well as the law
itself. A property that repeats its premise or excludes difficult cases gives
little assurance.

Confirm which obligations completed and whether the tool established examples,
bounded checking or proof. Errors, timeouts and missing laws remain unresolved.
Check important model assumptions at the real application boundary and retain
ordinary tests for behaviour outside the verified scope.
