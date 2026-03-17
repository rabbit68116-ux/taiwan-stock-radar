@echo off
setlocal
title Taiwan Stock Radar Desktop Launcher

cd /d "%~dp0"

echo ==========================================
echo Taiwan Stock Radar Windows Launcher
echo ==========================================
echo.

set "PY_CMD="
where py >nul 2>&1
if %errorlevel%==0 (
  set "PY_CMD=py"
) else (
  where python >nul 2>&1
  if %errorlevel%==0 (
    set "PY_CMD=python"
  )
)

if "%PY_CMD%"=="" (
  echo [ERROR] 找不到 Python。請先安裝 Python 3.10+ 並勾選加入 PATH。
  echo [ERROR] Python was not found. Install Python 3.10+ and add it to PATH first.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [INFO] 建立本地虛擬環境 .venv ...
  %PY_CMD% -m venv .venv
  if errorlevel 1 (
    echo [ERROR] 無法建立 .venv，請確認 Python venv 模組可用。
    echo [ERROR] Failed to create .venv. Make sure the Python venv module is available.
    pause
    exit /b 1
  )
)

set "VENV_PY=.venv\Scripts\python.exe"

echo [INFO] 檢查桌面版依賴...
%VENV_PY% -c "import PySide6" >nul 2>&1
if errorlevel 1 (
  echo [INFO] 第一次啟動或缺少依賴，正在安裝 requirements-desktop.txt ...
  %VENV_PY% -m pip install -r requirements-desktop.txt
  if errorlevel 1 (
    echo [ERROR] 套件安裝失敗，請檢查網路或 Python/PIP 設定。
    echo [ERROR] Package installation failed. Check your network or Python/PIP setup.
    pause
    exit /b 1
  )
)

echo [INFO] 啟動 Taiwan Stock Radar Desktop ...
%VENV_PY% apps\windows\main.py
set "APP_EXIT=%errorlevel%"

if not "%APP_EXIT%"=="0" (
  echo.
  echo [ERROR] 桌面版異常結束，代碼 %APP_EXIT%。
  echo [ERROR] The desktop app exited with code %APP_EXIT%.
  pause
  exit /b %APP_EXIT%
)

exit /b 0
