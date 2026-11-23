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
from run import check, checkpoint, execute, inventory, prepare
from workflow_cases import (AGGREGATION_INDEXED, AGGREGATION_PARTIAL,
                            AGGREGATION_POSITIVE_ONLY, AGGREGATION_REFERENCE,
                            LEASE_GOOD, LEASE_SPLIT, MEASURE_REFERENCE,
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
                self.assertNotIn("second_prompt", prepared)

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

    def test_aggregation_benchmark_checks_equal_work_and_records_paired_samples(self):
        target = self.trial("measure-to-improve")
        work = target / "work"
        original = inventory(work)
        workload = self.command(target, "-c", "\n".join([
            "import json",
            "from workload import make_workload",
            "rows, accounts = make_workload()",
            "print(json.dumps(sorted({row['account'] for row in rows})))",
        ]))
        self.assertEqual(workload.returncode, 0, workload.stderr)
        populated = json.loads(workload.stdout)
        self.assertEqual(len(populated), 160)
        self.assertEqual(populated, [f"acct-{index:04d}" for index in range(160)])
        for implementation in (AGGREGATION_REFERENCE, AGGREGATION_INDEXED):
            if implementation == AGGREGATION_INDEXED:
                first = checkpoint(target)
                self.assertEqual(first["changed_after_first_turn"], [])
                (work / "candidate.py").write_text(implementation)
            before = inventory(work)
            observed = self.command(target, "benchmark.py")
            self.assertEqual(observed.returncode, 0, observed.stderr)
            measured = json.loads(observed.stdout)
            self.assertEqual(measured["workload"], {
                "input_rows": 6000, "populated_accounts": 160, "requested_accounts": 173,
                "repetitions_per_sample": 2, "paired_samples": 6})
            self.assertEqual(measured["correctness"], {
                "contract_examples": {"reference": 5, "candidate": 5},
                "all_outputs_equal": True, "inputs_unchanged": True})
            self.assertEqual(len(measured["pairs"]), 6)
            for index, pair in enumerate(measured["pairs"]):
                self.assertEqual(pair["order"], ["reference", "candidate"]
                                 if index % 2 == 0 else ["candidate", "reference"])
                for label in ("reference", "candidate"):
                    self.assertEqual(pair[label]["calls"], 2)
                    self.assertEqual(pair[label]["completed_summaries"], 346)
                    self.assertGreater(pair[label]["seconds"], 0)
            self.assertTrue(measured["runtime"]["python"])
            self.assertEqual(measured["source_sha256"], {
                name: before[name] for name in (
                    "candidate.py", "reference.py", "workload.py", "benchmark.py", "SPEC.md")})
            self.assertEqual(inventory(work), before)
        report = check(target, run_code=True)
        self.assertEqual(report["status"], "needs_review", report)
        self.assertTrue(report["observations"]["independent_behavior"]["outputs_equal"])
        self.assertEqual(report["changed_files"], ["candidate.py"])
        self.assertTrue(report["manual_review_required"])
        self.assertNotEqual(inventory(work)["candidate.py"], original["candidate.py"])
        # Ratios are observed, never threshold-graded by helper controls.

    def test_aggregation_probe_accepts_correct_work_and_rejects_semantic_faults(self):
        target = self.trial("measure-to-improve")
        candidate = target / "work" / "candidate.py"
        for implementation in (AGGREGATION_REFERENCE, AGGREGATION_INDEXED):
            candidate.write_text(implementation)
            observed = self.observe(target, "aggregation")
            self.assertTrue(observed["successful"], observed)
            self.assertTrue(observed["outputs_equal"])
            self.assertEqual(observed["cases_checked_per_implementation"], 8)
            self.assertTrue(observed["inputs_unchanged"])
            self.assertTrue(observed["changed_inputs_rechecked"])
        shared = '''def summarize(rows, accounts):
    totals = {}
    for row in rows:
        entry = totals.setdefault(row["account"],
                                  {"account": row["account"], "count": 0, "total": 0})
        entry["count"] += 1
        entry["total"] += row["delta"]
    return [totals.get(account, {"account": account, "count": 0, "total": 0})
            for account in accounts]
'''
        reused_buffer = '''buffer = []


def summarize(rows, accounts):
    totals = {}
    for row in rows:
        count, total = totals.get(row["account"], (0, 0))
        totals[row["account"]] = (count + 1, total + row["delta"])
    del buffer[len(accounts):]
    while len(buffer) < len(accounts):
        buffer.append({})
    for item, account in zip(buffer, accounts):
        count, total = totals.get(account, (0, 0))
        item.update(account=account, count=count, total=total)
    return buffer
'''
        for implementation, expected_error in (
                (AGGREGATION_PARTIAL, "summary differs"),
                (AGGREGATION_POSITIVE_ONLY, "summary differs"),
                (shared, "shares output dictionaries"),
                (reused_buffer, "reuses output dictionaries across calls")):
            with self.subTest(defect=expected_error, source=implementation):
                candidate.write_text(implementation)
                observed = self.observe(target, "aggregation")
                self.assertFalse(observed["successful"], observed)
                self.assertIn("AssertionError: Candidate", observed["error"])
                self.assertIn(expected_error, observed["error"])
                measured = self.command(target, "benchmark.py")
                self.assertNotEqual(measured.returncode, 0)
                self.assertIn("ValueError: candidate:", measured.stderr)
                self.assertEqual(measured.stdout, "")

    def test_measure_to_improve_checkpoint_allows_only_the_second_turn_to_change_work(self):
        target = self.trial("measure-to-improve")
        case = WORKFLOW_CASES["measure-to-improve"]
        before_checkpoint = check(target)
        self.assertFalse(before_checkpoint["objective_checks"]["first_turn_unchanged"])
        first = checkpoint(target)
        self.assertEqual(first["changed_after_first_turn"], [])
        self.assertEqual(first["next_prompt"], case["second_prompt"])
        work = target / "work"
        (work / "candidate.py").write_text(AGGREGATION_INDEXED)
        tests = work / "tests"
        tests.mkdir()
        (tests / "test_summary.py").write_text(
            "import unittest\nfrom candidate import summarize\n\n"
            "class SummaryTests(unittest.TestCase):\n"
            "    def test_signed_deltas(self):\n"
            "        self.assertEqual(summarize([{'account': 'a', 'delta': -3},\n"
            "                                    {'account': 'a', 'delta': 0}], ['a']),\n"
            "                         [{'account': 'a', 'count': 2, 'total': -3}])\n")
        result = self.command(target, "-m", "unittest", "discover", "-s", "tests")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran 1 test", result.stderr)
        (work / "local-evidence.txt").write_text(
            "Scope-allowance control: the signed-delta unittest ran successfully.\n")
        after = check(target, run_code=True)
        self.assertTrue(all(after["objective_checks"].values()), after)
        self.assertEqual(after["status"], "needs_review")
        self.assertEqual(after["changed_files"], [
            "candidate.py", "local-evidence.txt", "tests/test_summary.py"])

    def test_measure_to_improve_checkpoint_retains_first_turn_edits_additions_and_removals(self):
        for violation in ("edit", "addition", "removal"):
            with self.subTest(violation=violation):
                target = self.root / violation
                prepare("measure-to-improve", target)
                work = target / "work"
                if violation == "edit":
                    path = work / "candidate.py"
                    original = path.read_text()
                    path.write_text(AGGREGATION_INDEXED)
                elif violation == "addition":
                    path = work / "premature-report.txt"
                    original = None
                    path.write_text("The first turn did not authorize writing a report.\n")
                else:
                    path = work / "reference.py"
                    original = path.read_text()
                    path.unlink()
                first = checkpoint(target)
                self.assertEqual(first["changed_after_first_turn"], [path.name])
                if original is None:
                    path.unlink()
                else:
                    path.write_text(original)
                after_restoration = check(target)
                self.assertTrue(after_restoration["objective_checks"]["protected_files_unchanged"])
                self.assertFalse(after_restoration["objective_checks"]["first_turn_unchanged"])
                self.assertEqual(after_restoration["status"], "failed_checks")
                with self.assertRaisesRegex(ValueError, "already exists"):
                    checkpoint(target)

    def test_measure_to_improve_frozen_inputs_cannot_be_changed(self):
        target = self.trial("measure-to-improve")
        checkpoint(target)
        for name in WORKFLOW_CASES["measure-to-improve"]["protected"]:
            with self.subTest(path=name):
                path = target / "work" / name
                original = path.read_text()
                path.write_text(original + "\n# Unrequested change\n")
                changed = check(target)
                self.assertFalse(changed["objective_checks"]["protected_files_unchanged"])
                self.assertEqual(changed["status"], "failed_checks")
                path.write_text(original)
        restored = check(target)
        self.assertEqual(restored["status"], "needs_review")


if __name__ == "__main__":
    unittest.main()
