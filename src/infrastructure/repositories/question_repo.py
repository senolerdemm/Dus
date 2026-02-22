"""IQuestionRepository implementasyonu."""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from src.domain.entities import Question
from src.domain.interfaces import IQuestionRepository
from src.domain.value_objects import DifficultyLevel
from src.infrastructure.database.models import QuestionModel, CategoryModel


class QuestionRepository(IQuestionRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        category_id: Optional[int] = None,
        difficulty: Optional[DifficultyLevel] = None,
    ) -> list[Question]:
        query = self.db.query(QuestionModel).join(CategoryModel)

        if category_id:
            query = query.filter(QuestionModel.category_id == category_id)
        if difficulty:
            query = query.filter(QuestionModel.difficulty == difficulty.value)

        return [self._to_entity(q) for q in query.all()]

    def get_by_id(self, question_id: int) -> Optional[Question]:
        q = (
            self.db.query(QuestionModel)
            .join(CategoryModel)
            .filter(QuestionModel.id == question_id)
            .first()
        )
        return self._to_entity(q) if q else None

    def get_random(
        self,
        count: int = 20,
        category_id: Optional[int] = None,
    ) -> list[Question]:
        query = self.db.query(QuestionModel).join(CategoryModel)

        if category_id:
            query = query.filter(QuestionModel.category_id == category_id)

        # Rastgele sırala
        questions = query.order_by(func.random()).limit(count).all()
        return [self._to_entity(q) for q in questions]

    def count_by_category(self) -> dict[int, int]:
        results = (
            self.db.query(
                QuestionModel.category_id,
                func.count(QuestionModel.id),
            )
            .group_by(QuestionModel.category_id)
            .all()
        )
        return {cat_id: count for cat_id, count in results}

    @staticmethod
    def _to_entity(model: QuestionModel) -> Question:
        return Question(
            id=model.id,
            category_id=model.category_id,
            question_text=model.question_text,
            option_a=model.option_a,
            option_b=model.option_b,
            option_c=model.option_c,
            option_d=model.option_d,
            option_e=model.option_e,
            correct_answer=model.correct_answer,
            explanation=model.explanation,
            difficulty=DifficultyLevel(model.difficulty),
            source=model.source or "",
            category_name=model.category.name if model.category else "",
        )
