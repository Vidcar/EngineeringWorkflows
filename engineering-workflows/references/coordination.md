# Delegate, hand off and resume

Keep one lead responsible for integration. When coordination needs a record, keep
one short record of the goal, permissions, owners, source and base, dependencies,
current state, evidence and next action. The lead updates it; workers return their
own results. Check actual state when resuming rather than relying on chat history.

## Assign work that can be checked

Give each worker a result to produce, acceptance examples, exact inputs, files and
resources it may change, dependencies, checks and a stopping condition. Provide
accessible references, including applicable project skills and the method needed
for that phase. Give reviewers a fixed target and a neutral brief, with
target edits prohibited. Workers stay within their assignment.

Decide whether workers cover separate required parts or produce alternatives for
selection. Every required part must be covered; do not turn unfinished work into
a race to accept the first answer. Respect the available concurrency.

Use separate worktrees or checkouts and separate mutable resources for concurrent
writers. Different branches in one folder do not isolate files. If workers share
a folder, assign disjoint files and let the coordinator perform all Git operations.
Isolate ports, databases and output folders where they could collide.

## Hand off actual inputs

Identify the repository, base and exact content, including relevant dirty and new
files. Supply an accessible commit, patch or bundle, setup instructions, data and
configuration assumptions, resource ownership and a return location. Keep secrets
out of briefs. The receiver must confirm the inputs it has before writing; missing
bytes block that handoff. Code transfer does not establish computer access.

Inspect returned changes and evidence. Integrate accepted changes one at a time,
account for the new base, and check interactions in the combined result. Start
dependent work only after its required inputs are available.

## Stop and resume safely

Before replacing a writer, stop it and observe acknowledgement or termination.
A timeout does not release its files or resources. Preserve partial work. If its
state is uncertain, hold those resources and continue independent tasks.

On STOP, halt new effects, pass the stop to workers and record any live processes
or unfinished operations. On resumption, check source, ownership and whether the
evidence is still current. Reuse valid completed work.

Before cleanup, check for active owners, dirty or new work, unshared commits and
dependent processes. Preserve needed evidence and remove only resources you own.
