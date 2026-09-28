@echo off
setlocal
cd /d "%~dp0.."

echo ========================================================
echo  Running StatSkill AI Full Verification & Test Suites
echo ========================================================
echo.

echo [1/3] Running Mypy Static Type Checking...
python -m mypy --explicit-package-bases --ignore-missing-imports backend/
if errorlevel 1 (
    echo [ERROR] Mypy typing check failed.
    pause
    exit /b 1
)
echo [OK] Mypy passed!
echo.

echo [2/3] Running Full Pytest Suite (90 Test Cases)...
python -m pytest -v
if errorlevel 1 (
    echo [ERROR] Pytest execution encountered failures.
    pause
    exit /b 1
)
echo [OK] All 90 Pytest test cases passed!
echo.

echo [3/3] Testing Frontend Production Bundle Build...
cd frontend
call npm run build
if errorlevel 1 (
    echo [ERROR] Frontend build failed.
    pause
    exit /b 1
)
cd ..
echo [OK] Frontend bundle built successfully!
echo.

echo ========================================================
echo  All 90 Test Cases, Type Checks, and Builds Passed!
echo ========================================================
pause
