"""Run trusted evaluator checks in a disposable candidate workspace."""
import importlib
import io
import json
import sys
import unittest
from pathlib import Path


def probe(work, mode):
    sys.path.insert(0, str(work))
    if mode == "suite":
        suite = unittest.defaultTestLoader.discover(str(work / "tests"), pattern="test*.py")
        result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
        return {"run": result.testsRun, "skipped": len(result.skipped),
                "failures": len(result.failures), "errors": len(result.errors),
                "expected_failures": len(result.expectedFailures),
                "successful": result.wasSuccessful()}
    if mode == "billing":
        total = importlib.import_module("billing").total
        for amounts, expected in [([], 0), ([2, 3], 5), ([4, -1], 3), ([0], 0)]:
            original = list(amounts)
            assert total(amounts) == expected, (amounts, expected)
            assert amounts == original, "Input list was changed"
    elif mode == "delivery":
        deliver = importlib.import_module("delivery").deliver
        outbox = []
        assert deliver(outbox, "a", "hello") == "a"
        assert deliver(outbox, "a", "hello") == "a"
        assert outbox == [("a", "hello")], outbox
        try:
            deliver(outbox, "a", "different")
        except ValueError:
            pass
        else:
            raise AssertionError("Conflicting key was accepted")
        assert outbox == [("a", "hello")], outbox
        deliver(outbox, "b", "hello")
        assert outbox == [("a", "hello"), ("b", "hello")], outbox
    else:
        raise ValueError("Unknown probe")
    return {"successful": True}


if __name__ == "__main__":
    work, mode, result_path = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3])
    try:
        result = probe(work, mode)
    except Exception as error:
        result = {"successful": False, "error": f"{type(error).__name__}: {error}"}
    result_path.write_text(json.dumps(result, indent=2) + "\n")
