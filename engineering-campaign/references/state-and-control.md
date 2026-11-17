# Program state, control and recovery

Read before dispatching units or resuming a program. Keep one coordinator-written
record linking separately owned outputs; use existing storage, not new workflow
infrastructure. Record only what coordination needs:

- User outcome, exclusions, authority, finish and resource/stop bounds.
- Unit dependencies, current states, owner, allowed writes and active resources.
- Exact input/output identities, dirty/new content and relevant environment.
- Acceptance evidence, findings, stale checks, unresolved decisions and next work.

Distinguish planned, running, blocked, review-pending, verified, handed-off,
delivered, paused and cancelled. Queued work is not delivery. A unit awaiting its
input or the coordinator needs that dependency resolved, not automatic replacement.
Use supported event notifications where available; otherwise use bounded
active-session polling. Create schedules only when explicitly requested.

Choose sequential or parallel work by dependency and actual host capacity. One
integrator owns the assembly. A representative first unit tests the dispatch,
verification and authorized finish before repeating the pattern at scale.

For each writer, name its resource ownership and starting content. Before
replacement, observe stop acknowledgment or termination, inspect saved work and
live resource state, then assign a fresh ownership generation. Silence, timeout
and stale status are insufficient. If stop is unconfirmed, hold that unit's
writes and continue separately isolated work. Late output goes to the current
owner for inspection, never directly over current state.

Use shared coordination.md for source transfer and isolation details. Receivers
acknowledge accessible inputs, exact versions and owned outputs before writing.
A changed dependency makes affected downstream evidence stale; recheck after
integration rather than forwarding branch-level passes.

On interruption, checkpoint decisions, actual artifacts/evidence, active workers,
owned resources and operations with uncertain effects. Resume by inspecting live
state and confirming no old writer retains ownership. Reconcile uncertain external
effects before retrying. Preserve useful evidence before task-owned cleanup.

Bound retries by their diagnosed purpose and remaining resources. Replan when
repeated attempts add no evidence. Report exhausted or unavailable units explicitly;
a successful subset does not certify the whole program.
