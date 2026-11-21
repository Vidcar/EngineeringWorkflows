# Engineering Workflows

Seven agent skills for carrying software work from a clear goal to a verified result.
The pack is based on [v2.1.0 at `e8ae675`](https://github.com/Vidcar/EngineeringWorkflows/commit/e8ae675031320195b0ef3a827adfd05b782909f0),
with directory-symlink support in the skill resolver.

## Skills and routing

| Skill | Use it for |
| --- | --- |
| [engineering-workflows](engineering-workflows/SKILL.md) | Implementing, repairing, refactoring, investigating, or planning software work. Owns mixed tasks through their requested finish. |
| [engineering-check](engineering-check/SKILL.md) | Reviewing a change or assessing readiness without editing the target. |
| [engineering-verify](engineering-verify/SKILL.md) | Running defined checks or creating verification assets. |
| [engineering-measure](engineering-measure/SKILL.md) | Designing benchmarks and evaluating quantitative results. |
| [engineering-arena](engineering-arena/SKILL.md) | Producing independent alternatives and judging them against one rubric. |
| [engineering-campaign](engineering-campaign/SKILL.md) | Coordinating a bounded engineering program when directly requested. |
| [engineering-configure](engineering-configure/SKILL.md) | Inspecting or changing the skill pack and supported role preferences when directly requested. |

Install all seven folders together. The specialist skills resolve
`engineering-workflows` by its exact skill name and share its
[operating contract](engineering-workflows/references/contract.md).
One lead owns the outcome; specialists receive bounded assignments.

Campaign and Configure require direct user intent, including an ordinary
natural-language request. Task size or routine capability discovery alone does
not select them.

## Agent setup

### 1. Get the pack and validation tools

You need an agent host that supports skill folders, Git with access to this
repository, and Python 3.9 or newer. The validator and pack tests also require
PyYAML. The skills use the models, tools, credentials, and delegation capabilities
already available in the host.

The commands below use a POSIX shell, such as Bash on Linux, macOS, or WSL.

```bash
git clone https://github.com/Vidcar/EngineeringWorkflows.git
cd EngineeringWorkflows
ENGINEERING_PACK_SRC="$(pwd)"

python3 -m venv ../engineering-workflows-venv
. ../engineering-workflows-venv/bin/activate
python -m pip install PyYAML

python engineering-workflows/scripts/validate_pack.py --root .
```

Keep the checkout in a stable location if you choose a linked installation.
The virtual environment lives beside the checkout so it stays out of the pack.

### 2. Choose the host and installation scope

Set `ENGINEERING_SKILLS_DIR` to one destination:

| Host | Project scope | Personal scope |
| --- | --- | --- |
| Codex CLI / IDE | `/absolute/path/to/project/.agents/skills` | `$HOME/.agents/skills` |
| Claude Code | `/absolute/path/to/project/.claude/skills` | `$HOME/.claude/skills` |

These are local installation locations from the official
[Codex skill documentation](https://developers.openai.com/codex/skills) and
[Claude Code skill documentation](https://code.claude.com/docs/en/skills).
For a hosted agent or another product, use that host's supported skill
installation mechanism and register all seven skills. A local installation
applies only where those files are accessible to the host.

For example, to install for your personal Codex environment:

```bash
ENGINEERING_SKILLS_DIR="$HOME/.agents/skills"
ENGINEERING_INSTALL_MODE="link"
```

Use `link` for a local installation that follows your checkout: updating the
checkout updates the linked skills. Both Codex and Claude Code support skill
directory symlinks. Use `copy` for a self-contained installation, a shared project,
or a host that cannot access symlink targets. Absolute links into your home
directory are specific to your machine; copy the folders when committing them
for a team.

### 3. Install complete skill directories

Run this in the same shell after setting the variables above. It checks all
seven destination names before creating anything and stops if any already exist,
including broken links. Review an existing installation before replacing it.

```bash
python - "$ENGINEERING_PACK_SRC" "$ENGINEERING_SKILLS_DIR" "$ENGINEERING_INSTALL_MODE" <<'PY'
import json
import shutil
import sys
from pathlib import Path

source = Path(sys.argv[1]).expanduser().resolve()
destination = Path(sys.argv[2]).expanduser().resolve()
mode = sys.argv[3]
if mode not in {"link", "copy"}:
    raise SystemExit("Installation mode must be 'link' or 'copy'.")

manifest = json.loads(
    (source / "engineering-workflows/references/pack-contract.json").read_text()
)
names = [skill["name"] for skill in manifest["skills"]]
conflicts = [
    str(destination / name) for name in names
    if (destination / name).exists() or (destination / name).is_symlink()
]
if conflicts:
    raise SystemExit("Existing destinations; nothing changed:\n" + "\n".join(conflicts))

destination.mkdir(parents=True, exist_ok=True)
for name in names:
    if mode == "link":
        (destination / name).symlink_to(source / name, target_is_directory=True)
    else:
        shutil.copytree(
            source / name, destination / name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
print(f"Installed {len(names)} skills in {destination} using {mode}.")
PY
```

Each installed skill must contain its full `SKILL.md`, supporting references,
scripts where present, metadata, assets, and license. The repository root is a
collection of skills; it is not itself a single installable skill.

The resolver follows directory symlinks and resolves skill names to canonical
directories. Multiple links to the same directory count as one installation.
Distinct directories declaring the same skill name remain an error. Directory
cycles are bounded, and a symlink to an individual `SKILL.md` is not accepted:
link the whole skill directory.

### 4. Verify the installed files

```bash
python "$ENGINEERING_SKILLS_DIR/engineering-workflows/scripts/resolve_skill.py" \
  engineering-workflows --root "$ENGINEERING_SKILLS_DIR"

python "$ENGINEERING_SKILLS_DIR/engineering-workflows/scripts/validate_pack.py" \
  --root "$ENGINEERING_SKILLS_DIR"

ENGINEERING_PACK_TEST_ROOT="$ENGINEERING_SKILLS_DIR" \
  python -m unittest discover \
  -s "$ENGINEERING_SKILLS_DIR/engineering-workflows/scripts" \
  -p 'test_*.py' -v
```

A successful validation reports `"valid": true`, `"skill_count": 7`,
`"version": "2.1.0"`, and an empty `errors` list. These checks cover files,
schemas, references, and declared routing. Host registration and live agent
behavior need the separate check below.

The `--root` option is repeatable when you need to inspect more than one active
skill location. Two copied installations of the same skill are duplicates even
if their contents match. Validate the source checkout and copied installation
separately; add multiple roots deliberately when diagnosing duplicates.

### 5. Check discovery and try a small task

Open the project in your host and check that all seven skills appear in its
catalog. If the list is stale, refresh or reopen the skill selector, or start a
fresh session.

In Codex CLI or the IDE extension, select a skill with `/skills` or mention it
with `$`:

```text
$engineering-workflows Explain this repository's structure and available checks.
Do not change files or settings.
```

In Claude Code, invoke the skill with a slash command:

```text
/engineering-workflows Explain this repository's structure and available checks.
Do not change files or settings.
```

Check that the agent reads the selected skill and shared contract, respects the
read-only scope, and reports any unavailable capabilities. For more routing
examples, see the [routing and scope probes](engineering-configure/references/routing-cases.md).

## Working on this repository

The repository contains Markdown instructions, YAML metadata, a JSON pack
contract, and Python validation/helpers. Read the relevant `SKILL.md` and shared
contract before changing behavior. Keep the skill names, references, and
[pack contract](engineering-workflows/references/pack-contract.json) consistent.

With the validation environment activated, run these from the repository root:

```bash
python engineering-workflows/scripts/validate_pack.py --root .
python -m unittest discover -s engineering-workflows/scripts -p 'test_*.py' -v
```

The tests exercise the resolver, Git snapshot helper, pack structure, and
rejection of invalid declarations. For changes to routing or execution policy,
also exercise the affected task in the real host; passing structural checks
does not establish behavioral correctness.

If you install the pack into this checkout's own host directory, use links.
Copied skills nested inside the source tree create duplicate active skill names
when validating the source root.

## Updating and troubleshooting

For a linked installation, review local edits, update the checkout with
`git pull --ff-only`, and rerun validation against `ENGINEERING_SKILLS_DIR`.
Links expose local edits immediately; use a stable checkout for everyday work.
If you move or delete the checkout, recreate the links at the new location.

For a copied installation, keep a backup outside all active skill roots, replace
only this pack's seven folders with complete copies, and rerun validation and
the host discovery check. The install snippet deliberately stops on existing
destinations instead of merging versions.

| Symptom | Check |
| --- | --- |
| Repository cannot be cloned | Confirm your Git credentials can access `Vidcar/EngineeringWorkflows`. |
| `Pack validation needs PyYAML` | Activate the virtual environment and install PyYAML using that environment's `python -m pip`. |
| Resolver reports `found 0` | Confirm the selected root, the complete skill directory, and any link target exist and are readable. Link directories, not individual `SKILL.md` files. |
| Resolver reports `found 2` or more | Inspect active roots for distinct copies with the same frontmatter name; move retired copies outside active roots. |
| Validation passes but the host cannot find a skill | Check the host's catalog, installation scope, filesystem access, and enabled-skill settings. |
| Agent cannot delegate or run a tool | Check capabilities actually exposed by the host. Installing this pack does not provision extra capabilities. |

## License

Each skill includes an [MIT license](engineering-workflows/LICENSE) with attribution
to Lauren Tan and Matt Pocock. Preserve those notices when copying or
redistributing the pack.
