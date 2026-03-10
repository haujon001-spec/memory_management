# Adding New Projects to Memory Management System

## Step-by-Step Procedure

### Step 1: Create Project Directory Structure
```powershell
# Create the new project folder in DEV workspace
$projectName = "your_project_name"
$projectPath = "C:\Users\haujo\projects\DEV\$projectName"

New-Item -ItemType Directory -Path $projectPath -Force
New-Item -ItemType Directory -Path "$projectPath\docs" -Force
New-Item -ItemType Directory -Path "$projectPath\sessions" -Force
New-Item -ItemType Directory -Path "$projectPath\notes" -Force
```

---

### Step 2: Add Project to Configuration
Edit `~/.openclaw/projects.json` and add:

```json
{
  "id": "your_project_name",
  "name": "your_project_name",
  "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\your_project_name",
  "domain": "domain_name",
  "peacock": "#XXXXXX",
  "python_interpreter": ".venv\\Scripts\\python.exe",
  "description": "Project description"
}
```

**Fields explained**:
- `id`: Unique project identifier (lowercase, no spaces)
- `name`: Display name
- `workspace_root`: Full path to project
- `domain`: Category (trading, data_science, infrastructure, etc.)
- `peacock`: Hex color code (see Step 7)
- `description`: Brief project purpose

---

### Step 3: Create VS Code Workspace File
Create `.vscode/settings.json` in the new project:

```json
{
  "peacock.color": "#XXXXXX",
  "peacock.remoteColor": "#XXXXXX",
  "workbench.colorCustomizations": {
    "activityBar.activeBackground": "#DERIVED_LIGHTER",
    "activityBar.background": "#XXXXXX",
    "activityBar.foreground": "#e7e7e7",
    "activityBar.inactiveForeground": "#e7e7e799",
    "activityBarBadge.background": "#FFD700",
    "activityBarBadge.foreground": "#15202b",
    "commandCenter.border": "#e7e7e799",
    "sash.hoverBorder": "#XXXXXX",
    "statusBar.background": "#XXXXXX",
    "statusBar.foreground": "#e7e7e7",
    "statusBarItem.hoverBackground": "#DERIVED_LIGHTER",
    "statusBarItem.remoteBackground": "#XXXXXX",
    "statusBarItem.remoteForeground": "#e7e7e7",
    "titleBar.activeBackground": "#XXXXXX",
    "titleBar.activeForeground": "#e7e7e7",
    "titleBar.inactiveBackground": "#XXXXXX99",
    "titleBar.inactiveForeground": "#e7e7e799"
  },
  "python.defaultInterpreterPath": "C:\\Users\\haujo\\projects\\DEV\\your_project_name\\.venv\\Scripts\\python.exe"
}
```

---

### Step 4: Create Python Virtual Environment
```powershell
cd C:\Users\haujo\projects\DEV\your_project_name
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # if applicable
```

---

### Step 5: Initialize Project Documentation
Create initial documentation structure:

```powershell
# Create docs folder structure
New-Item -ItemType File -Path "docs\README.md" -Force
New-Item -ItemType File -Path "docs\index.qmd" -Force

# Create sessions folder for memory storage
New-Item -ItemType File -Path "sessions\.gitkeep" -Force

# Create notes folder
New-Item -ItemType File -Path "notes\.gitkeep" -Force
```

Example `docs/README.md`:
```markdown
# Project: your_project_name

## Overview
[Project description]

## Documentation
- Index: [index.qmd](index.qmd)

## Memory System
This project is part of the OpenClaw 3-Tier Memory Management System.
- Global memory: `~/.openclaw/global_facts.json`
- Domain memory: `~/.openclaw/[domain]/domain_facts.json`
- Project memory: `~/.openclaw/semantic/[project_id]/`
```

---

### Step 6: Configure ChromaDB Collections
The collections are created automatically on first indexing, but verify they work:

```python
from semantic_memory import SemanticMemoryIndexer
from pathlib import Path

indexer = SemanticMemoryIndexer(
    project_id='your_project_name',
    workspace_root=Path(r'C:\Users\haujo\projects\DEV\your_project_name')
)

# This will create the collections automatically
print("Collections created successfully")
```

---

### Step 7: Assign Peacock Color Code
Select a unique color for your project:

#### Color Palette Options

**Warm Colors**:
- `#FF6B6B` - Red/Coral
- `#FFA500` - Orange
- `#A0522D` - Sienna Brown
- `#8B4513` - Saddle Brown

**Cool Colors**:
- `#0B5FFF` - Blue
- `#0BBF5F` - Green
- `#9b59b6` - Purple
- `#1E90FF` - Dodger Blue

**Neutral/Special**:
- `#FFD700` - Gold
- `#808080` - Gray
- `#20B2AA` - Light Sea Green
- `#DC143C` - Crimson

**Process**:
1. Choose a color that represents your project domain
2. Record hex code (e.g., `#0B5FFF`)
3. Use it in:
   - `projects.json` → `peacock` field
   - `.vscode/settings.json` → `peacock.color` and `workbench.colorCustomizations`
4. Document the color meaning in project notes

**Example Color Assignment Strategy**:
- Trading projects: Blues
- Data projects: Greens
- Infrastructure: Purples/Browns
- Content creation: Warm colors (Gold, Orange)
- Utilities: Neutral colors

---

### Step 8: Run Initial Indexing
```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Run indexer to create initial collections
python ..\memory_management\daily_indexer.py

# Verify
Get-Content "$env:USERPROFILE\.openclaw\scheduler\indexer.log" -Tail 10
```

---

### Step 9: Test Multi-Project Setup
```powershell
# Test file watcher for new project
cd ..\memory_management
python file_watcher.py your_project_name

# Test semantic search
python test_semantic.py
# Should show your new project in the test results

# Test three-tier manager
python three_tier_manager.py
# Should load your project from configuration
```

---

### Step 10: Verify Integration
Checklist:
- [ ] Project appears in `projects.json`
- [ ] ChromaDB collections created: `~/.openclaw/semantic/your_project_name/`
- [ ] `.vscode/settings.json` has peacock color
- [ ] Peacock color displays in VS Code
- [ ] File watcher works for the project
- [ ] Semantic search returns results
- [ ] `daily_indexer.py` includes new project

---

## Automation Script (Optional)

Create `add_project.ps1` for automated setup:

```powershell
param(
    [string]$ProjectName,
    [string]$Domain = "general",
    [string]$PeacockColor = "#808080",
    [string]$Description = "New project"
)

$ProjectPath = "C:\Users\haujo\projects\DEV\$ProjectName"

# Create directories
New-Item -ItemType Directory -Path "$ProjectPath\docs", "$ProjectPath\sessions", "$ProjectPath\notes" -Force

# Create .vscode folder
New-Item -ItemType Directory -Path "$ProjectPath\.vscode" -Force

# Create settings.json (template)
# ... (settings content)

# Create .gitignore
# ... (gitignore content)

Write-Host "✓ Project directory structure created"
Write-Host "✓ Next: Update ~/.openclaw/projects.json with your project config"
```

---

## Checklist for New Projects

```
Preparation:
- [ ] Project name finalized
- [ ] Domain assigned (trading, data_science, infrastructure, etc.)
- [ ] Peacock color selected (Step 7)

Setup:
- [ ] Directory structure created (Step 1)
- [ ] Added to projects.json (Step 2)
- [ ] .vscode/settings.json created (Step 3)
- [ ] Virtual environment created (Step 4)
- [ ] Initial docs created (Step 5)
- [ ] ChromaDB collections created (Step 6)

Integration:
- [ ] File watcher tested
- [ ] Semantic search tested
- [ ] Daily indexer includes project
- [ ] Peacock color displays
- [ ] Remote colors configured for multi-workspace

Maintenance:
- [ ] Add to GitHub README examples
- [ ] Document in project notes
- [ ] Train users on project access
```

---

## Example: Adding "ml_experiments" Project

```powershell
# Step 1-3
$projectPath = "C:\Users\haujo\projects\DEV\ml_experiments"
mkdir -p "$projectPath\{docs,sessions,notes}"

# Step 2: Add to projects.json
# {
#   "id": "ml_experiments",
#   "name": "ML Experiments",
#   "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\ml_experiments",
#   "domain": "data_science",
#   "peacock": "#20B2AA",  # Light Sea Green (Step 7)
#   "description": "Machine learning experimentation and validation"
# }

# Step 3: Create .vscode/settings.json with peacock color #20B2AA
# Step 4: Setup Python environment
# Step 8: Run indexing
```

---

## Notes
- **Peacock color must be unique** to distinguish projects in VS Code
- **Domain** groups related projects for semantic organization
- **Remote color** ensures colors appear in remote connections
- Test each project immediately after setup
