@echo off
title Blue Carbon Registry System Startup
color 0A

echo.
echo ================================================================
echo                 Blue Carbon Registry System
echo                       Startup Script
echo ================================================================
echo.

cd /d "%~dp0"

echo [0/5] Checking for previous projects...
python auto-backup.py restore
echo.

echo [1/5] Starting Hardhat blockchain node with persistence...
if not exist "blue-carbon-contracts\cache" mkdir "blue-carbon-contracts\cache"
start "Hardhat Node" cmd /k "cd blue-carbon-contracts && npx hardhat node --hostname 0.0.0.0"
echo   Waiting for Hardhat node to start...
timeout /t 10 /nobreak > nul

echo [2/5] Starting FastAPI backend server...
start "Backend API" cmd /k "cd blue-carbon-backend && python -m uvicorn main:app --reload --port 8000"
timeout /t 3 /nobreak > nul

echo [3/5] Deploying smart contracts...
echo   Waiting for node to be ready...
timeout /t 8 /nobreak > nul
start "Contract Deployment" cmd /k "cd blue-carbon-contracts && npx hardhat run scripts/deploy.mjs --network localhost"
timeout /t 2 /nobreak > nul

echo [4/5] Starting Next.js frontend...
start "Frontend" cmd /k "cd bluecarbon-frontend && npm run dev"

echo [5/5] Creating backup of current session...
python auto-backup.py backup

echo.
echo ================================================================
echo                     Startup Complete!
echo ================================================================
echo.
echo Services are starting in separate windows:
echo   • Hardhat Node:      http://localhost:8545
echo   • Backend API:       http://localhost:8000
echo   • API Documentation: http://localhost:8000/docs  
echo   • Frontend App:      http://localhost:3000
echo.
echo The AI verification system is now ready for before/after
echo image analysis and dynamic carbon credit calculation!
echo.
echo Press any key to close this window (services will continue)...
pause > nul