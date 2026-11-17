# Delegate, hand off and resume

Keep one lead and integration owner. Use one compact task record when coordination
or resumption needs it: goal/authority, owners, workspace/branch/base, dependencies,
state, evidence and next action. The lead updates this record; workers return
separate artifacts. Conversations provide context, not authoritative current state.

## Assign useful work

Give each worker its outcome, acceptance examples, exact inputs, owned writes,
dependencies, checks, return artifact and stopping condition. Use bounded reads
and accessible pointers. A reviewer gets a frozen target and neutral brief, with
target edits prohibited. Workers do not start another coordination lifecycle.

Distinguish partitioned work, where every required part must finish, from competing
attempts, where a declared selection rule chooses an output. Do not silently turn
missing coverage into a first-result race. Respect actual concurrency capacity.

Concurrent writers default to separate worktrees/checkouts, task branches and
mutable runtime resources such as ports, databases and output folders. Different
branches in one folder do not isolate files. If workers must share a folder,
they only patch assigned files; the coordinator owns every Git operation there.

## Cross-host transfer

Identify repository, exact base and input content, including relevant dirty/new
files; use an accessible commit, patch or content bundle. Include required setup,
data/configuration assumptions, owned resources and the return location. Never
put secrets in a brief. The receiver acknowledges the actual source and inputs
before writing; missing local bytes are a blocked handoff, not permission to guess.
Computer access and code synchronisation are separate capabilities.

Inspect returned changes and evidence. Integrate accepted work one change at a
time, account for the new base, and verify interactions on the combined artifact.
Only unlock dependent work when its required output is actually available.

## Interruption and cleanup

Before replacement, stop the previous writer and observe acknowledgment or
termination. Timeout alone does not release ownership. Preserve partial work;
if termination is uncertain, hold those resources and continue independent tasks.
On STOP, stop new effects and propagate it to workers. Record live processes and
unfinished operations. Resume by checking actual source, ownership and evidence
freshness before continuing; do not restart valid completed discovery.

Remove only task-owned resources after checking for active owners, dirty/new work,
unshared required commits and dependent runtimes. Preserve evidence first.
