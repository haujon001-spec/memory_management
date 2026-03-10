# OpenClaw Memory System - Startup Setup Guide

## Problem: Dependency Ordering

❌ **Previous Issue**: `activate.ps1` was running at Windows startup WITHOUT waiting for OpenClaw Gateway  
✅ **Solution**: New startup orchestrator respects the startup dependency chain

## Dependency Chain (Correct Order)

```
1. Windows starts
   ↓
2. OpenClaw Gateway starts (Node.js, listening on port 18000)
   ↓
3. [WAIT FOR READY] ← NEW: Gateway health check
   ↓
4. Memory System initializes (3-tier structure ready)
   ↓
5. File Watcher starts (real-time indexing enabled)
```

---

## Setup Instructions

### Step 1: Verify Prerequisites

Before setting up startup automation, ensure these are working:

```powershell
# 1. Check OpenClaw Gateway is installed
Get-Process node | Select-Object Name, Id, CommandLine

# 2. Check memory system is installed
Test-Path "$env:USERPROFILE\.openclaw\agents\main\memory\global\global_facts.json"

# 3. Check Python virtual environment
Test-Path "C:\Users\haujo\projects\DEV\memory_management\.venv\Scripts\python.exe"
```

### Step 2: Register with Windows Startup (Admin Required)

**Right-click PowerShell** and select "Run as Administrator", then:

```powershell
cd C:\Users\haujo\projects\DEV\memory_management

# Register memory system startup script
.\register_memory_startup.ps1
```

**What this does**:
- Creates a shortcut in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`
- Script runs silently at next Windows startup
- Automatically waits for Gateway → Initializes Memory → Starts Watcher

### Step 3: Verify Installation

**Before rebooting**, verify the setup using this diagnostic script:

```powershell
.\check_memory_startup_status.ps1
```

Expected output:
```
✅ OpenClaw Gateway Status - Running
✅ Tier 1 Memory (Global Knowledge) - Found
✅ Tier 2 Memory (Domain-Specific) - Found  
✅ Tier 3b Memory (Semantic Search) - Initialized
✅ Windows Startup Registration - Registered
```

### Step 4: Manual Testing

**Test the startup script manually** (before Windows restart):

```powershell
# This simulates what will happen at next startup
.\startup_memory_system.ps1

# Check the log output
Get-Content "$env:USERPROFILE\.openclaw\scheduler\memory_startup.log" -Tail 20
```

Expected log sequence:
```
[2026-03-10 10:15:30] [INFO] Waiting for OpenClaw Gateway (127.0.0.1:18000)...
[2026-03-10 10:15:35] [INFO]   Checking... (5/60 seconds)
[2026-03-10 10:15:39] [SUCCESS] ✅ OpenClaw Gateway is READY
[2026-03-10 10:15:39] [INFO] Initializing 3-Tier Memory System...
[2026-03-10 10:15:40] [SUCCESS] ✅ Memory system initialized
[2026-03-10 10:15:40] [INFO] Starting File Watcher for real-time indexing...
[2026-03-10 10:15:41] [SUCCESS] ✅ File Watcher started (PID: 12345)
[2026-03-10 10:15:41] [INFO] STARTUP COMPLETE - Memory system ready
```

---

## Monitoring & Troubleshooting

### Check Status Anytime

```powershell
# Quick status check
.\check_memory_startup_status.ps1

# View startup logs
Get-Content "$env:USERPROFILE\.openclaw\scheduler\memory_startup.log" -Tail 50

# Check if file watcher is running
Get-Process python | Where-Object { $_.CommandLine -match 'file_watcher' }
```

### If Gateway Doesn't Start

The startup script will **wait up to 60 seconds** for the Gateway.

**If it times out:**

1. **Check if Gateway process exists:**
   ```powershell
   Get-Process node
   # If not found, start OpenClaw manually first
   ```

2. **Check Gateway health manually:**
   ```powershell
   Invoke-WebRequest http://127.0.0.1:18000/health -TimeoutSec 3
   # Should return 200 OK
   ```

3. **Check Gateway logs:**
   ```powershell
   Get-Content "$env:USERPROFILE\.openclaw\logs\gateway.log" -Tail 50
   ```

### If Memory System Won't Initialize

1. **Verify Tier 1 & 2 memory files exist:**
   ```powershell
   $files = @(
       "$env:USERPROFILE\.openclaw\agents\main\memory\global\global_facts.json",
       "$env:USERPROFILE\.openclaw\agents\main\memory\domains\trading\domain_facts.json",
       "$env:USERPROFILE\.openclaw\agents\main\memory\domains\infrastructure\domain_facts.json"
   )
   foreach ($file in $files) {
       Test-Path $file
   }
   ```

2. **If files missing, re-run installer:**
   ```powershell
   .\install_3tier_memory.ps1
   ```

### If File Watcher Won't Start

File watcher is **optional** but recommended for real-time indexing:

```powershell
# Disable it in startup script by modifying startup_memory_system.ps1:
# Change: [bool]$EnableFileWatcher = $true
# To:     [bool]$EnableFileWatcher = $false

# Or start it manually:
python file_watcher.py
```

---

## Removing from Startup

If you need to disable automatic startup:

```powershell
# Run as Administrator
.\register_memory_startup.ps1 -Remove
```

This removes the startup shortcut but does NOT delete the `startup_memory_system.ps1` script.

---

## Script Reference

### startup_memory_system.ps1
- **Purpose**: Main orchestrator - waits for Gateway, initializes memory, starts watcher
- **Runs**: Silently at Windows startup (via registered shortcut)
- **Parameters**: `-GatewayCheckIntervalSeconds`, `-MaxGatewayWaitSeconds`, `-EnableFileWatcher`
- **Logs to**: `~/.openclaw/scheduler/memory_startup.log`

### register_memory_startup.ps1
- **Purpose**: Registers startup_memory_system.ps1 with Windows startup
- **Requires**: Administrator PowerShell
- **Parameters**: `-Remove` (to unregister)

### check_memory_startup_status.ps1
- **Purpose**: Diagnostic script to verify startup readiness
- **Checks**: Gateway, Tier 1/2/3 memory, File watcher, Startup registration, Logs

---

## Summary

| Stage | Responsibility | Timeout | Status |
|-------|----------------|---------| -------|
| Gateway Startup | OpenClaw Node.js | 60 sec | Automatic (external) |
| **Memory Initialization** | startup_memory_system.ps1 | 5 sec check | ✅ This script ensures it |
| **File Watcher Start** | startup_memory_system.ps1 | 3 sec | ✅ Automatic if enabled |

The key improvement: **Your memory system now respects the Gateway dependency** and won't fail on startup.

