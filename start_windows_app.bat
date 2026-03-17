@echo off
setlocal EnableExtensions
title Taiwan Stock Radar Desktop Launcher

cd /d "%~dp0"

echo ==========================================
echo Taiwan Stock Radar Windows Launcher
echo ==========================================
echo.

set "PY_CMD="
where py >nul 2>nul
if not errorlevel 1 (
  set "PY_CMD=py"
)

if not defined PY_CMD (
  where python >nul 2>nul
  if not errorlevel 1 (
    set "PY_CMD=python"
  )
)

if not defined PY_CMD (
  echo [ERROR] Python 3.10+ was not found on PATH.
  echo [ERROR] Install Python and enable "Add Python to PATH", then try again.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [INFO] Creating local virtual environment .venv ...
  "%PY_CMD%" -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create .venv.
    echo [ERROR] Make sure the Python venv module is available.
    pause
    exit /b 1
  )
)

set "VENV_PY=.venv\Scripts\python.exe"

echo [INFO] Checking desktop dependencies...
"%VENV_PY%" -c "import PySide6" >nul 2>nul
if errorlevel 1 (
  echo [INFO] Installing requirements-desktop.txt ...
  "%VENV_PY%" -m pip install -r requirements-desktop.txt
  if errorlevel 1 (
    echo [ERROR] Package installation failed.
    echo [ERROR] Check your network, Python, and pip configuration.
    pause
    exit /b 1
  )
)

echo [INFO] Starting Taiwan Stock Radar Desktop...
"%VENV_PY%" apps\windows\main.py
set "APP_EXIT=%errorlevel%"

if not "%APP_EXIT%"=="0" (
  echo.
  echo [ERROR] The desktop app exited with code %APP_EXIT%.
  pause
  exit /b %APP_EXIT%
)

exit /b 0
