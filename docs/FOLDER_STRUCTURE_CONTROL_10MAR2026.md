# Folder Structure Control - Memory Management Project

**Last Updated**: March 10, 2026  
**Structure Version**: 1.0  
**Strict Folder Control**: Enabled

---

## Project Documentation Structure

```
memory_management/
│
├── docs/                           ← Documentation directory (STRICT CONTROL)
│   ├── setup/                      ← Installation & Setup guides
│   │   ├── STARTUP_SETUP_GUIDE_10MAR2026.md
│   │   ├── STARTUP_REGISTRATION_INSTRUCTIONS_10MAR2026.md
│   │   └── GITHUB_SETUP_10MAR2026.md
│   │
│   ├── guides/                     ← User guides & procedures
│   │   └── ADD_NEW_PROJECT_PROCEDURE_10MAR2026.md
│   │
│   ├── status/                     ← Project status & completion reports
│   │   ├── COMPLETE_STATUS_10MAR2026.md
│   │   ├── IMPLEMENTATION_COMPLETE_10MAR2026.md
│   │   ├── THREE_TIER_TEST_RESULTS_10MAR2026.md
│   │   ├── COMPLETION_LOG_10MAR2026.md
│   │   ├── SCRIPT_AUDIT_10MAR2026.md
│   │   ├── STEPS_1_TO_4_COMPLETE_10MAR2026.md
│   │   ├── INDEXING_COMPLETE_10MAR2026.md
│   │   └── TODOLIST_10MAR2026.md
│   │
│   ├── architecture/                ← Technical architecture documents
│   │   ├── PROJECTPLAN_10MAR2026.md
│   │   └── UNIFY_MEMORY_API_10MAR2026.md
│   │
│   ├── api/                         ← API integration documentation
│   │   └── OPENCLAW_INTEGRATION_10MAR2026.md
│   │
│   └── project/                     ← Main project documentation
│       ├── README_10MAR2026.md
│       ├── GITHUB_READY_10MAR2026.md
│       └── LINKEDIN_POST_10MAR2026.md
│
├── Core Modules (5 files)
│   ├── qmd_parser.py
│   ├── semantic_memory.py
│   ├── daily_indexer.py
│   ├── three_tier_manager.py
│   └── file_watcher.py
│
├── PowerShell Scripts (2 files)
│   ├── install_3tier_memory.ps1
│   └── schedule_daily_indexer.ps1
│
├── Startup & Diagnostic Scripts
│   ├── startup_memory_system.ps1
│   ├── register_memory_startup.ps1
│   ├── register_memory_startup.bat
│   └── check_memory_startup_status.ps1
│
├── Test Scripts (4 files)
│   ├── test_semantic.py
│   ├── test_indexing.py
│   ├── test_all_tiers.py
│   └── init_memory_tiers.py
│
├── Requirements & Config
│   ├── requirements.txt
│   ├── .gitignore
│   ├── LICENSE
│   └── FOLDER_STRUCTURE_CONTROL_10MAR2026.md (this file)
│
└── Virtual Environment
    └── .venv/
```

---

## Folder Structure Rules

### ✅ ALLOWED Locations for .md Files

| Folder | Purpose | File Naming Convention |
|--------|---------|------------------------|
| `docs/setup/` | Installation, setup, configuration guides | `FILENAME_10MAR2026.md` |
| `docs/guides/` | User guides, procedures, tutorials | `FILENAME_10MAR2026.md` |
| `docs/status/` | Status reports, completion logs, test results | `FILENAME_10MAR2026.md` |
| `docs/architecture/` | Technical specs, system design, API design | `FILENAME_10MAR2026.md` |
| `docs/api/` | API integration, gateway integration | `FILENAME_10MAR2026.md` |
| `docs/project/` | Main project README, marketing, misc docs | `FILENAME_10MAR2026.md` |

### ❌ NOT ALLOWED

- ✗ .md files in root directory (must be in `docs/` subfolder)
- ✗ Files without date suffix (must have `_10MAR2026.md` format)
- ✗ Undated files mixed with dated files
- ✗ New folders created without approval (only approved folders above)

---

## Adding New Documentation

### When Adding New .md Files

1. **Determine Category**: Setup, Guides, Status, Architecture, API, or Project
2. **Use Correct Folder**: Place in appropriate `docs/` subfolder
3. **Add Date Suffix**: Use format `FILENAME_10MAR2026.md` (today's date)
4. **Update Index**: Add entry to [DOCUMENTATION_INDEX_10MAR2026.md](DOCUMENTATION_INDEX_10MAR2026.md)

### Example

Adding a new debugging guide:

```
NEW: Debugging Guide
FOLDER: docs/guides/
FILENAME: DEBUGGING_GUIDE_10MAR2026.md
```

---

## File Management

### Current Reorganization (March 10, 2026)

| Category | Count | Location |
|----------|-------|----------|
| Setup Docs | 3 | `docs/setup/` |
| Guides | 1 | `docs/guides/` |
| Status Reports | 8 | `docs/status/` |
| Architecture | 2 | `docs/architecture/` |
| API Integration | 1 | `docs/api/` |
| Project Docs | 3 | `docs/project/` |
| **TOTAL** | **18** | `docs/*/` |

### Code Files (Root Level)

- Core modules: 5 `.py` files
- PowerShell scripts: 6 `.ps1` files + 1 `.bat`
- Test scripts: 4 `.py` files
- Config files: `requirements.txt`, `.gitignore`, `LICENSE`

---

## Maintenance Guidelines

### Version Control

- Each .md file includes date suffix in filename
- Enables version tracking without branches
- Latest version always named with current date
- Old versions can be archived if needed

### Archiving Old Documentation

**When archiving older versions**:

1. Create `docs/archive/` folder
2. Move old dated files to archive
3. Update index to show archived versions
4. Keep most recent version in active folder

Example:
```
docs/
├── setup/
│   └── STARTUP_SETUP_GUIDE_10MAR2026.md (current)
└── archive/
    └── STARTUP_SETUP_GUIDE_07MAR2026.md (archived)
```

---

## GitHub Integration

### Files Tracked in Git

```
✅ All .md files in docs/
✅ All .py scripts
✅ PowerShell scripts (.ps1, .bat)
✅ requirements.txt
✅ .gitignore
✅ LICENSE
✅ FOLDER_STRUCTURE_CONTROL_10MAR2026.md
```

### .gitignore Rules

```
.venv/
__pycache__/
*.pyc
.DS_Store
*.log
```

---

## Enforcement Checklist

Before each Git commit, verify:

- [ ] All .md files are in `docs/` subfolder (not root)
- [ ] All .md files have date suffix `_10MAR2026.md`
- [ ] File is in correct category folder
- [ ] No unauthorized folders created
- [ ] DOCUMENTATION_INDEX.md is updated
- [ ] This control file is up-to-date

---

## Contact & Questions

For questions about folder structure:
1. Review this document
2. Check similar files in the same category
3. Consult DOCUMENTATION_INDEX for guidance

---

**Structure Enforced**: ✅  
**Last Audit**: March 10, 2026  
**Next Review**: March 17, 2026
