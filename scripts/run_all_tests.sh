#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "========================================================"
echo " Running StatSkill AI Full Verification & Test Suites"
echo "========================================================"

echo ">> [1/3] Running Mypy Static Type Checking..."
python3 -m mypy --explicit-package-bases --ignore-missing-imports backend/
echo ">> [OK] Mypy passed!"

echo ">> [2/3] Running Full Pytest Suite (90 Test Cases)...
python3 -m pytest -v
echo ">> [OK] All 90 Pytest test cases passed!"

echo ">> [3/3] Testing Frontend Production Bundle Build..."
cd frontend
npm run build
cd ..
echo ">> [OK] Frontend bundle built successfully!"

echo "========================================================"
echo " All 90 Test Cases, Type Checks, and Builds Passed!"
echo "========================================================"
