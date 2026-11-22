"""Executed known-good and known-bad controls; these are not agent trials."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run
from cases import CASES
from run import check, execute, inventory, prepare
from workflow_cases import (LEASE_GOOD, LEASE_SPLIT, MEASURE_REFERENCE,
                            NOTES_DUPLICATES, SERIALIZERS_BRIDGE, SERIALIZERS_NEW,
                            WORKFLOW_CASES)


class WorkflowControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workflow-eval-control-")
        self.root = Path(self.temp.name)
        self.probe_number = 0

    def tearDown(self):
        self.temp.cleanup()

    def trial(self, case):
        target = self.root / case
        prepare(case, target)
        return target

    def observe(self, target, mode):
        self.probe_number += 1
        return execute(target / "work", mode, self.root / f"probe-{self.probe_number}.json")

    def command(self, target, *args):
        return subprocess.run([sys.executable, "-B", *args], cwd=target / "work",
                              capture_output=True, text=True, timeout=10,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})

    def test_all_workflow_tasks_hide_judge_materials(self):
        for name, case in WORKFLOW_CASES.items():
            with self.subTest(case=name):
                target = self.root / name
                prepared = prepare(name, target)
                self.assertEqual(set(inventory(target / "work")),
                                 set(case["files"]) | {"TASK.md"})
                self.assertEqual((target / "work" / "TASK.md").read_text(),
                                 case["prompt"] + "\n")
                self.assertNotIn("manual_review_required", (target / "work" / "TASK.md").read_text())
                self.assertEqual("fresh_agent_followup" in prepared, name == "application-create")

    def test_real_lease_baseline_holds_and_split_claim_is_detected(self):
        target = self.trial("formal-create")
        baseline = self.observe(target, "lease")
        self.assertTrue(baseline["successful"], baseline)
        self.assertTrue(baseline["holds"])
        self.assertEqual(baseline["schedules_checked"], 256)

        (target / "work" / "lease.py").write_text(LEASE_SPLIT)
        broken = self.observe(target, "lease")
        self.assertTrue(broken["successful"], broken)
        self.assertFalse(broken["holds"])
        self.assertEqual(broken["counterexample"][-1]["active"], ["A", "B"])
        self.assertLessEqual(len(broken["counterexample"]), 8)
        replay = self.command(target, "-c", "\n".join([
            "import json, lease",
            f"schedule = {repr([step['worker'] for step in broken['counterexample']])}",
            "state = lease.Lease()",
            "workers = {name: lease.work(state, name) for name in ('A', 'B')}",
            "for name in schedule: next(workers[name], None)",
            "print(json.dumps(sorted(state.active)))",
        ]))
        self.assertEqual(replay.returncode, 0, replay.stderr)
        self.assertEqual(json.loads(replay.stdout), ["A", "B"])
        (target / "work" / "lease.py").write_text(LEASE_GOOD)
        self.assertTrue(self.observe(target, "lease")["holds"])

    def test_stale_model_passes_until_atomicity_is_updated(self):
        target = self.trial("formal-maintain")
        work = target / "work"
        coverage = json.loads((work / "verification" / "coverage.json").read_text())
        recorded = coverage["synchronization"]["files"]["lease.py"]
        self.assertEqual(recorded, hashlib.sha256(LEASE_GOOD.encode()).hexdigest())
        self.assertNotEqual(recorded, hashlib.sha256((work / "lease.py").read_bytes()).hexdigest())
        old = self.command(target, "verification/check_lease.py")
        self.assertEqual(old.returncode, 0, old.stderr)
        self.assertTrue(json.loads(old.stdout)["holds"])
        self.assertFalse(self.observe(target, "lease")["holds"])

        (work / "verification" / "model.py").write_text(LEASE_SPLIT)
        current = self.command(target, "verification/check_lease.py")
        self.assertEqual(current.returncode, 1, current.stderr)
        self.assertFalse(json.loads(current.stdout)["holds"])
        self.assertEqual(json.loads(current.stdout)["counterexample"][-1]["active"], ["A", "B"])
        self.assertEqual((work / "lease.py").read_text(), LEASE_SPLIT)

    def test_empty_notes_store_persistence_and_duplicate_fault(self):
        target = self.trial("application-create")
        before = inventory(target / "work")
        good = self.observe(target, "notes")
        self.assertTrue(good["successful"], good)
        self.assertEqual(good["processes_run"], 9)
        self.assertTrue(good["owned_store_cleaned"])
        self.assertEqual(inventory(target / "work"), before)
        (target / "work" / "notes.py").write_text(NOTES_DUPLICATES)
        bad = self.observe(target, "notes")
        self.assertFalse(bad["successful"])
        self.assertIn("Retry duplicated a note", bad["error"])

    def test_incomplete_conversion_is_not_equal_work(self):
        target = self.trial("measured-comparison")
        timing = self.command(target, "benchmark.py")
        self.assertEqual(timing.returncode, 0, timing.stderr)
        self.assertEqual(set(json.loads(timing.stdout)), {"reference", "candidate"})
        partial = self.observe(target, "conversion")
        self.assertTrue(partial["successful"], partial)
        self.assertFalse(partial["outputs_equal"])
        self.assertEqual(partial["cases"][-1]["candidate_outputs"], 200)
        (target / "work" / "candidate.py").write_text(MEASURE_REFERENCE)
        complete = self.observe(target, "conversion")
        self.assertTrue(complete["successful"], complete)
        self.assertTrue(complete["outputs_equal"])
        self.assertEqual(complete["cases"][-1]["candidate_outputs"], 2000)
        # Timing values are deliberately not graded: equal-work validity is the control.

    def test_dynamic_saved_routes_accept_bridge_and_reject_removed_exports(self):
        target = self.trial("refactor-contract")
        baseline = self.observe(target, "saved_routes")
        self.assertTrue(baseline["successful"], baseline)
        self.assertEqual(baseline["examples_checked"], 10)
        (target / "work" / "reports.py").write_text(SERIALIZERS_NEW)
        (target / "work" / "handlers.py").write_text(SERIALIZERS_BRIDGE)
        good = self.observe(target, "saved_routes")
        self.assertTrue(good["successful"], good)
        (target / "work" / "handlers.py").write_text("from reports import render\n")
        broken = self.observe(target, "saved_routes")
        self.assertFalse(broken["successful"])
        self.assertIn("AttributeError", broken["error"])

    def test_manual_report_preserves_failed_artifacts_and_requires_judgment(self):
        target = self.trial("formal-create")
        missing = check(target, run_code=True)
        self.assertEqual(missing["status"], "failed_checks")
        self.assertFalse(missing["objective_checks"]["project_skill_present"])
        before = inventory(Path(missing["report_path"]).parent)
        skill = target / "work" / ".agents" / "skills" / "incomplete" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("This is an intentionally inadequate control artifact.\n")
        structural = check(target, run_code=True)
        self.assertTrue(all(structural["objective_checks"].values()), structural)
        self.assertEqual(structural["status"], "needs_review")
        self.assertIn("not the authored verification asset", structural["probe_limit"])
        self.assertTrue(structural["manual_review_required"])
        self.assertEqual(inventory(Path(missing["report_path"]).parent), before)
        first_snapshot = Path(missing["artifact_snapshot"])
        self.assertFalse((first_snapshot / ".agents").exists())
        second_snapshot = Path(structural["artifact_snapshot"])
        self.assertTrue((second_snapshot / skill.relative_to(target / "work")).exists())
        self.assertEqual(inventory(second_snapshot), structural["artifact_hashes"])

    def test_new_probe_identity_rejects_changed_evaluator(self):
        evaluator = self.root / "evaluator"
        evaluator.mkdir()
        for name in run.fixture_identity():
            (evaluator / name).write_bytes((run.HERE / name).read_bytes())
        with patch.object(run, "HERE", evaluator):
            target = self.trial("formal-maintain")
            self.assertEqual(check(target)["status"], "needs_review")
            (evaluator / "workflow_probe.py").write_text("changed independent probe\n")
            with self.assertRaisesRegex(ValueError, "prepare a fresh run"):
                check(target)

    def test_candidate_module_does_not_shadow_trusted_probe(self):
        target = self.trial("formal-create")
        (target / "work" / "workflow_probe.py").write_text(
            "raise RuntimeError('Candidate module shadowed evaluator')\n")
        observed = self.observe(target, "lease")
        self.assertTrue(observed["successful"], observed)
        self.assertTrue(observed["holds"])
        self.assertEqual(observed["schedules_checked"], 256)

    def test_measurement_is_read_only_even_when_the_candidate_is_incorrect(self):
        target = self.trial("measured-comparison")
        report = check(target, run_code=True)
        self.assertEqual(report["status"], "needs_review")
        self.assertFalse(report["observations"]["independent_behavior"]["outputs_equal"])
        (target / "work" / "candidate.py").write_text(MEASURE_REFERENCE)
        repaired = check(target, run_code=True)
        self.assertFalse(repaired["objective_checks"]["protected_files_unchanged"])
        self.assertEqual(repaired["status"], "failed_checks")


if __name__ == "__main__":
    unittest.main()
