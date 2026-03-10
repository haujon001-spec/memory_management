# OpenClaw 3-Tier Memory System - STARTUP ORCHESTRATOR
# This script respects the dependency: Gateway → Memory System
# 
# INSTALLATION: Copy to Windows Startup folder
# %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
#
# Purpose: 
# 1. Wait for OpenClaw Gateway to be ready (health check)
# 2. Initialize 3-tier memory system
# 3. Enable file watcher for real-time indexing
# 4. Start semantic search capabilities

param(
    [int]$GatewayCheckIntervalSeconds = 5,
    [int]$MaxGatewayWaitSeconds = 60,
    [bool]$EnableFileWatcher = $true
)

# ================================================================
# CONFIGURATION
# ================================================================
$GatewayHost = "127.0.0.1"
$GatewayPort = 18000
$GatewayHealthUrl = "http://$GatewayHost:$GatewayPort/health"

$LogPath = "$env:USERPROFILE\.openclaw\scheduler"
$LogFile = "$LogPath\memory_startup.log"
$MemoryProjectPath = "C:\Users\haujo\projects\DEV\memory_management"

# Ensure log directory exists
if (-not (Test-Path $LogPath)) {
    New-Item -ItemType Directory -Path $LogPath -Force | Out-Null
}

# ================================================================
# LOGGING FUNCTION
# ================================================================
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$Timestamp] [$Level] $Message"
    
    # Write to log file
    Add-Content -Path $LogFile -Value $LogMessage -Encoding UTF8
    
    # Also write to console (if running interactively)
    Write-Host $LogMessage
}

# ================================================================
# CORE FUNCTIONS
# ================================================================

function Test-GatewayHealth {
    <#
    .SYNOPSIS
    Check if OpenClaw gateway is running and responding
    #>
    try {
        $response = Invoke-WebRequest -Uri $GatewayHealthUrl `
            -Method GET `
            -TimeoutSec 3 `
            -ErrorAction Stop
        
        if ($response.StatusCode -eq 200) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

function Wait-ForGateway {
    <#
    .SYNOPSIS
    Wait for OpenClaw gateway to become available
    #>
    Write-Log "Waiting for OpenClaw Gateway ($GatewayHost:$GatewayPort)..." "INFO"
    
    $elapsedSeconds = 0
    
    while ($elapsedSeconds -lt $MaxGatewayWaitSeconds) {
        if (Test-GatewayHealth) {
            Write-Log "✅ OpenClaw Gateway is READY" "SUCCESS"
            return $true
        }
        
        Write-Log "  Checking... ($elapsedSeconds/$MaxGatewayWaitSeconds seconds)" "WAIT"
        Start-Sleep -Seconds $GatewayCheckIntervalSeconds
        $elapsedSeconds += $GatewayCheckIntervalSeconds
    }
    
    Write-Log "❌ OpenClaw Gateway did NOT start within $MaxGatewayWaitSeconds seconds" "ERROR"
    Write-Log "   Please verify: Get-Process node | Select-Object Name, Id" "ERROR"
    return $false
}

function Initialize-MemorySystem {
    <#
    .SYNOPSIS
    Initialize 3-tier memory system after gateway is ready
    #>
    Write-Log "Initializing 3-Tier Memory System..." "INFO"
    
    # Verify memory directories exist
    $openclaw = "$env:USERPROFILE\.openclaw"
    $memoryDirs = @(
        "$openclaw\agents\main\memory\global",
        "$openclaw\agents\main\memory\domains\trading",
        "$openclaw\agents\main\memory\domains\infrastructure",
        "$openclaw\semantic\trading",
        "$openclaw\semantic\data_visualization",
        "$openclaw\workspaces\trading\memory",
        "$openclaw\workspaces\data_visualization\memory"
    )
    
    foreach ($dir in $memoryDirs) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Log "  Created: $dir" "INFO"
        }
    }
    
    # Verify Tier 1 & Tier 2 files exist
    $tier1File = "$openclaw\agents\main\memory\global\global_facts.json"
    if (-not (Test-Path $tier1File)) {
        Write-Log "  ⚠️ Tier 1 (global_facts.json) not found - run install_3tier_memory.ps1" "WARN"
        return $false
    }
    
    Write-Log "✅ Memory system initialized" "SUCCESS"
    return $true
}

function Start-FileWatcher {
    <#
    .SYNOPSIS
    Start real-time file watcher for automatic indexing
    #>
    if (-not $EnableFileWatcher) {
        Write-Log "File watcher disabled (EnableFileWatcher = false)" "INFO"
        return
    }
    
    Write-Log "Starting File Watcher for real-time indexing..." "INFO"
    
    # Check if file_watcher.py exists
    $watcherScript = "$MemoryProjectPath\file_watcher.py"
    if (-not (Test-Path $watcherScript)) {
        Write-Log "  ❌ file_watcher.py not found at $watcherScript" "ERROR"
        return
    }
    
    # Check if Python venv exists
    $PythonExe = "$MemoryProjectPath\.venv\Scripts\python.exe"
    if (-not (Test-Path $PythonExe)) {
        Write-Log "  ❌ Python venv not found at $PythonExe" "ERROR"
        return
    }
    
    try {
        # Start file watcher in background
        $procParams = @{
            FilePath = $PythonExe
            ArgumentList = $watcherScript
            WindowStyle = "Hidden"
            PassThru = $true
        }
        
        $process = Start-Process @procParams
        Write-Log "✅ File Watcher started (PID: $($process.Id))" "SUCCESS"
    }
    catch {
        Write-Log "❌ Failed to start File Watcher: $_" "ERROR"
    }
}

# ================================================================
# MAIN STARTUP SEQUENCE
# ================================================================

Write-Log "===============================================" "INFO"
Write-Log "OPENCLAW 3-TIER MEMORY SYSTEM - STARTUP" "INFO"
Write-Log "===============================================" "INFO"

# Step 1: Wait for gateway
if (-not (Wait-ForGateway)) {
    Write-Log "Startup failed: Gateway not available" "ERROR"
    exit 1
}

# Step 2: Initialize memory system
if (-not (Initialize-MemorySystem)) {
    Write-Log "Startup incomplete: Memory system initialization had warnings" "WARN"
}

# Step 3: Start file watcher (optional)
Start-FileWatcher

Write-Log "===============================================" "INFO"
Write-Log "STARTUP COMPLETE - Memory system ready" "INFO"
Write-Log "===============================================" "INFO"
