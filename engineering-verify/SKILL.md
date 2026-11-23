---
name: engineering-verify
description: Run defined checks or create and maintain tests, project verification skills and formal checks. Use for regression coverage, real application journeys, visual comparison, invariants and verification drift. Reviews and readiness decisions belong to engineering-check.
---

# Verify the behaviour

Resolve `engineering-workflows` by exact catalog name and read its
`references/contract.md` once per task. If it is unavailable, report the gap and
continue useful work within the agreed scope.

Handle requests for checks or verification assets. Workflows leads requests that
also change production code. When supporting another lead, keep the assigned
scope, allowed writes and budget; return evidence without invoking other engineering
skills. For user-directed scope changes, follow "When the user changes the
outcome" in the shared contract.

1. Identify the behaviour to check, the expected result and its source. Identify
   the actual code, including dirty or new files, and the relevant environment,
   version, data and entrypoint.
2. Discover relevant project verification skills and harnesses through the active
   catalog, instructions and host-supported project locations. Read their
   coverage, prerequisites and freshness. Reuse a suitable procedure; a file's
   presence alone does not establish host registration.
3. Choose a check that exercises the responsible code and can detect the relevant
   mistake. Inspect important persisted or external effects when warranted, using
   disposable resources and only permitted operations. For a repair, reproduce
   the original failure when practical. Keep a bounded check bounded; create a
   project skill when requested or justified within scope.
4. Run the intended checks and confirm they completed. Establish what ran, what
   was skipped and what failed during setup. Limit each claim to what the check
   actually establishes.
5. Refresh affected evidence and procedures after edits or integration. Report the
   input, observation, result and limits. Keep baseline failures, blocked checks and
   untested claims visible.

Read the reference needed for the work:

- [Testing](references/testing.md) before writing, materially changing or
  assessing tests.
- [Application verification](references/application.md) for real application
  journeys or creating and maintaining a project control skill or feature map.
- [Formal verification](references/formal.md) for model checking, proof,
  consequential invariants or maintaining correspondence between checks and code.
- [Other checks](references/methods.md) for visual comparison or generated inputs.
- [Bend laws](references/bend.md) when the project uses Bend or it is requested.
