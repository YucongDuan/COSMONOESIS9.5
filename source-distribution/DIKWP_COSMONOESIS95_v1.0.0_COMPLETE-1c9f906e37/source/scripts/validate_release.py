from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
env = dict(os.environ)
env["PYTHONPATH"] = str(ROOT / "src")

def run(args):
    p = subprocess.run([sys.executable, *args], cwd=ROOT, env=env, capture_output=True, text=True)
    return {"args": args, "returncode": p.returncode, "stdout": p.stdout[-20000:], "stderr": p.stderr[-20000:]}

results = []
results.append(run(["run.py", "doctor"]))
results.append(run(["-m", "unittest", "discover", "-s", "tests", "-v"]))
with tempfile.TemporaryDirectory() as td:
    out = Path(td) / "demo"
    results.append(run(["run.py", "demo", "--out", str(out)]))
    results.append(run(["run.py", "verify", str(out)]))
report = {
    "system": "DIKWP-COSMONOESIS 9.5",
    "valid": all(x["returncode"] == 0 for x in results),
    "steps": results,
    "automatic_external_action_authority": 0,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if report["valid"] else 2)
