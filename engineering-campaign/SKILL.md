---
name: engineering-campaign
description: Coordinate an engineering program, campaign or work queue when the user directly requests it. Large or lengthy tasks alone do not need Campaign. Persistent automation requires its own request.
---

# Coordinate a program

Use Campaign only for a direct request to coordinate a program or queue; ordinary
language is enough. Keep the existing lead when this is part of a larger request.
Resolve `engineering-workflows` by exact catalog name and read its
`references/contract.md` once per task. Reading it does not call that skill. Report
missing guidance and continue within the agreed scope.

1. Define the outcome, exclusions, work units, dependencies, acceptance checks,
   requested finish and resource limits. Keep one coordinator and one durable
   program record. Read [state-and-control.md](references/state-and-control.md)
   before dispatch or resume, and Workflows' `references/coordination.md` before
   parallel work, source transfer or writer replacement.
2. Assign specific units to Workflows for investigation or implementation, Check
   for review, Verify for checks and tests, Measure for measurements, or Arena for
   alternatives. Include exact inputs, allowed writes, review requirements, budget
   and return conditions. Workers stay within their assignment. Do not start
   another campaign or call Configure automatically.
3. Complete and verify a representative unit before repeating the pattern at
   scale. Respect dependencies and isolate writers and runtime resources. Inspect
   actual outputs and failures, using the shared review rules. Diagnose stalled
   work before retrying; a worker's progress report alone is insufficient.
4. Integrate through one owner and recheck the combined result. For external
   delivery, read Workflows' `references/delivery.md` and confirm the actual
   destination state. Report each unit's status, evidence, open findings and next
   action.

Coordination grants no additional permission to deploy, message, spend or schedule
background work. Reuse existing permission; finish a planning-only request with
the plan. On STOP, halt new actions, confirm writers have stopped and preserve
unfinished work. Claim ongoing monitoring only when the user requested it and a
supported persistent mechanism is actually running.
