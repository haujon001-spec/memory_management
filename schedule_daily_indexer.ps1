# Schedule daily indexer with Windows Task Scheduler

$TaskName = "OpenClaw-SemanticIndexer"
$PythonExe = "C:\Users\haujo\projects\DEV\memory_management\.venv\Scripts\python.exe"
$ScriptPath = "C:\Users\haujo\projects\DEV\memory_management\daily_indexer.py"

Write-Host @"
================================================================================
WINDOWS TASK SCHEDULER - DAILY INDEXER SETUP
================================================================================
"@

# Check if PowerShell is running as admin
$adminCheck = [Security.Principal.WindowsIdentity]::GetCurrent().Groups -contains 'S-1-5-32-544'
if (-not $adminCheck) {
    Write-Host "[ERROR] This script must be run as Administrator"
    Write-Host "Please right-click PowerShell and select 'Run as administrator'"
    exit 1
}

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "`n[INFO] Task '$TaskName' already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Start-Sleep -Seconds 2
}

Write-Host "`n[1/3] Creating scheduled task action..."

# Create action
$Action = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument $ScriptPath

Write-Host "    [OK] Action created"

Write-Host "`n[2/3] Creating trigger (daily at 2:00 AM)..."

# Create trigger (daily at 2:00 AM)
$Trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM

Write-Host "    [OK] Trigger created for 2:00 AM daily"

Write-Host "`n[3/3] Registering task with Windows Task Scheduler..."

# Create settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false

# Register task
$Task = Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Daily semantic indexing for OpenClaw 3-tier memory system" `
    -ErrorAction Stop

Write-Host "    [OK] Task registered successfully"

Write-Host @"

================================================================================
TASK SCHEDULER SETUP COMPLETE
================================================================================

Task Name:     '$TaskName'
Schedule:      Daily at 2:00 AM
Script:        $ScriptPath
Python:        $PythonExe

Status:        READY

To test the task (run immediately):
  PS> Start-ScheduledTask -TaskName "$TaskName"

To disable the task:
  PS> Disable-ScheduledTask -TaskName "$TaskName"

To view task history:
  PS> Get-ScheduledTask -TaskName "$TaskName" | Get-ScheduledTaskInfo

To check logs:
  PS> Get-Content `$env:USERPROFILE\.openclaw\scheduler\indexer.log -Tail 50

"@
