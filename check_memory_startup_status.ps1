# OpenClaw Memory System - Startup Status Check
# 
# Use this to verify everything is properly initialized after startup
# or to diagnose issues if something isn't working

Write-Host @"
================================================================================
OPENCLAW MEMORY SYSTEM - STARTUP DIAGNOSTICS
================================================================================
"@ -ForegroundColor Cyan

$Checks = $true

# ================================================================
# CHECK 1: OpenClaw Gateway
# ================================================================
Write-Host "`n[1] OpenClaw Gateway Status" -ForegroundColor Yellow

$gatewayProcess = Get-Process node -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -eq 'node' }
if ($gatewayProcess) {
    Write-Host "   ✅ Gateway process running (PID: $($gatewayProcess.Id))" -ForegroundColor Green
    
    # Test health endpoint
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:18000/health" -TimeoutSec 3 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "   ✅ Gateway health check: PASS (responding on port 18000)" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "   ⚠️  Gateway running but not responding to health checks" -ForegroundColor Yellow
        $Checks = $false
    }
}
else {
    Write-Host "   ❌ Gateway NOT running (Node.js process not found)" -ForegroundColor Red
    Write-Host "      Start OpenClaw manually first" -ForegroundColor Yellow
    $Checks = $false
}

# ================================================================
# CHECK 2: Tier 1 Memory (Global Facts)
# ================================================================
Write-Host "`n[2] Tier 1 Memory (Global Knowledge)" -ForegroundColor Yellow

$tier1 = "$env:USERPROFILE\.openclaw\agents\main\memory\global\global_facts.json"
if (Test-Path $tier1) {
    $size = (Get-Item $tier1).Length
    Write-Host "   ✅ global_facts.json found ($size bytes)" -ForegroundColor Green
}
else {
    Write-Host "   ❌ global_facts.json NOT found" -ForegroundColor Red
    Write-Host "      Run: .\install_3tier_memory.ps1" -ForegroundColor Yellow
    $Checks = $false
}

# ================================================================
# CHECK 3: Tier 2 Memory (Domain Facts)
# ================================================================
Write-Host "`n[3] Tier 2 Memory (Domain-Specific Knowledge)" -ForegroundColor Yellow

$tier2files = @{
    "trading" = "$env:USERPROFILE\.openclaw\agents\main\memory\domains\trading\domain_facts.json";
    "infrastructure" = "$env:USERPROFILE\.openclaw\agents\main\memory\domains\infrastructure\domain_facts.json"
}

foreach ($domain in $tier2files.Keys) {
    $path = $tier2files[$domain]
    if (Test-Path $path) {
        $size = (Get-Item $path).Length
        Write-Host "   ✅ $domain/domain_facts.json found ($size bytes)" -ForegroundColor Green
    }
    else {
        Write-Host "   ⚠️  $domain/domain_facts.json NOT found" -ForegroundColor Yellow
    }
}

# ================================================================
# CHECK 4: Tier 3b Memory (Semantic Search - ChromaDB)
# ================================================================
Write-Host "`n[4] Tier 3b Memory (Semantic Search - ChromaDB)" -ForegroundColor Yellow

$semanticPath = "$env:USERPROFILE\.openclaw\semantic"
if (Test-Path $semanticPath) {
    $projects = Get-ChildItem -Path $semanticPath -Directory -ErrorAction SilentlyContinue
    if ($projects) {
        Write-Host "   ✅ Semantic indexing initialized for $($projects.Count) project(s):" -ForegroundColor Green
        foreach ($project in $projects) {
            Write-Host "      - $($project.Name)" -ForegroundColor Green
        }
    }
    else {
        Write-Host "   ⚠️  Semantic path exists but no projects indexed yet" -ForegroundColor Yellow
        Write-Host "      Run: python daily_indexer.py" -ForegroundColor Yellow
    }
}
else {
    Write-Host "   ⚠️  Semantic indexing not initialized" -ForegroundColor Yellow
    Write-Host "      Run: .\install_3tier_memory.ps1" -ForegroundColor Yellow
}

# ================================================================
# CHECK 5: File Watcher
# ================================================================
Write-Host "`n[5] File Watcher Status" -ForegroundColor Yellow

$watcherProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'file_watcher' }
if ($watcherProcess) {
    Write-Host "   ✅ File watcher running (PID: $($watcherProcess.Id))" -ForegroundColor Green
}
else {
    Write-Host "   ℹ️  File watcher NOT running (this is normal if disabled)" -ForegroundColor Cyan
    Write-Host "      To enable: python file_watcher.py" -ForegroundColor Cyan
}

# ================================================================
# CHECK 6: Startup Registration
# ================================================================
Write-Host "`n[6] Windows Startup Registration" -ForegroundColor Yellow

$startupShortcut = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw-Memory-Startup.lnk"
if (Test-Path $startupShortcut) {
    Write-Host "   ✅ Startup shortcut registered" -ForegroundColor Green
}
else {
    Write-Host "   ⚠️  Startup shortcut NOT registered" -ForegroundColor Yellow
    Write-Host "      Run as Administrator: .\register_memory_startup.ps1" -ForegroundColor Yellow
}

# ================================================================
# CHECK 7: Startup Logs
# ================================================================
Write-Host "`n[7] Startup Logs" -ForegroundColor Yellow

$logFile = "$env:USERPROFILE\.openclaw\scheduler\memory_startup.log"
if (Test-Path $logFile) {
    $lastLine = Get-Content $logFile | Select-Object -Last 1
    Write-Host "   ✅ Log file exists" -ForegroundColor Green
    Write-Host "      Latest: $lastLine" -ForegroundColor Cyan
}
else {
    Write-Host "   ℹ️  No startup log yet (normal if not rebooted)" -ForegroundColor Cyan
}

# ================================================================
# SUMMARY
# ================================================================
Write-Host "`n================================================================================`n" -ForegroundColor Cyan

if ($Checks) {
    Write-Host "✅ ALL CRITICAL CHECKS PASSED" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your system is ready! At next Windows startup:"
    Write-Host "  1. Startup script will wait for Gateway"
    Write-Host "  2. Memory system will initialize"
    Write-Host "  3. File watcher will start"
}
else {
    Write-Host "⚠️  SOME CHECKS FAILED" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Critical issues:"
    Write-Host "  • Gateway not running - OpenClaw needs to start first"
    Write-Host "  • Memory files missing - run install_3tier_memory.ps1"
    Write-Host ""
    Write-Host "Correct these issues before testing startup sequence"
}

Write-Host "`n[HELP] For more help:"
Write-Host "  - View startup logs: Get-Content `"$env:USERPROFILE\.openclaw\scheduler\memory_startup.log`" -Tail 50"
Write-Host "  - Check gateway: Get-Process node"
Write-Host "  - Test gateway: Invoke-WebRequest http://127.0.0.1:18000/health"
Write-Host ""
