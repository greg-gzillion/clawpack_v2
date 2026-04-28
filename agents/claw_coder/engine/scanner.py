"""Codebase scanner - reads project structure and extracts patterns"""
from pathlib import Path
from typing import Dict, List, Optional

class ProjectScanner:
    def __init__(self, root: Path):
        self.root = Path(root)
    
    def scan_structure(self, max_depth: int = 3) -> str:
        """Generate a tree overview of the project."""
        lines = []
        lines.append(f"Project: {self.root.name}")
        lines.append("=" * 50)
        
        def walk(path, depth=0, prefix=""):
            if depth > max_depth:
                return
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
            for i, item in enumerate(items):
                if item.name.startswith('.') or item.name == '__pycache__':
                    continue
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                if item.is_dir():
                    lines.append(f"{prefix}{connector}{item.name}/")
                    walk(item, depth + 1, prefix + ("    " if is_last else "│   "))
                else:
                    size = item.stat().st_size
                    lines.append(f"{prefix}{connector}{item.name} ({size:,} bytes)")
        
        walk(self.root)
        return "\n".join(lines)
    
    def extract_patterns(self, lang: str = "python") -> str:
        """Extract coding patterns from the project (imports, naming, structure)."""
        ext_map = {
            "python": ".py", "rust": ".rs", "go": ".go",
            "javascript": ".js", "typescript": ".ts", "java": ".java"
        }
        ext = ext_map.get(lang, ".py")
        
        patterns = []
        imports = set()
        classes = []
        
        for file_path in self.root.rglob(f"*{ext}"):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                lines = content.split("\n")
                
                # Extract imports
                for line in lines[:20]:
                    if line.strip().startswith("import ") or line.strip().startswith("from "):
                        imports.add(line.strip())
                
                # Extract class names
                for line in lines:
                    if line.strip().startswith("class "):
                        name = line.strip().split("class ")[1].split("(")[0].split(":")[0]
                        classes.append(name)
                
                # Detect patterns
                if "def __init__" in content:
                    patterns.append(f"  Uses: Constructor injection in {file_path.name}")
                if "raise " in content:
                    patterns.append(f"  Uses: Custom exceptions in {file_path.name}")
                if "async def" in content:
                    patterns.append(f"  Uses: Async/await in {file_path.name}")
                if "@dataclass" in content:
                    patterns.append(f"  Uses: Dataclasses in {file_path.name}")
                
            except:
                pass
        
        result = []
        result.append(f"Language: {lang}")
        result.append(f"Files scanned: {len(list(self.root.rglob(f'*{ext}')))}")
        
        if imports:
            result.append(f"\nImports ({len(imports)} unique):")
            for imp in sorted(imports)[:15]:
                result.append(f"  {imp}")
        
        if classes:
            result.append(f"\nClasses ({len(classes)}):")
            for cls in sorted(set(classes))[:20]:
                result.append(f"  {cls}")
        
        if patterns:
            result.append("\nDetected Patterns:")
            for p in set(patterns):
                result.append(p)
        
        return "\n".join(result)
    
    def full_context(self, query: str, lang: str = "python") -> str:
        """Get full project context for code generation."""
        parts = []
        
        # Project structure
        parts.append(self.scan_structure(max_depth=2))
        
        # Patterns
        parts.append("\n" + self.extract_patterns(lang))
        
        # Relevant files
        ext = {"python": ".py", "rust": ".rs", "go": ".go", 
               "javascript": ".js", "typescript": ".ts"}.get(lang, ".py")
        
        relevant_files = []
        for file_path in self.root.rglob(f"*{ext}"):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if query.lower() in content.lower() or any(
                    word in file_path.name.lower() for word in query.lower().split()
                ):
                    relevant_files.append((file_path, content[:1000]))
                    if len(relevant_files) >= 3:
                        break
            except:
                pass
        
        if relevant_files:
            parts.append("\nRelevant Files:")
            for fp, content in relevant_files:
                parts.append(f"\n### {fp.relative_to(self.root)}")
                parts.append(f"```{lang}\n{content}\n```")
        
        return "\n".join(parts)