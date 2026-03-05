# -*- coding: utf-8 -*-
# Install 3-Tier Memory System

Write-Host @"
================================================================================
3-TIER MEMORY SYSTEM INSTALLATION
================================================================================
"@

$ErrorActionPreference = "Stop"

# ------------------------------------------------------------------ #
# Step 1: Verify Python environment
# ------------------------------------------------------------------ #
Write-Host "`n[1/6] Verifying Python environment..."

$PythonExe = "C:\Users\haujo\projects\DEV\memory_management\.venv\Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
    Write-Host "    [ERROR] Python executable not found at $PythonExe"
    exit 1
}

$PythonVersion = & $PythonExe --version
Write-Host "    [OK] Python found: $PythonVersion"

# ------------------------------------------------------------------ #
# Step 2: Install Quarto CLI
# ------------------------------------------------------------------ #
Write-Host "`n[2/6] Installing Quarto CLI..."

try {
    $quartoVersion = & quarto --version 2>$null
    Write-Host "    [OK] Quarto already installed: $quartoVersion"
} catch {
    Write-Host "    Installing Quarto via winget..."
    winget install Posit.Quarto --accept-source-agreements --accept-package-agreements
    Write-Host "    [OK] Quarto installed"
}

# ------------------------------------------------------------------ #
# Step 3: Create directory structure
# ------------------------------------------------------------------ #
Write-Host "`n[3/6] Creating directory structure..."

$openclawHome = "$env:USERPROFILE\.openclaw"

$directories = @(
    "$openclawHome\agents\main\memory\global",
    "$openclawHome\agents\main\memory\domains\trading",
    "$openclawHome\agents\main\memory\domains\data_science",
    "$openclawHome\semantic\trading",
    "$openclawHome\semantic\data_visualization",
    "$openclawHome\semantic\x_monetization",
    "$openclawHome\workspaces\trading\memory",
    "$openclawHome\workspaces\data_visualization\memory",
    "$openclawHome\workspaces\x_monetization\memory",
    "$openclawHome\scheduler"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    Write-Host "    [OK] Created $dir"
}

# ------------------------------------------------------------------ #
# Step 4: Create project documentation folders
# ------------------------------------------------------------------ #
Write-Host "`n[4/6] Creating project documentation folders..."

$projects = @(
    @{path = "C:\Users\haujo\projects\DEV\trading"; name = "trading"},
    @{path = "C:\Users\haujo\projects\DEV\Data_visualization"; name = "data_visualization"},
    @{path = "C:\Users\haujo\projects\DEV\X_Monetization"; name = "x_monetization"}
)

foreach ($project in $projects) {
    if (Test-Path $project.path) {
        foreach ($folder in @("docs", "sessions", "notes")) {
            $folderPath = Join-Path $project.path $folder
            New-Item -ItemType Directory -Force -Path $folderPath | Out-Null
            Write-Host "    [OK] Created $folderPath"
        }
    } else {
        Write-Host "    [SKIP] Project not found: $($project.path)"
    }
}

# ------------------------------------------------------------------ #
# Step 5: Download sentence transformer model
# ------------------------------------------------------------------ #
Write-Host "`n[5/6] Downloading sentence transformer model (~500MB)..."

$pythonScript = @"
from sentence_transformers import SentenceTransformer
print('Downloading model...')
model = SentenceTransformer('all-MiniLM-L6-v2')
print('✓ Model downloaded and cached successfully')
"@

$pythonScript | & $PythonExe -
Write-Host "    [OK] Model cached"

# ------------------------------------------------------------------ #
# Step 6: Create projects.json configuration
# ------------------------------------------------------------------ #
Write-Host "`n[6/6] Creating projects configuration..."

$projectsJson = @'
{
  "version": "1.0",
  "created_at": "2026-03-05",
  "projects": [
    {
      "id": "trading",
      "name": "trading",
      "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\trading",
      "domain": "trading",
      "peacock": "#0B5FFF",
      "python_interpreter": ".venv\\Scripts\\python.exe",
      "description": "Crypto trading system with HSMM regime detection"
    },
    {
      "id": "data_visualization",
      "name": "data_visualization",
      "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\Data_visualization",
      "domain": "data_science",
      "peacock": "#0BBF5F",
      "python_interpreter": ".venv\\Scripts\\python.exe",
      "description": "Global market cap data visualization and analytics"
    },
    {
      "id": "x_monetization",
      "name": "x_monetization",
      "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\X_Monetization",
      "domain": "trading",
      "peacock": "#FF6B6B",
      "python_interpreter": ".venv\\Scripts\\python.exe",
      "description": "Twitter monetization and content strategy"
    },
    {
      "id": "memory_management",
      "name": "memory_management",
      "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\memory_management",
      "domain": "infrastructure",
      "peacock": "#9b59b6",
      "python_interpreter": ".venv\\Scripts\\python.exe",
      "description": "3-tier memory management system for OpenClaw"
    }
  ]
}
'@

$projectsJsonPath = "$openclawHome\projects.json"
$projectsJson | Out-File -FilePath $projectsJsonPath -Encoding UTF8
Write-Host "    [OK] Created $projectsJsonPath"

# ------------------------------------------------------------------ #
# Done
# ------------------------------------------------------------------ #
Write-Host @"

================================================================================
INSTALLATION COMPLETE
================================================================================

✓ Python dependencies installed
✓ Directory structure created
✓ Project folders created
✓ Embedding model cached
✓ Configuration file created

Next steps:
1. Register scheduled task: .\schedule_daily_indexer.ps1
2. Run initial indexing: python daily_indexer.py
3. Start file watcher: python file_watcher.py
4. Check logs: Get-Content `$env:USERPROFILE\.openclaw\scheduler\indexer.log

"@
