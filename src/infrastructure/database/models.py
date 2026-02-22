"""
Infrastructure — SQLAlchemy ORM Models
=======================================
Domain entity'leri ile 1:1 eşleşen ORM modelleri.
user_id alanları String (Supabase UUID).
"""

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime,
    ForeignKey, func
)
from sqlalchemy.orm import relationship

from src.infrastructure.database.supabase_client import Base


class UserModel(Base):
    """Local kullanıcı profili — Supabase Auth ile sync."""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)  # Supabase UUID
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False, default="")
    created_at = Column(DateTime, server_default=func.now())

    quiz_sessions = relationship("QuizSessionModel", back_populates="user")
    bookmarks = relationship("BookmarkModel", back_populates="user")


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, default="")
    icon = Column(String(10), default="📚")
    color = Column(String(7), default="#6C5CE7")

    questions = relationship("QuestionModel", back_populates="category")


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    option_e = Column(Text, nullable=False)
    correct_answer = Column(String(1), nullable=False)
    explanation = Column(Text, nullable=False)
    difficulty = Column(String(10), default="orta")
    source = Column(String(200), default="")

    category = relationship("CategoryModel", back_populates="questions")
    user_answers = relationship("UserAnswerModel", back_populates="question")
    bookmarks = relationship("BookmarkModel", back_populates="question")


class QuizSessionModel(Base):
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    time_spent_seconds = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", back_populates="quiz_sessions")
    category = relationship("CategoryModel")
    answers = relationship("UserAnswerModel", back_populates="session")


class UserAnswerModel(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_answer = Column(String(1), nullable=False)
    is_correct = Column(Boolean, default=False)

    session = relationship("QuizSessionModel", back_populates="answers")
    question = relationship("QuestionModel", back_populates="user_answers")


class BookmarkModel(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("UserModel", back_populates="bookmarks")
    question = relationship("QuestionModel", back_populates="bookmarks")
