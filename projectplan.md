# Memory Management System - Project Plan

**Project Name**: OpenClaw 3-Tier Memory Management System  
**Peacock Color**: Purple (#9b59b6)  
**Created**: March 5, 2026  
**Status**: Planning Phase  

---

## 1. Executive Summary

This project implements a robust 3-tier memory management system for the OpenClaw multi-project workspace, replacing the current 2-tier JSON-based approach with a hybrid architecture that combines persistent storage, domain-specific knowledge, and semantic vector search capabilities.

### Key Objectives

- ✅ Extend OpenClaw gateway with semantic memory layer
- ✅ Index Quarto Markdown (.qmd) documentation for semantic search
- ✅ Implement daily scheduled indexing (2:00 AM)
- ✅ Support multi-project workspace (trading, data_visualization, x_monetization)
- ✅ Preserve existing OpenClaw functionality while adding new capabilities

---

## 2. Current System Analysis

### 2.1 OpenClaw Gateway Status (Verified Operational)

**Gateway Configuration**:
- **Process**: Node.js PID 30888
- **Port**: 18000 (loopback 127.0.0.1)
- **Started**: March 4, 2026 at 11:26 PM
- **Token**: f59000bd39709f81e2b1cff7f892ffae6693692ca64cc230
- **Model**: mistralai/mistral-small-3.2-24b-instruct (OpenRouter)
- **Version**: OpenClaw 2026.2.17 (4134875)
- **Memory**: Enabled (auto-index: true)

### 2.2 Current 2-Tier Architecture

```
~/.openclaw/
├── agents/main/memory/          ← Tier 1: Global (299 bytes)
│   └── memory_meta.json
│       - workspace_path
│       - memory_enabled: true
│       - auto_index: true
│       - last_updated: 2026-02-20
│
└── workspaces/                  ← Tier 2: Workspace (239 bytes)
    └── trading/memory/
        └── index.json
```

### 2.3 Limitations of Current System

- ❌ No semantic search capabilities
- ❌ No domain-level knowledge separation
- ❌ No support for .qmd documentation indexing
- ❌ No scheduled automated indexing
- ❌ Limited to flat JSON storage
- ❌ No vector embeddings for context retrieval

---

## 3. Target 3-Tier Architecture

### 3.1 Architecture Overview

```
~/.openclaw/
├── agents/main/memory/
│   ├── global/                  ← Tier 1: Universal knowledge
│   │   └── global_facts.json    (Language syntax, common patterns)
│   │
│   └── domains/                 ← Tier 2: Domain-specific knowledge (NEW)
│       ├── trading/             (Strategies, market knowledge, HSMM specs)
│       │   ├── domain_facts.json
│       │   └── conventions.json
│       └── data_science/        (ML models, analytics, visualization)
│           ├── domain_facts.json
│           └── conventions.json
│
├── workspaces/                  ← Tier 3a: Project-specific memory
│   ├── trading/memory/
│   │   └── index.json
│   ├── data_visualization/memory/
│   │   └── index.json
│   └── x_monetization/memory/
│       └── index.json
│
├── semantic/                    ← Tier 3b: Vector Database (NEW)
│   ├── trading/
│   │   ├── docs.chroma/         (ChromaDB collection)
│   │   ├── sessions.chroma/
│   │   └── index_meta.json
│   ├── data_visualization/
│   │   ├── docs.chroma/
│   │   ├── sessions.chroma/
│   │   └── index_meta.json
│   └── x_monetization/
│       ├── docs.chroma/
│       ├── sessions.chroma/
│       └── index_meta.json
│
└── scheduler/                   ← Scheduling System (NEW)
    ├── indexer.log              (Daily indexing logs)
    ├── last_run.json            (Smart re-indexing tracking)
    └── indexing_tasks.json      (Task queue)
```

### 3.2 Memory Tier Responsibilities

| Tier | Scope | Storage | Examples | Query Time |
|------|-------|---------|----------|------------|
| **Tier 1: Global** | Universal knowledge shared across all projects | JSON | Python syntax, common algorithms | Instant |
| **Tier 2: Domains** | Domain-specific knowledge shared across related projects | JSON | Trading strategies, ML model types | Instant |
| **Tier 3a: Workspace** | Project-specific facts | JSON | File paths, dependencies, conventions | Instant |
| **Tier 3b: Semantic** | Documentation, sessions, notes | ChromaDB | .qmd docs, session transcripts | <100ms |

---

## 4. Projects Configuration

### 4.1 Project Taxonomy

| Project | Path | Peacock | Domain | Python |
|---------|------|---------|--------|--------|
| **trading** | C:\Users\haujo\projects\DEV\trading | Blue (#0B5FFF) | trading | .venv\Scripts\python.exe ✅ |
| **data_visualization** | C:\Users\haujo\projects\DEV\Data_visualization | Green (#0BBF5F) | data_science | .venv\Scripts\python.exe ✅ |
| **x_monetization** | C:\Users\haujo\projects\DEV\X_Monetization | TBD | trading | TBD |
| **memory_management** | C:\Users\haujo\projects\DEV\memory_management | Purple (#9b59b6) | infrastructure | .venv\Scripts\python.exe |

### 4.2 Domain Mapping

**Trading Domain** (macro regime modeling, market analysis):
- trading project
- x_monetization project

**Data Science Domain** (ML models, analytics, visualization):
- data_visualization project

**Infrastructure Domain** (system architecture, memory management):
- memory_management project

---

## 5. Technical Requirements

### 5.1 System Requirements

| Component | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| **OS** | Windows 10/11 | ✅ Met | Current: Windows |
| **Python** | >= 3.10 | ✅ Met | .venv verified in projects |
| **RAM** | >= 8 GB | ⏳ TBD | Recommended for embedding model |
| **Disk** | >= 5 GB free | ⏳ TBD | For vector DB + models |
| **Quarto** | >= 1.3 | ⏳ Install | winget install Posit.Quarto |
| **OpenClaw** | Running | ✅ Met | PID 30888, port 18000 |

### 5.2 Python Dependencies

```bash
# Core semantic indexing
pip install sentence-transformers>=2.3.0  # ~500MB model download
pip install chromadb>=0.4.22             # Vector database

# Quarto .qmd file support
pip install quartodoc                    # Quarto documentation parser
pip install nbformat                     # Notebook format support
pip install jupyter-client               # Jupyter integration

# File system monitoring
pip install watchdog>=3.0.0              # Real-time file watcher

# Task scheduling
pip install schedule>=1.2.0              # Python task scheduler

# Utilities
pip install markdown>=3.5.0              # Markdown parsing
pip install pyyaml>=6.0                  # YAML parsing
pip install pandas>=2.0.0                # Data manipulation
pip install numpy>=1.24.0                # Numerical operations
```

### 5.3 System Tools

```powershell
# Install Quarto CLI
winget install Posit.Quarto

# Verify installation
quarto --version  # Should show >= 1.3
```

---

## 6. Quarto Markdown (.qmd) Processing

### 6.1 File Format Overview

Quarto Markdown combines:
- **YAML frontmatter** (metadata: title, date, tags, author)
- **Markdown body** (documentation content)
- **Code cells** (Python/R code blocks)
- **Outputs** (execution results)

Example `.qmd` file:
```markdown
---
title: "HSMM Regime Profiler Specification"
date: "2026-02-24"
tags: ["trading", "machine-learning", "regime-detection"]
author: "OpenClaw Trading System"
---

# HSMM Regime Profiler

This document specifies the Hidden Semi-Markov Model...

\`\`\`python
from hsmmlearn.hsmm import GaussianHSMM
model = GaussianHSMM(n_components=2, ...)
\`\`\`
```

### 6.2 QmdParser Class Specification

**File**: `qmd_parser.py`

```python
# -*- coding: utf-8 -*-
"""
QmdParser - Parse Quarto Markdown (.qmd) files for memory indexing
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class QmdParser:
    """
    Parse Quarto Markdown files extracting:
    - YAML frontmatter (metadata)
    - Markdown content (main documentation)
    - Code cells (Python/R code blocks)
    - File metadata (path, modified time)
    """
    
    def __init__(self):
        self.code_fence_pattern = re.compile(
            r'```(\w+)\n(.*?)```', 
            re.DOTALL
        )
    
    def parse_qmd(self, filepath: Path) -> Dict:
        """
        Parse a .qmd file and extract all components.
        
        Args:
            filepath: Path to .qmd file
            
        Returns:
            Dict with keys:
                - frontmatter: Dict (parsed YAML)
                - content: str (Markdown body without frontmatter)
                - code_cells: List[Dict] (language, code)
                - filepath: str
                - modified: datetime
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        # Extract YAML frontmatter
        frontmatter = {}
        content = raw_content
        
        if raw_content.startswith('---'):
            parts = raw_content.split('---', 2)
            if len(parts) >= 3:
                yaml_str = parts[1]
                content = parts[2].strip()
                try:
                    frontmatter = yaml.safe_load(yaml_str)
                except yaml.YAMLError:
                    frontmatter = {}
        
        # Extract code cells
        code_cells = []
        for match in self.code_fence_pattern.finditer(content):
            language = match.group(1)
            code = match.group(2).strip()
            code_cells.append({
                'language': language,
                'code': code
            })
        
        # File metadata
        stat = filepath.stat()
        modified = datetime.fromtimestamp(stat.st_mtime)
        
        return {
            'frontmatter': frontmatter,
            'content': content,
            'code_cells': code_cells,
            'filepath': str(filepath),
            'modified': modified
        }
    
    def extract_tags(self, parsed: Dict) -> List[str]:
        """Extract tags from frontmatter."""
        frontmatter = parsed.get('frontmatter', {})
        tags = frontmatter.get('tags', [])
        return tags if isinstance(tags, list) else []
    
    def extract_title(self, parsed: Dict) -> str:
        """Extract title from frontmatter or first heading."""
        frontmatter = parsed.get('frontmatter', {})
        if 'title' in frontmatter:
            return frontmatter['title']
        
        # Fallback: first heading in content
        content = parsed.get('content', '')
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1)
        
        return Path(parsed['filepath']).stem
```

---

## 7. Semantic Memory Indexing

### 7.1 Vector Database Technology

**Selected**: ChromaDB (embedded, no server required)

**Alternatives**:
- FAISS (faster queries, more setup)
- Qdrant (production-grade, requires Docker)

**Embedding Model**: sentence-transformers 'all-MiniLM-L6-v2'
- Dimensions: 384
- Size: ~500MB download
- Speed: ~100 docs/sec
- Quality: Good for documentation search

### 7.2 SemanticMemoryIndexer Class Specification

**File**: `semantic_memory.py`

```python
# -*- coding: utf-8 -*-
"""
SemanticMemoryIndexer - Tier 3 semantic indexing using ChromaDB
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List, Dict
import json
from datetime import datetime

from qmd_parser import QmdParser

class SemanticMemoryIndexer:
    """
    Tier 3 - Semantic memory indexing for .qmd, .md, and documentation.
    
    Uses:
    - ChromaDB for vector storage
    - sentence-transformers for embeddings
    - Separate collections for docs and sessions
    """
    
    def __init__(self, project_id: str, workspace_root: Path):
        """
        Initialize semantic indexer for a project.
        
        Args:
            project_id: Unique project identifier (e.g., 'trading')
            workspace_root: Project root directory
        """
        self.project_id = project_id
        self.workspace_root = Path(workspace_root)
        
        # Vector DB path
        self.db_path = Path.home() / '.openclaw' / 'semantic' / project_id
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Embedding model
        print(f"    [Semantic] Loading embedding model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Collections
        self.docs_collection = self.client.get_or_create_collection(
            name='docs',
            metadata={'description': 'Documentation files'}
        )
        
        self.sessions_collection = self.client.get_or_create_collection(
            name='sessions',
            metadata={'description': 'Session transcripts'}
        )
        
        # Parser
        self.qmd_parser = QmdParser()
        
        # Index metadata
        self.index_meta_path = self.db_path / 'index_meta.json'
        self.index_meta = self._load_index_meta()
    
    def _load_index_meta(self) -> Dict:
        """Load indexing metadata (last indexed times)."""
        if self.index_meta_path.exists():
            with open(self.index_meta_path, 'r') as f:
                return json.load(f)
        return {'files': {}}
    
    def _save_index_meta(self):
        """Save indexing metadata."""
        with open(self.index_meta_path, 'w') as f:
            json.dump(self.index_meta, f, indent=2, default=str)
    
    def _chunk_text(self, text: str, chunk_size: int = 500, 
                    overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Characters per chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        
        return chunks
    
    def index_qmd_file(self, filepath: Path, collection_name: str = 'docs'):
        """
        Index a .qmd file to the semantic database.
        
        Args:
            filepath: Path to .qmd file
            collection_name: 'docs' or 'sessions'
        """
        print(f"    [Semantic] Indexing {filepath.name}...")
        
        # Parse .qmd file
        parsed = self.qmd_parser.parse_qmd(filepath)
        content = parsed['content']
        title = self.qmd_parser.extract_title(parsed)
        tags = self.qmd_parser.extract_tags(parsed)
        
        # Chunk content
        chunks = self._chunk_text(content, chunk_size=500, overlap=50)
        
        # Generate embeddings
        embeddings = self.embedder.encode(chunks).tolist()
        
        # Prepare metadata
        metadatas = []
        ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filepath.stem}_{i}"
            metadatas.append({
                'filepath': str(filepath),
                'title': title,
                'tags': ','.join(tags),
                'chunk_index': i,
                'modified': str(parsed['modified'])
            })
            ids.append(chunk_id)
        
        # Select collection
        collection = (self.docs_collection if collection_name == 'docs' 
                     else self.sessions_collection)
        
        # Upsert to ChromaDB
        collection.upsert(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
        # Update index metadata
        self.index_meta['files'][str(filepath)] = {
            'indexed_at': datetime.now().isoformat(),
            'chunks': len(chunks),
            'collection': collection_name
        }
        self._save_index_meta()
    
    def index_markdown_file(self, filepath: Path, collection_name: str = 'docs'):
        """
        Index a .md file to the semantic database.
        
        Args:
            filepath: Path to .md file
            collection_name: 'docs' or 'sessions'
        """
        print(f"    [Semantic] Indexing {filepath.name}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chunk content
        chunks = self._chunk_text(content, chunk_size=500, overlap=50)
        
        # Generate embeddings
        embeddings = self.embedder.encode(chunks).tolist()
        
        # Prepare metadata
        metadatas = []
        ids = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filepath.stem}_{i}"
            metadatas.append({
                'filepath': str(filepath),
                'title': filepath.stem,
                'chunk_index': i,
                'modified': str(datetime.fromtimestamp(filepath.stat().st_mtime))
            })
            ids.append(chunk_id)
        
        # Select collection
        collection = (self.docs_collection if collection_name == 'docs' 
                     else self.sessions_collection)
        
        # Upsert to ChromaDB
        collection.upsert(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )
        
        # Update index metadata
        self.index_meta['files'][str(filepath)] = {
            'indexed_at': datetime.now().isoformat(),
            'chunks': len(chunks),
            'collection': collection_name
        }
        self._save_index_meta()
    
    def search(self, query: str, n_results: int = 5, 
               collection_name: str = 'docs') -> List[Dict]:
        """
        Semantic search across indexed documents.
        
        Args:
            query: Search query
            n_results: Number of results to return
            collection_name: 'docs' or 'sessions'
            
        Returns:
            List of dicts with keys: document, metadata, distance
        """
        # Generate query embedding
        query_embedding = self.embedder.encode([query])[0].tolist()
        
        # Select collection
        collection = (self.docs_collection if collection_name == 'docs' 
                     else self.sessions_collection)
        
        # Query ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted = []
        for i in range(len(results['documents'][0])):
            formatted.append({
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return formatted
    
    def index_all_docs(self):
        """Index all .qmd and .md files in docs/ and sessions/."""
        docs_dir = self.workspace_root / 'docs'
        sessions_dir = self.workspace_root / 'sessions'
        notes_dir = self.workspace_root / 'notes'
        
        indexed_count = 0
        
        # Index docs/
        if docs_dir.exists():
            for filepath in docs_dir.rglob('*.qmd'):
                self.index_qmd_file(filepath, collection_name='docs')
                indexed_count += 1
            
            for filepath in docs_dir.rglob('*.md'):
                self.index_markdown_file(filepath, collection_name='docs')
                indexed_count += 1
        
        # Index sessions/
        if sessions_dir.exists():
            for filepath in sessions_dir.rglob('*.qmd'):
                self.index_qmd_file(filepath, collection_name='sessions')
                indexed_count += 1
        
        # Index notes/
        if notes_dir.exists():
            for filepath in notes_dir.rglob('*.md'):
                self.index_markdown_file(filepath, collection_name='docs')
                indexed_count += 1
        
        print(f"    [Semantic] Indexed {indexed_count} files for {self.project_id}")
        return indexed_count
```

---

## 8. Daily Scheduled Indexing

### 8.1 Scheduling Approach

**Primary**: Windows Task Scheduler (native, reliable, survives reboots)
- Task name: `OpenClaw-SemanticIndexer`
- Trigger: Daily at 2:00 AM
- Action: `python semantic_indexer_daemon.py`
- Settings: Allow start if on batteries, don't stop on battery power

**Alternative**: Python `schedule` daemon (background process)

**Real-time**: Watchdog file watcher (immediate indexing on file save)

### 8.2 DailyIndexer Class Specification

**File**: `daily_indexer.py`

```python
# -*- coding: utf-8 -*-
"""
DailyIndexer - Scheduled background indexer for all projects
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging

from semantic_memory import SemanticMemoryIndexer

class DailyIndexer:
    """
    Daily background indexer for all projects.
    
    Features:
    - Smart re-indexing (only modified files)
    - Logs to ~/.openclaw/scheduler/indexer.log
    - Tracks last run timestamp
    """
    
    def __init__(self):
        self.scheduler_dir = Path.home() / '.openclaw' / 'scheduler'
        self.scheduler_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.scheduler_dir / 'indexer.log'
        self.last_run_file = self.scheduler_dir / 'last_run.json'
        
        # Setup logging
        logging.basicConfig(
            filename=str(self.log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load last run info
        self.last_run = self._load_last_run()
        
        # Load projects config
        self.projects = self._load_projects_config()
    
    def _load_last_run(self) -> Dict:
        """Load last run metadata."""
        if self.last_run_file.exists():
            with open(self.last_run_file, 'r') as f:
                return json.load(f)
        return {'timestamp': None, 'indexed_files': {}}
    
    def _save_last_run(self):
        """Save last run metadata."""
        self.last_run['timestamp'] = datetime.now().isoformat()
        with open(self.last_run_file, 'w') as f:
            json.dump(self.last_run, f, indent=2)
    
    def _load_projects_config(self) -> List[Dict]:
        """Load projects configuration."""
        config_path = Path.home() / '.openclaw' / 'projects.json'
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)['projects']
        
        # Default configuration
        return [
            {
                'id': 'trading',
                'name': 'trading',
                'workspace_root': r'C:\Users\haujo\projects\DEV\trading',
                'domain': 'trading',
                'peacock': '#0B5FFF'
            },
            {
                'id': 'data_visualization',
                'name': 'data_visualization',
                'workspace_root': r'C:\Users\haujo\projects\DEV\Data_visualization',
                'domain': 'data_science',
                'peacock': '#0BBF5F'
            },
            {
                'id': 'x_monetization',
                'name': 'x_monetization',
                'workspace_root': r'C:\Users\haujo\projects\DEV\X_Monetization',
                'domain': 'trading',
                'peacock': '#FF6B6B'
            }
        ]
    
    def _should_reindex_file(self, filepath: Path) -> bool:
        """
        Check if file should be re-indexed.
        
        Returns True if:
        - File never indexed before
        - File modified since last indexing
        """
        filepath_str = str(filepath)
        
        if filepath_str not in self.last_run['indexed_files']:
            return True
        
        last_indexed = self.last_run['indexed_files'][filepath_str]
        last_modified = datetime.fromtimestamp(filepath.stat().st_mtime)
        last_indexed_dt = datetime.fromisoformat(last_indexed)
        
        return last_modified > last_indexed_dt
    
    def index_project(self, project: Dict) -> int:
        """
        Index a single project.
        
        Args:
            project: Project config dict
            
        Returns:
            Number of files indexed
        """
        self.logger.info(f"Indexing project: {project['id']}")
        print(f"\n[Indexer] Processing project: {project['id']}")
        
        workspace_root = Path(project['workspace_root'])
        if not workspace_root.exists():
            self.logger.warning(f"Workspace not found: {workspace_root}")
            return 0
        
        # Create indexer
        indexer = SemanticMemoryIndexer(
            project_id=project['id'],
            workspace_root=workspace_root
        )
        
        # Find files to index
        docs_dir = workspace_root / 'docs'
        sessions_dir = workspace_root / 'sessions'
        notes_dir = workspace_root / 'notes'
        
        files_to_index = []
        
        # Collect .qmd and .md files
        for directory, collection in [
            (docs_dir, 'docs'),
            (sessions_dir, 'sessions'),
            (notes_dir, 'docs')
        ]:
            if not directory.exists():
                continue
            
            for pattern in ['*.qmd', '*.md']:
                for filepath in directory.rglob(pattern):
                    if self._should_reindex_file(filepath):
                        files_to_index.append((filepath, collection))
        
        # Index files
        indexed_count = 0
        for filepath, collection in files_to_index:
            try:
                if filepath.suffix == '.qmd':
                    indexer.index_qmd_file(filepath, collection_name=collection)
                else:
                    indexer.index_markdown_file(filepath, collection_name=collection)
                
                self.last_run['indexed_files'][str(filepath)] = datetime.now().isoformat()
                indexed_count += 1
                
            except Exception as e:
                self.logger.error(f"Failed to index {filepath}: {e}")
        
        self.logger.info(f"Indexed {indexed_count} files for {project['id']}")
        return indexed_count
    
    def index_all_projects(self):
        """Index all configured projects."""
        self.logger.info("=" * 80)
        self.logger.info("Starting daily indexing run")
        print("\n" + "=" * 80)
        print("DAILY SEMANTIC INDEXER - STARTING")
        print("=" * 80)
        
        total_indexed = 0
        
        for project in self.projects:
            count = self.index_project(project)
            total_indexed += count
        
        self._save_last_run()
        
        self.logger.info(f"Daily indexing complete. Indexed {total_indexed} files.")
        print(f"\n[Indexer] Complete. Indexed {total_indexed} files across {len(self.projects)} projects.")
        print("=" * 80)


def main():
    """Main entry point for daily indexer."""
    indexer = DailyIndexer()
    indexer.index_all_projects()


if __name__ == '__main__':
    main()
```

### 8.3 schedule_daily_indexer.ps1 Script

**File**: `schedule_daily_indexer.ps1`

```powershell
# Schedule daily indexer with Windows Task Scheduler

$TaskName = "OpenClaw-SemanticIndexer"
$PythonExe = "C:\Users\haujo\projects\DEV\memory_management\.venv\Scripts\python.exe"
$ScriptPath = "C:\Users\haujo\projects\DEV\memory_management\daily_indexer.py"

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "[INFO] Task already exists. Removing old task..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create action
$Action = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument $ScriptPath

# Create trigger (daily at 2:00 AM)
$Trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM

# Create settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

# Register task
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Daily semantic indexing for OpenClaw memory system"

Write-Host "[OK] Task '$TaskName' registered successfully"
Write-Host "     Trigger: Daily at 2:00 AM"
Write-Host "     Action: $PythonExe $ScriptPath"
```

---

## 9. Real-Time File Watching

### 9.1 FileWatcher Class Specification

**File**: `file_watcher.py`

```python
# -*- coding: utf-8 -*-
"""
FileWatcher - Real-time file system monitoring for immediate indexing
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from typing import Dict
import time
import logging

from semantic_memory import SemanticMemoryIndexer

class QmdFileHandler(FileSystemEventHandler):
    """
    Watch for .qmd and .md file changes and auto-index.
    """
    
    def __init__(self, project_id: str, workspace_root: Path):
        super().__init__()
        self.project_id = project_id
        self.workspace_root = workspace_root
        
        self.indexer = SemanticMemoryIndexer(
            project_id=project_id,
            workspace_root=workspace_root
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _should_index(self, filepath: Path) -> bool:
        """Check if file should be indexed."""
        if filepath.suffix not in ['.qmd', '.md']:
            return False
        
        # Check if in docs/, sessions/, or notes/
        try:
            relative = filepath.relative_to(self.workspace_root)
            if relative.parts[0] in ['docs', 'sessions', 'notes']:
                return True
        except ValueError:
            pass
        
        return False
    
    def _determine_collection(self, filepath: Path) -> str:
        """Determine which collection to index to."""
        try:
            relative = filepath.relative_to(self.workspace_root)
            if relative.parts[0] == 'sessions':
                return 'sessions'
        except ValueError:
            pass
        
        return 'docs'
    
    def on_modified(self, event):
        """Handle file modification."""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        if self._should_index(filepath):
            collection = self._determine_collection(filepath)
            
            self.logger.info(f"File modified: {filepath.name}, re-indexing...")
            try:
                if filepath.suffix == '.qmd':
                    self.indexer.index_qmd_file(filepath, collection_name=collection)
                else:
                    self.indexer.index_markdown_file(filepath, collection_name=collection)
                
                self.logger.info(f"Successfully indexed: {filepath.name}")
            except Exception as e:
                self.logger.error(f"Failed to index {filepath.name}: {e}")
    
    def on_created(self, event):
        """Handle file creation."""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        if self._should_index(filepath):
            collection = self._determine_collection(filepath)
            
            self.logger.info(f"New file detected: {filepath.name}, indexing...")
            try:
                if filepath.suffix == '.qmd':
                    self.indexer.index_qmd_file(filepath, collection_name=collection)
                else:
                    self.indexer.index_markdown_file(filepath, collection_name=collection)
                
                self.logger.info(f"Successfully indexed: {filepath.name}")
            except Exception as e:
                self.logger.error(f"Failed to index {filepath.name}: {e}")


def start_file_watcher(project_id: str, workspace_root: Path):
    """
    Start file watcher for a project.
    
    Args:
        project_id: Project identifier
        workspace_root: Project root directory
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    event_handler = QmdFileHandler(project_id, workspace_root)
    observer = Observer()
    
    # Watch docs/, sessions/, notes/
    for directory in ['docs', 'sessions', 'notes']:
        watch_path = workspace_root / directory
        if watch_path.exists():
            observer.schedule(event_handler, str(watch_path), recursive=True)
            logger.info(f"Watching: {watch_path}")
    
    observer.start()
    logger.info(f"File watcher started for project: {project_id}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("File watcher stopped")
    
    observer.join()


if __name__ == '__main__':
    # Example: watch trading project
    start_file_watcher(
        project_id='trading',
        workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
    )
```

---

## 10. Three-Tier Memory Manager

### 10.1 ThreeTierMemoryManager Class Specification

**File**: `three_tier_manager.py`

```python
# -*- coding: utf-8 -*-
"""
ThreeTierMemoryManager - Unified interface for 3-tier memory system
"""

import json
from pathlib import Path
from typing import Dict, List

from semantic_memory import SemanticMemoryIndexer

class ThreeTierMemoryManager:
    """
    Manages 3-tier memory with semantic search.
    
    Query flow:
    1. Query Tier 3 (semantic) for relevant documentation
    2. Load Tier 2 (domain) facts
    3. Load Tier 1 (global) facts
    4. Combine and return enriched context
    """
    
    def __init__(self, project_id: str, workspace_root: Path, domain: str):
        """
        Initialize 3-tier memory manager.
        
        Args:
            project_id: Project identifier (e.g., 'trading')
            workspace_root: Project root directory
            domain: Domain name (e.g., 'trading', 'data_science')
        """
        self.project_id = project_id
        self.workspace_root = Path(workspace_root)
        self.domain = domain
        
        # Tier 3: Semantic indexer
        self.semantic = SemanticMemoryIndexer(project_id, workspace_root)
        
        # Memory paths
        openclaw_home = Path.home() / '.openclaw'
        self.global_memory_path = openclaw_home / 'agents' / 'main' / 'memory' / 'global'
        self.domain_memory_path = openclaw_home / 'agents' / 'main' / 'memory' / 'domains' / domain
        self.workspace_memory_path = openclaw_home / 'workspaces' / project_id / 'memory'
    
    def _load_json_memory(self, memory_path: Path, filename: str) -> Dict:
        """Load JSON memory file."""
        filepath = memory_path / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
    
    def enrich_query(self, query: str, context_size: int = 5) -> str:
        """
        Enrich a query with context from all 3 tiers.
        
        Args:
            query: User query
            context_size: Number of semantic search results
            
        Returns:
            Enriched context string for LLM
        """
        context_parts = []
        
        # Tier 3b: Semantic search
        semantic_results = self.semantic.search(query, n_results=context_size)
        if semantic_results:
            context_parts.append("## Relevant Documentation\n")
            for i, result in enumerate(semantic_results, 1):
                doc = result['document']
                meta = result['metadata']
                filepath = meta.get('filepath', 'unknown')
                title = meta.get('title', 'Untitled')
                
                context_parts.append(f"### {i}. {title}\n")
                context_parts.append(f"Source: {filepath}\n")
                context_parts.append(f"{doc}\n\n")
        
        # Tier 2: Domain knowledge
        domain_facts = self._load_json_memory(self.domain_memory_path, 'domain_facts.json')
        if domain_facts:
            context_parts.append("## Domain Knowledge\n")
            for key, value in domain_facts.items():
                context_parts.append(f"- {key}: {value}\n")
            context_parts.append("\n")
        
        # Tier 1: Global knowledge
        global_facts = self._load_json_memory(self.global_memory_path, 'global_facts.json')
        if global_facts:
            context_parts.append("## Global Knowledge\n")
            for key, value in global_facts.items():
                context_parts.append(f"- {key}: {value}\n")
            context_parts.append("\n")
        
        # Tier 3a: Workspace facts
        workspace_index = self._load_json_memory(self.workspace_memory_path, 'index.json')
        if workspace_index:
            context_parts.append("## Workspace Facts\n")
            context_parts.append(f"Project: {self.project_id}\n")
            context_parts.append(f"Domain: {self.domain}\n")
            if 'python_interpreter' in workspace_index:
                context_parts.append(f"Python: {workspace_index['python_interpreter']}\n")
            context_parts.append("\n")
        
        return ''.join(context_parts)
    
    def search_documentation(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search documentation only (Tier 3b).
        
        Args:
            query: Search query
            n_results: Number of results
            
        Returns:
            List of search results
        """
        return self.semantic.search(query, n_results=n_results, collection_name='docs')
    
    def search_sessions(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search session transcripts (Tier 3b).
        
        Args:
            query: Search query
            n_results: Number of results
            
        Returns:
            List of search results
        """
        return self.semantic.search(query, n_results=n_results, collection_name='sessions')
```

---

## 11. Installation Script

### 11.1 install_3tier_memory.ps1

**File**: `install_3tier_memory.ps1`

```powershell
# -*- coding: utf-8 -*-
# Install 3-Tier Memory System

Write-Host @"
================================================================================
3-TIER MEMORY SYSTEM INSTALLATION
================================================================================
"@

$ErrorActionPreference = "Stop"

# ------------------------------------------------------------------ #
# Step 1: Install Quarto CLI
# ------------------------------------------------------------------ #
Write-Host "`n[1/6] Installing Quarto CLI..."

try {
    $quartoVersion = & quarto --version 2>$null
    Write-Host "    [OK] Quarto already installed: $quartoVersion"
} catch {
    Write-Host "    Installing Quarto via winget..."
    winget install Posit.Quarto --accept-source-agreements --accept-package-agreements
    Write-Host "    [OK] Quarto installed"
}

# ------------------------------------------------------------------ #
# Step 2: Install Python packages
# ------------------------------------------------------------------ #
Write-Host "`n[2/6] Installing Python packages..."

$packages = @(
    "sentence-transformers>=2.3.0",
    "chromadb>=0.4.22",
    "quartodoc",
    "nbformat",
    "jupyter-client",
    "watchdog>=3.0.0",
    "schedule>=1.2.0",
    "markdown>=3.5.0",
    "pyyaml>=6.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0"
)

foreach ($package in $packages) {
    Write-Host "    Installing $package..."
    & python -m pip install $package --quiet
}

Write-Host "    [OK] All Python packages installed"

# ------------------------------------------------------------------ #
# Step 3: Create directory structure
# ------------------------------------------------------------------ #
Write-Host "`n[3/6] Creating directory structure..."

$openclawHome = "$env:USERPROFILE\.openclaw"

$directories = @(
    "$openclawHome\agents\main\memory\global",
    "$openclawHome\agents\main\memory\domains\trading",
    "$openclawHome\agents\main\memory\domains\data_science",
    "$openclawHome\semantic\trading",
    "$openclawHome\semantic\data_visualization",
    "$openclawHome\semantic\x_monetization",
    "$openclawHome\scheduler"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    Write-Host "    [OK] Created $dir"
}

# ------------------------------------------------------------------ #
# Step 4: Create project docs folders
# ------------------------------------------------------------------ #
Write-Host "`n[4/6] Creating project documentation folders..."

$projects = @(
    "C:\Users\haujo\projects\DEV\trading",
    "C:\Users\haujo\projects\DEV\Data_visualization",
    "C:\Users\haujo\projects\DEV\X_Monetization"
)

foreach ($project in $projects) {
    if (Test-Path $project) {
        foreach ($folder in @("docs", "sessions", "notes")) {
            $folderPath = Join-Path $project $folder
            New-Item -ItemType Directory -Force -Path $folderPath | Out-Null
            Write-Host "    [OK] Created $folderPath"
        }
    }
}

# ------------------------------------------------------------------ #
# Step 5: Download sentence transformer model
# ------------------------------------------------------------------ #
Write-Host "`n[5/6] Downloading sentence transformer model (~500MB)..."

$pythonScript = @"
from sentence_transformers import SentenceTransformer
print('Downloading model...')
model = SentenceTransformer('all-MiniLM-L6-v2')
print('Model downloaded and cached successfully')
"@

$pythonScript | & python -
Write-Host "    [OK] Model cached"

# ------------------------------------------------------------------ #
# Step 6: Setup Windows Task Scheduler
# ------------------------------------------------------------------ #
Write-Host "`n[6/6] Setting up Windows Task Scheduler..."

$TaskName = "OpenClaw-SemanticIndexer"
$PythonExe = "C:\Users\haujo\projects\DEV\memory_management\.venv\Scripts\python.exe"
$ScriptPath = "C:\Users\haujo\projects\DEV\memory_management\daily_indexer.py"

# Check if task exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "    [INFO] Task already exists, updating..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create task
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument $ScriptPath
$Trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Daily semantic indexing for OpenClaw memory system" | Out-Null

Write-Host "    [OK] Task '$TaskName' registered (daily at 2:00 AM)"

# ------------------------------------------------------------------ #
# Done
# ------------------------------------------------------------------ #
Write-Host @"

================================================================================
INSTALLATION COMPLETE
================================================================================

Next steps:
1. Create Python virtual environment for memory_management project
2. Run initial indexing: python daily_indexer.py
3. Test semantic search: python -c "from semantic_memory import SemanticMemoryIndexer; ..."
4. Check logs: Get-Content ~/.openclaw/scheduler/indexer.log

Scheduled task 'OpenClaw-SemanticIndexer' will run daily at 2:00 AM.

"@
```

---

## 12. Projects Configuration

### 12.1 projects.json

**File**: `~/.openclaw/projects.json`

```json
{
  "version": "1.0",
  "created_at": "2026-03-05",
  "projects": [
    {
      "id": "trading",
      "name": "trading",
      "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\trading",
      "domain": "trading",
      "peacock": "#0B5FFF",
      "python_interpreter": ".venv\\Scripts\\python.exe",
      "description": "Crypto trading system with HSMM regime detection"
    },
    {
      "id": "data_visualization",
      "name": "data_visualization",
      "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\Data_visualization",
      "domain": "data_science",
      "peacock": "#0BBF5F",
      "python_interpreter": ".venv\\Scripts\\python.exe",
      "description": "Global market cap data visualization and analytics"
    },
    {
      "id": "x_monetization",
      "name": "x_monetization",
      "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\X_Monetization",
      "domain": "trading",
      "peacock": "#FF6B6B",
      "python_interpreter": ".venv\\Scripts\\python.exe",
      "description": "𝕏 (Twitter) monetization and content strategy"
    },
    {
      "id": "memory_management",
      "name": "memory_management",
      "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\memory_management",
      "domain": "infrastructure",
      "peacock": "#9b59b6",
      "python_interpreter": ".venv\\Scripts\\python.exe",
      "description": "3-tier memory management system for OpenClaw"
    }
  ]
}
```

---

## 13. Implementation Roadmap

### 13.1 Phase 1: Foundation Setup (1-2 hours)

**Status**: ⏳ NOT STARTED

**Tasks**:
- [x] Create memory_management project directory
- [x] Configure Peacock purple color (#9b59b6)
- [x] Create projectplan.md (this document)
- [ ] Create Python virtual environment
- [ ] Install dependencies (sentence-transformers, chromadb, etc.)
- [ ] Install Quarto CLI
- [ ] Create directory structure in ~/.openclaw/

**Commands**:
```powershell
cd C:\Users\haujo\projects\DEV\memory_management
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
winget install Posit.Quarto
.\install_3tier_memory.ps1
```

### 13.2 Phase 2: Core Classes Implementation (2-3 hours)

**Status**: ⏳ NOT STARTED

**Tasks**:
- [ ] Create `qmd_parser.py` (QmdParser class)
- [ ] Create `semantic_memory.py` (SemanticMemoryIndexer class)
- [ ] Create `daily_indexer.py` (DailyIndexer class)
- [ ] Create `three_tier_manager.py` (ThreeTierMemoryManager class)
- [ ] Create `file_watcher.py` (QmdFileHandler class)
- [ ] Create unit tests for each class

**Files to Create**:
- qmd_parser.py (~100 lines)
- semantic_memory.py (~250 lines)
- daily_indexer.py (~150 lines)
- three_tier_manager.py (~100 lines)
- file_watcher.py (~100 lines)

### 13.3 Phase 3: Integration (1-2 hours)

**Status**: ⏳ NOT STARTED

**Tasks**:
- [ ] Create projects.json configuration
- [ ] Update OpenClaw integration (if needed)
- [ ] Create startup script for file watcher
- [ ] Create manual indexing script
- [ ] Test integration with OpenClaw gateway

**Files to Create**:
- ~/.openclaw/projects.json
- run_file_watcher.py
- manual_index.py

### 13.4 Phase 4: Documentation Structure (1 hour)

**Status**: ⏳ NOT STARTED

**Tasks**:
- [ ] Create docs/ folders in all projects
- [ ] Create template .qmd files
- [ ] Create FOLDER_STRUCTURE.md for each project
- [ ] Create ENVIRONMENT.md for each project
- [ ] Create CONVENTIONS.md for each project

**Template Files**:
```
trading/docs/
├── FOLDER_STRUCTURE.md
├── ENVIRONMENT.md
├── CONVENTIONS.md
├── planning/
│   └── HSMM_PureModelTradingProfiler_V2.md (existing)
└── specifications/
    └── hsmm_regime_detection.qmd (new)
```

### 13.5 Phase 5: Testing & Validation (1-2 hours)

**Status**: ⏳ NOT STARTED

**Tasks**:
- [ ] Test QmdParser with sample .qmd files
- [ ] Test semantic indexing (create test docs, verify ChromaDB)
- [ ] Test scheduled task (trigger manually, verify logging)
- [ ] Test file watcher (edit .qmd file, verify immediate indexing)
- [ ] Test semantic search (query for documentation chunks)
- [ ] Test ThreeTierMemoryManager.enrich_query()
- [ ] Verify all 3 projects indexed correctly

**Validation Commands**:
```powershell
# Test semantic search
python -c "from semantic_memory import SemanticMemoryIndexer; indexer = SemanticMemoryIndexer('trading', Path(r'C:\Users\haujo\projects\DEV\trading')); print(indexer.search('HSMM regime profiler'))"

# Check scheduled task
Get-ScheduledTask -TaskName "OpenClaw-SemanticIndexer"

# Check logs
Get-Content "$env:USERPROFILE\.openclaw\scheduler\indexer.log" -Tail 20

# Verify ChromaDB collections
python -c "import chromadb; client = chromadb.PersistentClient(path=r'C:\Users\haujo\.openclaw\semantic\trading'); print(client.list_collections())"
```

### 13.6 Total Estimated Time: 6-10 hours

---

## 14. Success Criteria

### 14.1 Installation Success Indicators

✅ Quarto CLI installed (`quarto --version` works)  
✅ Python packages installed (`pip list | findstr sentence-transformers`)  
✅ Directory structure created (`~/.openclaw/semantic/`, etc.)  
✅ Scheduled task registered (visible in Task Scheduler)  
✅ Embedding model downloaded (~500MB in cache)  
✅ ChromaDB collections created (docs, sessions)  
✅ File watcher running (monitors docs/, sessions/, notes/)  
✅ Logs updating daily in `~/.openclaw/scheduler/indexer.log`

### 14.2 Functional Success Indicators

✅ .qmd files parsed correctly (YAML frontmatter + Markdown body + code cells)  
✅ Semantic search returns relevant results (<100ms query time)  
✅ Daily indexing runs automatically at 2:00 AM  
✅ File watcher indexes new/modified files immediately  
✅ All 3 projects (trading, data_visualization, x_monetization) indexed  
✅ ThreeTierMemoryManager combines Tier 1 + 2 + 3 context correctly  
✅ OpenClaw gateway continues running without issues  

---

## 15. Maintenance & Monitoring

### 15.1 Daily Monitoring

**Check logs**:
```powershell
Get-Content "$env:USERPROFILE\.openclaw\scheduler\indexer.log" -Tail 50
```

**Verify scheduled task**:
```powershell
Get-ScheduledTask -TaskName "OpenClaw-SemanticIndexer" | Get-ScheduledTaskInfo
```

**Check ChromaDB size**:
```powershell
Get-ChildItem -Recurse "$env:USERPROFILE\.openclaw\semantic" | Measure-Object -Property Length -Sum
```

### 15.2 Troubleshooting

**Issue: Scheduled task not running**
```powershell
# Check task history
Get-ScheduledTask -TaskName "OpenClaw-SemanticIndexer" | Get-ScheduledTaskInfo

# Trigger manually
Start-ScheduledTask -TaskName "OpenClaw-SemanticIndexer"
```

**Issue: ChromaDB collection not found**
```python
import chromadb
client = chromadb.PersistentClient(path=r'C:\Users\haujo\.openclaw\semantic\trading')
print(client.list_collections())
# Expected: ['docs', 'sessions']
```

**Issue: File watcher not detecting changes**
```powershell
# Check if file watcher process is running
Get-Process python | Where-Object {$_.CommandLine -like "*file_watcher.py*"}

# Restart file watcher
python file_watcher.py
```

---

## 16. Future Enhancements

### 16.1 Short-Term (Next 3 months)

- [ ] Add support for .ipynb (Jupyter notebooks) indexing
- [ ] Implement query expansion (synonyms, related terms)
- [ ] Add vector DB reranking for improved search quality
- [ ] Create VS Code extension for semantic search UI
- [ ] Add telemetry (indexing speed, query latency, cache hit rate)

### 16.2 Long-Term (6+ months)

- [ ] Migrate to production vector DB (Qdrant or Weaviate)
- [ ] Implement hybrid search (BM25 + semantic)
- [ ] Add citation tracking (which docs influenced which decisions)
- [ ] Build knowledge graph on top of semantic memory
- [ ] Implement memory pruning (archive old, low-value memories)

---

## 17. Appendix

### 17.1 File Checklist

**Memory Management Project Files**:
- [x] .vscode/settings.json (Peacock purple configuration)
- [x] projectplan.md (this document)
- [ ] requirements.txt (Python dependencies)
- [ ] qmd_parser.py
- [ ] semantic_memory.py
- [ ] daily_indexer.py
- [ ] three_tier_manager.py
- [ ] file_watcher.py
- [ ] install_3tier_memory.ps1
- [ ] schedule_daily_indexer.ps1
- [ ] run_file_watcher.py
- [ ] manual_index.py
- [ ] README.md

**OpenClaw Configuration Files**:
- [ ] ~/.openclaw/projects.json
- [ ] ~/.openclaw/agents/main/memory/global/global_facts.json
- [ ] ~/.openclaw/agents/main/memory/domains/trading/domain_facts.json
- [ ] ~/.openclaw/agents/main/memory/domains/data_science/domain_facts.json

**Project Documentation Folders**:
- [ ] trading/docs/
- [ ] trading/sessions/
- [ ] trading/notes/
- [ ] data_visualization/docs/
- [ ] data_visualization/sessions/
- [ ] data_visualization/notes/
- [ ] x_monetization/docs/
- [ ] x_monetization/sessions/
- [ ] x_monetization/notes/

### 17.2 References

- **OpenClaw Documentation**: https://github.com/openclaw/openclaw
- **ChromaDB Documentation**: https://docs.trychroma.com/
- **Sentence Transformers**: https://www.sbert.net/
- **Quarto Documentation**: https://quarto.org/docs/
- **Watchdog Documentation**: https://python-watchdog.readthedocs.io/

---

**Document Status**: Complete  
**Last Updated**: March 5, 2026  
**Next Review**: After Phase 1 completion
