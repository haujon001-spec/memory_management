#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick indexing test - indexes a single file from each project
"""

from pathlib import Path
from semantic_memory import SemanticMemoryIndexer

print("\n" + "="*80)
print("SEMANTIC INDEXING TEST - Single File Per Project")
print("="*80)

projects = [
    {
        'id': 'trading',
        'workspace': r'C:\Users\haujo\projects\DEV\trading',
        'file': 'docs/hsmm_regime_detection.qmd'
    },
    {
        'id': 'data_visualization',
        'workspace': r'C:\Users\haujo\projects\DEV\Data_visualization',
        'file': 'docs/market_capitalization_vis.qmd'
    },
    {
        'id': 'x_monetization',
        'workspace': r'C:\Users\haujo\projects\DEV\X_Monetization',
        'file': 'docs/twitter_monetization_strategy.qmd'
    }
]

total_indexed = 0

for proj in projects:
    print(f"\n[1/3] Processing project: {proj['id']}")
    
    try:
        indexer = SemanticMemoryIndexer(
            project_id=proj['id'],
            workspace_root=Path(proj['workspace'])
        )
        
        filepath = Path(proj['workspace']) / proj['file']
        
        print(f"     Indexing: {filepath.name}")
        
        if filepath.exists():
            if filepath.suffix == '.qmd':
                indexer.index_qmd_file(filepath, collection_name='docs')
            else:
                indexer.index_markdown_file(filepath, collection_name='docs')
            
            print(f"     [OK] Successfully indexed {filepath.name}")
            total_indexed += 1
        else:
            print(f"     [SKIP] File not found: {filepath}")
            
    except Exception as e:
        print(f"     [ERROR] {str(e)}")

print("\n" + "="*80)
print(f"INDEXING COMPLETE - {total_indexed} files indexed")
print("="*80)

# Test semantic search
print("\n[Testing Semantic Search]")

try:
    trading_indexer = SemanticMemoryIndexer(
        project_id='trading',
        workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
    )
    
    results = trading_indexer.search("HSMM regime detection", n_results=3)
    
    print(f"\nQuery: 'HSMM regime detection'")
    print(f"Results: {len(results)} found\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['metadata']['title']}")
        print(f"   Distance: {result['distance']:.4f}")
        print(f"   Preview: {result['document'][:100]}...")
        print()
        
except Exception as e:
    print(f"[ERROR] Search failed: {str(e)}")

print("="*80)
print("TEST COMPLETE")
print("="*80)
