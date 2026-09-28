@echo off
setlocal
cd /d "%~dp0backend"

echo.
echo === StatSkill AI FastAPI Backend ===
echo Working directory:
cd
echo.

set "PY_CMD=python"
python -m pip --version >nul 2>&1
if errorlevel 1 (
  py -3.12 -m pip --version >nul 2>&1
  if not errorlevel 1 (
    set "PY_CMD=py -3.12"
  ) else (
    where py >nul 2>&1
    if not errorlevel 1 (
      set "PY_CMD=py"
    ) else (
      where python >nul 2>&1
      if errorlevel 1 (
        echo ERROR: Python is not available on PATH.
        pause
        exit /b 1
      )
    )
  )
)

echo Using Python command: %PY_CMD%
%PY_CMD% --version
echo.
echo Installing backend dependencies...
%PY_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo WARNING: Some pip dependencies could not be re-installed. Attempting to start server...
)

echo.
echo Starting FastAPI on http://127.0.0.1:8000 ...
%PY_CMD% -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause

