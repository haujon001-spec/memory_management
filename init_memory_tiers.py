#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialize Tier 1 and Tier 2 memory with proper JSON structure
"""

import json
from pathlib import Path

print("\n" + "="*80)
print("INITIALIZING TIER 1 & TIER 2 MEMORY")
print("="*80)

# ================================================================
# TIER 1: GLOBAL FACTS
# ================================================================
print("\n[Tier 1] Global Facts")

tier1_dir = Path.home() / '.openclaw' / 'agents' / 'main' / 'memory' / 'global'
tier1_dir.mkdir(parents=True, exist_ok=True)
tier1_file = tier1_dir / 'global_facts.json'

tier1_facts = {
    "system_architecture": "3-tier memory management system for multi-project workspace",
    "project_name": "OpenClaw 3-Tier Memory Management System",
    "peacock_color": "Purple (#9b59b6)",
    "created_date": "March 5, 2026",
    "status": "Implementation Complete",
    "supported_projects": ["trading", "data_visualization", "x_monetization"],
    "embedding_model": "all-MiniLM-L6-v2",
    "vector_database": "ChromaDB",
    "scheduled_indexing": "Windows Task Scheduler - Daily at 2:00 AM",
    "python_version": "3.10+",
    "platform": "Windows 10/11",
    "memory_base_path": "~/.openclaw/",
    "tier1_purpose": "Universal knowledge shared across all projects",
    "tier2_purpose": "Domain-specific knowledge for trading, data_science, infrastructure",
    "tier3a_purpose": "Project-specific facts stored as JSON",
    "tier3b_purpose": "Semantic search via ChromaDB for documentation"
}

with open(tier1_file, 'w', encoding='utf-8') as f:
    json.dump(tier1_facts, f, indent=2, ensure_ascii=False)

print(f"✅ Created: {tier1_file}")
print(f"   Size: {tier1_file.stat().st_size} bytes")
print(f"   Facts: {len(tier1_facts)}")

# ================================================================
# TIER 2: TRADING DOMAIN FACTS
# ================================================================
print("\n[Tier 2] Trading Domain Facts")

tier2_trading_dir = Path.home() / '.openclaw' / 'agents' / 'main' / 'memory' / 'domains' / 'trading'
tier2_trading_dir.mkdir(parents=True, exist_ok=True)
tier2_trading_file = tier2_trading_dir / 'domain_facts.json'

tier2_trading_facts = {
    "domain": "trading",
    "projects": ["trading", "x_monetization"],
    "peacock_colors": {
        "trading": "#0B5FFF",
        "x_monetization": "TBD"
    },
    "primary_framework": "HSMM regime detection and market analysis",
    "key_concepts": [
        "HSMM = Hidden Semi-Markov Model for regime detection",
        "Regime-based trading strategies",
        "Market analysis and profiling",
        "Exit signal generation (B-Trail integration)",
        "Seasonal patterns and consolidation detection"
    ],
    "phase_status": "Phase 13 in progress",
    "latest_implementation": "PHASE12_EXIT_B_RTRAIL_INTEGRATION",
    "core_modules": [
        "HSMM regime profiler",
        "Exit signal generator",
        "Backtest framework"
    ],
    "python_interpreter": ".venv\\Scripts\\python.exe",
    "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\trading"
}

with open(tier2_trading_file, 'w', encoding='utf-8') as f:
    json.dump(tier2_trading_facts, f, indent=2, ensure_ascii=False)

print(f"✅ Created: {tier2_trading_file}")
print(f"   Size: {tier2_trading_file.stat().st_size} bytes")
print(f"   Facts: {len(tier2_trading_facts)}")

# ================================================================
# TIER 2: INFRASTRUCTURE DOMAIN FACTS
# ================================================================
print("\n[Tier 2] Infrastructure Domain Facts")

tier2_infra_dir = Path.home() / '.openclaw' / 'agents' / 'main' / 'memory' / 'domains' / 'infrastructure'
tier2_infra_dir.mkdir(parents=True, exist_ok=True)
tier2_infra_file = tier2_infra_dir / 'domain_facts.json'

tier2_infra_facts = {
    "domain": "infrastructure",
    "projects": ["memory_management"],
    "peacock_color": "#9b59b6",
    "purpose": "3-Tier memory management system for OpenClaw gateway integration",
    "core_modules": [
        "qmd_parser.py - Parse Quarto Markdown files",
        "semantic_memory.py - ChromaDB vector indexing",
        "daily_indexer.py - Scheduled background indexer",
        "three_tier_manager.py - Unified memory interface",
        "file_watcher.py - Real-time file monitoring"
    ],
    "memory_tiers": {
        "Tier1": "Global knowledge (universal concepts)",
        "Tier2": "Domain-specific knowledge (trading, data_science, infrastructure)",
        "Tier3a": "Workspace memory (JSON index.json)",
        "Tier3b": "Semantic search (ChromaDB vectors)"
    },
    "indexing_schedule": "Windows Task Scheduler - Daily at 2:00 AM",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "dependencies": ["chromadb", "sentence-transformers", "watchdog", "quarto-cli"],
    "status": "Production ready"
}

with open(tier2_infra_file, 'w', encoding='utf-8') as f:
    json.dump(tier2_infra_facts, f, indent=2, ensure_ascii=False)

print(f"✅ Created: {tier2_infra_file}")
print(f"   Size: {tier2_infra_file.stat().st_size} bytes")
print(f"   Facts: {len(tier2_infra_facts)}")

# ================================================================
# DATA SCIENCE DOMAIN (OPTIONAL)
# ================================================================
print("\n[Tier 2] Data Science Domain Facts (Optional)")

tier2_ds_dir = Path.home() / '.openclaw' / 'agents' / 'main' / 'memory' / 'domains' / 'data_science'
tier2_ds_dir.mkdir(parents=True, exist_ok=True)
tier2_ds_file = tier2_ds_dir / 'domain_facts.json'

tier2_ds_facts = {
    "domain": "data_science",
    "projects": ["data_visualization"],
    "peacock_color": "#0BBF5F",
    "purpose": "Data visualization and analytics frameworks",
    "primary_frameworks": [
        "Market capitalization visualization",
        "Data analysis and profiling",
        "Real-time data dashboards"
    ],
    "core_technologies": ["Python", "Pandas", "Matplotlib", "Plotly"],
    "workspace_root": "C:\\Users\\haujo\\projects\\DEV\\Data_visualization"
}

with open(tier2_ds_file, 'w', encoding='utf-8') as f:
    json.dump(tier2_ds_facts, f, indent=2, ensure_ascii=False)

print(f"✅ Created: {tier2_ds_file}")
print(f"   Size: {tier2_ds_file.stat().st_size} bytes")

# ================================================================
# VERIFICATION
# ================================================================
print("\n" + "="*80)
print("VERIFICATION")
print("="*80)

files_created = [
    (tier1_file, "Tier 1"),
    (tier2_trading_file, "Tier 2 (Trading)"),
    (tier2_infra_file, "Tier 2 (Infrastructure)"),
    (tier2_ds_file, "Tier 2 (Data Science)")
]

total_size = 0
for file_path, tier_name in files_created:
    size = file_path.stat().st_size
    total_size += size
    status = "✅" if size > 0 else "❌"
    print(f"{status} {tier_name:30} {size:6} bytes - {file_path.name}")

print(f"\nTotal memory initialized: {total_size} bytes")
print(f"\n✅ TIER 1 & TIER 2 MEMORY INITIALIZATION COMPLETE")
print("="*80 + "\n")
