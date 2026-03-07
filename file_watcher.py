# -*- coding: utf-8 -*-
"""
FileWatcher - Real-time file system monitoring for immediate indexing

Part of the OpenClaw 3-Tier Memory Management System
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
            print(f"  [FileWatcher] Modified: {filepath.name}, re-indexing...")
            
            try:
                if filepath.suffix == '.qmd':
                    self.indexer.index_qmd_file(filepath, collection_name=collection)
                else:
                    self.indexer.index_markdown_file(filepath, collection_name=collection)
                
                self.logger.info(f"Successfully indexed: {filepath.name}")
                print(f"  [OK] Indexed: {filepath.name}")
            except Exception as e:
                self.logger.error(f"Failed to index {filepath.name}: {e}")
                print(f"  [ERROR] Failed to index {filepath.name}: {e}")
    
    def on_created(self, event):
        """Handle file creation."""
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        if self._should_index(filepath):
            collection = self._determine_collection(filepath)
            
            self.logger.info(f"New file detected: {filepath.name}, indexing...")
            print(f"  [FileWatcher] New file: {filepath.name}, indexing...")
            
            try:
                if filepath.suffix == '.qmd':
                    self.indexer.index_qmd_file(filepath, collection_name=collection)
                else:
                    self.indexer.index_markdown_file(filepath, collection_name=collection)
                
                self.logger.info(f"Successfully indexed: {filepath.name}")
                print(f"  [OK] Indexed: {filepath.name}")
            except Exception as e:
                self.logger.error(f"Failed to index {filepath.name}: {e}")
                print(f"  [ERROR] Failed to index {filepath.name}: {e}")


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
    watched_dirs = []
    for directory in ['docs', 'sessions', 'notes']:
        watch_path = workspace_root / directory
        if watch_path.exists():
            observer.schedule(event_handler, str(watch_path), recursive=True)
            watched_dirs.append(str(watch_path))
            logger.info(f"Watching: {watch_path}")
            print(f"  [FileWatcher] Watching: {watch_path}")
    
    if not watched_dirs:
        print(f"  [WARNING] No directories to watch in {workspace_root}")
        return
    
    observer.start()
    logger.info(f"File watcher started for project: {project_id}")
    print(f"\n[FileWatcher] Active for {project_id}")
    print("  Press Ctrl+C to stop...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("File watcher stopped")
        print("\n[FileWatcher] Stopped")
    
    observer.join()


if __name__ == '__main__':
    import sys
    import json
    
    # Parse command-line arguments
    project_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("\n" + "=" * 80)
    print("FILE WATCHER - REAL-TIME INDEXING")
    print("=" * 80)
    
    if project_id:
        # Load project from config
        config_path = Path.home() / '.openclaw' / 'projects.json'
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                projects = {p['id']: p for p in data.get('projects', [])}
                
                if project_id in projects:
                    project = projects[project_id]
                    print(f"\n[FileWatcher] Starting for project: {project_id}")
                    print(f"[FileWatcher] Watching: {project['workspace_root']}\n")
                    
                    start_file_watcher(
                        project_id=project_id,
                        workspace_root=Path(project['workspace_root'])
                    )
                else:
                    print(f"[ERROR] Project '{project_id}' not found in configuration")
                    print(f"[INFO] Available projects: {', '.join(projects.keys())}")
        else:
            print(f"[ERROR] Configuration not found: {config_path}")
    else:
        # Default: watch trading project
        print("\n[FileWatcher] Usage: python file_watcher.py <project_id>")
        print("[FileWatcher] Example: python file_watcher.py trading")
        print("[FileWatcher] Example: python file_watcher.py data_visualization")
        print("\n[FileWatcher] Starting default watcher for 'trading' project...\n")
        
        start_file_watcher(
            project_id='trading',
            workspace_root=Path(r'C:\Users\haujo\projects\DEV\trading')
        )
