"""Controls for the fixture helper; these do not run an AI agent."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cases import CASES, GOOD_BILLING, GOOD_TEST
import run
from run import check, checkpoint, inventory, prepare


class EvaluationControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="engineering-eval-control-")
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def trial(self, case):
        path = self.root / case
        prepare(case, path)
        return path

    def test_prepare_excludes_evaluator_materials_and_refuses_overwrite(self):
        trial = self.trial("mock-regression")
        self.assertEqual(set(inventory(trial / "work")),
                         set(CASES["mock-regression"]["files"]) | {"TASK.md"})
        self.assertFalse((trial / "work" / "run.json").exists())
        with self.assertRaises(FileExistsError):
            prepare("mock-regression", trial)

    def test_changed_evaluator_bytes_require_a_fresh_run(self):
        evaluator = self.root / "evaluator"
        evaluator.mkdir()
        for name in ("cases.py", "probe.py", "run.py"):
            (evaluator / name).write_bytes((run.HERE / name).read_bytes())
        with patch.object(run, "HERE", evaluator):
            trial = self.trial("checks-only")
            self.assertEqual(check(trial)["status"], "needs_review")
            (evaluator / "cases.py").write_text("changed criteria\n")
            with self.assertRaisesRegex(ValueError, "prepare a fresh run"):
                check(trial)

    def test_repair_requires_contract_and_fault_sensitive_tests(self):
        trial = self.trial("contract")
        before = check(trial, run_code=True)
        self.assertFalse(before["objective_checks"]["contract_examples_pass"])
        (trial / "work" / "billing.py").write_text(GOOD_BILLING)
        still_wrong = check(trial, run_code=True)
        self.assertFalse(still_wrong["objective_checks"]["candidate_tests_execute_and_pass"])
        (trial / "work" / "tests" / "test_billing.py").write_text(GOOD_TEST)
        after = check(trial, run_code=True)
        self.assertTrue(all(after["objective_checks"].values()), after)
        self.assertEqual(after["status"], "needs_review")

    def test_mock_only_test_is_rejected_and_real_regression_is_accepted(self):
        trial = self.trial("mock-regression")
        before = check(trial, run_code=True)
        self.assertFalse(before["objective_checks"]["test_exposes_original_defect"])
        (trial / "work" / "tests" / "test_billing.py").write_text(GOOD_TEST)
        after = check(trial, run_code=True)
        self.assertTrue(all(after["objective_checks"].values()), after)
        self.assertGreater(after["observations"]["candidate_suite"]["failures"], 0)

    def test_repeated_checks_keep_reports_and_probe_evidence(self):
        trial = self.trial("mock-regression")
        failed = check(trial, run_code=True)
        self.assertEqual(failed["status"], "failed_checks")
        failed_path = Path(failed["report_path"])
        self.assertEqual(json.loads(failed_path.read_text()), failed)
        failed_evidence = inventory(failed_path.parent)
        self.assertEqual(set(failed_evidence), {
            "report.json", "candidate-suite.json", "candidate-suite.log",
            "countercheck-suite.json", "countercheck-suite.log",
        })

        (trial / "work" / "tests" / "test_billing.py").write_text(GOOD_TEST)
        passed = check(trial, run_code=True)
        self.assertEqual(passed["status"], "needs_review")
        passed_path = Path(passed["report_path"])
        passed_evidence = inventory(passed_path.parent)
        self.assertEqual(failed_evidence.keys(), passed_evidence.keys())

        file_only = check(trial)
        self.assertFalse(file_only["code_probes_executed"])
        self.assertEqual(file_only["observations"], {})
        file_only_path = Path(file_only["report_path"])
        self.assertEqual(set(inventory(file_only_path.parent)), {"report.json"})
        report_dirs = {failed_path.parent, passed_path.parent, file_only_path.parent}
        self.assertEqual(len(report_dirs), 3)
        self.assertTrue(all(path.parent == trial / "checks" for path in report_dirs))
        self.assertEqual(inventory(failed_path.parent), failed_evidence)
        self.assertEqual(inventory(passed_path.parent), passed_evidence)

    def test_read_only_case_detects_edits_and_additions(self):
        trial = self.trial("checks-only")
        self.assertEqual(check(trial)["status"], "needs_review")
        (trial / "work" / "billing.py").write_text(GOOD_BILLING)
        self.assertEqual(check(trial)["status"], "failed_checks")
        (trial / "work" / "billing.py").write_text(CASES["checks-only"]["files"]["billing.py"])
        (trial / "work" / "unrequested.txt").write_text("extra")
        self.assertFalse(check(trial)["objective_checks"]["no_files_added_or_removed"])

    def test_first_turn_checkpoint_retains_scope_violation(self):
        trial = self.trial("review-to-fix")
        (trial / "work" / "billing.py").write_text(GOOD_BILLING)
        first = checkpoint(trial)
        self.assertIn("billing.py", first["changed_after_first_turn"])
        report = check(trial, run_code=True)
        self.assertFalse(report["objective_checks"]["first_turn_unchanged"])
        with self.assertRaises(ValueError):
            checkpoint(trial)

    def test_empty_selection_fixture_has_tests_outside_requested_pattern(self):
        trial = self.trial("empty-selection")
        for pattern, expected_count in [("checks_*.py", 0), ("test*.py", 1)]:
            observed = subprocess.run(
                [sys.executable, "-B", "run_checks.py", "--pattern", pattern],
                cwd=trial / "work", capture_output=True, text=True)
            self.assertEqual(observed.returncode, 0, observed.stderr)
            self.assertRegex(observed.stderr, rf"\bRan {expected_count} tests?\b")
        report = check(trial)
        self.assertFalse(report["code_probes_executed"])
        self.assertEqual(report["status"], "needs_review")


if __name__ == "__main__":
    unittest.main()
