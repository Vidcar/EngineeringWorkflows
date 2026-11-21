# Track and resume a program

## Keep one record

Use the project's existing storage. The coordinator maintains a record linking
each worker's output. Include only what is needed to coordinate the work:

- Goal, exclusions, permission, requested finish and resource limits.
- Units, dependencies, status, owner, allowed writes and active resources.
- Exact inputs and outputs, including uncommitted or new files and the environment.
- Acceptance evidence, findings, stale checks, unresolved decisions and next work.

Distinguish planned, running, blocked, awaiting review, verified, handed off,
delivered, paused and cancelled work. Queued work has not been delivered. Resolve
missing inputs or coordinator decisions before replacing a waiting worker.

Use supported event notifications or limited polling during the active session.
Create a schedule only when requested. Choose sequential or parallel work from
the dependencies and actual host capacity. One integrator assembles the result.
Use the first representative unit to check dispatch, verification and delivery.

## Replace writers safely

Record each writer's starting content and owned resources. Before replacement,
observe a stop acknowledgement or termination, inspect saved work and live
resources, then record the replacement's assignment ID and ownership. Silence,
a timeout or an old status message does not establish that writing has stopped.

If stopping is unconfirmed, hold writes to those resources and continue other,
isolated work. Send late output to the current owner for inspection; do not let it
overwrite current work.

Follow Workflows' `references/coordination.md` for isolation and source transfer.
Receivers confirm accessible inputs, exact versions and owned outputs before
writing. When a dependency changes, rerun affected checks after integration.

## Recover and finish

On interruption, save decisions, actual outputs and evidence, active workers,
owned resources and operations whose effects are uncertain. On resume, inspect
live state and confirm who still owns each resource. Check uncertain external
effects before retrying. Preserve useful evidence before removing temporary work.

Tie retries to a diagnosis and the remaining budget. Replan when attempts stop
producing useful evidence. Report exhausted or unavailable units explicitly; a
successful subset does not establish that the whole program succeeded.
