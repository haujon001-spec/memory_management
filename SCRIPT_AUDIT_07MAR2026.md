# Script Audit - Memory Management Project

## Analysis Date: March 7, 2026

### Executive Summary
The memory_management scripts have a **good architecture** that supports all projects via configuration files. However, there are **hardcoded trading references in test/example code** that should be updated to support all projects or be made configurable.

---

## Script-by-Script Audit

### ✅ Core Scripts (Production-Ready)

#### 1. `daily_indexer.py` - **PRODUCTION READY**
**Status**: ✅ Properly handles all projects
- Loads all projects from `~/.openclaw/projects.json`
- Iterates through all configured projects
- Contains default fallback configurations for all 6 projects
- No hardcoded project-specific logic
- **Result**: Works correctly for all projects

**How it works**:
```python
def index_all_projects(self):
    for project in self.projects:  # self.projects loaded from config
        count = self.index_project(project)
```

---

#### 2. `semantic_memory.py` - **PRODUCTION READY**
**Status**: ✅ Properly parameterized
- Accepts `project_id` and `workspace_root` as parameters
- Uses ChromaDB with project-specific databases
- No hardcoded paths
- **Result**: Works correctly for all projects

---

#### 3. `three_tier_manager.py` - **PRODUCTION READY**
**Status**: ✅ Properly parameterized
- Constructor requires `project_id`, `workspace_root`, and `domain`
- Only has example code in `__main__` that uses trading
- **Issue**: Example code should show all projects or be removed
- **Action**: Update example code to show multi-project usage (LOW PRIORITY)

---

#### 4. `file_watcher.py` - **NEEDS ATTENTION**
**Status**: ⚠️ Parameterized class, but hardcoded test code

**Good**:
- `QmdFileHandler` class properly parameterized
- `start_file_watcher()` function accepts project parameters

**Issues**:
```python
if __name__ == '__main__':
    start_file_watcher(
        project_id='trading',  # ❌ Hardcoded to trading only
        workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
    )
```

**Problem**: When someone runs `python file_watcher.py`, it only watches the trading project.
**Solution**: Should either:
1. Accept command-line argument for project
2. Watch all projects from config
3. Make it clear it's for testing only

---

### 🟡 Test/Validation Scripts (Testing Code)

#### 5. `test_indexing.py` - **TESTING CODE**
**Status**: ✅ Correctly tests multiple projects
- Tests all 3 projects (trading, data_visualization, x_monetization)
- Hardcoded paths are intentional for testing
- **Result**: This is correct for testing purposes

---

#### 6. `test_semantic.py` - **TESTING CODE**
**Status**: ⚠️ Only tests trading project
- Has hardcoded trading project
- Should test all projects or accept arguments
- **Priority**: LOW (Testing code only)

```python
if __name__ == '__main__':
    indexer = SemanticMemoryIndexer(
        project_id='trading',  # ❌ Only tests trading
        workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
    )
```

---

#### 7. `qmd_parser.py` - **TESTING CODE**
**Status**: ⚠️ Hardcoded test file path
- Test section only, not production code
- **Issue**: Test file from trading project
- **Priority**: LOW (Testing code only)

```python
if __name__ == '__main__':
    test_file = Path(r'C:\Users\haujo\projects\DEV\trading\docs\planning\...')
```

---

#### 8. `validate_universal_memory.py` - **UTILITY SCRIPT**
**Status**: ⚠️ Mixed: Some all-projects, some trading-specific
- Has references to `trading_root`
- Also properly iterates through dev projects
- **Priority**: LOW (Utility validation script)

---

### 📊 Summary Table

| Script | Status | Hardcoded Trading | Handles All Projects | Action |
|--------|--------|------------------|----------------------|--------|
| `daily_indexer.py` | ✅ PROD | ✓ (defaults only) | ✅ Yes | None |
| `semantic_memory.py` | ✅ PROD | ✗ | ✅ Yes | None |
| `three_tier_manager.py` | ✅ PROD | ✓ (example) | ✅ Yes | Update example |
| `file_watcher.py` | ⚠️ | ✓ (test code) | ✅ Class OK | Add CLI arg |
| `test_indexing.py` | ✅ TEST | ✗ | ✅ Yes | None |
| `test_semantic.py` | 🟡 TEST | ✓ (test only) | ⚠️ No | Update test |
| `qmd_parser.py` | ✅ UTIL | ✓ (test only) | ✅ No | Minor update |
| `validate_universal_memory.py` | 🟡 UTIL | ✓ (mixed) | ⚠️ Partial | No change needed |

---

## Recommendations

### High Priority (None - Production code is good!)
- Daily indexer and semantic memory are correctly multi-project aware

### Medium Priority
1. **file_watcher.py**: Add command-line argument support to watch any project
2. **test_semantic.py**: Update to test all projects or accept arguments

### Low Priority
1. **three_tier_manager.py**: Update example in `__main__` to show all projects
2. **qmd_parser.py**: Update test file path to use any project

---

## Conclusion

The core infrastructure is **excellent** - it properly implements multi-project support through configuration files. The hardcoded references are limited to test/example code in `__main__` blocks. 

**Key Strengths**:
- ✅ `daily_indexer.py` handles all 6 projects automatically
- ✅ Parameterized classes allow any project usage
- ✅ Configuration-driven approach is scalable
- ✅ No hardcoded paths in production classes

**Minor Issues**:
- Test code could be more flexible
- CLI tools could accept project parameters

**Recommended Action**: Consider these improvements but not critical for functionality.
