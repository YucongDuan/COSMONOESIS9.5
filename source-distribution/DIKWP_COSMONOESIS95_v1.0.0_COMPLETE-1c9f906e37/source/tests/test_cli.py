from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "run.py"


def call(*args: str) -> tuple[int, dict]:
    env = dict(os.environ)
    proc = subprocess.run([sys.executable, str(RUN), *args], cwd=ROOT, env=env, capture_output=True, text=True)
    stream = proc.stdout if proc.stdout.strip() else proc.stderr
    return proc.returncode, json.loads(stream)


class CliTests(unittest.TestCase):
    def test_doctor(self):
        code, result = call("doctor")
        self.assertEqual(code, 0)
        self.assertTrue(result["valid"])

    def test_normalize(self):
        code, result = call("normalize", "道", "--context", "无为与自然")
        self.assertEqual(code, 0)
        self.assertEqual(result["out_of_space_residual"], 0.0)

    def test_compare(self):
        code, result = call("compare", "ubuntu", "仁")
        self.assertEqual(code, 0)
        self.assertFalse(result["comparison"]["equivalence_claim"])

    def test_map_centroid(self):
        code, result = call("map", "centroid")
        self.assertEqual(code, 0)
        self.assertEqual(result["out_of_space_residual"], 0.0)

    def test_assess_file(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "candidate.json"
            p.write_text(json.dumps({"id":"x","name_cn":"测试","scores":{"C.D1_EVENT_REGISTRATION":0.8}}), encoding="utf-8")
            code, result = call("assess", str(p))
            self.assertEqual(code, 0)
            self.assertIsNone(result["binary_consciousness_certificate"])

    def test_compile_and_verify(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            code, compiled = call("demo", "--out", str(out))
            self.assertEqual(code, 0)
            code, verified = call("verify", str(out))
            self.assertEqual(code, 0)
            self.assertTrue(verified["valid"])


if __name__ == "__main__":
    unittest.main()
