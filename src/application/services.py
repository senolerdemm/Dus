"""
Application Services (Use Cases)
=================================
İş mantığı. Domain interface'leri kullanır, infrastructure'a bağımlı değil.
"""

from typing import Optional
from src.domain.entities import User, QuizSession, UserAnswer
from src.domain.interfaces import IUserRepository, IQuestionRepository, IQuizRepository, IBookmarkRepository
from src.domain.value_objects import ScoreGrade


# ─── Auth Service ───

class AuthService:
    """Kullanıcı profil yönetimi (Supabase Auth ile birlikte)."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def ensure_profile(self, user_id: str, email: str, full_name: str) -> User:
        """Supabase user'ı için local profil oluştur veya getir."""
        existing = self.user_repo.get_by_id(user_id)
        if existing:
            return existing
        user = User(id=user_id, email=email, full_name=full_name)
        return self.user_repo.create(user)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)


# ─── Quiz Service ───

class QuizService:
    def __init__(self, question_repo: IQuestionRepository, quiz_repo: IQuizRepository):
        self.question_repo = question_repo
        self.quiz_repo = quiz_repo

    def start_quiz(self, user_id: str, category_id: Optional[int], question_count: int = 20) -> tuple:
        questions = self.question_repo.get_random(count=question_count, category_id=category_id)
        if not questions:
            raise ValueError("Bu kategori için yeterli soru bulunamadı")
        session = QuizSession(user_id=user_id, category_id=category_id, total_questions=len(questions))
        session = self.quiz_repo.create_session(session)
        return session, questions

    def submit_answer(self, session_id: int, question_id: int, selected_answer: str) -> dict:
        question = self.question_repo.get_by_id(question_id)
        if not question:
            raise ValueError("Soru bulunamadı")
        is_correct = selected_answer.upper() == question.correct_answer.upper()
        answer = UserAnswer(session_id=session_id, question_id=question_id,
                           selected_answer=selected_answer.upper(), is_correct=is_correct)
        self.quiz_repo.save_answer(answer)
        return {"is_correct": is_correct, "correct_answer": question.correct_answer,
                "explanation": question.explanation, "selected_answer": selected_answer.upper()}

    def finish_quiz(self, session_id: int, time_spent_seconds: int) -> dict:
        answers = self.quiz_repo.get_session_answers(session_id)
        session = self.quiz_repo.get_session(session_id)
        if not session:
            raise ValueError("Oturum bulunamadı")
        correct_count = sum(1 for a in answers if a.is_correct)
        total = len(answers) if answers else session.total_questions
        percentage = round((correct_count / total) * 100, 1) if total > 0 else 0
        grade = ScoreGrade.from_score(int(percentage))
        self.quiz_repo.finish_session(session_id=session_id, score=correct_count,
                                       total_questions=total, time_spent_seconds=time_spent_seconds)
        return {"session_id": session_id, "score": correct_count, "total_questions": total,
                "percentage": percentage, "grade_label": grade.label, "time_spent_seconds": time_spent_seconds}

    def get_history(self, user_id: str, limit: int = 20) -> list[QuizSession]:
        return self.quiz_repo.get_user_history(user_id, limit)


# ─── Stats Service ───

class StatsService:
    def __init__(self, quiz_repo: IQuizRepository):
        self.quiz_repo = quiz_repo

    def get_overview(self, user_id: str) -> dict:
        stats = self.quiz_repo.get_user_stats(user_id)
        total = stats.get("total_answered", 0)
        correct = stats.get("correct_answers", 0)
        percentage = round((correct / total) * 100, 1) if total > 0 else 0
        grade = ScoreGrade.from_score(int(percentage))
        return {"total_quizzes": stats.get("total_quizzes", 0), "total_questions_answered": total,
                "correct_answers": correct, "wrong_answers": total - correct,
                "overall_percentage": percentage, "grade_label": grade.label}

    def get_by_category(self, user_id: str) -> list[dict]:
        return self.quiz_repo.get_category_stats(user_id)


# ─── Bookmark Service ───

class BookmarkService:
    def __init__(self, bookmark_repo: IBookmarkRepository):
        self.bookmark_repo = bookmark_repo

    def add_bookmark(self, user_id: str, question_id: int, note: Optional[str] = None):
        if self.bookmark_repo.is_bookmarked(user_id, question_id):
            raise ValueError("Bu soru zaten işaretlenmiş")
        return self.bookmark_repo.add(user_id, question_id, note)

    def remove_bookmark(self, bookmark_id: int, user_id: str) -> bool:
        return self.bookmark_repo.remove(bookmark_id, user_id)

    def get_bookmarks(self, user_id: str):
        return self.bookmark_repo.get_user_bookmarks(user_id)
