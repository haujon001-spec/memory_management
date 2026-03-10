# REGISTER MEMORY SYSTEM WITH WINDOWS STARTUP

## Status
✅ All 3-tier memory files are created and working  
⏳ Startup registration pending (requires Administrator)

---

## What Needs to Be Done

The memory system needs to be registered with Windows Task Scheduler so it:
1. Waits for OpenClaw Gateway to be ready
2. Initializes memory system after Gateway responds
3. Starts file watcher for real-time indexing

---

## Method 1: Auto-Registration (Simplest)

**Right-click as Administrator and run**:

```bash
register_memory_startup.bat
```

This batch file will:
- ✅ Check for admin privileges
- ✅ Run the PowerShell registration script
- ✅ Confirm success

---

## Method 2: Manual PowerShell Registration

Open PowerShell **as Administrator** (right-click → Run as administrator):

```powershell
cd C:\Users\haujo\projects\DEV\memory_management
.\register_memory_startup.ps1
```

**Expected Output**:
```
================================================================================
WINDOWS STARTUP REGISTRATION - MEMORY SYSTEM
================================================================================

This will create a startup shortcut that:
  1. Waits for OpenClaw Gateway to be ready
  2. Initializes 3-tier memory system
  3. Starts real-time file watcher

Removing old shortcut...
✅ Startup shortcut created successfully!
   Location: C:\Users\haujo\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw-Memory-Startup.lnk

📋 What happens at next Windows startup:
   1. Script runs silently in background
   2. Waits for OpenClaw Gateway to start (checks every 5 seconds)
   3. Once Gateway is ready, initializes memory system
   4. Starts file watcher for real-time indexing
   5. Logs all activity to: C:\Users\haujo\.openclaw\scheduler\memory_startup.log
```

---

## Method 3: Direct File Creation (Manual)

If you can't run scripts, you can manually create the startup shortcut:

**Step 1**: Press `Win + R`, type:
```
shell:startup
```

Press Enter. This opens the Startup folder.

**Step 2**: Right-click in the empty space → New → Shortcut

**Step 3**: Paste this as the target:
```
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\haujo\projects\DEV\memory_management\startup_memory_system.ps1"
```

**Step 4**: 
- Name it: `OpenClaw-Memory-Startup`
- Click Finish
- Right-click the shortcut → Properties
- Set "Run" to "Minimized"
- Click OK

---

## Verification

After registration, verify with:

```powershell
# Check if shortcut was created
Test-Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw-Memory-Startup.lnk"

# Should return: True
```

---

## At Next Windows Restart

The startup sequence will automatically:

1. ✅ **Tier 1**: Load global_facts.json (910 bytes)
2. ✅ **Tier 2**: Load domain_facts.json (trading, infrastructure)
3. ✅ **Tier 3a**: Load workspace index.json
4. ✅ **Tier 3b**: Activate semantic search (6,788 docs)
5. ✅ **File Watcher**: Start for real-time indexing

**Logs**: Check progress at:
```powershell
Get-Content "$env:USERPROFILE\.openclaw\scheduler\memory_startup.log" -Tail 50
```

---

## Quick Check Commands

```powershell
# Check if memory files exist
$files = @(
    "$env:USERPROFILE\.openclaw\agents\main\memory\global\global_facts.json",
    "$env:USERPROFILE\.openclaw\agents\main\memory\domains\trading\domain_facts.json",
    "$env:USERPROFILE\.openclaw\agents\main\memory\domains\infrastructure\domain_facts.json"
)
foreach ($f in $files) { 
    "$(Split-Path $f -Leaf): $(if(Test-Path $f) {'✅ OK'} else {'❌ MISSING'})"
}

# Check startup shortcut
Test-Path "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw-Memory-Startup.lnk"

# Check if OpenClaw Gateway is running
Get-Process node | Select-Object Name, Id, CommandLine
```

---

## Troubleshooting

**"Access denied" or "admin error":**
- Close all PowerShell windows
- Open new PowerShell window
- Right-click → "Run as Administrator"
- Try again

**Shortcut not showing up:**
- Clear the Startup folder cache: `Win + R` → `shell:startup`
- Restart Windows

**Still having issues?**
- Run diagnostic: `.\check_memory_startup_status.ps1`
- Check logs: `Get-Content ~/.openclaw/scheduler/memory_startup.log -Tail 100`

---

## Summary

| Item | Status |
|------|--------|
| Tier 1 Memory (Global) | ✅ Ready |
| Tier 2 Memory (Domain) | ✅ Ready |
| Tier 3a Memory (Workspace) | ✅ Ready |
| Tier 3b Memory (Semantic) | ✅ Ready (6,788 docs) |
| Startup Orchestrator | ✅ Created |
| **Startup Registration** | ⏳ Pending (you do this) |

---

## Next Steps

**Choose one method above**:
- **Easiest**: Run `register_memory_startup.bat` (right-click as admin)
- **Manual**: Run PowerShell script as admin
- **No scripts**: Use Method 3 (create shortcut manually)

Then verify with: `check_memory_startup_status.ps1`

That's it! Your memory system will automatically start on the next Windows restart. 🚀

