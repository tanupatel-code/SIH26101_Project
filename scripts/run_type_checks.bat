@echo off
setlocal
cd /d "%~dp0.."

echo ========================================================
echo  Running StatSkill AI Type Case Checks & Static Typing
echo ========================================================
echo.

echo [1/2] Running Mypy Static Type Analysis...
python -m mypy --explicit-package-bases --ignore-missing-imports backend/
if errorlevel 1 (
    echo.
    echo [ERROR] Mypy found static type errors.
    pause
    exit /b 1
)
echo [OK] Mypy static type analysis passed!
echo.

echo [2/2] Running Pytest Type Case & Schema Validation Tests...
python -m pytest backend/tests/test_type_cases.py -v
if errorlevel 1 (
    echo.
    echo [ERROR] Pytest type case tests failed.
    pause
    exit /b 1
)
echo.
echo ========================================================
echo  All Type Checks & Type Case Tests Passed (100%% Success)
echo ========================================================
pause
