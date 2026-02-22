"""
Domain Entities
===============
Saf Python — hiçbir dış bağımlılık yok.
İş alanının temel varlıkları.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.domain.value_objects import DifficultyLevel


@dataclass
class User:
    """Kullanıcı entity'si — id Supabase UUID."""
    id: str = ""                # Supabase Auth UUID
    email: str = ""
    full_name: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Category:
    """DUS soru kategorisi."""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    icon: str = ""
    color: str = ""
    question_count: int = 0


@dataclass
class Question:
    """DUS sorusu."""
    id: Optional[int] = None
    category_id: int = 0
    question_text: str = ""
    option_a: str = ""
    option_b: str = ""
    option_c: str = ""
    option_d: str = ""
    option_e: str = ""
    correct_answer: str = ""
    explanation: str = ""
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    source: str = ""
    category_name: str = ""


@dataclass
class QuizSession:
    """Bir sınav oturumu."""
    id: Optional[int] = None
    user_id: str = ""           # Supabase UUID
    category_id: Optional[int] = None
    score: int = 0
    total_questions: int = 0
    time_spent_seconds: int = 0
    completed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    percentage: float = 0.0
    category_name: str = ""


@dataclass
class UserAnswer:
    """Kullanıcının bir soruya verdiği cevap."""
    id: Optional[int] = None
    session_id: int = 0
    question_id: int = 0
    selected_answer: str = ""
    is_correct: bool = False


@dataclass
class Bookmark:
    """Kullanıcının işaretlediği soru."""
    id: Optional[int] = None
    user_id: str = ""           # Supabase UUID
    question_id: int = 0
    note: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    question: Optional[Question] = None
