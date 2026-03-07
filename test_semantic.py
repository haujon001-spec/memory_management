# -*- coding: utf-8 -*-
"""
Test script for semantic indexing across all projects
"""

import json
from pathlib import Path
from semantic_memory import SemanticMemoryIndexer
import sys


def test_project(project_config):
    """Test semantic indexing for a single project."""
    project_id = project_config['id']
    workspace_root = Path(project_config['workspace_root'])
    
    print(f"\n[Testing] {project_id.upper()}")
    print(f"  Path: {workspace_root}")
    
    # Check if workspace exists
    if not workspace_root.exists():
        print(f"  [SKIP] Workspace not found")
        return False
    
    try:
        # Initialize indexer
        indexer = SemanticMemoryIndexer(
            project_id=project_id,
            workspace_root=workspace_root
        )
        print(f"  [OK] Indexer initialized")
        
        # Check collections
        if indexer.docs_collection:
            print(f"  [OK] Docs collection exists")
        else:
            print(f"  [WARN] Docs collection not ready")
        
        # Try a search if docs exist
        try:
            results = indexer.search("documentation", n_results=1)
            print(f"  [OK] Search works ({len(results)} results found)")
        except Exception as e:
            print(f"  [WARN] Search failed: {str(e)[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"  [ERROR] {str(e)[:80]}")
        return False


try:
    print("=" * 80)
    print("SEMANTIC INDEXING TEST - ALL PROJECTS")
    print("=" * 80)
    
    # Load project configuration
    config_path = Path.home() / '.openclaw' / 'projects.json'
    
    if not config_path.exists():
        print(f"\n[ERROR] Configuration not found: {config_path}")
        print("[INFO] Run: python install_3tier_memory.ps1")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        projects = data.get('projects', [])
    
    print(f"\n[Info] Found {len(projects)} projects")
    
    # Test each project
    passed = 0
    failed = 0
    skipped = 0
    
    for project in projects:
        result = test_project(project)
        if result is None:
            skipped += 1
        elif result:
            passed += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Passed:  {passed}")
    print(f"Failed:  {failed}")
    print(f"Skipped: {skipped}")
    print(f"Total:   {len(projects)}")
    print("=" * 80)
    
    if failed > 0:
        sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
