# Tomorrow's Priorities - March 8, 2026

## Tasks to Continue

### 1. Verify Multi-Project Script Usage
- [ ] Test `file_watcher.py` with command-line arguments for different projects
  - `python file_watcher.py trading`
  - `python file_watcher.py data_visualization`
  - `python file_watcher.py openclaw`
- [ ] Run `test_semantic.py` to verify all projects test correctly
- [ ] Verify `three_tier_manager.py` loads correct project from config

### 2. Monitor Scheduled Indexing
- [ ] Check that 2:00 AM scheduled task ran successfully
- [ ] Review `~/.openclaw/scheduler/indexer.log` for any errors
- [ ] Verify all 6 projects indexed without UTF-8 issues
- [ ] Confirm peacock colors applied in VS Code workspace tabs

### 3. Validate Peacock Color Implementation
- [ ] Open each workspace and verify colors display:
  - memory_management: Purple (#9b59b6) ✓
  - trading: Blue (#0B5FFF)
  - data_visualization: Green (#0BBF5F)
  - x_monetization: Red (#FF6B6B)
  - openclaw: Sienna Brown (#A0522D) ✓
  - pets: Gold (#FFD700) ✓
- [ ] Check `workbench.colorCustomizations` in each `.vscode/settings.json`

### 4. Code Quality & Documentation
- [ ] Review untracked files: 
  - `UNIFY_MEMORY_API-2026-03-07.md`
  - `check_semantic_indexing_status.py`
  - `validate_universal_memory.py`
  - Decide: commit, delete, or keep as draft
- [ ] Update README.md examples to show multi-project usage
- [ ] Add command-line usage examples for `file_watcher.py`
- [ ] **Review and validate `ADD_NEW_PROJECT_PROCEDURE.md`**
  - This 10-step procedure covers systematic project onboarding
  - **Step 7**: Peacock color code assignment with color palette
  - Documents automation approach for future projects
  - Includes checklist template

### 5. Test Semantic Search Across All Projects
- [ ] Run semantic search query for each project
- [ ] Verify ChromaDB collections properly created
- [ ] Test query enrichment with `three_tier_manager.py`
- [ ] Document search latency metrics

### 6. Integration Testing
- [ ] Test OpenClaw gateway integration with updated memory system
- [ ] Verify that remote sessions have correct peacock colors
- [ ] Check that all 6 projects can be searched simultaneously
- [ ] Validate performance impact of multi-project indexing

### 7. Systematic New Project Onboarding (Step 7 = Peacock Color)
- [ ] Review `ADD_NEW_PROJECT_PROCEDURE.md` - 10-step systematic guide
- [ ] Validate all steps are accurate and tested
- [ ] **Step 7 specification**: Assign unique peacock color code
  - Color palette defined with domain mapping
  - Color selection strategy documented
  - Integration with projects.json and .vscode/settings.json verified
- [ ] Test procedure with a hypothetical new project
- [ ] Document any edge cases or improvements needed
- [ ] Create `add_project.ps1` automation script (if feasible)

---

## Files Added/Updated Today
- `ADD_NEW_PROJECT_PROCEDURE.md` - Systematic guide for onboarding new projects
- `TODOLIST_08MAR2026.md` - Updated with new task for project onboarding procedure
- All core scripts now support multi-project operation ✓
- UTF-8 encoding issues resolved ✓
- Peacock colors configured for openclaw and pets ✓
- GitHub updated with script refactoring ✓

## Blockers / Issues to Address
- None currently identified

## Success Criteria
- [ ] All 6 projects can be watched/indexed independently
- [ ] Semantic search works across all projects
- [ ] Peacock colors display in all VS Code workspaces
- [ ] Scheduled task runs without errors
