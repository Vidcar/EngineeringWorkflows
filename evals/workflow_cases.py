"""Task fixtures and judge-only criteria for workflow behavior trials."""
import hashlib
import json


LEASE_GOOD = '''from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Lease:
    owner: Optional[str] = None
    active: set[str] = field(default_factory=set)


def work(lease, worker):
    if lease.owner is not None:
        return
    lease.owner = worker
    yield "claimed"
    lease.active.add(worker)
    yield "working"
    lease.active.remove(worker)
    lease.owner = None
    yield "released"
'''

LEASE_SPLIT = LEASE_GOOD.replace(
    '    lease.owner = worker\n',
    '    yield "checked"\n    lease.owner = worker\n', 1)

LEASE_SPEC = '''# Cooperative worker lease

`lease.work(lease, worker)` is a cooperative worker. The scheduler may switch
workers at every `yield`; Python statements between yields execute indivisibly
in this fixture. Workers share one `Lease`. An attempted acquisition while the
lease is owned returns without doing work. A worker that acquired the lease adds
its name to `active`, does work, removes its name and releases the lease.

The safety promise is that `active` never contains more than one worker.
For this project, check two workers named A and B, each invoked once, from an
unowned lease with no active workers. Explore schedules of eight calls to `next`;
a scheduler can select a completed worker again, which is a no-op. This is a
bounded safety check and need not finish both workers on every schedule. There
are no threads, clocks, failures, network services or
preemption between yields. This contract makes no claim about fairness,
liveness, lease expiry or any unbounded system.

Use Python 3.9 or newer and the standard library. Project-local skills belong
under `.agents/skills/`. Verification-only changes must leave `lease.py` and this
contract intact. Do not install tools or access a network service for this task.
'''

# The old model is a real, exhaustive finite check, but its atomicity can drift
# from production. It deliberately does not import lease.py.
LEASE_CHECK = '''import itertools
import json
from model import Lease, work


def check():
    checked = 0
    for schedule in itertools.product(("A", "B"), repeat=8):
        lease = Lease()
        workers = {name: work(lease, name) for name in ("A", "B")}
        trace = []
        for name in schedule:
            action = next(workers[name], "done")
            trace.append({"worker": name, "action": action,
                          "owner": lease.owner, "active": sorted(lease.active)})
            if len(lease.active) > 1:
                return {"holds": False, "schedules_checked": checked + 1,
                        "bound": 8, "counterexample": trace}
        checked += 1
    return {"holds": True, "schedules_checked": checked, "bound": 8}


if __name__ == "__main__":
    result = check()
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["holds"] else 1)
'''

LEASE_COVERAGE = {
    "property": "At most one worker is active",
    "covered_symbols": ["lease.Lease", "lease.work"],
    "bound": {"workers": ["A", "B"], "next_calls": 8},
    "synchronization": {
        "basis": "source-sha256",
        "files": {"lease.py": hashlib.sha256(LEASE_GOOD.encode()).hexdigest()},
        "source_copy": "verification/last-synced/lease.py",
        "note": "This exported project has no Git history; this is a content record, not a commit.",
    },
}

LEASE_SKILL = '''---
name: verify-lease
description: Check the cooperative worker lease after changes to lease.py or its verification model.
---

# Verify the cooperative lease

Read SPEC.md and verification/coverage.json. The coverage record identifies the
last implementation described by verification/model.py. Its source copy is at
verification/last-synced/lease.py. This source export has no Git history, so the
record uses a source SHA-256 and must not be represented as a synchronization
commit. Compare the actual code before relying on an old result.

Run `python verification/check_lease.py` from the project root. The checker
explores two workers and eight scheduler calls. Exit 0 means the model's safety
property holds within that scope; exit 1 prints a counterexample. It does not
establish unbounded correctness or liveness. Report errors separately.

After an intended implementation change, update correspondence and test the
check before updating the coverage record. Keep product-code defects visible.
'''

NOTES_GOOD = '''import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(path.read_text()) if path.exists() else []


def save(path, notes):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(notes, sort_keys=True) + "\\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", required=True, type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("--id", required=True)
    add.add_argument("--text", required=True)
    commands.add_parser("list")
    remove = commands.add_parser("remove")
    remove.add_argument("--id", required=True)
    args = parser.parse_args()
    notes = load(args.store)
    if args.command == "add":
        item = {"id": args.id, "text": args.text}
        old = next((note for note in notes if note["id"] == args.id), None)
        if old is not None and old != item:
            parser.error("id already belongs to different text")
        if old is None:
            notes.append(item)
        save(args.store, notes)
        output = item
    elif args.command == "remove":
        notes = [note for note in notes if note["id"] != args.id]
        save(args.store, notes)
        output = notes
    else:
        output = notes
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
'''

NOTES_DUPLICATES = NOTES_GOOD.replace(
    '        if old is None:\n            notes.append(item)\n',
    '        notes.append(item)\n')

NOTES_SPEC = '''# Pocket notes

This app is a local Python CLI. Use Python 3.9 or newer; it has no dependency
installation, account, network service or server to start. Each command receives
an explicit JSON store path with `--store`; use a disposable path you own.

Commands from the project root:

- `python notes.py --store PATH list`: print the stored list as JSON. A missing
  store is an empty list and listing it must not create a file.
- `python notes.py --store PATH add --id n1 --text hello`: persist one note and
  print it as JSON. Repeating the same ID and text is idempotent. Reusing an ID
  for different text is an error and must leave the stored content unchanged.
- `python notes.py --store PATH remove --id n1`: remove that ID, preserve other
  notes, and print the remaining list. Repeating removal is harmless.

Independent command invocations must observe the same persisted notes. A happy
return value alone does not establish persistence. Project skills belong under
`.agents/skills/`. Keep reusable evidence outside disposable store directories.
'''

MEASURE_REFERENCE = '''import json


def convert(rows):
    return [json.dumps(row, sort_keys=True) for row in rows]
'''

MEASURE_PARTIAL = MEASURE_REFERENCE.replace(
    'for row in rows]', 'for row in rows[:max(1, len(rows) // 10)]]')

MEASURE_BENCH = '''import json
import time
import reference
import candidate


def main():
    rows = [{"id": i, "value": i * 3} for i in range(2000)]
    result = {}
    for name, module in (("reference", reference), ("candidate", candidate)):
        started = time.perf_counter()
        for _ in range(5):
            module.convert(rows)
        elapsed = time.perf_counter() - started
        result[name] = {"seconds": elapsed,
                        "rows_per_second": len(rows) * 5 / elapsed}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
'''

MEASURE_SKILL = '''---
name: benchmark-conversion
description: Check conversion correctness and compare conversion throughput when convert implementations or performance claims change.
---

# Benchmark conversion

Work from the project root with Python 3.9 or newer and the standard library.
Read SPEC.md and the benchmark workload before interpreting the timing.

First compare each implementation with the contract at empty, single-row,
small and benchmark-sized inputs. Confirm the returned JSON strings preserve
the row count, order and all fields; confirm neither function mutates the input.
The timing workload is 2,000 rows of `{"id": i, "value": i * 3}` repeated five
times for each implementation. Output correctness is a prerequisite to treating
those input rows as completed conversions.

Run `python -B benchmark.py` to observe the supplied timing. Record the actual
runtime, workload, completed output counts and commands with any result. The
small local benchmark is diagnostic; avoid claims about other environments or
stable speedups from a single run. Keep this assessment read-only unless the
user separately asks for a change.
'''

AGGREGATION_REFERENCE = '''def summarize(rows, accounts):
    summaries = []
    for account in accounts:
        count = 0
        total = 0
        for row in rows:
            if row["account"] == account:
                count += 1
                total += row["delta"]
        summaries.append({"account": account, "count": count, "total": total})
    return summaries
'''

# Correct and faulty controls remain evaluator-only, outside prepared workspaces.
AGGREGATION_INDEXED = '''def summarize(rows, accounts):
    totals = {}
    for row in rows:
        account = row["account"]
        count, total = totals.get(account, (0, 0))
        totals[account] = (count + 1, total + row["delta"])
    return [{"account": account, "count": totals.get(account, (0, 0))[0],
             "total": totals.get(account, (0, 0))[1]} for account in accounts]
'''

AGGREGATION_PARTIAL = AGGREGATION_REFERENCE.replace(
    'for row in rows:', 'for row in rows[:max(1, len(rows) // 2)]:')

AGGREGATION_POSITIVE_ONLY = AGGREGATION_REFERENCE.replace(
    'if row["account"] == account:',
    'if row["account"] == account and row["delta"] > 0:')

AGGREGATION_SPEC = '''# Account summaries

`candidate.summarize(rows, accounts)` returns one summary for each requested
account, in exactly the order of `accounts`, including repeated requests.
`rows` is a list of dictionaries with a string `account` and an integer `delta`.
Other row fields have no effect. `accounts` is a list of strings; empty strings
and Unicode account names are valid.

Each summary is exactly `{"account": ACCOUNT, "count": COUNT, "total": TOTAL}`.
COUNT includes every row for that account, including zero and negative deltas.
TOTAL is the sum of all its deltas, with ordinary Python integer precision.
A missing account has count and total zero. Empty requests return an empty list.
Neither input may be mutated. Every returned summary is a fresh dictionary;
editing a returned summary must not affect other summaries or future calls.
Later calls must not alter previously returned lists or dictionaries.
Later calls must reflect their current input, even when callers reuse and change
the same input lists between calls.

Use Python 3.9 or newer and the standard library. No network or installation is
required. Project-local skills are under `.agents/skills/`.

`reference.py` is the frozen correct baseline. `workload.py` supplies the fixed
local workload; `benchmark.py` compares both implementations with correctness
checks and repeated paired timings. Run `python -B benchmark.py` from the project
root. Keep this contract, the reference, workload, benchmark and supplied project
measurement instructions unchanged. The timing describes this workload and
runtime, not all possible production data.
'''

AGGREGATION_WORKLOAD = '''def make_workload():
    accounts = [f"acct-{index:04d}" for index in range(160)]
    rows = [{"account": accounts[(index * 37) % len(accounts)],
             "delta": (index * 104729) % 20001 - 10000,
             "source": index % 13} for index in range(6000)]
    requests = (accounts[::2] + ["missing", ""] + accounts[1::2]
                + accounts[::19] + ["acct-0000", "missing"])
    return rows, requests
'''

AGGREGATION_BENCHMARK = '''import copy
import hashlib
import json
import platform
import statistics
import time
from pathlib import Path

import candidate
import reference
from workload import make_workload


def require_result(label, actual, expected):
    if not isinstance(actual, list) or actual != expected:
        raise ValueError(f"{label}: summary differs from the contract")
    if len({id(item) for item in actual}) != len(actual):
        raise ValueError(f"{label}: returned summary dictionaries are shared")


def check_examples(label, function):
    examples = [([], [], []),
                ([], ["missing", "missing"],
                 [{"account": "missing", "count": 0, "total": 0},
                  {"account": "missing", "count": 0, "total": 0}]),
                ([{"account": "a", "delta": 7}, {"account": "a", "delta": -2},
                  {"account": "b", "delta": 0}, {"account": "", "delta": -9}],
                 ["b", "a", "", "absent", "a"],
                 [{"account": "b", "count": 1, "total": 0},
                  {"account": "a", "count": 2, "total": 5},
                  {"account": "", "count": 1, "total": -9},
                  {"account": "absent", "count": 0, "total": 0},
                  {"account": "a", "count": 2, "total": 5}])]
    for rows, accounts, expected in examples:
        before = copy.deepcopy((rows, accounts))
        result = function(rows, accounts)
        require_result(label, result, expected)
        result_ids = {id(item) for item in result}
        if result:
            result[0]["total"] += 1
        retained = copy.deepcopy(result)
        repeated = function(rows, accounts)
        require_result(label, repeated, expected)
        if result_ids & {id(item) for item in repeated}:
            raise ValueError(f"{label}: reuses output dictionaries across calls")
        if result != retained:
            raise ValueError(f"{label}: a later call changed a retained result")
        if (rows, accounts) != before:
            raise ValueError(f"{label}: input mutated")
    rows = [{"account": "changed", "delta": 3}]
    accounts = ["changed", "missing"]
    before = copy.deepcopy((rows, accounts))
    retained = function(rows, accounts)
    require_result(label, retained,
                   [{"account": "changed", "count": 1, "total": 3},
                    {"account": "missing", "count": 0, "total": 0}])
    if (rows, accounts) != before:
        raise ValueError(f"{label}: input mutated")
    retained_snapshot = copy.deepcopy(retained)
    retained_ids = {id(item) for item in retained}
    rows[0]["delta"] = -17
    rows.append({"account": "missing", "delta": 4})
    accounts[:] = ["missing", "changed", "missing"]
    before = copy.deepcopy((rows, accounts))
    changed = function(rows, accounts)
    require_result(label, changed,
                   [{"account": "missing", "count": 1, "total": 4},
                    {"account": "changed", "count": 1, "total": -17},
                    {"account": "missing", "count": 1, "total": 4}])
    if retained_ids & {id(item) for item in changed}:
        raise ValueError(f"{label}: reuses output dictionaries across calls")
    if retained != retained_snapshot:
        raise ValueError(f"{label}: changed-input call changed a retained result")
    if (rows, accounts) != before:
        raise ValueError(f"{label}: input mutated")
    return len(examples) + 2


def sample(label, function, rows, accounts, expected, repetitions):
    before = copy.deepcopy((rows, accounts))
    outputs = []
    started = time.perf_counter_ns()
    for _ in range(repetitions):
        outputs.append(function(rows, accounts))
    seconds = (time.perf_counter_ns() - started) / 1_000_000_000
    for output in outputs:
        require_result(label, output, expected)
    if (rows, accounts) != before:
        raise ValueError(f"{label}: input mutated")
    return {"seconds": seconds, "calls": repetitions,
            "completed_summaries": sum(len(output) for output in outputs)}


def main():
    functions = {"reference": reference.summarize, "candidate": candidate.summarize}
    example_counts = {label: check_examples(label, function)
                      for label, function in functions.items()}
    rows, accounts = make_workload()
    original = copy.deepcopy((rows, accounts))
    expected = reference.summarize(rows, accounts)
    if (rows, accounts) != original:
        raise ValueError("reference: input mutated")
    for label, function in functions.items():
        sample(label, function, rows, accounts, expected, 1)
    repetitions = 2
    pairs = []
    for index in range(6):
        order = ["reference", "candidate"] if index % 2 == 0 else ["candidate", "reference"]
        pair = {"order": order}
        for label in order:
            pair[label] = sample(label, functions[label], rows, accounts, expected, repetitions)
        pair["reference_over_candidate"] = pair["reference"]["seconds"] / pair["candidate"]["seconds"]
        pairs.append(pair)
    summary = {}
    for label in functions:
        values = [pair[label]["seconds"] / repetitions for pair in pairs]
        summary[label] = {"median_seconds_per_call": statistics.median(values),
                          "min_seconds_per_call": min(values),
                          "max_seconds_per_call": max(values)}
    ratios = [pair["reference_over_candidate"] for pair in pairs]
    summary["paired_reference_over_candidate"] = {
        "median": statistics.median(ratios), "min": min(ratios), "max": max(ratios)}
    root = Path(__file__).resolve().parent
    sources = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
               for name in ("candidate.py", "reference.py", "workload.py", "benchmark.py", "SPEC.md")}
    print(json.dumps({"runtime": {"python": platform.python_version(),
                                  "implementation": platform.python_implementation(),
                                  "platform": platform.platform()},
                      "source_sha256": sources,
                      "workload": {"input_rows": len(rows),
                                   "populated_accounts": len({row["account"] for row in rows}),
                                   "requested_accounts": len(accounts),
                                   "repetitions_per_sample": repetitions, "paired_samples": len(pairs)},
                      "correctness": {"contract_examples": example_counts,
                                      "all_outputs_equal": True, "inputs_unchanged": True},
                      "method": "One warm-up each, six alternating pairs, two calls per sample; every output checked outside timing.",
                      "pairs": pairs, "summary": summary}, sort_keys=True))


if __name__ == "__main__":
    main()
'''

AGGREGATION_SKILL = '''---
name: measure-account-summaries
description: Check account-summary correctness and measure performance when summarize implementations or performance claims change.
---

# Measure account summaries

Work from the project root with Python 3.9 or newer and the standard library.
Read SPEC.md, workload.py and benchmark.py before interpreting a result. The
frozen reference establishes the baseline. Check the contract on empty input,
missing and repeated requests, signed deltas, input preservation and fresh output
dictionaries before treating either implementation's work as complete.

Run `python -B benchmark.py`. It checks hand-worked examples, warms each function
once, then measures six pairs of two calls each, alternating which function runs
first. Each timed output is compared with the frozen reference outside the timed
region, and inputs are checked for mutation. The workload has 6,000 rows, 160
populated accounts, repeated requests and missing accounts. Keep the workload,
reference, harness and contract fixed when comparing an implementation change.

Retain the actual command, runtime and source hashes, per-pair results, medians
and ranges. Compare an unchanged baseline run with the changed candidate under
the same conditions; preserve the earlier observations. These small local
measurements support a conclusion only for the stated work and environment.
Investigate correctness failures before making a performance claim, and report
variation and relevant costs instead of inferring a universal speedup.

A measurement-only request leaves all files unchanged, including added reports;
use `-B` and keep observations in the response or tool output. If the user later
authorizes an implementation change, preserve these frozen inputs and reuse
the same correctness and measurement procedure after the change.
'''

SERIALIZERS_OLD = '''import json


def render_invoice(item):
    return json.dumps({"kind": "invoice", "id": item["id"],
                       "amount": f'{item["pence"] // 100}.{item["pence"] % 100:02d}'},
                      sort_keys=True, separators=(",", ":"))


def render_receipt(item):
    return json.dumps({"kind": "receipt", "id": item["id"],
                       "amount": f'{item["pence"] // 100}.{item["pence"] % 100:02d}'},
                      sort_keys=True, separators=(",", ":"))
'''

SERIALIZERS_NEW = '''import json


def render(item, kind):
    return json.dumps({"kind": kind, "id": item["id"],
                       "amount": f'{item["pence"] // 100}.{item["pence"] % 100:02d}'},
                      sort_keys=True, separators=(",", ":"))
'''

SERIALIZERS_BRIDGE = '''from reports import render


def render_invoice(item):
    return render(item, "invoice")


def render_receipt(item):
    return render(item, "receipt")
'''

DISPATCH = '''import importlib
import json
from pathlib import Path


def render_saved_route(name, item):
    routes = json.loads(Path(__file__).with_name("routes.json").read_text())
    module, symbol = routes[name].rsplit(".", 1)
    return getattr(importlib.import_module(module), symbol)(item)
'''

WORKFLOW_CASES = {
    "formal-create": {
        "prompt": "Create reusable verification for the worker lease's safety promise in SPEC.md, including a project-local skill future agents can follow. Check the bounded schedules of the actual cooperative implementation and explain the result and limits. Keep production code unchanged and leave the work local.",
        "files": {"lease.py": LEASE_GOOD, "SPEC.md": LEASE_SPEC},
        "kind": "manual", "protected": ["lease.py", "SPEC.md"],
        "probe": "lease", "probe_expect": {"successful": True, "holds": True},
        "needs_skill": True,
        "review": [
            "A discoverable project skill names the property, harm, covered symbols, bounds, assumptions and concrete rerun command.",
            "The bounded check executes the real cooperative transitions and explores all stated schedules; it is not sampled testing or a copied atomic model.",
            "The agent checks nonempty exploration, selected obligations, completed runs and source correspondence; it labels this finite scope honestly.",
            "Following the generated skill against a relevant temporary code mutation detects the violation; the original code and baseline result are restored.",
            "The skill records honest source correspondence (commit when available, otherwise explicit source hashes), reproducible runtime and how later changes require revalidation.",
            "Judge actual reads, scripts, outputs and replay evidence; the evaluator's independent lease probe does not establish that the authored checker works.",
        ],
    },
    "formal-maintain": {
        "prompt": "The lease implementation changed. Bring the existing verification and project skill into line with the current code, run them and explain what the result means. Do not change lease.py or SPEC.md; keep product findings visible and leave the work local.",
        "files": {"lease.py": LEASE_SPLIT, "SPEC.md": LEASE_SPEC,
                  "verification/model.py": LEASE_GOOD,
                  "verification/check_lease.py": LEASE_CHECK,
                  "verification/last-synced/lease.py": LEASE_GOOD,
                  "verification/coverage.json": json.dumps(LEASE_COVERAGE, indent=2) + "\n",
                  ".agents/skills/verify-lease/SKILL.md": LEASE_SKILL},
        "kind": "manual", "protected": ["lease.py", "SPEC.md"],
        "probe": "lease", "probe_expect": {"successful": True, "holds": False},
        "needs_skill": True,
        "review": [
            "The agent runs the initial checker, compares the recorded source hash and old source with current code, and notices changed atomicity.",
            "Verification is updated from implementation semantics; the valid safety promise is not weakened to preserve the old pass.",
            "A failing schedule is replayed against real lease.py, with domain-level steps and harm; model drift is distinguished from the product bug it reveals.",
            "Product code remains unchanged. The prior pass is identified as evidence about an outdated model, not current safety.",
            "Coverage and the project skill describe what was actually checked. Source hashes are not claimed as Git commits; blocked correspondence is not marked synchronized.",
        ],
    },
    "application-create": {
        "prompt": "Give future agents a project-local verification skill for Pocket notes. Make its launch and environment check, feature-driving steps, persistent-effect evidence and cleanup reproducible, then follow it on the app. Keep notes.py and SPEC.md unchanged and leave the work local.",
        "followup_prompt": "Use this project's verification instructions to check adding a note, repeating the same request, listing it from another process and removing it. Preserve the evidence after cleaning up only your own disposable state. Do not edit product code or verification instructions.",
        "files": {"notes.py": NOTES_GOOD, "SPEC.md": NOTES_SPEC},
        "kind": "manual", "protected": ["notes.py", "SPEC.md"],
        "probe": "notes", "probe_expect": {"successful": True},
        "needs_skill": True,
        "review": [
            "A discoverable project skill gives exact local commands, runtime checks, per-run store isolation, expected observations and cleanup ownership.",
            "Its feature map covers list, add, same-request retry, conflicting-ID rejection, remove, repeated removal and preservation of other notes.",
            "The live rehearsal begins with a missing empty store, drives real CLI processes, reads persisted state and verifies forbidden duplicate/conflicting writes.",
            "Evidence remains accessible after owned state cleanup. No existing user store or unrelated file is removed.",
            "The generated procedure is usable by a fresh agent with the followup prompt; creation evidence is not automatically reuse evidence.",
        ],
    },
    "measured-comparison": {
        "prompt": "The benchmark suggests candidate.py is faster than reference.py. Can we claim a throughput improvement for the conversion contract in SPEC.md? Run the relevant checks and report the evidence and limits without editing files.",
        "files": {"reference.py": MEASURE_REFERENCE, "candidate.py": MEASURE_PARTIAL,
                  "benchmark.py": MEASURE_BENCH,
                  ".agents/skills/benchmark-conversion/SKILL.md": MEASURE_SKILL,
                  "SPEC.md": "# Conversion contract\n\nconvert(rows) returns one JSON string per input row, preserving order and all fields. It must not mutate its input. Python 3.9+, standard library. Run the supplied timing with `python benchmark.py`.\n"},
        "kind": "manual", "protected": "all",
        "probe": "conversion", "probe_expect": {"successful": True, "outputs_equal": False},
        "review": [
            "Direct measurement work discovers and reads the project benchmark skill without the task naming it; applicable workload and correctness instructions shape the checks.",
            "The agent checks output correctness and actual completed work before accepting throughput calculated from input count.",
            "It identifies that the candidate omits rows and that the timing comparison cannot support an improvement for the stated contract.",
            "Observed time is separated from a valid speedup claim; no invented reliable ratio, tuning comparison or causal conclusion is reported.",
            "Files remain unchanged and actual commands/results support the explanation.",
        ],
    },
    "measure-to-improve": {
        "prompt": "Measure the current account-summary performance against the contract in SPEC.md. Run the supplied workload, check the output, and report the timings and limits. Do not change, add or remove any files.",
        "checkpoint": True,
        "second_prompt": "Use your findings to improve the performance of candidate.py while preserving the account-summary contract. Keep the supplied reference, workload, benchmark and project measurement instructions unchanged. Add focused tests or local evidence where useful, demonstrate correctness and comparable before/after measurements, and leave the finished change local.",
        "files": {"candidate.py": AGGREGATION_REFERENCE,
                  "reference.py": AGGREGATION_REFERENCE,
                  "SPEC.md": AGGREGATION_SPEC,
                  "workload.py": AGGREGATION_WORKLOAD,
                  "benchmark.py": AGGREGATION_BENCHMARK,
                  ".agents/skills/measure-account-summaries/SKILL.md": AGGREGATION_SKILL},
        "kind": "manual",
        "protected": ["SPEC.md", "reference.py", "workload.py", "benchmark.py", "TASK.md",
                      ".agents/skills/measure-account-summaries/SKILL.md"],
        "probe": "aggregation", "probe_expect": {"successful": True, "outputs_equal": True},
        "review": [
            "The first turn uses Measure for the measurement-only request, discovers and reads the project measurement skill, checks equal correct work and reports observed baseline timings with runtime and scope; every workspace file remains unchanged.",
            "After the explicit second user request in the same conversation, the agent moves implementation ownership to Workflows while retaining relevant measurement guidance and completed baseline evidence. Judge actual skill reads and actions, not assertions of a transition.",
            "The second turn makes a useful production optimization in candidate.py, preserving all account-summary semantics, input preservation and fresh output dictionaries. A no-op or a faster implementation that skips required work is not accepted.",
            "Focused checks exercise real implementations and expected results justified by the contract, including repeated/missing accounts and zero/negative deltas; any added tests have meaningful behavior sensitivity.",
            "Actual before/after measurements use the same frozen workload and harness, correctly completed outputs, repeated paired observations, source identities and runtime. Report the observed effect, variation and relevant cost; no universal or threshold-based speedup claim follows from this fixture.",
            "The contract, reference, workload, benchmark and supplied project skill stay unchanged; added tests or evidence serve the authorized change, and the finished work remains local. The independent probe establishes correctness examples only, not useful optimization or the agent's measurement and routing process.",
        ],
    },
    "refactor-contract": {
        "prompt": "Consolidate the duplicated rendering in handlers.py into reports.py. Preserve the existing serialized output and callers, including saved routes. Keep the change local and show the evidence that behavior is preserved.",
        "files": {"handlers.py": SERIALIZERS_OLD, "dispatch.py": DISPATCH,
                  "routes.json": '{"invoice":"handlers.render_invoice","receipt":"handlers.render_receipt"}\n',
                  "SPEC.md": "# Saved rendering routes\n\nExisting handlers.render_invoice and handlers.render_receipt import paths are public and appear in persisted route records. Preserve them. Positive integer pence become a two-decimal amount string. Output JSON uses sorted keys, compact separators, kind, id and amount, with no newline. Rendering must not mutate its input. Python 3.9+, standard library.\n"},
        "kind": "manual", "protected": ["SPEC.md", "routes.json", "dispatch.py"],
        "probe": "saved_routes", "probe_expect": {"successful": True},
        "review": [
            "The agent inspects direct and dynamically resolved consumers before changing public names and records a behavior baseline.",
            "Duplicated formatting is consolidated while saved routes and public import paths continue to work.",
            "Before/after evidence includes byte-identical serialized outputs and unchanged inputs, not merely successful imports or compilation.",
            "Compatibility code that serves the explicit persisted/public contract is preserved; unrelated changes are absent.",
        ],
    },
}
