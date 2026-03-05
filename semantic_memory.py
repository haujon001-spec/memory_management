# -*- coding: utf-8 -*-
"""
SemanticMemoryIndexer - Tier 3 semantic indexing using ChromaDB

Part of the OpenClaw 3-Tier Memory Management System
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
        print(f"    [Semantic] Loading embedding model for {project_id}...")
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
            with open(self.index_meta_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'files': {}}
    
    def _save_index_meta(self):
        """Save indexing metadata."""
        with open(self.index_meta_path, 'w', encoding='utf-8') as f:
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
            if chunk.strip():  # Only add non-empty chunks
                chunks.append(chunk)
            start = end - overlap
        
        return chunks if chunks else [text]  # Return original if no chunks created
    
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
        
        if not chunks:
            print(f"    [WARNING] No content to index in {filepath.name}")
            return
        
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
        
        if not chunks:
            print(f"    [WARNING] No content to index in {filepath.name}")
            return
        
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
        if results['documents'] and len(results['documents']) > 0:
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


if __name__ == '__main__':
    # Test indexer
    print("\n" + "=" * 80)
    print("SEMANTIC MEMORY INDEXER - TEST")
    print("=" * 80)
    
    indexer = SemanticMemoryIndexer(
        project_id='trading',
        workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
    )
    
    # Index all docs
    count = indexer.index_all_docs()
    print(f"\nIndexed {count} files")
    
    # Test search
    print("\n" + "-" * 80)
    print("Testing semantic search...")
    results = indexer.search('HSMM regime detection', n_results=3)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['metadata']['title']}")
        print(f"   File: {result['metadata']['filepath']}")
        print(f"   Distance: {result['distance']:.4f}")
        print(f"   Snippet: {result['document'][:200]}...")
