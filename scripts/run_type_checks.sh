#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "========================================================"
echo " Running StatSkill AI Type Case Checks & Static Typing"
echo "========================================================"

echo ">> [1/2] Running Mypy Static Type Analysis..."
python3 -m mypy --explicit-package-bases --ignore-missing-imports backend/
echo ">> [OK] Mypy static type analysis passed!"

echo ">> [2/2] Running Pytest Type Case & Schema Validation Tests..."
python3 -m pytest backend/tests/test_type_cases.py -v

echo "========================================================"
echo " All Type Checks & Type Case Tests Passed (100% Success)"
echo "========================================================"
