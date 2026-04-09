"""Core translator classes with auto-fallback"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import time

@dataclass
class TranslationResult:
    """Result of a translation operation"""
    success: bool
    original_text: str
    translated_text: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None
    processing_time: float = 0.0
    error: Optional[str] = None
    chunks_processed: int = 0
    engine_used: str = ""
    
    def summary(self) -> str:
        if self.success:
            return f"✅ Translated {len(self.original_text)} chars in {self.processing_time:.2f}s using {self.engine_used}"
        return f"❌ Failed: {self.error}"

class Translator:
    """Main translator orchestrator with auto-fallback"""
    
    def __init__(self, engine=None, chunk_size: int = 2000):
        self.chunk_size = chunk_size
        self._primary_engine = engine
        self._fallback_engine = None
        self._setup_engines()
    
    def _setup_engines(self):
        from .engines import WebClawEngine, SimpleEngine
        
        # Setup primary engine
        if self._primary_engine is None:
            self._primary_engine = WebClawEngine()
        
        # Setup fallback
        self._fallback_engine = SimpleEngine()
    
    def _get_available_engine(self):
        """Get the best available engine"""
        if self._primary_engine.is_available():
            return self._primary_engine, self._primary_engine.name
        else:
            return self._fallback_engine, f"{self._fallback_engine.name} (fallback)"
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = "auto") -> TranslationResult:
        """Translate a single text"""
        start_time = time.time()
        
        if not text or not text.strip():
            return TranslationResult(
                success=False,
                original_text=text,
                translated_text="",
                error="Empty text"
            )
        
        try:
            engine, engine_name = self._get_available_engine()
            translated = engine.translate(text, target_lang, source_lang)
            return TranslationResult(
                success=True,
                original_text=text,
                translated_text=translated,
                source_lang=source_lang,
                target_lang=target_lang,
                processing_time=time.time() - start_time,
                engine_used=engine_name
            )
        except Exception as e:
            return TranslationResult(
                success=False,
                original_text=text,
                translated_text="",
                error=str(e),
                processing_time=time.time() - start_time
            )
    
    def translate_document(self, file_path: Path, target_lang: str, source_lang: str = "auto") -> TranslationResult:
        """Translate an entire document"""
        start_time = time.time()
        
        if not file_path.exists():
            return TranslationResult(
                success=False,
                original_text="",
                translated_text="",
                error=f"File not found: {file_path}"
            )
        
        # Get format handler
        format_handler = self._get_format_handler(file_path)
        if not format_handler:
            return TranslationResult(
                success=False,
                original_text="",
                translated_text="",
                error=f"Unsupported format: {file_path.suffix}"
            )
        
        try:
            # Extract text from document
            original_text = format_handler.extract(file_path)
            
            # Translate in chunks
            chunks = self._chunk_text(original_text)
            translated_chunks = []
            engine, engine_name = self._get_available_engine()
            
            for i, chunk in enumerate(chunks):
                try:
                    translated = engine.translate(chunk, target_lang, source_lang)
                    translated_chunks.append(translated)
                except:
                    translated_chunks.append(chunk)  # Fallback to original
            
            translated_text = "\n".join(translated_chunks)
            
            # Save translated document
            output_path = format_handler.save(file_path, translated_text, target_lang)
            
            return TranslationResult(
                success=True,
                original_text=original_text,
                translated_text=translated_text,
                source_lang=source_lang,
                target_lang=target_lang,
                processing_time=time.time() - start_time,
                chunks_processed=len(chunks),
                engine_used=engine_name
            )
            
        except Exception as e:
            return TranslationResult(
                success=False,
                original_text="",
                translated_text="",
                error=str(e),
                processing_time=time.time() - start_time
            )
    
    def _get_format_handler(self, file_path: Path):
        """Get appropriate format handler for file type"""
        from .formats import TextFormat, MarkdownFormat, DocxFormat
        
        handlers = {
            '.txt': TextFormat(),
            '.md': MarkdownFormat(),
            '.markdown': MarkdownFormat(),
            '.docx': DocxFormat(),
        }
        
        return handlers.get(file_path.suffix.lower())
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into manageable chunks"""
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1
            if current_size + word_size > self.chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
