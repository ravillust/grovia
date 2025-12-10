# GROVIA Backend Server Starter (PowerShell)
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "GROVIA Backend Server Starter" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Find correct Python installation (skip msys64)
Write-Host "[INFO] Finding Python installation..." -ForegroundColor Yellow
$pythonCmd = $null

# Check py launcher first (recommended for Windows)
try {
    $pyVersion = py -3 --version 2>&1
    if ($LASTEXITCODE -eq 0 -and $pyVersion -match "Python") {
        $pythonCmd = "py -3"
        Write-Host "Found Python via py launcher: $pyVersion" -ForegroundColor Green
    }
} catch {}

# If py launcher not found, try python command but exclude msys64
if (-not $pythonCmd) {
    try {
        $pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
        if ($pythonPath -and $pythonPath -notmatch "msys64") {
            $pythonVersion = python --version 2>&1
            $pythonCmd = "python"
            Write-Host "Found Python: $pythonVersion at $pythonPath" -ForegroundColor Green
        }
    } catch {}
}

# If still not found, try python3
if (-not $pythonCmd) {
    try {
        $pythonPath = (Get-Command python3 -ErrorAction SilentlyContinue).Source
        if ($pythonPath -and $pythonPath -notmatch "msys64") {
            $pythonVersion = python3 --version 2>&1
            $pythonCmd = "python3"
            Write-Host "Found Python3: $pythonVersion at $pythonPath" -ForegroundColor Green
        }
    } catch {}
}

if (-not $pythonCmd) {
    Write-Host "[ERROR] Python not found or only msys64 Python available!" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Check uvicorn installation
Write-Host "[INFO] Checking uvicorn installation..." -ForegroundColor Yellow
$uvicornCheck = python -m uvicorn --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] Uvicorn not found. Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host ""

# Start server
Write-Host "[INFO] Starting FastAPI server..." -ForegroundColor Yellow
Write-Host "Server will run at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
