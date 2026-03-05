# -*- coding: utf-8 -*-
"""
DailyIndexer - Scheduled background indexer for all projects

Part of the OpenClaw 3-Tier Memory Management System
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
            with open(self.last_run_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'timestamp': None, 'indexed_files': {}}
    
    def _save_last_run(self):
        """Save last run metadata."""
        self.last_run['timestamp'] = datetime.now().isoformat()
        with open(self.last_run_file, 'w', encoding='utf-8') as f:
            json.dump(self.last_run, f, indent=2)
    
    def _load_projects_config(self) -> List[Dict]:
        """Load projects configuration."""
        config_path = Path.home() / '.openclaw' / 'projects.json'
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                return data.get('projects', [])
        
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
            print(f"  [WARNING] Workspace not found: {workspace_root}")
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
                print(f"  [ERROR] Failed to index {filepath.name}: {e}")
        
        self.logger.info(f"Indexed {indexed_count} files for {project['id']}")
        print(f"  [OK] Indexed {indexed_count} files")
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
