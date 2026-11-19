# Engineering skills for CodeDen dark factory

A reusable project skill pack derived from **EngineeringWorkflows 2.1.0**.
CodeDen runs the factory; these skills improve the engineering judgment inside
its assignments.

**Seven skills, two provider layouts, one installer.** The core principles are
observable acceptance, diagnosis before implementation, independent review,
meaningful behavioral evidence, current verification, bounded work, preserved
compatibility, and truthful handoffs.

Read [the source analysis](ANALYSIS.md) for the full design and
[the validation record](VALIDATION.md) for what was actually checked.

## What you get

| Skill | Native assignment | Result |
| --- | --- | --- |
| [codeden-scout](skills/codeden-scout/SKILL.md) | Scout planning/filing or discovery area review | Evidence-backed, deduplicated work tied to the vision; native round/report/issue tools. |
| [codeden-investigate](skills/codeden-investigate/SKILL.md) | Bug Reproduce or feature Analyze | A demonstrated reproduction or sound spec/decision before implementation. |
| [codeden-build](skills/codeden-build/SKILL.md) | Implement, fix, docs, Revise, explicit rebuild | A coherent change, current evidence, PR, and native finish. |
| [codeden-review](skills/codeden-review/SKILL.md) | Independent PR review or narrow re-check | Criterion-by-criterion judgment and a consistent native verdict. |
| [codeden-integrate](skills/codeden-integrate/SKILL.md) | Explicit rebase, CI kick, revert, post-revert recovery | The narrowly assigned recovery action with refreshed evidence. |
| [codeden-verify](skills/codeden-verify/SKILL.md) | Evidence work inside an existing stage | Independent oracles, real-path checks, and accurate pass/fail/blocked/untested claims. |
| [codeden-measure](skills/codeden-measure/SKILL.md) | A necessary quantitative comparison | Comparable conditions, correctness gates, variability, and a bounded conclusion. |

The first five skills follow native assignments. Verify and Measure are
supporting methods; they never create another factory stage or reviewer.
A short PM clause in the project instructions supplies exception-decision
discipline without adding another PM skill.

Each skill is a complete, real directory with a lean `SKILL.md`, optional-provider
UI metadata in `agents/openai.yaml`, and the preserved upstream `LICENSE`.
No skill depends on this ChatGPT session or an installed EngineeringWorkflows
catalog.

## Install in a project

Use Python 3.10 or later. No Python packages or network requests are required
by the installer. Keep this distribution outside the target project and run it
while nobody else is editing the target's instruction or skill files.

From the `codeden-dark-factory` directory in your checked-out distribution:

```bash
# Preview the exact destination files; writes nothing.
python3 scripts/install.py --project /absolute/path/to/your-project --provider both

# Apply that installation.
python3 scripts/install.py --project /absolute/path/to/your-project --provider both --apply
```

Use `--provider codex` or `--provider claude` when only one provider is needed.
Use `both` when builder/reviewer/scout selection or fallback can use either.
The source text is portable, but this release's installation paths are verified
for CodeDen's Codex and Claude integration; other providers need a separate
native-loading check.

The installation creates:

| Destination | Purpose |
| --- | --- |
| `.agents/skills/codeden-*/` | Complete Codex-native skill directories. |
| `.claude/skills/codeden-*/` | Complete Claude-native skill directories. |
| `AGENTS.md` | One managed Codex routing block, appended to existing text. |
| `CLAUDE.md` | One managed Claude routing block, appended to existing text. |
| `.codeden-engineering-skills.json` | Installed-file and routing-block hashes for safe reruns/upgrades. |

Only selected providers' directories and instruction files are written.
The installer preflights the whole change, refuses unknown collisions and edited
managed content, and uses atomic file replacement with rollback on an ordinary
write failure. It preserves text outside its managed blocks. It refuses symlink
paths, malformed blocks, and a Codex installation shadowed by root
`AGENTS.override.md`. This is a conservative installer; there is no force mode.

A rerun with the same pack changes nothing. An upgrade replaces only unmodified
files it owns. If you customized a skill or the managed routing, reconcile those
edits deliberately before upgrading. Keep project-specific commands/rules in
your existing instructions outside the managed block. Removed upstream files
are reported for manual review rather than silently deleted.

For a manual installation, copy the complete desired skill directories to the
corresponding native root, then merge the appropriate
[Codex](templates/AGENTS.block.md) or [Claude](templates/CLAUDE.block.md) routing
body into your active project instructions. Manual copies are not automatically
adopted by the installer's ownership manifest. Preserve every skill's license.

## Activate it in CodeDen

1. **Review the generated project changes and commit them through your normal
   setup process.** Get them onto the project's default branch before starting
   new factory worktrees. A file present only in the main checkout is not enough
   for future Git worktrees. Do not alter an in-flight worker's instructions
   behind its current task.
2. In **Agents → Skills**, select the project and check that the seven names
   appear for the providers you use. Enable full automatic discovery. Claude's
   `name-only` or `user-invocable-only` state is not equivalent to ordinary
   automatic availability. A Codex disable rule by skill name can apply across
   worktrees.
3. Confirm the active project instructions contain the routing block. Resolve
   overriding/nested instructions deliberately. The installer does not edit
   global settings or provider preferences.
4. Start a bounded task with automatic merging off and inspect the transcript
   for the relevant `SKILL.md` read and the correct native report/tool result.
   **What's loaded is an inventory, not proof that a skill body was used.**
5. Check a bug investigation, a small feature, and a reviewer task before relying
   on unattended operation. The rollout checks below are suggestions, not an
   additional skill-owned workflow.

CodeDen does not expose a per-factory-role skill selector in the inspected
version. The installed routing selects by the **current brief and tools**.
Scout, lens, builder, reviewer, and integrator all have the broad role `agent`.
A manually started session in a dark-factory project is not automatically an
unattended factory task.

These integration facts are grounded in
[agent configuration](https://github.com/leonvanzyl/codeden/blob/911551159b30ae44367c1cea5f2ba3fa9f755346/docs/agent-config.md),
[session creation](https://github.com/leonvanzyl/codeden/blob/911551159b30ae44367c1cea5f2ba3fa9f755346/apps/server/src/services/factory/sessions.ts),
and [unattended handling](https://github.com/leonvanzyl/codeden/blob/911551159b30ae44367c1cea5f2ba3fa9f755346/apps/server/src/services/factory/unattended.ts).

## Set the project quality bar

Keep concrete project facts in existing project guidance: setup/check commands,
how to exercise a real user/API path, state/data assumptions, compatibility
promises, and costly failure modes. Keep the product goals and exclusions in
the native vision. The skills should not invent these facts.

An example addition to the vision's existing **Quality bar** section:

```markdown
## Quality bar
- Each behavioral acceptance criterion has identifiable evidence.
- Bug repairs preserve a regression test where practical and show the original failure.
- Verification identifies the tested revision and material environment limits.
- Changes preserve the documented public contract and account/data isolation.
- The independent review distinguishes blockers from optional follow-ups.
- Quantitative improvement claims preserve correctness and report comparable measurements.
```

Adapt that to your project; do not duplicate or replace unrelated vision
sections. Instructions in the vision and skills remain agent guidance.
Actual CI, trust, protection, spending, review, and merge settings remain
CodeDen's enforcement mechanisms.

### Keep governing instructions under deliberate control

CodeDen automatically protects its `.codeden/` folder, the vision, and license
files. Agent instruction paths are excluded from its docs-only shortcut, but
are not all automatically protected from automatic merging. If you want policy
changes to require your review, add these paths to **Protected paths** or the
vision's **Protected areas** using the normal operator setup:

```markdown
- `.agents/**`
- `.claude/**`
- `.codex/**`
- `AGENTS.md`
- `AGENTS.override.md`
- `CLAUDE.md`
- `.codeden-engineering-skills.json`
```

Add nested instruction paths used by your project. The installer does not change
these protections for you. The initial installation itself includes license and
governing files, so handle it as an operator setup change.

Source:
[path policy](https://github.com/leonvanzyl/codeden/blob/911551159b30ae44367c1cea5f2ba3fa9f755346/apps/server/src/services/factory/policy.ts).

## Suggested operating choices

These are rollout recommendations, separate from the skill content:

- Start with auto-merge off, real PR CI, a useful audit command, an explicit
  daily budget, and an item budget appropriate to one task.
- Keep discovery small enough that you can inspect outcomes. The built-in
  work-in-progress limit already prioritizes finishing work.
- Choose strict merging when changes interact strongly or you require CI on
  the updated base. Fast mode can merge a behind-base PR on its own green CI;
  the skills cannot turn that into proof of the combined state.
- Observe whether criteria, evidence, and review findings are useful before
  raising throughput. A longer transcript or more tests is not itself quality.
- Use native lessons for demonstrated reusable observations. Promote deliberate
  policy changes through project instructions; do not have workers rewrite
  their governing skills after each task.

Dark mode alone does **not** enable automatic merging. It requires a GitHub
project, a vision and a daily budget. Auto-merge and deployment permission are
separate, default-off settings. See
[mode/limit contracts](https://github.com/leonvanzyl/codeden/blob/911551159b30ae44367c1cea5f2ba3fa9f755346/packages/contracts/src/factory.ts)
and [factory prerequisites](https://github.com/leonvanzyl/codeden/blob/911551159b30ae44367c1cea5f2ba3fa9f755346/docs/software-factory.md#L273-L287).

## What changed from EngineeringWorkflows

| Original responsibility | Where it belongs here |
| --- | --- |
| One owner of the outcome | CodeDen owns lifecycle; assigned agent owns its stage deliverable. |
| Workflows implementation and diagnosis | Investigate, Build, and narrowly assigned Integrate. |
| Check | The existing independent reviewer uses Review. |
| Verify | Evidence method inside the current role and permission boundary. |
| Measure | Optional quantitative method with correctness first. |
| Arena | Bounded comparison in investigation/measurement; no nested team by default. |
| Campaign | Native factory scheduling, slots, queues, limits, retries and stop controls. |
| Configure | Operator setup of native skills/settings; no runtime policy administration. |
| Shared custom state and delivery loops | Native issue/item/spec/reproduction/verdict/PR/evidence records. |

The adaptation preserves the principles while moving lifecycle machinery to
the host that already implements it. The current factory brief always controls
special cases: narrow missing-head fetches, exact reverts, environment-only
review returns, and explicit rebuild/post-revert branches.

## Validate or maintain the pack

```bash
python3 -B scripts/validate.py
python3 -B scripts/test_install.py
```

Static validation establishes structure and routing consistency, not model
compliance. Installer tests establish local file behavior. The recorded offline
agent trials establish several important behaviors under their supplied tasks.
No live CodeDen/model run, project CI, GitHub merge, or deployment was exercised
as part of this pack's validation.

## Provenance and license

Analyzed on **19 November 2026**:

- CodeDen: `leonvanzyl/codeden@911551159b30ae44367c1cea5f2ba3fa9f755346`.
- EngineeringWorkflows: `Vidcar/EngineeringWorkflows@e8ae675031320195b0ef3a827adfd05b782909f0`,
  declared pack version 2.1.0.

[pack.json](pack.json) pins those sources. This adaptation is independent of
CodeDen and the upstream skill authors. The original EngineeringWorkflows MIT
notice, including its compilation attribution and copyright notices for Lauren
Tan and Matt Pocock, is preserved in [LICENSE](LICENSE) and every distributed
skill. Source code evolves; recheck native tool contracts and loading behavior
when upgrading CodeDen.
