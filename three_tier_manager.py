# -*- coding: utf-8 -*-
"""
ThreeTierMemoryManager - Unified interface for 3-tier memory system

Part of the OpenClaw 3-Tier Memory Management System
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
        
        # Create directories if they don't exist
        self.global_memory_path.mkdir(parents=True, exist_ok=True)
        self.domain_memory_path.mkdir(parents=True, exist_ok=True)
        self.workspace_memory_path.mkdir(parents=True, exist_ok=True)
    
    def _load_json_memory(self, memory_path: Path, filename: str) -> Dict:
        """Load JSON memory file."""
        filepath = memory_path / filename
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
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
        try:
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
        except Exception as e:
            context_parts.append(f"## Semantic Search Error\n{str(e)}\n\n")
        
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


if __name__ == '__main__':
    # Test 3-tier memory manager
    print("\n" + "=" * 80)
    print("THREE-TIER MEMORY MANAGER - TEST")
    print("=" * 80)
    
    manager = ThreeTierMemoryManager(
        project_id='trading',
        workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading'),
        domain='trading'
    )
    
    # Test enriched query
    print("\nTesting enriched query...")
    query = "How does HSMM regime detection work?"
    enriched_context = manager.enrich_query(query, context_size=3)
    
    print(f"\nQuery: {query}")
    print("\nEnriched Context:")
    print("-" * 80)
    print(enriched_context)
