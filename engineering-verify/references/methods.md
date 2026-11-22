# Other verification methods

## Visual checks

Capture the independent reference and compare the rendered result at matching
viewport and state. Check relevant responsive layouts and interactions. Describe
visible differences precisely. A successful build or one screenshot cannot
establish behaviour in states that were not observed.

## Generated-input checks

Exercise the responsible implementation rather than a duplicate of its algorithm.
Derive properties from the required behaviour. State the input domain, generators,
filters, seeds and limits that affect the claim. Check that useful valid and invalid
cases remain reachable and the intended assertions actually execute. Retain a
small reproducible counterexample when generation finds a failure.

Use the testing reference's sensitivity checks for consequential properties.
Sampled generated inputs are testing; an exhausted finite domain is evidence only
for that domain. Neither establishes an unbounded proof. Keep errors, timeouts,
discarded cases and incomplete runs visible.

For checks that others will maintain, keep setup, inputs, expected observations,
cleanup and environmental limits beside the check or in the existing test guide.
Use the application and formal references for those verification lifecycles.
