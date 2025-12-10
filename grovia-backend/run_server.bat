@echo off
echo ================================================
echo GROVIA Backend Server Starter
echo ================================================
echo.

cd /d "%~dp0"

echo [INFO] Checking Python installation...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found in PATH!
    echo Please install Python or add it to PATH
    pause
    exit /b 1
)
echo.

echo [INFO] Checking uvicorn installation...
python -m uvicorn --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Uvicorn not found. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
)
echo.

echo [INFO] Starting FastAPI server...
echo Server will run at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Press CTRL+C to stop the server
echo.
echo ================================================
echo.

REM Set PYTHONPATH to current directory to ensure app module is found
set PYTHONPATH=%CD%
echo [DEBUG] Current directory: %CD%
echo [DEBUG] PYTHONPATH: %PYTHONPATH%
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
