# Finish at the requested destination

Use the requested finish and existing permission: local changes, a shared branch,
draft PR, readiness assessment, merge or deployment. Prepare the concrete result
before any necessary final approval. Readiness alone does not authorise release.

Resolve supported review findings and required CI checks on the current change.
Separate product defects from existing failures and infrastructure problems.
Retry a transient failure for a stated reason and with a limit. Keep useful checks
intact.

Before an external action, confirm the destination, revision, required checks and
permission. Use expected-revision safeguards where available. Deliver dependent
changes in order, only as far as the verified work permits. If an action's result
is uncertain, inspect remote state before retrying. Read back the actual merged,
published or deployed version; a queued action is still pending.

Send only requested or already authorised notifications. If delivery is blocked,
preserve the work and evidence and state the exact missing decision or capability.
