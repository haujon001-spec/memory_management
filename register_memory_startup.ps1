# Register Memory System with Windows Startup
# This creates a startup shortcut that waits for gateway before initializing memory
# 
# Run as Administrator

param(
    [switch]$Remove,
    [string]$StartupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
)

$ShortcutName = "OpenClaw-Memory-Startup.lnk"
$ShortcutPath = "$StartupFolder\$ShortcutName"
$ScriptPath = "C:\Users\haujo\projects\DEV\memory_management\startup_memory_system.ps1"

# Check if running as administrator
$adminCheck = [Security.Principal.WindowsIdentity]::GetCurrent().Groups -contains 'S-1-5-32-544'
if (-not $adminCheck) {
    Write-Host "[ERROR] This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as administrator'"
    exit 1
}

if ($Remove) {
    # Remove startup shortcut
    if (Test-Path $ShortcutPath) {
        Remove-Item $ShortcutPath -Force
        Write-Host "[OK] Removed startup shortcut: $ShortcutName" -ForegroundColor Green
    }
    else {
        Write-Host "[INFO] Shortcut not found (may already be removed)" -ForegroundColor Yellow
    }
    exit 0
}

# Create startup shortcut
Write-Host "================================================================================"
Write-Host "WINDOWS STARTUP REGISTRATION - MEMORY SYSTEM"
Write-Host "================================================================================"
Write-Host ""
Write-Host "This will create a startup shortcut that:"
Write-Host "  1. Waits for OpenClaw Gateway to be ready"
Write-Host "  2. Initializes 3-tier memory system"
Write-Host "  3. Starts real-time file watcher"
Write-Host ""

# Verify script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "[ERROR] Script not found: $ScriptPath" -ForegroundColor Red
    exit 1
}

# Remove old shortcut if exists
if (Test-Path $ShortcutPath) {
    Write-Host "Removing old shortcut..."
    Remove-Item $ShortcutPath -Force
}

# Create COM object for shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Configure shortcut properties
$Shortcut.TargetPath = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
$Shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""
$Shortcut.IconLocation = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe,0"
$Shortcut.WindowStyle = 7
$Shortcut.Description = "OpenClaw 3-Tier Memory System Startup"

# Save shortcut
$Shortcut.Save()

Write-Host ""
Write-Host "[OK] Startup shortcut created successfully!" -ForegroundColor Green
Write-Host "Location: $ShortcutPath"
Write-Host ""
Write-Host "WHAT HAPPENS AT NEXT WINDOWS STARTUP:"
Write-Host "  1. Script runs silently in background"
Write-Host "  2. Waits for OpenClaw Gateway to start (checks every 5 seconds)"
Write-Host "  3. Once Gateway is ready, initializes memory system"
Write-Host "  4. Starts file watcher for real-time indexing"
Write-Host "  5. Logs all activity to: $env:USERPROFILE\.openclaw\scheduler\memory_startup.log"
Write-Host ""
Write-Host "VIEW STARTUP LOGS:"
Write-Host "  Get-Content '$env:USERPROFILE\.openclaw\scheduler\memory_startup.log' -Tail 50"
Write-Host ""
Write-Host "TO REMOVE FROM STARTUP:"
Write-Host "  .\register_memory_startup.ps1 -Remove"
Write-Host ""
Write-Host "================================================================================"
Write-Host "[SUCCESS] Memory startup registration complete"
Write-Host "================================================================================"
