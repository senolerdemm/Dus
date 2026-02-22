"""
Application DTOs (Data Transfer Objects)
=========================================
Pydantic modelleri — API request/response şemaları.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ─── Auth ───

class RegisterRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2, max_length=100)


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str = ""
    token_type: str = "bearer"
    user_id: str = ""


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: Optional[datetime] = None


# ─── Category ───

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    color: str
    question_count: int = 0


# ─── Question ───

class QuestionResponse(BaseModel):
    id: int
    category_id: int
    category_name: str = ""
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    option_e: str
    difficulty: str


class QuestionWithAnswerResponse(BaseModel):
    id: int
    category_id: int
    category_name: str = ""
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    option_e: str
    correct_answer: str
    explanation: str
    difficulty: str
    source: str = ""


# ─── Quiz ───

class QuizStartRequest(BaseModel):
    category_id: Optional[int] = None
    question_count: int = Field(default=20, ge=5, le=50)


class QuizStartResponse(BaseModel):
    session_id: int
    questions: list[QuestionResponse]
    total_questions: int


class AnswerRequest(BaseModel):
    session_id: int
    question_id: int
    selected_answer: str = Field(..., pattern="^[A-E]$")


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str
    selected_answer: str


class QuizFinishRequest(BaseModel):
    session_id: int
    time_spent_seconds: int = Field(..., ge=0)


class QuizFinishResponse(BaseModel):
    session_id: int
    score: int
    total_questions: int
    percentage: float
    grade_label: str
    time_spent_seconds: int
    category_breakdown: list[dict] = []


class QuizHistoryItem(BaseModel):
    id: int
    category_name: str = "Karışık"
    score: int
    total_questions: int
    percentage: float
    time_spent_seconds: int
    completed_at: Optional[datetime] = None


# ─── Stats ───

class StatsOverview(BaseModel):
    total_quizzes: int = 0
    total_questions_answered: int = 0
    correct_answers: int = 0
    wrong_answers: int = 0
    overall_percentage: float = 0.0
    grade_label: str = ""


class CategoryStat(BaseModel):
    category_id: int
    category_name: str
    icon: str = ""
    color: str = ""
    total_answered: int = 0
    correct: int = 0
    percentage: float = 0.0


# ─── Bookmark ───

class BookmarkAddRequest(BaseModel):
    question_id: int
    note: Optional[str] = None


class BookmarkResponse(BaseModel):
    id: int
    question_id: int
    question_text: str = ""
    category_name: str = ""
    note: Optional[str] = None
    created_at: datetime


# ─── AI ───

class HintRequest(BaseModel):
    question_id: int


class HintResponse(BaseModel):
    hint: str


class ExplainRequest(BaseModel):
    question_id: int
    selected_answer: str = Field(..., pattern="^[A-E]$")


class ExplainResponse(BaseModel):
    explanation: str


class WeaknessResponse(BaseModel):
    analysis: str
    weak_categories: list[dict] = []
