# EngineeringWorkflows

Two reusable engineering skillsets live in this repository. Choose the set that
matches **who owns the workflow**, then follow its installation path below.

| Skillset | Use it when | Source folders |
| --- | --- | --- |
| **EngineeringWorkflows** | The coding agent should own investigation, implementation, review coordination, verification, and the requested delivery outcome. | The seven `engineering-*` folders at the repository root. |
| **CodeDen dark factory** | CodeDen already owns scheduling, worktrees, pipeline transitions, review assignment, retries, and merging. Agents need methods for their assigned stages. | `codeden-dark-factory/skills/codeden-*`. |

**For installing agents:** this README is the setup entry point for either
skillset. Complete the requested installation and verification; a plan or copied
`SKILL.md` alone is not a completed installation.

## Agent installation procedure

1. **Identify the target.** Use the project path, skillset, and provider supplied
   by the user or established by the current project context. Default to a
   project-local installation. Use the original set for ordinary agent-led work
   and the CodeDen set for factory assignments. Choose `codex`, `claude`, or
   `both` from the providers the project actually uses. Ask only when a missing
   choice would change the destination or workflow; do not ask again for an
   installation the user already authorized.
2. **Inspect before writing.** Read the target's active instructions, including
   `AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, relevant nested instructions,
   and provider settings. Inspect existing skill folders and Git status.
   Preserve user edits and unrelated skills.
3. **Use a separate source checkout.** Keep this distribution outside the target
   project and outside native skill roots. Use an existing authorized checkout,
   a GitHub connector, or clone the repository with the user's existing access.
   Record its commit. Do not reset a dirty checkout to obtain the source.
4. **Install one selected set** using [EngineeringWorkflows](#install-engineeringworkflows)
   or [CodeDen](#install-codeden-dark-factory). Copy whole skill folders,
   including licenses, references, scripts, metadata, and assets.
5. **Connect the project instructions.** Preserve existing instructions and add
   the appropriate bounded routing. Do not turn both packs into competing
   automatic workflow owners.
6. **Verify files and discovery.** Run the correct structural validator, inspect
   the provider's skill discovery, and distinguish visible metadata from an
   actually read skill body. Report any unavailable runtime check accurately.
7. **Deliver the setup.** Follow the target repository's authorized commit/review
   process. Report the pack, provider roots, source commit, changed instruction
   files, checks, and remaining limitations. Installation does not authorize
   changing budgets, trust, auto-merge, deployment, or unrelated global settings.

These are repository-level instructions for Codex and Claude. A managed personal
skill directory, including ChatGPT's personal skills, has its own supported
installation mechanism; use that mechanism if personal installation was requested.
Do not treat copying files into a project as installing personal skills.

### Source and target variables

Examples use a POSIX shell and Python 3.10+. Replace the paths before running.
On Windows, use the equivalent Python executable and argument paths in your shell.

```bash
# If an appropriate checkout does not already exist:
git clone https://github.com/Vidcar/EngineeringWorkflows.git /absolute/path/to/engineering-workflows-source

EW_SOURCE="/absolute/path/to/engineering-workflows-source"
EW_PROJECT="/absolute/path/to/your-project"
EW_PROVIDER="both"

git -C "$EW_SOURCE" rev-parse HEAD
git -C "$EW_PROJECT" status --short
```

The default branch contains both sets. For a release or revision specified by
the user, obtain that exact revision and record it instead of silently taking a
different version. If access or filesystem permissions are missing, name the
specific block; do not claim installation.

## Install EngineeringWorkflows

### 1. Install all seven complete skills

| Skill | Role |
| --- | --- |
| [engineering-workflows](engineering-workflows/SKILL.md) | Own implementation, repair, investigation, planning, and mixed engineering requests. |
| [engineering-check](engineering-check/SKILL.md) | Independent assessment and actionable review findings. |
| [engineering-verify](engineering-verify/SKILL.md) | Defined behavior checks and verification assets. |
| [engineering-measure](engineering-measure/SKILL.md) | Quantitative evaluation and benchmarking. |
| [engineering-arena](engineering-arena/SKILL.md) | Explicit competing alternatives, comparison, and verified synthesis. |
| [engineering-campaign](engineering-campaign/SKILL.md) | Directly requested bounded program or queue orchestration. |
| [engineering-configure](engineering-configure/SKILL.md) | Directly requested skill-pack administration. |

Install them as siblings in each selected provider root:

| Provider | Target root |
| --- | --- |
| Codex | `<project>/.agents/skills/` |
| Claude | `<project>/.claude/skills/` |

Specialists resolve `engineering-workflows` by its exact skill name and read
the shared contract from that skill. Preserve
`engineering-workflows/references/`, its scripts, and every other folder's
resources. Preserve `assets/icon.svg` as well as `agents/openai.yaml`; the UI
metadata refers to the icon. There is no extra registry-generation step in this
pack. The provider must discover the native directories.

The following **initial-install** command preflights all destinations and refuses
existing same-name folders. It copies no files if that preflight finds a collision.
If the skills already exist, use [updates and conflicts](#updates-and-conflicts)
instead of forcing a replacement. Run while the target's skill files are idle.

```bash
python3 - "$EW_SOURCE" "$EW_PROJECT" "$EW_PROVIDER" <<'PY'
import os
import shutil
import sys
from pathlib import Path

source, project = [Path(os.path.abspath(p)) for p in sys.argv[1:3]]
provider = sys.argv[3]
roots = {"codex": ".agents/skills", "claude": ".claude/skills"}
selected = tuple(roots) if provider == "both" else (provider,)
if not selected or any(p not in roots for p in selected):
    raise SystemExit("Choose codex, claude, or both.")
names = (
    "engineering-workflows", "engineering-check", "engineering-verify",
    "engineering-measure", "engineering-arena", "engineering-campaign",
    "engineering-configure",
)

def reject_links(path):
    for item in (path, *path.parents):
        if item.is_symlink():
            raise SystemExit(f"Resolve the symlink deliberately before installing: {item}")

for directory in (source, project):
    reject_links(directory)
    if not directory.is_dir():
        raise SystemExit(f"Expected an existing directory: {directory}")
if source == project or source in project.parents or project in source.parents:
    raise SystemExit("Keep the source checkout separate from the target project.")

copies = []
for name in names:
    original = source / name
    reject_links(original)
    for required in ("SKILL.md", "LICENSE"):
        if not (original / required).is_file():
            raise SystemExit(f"Incomplete source skill: {original}")
    if any(p.is_symlink() for p in original.rglob("*")):
        raise SystemExit(f"Source skill contains a symlink: {original}")
    for choice in selected:
        destination = project / roots[choice] / name
        reject_links(destination)
        for parent in destination.parents:
            if parent.exists() and not parent.is_dir():
                raise SystemExit(f"Destination parent is not a directory: {parent}")
        if destination.exists():
            raise SystemExit(f"Already present; compare and preserve it: {destination}")
        copies.append((original, destination))

for original, destination in copies:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(original, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    print(f"Copied {original.name} to {destination}")
PY
```

This command handles a new installation, not transactional upgrades. If an I/O
failure interrupts copying, inspect the partial result against the source before
continuing; do not blindly delete or overwrite it.

### 2. Add bounded project routing

Merge the following section into the **active** project instruction file for
each selected provider. Use `AGENTS.md` for Codex unless an override is active;
use the project's active Claude instructions for Claude. Do not replace the
whole file or duplicate an existing equivalent section.

```markdown
## EngineeringWorkflows

For implementation, repair, refactoring, investigation, planning, or mixed
engineering requests, use engineering-workflows as the owner of the requested
outcome. Resolve skills by their exact names from the provider's skill catalog.

Use engineering-check for assessment-only work, engineering-verify for defined
checks, engineering-measure for quantitative evaluations, and engineering-arena
for requested competing alternatives. Supporting assignments retain the
existing owner, scope, permissions, budget, and requested endpoint.

Use engineering-campaign or engineering-configure only when the user directly
requests program orchestration or pack administration. Task size alone does not
activate them. Read shared references from the resolved engineering-workflows
skill; do not invent another task owner or bypass project rules.
```

Retain the original skill names and metadata. Campaign and Configure's
direct-user-intent condition is a routing rule, not a reason to change their
`allow_implicit_invocation` metadata.

### 3. Validate one installed provider root at a time

The resolver uses the Python standard library. The pack validator also requires
**PyYAML**. Use an existing interpreter that has it. If it is missing, create a
task-specific validation environment instead of changing application
dependencies or global Python packages:

```bash
# Optional, only if the available interpreter cannot import yaml:
python3 -m venv /absolute/path/to/ew-validation-env
/absolute/path/to/ew-validation-env/bin/python -m pip install PyYAML
```

Set `EW_VALIDATOR_PY` to that environment's Python, or to `python3` when PyYAML
is already available. Windows virtual environments use `Scripts/python.exe`.

```bash
EW_VALIDATOR_PY="python3"
EW_SKILL_ROOT="$EW_PROJECT/.agents/skills"

"$EW_VALIDATOR_PY" -B "$EW_SKILL_ROOT/engineering-workflows/scripts/resolve_skill.py" \
  engineering-workflows --root "$EW_SKILL_ROOT"

"$EW_VALIDATOR_PY" -B "$EW_SKILL_ROOT/engineering-workflows/scripts/validate_pack.py" \
  --root "$EW_SKILL_ROOT"
```

For Claude, set `EW_SKILL_ROOT="$EW_PROJECT/.claude/skills"` and repeat. If you
installed only Claude, start with that root. A successful validator reports
`valid: true`, seven skills, and an empty `errors` array; this source pack's
version is 2.1.0.

**Validate each root separately.** Do not pass both provider roots together or
combine source and destination roots: duplicate exact skill names make
resolution fail. Other unrelated skills in one root are allowed.
`resolve_skill.py` verifies name resolution; it does not register skills with
the provider. See the [pack contract](engineering-workflows/references/pack-contract.json)
and [validator](engineering-workflows/scripts/validate_pack.py).

Then inspect native discovery in a fresh provider session. A bounded read-only
task such as “Use engineering-workflows to identify this project's test commands;
do not edit files” can confirm the relevant skill is read. Record separately
whether you verified files, discovery, and invocation.

## Install CodeDen dark factory

### 1. Use the included installer

The CodeDen pack provides its own installer. Use it rather than the original
pack's copy command. Run validation from the writable target project, outside
the source distribution: the validator temporarily creates a disposable project
beneath its current working directory.

```bash
# Check the distribution and preview the target changes.
cd "$EW_PROJECT"
python3 -B "$EW_SOURCE/codeden-dark-factory/scripts/validate.py"
python3 -B "$EW_SOURCE/codeden-dark-factory/scripts/install.py" \
  --project "$EW_PROJECT" --provider "$EW_PROVIDER"

# If the preview matches the requested setup, apply it.
python3 -B "$EW_SOURCE/codeden-dark-factory/scripts/install.py" \
  --project "$EW_PROJECT" --provider "$EW_PROVIDER" --apply

# Rerun to verify that no further changes are planned.
python3 -B "$EW_SOURCE/codeden-dark-factory/scripts/install.py" \
  --project "$EW_PROJECT" --provider "$EW_PROVIDER"
```

An authorized installation does not need a second permission question just
because the installer has a preview. Inspect the preview, resolve any real
conflict, and apply the requested setup.

The installer copies all seven `codeden-*` folders into the selected native
roots, adds managed routing blocks to `AGENTS.md` and/or `CLAUDE.md`, and
creates `.codeden-engineering-skills.json` to track owned file and block hashes.
It preserves other instruction text and refuses edited managed content,
unknown collisions, symlinks, malformed markers, and a Codex install shadowed
by root `AGENTS.override.md`. Do not remove that override just to pass the
check; reconcile active instructions deliberately or use the documented manual
installation path.

The installer and validator require Python 3.10+ and its standard library.
They do not require PyYAML.

### 2. Make the installation available to the factory

1. Review the installed files and follow the target project's authorized
   commit/review process. The installation must reach its **default branch**
   before new factory worktrees are expected to contain it.
2. In CodeDen's **Agents → Skills**, select the project and check all seven
   names for the actual builder/reviewer/scout providers. Ensure they are fully
   available for automatic discovery, rather than disabled or manual-only.
3. Check the active instruction routing. It must select by the **current
   factory brief and tools**, because several factory assignments share the
   broad session role `agent`.
4. When a bounded live task is authorized, inspect its transcript for a relevant
   skill-body read and the native stage report. **What's loaded is an inventory,
   not proof of invocation.** If the request was installation only, report an
   unperformed live check instead of starting autonomous work just to claim it.

CodeDen remains responsible for its own state transitions and operational
settings. Do not copy the original EngineeringWorkflows owner-routing section
into a factory-only setup. The CodeDen templates already contain the correct
conditional routing, including ordinary manually started session behavior.

For factory prerequisites, vision guidance, recommended protection of governing
files, provider restrictions, and manual installation, read the
[CodeDen setup guide](codeden-dark-factory/README.md). Its
[source analysis](codeden-dark-factory/ANALYSIS.md) explains the seven-skill
design and native control boundaries; its
[validation record](codeden-dark-factory/VALIDATION.md) distinguishes executed
checks from untested live behavior.

## Updates and conflicts

- **Identical existing installation:** compare the complete installed folders
  with the requested source revision, verify routing and discovery, and report
  it as already installed. Do not create duplicate names.
- **Original pack update:** establish the installed source version and preserve
  local changes. Apply a reviewed source-to-source delta only to the seven
  owned folders; use a three-way comparison when needed. If the old version or
  ownership is unknown, report the concrete conflict rather than overwriting.
  Revalidate each provider root after the update.
- **CodeDen pack update:** rerun its installer. Its manifest permits updates to
  unmodified owned content and refuses local edits or removed upstream files
  that need reconciliation. Preserve the manifest; deleting it does not safely
  resolve a conflict.
- **Both packs are intentionally available:** keep original owner routing for
  ordinary agent-led work and CodeDen routing for actual factory assignments.
  Existing user/global skills may also be visible. Do not globally disable
  skills used by unrelated projects; use supported project-scoped controls or
  explicit task routing. Do not silently remove either pack.
- **Source or target access is blocked:** preserve any completed local work and
  state exactly which copy, validation, discovery, or runtime check remains
  incomplete.

## Completion report for the installing agent

Return a concise report with:

- Selected skillset, provider(s), target project, and source commit.
- Installed paths and instruction files changed, or an already-current result.
- Structural validation commands and actual outcomes.
- Whether provider discovery and a skill-body invocation were observed.
- Any conflict, unavailable dependency, or unperformed live check.
- Actual delivery state: local changes, commit, branch, or merged setup, as
  applicable to the user's authorized endpoint.

Do not equate a copied folder, a successful validator, a visible catalog entry,
and an invoked skill. They are different observations.

## License

Preserve the `LICENSE` file in every distributed skill. The original
[EngineeringWorkflows license](engineering-workflows/LICENSE) credits Lauren Tan
and Matt Pocock; the [CodeDen adaptation](codeden-dark-factory/LICENSE) retains
those notices. The adaptation is independent of CodeDen and the upstream authors.
