from sqlalchemy.orm import Session


class BaseDAO:
    def __init__(self, db: Session):
        self.db = db


class ProtectedBaseDAO(BaseDAO):
    def __init__(self, db: Session, user_id: int):
        super().__init__(db)

        self.user_id = user_id
