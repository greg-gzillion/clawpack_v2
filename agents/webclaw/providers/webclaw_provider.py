"""Webclaw Provider - Fast bitmap search for references"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from shared.search import BitmapIndex, FuzzyScorer, SearchResult

class WebclawProvider:
    """Fast search across 300+ reference files using bitmap pre-filters"""
    
    def __init__(self):
        self.references_path = Path("C:/Users/greg/dev/clawpack_v2/agents/webclaw/references")
        self.index = BitmapIndex("webclaw_references")
        self._indexed = False
    
    def build_index(self) -> None:
        """Build bitmap index of all reference files"""
        if self._indexed:
            return
        
        print("   📚 Building reference index...")
        
        if self.references_path.exists():
            items = []
            for md_file in self.references_path.rglob("*.md"):
                # Extract category from path
                parts = md_file.parts
                category = parts[-2] if len(parts) > 1 else "general"
                display_name = md_file.stem.replace('_', ' ').replace('-', ' ')
                
                items.append((str(md_file), display_name, category))
            
            self.index.add_batch(items)
            self.index.build()
            self._indexed = True
            
            stats = self.index.get_stats()
            print(f"   ✅ Indexed {stats['total_items']} files in {stats['build_time_ms']:.2f}ms")
        else:
            print(f"   ⚠️ References path not found: {self.references_path}")
    
    def search(self, query: str, max_results: int = 20) -> List[SearchResult]:
        """
        Fast search using bitmap pre-filter.
        Only scores candidates that pass the pre-filter.
        """
        self.build_index()
        
        if not query:
            return []
        
        # Get pre-filtered candidates
        items = self.index.search(query, max_results)
        
        # Convert to SearchResult
        results = []
        for item in items:
            results.append(SearchResult(
                path=item.path,
                display_name=item.display_name,
                score=0,  # Score already applied in index.search
                category=item.category
            ))
        
        return results
    
    def search_with_highlight(self, query: str) -> List[Dict]:
        """Search with match highlighting"""
        results = self.search(query)
        
        scorer = FuzzyScorer(query)
        output = []
        
        for r in results:
            output.append({
                "path": r.path,
                "display_name": r.display_name,
                "highlighted": scorer.highlight_matches(r.display_name),
                "category": r.category,
                "score": r.score
            })
        
        return output
    
    def get_reference_content(self, path: str, max_chars: int = 2000) -> Optional[str]:
        """Get content of a reference file"""
        try:
            filepath = Path(path)
            if filepath.exists():
                content = filepath.read_text(encoding='utf-8')
                return content[:max_chars]
        except Exception as e:
            print(f"   ⚠️ Error reading {path}: {e}")
        
        return None
    
    def get_stats(self) -> dict:
        """Get search index statistics"""
        if not self._indexed:
            self.build_index()
        return self.index.get_stats()
