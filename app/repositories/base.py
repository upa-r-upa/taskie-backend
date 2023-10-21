from sqlalchemy.orm import Session

from app.models.models import User


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db


class ProtectedBaseRepository(BaseRepository):
    def __init__(self, db: Session, user: User):
        super().__init__(db)

        self.user_id = user.id
        self.username = user.username
