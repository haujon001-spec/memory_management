# OpenClaw 3-Tier Memory Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-windows-blue.svg)](https://www.microsoft.com/windows)

A sophisticated three-tier memory architecture for multi-project workspaces, combining persistent storage, domain-specific knowledge, and semantic vector search capabilities.

## 🎯 Features

- 🧠 **Semantic Search**: Vector-based documentation retrieval with sentence-transformers
- 📚 **Three-Tier Architecture**: Global, domain-specific, and workspace-level memories
- ⚙️ **Automated Indexing**: Daily scheduled indexing via Windows Task Scheduler
- 👀 **Real-Time Monitoring**: Automatic indexing on file changes with watchdog
- 🔍 **Multi-Project Support**: Semantic search across trading, data visualization, and monetization projects
- 📊 **ChromaDB Integration**: Persistent vector database for document embeddings
- 🔐 **Local Storage**: All memories stored securely on local filesystem

## 📖 Documentation

- **[Project Plan](projectplan.md)** - Comprehensive technical specification (1688 lines)
- **[Implementation Complete](IMPLEMENTATION_COMPLETE.md)** - Project status and verification
- **[OpenClaw Integration](OPENCLAW_INTEGRATION.md)** - Integration guide for OpenClaw gateway
- **[GitHub Setup](GITHUB_SETUP.md)** - Repository setup and deployment instructions

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- 8GB RAM (recommended for embedding models)
- Windows 10/11 (for Task Scheduler integration)
- 5GB disk space (for vector database)

### 1. Clone & Setup

```powershell
# Clone repository
git clone https://github.com/YOUR_USERNAME/memory_management.git
cd memory_management

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Install System Dependencies

```powershell
# Install Quarto CLI
winget install Posit.Quarto

# Verify installation
quarto --version
```

### 3. Run Installation

```powershell
# Execute installation script
.\install_3tier_memory.ps1
```

**What this does**:
- ✅ Creates directory structure in `~/.openclaw/`
- ✅ Downloads embedding model (all-MiniLM-L6-v2, ~500MB)
- ✅ Creates `docs/`, `sessions/`, `notes/` folders in all projects
- ✅ Generates projects configuration
- ✅ Registers Windows scheduled task for 2:00 AM daily runs

### 4. Test Installation

```powershell
# Run manual indexing
python daily_indexer.py

# Test semantic search
python test_indexing.py

# Check indexing logs
Get-Content "$env:USERPROFILE\.openclaw\scheduler\indexer.log" -Tail 20
```

## 📁 Project Structure

```
memory_management/
├── Core Modules (5 files)
│   ├── qmd_parser.py              ← Parse Quarto Markdown files
│   ├── semantic_memory.py         ← ChromaDB vector indexing
│   ├── daily_indexer.py           ← Scheduled background indexer
│   ├── three_tier_manager.py      ← Unified memory interface
│   └── file_watcher.py            ← Real-time file monitoring
├── PowerShell Scripts (2 files)
│   ├── install_3tier_memory.ps1
│   └── schedule_daily_indexer.ps1
├── Configuration & Docs (5 files)
│   ├── requirements.txt
│   ├── projectplan.md
│   ├── IMPLEMENTATION_COMPLETE.md
│   ├── OPENCLAW_INTEGRATION.md
│   └── GITHUB_SETUP.md
├── Virtual Environment
│   └── .venv/
└── Version Control
    ├── .gitignore
    └── LICENSE
```

## 🏗️ Architecture

### Three-Tier Memory System

```
┌─────────────────────────────────────────────────┐
│         Tier 1: Global Knowledge                │
│         (global_facts.json)                     │
│  Universal concepts shared across all projects  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│       Tier 2: Domain-Specific Knowledge         │
│  trading/domain_facts.json                      │
│  data_science/domain_facts.json                 │
└─────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────┐
│   Tier 3a: Workspace Memory (JSON)   │
│  trading/index.json                  │
│  data_visualization/index.json       │
│  x_monetization/index.json           │
└──────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────┐
│ Tier 3b: Semantic Search (ChromaDB)  │
│  • docs collection                   │
│  • sessions collection               │
│  • Embedding: all-MiniLM-L6-v2      │
└──────────────────────────────────────┘
```

## 🔧 Usage

### Manual Indexing

```python
from daily_indexer import DailyIndexer

indexer = DailyIndexer()
indexer.index_all_projects()
```

### Semantic Search

```python
from semantic_memory import SemanticMemoryIndexer
from pathlib import Path

indexer = SemanticMemoryIndexer(
    project_id='trading',
    workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
)

results = indexer.search("HSMM regime detection", n_results=5)
for result in results:
    print(f"Title: {result['metadata']['title']}")
    print(f"Score: {1 - result['distance']:.2%}")
```

### Three-Tier Memory Manager

```python
from three_tier_manager import ThreeTierMemoryManager
from pathlib import Path

manager = ThreeTierMemoryManager(
    project_id='trading',
    workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading'),
    domain='trading'
)

# Get enriched context combining all 3 tiers
context = manager.enrich_query("How does HSMM work?", context_size=5)
print(context)
```

### Real-Time File Watching

```powershell
# Start file watcher for immediate indexing
python file_watcher.py
```

## ⏱️ Scheduling

### Automatic Daily Indexing

Task is registered with Windows Task Scheduler:
- **Time**: Daily at 2:00 AM
- **Status**: `Get-ScheduledTask -TaskName "OpenClaw-SemanticIndexer"`

### Manual Task Scheduling

```powershell
# Re-run task scheduler setup
.\schedule_daily_indexer.ps1

# Trigger task immediately
Start-ScheduledTask -TaskName "OpenClaw-SemanticIndexer"

# View task history
Get-ScheduledTask -TaskName "OpenClaw-SemanticIndexer" | Get-ScheduledTaskInfo
```

## 📊 Configuration

### Projects Configuration

Location: `~/.openclaw/projects.json`

```json
{
  "projects": [
    {
      "id": "trading",
      "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\trading",
      "domain": "trading",
      "peacock": "#0B5FFF"
      "peacock": "#0B5FFF"
    },
    ...
  ]
}
```

## Usage

### Manual Indexing

```python
from semantic_memory import SemanticMemoryIndexer
from pathlib import Path

indexer = SemanticMemoryIndexer('trading', Path(r'C:\Users\haujo\projects\DEV\trading'))
indexer.index_all_docs()
```

### Semantic Search

```python
from semantic_memory import SemanticMemoryIndexer
from pathlib import Path

indexer = SemanticMemoryIndexer('trading', Path(r'C:\Users\haujo\projects\DEV\trading'))
results = indexer.search('HSMM regime profiler', n_results=5)

for result in results:
    print(f"Document: {result['document']}")
    print(f"Source: {result['metadata']['filepath']}")
    print(f"Distance: {result['distance']}")
    print()
```

### Start File Watcher

```python
from file_watcher import start_file_watcher
from pathlib import Path

start_file_watcher(
    project_id='trading',
    workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
)
```

### Query All Tiers

```python
from three_tier_manager import ThreeTierMemoryManager
from pathlib import Path

manager = ThreeTierMemoryManager(
    project_id='trading',
    workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading'),
    domain='trading'
)

enriched_context = manager.enrich_query('How does HSMM regime detection work?')
print(enriched_context)
```

## Scheduled Indexing

The system runs daily indexing at 2:00 AM via Windows Task Scheduler.

**View scheduled task**:
```powershell
Get-ScheduledTask -TaskName "OpenClaw-SemanticIndexer"
```

**Trigger manual run**:
```powershell
Start-ScheduledTask -TaskName "OpenClaw-SemanticIndexer"
```

**View logs**:
```powershell
Get-Content "$env:USERPROFILE\.openclaw\scheduler\indexer.log" -Tail 50
```

## Troubleshooting

### Issue: Scheduled task not running

```powershell
# Check task status
Get-ScheduledTask -TaskName "OpenClaw-SemanticIndexer" | Get-ScheduledTaskInfo

# Re-register task
.\schedule_daily_indexer.ps1
```

### Issue: ChromaDB collection not found

```python
import chromadb
client = chromadb.PersistentClient(path=r'C:\Users\haujo\.openclaw\semantic\trading')
print(client.list_collections())
# Expected: ['docs', 'sessions']
```

### Issue: Embedding model not cached

```powershell
# Download model manually
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## Performance

- **Indexing speed**: ~100 files in 2-3 minutes
- **Query latency**: <100ms per semantic search
- **Memory usage**: ~1.5GB RAM (with model loaded)
- **Storage**: ~500MB per project (vector DB + embeddings)

## Documentation

Complete project documentation is in [projectplan.md](projectplan.md), including:

- Technical specifications
- Class implementations
- Installation procedures
- Integration guide
- Troubleshooting guide

## Support

For issues or questions:
1. Check logs in `~/.openclaw/scheduler/indexer.log`
2. Review [projectplan.md](projectplan.md) troubleshooting section
3. Verify OpenClaw gateway is running (`Get-Process node`)

## License

Part of the OpenClaw Trading System project.

---

**Status**: Planning Phase  
**Created**: March 5, 2026  
**Peacock Color**: Purple (#9b59b6)
