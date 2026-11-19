#!/usr/bin/env python3
"""Behavior checks for installation into disposable projects; no network or Git calls."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("install.py").absolute()
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("codeden_skill_installer", SCRIPT)
assert spec and spec.loader
installer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = installer
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        # Keep all fixture writes under the caller's workspace, not a home directory.
        self.temporary = tempfile.TemporaryDirectory(prefix="installer-test-", dir=Path.cwd())
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "distribution"
        self.project = self.root / "project"
        self.project.mkdir()
        (self.project / ".git").mkdir()
        (self.source / "scripts").mkdir(parents=True)
        shutil.copyfile(SCRIPT, self.source / "scripts/install.py")
        for name in ("factory-alpha", "factory-beta"):
            self.source_write(f"skills/{name}/SKILL.md", f"---\nname: {name}\ndescription: A focused factory method\n---\n\nRead references/check.md.\n")
            self.source_write(f"skills/{name}/LICENSE", "MIT fixture license\n")
            self.source_write(f"skills/{name}/references/check.md", "Check the assigned behavior.\n")
        self.source_write("skills/factory-alpha/assets/sample.bin", b"\x00\xff\x80\n")
        self.source_write("templates/AGENTS.block.md", "## Factory routing\n\nRead .agents/skills/factory-alpha/SKILL.md.\n")
        self.source_write("templates/CLAUDE.block.md", "## Factory routing\n\nRead .claude/skills/factory-alpha/SKILL.md.\n")

    def source_write(self, path: str, data: str | bytes):
        destination = self.source / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data.encode() if isinstance(data, str) else data)

    def project_write(self, path: str, data: str | bytes):
        destination = self.project / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data.encode() if isinstance(data, str) else data)

    def plan(self, providers=("codex", "claude")):
        return installer.make_plan(self.source, self.project, providers)

    def install(self, providers=("codex", "claude")):
        plan = self.plan(providers)
        installer.apply_plan(plan)
        return plan

    def snapshot(self):
        return {p.relative_to(self.project).as_posix(): p.read_bytes()
                for p in self.project.rglob("*") if p.is_file()}

    def command(self, *args):
        return subprocess.run(
            [sys.executable, str(self.source / "scripts/install.py"), "--project", str(self.project), *args],
            text=True, capture_output=True, check=False,
        )

    def test_cli_defaults_to_dry_run_with_no_changes(self):
        self.project_write("AGENTS.md", "Existing instructions.\n")
        before = self.snapshot()
        result = self.command()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry run", result.stdout)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / installer.MANIFEST).exists())

    def test_both_providers_copy_complete_real_directories_and_preserve_instructions(self):
        self.project_write("AGENTS.md", b"# Existing Codex instructions\r\n\r\nKeep my conventions.\r\n")
        self.project_write("CLAUDE.md", "# Existing Claude instructions\nKeep my conventions.")
        before = self.snapshot()
        result = self.command("--provider", "both", "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        for target in (".agents", ".claude"):
            for source in (self.source / "skills").rglob("*"):
                relative = source.relative_to(self.source / "skills")
                copied = self.project / target / "skills" / relative
                self.assertFalse(copied.is_symlink())
                if source.is_file():
                    self.assertEqual(source.read_bytes(), copied.read_bytes())
                else:
                    self.assertTrue(copied.is_dir())
        for filename in ("AGENTS.md", "CLAUDE.md"):
            data = (self.project / filename).read_bytes()
            self.assertTrue(data.startswith(before[filename]))
            self.assertEqual(data.count(installer.BEGIN.encode()), 1)
            self.assertEqual(data.count(installer.END.encode()), 1)
        self.assertIn(b"\r\n" + installer.BEGIN.encode() + b"\r\n", (self.project / "AGENTS.md").read_bytes())
        manifest = json.loads((self.project / installer.MANIFEST).read_bytes())
        self.assertEqual(set(manifest["providers"]), {"codex", "claude"})
        self.assertFalse((self.project / ".codeden").exists())

    def test_rerun_is_idempotent_including_manifest(self):
        self.install()
        before = self.snapshot()
        mtimes = {p: (self.project / p).stat().st_mtime_ns for p in before}
        self.assertEqual(self.plan().writes, [])
        result = self.command("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Already up to date", result.stdout)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual({p: (self.project / p).stat().st_mtime_ns for p in before}, mtimes)

    def test_collision_in_second_provider_causes_no_partial_install(self):
        self.project_write("AGENTS.md", "My original instructions\n")
        self.project_write(".claude/skills/factory-beta/SKILL.md", "A separately maintained skill\n")
        before = self.snapshot()
        result = self.command("--apply")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Unowned skill folder", result.stderr)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / installer.MANIFEST).exists())

    def test_edits_to_installed_skill_are_preserved_and_refused(self):
        self.install()
        self.project_write(".agents/skills/factory-alpha/SKILL.md", "My deliberate edits\n")
        self.source_write("skills/factory-beta/references/check.md", "New upstream guidance\n")
        before = self.snapshot()
        with self.assertRaisesRegex(installer.InstallError, "Owned file was edited"):
            self.plan()
        self.assertEqual(self.snapshot(), before)

    def test_edits_to_owned_routing_are_preserved_and_refused(self):
        self.install()
        path = self.project / "AGENTS.md"
        path.write_text(path.read_text().replace("## Factory routing", "## My revised factory routing"))
        before = self.snapshot()
        with self.assertRaisesRegex(installer.InstallError, "Owned routing block was edited"):
            self.plan()
        self.assertEqual(self.snapshot(), before)

    def test_unmodified_upgrade_preserves_unselected_provider_and_external_prose(self):
        self.project_write("AGENTS.md", "Original prefix\n")
        self.install()
        original_claude = (self.project / ".claude/skills/factory-alpha/SKILL.md").read_bytes()
        previous_manifest = json.loads((self.project / installer.MANIFEST).read_bytes())
        path = self.project / "AGENTS.md"
        path.write_bytes(b"New preface\n" + path.read_bytes() + b"\nNew suffix\n")
        self.source_write("skills/factory-alpha/SKILL.md", "---\nname: factory-alpha\ndescription: Updated method\n---\nUpdated guidance.\n")
        self.source_write("skills/factory-alpha/references/new.md", "New reference\n")
        self.source_write("templates/AGENTS.block.md", "Updated routing, with the same native boundary.\n")
        self.install(("codex",))
        manifest = json.loads((self.project / installer.MANIFEST).read_bytes())
        self.assertEqual(manifest["providers"]["claude"], previous_manifest["providers"]["claude"])
        self.assertEqual((self.project / ".claude/skills/factory-alpha/SKILL.md").read_bytes(), original_claude)
        self.assertIn(b"Updated guidance", (self.project / ".agents/skills/factory-alpha/SKILL.md").read_bytes())
        self.assertTrue((self.project / ".agents/skills/factory-alpha/references/new.md").is_file())
        self.assertTrue(path.read_bytes().startswith(b"New preface\nOriginal prefix\n"))
        self.assertTrue(path.read_bytes().endswith(b"\nNew suffix\n"))

    def test_destination_symlink_escape_is_refused(self):
        outside = self.root / "outside"
        outside.mkdir()
        try:
            (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("This environment cannot create symlinks")
        with self.assertRaisesRegex(installer.InstallError, "Symlinks"):
            self.plan()
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / installer.MANIFEST).exists())

    def test_source_skill_symlink_is_refused(self):
        outside = self.root / "outside"
        outside.mkdir()
        try:
            (self.source / "skills/factory-linked").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("This environment cannot create symlinks")
        with self.assertRaisesRegex(installer.InstallError, "Symlinks"):
            self.plan()
        self.assertEqual(self.snapshot(), {})

    def test_invalid_or_unowned_markers_are_refused_without_writes(self):
        cases = (
            installer.BEGIN + "\nNo end\n",
            installer.END + "\n" + installer.BEGIN + "\n",
            installer.BEGIN + "\n" + installer.BEGIN + "\n" + installer.END + "\n",
            "inline " + installer.BEGIN + "\n" + installer.END + "\n",
            installer.BEGIN + "\nUnowned block\n" + installer.END + "\n",
        )
        for text in cases:
            with self.subTest(text=text):
                self.project_write("CLAUDE.md", text)
                before = self.snapshot()
                with self.assertRaises(installer.InstallError):
                    self.plan()
                self.assertEqual(self.snapshot(), before)
                self.assertFalse((self.project / ".agents").exists())

    def test_source_removal_is_reported_without_deleting_owned_files(self):
        self.install()
        before = self.snapshot()
        (self.source / "skills/factory-alpha/assets/sample.bin").unlink()
        with self.assertRaisesRegex(installer.InstallError, "Source removed"):
            self.plan()
        self.assertEqual(self.snapshot(), before)

    def test_codex_override_refuses_shadowed_install_but_does_not_block_claude(self):
        self.project_write("AGENTS.override.md", "Active Codex instructions\n")
        with self.assertRaisesRegex(installer.InstallError, "shadows"):
            self.plan(("codex",))
        self.install(("claude",))
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertTrue((self.project / "CLAUDE.md").is_file())

    def test_manifest_cannot_claim_paths_outside_provider_skill_root(self):
        self.install()
        path = self.project / installer.MANIFEST
        manifest = json.loads(path.read_bytes())
        manifest["providers"]["codex"]["files"]["../outside.txt"] = "0" * 64
        path.write_text(json.dumps(manifest))
        before = self.snapshot()
        with self.assertRaisesRegex(installer.InstallError, "Unsafe relative path"):
            self.plan()
        self.assertEqual(self.snapshot(), before)

    def test_edit_after_preview_prevents_apply(self):
        self.project_write("AGENTS.md", "Before preview\n")
        plan = self.plan()
        self.project_write("AGENTS.md", "Edit made after preview\n")
        before = self.snapshot()
        with self.assertRaisesRegex(installer.InstallError, "Destination changed after preview"):
            installer.apply_plan(plan)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.project / ".agents").exists())

    def test_write_failure_rolls_back_owned_mutations(self):
        self.project_write("AGENTS.md", "Instructions that must survive\n")
        before = self.snapshot()
        plan = self.plan()
        replace = installer.os.replace
        calls = 0

        def fail_once(source, target):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("simulated full disk")
            return replace(source, target)

        with patch.object(installer.os, "replace", side_effect=fail_once):
            with self.assertRaisesRegex(installer.InstallError, "rolled back"):
                installer.apply_plan(plan)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / installer.LOCK).exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
