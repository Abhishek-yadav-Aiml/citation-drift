#!/usr/bin/env python3
"""Non-invasive environment diagnostic. Does not download models or datasets."""
from __future__ import annotations

import importlib
import json
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

report = {
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "project_root": str(ROOT),
    "platform": platform.platform(),
    "system": platform.system(),
    "machine": platform.machine(),
    "python_version": sys.version,
    "python_executable": sys.executable,
    "checks": {},
    "overall_status": "UNKNOWN",
}

def add(name, status, details):
    report["checks"][name] = {"status": status, "details": details}

def command_output(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return {"returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    except Exception as exc:
        return {"error": repr(exc)}

# OS diagnostics
if platform.system() == "Darwin":
    add("macos_version", "INFO", command_output(["sw_vers"]))
    add("xcode_command_line_tools", "INFO", command_output(["xcode-select", "-p"]))
else:
    add("os", "INFO", platform.platform())

add("architecture", "INFO", platform.machine())
add("python", "INFO", sys.version)

# Core imports and versions
modules = {
    "numpy": "numpy",
    "pandas": "pandas",
    "sklearn": "scikit-learn",
    "rank_bm25": "rank-bm25",
    "pypdf": "pypdf",
    "yaml": "PyYAML",
    "psutil": "psutil",
}
missing = []
for module_name, package_name in modules.items():
    try:
        mod = importlib.import_module(module_name)
        version = getattr(mod, "__version__", "version_not_exposed")
        add(f"package:{package_name}", "PASS", {"module": module_name, "version": version})
    except Exception as exc:
        missing.append(package_name)
        add(f"package:{package_name}", "FAIL", {"error": repr(exc)})

# PyTorch and MPS
try:
    import torch
    torch_info = {
        "version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "mps_built": bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_built()),
        "mps_available": bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()),
    }
    add("pytorch_import", "PASS", torch_info)

    x_cpu = torch.tensor([1.0, 2.0])
    y_cpu = (x_cpu * 2).sum().item()
    add("pytorch_cpu_tensor_test", "PASS" if y_cpu == 6.0 else "FAIL", {"result": y_cpu})

    if torch_info["mps_available"]:
        try:
            x_mps = torch.tensor([1.0, 2.0], device="mps")
            y_mps = (x_mps * 2).sum().item()
            add("pytorch_mps_tensor_test", "PASS" if y_mps == 6.0 else "FAIL",
                {"result": y_mps, "device": str(x_mps.device)})
        except Exception as exc:
            add("pytorch_mps_tensor_test", "FAIL", {"error": repr(exc), "traceback": traceback.format_exc()})
    else:
        add("pytorch_mps_tensor_test", "WARN", "MPS unavailable; CPU fallback remains possible.")
except Exception as exc:
    add("pytorch_import", "FAIL", {"error": repr(exc), "traceback": traceback.format_exc()})
    add("pytorch_cpu_tensor_test", "SKIP", "PyTorch import failed.")
    add("pytorch_mps_tensor_test", "SKIP", "PyTorch import failed.")

# Package consistency
try:
    p = subprocess.run([sys.executable, "-m", "pip", "check"], capture_output=True, text=True, timeout=60)
    add("pip_check", "PASS" if p.returncode == 0 else "FAIL",
        {"returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()})
except Exception as exc:
    add("pip_check", "WARN", {"error": repr(exc)})

statuses = [v["status"] for v in report["checks"].values()]
if "FAIL" in statuses:
    report["overall_status"] = "FAIL"
elif "WARN" in statuses or missing:
    report["overall_status"] = "WARN"
else:
    report["overall_status"] = "PASS"

json_path = RESULTS / "environment_verification.json"
txt_path = RESULTS / "environment_verification.txt"
json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

lines = [
    "CITATION DRIFT ENVIRONMENT VERIFICATION",
    f"Timestamp UTC: {report['timestamp_utc']}",
    f"Overall status: {report['overall_status']}",
    f"Platform: {report['platform']}",
    f"Architecture: {report['machine']}",
    f"Python: {sys.version.split()[0]}",
    f"Executable: {sys.executable}",
    "",
]
for name, item in report["checks"].items():
    details = item["details"]
    lines.append(f"[{item['status']}] {name}: {details}")
lines += ["", f"JSON log: {json_path}", f"Text log: {txt_path}"]
txt_path.write_text("\n".join(lines), encoding="utf-8")

print("\n".join(lines))
print("\nDiagnostic complete. This test does not verify AlignScore inference or checkpoint compatibility.")
