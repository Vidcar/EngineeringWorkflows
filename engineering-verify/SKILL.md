---
name: engineering-verify
description: Run defined checks or create and maintain tests and other verification assets. Use for regression tests, real application checks, visual comparison and scoped formal checks. Reviews and readiness decisions belong to engineering-check.
---

# Verify the behaviour

Resolve `engineering-workflows` by exact catalog name and read its
`references/contract.md` once per task. If it is unavailable, report the gap and
continue useful work within the agreed scope.

Handle requests for checks or verification assets. Workflows leads requests that
also change production code. When supporting another lead, keep the assigned
scope, allowed writes and budget; return evidence without invoking other skills.
Follow the shared contract when the user changes the requested outcome.

1. Identify the behaviour to check, the expected result and its source. Identify
   the actual code, including dirty or new files, and the relevant environment,
   running version, data and entrypoint.
2. Choose a check that exercises the responsible code and can detect the relevant
   mistake. Inspect important persisted or external effects when warranted, using
   disposable resources and only permitted operations. For a repair, reproduce
   the original failure when practical.
3. Run the intended checks and confirm they completed. Establish what ran, what
   was skipped and what failed during setup. Limit each claim to what the check
   actually establishes.
4. Refresh affected evidence after edits or integration. Report the input,
   observation, result and limits. Keep baseline failures, blocked checks and
   untested claims visible.

Read the reference needed for the work:

- [Testing](references/testing.md) before writing, materially changing or
  assessing tests.
- [Other checks](references/methods.md) for application, visual or formal checks.
- [Bend laws](references/bend.md) when Bend is already used or requested, or a
  specific consequential invariant warrants considering it.
