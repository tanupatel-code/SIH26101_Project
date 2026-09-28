@echo off
setlocal
echo ==================================================
echo  Starting StatSkill AI Windows Deployment
echo ==================================================

where docker >nul 2>&1
if not errorlevel 1 (
    echo Docker detected. Deploying containerized services...
    docker compose down 2>nul
    docker compose up --build -d
    echo Containerized deployment complete!
    echo Backend: http://localhost:8000
    echo Frontend: http://localhost:80
    pause
    exit /b 0
)

echo Docker not detected. Performing local production build...
cd /d "%~dp0..\backend"
echo [1/2] Installing backend dependencies...
python -m pip install -r requirements.txt

cd /d "%~dp0..\frontend"
echo [2/2] Building frontend bundle...
call npm install
call npm run build

echo.
echo Production build finished!
echo Launch backend with START_BACKEND.bat
echo Launch frontend with START_FRONTEND.bat
pause
