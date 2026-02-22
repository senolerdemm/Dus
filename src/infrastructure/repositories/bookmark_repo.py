"""IBookmarkRepository implementasyonu."""

from typing import Optional
from sqlalchemy.orm import Session

from src.domain.entities import Bookmark, Question
from src.domain.interfaces import IBookmarkRepository
from src.domain.value_objects import DifficultyLevel
from src.infrastructure.database.models import BookmarkModel, QuestionModel, CategoryModel


class BookmarkRepository(IBookmarkRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, user_id: int, question_id: int, note: Optional[str] = None) -> Bookmark:
        db_bm = BookmarkModel(user_id=user_id, question_id=question_id, note=note)
        self.db.add(db_bm)
        self.db.commit()
        self.db.refresh(db_bm)
        return Bookmark(
            id=db_bm.id, user_id=db_bm.user_id,
            question_id=db_bm.question_id, note=db_bm.note,
            created_at=db_bm.created_at,
        )

    def remove(self, bookmark_id: int, user_id: int) -> bool:
        bm = (
            self.db.query(BookmarkModel)
            .filter(BookmarkModel.id == bookmark_id, BookmarkModel.user_id == user_id)
            .first()
        )
        if not bm:
            return False
        self.db.delete(bm)
        self.db.commit()
        return True

    def get_user_bookmarks(self, user_id: int) -> list[Bookmark]:
        bms = (
            self.db.query(BookmarkModel)
            .filter(BookmarkModel.user_id == user_id)
            .order_by(BookmarkModel.created_at.desc())
            .all()
        )
        result = []
        for bm in bms:
            q = self.db.query(QuestionModel).join(CategoryModel).filter(QuestionModel.id == bm.question_id).first()
            question = None
            if q:
                question = Question(
                    id=q.id, category_id=q.category_id,
                    question_text=q.question_text,
                    option_a=q.option_a, option_b=q.option_b,
                    option_c=q.option_c, option_d=q.option_d, option_e=q.option_e,
                    correct_answer=q.correct_answer, explanation=q.explanation,
                    difficulty=DifficultyLevel(q.difficulty), source=q.source or "",
                    category_name=q.category.name if q.category else "",
                )
            result.append(Bookmark(
                id=bm.id, user_id=bm.user_id, question_id=bm.question_id,
                note=bm.note, created_at=bm.created_at, question=question,
            ))
        return result

    def is_bookmarked(self, user_id: int, question_id: int) -> bool:
        return (
            self.db.query(BookmarkModel)
            .filter(BookmarkModel.user_id == user_id, BookmarkModel.question_id == question_id)
            .first()
        ) is not None
