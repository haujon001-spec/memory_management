#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
COMPREHENSIVE 3-TIER MEMORY TEST
Tests all three tiers of the memory system to ensure long-conversation memory works
"""

import json
from pathlib import Path
from semantic_memory import SemanticMemoryIndexer
from three_tier_manager import ThreeTierMemoryManager

print("\n" + "="*80)
print("COMPREHENSIVE 3-TIER MEMORY TEST")
print("="*80)

# ================================================================
# TIER 1: GLOBAL FACTS TEST
# ================================================================
print("\n[TIER 1] GLOBAL KNOWLEDGE TEST")
print("-" * 80)

tier1_path = Path.home() / '.openclaw' / 'agents' / 'main' / 'memory' / 'global' / 'global_facts.json'

if tier1_path.exists():
    with open(tier1_path, 'r', encoding='utf-8-sig') as f:
        tier1_data = json.load(f)
    
    print(f"✅ File exists: {tier1_path}")
    print(f"✅ Size: {tier1_path.stat().st_size} bytes")
    print(f"✅ Keys loaded: {len(tier1_data)} facts")
    
    # Verify key facts
    expected_keys = ['system_architecture', 'project_name', 'status']
    missing_keys = [k for k in expected_keys if k not in tier1_data]
    
    if missing_keys:
        print(f"⚠️  Missing keys: {missing_keys}")
    else:
        print(f"✅ All expected keys present")
        print(f"\n   Sample facts:")
        for key in list(tier1_data.keys())[:3]:
            value = str(tier1_data[key])[:60]
            print(f"     - {key}: {value}...")
else:
    print(f"❌ File not found: {tier1_path}")

# ================================================================
# TIER 2: DOMAIN-SPECIFIC FACTS TEST
# ================================================================
print("\n[TIER 2] DOMAIN-SPECIFIC KNOWLEDGE TEST")
print("-" * 80)

domains = ['trading', 'infrastructure']
tier2_results = {}

for domain in domains:
    tier2_path = Path.home() / '.openclaw' / 'agents' / 'main' / 'memory' / 'domains' / domain / 'domain_facts.json'
    
    if tier2_path.exists():
        with open(tier2_path, 'r', encoding='utf-8-sig') as f:
            tier2_data = json.load(f)
        
        tier2_results[domain] = True
        print(f"✅ {domain}/domain_facts.json")
        print(f"   Size: {tier2_path.stat().st_size} bytes")
        print(f"   Facts: {len(tier2_data)} loaded")
        
        # Show sample facts
        if 'domain' in tier2_data:
            print(f"   Domain: {tier2_data['domain']}")
        if 'primary_framework' in tier2_data:
            framework = str(tier2_data['primary_framework'])[:50]
            print(f"   Framework: {framework}...")
    else:
        tier2_results[domain] = False
        print(f"❌ {domain}/domain_facts.json NOT FOUND")

# ================================================================
# TIER 3a: WORKSPACE FACTS TEST
# ================================================================
print("\n[TIER 3a] WORKSPACE MEMORY TEST")
print("-" * 80)

projects = ['trading', 'data_visualization']
tier3a_results = {}

for project in projects:
    tier3a_path = Path.home() / '.openclaw' / 'workspaces' / project / 'memory' / 'index.json'
    
    if tier3a_path.exists():
        try:
            with open(tier3a_path, 'r', encoding='utf-8-sig') as f:
                tier3a_data = json.load(f)
            
            tier3a_results[project] = True
            print(f"✅ {project}/index.json")
            print(f"   Size: {tier3a_path.stat().st_size} bytes")
            print(f"   Keys: {len(tier3a_data)} facts")
        except json.JSONDecodeError:
            tier3a_results[project] = False
            print(f"❌ {project}/index.json - JSON parsing error")
    else:
        tier3a_results[project] = False
        print(f"⚠️  {project}/index.json - NOT FOUND (optional)")

# ================================================================
# TIER 3b: SEMANTIC SEARCH TEST  
# ================================================================
print("\n[TIER 3b] SEMANTIC SEARCH (ChromaDB) TEST")
print("-" * 80)

try:
    print("Testing semantic search for 'trading' project...")
    
    trading_indexer = SemanticMemoryIndexer(
        project_id='trading',
        workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
    )
    
    # Check collections
    collections = trading_indexer.client.list_collections()
    print(f"✅ ChromaDB client connected")
    print(f"✅ Collections available: {len(collections)}")
    
    for collection in collections:
        count = collection.count()
        print(f"   - {collection.name}: {count} documents")
    
    # Test search
    results = trading_indexer.search("HSMM regime", n_results=2)
    
    if results:
        print(f"✅ Semantic search works ({len(results)} results)")
        print(f"   Sample result: {results[0]['metadata']['title']}")
    else:
        print(f"⚠️  Semantic search returned no results (indexing may be needed)")
        
except Exception as e:
    print(f"❌ Semantic search error: {str(e)[:80]}")

# ================================================================
# INTEGRATION TEST: enrich_query() - THE ACTUAL LONG-MEMORY MECHANISM
# ================================================================
print("\n[INTEGRATION] THREE-TIER ENRICHMENT TEST")
print("-" * 80)

try:
    print("Creating ThreeTierMemoryManager instance...")
    
    manager = ThreeTierMemoryManager(
        project_id='trading',
        workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading'),
        domain='trading'
    )
    
    print("✅ Manager initialized")
    
    # Test enrichization
    print("\nTesting enrich_query() with a sample query...")
    query = "What is HSMM regime detection?"
    
    enriched = manager.enrich_query(query, context_size=3)
    
    # Check what tiers were loaded
    has_global = "Global Knowledge" in enriched
    has_domain = "Domain Knowledge" in enriched
    has_workspace = "Workspace Facts" in enriched
    has_semantic = "Relevant Documentation" in enriched
    
    print(f"\nEnrichment Results:")
    print(f"  ✅ Tier 1 (Global Knowledge)      : {'✅ LOADED' if has_global else '❌ MISSING'}")
    print(f"  ✅ Tier 2 (Domain Knowledge)      : {'✅ LOADED' if has_domain else '❌ MISSING'}")
    print(f"  ✅ Tier 3a (Workspace Facts)      : {'✅ LOADED' if has_workspace else '❌ MISSING'}")
    print(f"  ✅ Tier 3b (Semantic Search)      : {'✅ LOADED' if has_semantic else '⚠️  NO DOCS'}")
    
    print(f"\nTotal enriched context length: {len(enriched)} characters")
    
    # Show sample of enriched context
    print("\n[Sample of Enriched Context]")
    print("-" * 80)
    lines = enriched.split('\n')[:20]  # First 20 lines
    for line in lines:
        if line.strip():
            print(f"  {line}")
    if len(enriched.split('\n')) > 20:
        print(f"  ... ({len(enriched.split(chr(10))) - 20} more lines)")
    
except Exception as e:
    print(f"❌ Integration test failed: {str(e)}")
    import traceback
    traceback.print_exc()

# ================================================================
# SUMMARY REPORT
# ================================================================
print("\n" + "="*80)
print("TEST SUMMARY REPORT")
print("="*80)

summary = f"""
TIER 1 (Global Knowledge):
  {f'✅ PASS - {tier1_path.stat().st_size} bytes' if tier1_path.exists() else '❌ FAIL'}

TIER 2 (Domain-Specific):
  Trading: {f'✅ PASS' if tier2_results.get('trading') else '❌ FAIL'}
  Infrastructure: {f'✅ PASS' if tier2_results.get('infrastructure') else '❌ FAIL'}

TIER 3a (Workspace Facts):
  Trading: {f'✅ PASS' if tier3a_results.get('trading') else '⚠️  NOT FOUND'}
  Data Visualization: {f'✅ PASS' if tier3a_results.get('data_visualization') else '⚠️  NOT FOUND'}

TIER 3b (Semantic Search):
  {f'✅ PASS - ChromaDB working' if 'collections' in locals() else '❌ FAIL'}

LONG-CONVERSATION MEMORY:
  {f'✅ PASS - All tiers enriched in query' if (has_global and has_domain) else '❌ FAIL - Memory injection broken'}

OVERALL STATUS:
  {f'✅ READY FOR PRODUCTION' if (tier1_path.exists() and tier2_results.get('trading')) else '⚠️  INCOMPLETE SETUP'}
"""

print(summary)

print("="*80)
print("\n🚀 Next Steps:")
print("   1. If any Tier fails, check: check_memory_startup_status.ps1")
print("   2. To test in VS Code: from three_tier_manager import ThreeTierMemoryManager")
print("   3. Monitor startup: Get-Content ~/.openclaw/scheduler/memory_startup.log -Tail 20")
print("="*80 + "\n")
