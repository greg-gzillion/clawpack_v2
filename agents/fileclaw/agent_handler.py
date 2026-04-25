"""A2A Handler for FileClaw - Universal File Import/Export for All Agents"""
import sys
import json
import csv
from pathlib import Path
from datetime import datetime

FILECLAW_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FILECLAW_DIR.parent.parent
EXPORTS = PROJECT_ROOT / "exports"
sys.path.insert(0, str(PROJECT_ROOT))

from shared.base_agent import BaseAgent

class FileClawAgent(BaseAgent):
    def __init__(self):
        super().__init__('fileclaw')
        self.text_formats = {'.md', '.txt', '.html', '.xml', '.json', '.csv', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.py', '.js', '.ts', '.rs', '.go', '.cpp', '.c', '.java', '.rb', '.php', '.css', '.sql', '.r', '.sh', '.bat', '.ps1'}
        self.binary_importers = {'.pdf': self._read_pdf, '.docx': self._read_docx, '.xlsx': self._read_xlsx, '.pptx': self._read_pptx, '.rtf': self._read_rtf, '.png': self._read_image, '.jpg': self._read_image, '.jpeg': self._read_image, '.gif': self._read_image, '.bmp': self._read_image, '.webp': self._read_image, '.svg': self._read_image, '.zip': self._read_archive, '.tar': self._read_archive, '.gz': self._read_archive, '.mp3': self._read_media, '.mp4': self._read_media, '.wav': self._read_media, '.mkv': self._read_media, '.avi': self._read_media, '.mov': self._read_media, '.mpeg': self._read_media, '.mpg': self._read_media}

    # ══════════════════════════════════════════
    # FORMAT READERS
    # ══════════════════════════════════════════

    def _read_pdf(self, path: Path) -> str:
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            text = f"PDF: {path.name}, {len(reader.pages)} pages\n\n"
            for i, page in enumerate(reader.pages[:5]):  # First 5 pages
                text += f"--- Page {i+1} ---\n{page.extract_text() or '(no text)'}\n"
            return text
        except Exception as e:
            return f"PDF read error: {e}"

    def _read_docx(self, path: Path) -> str:
        try:
            from docx import Document
            doc = Document(str(path))
            text = f"DOCX: {path.name}\n\n"
            for para in doc.paragraphs[:50]:
                text += para.text + "\n"
            return text
        except Exception as e:
            return f"DOCX read error: {e}"

    def _read_xlsx(self, path: Path) -> str:
        try:
            import pandas as pd
            sheets = pd.read_excel(path, sheet_name=None)
            text = f"XLSX: {path.name}, {len(sheets)} sheets\n\n"
            for name, df in sheets.items():
                text += f"--- Sheet: {name} ---\n{df.head(20).to_string()}\n\n"
            return text
        except Exception as e:
            return f"XLSX read error: {e}"

    def _read_pptx(self, path: Path) -> str:
        try:
            from pptx import Presentation
            prs = Presentation(str(path))
            text = f"PPTX: {path.name}, {len(prs.slides)} slides\n\n"
            for i, slide in enumerate(prs.slides[:10]):
                text += f"--- Slide {i+1} ---\n"
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text:
                        text += shape.text + "\n"
            return text
        except Exception as e:
            return f"PPTX read error: {e}"

    def _read_rtf(self, path: Path) -> str:
        try:
            # RTF is complex - try basic text extraction
            content = path.read_text(encoding='utf-8', errors='replace')
            # Strip RTF tags for basic readability
            import re
            text = re.sub(r'\\[a-z]+\d*', '', content)
            text = re.sub(r'[{}]', '', text)
            return f"RTF: {path.name}\n\n{text[:2000]}"
        except Exception as e:
            return f"RTF read error: {e}"

    def _read_image(self, path: Path) -> str:
        try:
            from PIL import Image
            img = Image.open(path)
            info = f"IMAGE: {path.name}\n  Format: {img.format}\n  Size: {img.size[0]}x{img.size[1]}\n  Mode: {img.mode}\n  File size: {self._format_size(path.stat().st_size)}"
            # Try EXIF
            try:
                exif = img._getexif()
                if exif:
                    info += f"\n  EXIF: {len(exif)} tags"
            except:
                pass
            return info
        except Exception as e:
            return f"Image read error: {e}"

    def _read_archive(self, path: Path) -> str:
        try:
            import zipfile, tarfile
            text = f"ARCHIVE: {path.name}\n  Size: {self._format_size(path.stat().st_size)}\n\nContents:\n"
            if path.suffix == '.zip':
                with zipfile.ZipFile(path) as zf:
                    for info in zf.infolist()[:50]:
                        text += f"  {'📁' if info.is_dir() else '📄'} {info.filename} ({self._format_size(info.file_size)})\n"
            elif path.suffix in ('.tar', '.gz'):
                with tarfile.open(path) as tf:
                    for member in tf.getmembers()[:50]:
                        text += f"  {'📁' if member.isdir() else '📄'} {member.name} ({self._format_size(member.size)})\n"
            return text
        except Exception as e:
            return f"Archive read error: {e}"

    def _read_media(self, path: Path) -> str:
        return f"MEDIA: {path.name}\n  Type: {path.suffix}\n  Size: {self._format_size(path.stat().st_size)}\n  (Media files provide metadata only - use external tools for playback)"

    # ══════════════════════════════════════════
    # IMPORT
    # ══════════════════════════════════════════

    def _import(self, filepath: str) -> str:
        p = Path(filepath)
        if not p.exists():
            return f"Error: File not found: {filepath}"
        
        ext = p.suffix.lower()
        
        # Check binary importers first
        if ext in self.binary_importers:
            return self.binary_importers[ext](p)
        
        # Text formats
        if ext in self.text_formats:
            try:
                content = p.read_text(encoding='utf-8', errors='replace')
                return f"FILE: {p.name}\n  Size: {self._format_size(p.stat().st_size)}\n\n{content[:5000]}"
            except Exception as e:
                return f"Read error: {e}"
        
        # Unknown - try as text
        try:
            return f"UNKNOWN: {p.name}\n  Size: {self._format_size(p.stat().st_size)}\n\n{p.read_text(encoding='utf-8', errors='replace')[:2000]}"
        except:
            return f"UNKNOWN BINARY: {p.name}\n  Type: {ext}\n  Size: {self._format_size(p.stat().st_size)}"

    # ══════════════════════════════════════════
    # EXPORT
    # ══════════════════════════════════════════

    def _export(self, fmt: str, content: str, name: str = "") -> str:
        EXPORTS.mkdir(exist_ok=True)
        fmt = fmt.lower().lstrip('.')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name or 'export'}_{timestamp}.{fmt}"
        path = EXPORTS / filename

        try:
            if fmt == 'json':
                try:
                    data = json.loads(content) if isinstance(content, str) else content
                    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
                except:
                    path.write_text(content, encoding='utf-8')
            elif fmt == 'csv':
                try:
                    data = json.loads(content) if isinstance(content, str) else content
                    if isinstance(data, list) and data:
                        with open(path, 'w', newline='') as f:
                            writer = csv.DictWriter(f, fieldnames=data[0].keys())
                            writer.writeheader()
                            writer.writerows(data)
                except:
                    path.write_text(content, encoding='utf-8')
            elif fmt == 'html':
                if not content.strip().startswith('<'):
                    content = f"<html><head><meta charset='utf-8'><title>{name or 'Export'}</title><style>body{{font-family:Arial;max-width:800px;margin:40px auto;padding:20px}}pre{{background:#f5f5f5;padding:15px;border-radius:5px}}</style></head><body><pre>{content}</pre></body></html>"
                path.write_text(content, encoding='utf-8')
            elif fmt == 'md':
                # Convert basic HTML to markdown if needed
                if content.strip().startswith('<'):
                    try:
                        from markdown import markdown
                        content = f"# Export\n\n{content}"
                    except:
                        pass
                path.write_text(content, encoding='utf-8')
            else:
                path.write_text(content, encoding='utf-8')

            return f"Exported: {filename} ({self._format_size(path.stat().st_size)})"
        except Exception as e:
            return f"Export failed: {e}"

    # ══════════════════════════════════════════
    # CONVERT
    # ══════════════════════════════════════════

    def _convert(self, source: str, target_fmt: str) -> str:
        p = Path(source)
        if not p.exists():
            return f"Error: Source not found: {source}"
        content = self._import(source)
        name = p.stem
        return self._export(target_fmt, content, name)

    # ══════════════════════════════════════════
    # A2A HANDLER
    # ══════════════════════════════════════════

    def handle(self, task: str) -> dict:
        self.track_interaction()
        task = task.strip()
        if task.startswith('/'):
            parts = task.split(maxsplit=1)
            cmd = parts[0].lower()
            rest = parts[1] if len(parts) > 1 else ""
        else:
            cmd, rest = "", task

        try:
            if cmd == "/import" and rest:
                result = self._import(rest)
            elif cmd == "/export" and rest:
                fmt_parts = rest.split(maxsplit=1)
                result = self._export(fmt_parts[0], fmt_parts[1]) if len(fmt_parts) == 2 else "Usage: /export <format> <content>"
            elif cmd == "/convert" and rest:
                conv_parts = rest.rsplit(maxsplit=1)
                result = self._convert(conv_parts[0], conv_parts[1]) if len(conv_parts) == 2 else "Usage: /convert <source> <target_format>"
            elif cmd == "/help":
                result = f"""FileClaw - Universal File Handler

  /import <path>   Read: PDF, DOCX, XLSX, PPTX, RTF, images, archives, media, +{len(self.text_formats)} text formats
  /export <fmt> <content>   Save: md, html, txt, json, csv, xml
  /convert <src> <fmt>      Convert between formats

  Supported: PDF·DOCX·XLSX·PPTX·RTF·PNG·JPG·GIF·SVG·ZIP·TAR·MP3·MP4·MPEG·WAV·MKV + {len(self.text_formats)} text types"""
            elif cmd == "/stats":
                total_formats = len(self.text_formats) + len(self.binary_importers)
                result = f"FileClaw | {total_formats} formats | Import: {len(self.binary_importers)} binary + {len(self.text_formats)} text | Interactions: {self.state.get('interactions', 0)}"
            else:
                result = self.smart_ask(f"File management: {task}")
            return {"status": "success", "result": str(result)}
        except Exception as e:
            return {"status": "error", "result": str(e)}

    def _format_size(self, size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}TB"

_agent = FileClawAgent()
def process_task(task: str, agent: str = None):
    return _agent.handle(task)
