---
name: engineering-workflows
description: Implement, fix, refactor, investigate or plan software changes. Own requests that include a working change, with specialists helping on review, testing, measurement or alternatives. Exclude general programming questions and ordinary prose editing.
---

# Carry the work through

Read [the shared rules](references/contract.md) once per task; they apply to every
helper too.

## Choose the right starting point

For a new request, choose by the result the user wants:

| Requested result | Skill |
| --- | --- |
| Investigation, plan, prototype or working change | Workflows |
| Review or readiness assessment only | Check |
| Tests or execution of defined checks only | Verify |
| Benchmark or measured comparison only | Measure |
| Independent alternatives and a comparison only | Arena |

Keep one lead across skills and adjust the workflow when the user changes the
requested result. Preserve completed work.
Campaign and Configure require a direct request for program coordination or pack
administration; a large task or a missing tool does not select them.

## Do the work

1. Establish what must work, what must stay the same and where the task should
   finish. Read the relevant code, callers and project instructions. Discover
   existing project skills and harnesses by the behavior and code they cover,
   not just their names. Check that their commands and assumptions still apply.
2. Choose the needed phases using [routing](references/routing.md). Read
   [methods](references/methods.md) for investigation, design, impact analysis,
   repair or migration. Use Arena for a consequential unresolved choice; use
   Measure before changing a performance-sensitive path or interpreting numbers.
3. Before writing or materially changing tests, resolve `engineering-verify` by
   exact catalog name and read its `references/testing.md`. Apply it whether you
   write the tests yourself or delegate them. For real application checks or
   reusable control skills, read Verify's `references/application.md`; for formal
   checks or maintaining a model/proof, read its `references/formal.md`. Read the
   matching guidance before preparing the check, even when doing the work yourself.
4. Make coherent changes. Delegate when it helps; read
   [coordination](references/coordination.md) before parallel work, a handoff or
   resumption. Keep shared interfaces and integration with one owner.
5. Verify the combined result against the original requirements and preserved
   behaviour through the relevant project skill or real entrypoint. Reconcile
   changed verification assets with the code they describe. Follow the shared
   review rules; give Check the concrete change and remaining risks. Ask Verify
   or Measure a bounded evidence question when their help is useful.
6. Remove your temporary work, update instructions affected by the change and
   complete [delivery](references/delivery.md) at the requested finish.

For substantial technical prose or a reusable lesson, read
[writing and lessons](references/notes.md). Return the result, decisive checks
and remaining limits. Stop when the requested work is complete.
