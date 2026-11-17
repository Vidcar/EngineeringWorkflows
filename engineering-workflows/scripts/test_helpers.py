#!/usr/bin/env python3
"""Behavioral checks for read-only Git identity and exact skill resolution."""
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from snapshot import capture
from resolve_skill import resolve


def command(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        # Git writes are confined to this disposable repository, never the pack.
        self.temp = tempfile.TemporaryDirectory(prefix="engineering-snapshot-test-")
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        command(self.repo, "init", "-q")
        command(self.repo, "config", "user.email", "fixture@example.invalid")
        command(self.repo, "config", "user.name", "Fixture")
        (self.repo / "app.txt").write_text("original\n")
        (self.repo / ".gitignore").write_text("cache/\n")
        command(self.repo, "add", ".")
        command(self.repo, "commit", "-qm", "baseline")
        self.start = capture(self.repo)

    def tearDown(self):
        self.temp.cleanup()

    def test_unchanged_snapshot_is_stable(self):
        self.assertEqual(capture(self.repo), self.start)

    def test_named_comparison_base_moving_changes_identity(self):
        command(self.repo, "branch", "comparison")
        before = capture(self.repo, "comparison")
        tree = command(self.repo, "rev-parse", "HEAD^{tree}").decode().strip()
        other = command(self.repo, "commit-tree", tree, "-p", self.start["head"], "-m", "upstream moved").decode().strip()
        command(self.repo, "update-ref", "refs/heads/comparison", other)
        after = capture(self.repo, "comparison")
        self.assertEqual(after["head"], before["head"])
        self.assertNotEqual(after["base"], before["base"])
        self.assertNotEqual(after["snapshot_id"], before["snapshot_id"])

    def test_index_only_change_has_distinct_identity(self):
        (self.repo / "app.txt").write_text("staged next commit")
        command(self.repo, "add", "app.txt")
        (self.repo / "app.txt").write_text("original\n")
        current = capture(self.repo)
        self.assertEqual(current["content_sha256"], self.start["content_sha256"])
        self.assertNotEqual(current["index_sha256"], self.start["index_sha256"])
        self.assertNotEqual(current["snapshot_id"], self.start["snapshot_id"])

    def test_dirty_and_untracked_bytes_are_included(self):
        (self.repo / "app.txt").write_text("changed\n")
        dirty = capture(self.repo)
        self.assertNotEqual(dirty["snapshot_id"], self.start["snapshot_id"])
        (self.repo / "new.py").write_text("new behavior\n")
        current = capture(self.repo)
        self.assertNotEqual(current["snapshot_id"], dirty["snapshot_id"])
        self.assertIn("new.py", [file["path"] for file in current["files"]])

    def test_deletion_is_recorded(self):
        (self.repo / "app.txt").unlink()
        current = capture(self.repo)
        self.assertNotEqual(current["snapshot_id"], self.start["snapshot_id"])
        self.assertEqual(next(file for file in current["files"] if file["path"] == "app.txt")["kind"], "deleted")

    def test_same_content_new_head_changes_identity(self):
        command(self.repo, "commit", "--allow-empty", "-qm", "new integration context")
        current = capture(self.repo)
        self.assertEqual(current["content_sha256"], self.start["content_sha256"])
        self.assertNotEqual(current["head"], self.start["head"])
        self.assertNotEqual(current["snapshot_id"], self.start["snapshot_id"])

    def test_base_identity_is_part_of_snapshot(self):
        command(self.repo, "commit", "--allow-empty", "-qm", "new base")
        old_base = capture(self.repo, self.start["head"])
        new_base = capture(self.repo, "HEAD")
        self.assertNotEqual(old_base["snapshot_id"], new_base["snapshot_id"])

    def test_executable_mode_is_part_of_snapshot(self):
        os.chmod(self.repo / "app.txt", 0o755)
        self.assertNotEqual(capture(self.repo)["snapshot_id"], self.start["snapshot_id"])

    def test_symlink_is_hashed_without_following_target(self):
        outside = self.root / "outside.txt"
        outside.write_text("private first")
        (self.repo / "link").symlink_to(outside)
        first = capture(self.repo)
        outside.write_text("private second")
        self.assertEqual(capture(self.repo), first)
        self.assertEqual(next(file for file in first["files"] if file["path"] == "link")["kind"], "symlink")

    def test_parent_symlink_is_rejected(self):
        directory = self.repo / "nested"
        directory.mkdir()
        (directory / "tracked.txt").write_text("tracked")
        command(self.repo, "add", "nested")
        (directory / "tracked.txt").unlink()
        directory.rmdir()
        directory.symlink_to(self.root)
        with self.assertRaisesRegex(ValueError, "Parent symlink"):
            capture(self.repo)

    def test_ignored_outputs_need_separate_identity(self):
        (self.repo / "cache").mkdir()
        (self.repo / "cache" / "output").write_text("build artifact")
        self.assertEqual(capture(self.repo), self.start)

    def test_invalid_base_fails(self):
        with self.assertRaises(subprocess.CalledProcessError):
            capture(self.repo, "missing-fixture-base")

    def test_non_repository_fails(self):
        with self.assertRaises(subprocess.CalledProcessError):
            capture(self.root)


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="engineering-resolver-test-")
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def skill(self, folder, name="engineering-example"):
        location = self.root / folder
        location.mkdir(parents=True)
        (location / "SKILL.md").write_text(f"---\nname: {name}\ndescription: fixture\n---\n")
        return location

    def test_generated_folder_and_top_level_uninstalled(self):
        active = self.skill("skill-generated-id")
        self.skill("uninstalled/old")
        self.assertEqual(resolve("engineering-example", [self.root]), active)
        with self.assertRaisesRegex(ValueError, "found 2"):
            resolve("engineering-example", [self.root], include_disabled=True)

    def test_nested_uninstalled_does_not_hide_active_duplicate(self):
        self.skill("one")
        self.skill("nested/uninstalled/two")
        with self.assertRaisesRegex(ValueError, "found 2"):
            resolve("engineering-example", [self.root])

    def test_duplicate_active_skill_is_rejected(self):
        self.skill("one")
        self.skill("two")
        with self.assertRaisesRegex(ValueError, "found 2"):
            resolve("engineering-example", [self.root])

    def test_missing_name_has_no_directory_fallback(self):
        self.skill("engineering-example", "engineering-something-else")
        with self.assertRaisesRegex(ValueError, "found 0"):
            resolve("engineering-example", [self.root])

    def test_repeated_root_does_not_create_false_duplicate(self):
        active = self.skill("skill-generated-id")
        self.assertEqual(resolve("engineering-example", [self.root, self.root]), active)

    def test_symlinked_skill_file_is_not_active(self):
        source = self.skill("uninstalled/source")
        active = self.root / "shortcut"
        active.mkdir()
        (active / "SKILL.md").symlink_to(source / "SKILL.md")
        with self.assertRaisesRegex(ValueError, "found 0"):
            resolve("engineering-example", [self.root])


if __name__ == "__main__":
    unittest.main(verbosity=2)
