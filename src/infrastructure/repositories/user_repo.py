"""IUserRepository implementasyonu — Supabase UUID uyumlu."""

from typing import Optional
from sqlalchemy.orm import Session

from src.domain.entities import User
from src.domain.interfaces import IUserRepository
from src.infrastructure.database.models import UserModel


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        db_user = UserModel(
            id=user.id,  # Supabase UUID
            email=user.email,
            full_name=user.full_name,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)

    def get_by_id(self, user_id: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(db_user) if db_user else None

    def get_by_email(self, email: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(db_user) if db_user else None

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            created_at=model.created_at,
        )
