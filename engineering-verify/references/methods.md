# Other verification methods

## Application checks

Identify the process, revision, account, configuration and data being exercised.
Observe both the action and its important persisted or external effects. Use
disposable fixtures where possible. A command labelled dry-run still needs its
effects checked; the label grants no permission to write or send messages.

## Visual checks

Capture the independent reference and compare the rendered result at matching
viewport and state. Check relevant responsive layouts and interactions. Describe
visible differences precisely. A successful build or one screenshot cannot
establish behaviour in states that were not observed.

## Formal and generated-input checks

State the property, input domain, assumptions and bounds. Explain how the checked
model or function relates to the implementation. Confirm that valid starting
states and generated cases exist, filters have not discarded the useful domain,
the intended property is registered, and its check completed.

Use representative counterexamples or isolated faults to establish that a
consequential property rejects relevant bad behaviour. Keep errors, timeouts and
incomplete checks visible. Report uncovered states and assumptions; a result for
a bounded model supports claims within that model and bound.

For checks that others will maintain, keep setup, inputs, expected observations,
cleanup and environmental limits beside the check or in the existing test guide.
