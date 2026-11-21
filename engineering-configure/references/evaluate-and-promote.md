# Evaluate and save a change

An evaluation or review-package request leaves the active skills unchanged. Use
the requested source for a candidate. Follow the host's official skill-authoring
process when installation or a persistent personal-skill update is requested.

## Compare actual behaviour

1. Freeze baseline and candidate contents, including references and metadata.
   Define the decision, requirements and success criteria before running trials.
   Record the actual loaded catalog, host, model, tools and fixture versions.
2. Choose a small set of realistic tasks with real inputs and plausible failures.
   For substantive instruction changes, use fresh task runs or isolated fixtures.
   Check routing, permitted writes, recovery and honest completion where affected.
   Use [routing cases](routing-cases.md) for selection and scope changes. The source
   repository's `evals/` directory provides runnable fixtures when available.
3. Give runners ordinary requests and necessary inputs. Keep evaluator expectations,
   preferred answers and earlier reviews out of their context. Use comparable
   conditions and isolated outputs. Keep failed and partial attempts.
4. Inspect actual outputs, execution traces, checks and effects. Score what happened;
   a plan, claimed execution or agreement between models does not establish success.
   Use Arena for alternatives, Measure for quantitative comparisons, Check for
   judgment or Verify for specific checks, within the current assignment.

## Validate the candidate

Inspect the combined pack after edits, including references, metadata and routing.
Campaign and Configure still require a direct user request. Run Workflows'
`scripts/validate_pack.py --root PACK_ROOT` and relevant bundled tests against the
candidate being delivered or installed. These check files and helpers; agent
behaviour needs task trials. Reproduce material findings and refresh affected
evidence after changes.

Stop when the requested scope has enough evidence. Another round needs a specific
unresolved question or risk; honour any greater depth the user requested.

## Deliver the requested result

For a review package, deliver the candidate and state what was tested. For an
authorised installation or update, validate, save and inspect the resulting files
through the official process. Preserve a rollback where supported. Report
evaluated, saved and observed behaviour separately. If saving fails, retain the
candidate and explain the smallest step needed to finish.
