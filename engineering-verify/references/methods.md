# Verification methods

For behavioral tests, assert through the public interface or observable state. Include error paths and absence of duplicate or forbidden effects when material. Use an independent example or established contract for the oracle; for a consequential oracle, show in isolation that a representative defect makes the check fail. Preserve existing meaningful coverage.

For real application checks, identify the process, revision, account, configuration, and data as applicable; observe the action and resulting persisted state. A dry-run label does not prove the absence of writes or messages. Use disposable fixtures and do not infer authorization for external effects.

For visual parity, capture the independent reference and compare the actual rendered result at matching viewport and state, including responsive and interaction states when relevant. Record meaningful differences rather than relying on a build or one screenshot.

For formal or generated-input checks, specify the property, assumptions, boundaries, and relation between model and implementation. Confirm intended initial/reachable states are nonempty, the intended property is registered, and its check actually completed. Check representative counterexamples, report uncovered states and bounds, and do not claim a bounded model proves the whole application. For maintained verification assets, document setup, inputs, expected observation, cleanup and environmental limits.
