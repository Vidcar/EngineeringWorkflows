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
   finish. Read the relevant code, callers, project instructions and checks.
2. Choose an approach. Read [methods](references/methods.md) for investigation,
   planning, repair or migration. Use Arena for a consequential choice that needs
   independent alternatives.
3. Before writing or materially changing tests, resolve `engineering-verify` by
   exact catalog name and read its `references/testing.md`. Apply it whether you
   write the tests yourself or delegate them.
4. Make coherent changes. Delegate when it helps; read
   [coordination](references/coordination.md) before parallel work, a handoff or
   resumption. Keep shared interfaces and integration with one owner.
5. Verify the combined result against the original requirements and preserved
   behaviour. Follow the shared review rules. Ask Check, Verify or Measure a
   specific question when their help is useful.
6. Remove your temporary work, update instructions affected by the change and
   complete [delivery](references/delivery.md) at the requested finish.

For substantial technical prose or a reusable lesson, read
[writing and lessons](references/notes.md). Return the result, decisive checks
and remaining limits. Stop when the requested work is complete.
