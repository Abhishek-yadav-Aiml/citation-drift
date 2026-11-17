#!/usr/bin/env bash
set -u
echo "=== macOS ==="
sw_vers || true
echo "=== Architecture ==="
uname -m
echo "=== Python ==="
python --version || true
python -c "import platform,sys; print(platform.machine()); print(sys.executable)" || true
echo "=== Xcode command line tools ==="
xcode-select -p || true
echo "=== Disk ==="
df -h . || true
echo "=== NVIDIA diagnostic (expected not to apply to M1) ==="
command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi || echo "nvidia-smi not applicable/not found"
