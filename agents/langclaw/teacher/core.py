"""Langclaw Teacher - Language teaching engine"""

from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Lesson:
    """A language lesson"""
    title: str
    language: str
    level: str  # beginner, intermediate, advanced
    content: str
    vocabulary: Dict[str, str]
    exercises: List[str]

class LanguageTeacher:
    """Main teaching engine for Langclaw"""
    
    def __init__(self):
        self.lessons_dir = Path(__file__).parent / "lessons"
        self.exercises_dir = Path(__file__).parent / "exercises"
        self.current_lesson: Optional[Lesson] = None
        self.student_progress: Dict = {}
    
    def get_lesson(self, language: str, topic: str, level: str = "beginner") -> Optional[Lesson]:
        """Get a lesson by language and topic"""
        lesson_file = self.lessons_dir / language / f"{topic}_{level}.md"
        if lesson_file.exists():
            content = lesson_file.read_text(encoding='utf-8')
            return Lesson(
                title=topic,
                language=language,
                level=level,
                content=content,
                vocabulary=self._extract_vocab(content),
                exercises=self._get_exercises(language, topic)
            )
        return None
    
    def _extract_vocab(self, content: str) -> Dict[str, str]:
        """Extract vocabulary from lesson content"""
        vocab = {}
        for line in content.split('\n'):
            if '=' in line:
                word, translation = line.split('=', 1)
                vocab[word.strip()] = translation.strip()
        return vocab
    
    def _get_exercises(self, language: str, topic: str) -> List[str]:
        """Get exercises for a topic"""
        exercise_file = self.exercises_dir / language / f"{topic}_exercises.md"
        if exercise_file.exists():
            return exercise_file.read_text(encoding='utf-8').split('\n---\n')
        return ["Translate the following...", "Fill in the blank..."]
    
    def check_answer(self, question: str, answer: str) -> tuple[bool, str]:
        """Check if an answer is correct"""
        # This would use LLM or predefined answers
        return True, "Correct!"
    
    def get_progress(self) -> Dict:
        """Get student progress"""
        return self.student_progress

# Global instance
teacher = LanguageTeacher()
