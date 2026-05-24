from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(
            self,
            user_id: int,
    ) -> User | None:
        stmt = select(User).where(
            User.user_id == user_id
        )

        return self.db.scalar(stmt)
    
    def create_user(
            self,
            user: User,
    ) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def update_user(
            self,
            user: User
    ) -> User:
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def delete_user(
            self,
            user: User
    ) -> None:
        self.db.delete(user)
        self.db.commit()