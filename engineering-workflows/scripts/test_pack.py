#!/usr/bin/env python3
"""Validate canonical installed bytes and exercise rejection with disposable copies.

Copies are mutation fixtures, not evidence of installation or host registration.
Set ENGINEERING_PACK_TEST_ROOT to select the canonical installed skill root.
"""
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from resolve_skill import resolve
from validate_pack import validate


SOURCE = Path(os.environ.get("ENGINEERING_PACK_TEST_ROOT", Path(__file__).resolve().parents[2])).resolve()


class CanonicalPackTests(unittest.TestCase):
    def test_canonical_installed_structure(self):
        report = validate([SOURCE])
        self.assertTrue(report["valid"], json.dumps(report, indent=2))
        self.assertEqual(report["skill_count"], 7)
        self.assertEqual(report["explicit_only"], [])
        self.assertEqual(set(report["user_request_only"]), {"engineering-campaign", "engineering-configure"})



class PackFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="engineering-pack-fixture-")
        self.root = Path(self.temp.name) / "skills"
        core = resolve("engineering-workflows", [SOURCE])
        self.manifest = json.loads((core / "references/pack-contract.json").read_text())
        self.paths = {}
        for index, node in enumerate(self.manifest["skills"]):
            destination = self.root / f"skill-fixture-{index}"
            shutil.copytree(resolve(node["name"], [SOURCE]), destination,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            self.paths[node["name"]] = destination
        self.core = self.paths["engineering-workflows"]

    def tearDown(self):
        self.temp.cleanup()

    def write_manifest(self):
        (self.core / "references/pack-contract.json").write_text(json.dumps(self.manifest, indent=2) + "\n")

    def node(self, name):
        return next(node for node in self.manifest["skills"] if node["name"] == name)

    def assert_rejected(self, fragment, **kwargs):
        report = validate([self.root], **kwargs)
        self.assertFalse(report["valid"], report)
        self.assertTrue(any(fragment in error for error in report["errors"]), report)

    def test_copies_with_generated_directory_names_pass(self):
        report = validate([self.root])
        self.assertTrue(report["valid"], report)

    def test_complete_pack_with_directory_symlinks_passes(self):
        installed = Path(self.temp.name) / "installed"
        installed.mkdir()
        for name, source in self.paths.items():
            (installed / name).symlink_to(source, target_is_directory=True)
        report = validate([installed])
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["skill_count"], 7)

    def test_cycle_is_rejected(self):
        self.node("engineering-verify")["auto_calls"].append("engineering-workflows")
        self.write_manifest()
        self.assert_rejected("cycle")

    def test_explicit_only_automatic_call_is_rejected(self):
        self.node("engineering-verify")["disable_model_invocation"] = True
        self.write_manifest()
        self.assert_rejected("automatic edge to explicit-only engineering-verify")

    def test_user_request_only_automatic_call_is_rejected(self):
        self.node("engineering-workflows")["auto_calls"].append("engineering-configure")
        self.write_manifest()
        self.assert_rejected("automatic edge to user-request-only engineering-configure")

    def test_admin_cannot_drop_user_request_requirement(self):
        self.node("engineering-campaign")["user_request_required"] = False
        self.write_manifest()
        self.assert_rejected("user_request_required must be true only for Campaign and Configure")

    def test_support_cannot_be_redeclared_user_request_only(self):
        self.node("engineering-verify")["user_request_required"] = True
        self.write_manifest()
        self.assert_rejected("user_request_required must be true only for Campaign and Configure")

    def test_admin_must_allow_natural_language_selection(self):
        self.node("engineering-campaign")["disable_model_invocation"] = True
        self.write_manifest()
        self.assert_rejected("administrative skill must permit natural-language selection")

    def test_user_request_requirement_must_be_boolean(self):
        self.node("engineering-campaign")["user_request_required"] = "true"
        self.write_manifest()
        self.assert_rejected("user_request_required must be a Boolean")

    def test_unknown_callee_is_rejected(self):
        self.node("engineering-workflows")["auto_calls"].append("engineering-nonexistent")
        self.write_manifest()
        self.assert_rejected("unknown automatic")

    def test_duplicate_edge_is_rejected(self):
        node = self.node("engineering-workflows")
        node["auto_calls"].append(node["auto_calls"][0])
        self.write_manifest()
        self.assert_rejected("duplicates")

    def test_wrong_native_policy_is_rejected(self):
        file = self.paths["engineering-campaign"] / "agents/openai.yaml"
        file.write_text(file.read_text().replace("allow_implicit_invocation: true", "allow_implicit_invocation: false"))
        self.assert_rejected("native invocation policy mismatch")

    def test_yaml_duplicate_key_is_rejected(self):
        file = self.paths["engineering-check"] / "SKILL.md"
        file.write_text(file.read_text().replace("description:", "name: engineering-check\ndescription:", 1))
        self.assert_rejected("Duplicate YAML key")

    def test_yaml_bad_policy_type_is_rejected(self):
        file = self.paths["engineering-campaign"] / "agents/openai.yaml"
        file.write_text(file.read_text().replace("allow_implicit_invocation: true", "allow_implicit_invocation: 'true'"))
        self.assert_rejected("native invocation policy mismatch")

    def test_verify_without_testing_guide_is_rejected(self):
        verify = self.paths["engineering-verify"]
        entrypoint = verify / "SKILL.md"
        _, frontmatter, _ = entrypoint.read_text(encoding="utf-8").split("---\n", 2)
        # An older Verify entrypoint has no link to the new cross-skill dependency.
        entrypoint.write_text(f"---\n{frontmatter}---\n\n# Engineering Verify\n", encoding="utf-8")
        (verify / "references/testing.md").unlink()
        self.assert_rejected("engineering-verify: required file missing/unsafe: references/testing.md")

    def test_older_verify_cannot_hide_missing_lifecycle_guides(self):
        verify = self.paths["engineering-verify"]
        entrypoint = verify / "SKILL.md"
        _, frontmatter, _ = entrypoint.read_text(encoding="utf-8").split("---\n", 2)
        entrypoint.write_text(f"---\n{frontmatter}---\n\n# Engineering Verify\n", encoding="utf-8")
        for relative in ("references/application.md", "references/formal.md"):
            with self.subTest(reference=relative):
                path = verify / relative
                original = path.read_bytes()
                path.unlink()
                self.assert_rejected(f"engineering-verify: required file missing/unsafe: {relative}")
                path.write_bytes(original)

    def test_missing_phase_routes_are_rejected(self):
        (self.core / "references/routing.md").unlink()
        self.assert_rejected("routing.md")

    def test_missing_reference_is_rejected(self):
        (self.core / "references/contract.md").unlink()
        self.assert_rejected("contract.md")

    def test_broken_markdown_link_is_rejected(self):
        file = self.paths["engineering-check"] / "SKILL.md"
        file.write_text(file.read_text() + "\n[Missing](references/missing.md)\n")
        self.assert_rejected("broken/escaping link")

    def test_reference_definition_link_is_checked(self):
        file = self.paths["engineering-check"] / "SKILL.md"
        file.write_text(file.read_text() + "\n[Details][missing]\n\n[missing]: references/missing.md\n")
        self.assert_rejected("broken/escaping link")

    def test_escaping_markdown_link_is_rejected_even_if_target_exists(self):
        (self.root / "outside.md").write_text("fixture")
        file = self.paths["engineering-check"] / "SKILL.md"
        file.write_text(file.read_text() + "\n[Outside](%2e%2e/outside.md)\n")
        self.assert_rejected("broken/escaping link")

    def test_missing_icon_is_rejected(self):
        file = self.paths["engineering-check"] / "agents/openai.yaml"
        file.write_text(file.read_text().replace("assets/icon.svg", "assets/missing.svg"))
        self.assert_rejected("missing/unsafe icon")

    def test_duplicate_active_name_is_rejected(self):
        shutil.copytree(self.paths["engineering-check"], self.root / "skill-duplicate")
        self.assert_rejected("found 2")

    def test_schema_version_is_checked(self):
        self.manifest["schema_version"] = 1
        self.write_manifest()
        self.assert_rejected("schema_version 3")

    def test_count_cannot_hide_a_missing_skill(self):
        self.manifest["skills"].pop()
        self.manifest["expected_skill_count"] = 6
        self.write_manifest()
        self.assert_rejected("must both be 7")

    def test_malformed_auto_calls_returns_error(self):
        self.node("engineering-check")["auto_calls"] = {"callee": "engineering-verify"}
        self.write_manifest()
        self.assert_rejected("auto_calls must be a list")

    def test_malformed_ui_returns_error(self):
        (self.paths["engineering-check"] / "agents/openai.yaml").write_text("- not a mapping\n")
        self.assert_rejected("must contain interface and policy objects")

    def test_unsafe_required_file_is_rejected(self):
        self.node("engineering-check")["required_files"].append("../outside.md")
        (self.root / "outside.md").write_text("fixture")
        self.write_manifest()
        self.assert_rejected("required file missing/unsafe")



if __name__ == "__main__":
    unittest.main(verbosity=2)
