@echo off
REM ============================================================
REM OpenClaw Memory System - Startup Registration
REM ============================================================
REM 
REM This batch file registers the memory system with Windows startup
REM It MUST be run as Administrator
REM
REM Right-click this file and select "Run as administrator"
REM

echo.
echo ============================================================
echo OPENCLAW MEMORY SYSTEM - STARTUP REGISTRATION
echo ============================================================
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] This script must be run as Administrator
    echo.
    echo Please:
    echo   1. Right-click this file
    echo   2. Select "Run as administrator"
    echo   3. Click "Yes" in the UAC dialog
    echo.
    pause
    exit /b 1
)

echo [OK] Running as Administrator
echo.

REM Navigate to script directory
cd /d "C:\Users\haujo\projects\DEV\memory_management"

REM Run the PowerShell script
powershell -NoProfile -ExecutionPolicy Bypass -File ".\register_memory_startup.ps1"

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo [SUCCESS] Memory system registered with Windows startup
    echo ============================================================
    echo.
    echo Next steps:
    echo   1. Restart Windows (optional - takes effect at next boot)
    echo   2. Verify with: .\check_memory_startup_status.ps1
    echo   3. At next boot, memory system will start automatically
    echo.
    pause
) else (
    echo.
    echo [ERROR] Registration failed
    echo Please check the output above for details
    echo.
    pause
    exit /b 1
)
