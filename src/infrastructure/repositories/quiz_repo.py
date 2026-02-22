"""IQuizRepository + ICategoryRepository implementasyonu."""

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func as sa_func, case

from src.domain.entities import QuizSession, UserAnswer, Category
from src.domain.interfaces import IQuizRepository, ICategoryRepository
from src.infrastructure.database.models import (
    QuizSessionModel, UserAnswerModel, CategoryModel, QuestionModel
)


class CategoryRepository(ICategoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Category]:
        cats = self.db.query(CategoryModel).all()
        # Her kategori için soru sayısını hesapla
        counts = (
            self.db.query(
                QuestionModel.category_id,
                sa_func.count(QuestionModel.id),
            )
            .group_by(QuestionModel.category_id)
            .all()
        )
        count_map = {cat_id: cnt for cat_id, cnt in counts}

        return [
            Category(
                id=c.id,
                name=c.name,
                description=c.description,
                icon=c.icon,
                color=c.color,
                question_count=count_map.get(c.id, 0),
            )
            for c in cats
        ]

    def get_by_id(self, category_id: int) -> Optional[Category]:
        c = self.db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        if not c:
            return None
        count = (
            self.db.query(sa_func.count(QuestionModel.id))
            .filter(QuestionModel.category_id == category_id)
            .scalar()
        )
        return Category(
            id=c.id, name=c.name, description=c.description,
            icon=c.icon, color=c.color, question_count=count or 0,
        )


class QuizRepository(IQuizRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, session: QuizSession) -> QuizSession:
        db_session = QuizSessionModel(
            user_id=session.user_id,
            category_id=session.category_id,
            total_questions=session.total_questions,
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        session.id = db_session.id
        session.created_at = db_session.created_at
        return session

    def get_session(self, session_id: int) -> Optional[QuizSession]:
        s = self.db.query(QuizSessionModel).filter(QuizSessionModel.id == session_id).first()
        if not s:
            return None
        return QuizSession(
            id=s.id, user_id=s.user_id, category_id=s.category_id,
            score=s.score, total_questions=s.total_questions,
            time_spent_seconds=s.time_spent_seconds,
            completed_at=s.completed_at, created_at=s.created_at,
            category_name=s.category.name if s.category else "Karışık",
        )

    def save_answer(self, answer: UserAnswer) -> UserAnswer:
        db_answer = UserAnswerModel(
            session_id=answer.session_id,
            question_id=answer.question_id,
            selected_answer=answer.selected_answer,
            is_correct=answer.is_correct,
        )
        self.db.add(db_answer)
        self.db.commit()
        self.db.refresh(db_answer)
        answer.id = db_answer.id
        return answer

    def finish_session(
        self, session_id: int, score: int,
        total_questions: int, time_spent_seconds: int,
    ) -> QuizSession:
        s = self.db.query(QuizSessionModel).filter(QuizSessionModel.id == session_id).first()
        if s:
            s.score = score
            s.total_questions = total_questions
            s.time_spent_seconds = time_spent_seconds
            s.completed_at = datetime.now()
            self.db.commit()
            self.db.refresh(s)
        return self.get_session(session_id)

    def get_user_history(self, user_id: int, limit: int = 20) -> list[QuizSession]:
        sessions = (
            self.db.query(QuizSessionModel)
            .filter(QuizSessionModel.user_id == user_id)
            .filter(QuizSessionModel.completed_at.isnot(None))
            .order_by(QuizSessionModel.completed_at.desc())
            .limit(limit)
            .all()
        )
        result = []
        for s in sessions:
            total = s.total_questions or 1
            result.append(QuizSession(
                id=s.id, user_id=s.user_id, category_id=s.category_id,
                score=s.score, total_questions=s.total_questions,
                time_spent_seconds=s.time_spent_seconds,
                completed_at=s.completed_at, created_at=s.created_at,
                percentage=round((s.score / total) * 100, 1),
                category_name=s.category.name if s.category else "Karışık",
            ))
        return result

    def get_session_answers(self, session_id: int) -> list[UserAnswer]:
        answers = (
            self.db.query(UserAnswerModel)
            .filter(UserAnswerModel.session_id == session_id)
            .all()
        )
        return [
            UserAnswer(
                id=a.id, session_id=a.session_id,
                question_id=a.question_id,
                selected_answer=a.selected_answer,
                is_correct=a.is_correct,
            )
            for a in answers
        ]

    def get_user_stats(self, user_id: int) -> dict:
        total_quizzes = (
            self.db.query(sa_func.count(QuizSessionModel.id))
            .filter(QuizSessionModel.user_id == user_id)
            .filter(QuizSessionModel.completed_at.isnot(None))
            .scalar() or 0
        )
        answer_stats = (
            self.db.query(
                sa_func.count(UserAnswerModel.id),
                sa_func.sum(
                    case(
                        (UserAnswerModel.is_correct == True, 1),
                        else_=0,
                    )
                ),
            )
            .join(QuizSessionModel)
            .filter(QuizSessionModel.user_id == user_id)
            .first()
        )
        total_answered = answer_stats[0] or 0
        correct = int(answer_stats[1] or 0)

        return {
            "total_quizzes": total_quizzes,
            "total_answered": total_answered,
            "correct_answers": correct,
        }

    def get_category_stats(self, user_id: int) -> list[dict]:
        results = (
            self.db.query(
                CategoryModel.id,
                CategoryModel.name,
                CategoryModel.icon,
                CategoryModel.color,
                sa_func.count(UserAnswerModel.id),
                sa_func.sum(
                    case(
                        (UserAnswerModel.is_correct == True, 1),
                        else_=0,
                    )
                ),
            )
            .join(QuestionModel, QuestionModel.category_id == CategoryModel.id)
            .join(UserAnswerModel, UserAnswerModel.question_id == QuestionModel.id)
            .join(QuizSessionModel, QuizSessionModel.id == UserAnswerModel.session_id)
            .filter(QuizSessionModel.user_id == user_id)
            .group_by(CategoryModel.id)
            .all()
        )
        return [
            {
                "category_id": r[0],
                "category_name": r[1],
                "icon": r[2],
                "color": r[3],
                "total_answered": r[4] or 0,
                "correct": int(r[5] or 0),
                "percentage": round((int(r[5] or 0) / (r[4] or 1)) * 100, 1),
            }
            for r in results
        ]
