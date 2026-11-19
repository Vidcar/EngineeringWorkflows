#!/usr/bin/env python3
"""Check pack structure and provider routing; this does not prove agent behavior."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import tempfile

from install import make_plan, apply_plan, MANIFEST


EXPECTED = {
    "codeden-scout", "codeden-investigate", "codeden-build", "codeden-review",
    "codeden-integrate", "codeden-verify", "codeden-measure",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(root: Path) -> list[str]:
    metadata = json.loads((root / "pack.json").read_text(encoding="utf-8"))
    require(set(metadata["skills"]) == EXPECTED, "Pack metadata must name the seven skills")
    require(metadata["schema"] == 1, "Unknown pack metadata schema")
    require(set(metadata["providers"]) == {"codex", "claude"}, "Unexpected provider list")
    for source in metadata["sources"].values():
        require(re.fullmatch(r"[0-9a-f]{40}", source["commit"]) is not None,
                "Source identity must be pinned to a full commit")
    folders = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    require(folders == EXPECTED, "The actual skill folders differ from the declared set")
    license_bytes = (root / "LICENSE").read_bytes()
    summaries = []
    for name in sorted(EXPECTED):
        folder = root / "skills" / name
        require(not folder.is_symlink(), f"Skill must be a real directory: {name}")
        text = (folder / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", text)
        require(match is not None, f"Expected simple single-line metadata: {name}")
        assert match is not None
        require(match[1] == name and len(name) <= 64, f"Invalid skill name: {name}")
        description = json.loads(match[2])
        require(isinstance(description, str) and 1 <= len(description) <= 1024,
                f"Invalid description: {name}")
        require("<" not in description and ">" not in description,
                f"Description contains angle brackets: {name}")
        require(len(text.splitlines()) < 500, f"Skill exceeds the intended body limit: {name}")
        require("TODO" not in text and "[INSERT" not in text,
                f"Unresolved placeholder: {name}")
        require((folder / "LICENSE").read_bytes() == license_bytes,
                f"Source license not preserved: {name}")
        ui = (folder / "agents" / "openai.yaml").read_text(encoding="utf-8")
        for key in ("display_name", "short_description", "default_prompt"):
            found = re.search(rf'^  {key}: ("[^\n]*")$', ui, flags=re.MULTILINE)
            require(found is not None, f"Missing quoted interface field {key}: {name}")
            assert found is not None
            value = json.loads(found[1])
            if key == "short_description":
                require(25 <= len(value) <= 64, f"Invalid UI short description length: {name}")
            if key == "default_prompt":
                require("$" + name in value, f"Default prompt must name the skill: {name}")
        summaries.append(f"{name}: metadata, license, UI fields, {len(text.split())} words")

    for file, prefix in (("AGENTS.block.md", ".agents/skills"),
                         ("CLAUDE.block.md", ".claude/skills")):
        text = (root / "templates" / file).read_text(encoding="utf-8")
        require("SKILL_ROOT" not in text, f"Unresolved provider placeholder: {file}")
        for name in EXPECTED:
            require(f"{prefix}/{name}/SKILL.md" in text,
                    f"Missing provider routing: {file}: {name}")
        wrong = ".claude/skills" if prefix == ".agents/skills" else ".agents/skills"
        require(wrong not in text, f"Wrong provider root in {file}")

    # Exercise the actual distribution, beyond the installer's smaller test fixtures.
    # Keep temporary projects outside the distribution and remove them on completion.
    with tempfile.TemporaryDirectory(prefix="codeden-pack-check-", dir=Path.cwd()) as temp:
        project = Path(temp)
        existing = b"# Existing project rules\n\nPreserve account isolation.\n"
        (project / "AGENTS.md").write_bytes(existing)
        plan = make_plan(root, project, ("codex", "claude"))
        require(not (project / ".agents").exists(), "Preview unexpectedly wrote files")
        apply_plan(plan)
        require((project / "AGENTS.md").read_bytes().startswith(existing),
                "Installation changed existing project instructions")
        for provider_root in (".agents/skills", ".claude/skills"):
            for name in EXPECTED:
                for source in (root / "skills" / name).rglob("*"):
                    if source.is_file():
                        copied = project / provider_root / name / source.relative_to(root / "skills" / name)
                        require(copied.is_file() and not copied.is_symlink(),
                                f"Missing real installed file: {copied}")
                        require(copied.read_bytes() == source.read_bytes(),
                                f"Installed bytes differ: {copied}")
        require((project / MANIFEST).is_file(), "Ownership manifest is missing")
        require(not make_plan(root, project, ("codex", "claude")).writes,
                "Rerunning the actual distribution is not idempotent")
    summaries.append("Actual-pack smoke: both providers, preserved instructions, exact bytes, idempotence")
    return summaries


def main() -> int:
    root = Path(__file__).absolute().parents[1]
    try:
        for summary in validate(root):
            print("PASS " + summary)
        print("Structural validation passed. Live skill invocation and factory behavior are not tested here.")
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
