# -*- coding: utf-8 -*-
"""
Post-Implementation Validation - Universal Memory System

Validates:
1. All startup scripts exist
2. All projects are properly configured
3. Memory directories initialized
4. Semantic DB working
5. Projects.json valid
6. Configuration consistency
"""

import json
from pathlib import Path
from datetime import datetime
import subprocess
import sys

def print_header(title):
    """Print section header."""
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")


def print_check(name, passed, details=""):
    """Print validation check result."""
    status = "✓ PASS" if passed else "✗ FAIL"
    symbol = "  [✓]" if passed else "  [✗]"
    print(f"{symbol} {name}")
    if details:
        print(f"      {details}")


def validate_startup_scripts():
    """Validate all startup scripts exist."""
    print_header("1. STARTUP SCRIPTS VALIDATION")
    
    dev_root = Path(r"C:\Users\haujo\projects\DEV")
    trading_root = dev_root / "trading"
    
    scripts = {
        "Universal Startup": dev_root / "vscode_startup_memory_universal.ps1",
        "Trading Startup": trading_root / "vscode_startup_memory.ps1",
        "Trading Startup (Old)": trading_root / "vscode_startup_memory_universal.ps1"
    }
    
    all_exist = True
    for name, path in scripts.items():
        exists = path.exists()
        all_exist = all_exist and exists
        size = f"({path.stat().st_size} bytes)" if exists else ""
        print_check(name, exists, str(path) + f" {size}")
    
    return all_exist


def validate_projects_config():
    """Validate projects.json configuration."""
    print_header("2. PROJECTS CONFIGURATION VALIDATION")
    
    config_path = Path.home() / '.openclaw' / 'projects.json'
    
    # Check file exists
    exists = config_path.exists()
    print_check("Config File Exists", exists, str(config_path))
    
    if not exists:
        return False
    
    # Load and validate JSON
    try:
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            config = json.load(f)
        print_check("JSON Valid", True)
    except Exception as e:
        print_check("JSON Valid", False, str(e))
        return False
    
    # Validate projects
    projects = config.get('projects', [])
    print(f"\n  Projects in config: {len(projects)}")
    
    required_fields = {'id', 'name', 'workspace_root', 'domain', 'peacock'}
    all_valid = True
    
    for project in projects:
        name = project.get('name', 'UNKNOWN')
        missing = required_fields - set(project.keys())
        
        if missing:
            print_check(f"Project '{name}' Fields", False, f"Missing: {missing}")
            all_valid = False
        else:
            workspace = Path(project['workspace_root'])
            workspace_exists = workspace.exists()
            print_check(f"Project '{name}' Fields", True)
            print_check(f"  └─ Workspace Exists", workspace_exists, str(workspace))
    
    return all_valid


def validate_memory_directories():
    """Validate memory directory structure."""
    print_header("3. MEMORY DIRECTORY STRUCTURE VALIDATION")
    
    openclaw_base = Path.home() / '.openclaw'
    config_path = openclaw_base / 'projects.json'
    
    if not config_path.exists():
        print_check("Load Projects Config", False, "projects.json not found")
        return False
    
    with open(config_path, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
    projects = config.get('projects', [])
    
    # Check global directories
    global_dirs = {
        "Global Memory": openclaw_base / 'agents' / 'main' / 'memory' / 'global',
        "Sessions": openclaw_base / 'agents' / 'main' / 'sessions',
        "Scheduler": openclaw_base / 'scheduler',
        "Semantic DBs": openclaw_base / 'semantic',
    }
    
    print("  GLOBAL DIRECTORIES:")
    all_exist = True
    for name, path in global_dirs.items():
        exists = path.exists()
        all_exist = all_exist and exists
        print_check(name, exists, str(path))
    
    # Check project-specific directories
    print("\n  PROJECT-SPECIFIC DIRECTORIES:")
    for project in projects:
        project_id = project['id']
        workspace_memory = openclaw_base / 'workspaces' / project_id / 'memory'
        semantic_db = openclaw_base / 'semantic' / project_id
        
        mem_exists = workspace_memory.exists()
        sem_exists = semantic_db.exists()
        
        print_check(f"Memory ({project_id})", mem_exists, str(workspace_memory))
        print_check(f"Semantic DB ({project_id})", sem_exists, str(semantic_db))
        all_exist = all_exist and mem_exists and sem_exists
    
    return all_exist


def validate_metadata_files():
    """Validate metadata files."""
    print_header("4. METADATA FILES VALIDATION")
    
    openclaw_base = Path.home() / '.openclaw'
    config_path = openclaw_base / 'projects.json'
    
    if not config_path.exists():
        print_check("Projects Config", False)
        return False
    
    with open(config_path, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
    projects = config.get('projects', [])
    
    # Global memory metadata
    global_meta = openclaw_base / 'agents' / 'main' / 'memory' / 'memory_meta.json'
    global_meta_ok = global_meta.exists()
    print_check("Global Memory Metadata", global_meta_ok, str(global_meta))
    
    # Per-project indices
    all_ok = global_meta_ok
    print("\n  PROJECT INDICES:")
    for project in projects:
        project_id = project['id']
        index_path = openclaw_base / 'workspaces' / project_id / 'memory' / 'index.json'
        exists = index_path.exists()
        all_ok = all_ok and exists
        print_check(f"Index ({project_id})", exists, str(index_path))
    
    # Last run metadata
    last_run = openclaw_base / 'scheduler' / 'last_run.json'
    last_run_ok = last_run.exists()
    print_check("\nIndexer Last Run", last_run_ok, str(last_run))
    all_ok = all_ok and last_run_ok
    
    return all_ok


def validate_semantic_database():
    """Validate ChromaDB initialization."""
    print_header("5. SEMANTIC DATABASE VALIDATION")
    
    openclaw_base = Path.home() / '.openclaw'
    config_path = openclaw_base / 'projects.json'
    
    if not config_path.exists():
        print_check("Load Config", False)
        return False
    
    print_check("Load Config", True)
    
    with open(config_path, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
    projects = config.get('projects', [])
    
    all_ok = True
    for project in projects:
        project_id = project['id']
        db_path = openclaw_base / 'semantic' / project_id
        
        if not db_path.exists():
            print_check(f"ChromaDB ({project_id})", False, "Directory not initialized")
            all_ok = False
            continue
        
        # Check for ChromaDB files
        has_chroma_db = (db_path / 'chroma.db').exists()
        has_metadata = (db_path / 'index_meta.json').exists()
        
        db_ok = has_chroma_db or has_metadata
        print_check(f"ChromaDB ({project_id})", db_ok, 
                   f"DB: {has_chroma_db}, Metadata: {has_metadata}")
        all_ok = all_ok and db_ok
    
    return all_ok


def validate_logging():
    """Validate logging setup."""
    print_header("6. LOGGING VALIDATION")
    
    dev_root = Path(r"C:\Users\haujo\projects\DEV")
    openclaw_base = Path.home() / '.openclaw'
    
    log_paths = {
        "Universal Startup Log": dev_root / "logs" / "vscode_memory_universal_startup.log",
        "Scheduler Log": openclaw_base / "scheduler" / "indexer.log",
        "Logs Directory": dev_root / "logs",
    }
    
    all_ok = True
    for name, path in log_paths.items():
        if path.name.endswith('.log'):
            # For log files, just check parent exists
            exists = path.parent.exists()
        else:
            exists = path.exists()
        all_ok = all_ok and exists
        print_check(name, exists, str(path))
    
    return all_ok


def validate_permissions():
    """Validate file permissions and accessibility."""
    print_header("7. PERMISSIONS & ACCESSIBILITY VALIDATION")
    
    dev_root = Path(r"C:\Users\haujo\projects\DEV")
    openclaw_base = Path.home() / '.openclaw'
    
    paths_to_check = {
        "OpenClaw Base": openclaw_base,
        "Dev Root": dev_root,
        "Memory Management": dev_root / "memory_management",
    }
    
    all_ok = True
    for name, path in paths_to_check.items():
        if not path.exists():
            print_check(name, False, "Path does not exist")
            all_ok = False
            continue
        
        try:
            # Try to read directory
            list(path.iterdir())
            is_readable = True
        except PermissionError:
            is_readable = False
        
        all_ok = all_ok and is_readable
        print_check(name, is_readable, str(path))
    
    return all_ok


def validate_project_consistency():
    """Validate consistency across all configurations."""
    print_header("8. PROJECT CONSISTENCY VALIDATION")
    
    dev_root = Path(r"C:\Users\haujo\projects\DEV")
    openclaw_base = Path.home() / '.openclaw'
    config_path = openclaw_base / 'projects.json'
    
    if not config_path.exists():
        print_check("Config Exists", False)
        return False
    
    print_check("Config Exists", True)
    
    with open(config_path, 'r', encoding='utf-8-sig') as f:
        config = json.load(f)
    projects = config.get('projects', [])
    
    all_ok = True
    for project in projects:
        project_id = project['id']
        workspace = Path(project['workspace_root'])
        expected_venv = workspace / '.venv'
        expected_vscode = workspace / '.vscode'
        
        # Check workspace structure
        workspace_ok = workspace.exists()
        print_check(f"Workspace ({project_id})", workspace_ok, str(workspace))
        
        # Optional: check for standard structure
        has_structure = expected_venv.exists() and expected_vscode.exists()
        print_check(f"  └─ Standard Structure", has_structure or workspace_ok,
                   f"venv: {expected_venv.exists()}, vscode: {expected_vscode.exists()}")
        
        all_ok = all_ok and workspace_ok
    
    return all_ok


def main():
    """Run all validations."""
    print("\n" + "="*80)
    print("POST-IMPLEMENTATION VALIDATION - UNIVERSAL MEMORY SYSTEM")
    print("="*80)
    print(f"Validation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"OpenClaw Base: {Path.home() / '.openclaw'}")
    
    # Run validations
    results = {
        "Startup Scripts": validate_startup_scripts(),
        "Projects Config": validate_projects_config(),
        "Memory Directories": validate_memory_directories(),
        "Metadata Files": validate_metadata_files(),
        "Semantic Database": validate_semantic_database(),
        "Logging": validate_logging(),
        "Permissions": validate_permissions(),
        "Project Consistency": validate_project_consistency(),
    }
    
    # Summary
    print_header("VALIDATION SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, passed_val in results.items():
        status = "✓ PASS" if passed_val else "✗ FAIL"
        print(f"{status}  {name}")
    
    print(f"\n{'='*80}")
    print(f"RESULT: {passed}/{total} validation sections passed")
    if passed == total:
        print("✓ ALL VALIDATIONS PASSED - System is ready!")
    else:
        print(f"⚠ {total - passed} validation section(s) need attention")
    print(f"{'='*80}\n")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
