@echo off
setlocal
cd /d "%~dp0frontend"

echo.
echo === StatSkill AI Frontend ===
echo Working directory:
cd
echo.

where node >nul 2>&1
if errorlevel 1 (
  echo ERROR: Node.js is not available on PATH.
  echo Install/repair Node.js, then run this file again.
  pause
  exit /b 1
)

node --version
if exist "C:\Program Files\nodejs\npm.cmd" (
  set "NPM_CMD=C:\Program Files\nodejs\npm.cmd"
) else (
  where npm.cmd >nul 2>&1
  if not errorlevel 1 (
    set "NPM_CMD=npm.cmd"
  ) else (
    where npm.exe >nul 2>&1
    if not errorlevel 1 (
      set "NPM_CMD=npm.exe"
    ) else (
      where npm >nul 2>&1
      if not errorlevel 1 (
        set "NPM_CMD=npm"
      ) else (
        echo ERROR: npm is not available on PATH.
        pause
        exit /b 1
      )
    )
  )
)

echo Using: %NPM_CMD%
call "%NPM_CMD%" --version
if errorlevel 1 (
  echo ERROR: npm could not start.
  echo Check the Node.js installation.
  pause
  exit /b 1
)

echo.
echo Installing frontend dependencies...
call "%NPM_CMD%" install
if errorlevel 1 (
  echo.
  echo ERROR: npm install failed.
  echo The application source was not changed by this script.
  pause
  exit /b 1
)

echo.
echo Starting Vite...
call "%NPM_CMD%" run dev
pause
