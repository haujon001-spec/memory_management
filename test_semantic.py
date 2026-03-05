# -*- coding: utf-8 -*-
"""
Test script for indexing workflow
"""

from pathlib import Path
from semantic_memory import SemanticMemoryIndexer
import sys

try:
    print("=" * 80)
    print("TESTING SEMANTIC INDEXING")
    print("=" * 80)
    
    print("\n[1/3] Initializing SemanticMemoryIndexer for 'trading' project...")
    indexer = SemanticMemoryIndexer(
        project_id='trading',
        workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
    )
    print("[OK] Indexer initialized")
    
    print("\n[2/3] Testing search functionality...")
    results = indexer.search("HSMM", n_results=3)
    print(f"[OK] Search completed: {len(results)} results")
    
    print("\n[3/3] Checking ChromaDB collections...")
    print(f"[OK] Docs collection: {indexer.docs_collection}")
    print(f"[OK] Sessions collection: {indexer.sessions_collection}")
    
    print("\n" + "=" * 80)
    print("ALL TESTS PASSED")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
