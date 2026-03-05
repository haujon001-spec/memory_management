# -*- coding: utf-8 -*-
"""
QmdParser - Parse Quarto Markdown (.qmd) files for memory indexing

Part of the OpenClaw 3-Tier Memory Management System
"""

import yaml
import re
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class QmdParser:
    """
    Parse Quarto Markdown files extracting:
    - YAML frontmatter (metadata)
    - Markdown content (main documentation)
    - Code cells (Python/R code blocks)
    - File metadata (path, modified time)
    """
    
    def __init__(self):
        self.code_fence_pattern = re.compile(
            r'```(\w+)\n(.*?)```', 
            re.DOTALL
        )
    
    def parse_qmd(self, filepath: Path) -> Dict:
        """
        Parse a .qmd file and extract all components.
        
        Args:
            filepath: Path to .qmd file
            
        Returns:
            Dict with keys:
                - frontmatter: Dict (parsed YAML)
                - content: str (Markdown body without frontmatter)
                - code_cells: List[Dict] (language, code)
                - filepath: str
                - modified: datetime
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        # Extract YAML frontmatter
        frontmatter = {}
        content = raw_content
        
        if raw_content.startswith('---'):
            parts = raw_content.split('---', 2)
            if len(parts) >= 3:
                yaml_str = parts[1]
                content = parts[2].strip()
                try:
                    frontmatter = yaml.safe_load(yaml_str)
                    if frontmatter is None:
                        frontmatter = {}
                except yaml.YAMLError:
                    frontmatter = {}
        
        # Extract code cells
        code_cells = []
        for match in self.code_fence_pattern.finditer(content):
            language = match.group(1)
            code = match.group(2).strip()
            code_cells.append({
                'language': language,
                'code': code
            })
        
        # File metadata
        stat = filepath.stat()
        modified = datetime.fromtimestamp(stat.st_mtime)
        
        return {
            'frontmatter': frontmatter,
            'content': content,
            'code_cells': code_cells,
            'filepath': str(filepath),
            'modified': modified
        }
    
    def extract_tags(self, parsed: Dict) -> List[str]:
        """Extract tags from frontmatter."""
        frontmatter = parsed.get('frontmatter', {})
        if not isinstance(frontmatter, dict):
            return []
        
        tags = frontmatter.get('tags', [])
        return tags if isinstance(tags, list) else []
    
    def extract_title(self, parsed: Dict) -> str:
        """Extract title from frontmatter or first heading."""
        frontmatter = parsed.get('frontmatter', {})
        if isinstance(frontmatter, dict) and 'title' in frontmatter:
            return str(frontmatter['title'])
        
        # Fallback: first heading in content
        content = parsed.get('content', '')
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1)
        
        return Path(parsed['filepath']).stem


if __name__ == '__main__':
    # Test parser
    parser = QmdParser()
    
    # Test with a sample .qmd file (if exists)
    test_file = Path(r'C:\Users\haujo\projects\DEV\trading\docs\planning\HSMM_PureModelTradingProfiler_V2.md')
    
    if test_file.exists():
        print(f"Testing parser with: {test_file}")
        parsed = parser.parse_qmd(test_file)
        
        print(f"\nTitle: {parser.extract_title(parsed)}")
        print(f"Tags: {parser.extract_tags(parsed)}")
        print(f"Code cells: {len(parsed['code_cells'])}")
        print(f"Modified: {parsed['modified']}")
        print(f"Content length: {len(parsed['content'])} chars")
    else:
        print("Test file not found. Parser ready for use.")
