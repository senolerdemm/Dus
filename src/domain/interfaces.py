"""
Domain Interfaces (Repository Contracts)
=========================================
Saf Python — hiçbir dış bağımlılık yok.
Infrastructure katmanı bu interface'leri implemente eder.
"""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities import (
    User, Category, Question, QuizSession, UserAnswer, Bookmark
)
from src.domain.value_objects import DifficultyLevel


class IUserRepository(ABC):
    """Kullanıcı profil veri erişim sözleşmesi."""

    @abstractmethod
    def create(self, user: User) -> User:
        ...

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        ...


class IQuestionRepository(ABC):
    @abstractmethod
    def get_all(self, category_id: Optional[int] = None, difficulty: Optional[DifficultyLevel] = None) -> list[Question]:
        ...

    @abstractmethod
    def get_by_id(self, question_id: int) -> Optional[Question]:
        ...

    @abstractmethod
    def get_random(self, count: int = 20, category_id: Optional[int] = None) -> list[Question]:
        ...

    @abstractmethod
    def count_by_category(self) -> dict[int, int]:
        ...


class ICategoryRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Category]:
        ...

    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        ...


class IQuizRepository(ABC):
    @abstractmethod
    def create_session(self, session: QuizSession) -> QuizSession:
        ...

    @abstractmethod
    def get_session(self, session_id: int) -> Optional[QuizSession]:
        ...

    @abstractmethod
    def save_answer(self, answer: UserAnswer) -> UserAnswer:
        ...

    @abstractmethod
    def finish_session(self, session_id: int, score: int, total_questions: int, time_spent_seconds: int) -> QuizSession:
        ...

    @abstractmethod
    def get_user_history(self, user_id: str, limit: int = 20) -> list[QuizSession]:
        ...

    @abstractmethod
    def get_session_answers(self, session_id: int) -> list[UserAnswer]:
        ...

    @abstractmethod
    def get_user_stats(self, user_id: str) -> dict:
        ...

    @abstractmethod
    def get_category_stats(self, user_id: str) -> list[dict]:
        ...


class IBookmarkRepository(ABC):
    @abstractmethod
    def add(self, user_id: str, question_id: int, note: Optional[str] = None) -> Bookmark:
        ...

    @abstractmethod
    def remove(self, bookmark_id: int, user_id: str) -> bool:
        ...

    @abstractmethod
    def get_user_bookmarks(self, user_id: str) -> list[Bookmark]:
        ...

    @abstractmethod
    def is_bookmarked(self, user_id: str, question_id: int) -> bool:
        ...
