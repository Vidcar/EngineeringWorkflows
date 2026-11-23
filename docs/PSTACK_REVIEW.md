# Pstack review and adaptation recommendation

## Recommendation and scope

Keep Engineering Workflows' seven skills. Strengthen the links between task phases, project verification procedures, and the specialist that can resolve the current uncertainty. Add detailed application and formal verification guidance under Verify, where agents already look for evidence. Preserve one accountable lead, proportional checks, and the requested finish.

The comparison uses [pstack 0.15.46 at `7a583913`](https://github.com/cursor/plugins/tree/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack) and [Engineering Workflows 2.2.0 at `6277fe35`](https://github.com/Vidcar/EngineeringWorkflows/tree/6277fe359e25fd37e8c734a4627b3260d5245c78). The pinned upstream inventory contains **553 files, 58 top-level skills, 3 embedded Benny skills, 22 playbooks, and 2 agents**. Every skill and playbook has a disposition below. Supporting instructions are mapped separately; executable implementations and their tests are grouped by subsystem.

This is an instruction and architecture review, with scoped inspection of executable sources and representative tests. It is not a line-by-line audit of all 553 files. Generated corpora and illustration assets were inventoried. Pstack's runtimes were not executed as part of this source comparison. Actual candidate checks, agent trials, failures and unexercised integrations are recorded in [EVALUATION.md](EVALUATION.md), with the [source inventory and execution evidence](../evals/results/pstack-2.3.0/README.md).

**Adapt** means the candidate adds or strengthens the useful mechanism. **Covered** means an equivalent useful rule already exists and is retained. **Defer** means the feature is optional, host-specific, or unsuitable as a general default. A deferred component is not presented as an implemented capability.

## Why these changes matter

The baseline already required independent expectations, real execution, useful failure cases, honest limitations, bounded delegation and preservation of user work. Its weakest points were navigation and durable verification: agents could know that formal checks were allowed without receiving a complete creation and maintenance method, or overlook an existing project procedure during ordinary implementation.

The candidate addresses six concrete gaps:

1. **Route by the current need.** [Routing] connects task situations to relevant guidance and useful evidence. [Workflows] requires discovering project procedures by behavior and coverage, and loading applicable Verify guidance before preparing checks, including work done without delegation.
2. **Verify the actual application.** [Application] specifies target identity, usable readiness, real actions and effects, evidence retention, owned cleanup, reusable feature procedures and maintenance. A convenient alternate route cannot establish that an unexercised entry point works.
3. **Maintain formal correspondence.** [Formal] adds method selection, source mapping, realistic atomicity, property sensitivity, synchronization records and an executed real-code-break rehearsal. It distinguishes code/model drift from a genuine failing property and accounts for dirty content that a commit alone cannot identify.
4. **Improve design and impact analysis.** [Methods] makes state ownership, boundary validation, retries and compatibility explicit. [Impact] follows persisted formats, downstream consumers, pinned dependencies and lifecycle ordering, then investigates the assumptions that matter most.
5. **Trust measured work.** [Measurement] checks timing boundaries, completed work, output correctness, error counts, realistic settings, variability and plausible limits before interpreting a number. A measured difference remains distinct from its causal explanation.
6. **Finish and learn within scope.** [Delivery] separates status, remediation, PR creation and release. [Notes] turns repeated mistakes into tested structural prevention while preserving useful rationale. [Coordination] carries the relevant project references into bounded assignments.

## Architecture and phase routing

The seven roles remain Workflows for implementation and investigation, Check for judgment, Verify for execution and verification assets, Measure for quantitative evidence, Arena for competing alternatives, Campaign for explicitly requested programs, and Configure for explicitly requested pack administration. A specialist or reference does not replace an existing lead. Project-specific verification skills can be generated when useful within the task; they are not additional global pack roles.

The following routes are conditional. A small local edit does not need every phase or a new verification framework.

| Phase or situation | Candidate route | Evidence expected |
| --- | --- | --- |
| Understand, investigate or resume | [Methods] and [Coordination] | Current source, actual environment, supported history and explicit hypotheses. |
| Design interfaces, state or a consequential prototype | [Methods]; [Arena] when alternatives require comparison | Observable contract, owner of mutable state, affected consumers and a discriminating experiment. |
| Prepare or maintain checks | [Testing], [Application] or [Formal], plus relevant project instructions | A usable procedure tied to the implementation and the intended behavior. |
| Implement, repair or migrate | [Workflows] and [Methods] | A coherent change, preserved contracts, original failure evidence when practical and verified integration. |
| Review assumptions and readiness | [Check] and [Impact]; bounded Verify/Measure support | Supported findings, cleared risks, evidence limits and independent scrutiny. |
| Measure or optimize | [Measure] and [Measurement] | Comparable correct work, reproducible observations and a justified keep/revert decision. |
| Deliver or report status | [Delivery] | The authorized endpoint on the current head/base, complete relevant evidence and remote readback. |
| Coordinate a program or revise the pack | [Campaign] or [Configure] on direct request | Bounded units or an evaluated candidate; no implicit schedule, message or installation authority. |


## Every top-level skill

Each source link is pinned to the reviewed revision. Candidate links point to the implementation in this PR.

### Workflow, engineering and communication skills

| Pstack skill | Disposition | Useful mechanism and candidate destination |
| --- | --- | --- |
| [architect](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/architect/SKILL.md) | Adapt | Sketch consequential interfaces and state before logic; [Methods] and [Arena] resolve uncertain shapes without mandatory design ceremony. |
| [arena](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/arena/SKILL.md) | Covered | Independent alternatives, neutral judging and coherent synthesis remain in [Arena] and [Comparison]; no fixed model vendors. |
| [automate-me](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/automate-me/SKILL.md) | Adapt | Evidence-based skill improvement belongs in requested [Configure] work and [Notes]; history mining and personal-mode installation remain separate. |
| [benchmark-checklist](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/benchmark-checklist/SKILL.md) | Adapt | Completed timed work, errors, tuning and plausibility strengthen [Measurement]; sample counts follow the decision, not a universal quota. |
| [blast-radius](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/blast-radius/SKILL.md) | Adapt | Indirect contracts and pivotal safety assumptions enter [Impact], with bounded probes instead of speculative risk lists. |
| [bro](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/bro/SKILL.md) | Covered | Plain-language restatement is handled by [Notes]; a separate style skill adds no engineering capability. |
| [correct](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/correct/SKILL.md) | Adapt | Recurring mistakes trigger tested structural prevention in [Notes]; preserve legitimate cases and useful rationale. |
| [create-formal-verification-skill](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/create-formal-verification-skill/SKILL.md) | Adapt | [Formal] defines target/method choice, correspondence, reusable instructions, sensitivity and the complete defect-detection rehearsal. |
| [create-verification-skill](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/create-verification-skill/SKILL.md) | Adapt | [Application] provides real-interface launch, readiness, drive, observations, cleanup and a rehearsed project skill. |
| [figure-it-out](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/figure-it-out/SKILL.md) | Adapt | [Routing] and [Methods] combine evidence-led phases under one owner; use [Coordination] for consequential decisions and handoffs. |
| [how](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/how/SKILL.md) | Covered | Source-based runtime explanations remain in [Methods]; delegation is useful support rather than a mandatory explanation step. |
| [in-your-own-words](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/in-your-own-words/SKILL.md) | Covered | [Workflows] establishes goals and preservation conditions; restate material ambiguity without adding an approval gate. |
| [interrogate](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/interrogate/SKILL.md) | Adapt | [Impact] pursues falsifying evidence and retains supported findings. Static/design findings remain valid when execution cannot settle them. |
| [ketchup](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/ketchup/SKILL.md) | Adapt | [Notes] reports current outcomes and genuine user decisions; [Delivery] keeps a status request read-only. |
| [ketchup-video](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/ketchup-video/SKILL.md) | Defer | Optional evidence-based video presentation is outside core assurance; [Notes] can use a requested, available artifact capability. |
| [maintain-formal-verification-skill](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/maintain-formal-verification-skill/SKILL.md) | Adapt | [Formal] reconciles source since the correspondence record, classifies drift and bugs, reruns sensitivity and updates only supported records. |
| [maintain-verification-skill](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/maintain-verification-skill/SKILL.md) | Adapt | [Application] reconciles feature maps, exercises affected paths and separates documentation, harness and product failures. |
| [make-bot-ui](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/make-bot-ui/SKILL.md) | Defer | Cursor/Grok/Tailscale setup is a separate integration task. [Workflows] and [Capabilities] retain normal authority and capability checks. |
| [no-comments](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/no-comments/SKILL.md) | Defer | Reject blanket deletion of ambiguous constraints. [Notes] and [Impact] preserve rationale until evidence or equivalent enforcement makes it redundant. |
| [poteto-help](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-help/SKILL.md) | Adapt | [README] and [Routing] provide ordinary request examples and phase guidance; no extra help entrypoint. |
| [poteto-mode](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/SKILL.md) | Adapt | [Workflows] and [Routing] retain useful phase transitions without fixed models, universal fan-outs or unrelated notification permissions. |
| [recall](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/recall/SKILL.md) | Covered | [Coordination] revalidates source, ownership and evidence. Use authorized host context tools rather than hardcoded transcript directories. |
| [reflect](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/reflect/SKILL.md) | Adapt | [Notes] captures durable failures; requested [Configure] changes tune the relevant instruction or trigger and evaluate the result. |
| [setup-pstack](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/setup-pstack/SKILL.md) | Covered | [Configure] and [Capabilities] distinguish available, configured and exercised support. Normal engineering does not require a setup interview. |
| [sharpen](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/sharpen/SKILL.md) | Covered | [Methods] deepens a task through raw evidence, useful probes and independent acceptance without broadening its scope. |
| [show-me-your-work](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/show-me-your-work/SKILL.md) | Adapt | [Notes] records consequential decisions, reasons and evidence in the existing task record; no mandatory TSV or transcript audit. |
| [statechart](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/statechart/SKILL.md) | Adapt | [Formal] preserves raw results and domain-readable counterexamples; an available statechart skill is optional, not a bundled dependency. |
| [swarm](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/swarm/SKILL.md) | Covered | [Coordination] separates required coverage from races, isolates writers and preserves missing results as gaps. |
| [tdd](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/tdd/SKILL.md) | Covered | [Testing] and [Methods] require meaningful repair evidence where practical and allow a useful alternative when a new test is disproportionate. |
| [teach](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/teach/SKILL.md) | Adapt | [Notes] distinguishes mechanisms, historical motivation and uncertainty; visuals and depth follow the reader rather than mandatory presentation rules. |
| [technical-writing](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/technical-writing/SKILL.md) | Adapt | [Notes] adds real procedural commands and expected observations; project conventions govern formatting. |
| [typescript-best-practices](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/typescript-best-practices/SKILL.md) | Adapt | [Methods] adopts schema authority, explicit variants and validated boundaries. Language syntax and justified casts stay project-specific. |
| [unslop](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/unslop/SKILL.md) | Covered | [Notes] already requires concrete, concise prose and preserved meaning; no extra stylistic pipeline. |
| [why](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/why/SKILL.md) | Covered | [Methods] separates recorded intent, inference, missing history and a search that found nothing. |


### All 24 principles


| Pstack principle | Disposition | Useful mechanism and candidate destination |
| --- | --- | --- |
| [principle-attack-the-premise](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-attack-the-premise/SKILL.md) | Covered | [Methods] tests the assumption shared by repeated failed fixes before another attempt. |
| [principle-boundary-discipline](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-boundary-discipline/SKILL.md) | Adapt | [Methods] validates at actual trust boundaries while retaining internal checks justified by the failure model. |
| [principle-build-the-lever](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-build-the-lever/SKILL.md) | Adapt | [Methods] proves a representative transformation before a bounded rerunnable tool; ordinary nontrivial work does not always need a script. |
| [principle-encode-lessons-in-structure](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-encode-lessons-in-structure/SKILL.md) | Covered | [Notes] prefers effective prevention over repeated prose and verifies both failure rejection and legitimate behavior. |
| [principle-exhaust-the-design-space](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-exhaust-the-design-space/SKILL.md) | Covered | [Arena] compares consequential alternatives; a settled decision is not reopened without reason. |
| [principle-experience-first](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-experience-first/SKILL.md) | Covered | [Comparison] weighs user value, recovery and maintainability; [Workflows] makes the intended experience observable. |
| [principle-explain-the-number](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-explain-the-number/SKILL.md) | Adapt | [Measurement] rules out skipped work, errors, configuration mismatch and implausible savings before trusting a result. |
| [principle-fix-root-causes](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-fix-root-causes/SKILL.md) | Adapt | [Methods] distinguishes legitimate edge states from invalid states produced earlier; sibling repairs remain within scope. |
| [principle-foundational-thinking](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-foundational-thinking/SKILL.md) | Adapt | [Methods] establishes representations, access patterns, ownership and needed foundations before dependent logic. |
| [principle-guard-the-context-window](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-guard-the-context-window/SKILL.md) | Covered | [Routing] loads matching guidance; [Coordination] uses bounded assignments and a compact current record. |
| [principle-laziness-protocol](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-laziness-protocol/SKILL.md) | Covered | [Methods] avoids speculative abstraction; [Comparison] values maintainability rather than line count alone. |
| [principle-make-operations-idempotent](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-make-operations-idempotent/SKILL.md) | Adapt | [Methods] checks retries, interruption points, duplicate effects and ownership of stale resources. |
| [principle-migrate-callers-then-delete-legacy-apis](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | Covered | [Methods] accounts for supported consumers and compatibility before removing old paths. |
| [principle-minimize-reader-load](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-minimize-reader-load/SKILL.md) | Adapt | [Methods] centralizes decisions and mutable ownership without automatically deleting useful wrappers. |
| [principle-model-the-domain](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-model-the-domain/SKILL.md) | Adapt | [Methods] uses valid state representations and actual language guarantees to remove contradictory assumptions. |
| [principle-never-block-on-the-human](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-never-block-on-the-human/SKILL.md) | Covered | [Contract] resolves routine details and reuses permission while reserving consequential product choices and missing authority. |
| [principle-outcome-oriented-execution](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-outcome-oriented-execution/SKILL.md) | Covered | [Methods] permits isolated coupled migrations with explicit compatibility boundaries and combined verification. |
| [principle-prove-it-works](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-prove-it-works/SKILL.md) | Covered | [Contract] and [Verify] demand completed checks on real behavior and limit claims to observed evidence. |
| [principle-redesign-from-first-principles](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-redesign-from-first-principles/SKILL.md) | Adapt | [Methods] reconsiders shapes when requirements or repeated workarounds justify it; no universal rewrite mandate. |
| [principle-separate-before-serializing-shared-state](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md) | Covered | [Coordination] isolates agent resources; [Methods] gives necessary shared state an enforced synchronization mechanism. |
| [principle-sequence-verifiable-units](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-sequence-verifiable-units/SKILL.md) | Covered | [Workflows], [Coordination] and [Program] preserve dependency order and check integration, including coupled-change exceptions. |
| [principle-subtract-before-you-add](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-subtract-before-you-add/SKILL.md) | Covered | [Methods] removes evidenced unnecessary complexity within scope, preserving supported behavior and user work. |
| [principle-test-behavior-not-implementation](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-test-behavior-not-implementation/SKILL.md) | Covered | [Testing] uses independent expectations and real observable effects, preserving useful characterization and interaction tests. |
| [principle-type-system-discipline](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/principle-type-system-discipline/SKILL.md) | Adapt | [Methods] derives shapes from authoritative sources and validates constraints the type system cannot express. |


## All 22 poteto-mode playbooks

These recipes inform phase routing. They do not become 22 additional installed skills or mandatory stages.

| Playbook | Disposition | Useful mechanism and candidate destination |
| --- | --- | --- |
| [authoring-a-skill](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/authoring-a-skill.md) | Covered | [Configure] retains supported authoring, whole-candidate validation and meaningful behavior trials. |
| [autonomous-run](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/autonomous-run.md) | Adapt | [Routing] and [Coordination] use checkable completion and evidence-led iteration; long work alone does not create automation. |
| [autopilot-full](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/autopilot-full.md) | Adapt | [Program] keeps unit ownership, dependencies and readiness evidence. No automatic merge authority or premature writer replacement. |
| [autopilot-stack](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/autopilot-stack.md) | Adapt | [Delivery] distinguishes dependent branches and refreshed head/base evidence; unchanged patch IDs do not establish equivalence. |
| [babysit](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/babysit.md) | Adapt | [Delivery] separates status from authorized remediation and assesses comments as claims, without implicit replies or merge. |
| [bug-fix](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/bug-fix.md) | Adapt | [Methods] and [Application] discover the relevant project procedure, reproduce the separating state and preserve environment identity. |
| [eval](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/eval.md) | Covered | [Evaluation guidance] preserves neutral tasks, exact inputs, actual traces and failed attempts; no fixed vendor panel. |
| [feature](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/feature.md) | Adapt | [Routing] connects observable acceptance, state/interface design, dependencies and application verification. |
| [hillclimb](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/hillclimb.md) | Adapt | [Measurement] validates the workload and baseline; [Routing] keeps implementation with Workflows and calls for measured keep/revert decisions. |
| [investigation](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/investigation.md) | Covered | [Methods] distinguishes source observations, hypotheses and history; mixed requests continue with the same owner. |
| [multi-phase-plan](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/multi-phase-plan.md) | Covered | [Methods] and [Program] define dependencies, boundaries and evidence proportionately, without universal live/performance gates. |
| [opening-a-pr](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/opening-a-pr.md) | Adapt | [Delivery] uses the intended branch/base, concise problem/change/check description and actual remote readback. |
| [pause-safely](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/pause-safely.md) | Covered | [Coordination] stops writers, preserves current work and records next steps; it does not commit arbitrary dirty files. |
| [perf-issue](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/perf-issue.md) | Adapt | [Methods] and [Measurement] connect the correct runtime signal to source and test a bottleneck hypothesis. |
| [prototype](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/prototype.md) | Covered | [Methods] and [Comparison] use isolated bounded experiments with declared production limits. |
| [refactoring](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/refactoring.md) | Adapt | [Methods] pins relevant behavior, follows dynamic and persisted contracts and verifies preserved behavior after movement. |
| [runtime-forensics](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/runtime-forensics.md) | Adapt | [Methods] identifies actual revision/process/data before interpreting runtime evidence; diagnosis does not authorize live fixes. |
| [session-pickup](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/session-pickup.md) | Covered | [Coordination] preserves prior decisions while revalidating current source, ownership and evidence freshness. |
| [shipping](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/shipping.md) | Adapt | [Delivery] checks the current integrated artifact, required results, dependent order and authorized endpoint. |
| [trace-forensics](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/trace-forensics.md) | Adapt | [Methods] correlates signals, source and discriminating observations; no required SQLite conversion or unsupported causal claim. |
| [visual-parity](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/visual-parity.md) | Adapt | [Visual] compares independent baselines at matching states, with declared tolerance instead of a universal zero-diff rule. |
| [worktree-cleanup](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/playbooks/worktree-cleanup.md) | Covered | [Coordination] checks active owners, dirty/untracked work and unshared commits before removing only owned resources. |


## Benny automation and its three embedded skills

Benny is an optional issue-intake and repair deployment. Its useful evidence practices fit existing roles; its Slack wiring, schedules, credentials and host configuration are not installed by this change.

| Embedded skill | Disposition | Useful mechanism and candidate destination |
| --- | --- | --- |
| [setup-benny](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/skills/setup-benny/SKILL.md) | Defer | Vendor-specific installation remains a separate request; [Configure] and [Capabilities] retain supported setup and observed readiness. |
| [triage-issue-reports](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/skills/triage-issue-reports/SKILL.md) | Adapt | [Methods] and [Program] preserve report identity, inspect existing issues/fixes and route by supported cause rather than symptom keywords. |
| [reproduce-and-fix-issues](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/skills/reproduce-and-fix-issues/SKILL.md) | Adapt | [Methods] and [Application] verify the correct environment, discriminating state and concrete existing fix before competing repairs. |

| Supporting piece | Disposition and destination |
| --- | --- |
| [Benny README](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/README.md); [FOR_AGENTS](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/FOR_AGENTS.md) | Adapt stable report identity, adapter capabilities, budgets and source-controlled operational instructions into [Program]; defer the deployment. |
| [Triage routing example](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/skills/triage-issue-reports/references/routing.example.md) | Adapt cause-based ownership in [Methods]; no copied channels, recipients or automatic pings. |
| [Control adapter](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/skills/reproduce-and-fix-issues/references/control-adapter.md) | Adapt identity, isolation, doctor/reset and honest substitute-environment limits in [Application]. |
| [Existing-fix verification](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/skills/reproduce-and-fix-issues/references/verify-existing-fix.md) | Adapt equivalent baseline/patched checks in [Methods]; assessing a supplied artifact does not authorize replacing it. |
| [Feature-map example](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/skills/reproduce-and-fix-issues/references/feature-map.example.md) | Adapt relevant entry points, setup, observations and persistent effects in [Application], without universal media requirements. |
| [Configuration template](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/templates/configuration.example.yaml) | Defer provider, model, budget, media and integration configuration to an explicit deployment through [Configure]. |
| [Triage prompt](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/templates/triage-automation-prompt.md); [Repair prompt](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/automations/benny/templates/reproduce-automation-prompt.md) | Defer live automation shims. [Program] preserves immutable inputs and assignment boundaries; automation or messaging requires separate authority. |


## Agents and supporting instruction files

| Piece | Disposition and candidate destination |
| --- | --- |
| [poteto-agent](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/agents/poteto-agent.md) | Adapt inheritance of applicable instructions through [Coordination]; no Cursor agent type, cache scan or model dependency. |
| [comment-sicko](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/agents/comment-sicko.md) | Defer persona and deletion policy. [Impact] and [Notes] require evidence before discarding constraints or rationale. |
| [Worker contract](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/worker.md) | Covered by [Contract] and [Coordination]; briefs now include relevant project procedures and phase references. |
| [Review-comment triage](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/references/bugbot-triage.md) | Adapt current-source assessment in [Delivery] and [Impact]; reject anecdotal global skip lists and treating comments as new authority. |
| [Prompting](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-help/references/prompting.md); [Recipes](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-help/references/recipes.md) | Adapt ordinary examples into [README] and [Routing cases]; evaluator answers stay outside runner context. |
| [Feature-map index](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/create-verification-skill/references/feature-map-example/README.md) | Adapt a compact coverage index into [Application]; real paths and exercised coverage replace mandatory template fields. |
| [Create-note example](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/create-verification-skill/references/feature-map-example/create-note.md) | Adapt persistence, alternate entry points and cleanup checks in [Application]; no Notes-app fixture is copied. |
| [Search example](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/create-verification-skill/references/feature-map-example/search.md) | Adapt empty/failure states and route accountability in [Application]; an alternate route cannot verify the original. |
| [TypeScript patterns](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/typescript-best-practices/references/patterns.md) | Adapt language-neutral intent in [Methods]. Do not copy the example claiming a plain numeric duration excludes negative ranges. |
| [Statechart rendering](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/statechart/references/render.md) | Defer Pele-specific presentation. [Formal] preserves evidence and permits available visualization without claiming the chart is the proof. |
| [Decision-log template](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/show-me-your-work/references/decision-log-template.tsv) | Defer fixed TSV. [Notes] records consequential decisions and corrections in the existing record. |


## Documentation, packaging and executable components

### Guides and host adapter

| Source guide | Disposition and destination |
| --- | --- |
| [README](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/README.md) | Adapt: Goal-to-route overview is reflected in [README] and [Routing]. |
| [01-setup](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/01-setup.md) | Adapt: [README] and [Capabilities] retain actual host discovery; normal work needs no unsolicited configuration. |
| [02-poteto-mode](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/02-poteto-mode.md) | Adapt: [Routing] adapts task-phase selection and acceptance/preservation examples. |
| [03-understand](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/03-understand.md) | Adapt: [Methods] separates runtime behavior, historical motivation and causal uncertainty. |
| [04-design](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/04-design.md) | Adapt: [Methods] and [Comparison] adopt caller-first design and discriminating prototypes. |
| [05-build-and-clean](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/05-build-and-clean.md) | Adapt: [Methods] pins behavior and checks effects; blanket stylistic cleanup is deferred. |
| [06-verify-and-ship](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/06-verify-and-ship.md) | Adapt: [Application], [Formal], [Measurement] and [Delivery] provide the useful verification and handoff mechanisms. |
| [07-overnight](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/07-overnight.md) | Adapt: [Program] retains bounded completion and durable state; persistent execution requires explicit support and request. |
| [08-principles](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/08-principles.md) | Adapt: The 24 principle dispositions above place useful rules in one owning reference. |
| [09-make-it-yours](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/09-make-it-yours.md) | Adapt: [Configure] and [Evaluation guidance] preserve isolated candidates, actual trials and the promotion boundary. |
| [10-recipes-and-pitfalls](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/10-recipes-and-pitfalls.md) | Adapt: [Routing cases] supplies ordinary prompts and negative scope cases without leaking evaluator answers. |
| [Claude Code adapter](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/harness/claude-code.md) | Defer host-specific commands; [Capabilities] and [Routing] use exposed support and report missing required capabilities honestly. |


### Executable subsystem dispositions


| Source component group | Review scope and decision |
| --- | --- |
| [PR watcher](https://github.com/cursor/plugins/tree/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/scripts/watch-pr) | Inspect CLI, GitHub collection, policy, types/rendering and representative behavior tests. Adapt status/remediation separation, pagination, query failures and current-head evidence in [Delivery]. Do not vendor another forge client or treat watcher readiness as merge authorization. |
| [Watcher packaging](https://github.com/cursor/plugins/tree/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/scripts) | Inventory bootstrap, package manifest, lockfile and TypeScript configuration. Defer this runtime footprint; use available host or project tools. |
| [Worktree audit](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/poteto-mode/scripts/worktree-audit.sh) | Inspect cleanup signals and parsing. Retain [Coordination] safeguards; untracked files, closed PRs or a heuristic suggestion cannot establish disposability. |
| [Statechart application](https://github.com/cursor/plugins/tree/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/statechart/scripts) | Inspect launcher, CLI, TLC orchestration, semantic/config parsing, intermediate representation, graph passes and report backends. Adapt assurance boundaries in [Formal]; defer the independently maintained toolchain. |
| [Statechart tests and corpora](https://github.com/cursor/plugins/tree/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/statechart/scripts/test) | Inspect representative CLI, differential and fuzz tests; inventory captured outputs/models/charts. No claim that these tests or external TLC/Java integrations were run. Missing or skipped obligations remain visible. |
| [Decision logger](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/skills/show-me-your-work/scripts/log.sh) | Inspect append-only TSV and formula-prefix handling. Defer the helper because [Notes] does not require TSV; it is not a shared-writer synchronization mechanism. |


### Metadata and assets


| Source piece | Disposition |
| --- | --- |
| [Pstack README](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/README.md) | Reviewed capability overview; [README] and this document explain selected adaptations without reproducing the full catalog in agent context. |
| [Generic manifest](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/plugin.json); [Cursor manifest](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/.cursor-plugin/plugin.json) | Inventory both 0.15.46 manifests. Keep EW packaging and its seven-skill [Pack contract]; no Cursor registration or plugin dependency is added. |
| [.gitignore](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/.gitignore) | Packaging-only exclusions; no workflow behavior to adapt. |
| [Logo](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/assets/logo.png); [Six guide illustrations](https://github.com/cursor/plugins/tree/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/docs/guide/images) | Inventoried presentation assets; not copied, regenerated or treated as execution evidence. |
| [MIT license](https://github.com/cursor/plugins/blob/7a583913eb1b8d1a0ee76753d1a2cf072e7b54f9/pstack/LICENSE) | Preserve attribution for adapted material. Existing [EW license] includes Lauren Tan and Matt Pocock and identifies the compilation as independent. |


## Boundaries deliberately preserved

The candidate depends on its own instructions and available tools, not an installed pstack plugin. It does not provision TLA+, Java, a proof assistant, Pele, a video renderer, Slack automation or paid model access. Projects choose and pin tools appropriate to the claim. Generated-input tests remain sampled testing; finite exploration remains bounded; source correspondence is not a formal proof of implementation equivalence.

Creation of durable project verification is conditional on useful authorized work. Formal checking is not a gate for every edit. Full feature audits, per-feature workers, mandatory videos, a particular model vendor and fixed iteration counts are not universal requirements. Read-only reviews retain their scope; static/design evidence is not discarded merely because no executable reproduction is available.

Delivery keeps current approval and check requirements. Comments cannot expand authority. Status does not imply remediation, a PR does not imply merge, and long work does not imply a recurring automation. Cleanup preserves untracked work and unresolved ownership. A meaningful constraint comment stays until evidence invalidates it or enforcement replaces it.

## Coverage and test strategy

Coverage has four distinct layers:

1. **Inventory and routing:** all named upstream skills and playbooks receive a disposition, and every adopted mechanism has a real candidate destination. Structural validators detect missing files, broken references and inconsistent declarations.
2. **Executable fixture controls:** good and bad artifacts must produce different results for the intended reason. Keep the existing test-integrity cases and add application/formal cases that expose stale correspondence, false atomicity or unexercised entry points.
3. **Fresh task runs:** ordinary prompts and raw project artifacts exercise relevant discovery, read timing, allowed effects, completed checks and honest reporting. A separate agent should rerun generated instructions. Include a small task that should finish without new machinery.
4. **Independent assessment:** review the exact candidate and observed artifacts, including failed attempts. Structural success, skill-name recitation or reviewer agreement does not establish behavior.

Priority scenarios are real CLI verification creation and independent reuse; application maintenance that distinguishes harness drift from a product bug; a misleading healthy-but-unusable instance; real-code formal defect detection; stale source/model correspondence; changed refactor contracts; a benchmark that skips work; and a status-only request. Preserve outcome-specific evidence and untested hosts. A finite explicit-state fixture can validate workflow behavior without proving TLA+ integration.

Use [EVALUATION.md](EVALUATION.md) for observed execution and remaining limits. This recommendation is the design rationale and complete disposition map; the evaluation record supplies the supporting behavioral evidence.

[README]: ../README.md
[Workflows]: ../engineering-workflows/SKILL.md
[Routing]: ../engineering-workflows/references/routing.md
[Methods]: ../engineering-workflows/references/methods.md
[Notes]: ../engineering-workflows/references/notes.md
[Contract]: ../engineering-workflows/references/contract.md
[Coordination]: ../engineering-workflows/references/coordination.md
[Delivery]: ../engineering-workflows/references/delivery.md
[Verify]: ../engineering-verify/SKILL.md
[Testing]: ../engineering-verify/references/testing.md
[Application]: ../engineering-verify/references/application.md
[Formal]: ../engineering-verify/references/formal.md
[Visual]: ../engineering-verify/references/methods.md
[Check]: ../engineering-check/SKILL.md
[Impact]: ../engineering-check/references/critical-review.md
[Measure]: ../engineering-measure/SKILL.md
[Measurement]: ../engineering-measure/references/measurement.md
[Arena]: ../engineering-arena/SKILL.md
[Comparison]: ../engineering-arena/references/comparison.md
[Campaign]: ../engineering-campaign/SKILL.md
[Program]: ../engineering-campaign/references/state-and-control.md
[Configure]: ../engineering-configure/SKILL.md
[Capabilities]: ../engineering-configure/references/capabilities.md
[Evaluation guidance]: ../engineering-configure/references/evaluate-and-promote.md
[Routing cases]: ../engineering-configure/references/routing-cases.md
[Pack contract]: ../engineering-workflows/references/pack-contract.json
[EW license]: ../engineering-workflows/LICENSE
