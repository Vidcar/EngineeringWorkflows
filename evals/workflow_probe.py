"""Independent behavior probes for the manual workflow cases.

These inspect real product behavior. They do not grade the agent's reasoning or
establish that a verification asset authored by the agent is effective.
"""
import copy
import importlib
import itertools
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def lease_probe():
    module = importlib.import_module("lease")
    checked = 0
    for schedule in itertools.product(("A", "B"), repeat=8):
        state = module.Lease()
        workers = {name: module.work(state, name) for name in ("A", "B")}
        trace = []
        for name in schedule:
            action = next(workers[name], "done")
            trace.append({"worker": name, "action": action,
                          "owner": state.owner, "active": sorted(state.active)})
            if len(state.active) > 1:
                return {"successful": True, "holds": False, "bound": 8,
                        "schedules_checked": checked + 1, "counterexample": trace}
        checked += 1
    return {"successful": True, "holds": True, "bound": 8,
            "schedules_checked": checked}


def notes_probe(work):
    observations = []
    with tempfile.TemporaryDirectory(prefix="pocket-notes-probe-") as directory:
        store = Path(directory) / "owned" / "notes.json"

        def command(*args, expected_code=0):
            result = subprocess.run(
                [sys.executable, "-B", str(work / "notes.py"), "--store", str(store), *args],
                cwd=work, capture_output=True, text=True, timeout=5,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONOPTIMIZE": "0"})
            observations.append({"args": list(args), "returncode": result.returncode,
                                 "stdout": result.stdout, "stderr": result.stderr})
            if expected_code == 0:
                assert result.returncode == 0, observations[-1]
                return json.loads(result.stdout)
            assert result.returncode != 0, "Conflicting note was accepted"

        def persisted():
            return json.loads(store.read_text())

        first = {"id": "n1", "text": "hello"}
        second = {"id": "n2", "text": "keep me"}
        assert command("list") == []
        assert not store.exists(), "Listing a missing store created state"
        assert command("add", "--id", "n1", "--text", "hello") == first
        assert persisted() == [first], "The successful add was not persisted"
        assert command("add", "--id", "n1", "--text", "hello") == first
        assert persisted() == [first], "Retry duplicated a note"
        assert command("list") == [first], "A fresh process did not observe the note"
        original = store.read_bytes()
        command("add", "--id", "n1", "--text", "conflict", expected_code=1)
        assert store.read_bytes() == original, "Rejected request still changed state"
        assert command("add", "--id", "n2", "--text", "keep me") == second
        assert persisted() == [first, second]
        assert command("remove", "--id", "n1") == [second]
        assert persisted() == [second], "Removal damaged another note"
        assert command("remove", "--id", "n1") == [second]
        assert command("list") == [second]
        assert not store.with_name(store.name + ".tmp").exists(), "Temporary write leaked"
    return {"successful": True, "processes_run": len(observations),
            "observations": observations, "owned_store_cleaned": not store.exists()}


def conversion_probe():
    reference = importlib.import_module("reference").convert
    candidate = importlib.import_module("candidate").convert
    cases = []
    equal = True
    for size in (0, 1, 2, 10, 2000):
        rows = [{"id": i, "value": i * 3, "label": "é"} for i in range(size)]
        original = copy.deepcopy(rows)
        expected = [json.dumps(row, sort_keys=True) for row in rows]
        baseline = reference(rows)
        assert baseline == expected, "Reference violates the stated contract"
        assert rows == original, "Reference mutated input"
        actual = candidate(rows)
        assert rows == original, "Candidate mutated input"
        matches = actual == expected
        equal = equal and matches
        cases.append({"input_rows": size, "reference_outputs": len(baseline),
                      "candidate_outputs": len(actual), "outputs_equal": matches})
    return {"successful": True, "outputs_equal": equal, "cases": cases}


def saved_routes_probe():
    dispatch = importlib.import_module("dispatch").render_saved_route
    handlers = importlib.import_module("handlers")
    checked = 0
    for kind in ("invoice", "receipt"):
        direct = getattr(handlers, "render_" + kind)
        for pence, amount in ((1, "0.01"), (99, "0.99"), (100, "1.00"),
                              (109, "1.09"), (1000001, "10000.01")):
            item = {"id": 'saved-"route"', "pence": pence, "extra": [1, 2]}
            original = copy.deepcopy(item)
            expected = json.dumps({"amount": amount, "id": item["id"], "kind": kind},
                                  sort_keys=True, separators=(",", ":"))
            assert direct(item) == expected, (kind, pence, "public import output changed")
            assert dispatch(kind, item) == expected, (kind, pence, "saved route output changed")
            assert item == original, "Rendering mutated input"
            checked += 1
    return {"successful": True, "examples_checked": checked,
            "paths": ["public imports", "persisted dynamic routes"]}


def probe(work, mode):
    if mode == "lease":
        return lease_probe()
    if mode == "notes":
        return notes_probe(work)
    if mode == "conversion":
        return conversion_probe()
    if mode == "saved_routes":
        return saved_routes_probe()
    raise ValueError(f"Unknown workflow probe: {mode}")
