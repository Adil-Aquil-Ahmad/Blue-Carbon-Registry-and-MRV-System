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

echo [1/4] Starting Hardhat blockchain node...
start "Hardhat Node" cmd /k "cd blue-carbon-contracts && npx hardhat node"
timeout /t 5 /nobreak > nul

echo [2/4] Starting FastAPI backend server...
start "Backend API" cmd /k "cd blue-carbon-backend && python -m uvicorn main:app --reload --port 8000"
timeout /t 3 /nobreak > nul

echo [3/4] Deploying smart contracts...
timeout /t 5 /nobreak > nul
start "Contract Deployment" cmd /k "cd blue-carbon-contracts && npx hardhat run scripts/deploy.mjs --network localhost"
timeout /t 2 /nobreak > nul

echo [4/4] Starting Next.js frontend...
start "Frontend" cmd /k "cd bluecarbon-frontend && npm run dev"

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