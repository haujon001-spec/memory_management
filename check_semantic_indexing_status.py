# -*- coding: utf-8 -*-
"""
Semantic Indexing Status Reporter - Multi-Project Overview

Shows:
- Which files are indexed in each project
- ChromaDB collection stats
- Last indexing timestamp
- Indexed file counts by project
- Missing or un-indexed projects
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import chromadb
from chromadb.config import Settings

def load_projects_config() -> List[Dict]:
    """Load multi-project configuration."""
    config_path = Path.home() / '.openclaw' / 'projects.json'
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                return data.get('projects', [])
        except Exception as e:
            print(f"[ERROR] Failed to load projects config: {e}")
            return []
    
    print(f"[WARN] Projects config not found at: {config_path}")
    return []


def get_semantic_db_status(project_id: str) -> Dict:
    """Get ChromaDB status for a project."""
    db_path = Path.home() / '.openclaw' / 'semantic' / project_id
    result = {
        'project_id': project_id,
        'db_path': str(db_path),
        'exists': False,
        'docs_count': 0,
        'sessions_count': 0,
        'total_count': 0,
        'collections': [],
        'index_meta_path': str(db_path / 'index_meta.json') if db_path.exists() else None
    }
    
    if not db_path.exists():
        return result
    
    result['exists'] = True
    
    try:
        # Connect to ChromaDB
        client = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get collections
        collections = client.list_collections()
        result['collections'] = [c.name for c in collections]
        
        # Count documents in each collection
        for collection in collections:
            col = client.get_collection(name=collection.name)
            count = col.count()
            
            if collection.name == 'docs':
                result['docs_count'] = count
            elif collection.name == 'sessions':
                result['sessions_count'] = count
        
        result['total_count'] = result['docs_count'] + result['sessions_count']
        
        # Load index metadata
        index_meta_path = Path(result['index_meta_path'])
        if index_meta_path.exists():
            with open(index_meta_path, 'r', encoding='utf-8') as f:
                result['index_meta'] = json.load(f)
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def get_indexed_files(project_id: str) -> Dict[str, List[str]]:
    """Get list of indexed files from index_meta.json."""
    db_path = Path.home() / '.openclaw' / 'semantic' / project_id
    index_meta_path = db_path / 'index_meta.json'
    
    result = {
        'docs': [],
        'sessions': [],
        'total': 0
    }
    
    if index_meta_path.exists():
        try:
            with open(index_meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
                files = meta.get('files', {})
                
                for filepath, info in files.items():
                    if 'sessions' in filepath:
                        result['sessions'].append(filepath)
                    else:
                        result['docs'].append(filepath)
                
                result['total'] = len(files)
        except Exception as e:
            result['error'] = str(e)
    
    return result


def get_workspace_memory_status(project_id: str) -> Dict:
    """Get Tier 2 workspace memory status."""
    workspace_memory_path = Path.home() / '.openclaw' / 'workspaces' / project_id / 'memory'
    
    result = {
        'project_id': project_id,
        'memory_path': str(workspace_memory_path),
        'exists': workspace_memory_path.exists(),
        'index_exists': False,
        'index_age_days': None
    }
    
    if workspace_memory_path.exists():
        index_path = workspace_memory_path / 'index.json'
        result['index_exists'] = index_path.exists()
        
        if index_path.exists():
            try:
                stat = index_path.stat()
                age = (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days
                result['index_age_days'] = age
            except:
                pass
    
    return result


def format_size(bytes_val):
    """Format bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f}TB"


def print_project_report(project: Dict):
    """Print detailed report for a single project."""
    print(f"\n{'='*80}")
    print(f"PROJECT: {project['name'].upper()}")
    print(f"{'='*80}")
    print(f"  ID:              {project['id']}")
    print(f"  Workspace:       {project['workspace_root']}")
    print(f"  Domain:          {project['domain']}")
    print(f"  Peacock Color:   {project['peacock']}")
    
    # Check workspace
    workspace_path = Path(project['workspace_root'])
    if workspace_path.exists():
        print(f"  Status:          ✓ ACTIVE")
    else:
        print(f"  Status:          ✗ NOT FOUND")
        return
    
    # Semantic indexing status
    print(f"\n  SEMANTIC INDEXING (Tier 3b):")
    print(f"  {'-'*76}")
    sem_status = get_semantic_db_status(project['id'])
    
    if sem_status['exists']:
        print(f"    Database:      ✓ ACTIVE")
        print(f"    Collections:   {', '.join(sem_status['collections'])}")
        print(f"    Docs Indexed:  {sem_status['docs_count']}")
        print(f"    Sessions:      {sem_status['sessions_count']}")
        print(f"    Total:         {sem_status['total_count']}")
        
        # Show indexed files
        indexed_files = get_indexed_files(project['id'])
        if indexed_files['docs']:
            print(f"\n    Indexed Docs ({len(indexed_files['docs'])} files):")
            for i, filepath in enumerate(indexed_files['docs'][:10], 1):  # Show first 10
                rel_path = filepath.replace(project['workspace_root'].lower(), "").lstrip("\\")
                print(f"      {i}. {rel_path}")
            if len(indexed_files['docs']) > 10:
                print(f"      ... and {len(indexed_files['docs']) - 10} more")
    else:
        print(f"    Database:      ✗ NOT INITIALIZED")
    
    # Workspace memory status
    print(f"\n  WORKSPACE MEMORY (Tier 2):")
    print(f"  {'-'*76}")
    mem_status = get_workspace_memory_status(project['id'])
    
    if mem_status['exists']:
        print(f"    Path:          ✓ ACTIVE")
        if mem_status['index_exists']:
            age = mem_status['index_age_days']
            if age is not None:
                print(f"    Index:         ✓ ACTIVE (updated {age} day(s) ago)")
            else:
                print(f"    Index:         ✓ ACTIVE")
        else:
            print(f"    Index:         ✗ NOT INITIALIZED")
    else:
        print(f"    Path:          ✗ NOT INITIALIZED")


def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("SEMANTIC INDEXING STATUS REPORT - ALL PROJECTS")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load projects
    projects = load_projects_config()
    if not projects:
        print("\n[ERROR] No projects configured!")
        return
    
    print(f"Projects Found: {len(projects)}\n")
    
    # Summary statistics
    total_docs = 0
    total_sessions = 0
    total_indexed = 0
    active_projects = 0
    initialized_dbs = 0
    
    # Detailed reports
    for project in projects:
        print_project_report(project)
        
        sem_status = get_semantic_db_status(project['id'])
        if workspace_path := Path(project['workspace_root']):
            if workspace_path.exists():
                active_projects += 1
        
        if sem_status['exists']:
            initialized_dbs += 1
            total_docs += sem_status['docs_count']
            total_sessions += sem_status['sessions_count']
            indexed_files = get_indexed_files(project['id'])
            total_indexed += indexed_files['total']
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"  Total Projects:              {len(projects)}")
    print(f"  Active Workspaces:           {active_projects}")
    print(f"  Databases Initialized:       {initialized_dbs}")
    print(f"  Total Files Indexed:         {total_indexed}")
    print(f"    ├─ Documentation:          {total_docs}")
    print(f"    └─ Sessions:               {total_sessions}")
    print(f"\n  OpenClaw Base Path:          {Path.home() / '.openclaw'}")
    print(f"  Projects Config:             {Path.home() / '.openclaw' / 'projects.json'}")
    print(f"  Last Updated:                {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
