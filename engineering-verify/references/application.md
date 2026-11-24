# Verify the real application

Use the project's actual interface: UI, CLI, service or library. Establish the
task's required journeys and effects before choosing tools. Reuse a relevant
project verification skill or existing harness. Inspect its instructions and the
code; do not assume a familiar command still drives the current implementation.

## Establish and exercise the target

Identify the revision and dirty content, process, account, configuration, data and
entrypoint being checked. Derive startup and interaction commands from the repo.
Use supported interface-control tools and stable handles such as accessible names,
documented commands and routes. Arrange disposable prerequisites without injecting
the result the check is supposed to establish.

1. **Launch:** use an isolated data directory, profile, port or session as needed.
   Include migrations and seed data. Require a usable state; a listening port or
   healthy database may precede application readiness. For a short-lived command,
   build once if needed and use an isolated invocation for each journey.
2. **Doctor:** perform a read-only check of identity, revision, ownership, data,
   authentication and readiness relevant to this interface. Run it before driving
   a new session and after surprising failures. Reset or relaunch when a healthy
   process still has an unusable interface. Diagnose missing capabilities rather
   than guessing selectors or driving an unrelated instance.
3. **Drive and observe:** exercise the real user path. Record the action, expected
   result and actual result, including important persistent effects and forbidden
   effects. A success message alone does not prove saved state. Inspect what a
   dry-run actually skips; its name grants no permission for external effects.
   Choose relevant failure, retry, permission and empty states rather than adding
   every state to every check.
4. **Preserve evidence and clean up:** keep commands, outputs and useful captures
   outside disposable state. Stop only owned processes and remove owned fixtures
   after each failed attempt and at completion. Do not kill by process name or
   discard user work. Confirm evidence still exists after teardown.

Use equivalent baseline and patched environments for a repair. Describe the state
that separates correct from broken behaviour. Label translated or substitute
environments and their limitations; they do not establish unavailable platform
behaviour. Report setup failures and unexercised paths explicitly.

## Leave a reusable procedure when warranted

For requested creation or useful ongoing coverage within scope, prefer the
project's existing runbook and verification commands. Create or update a
discoverable area-specific `SKILL.md` when requested or when it materially
improves discovery. Follow the host's supported authoring process and repository
conventions; describe the application, surface and relevant change triggers.
Avoid personal installation or hard-coded host/cache locations.

Include actual launch, readiness, doctor, drive, evidence and cleanup commands;
dependencies and versions; relevant environment limits; and documented helper
invocations. Leave no placeholders. Keep a small feature map of relevant journeys:
user entry points, prerequisites/reset, stable commands, expected observations and
known traps. Seed the important journeys without claiming untested coverage.

Follow the resulting instructions from a fresh state through one mapped journey,
capture its effects, clean up and confirm the retained evidence. Repair failed
instructions within scope and repeat the affected steps. An unexecuted procedure
is a draft. A successful single journey validates that journey and the exercised
harness, not every feature in the map.

## Maintain the procedure

Check the index against its feature files and relevant source changes. Follow moved
entrypoints and look for new user-facing paths. A task-scoped update exercises its
affected journeys; an explicit full audit requires source and live coverage for
every mapped reachable feature. Report unreachable paths with the attempted route
and missing prerequisite. A convenient alternate route does not verify the original.

Separate documentation drift, harness defects and product regressions using the
intended contract. Correct authorised documentation or harness issues and re-drive
each affected path. Preserve genuine product findings instead of changing expected
behaviour to fit them. Production fixes, external delivery and automation require
their own task authority. Return out-of-scope work to the lead.

Report exercised and blocked coverage, corrections, remaining findings and evidence
locations. Keep cleanup and evidence preservation valid through all retries.
