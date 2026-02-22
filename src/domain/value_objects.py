"""
Domain Value Objects
====================
Saf Python — hiçbir dış bağımlılık yok.
İş kurallarını ifade eden değer objeleri.
"""

from enum import Enum


class DifficultyLevel(Enum):
    """Soru zorluk seviyeleri."""
    EASY = "kolay"
    MEDIUM = "orta"
    HARD = "zor"


class AnswerOption(Enum):
    """Geçerli cevap şıkları."""
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


class ScoreGrade(Enum):
    """Sınav sonuç dereceleri."""
    EXCELLENT = ("Mükemmel! 🌟", 90, 100)
    GREAT = ("Çok İyi! 💪", 70, 89)
    GOOD = ("Geliştirebilirsin 📚", 50, 69)
    FAIR = ("Daha fazla çalış 📖", 30, 49)
    POOR = ("Vazgeçme! 🎯", 0, 29)

    def __init__(self, label: str, min_score: int, max_score: int):
        self.label = label
        self.min_score = min_score
        self.max_score = max_score

    @classmethod
    def from_score(cls, score: int) -> "ScoreGrade":
        """Skora göre dereceyi döndürür."""
        for grade in cls:
            if grade.min_score <= score <= grade.max_score:
                return grade
        return cls.POOR
