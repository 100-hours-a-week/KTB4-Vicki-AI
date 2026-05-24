from fastapi import HTTPException
from repositories.users import UserRepository

from models import User
from schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user(
            self,
            user_id: int
    ):
        return self.repo.get_user_by_id(user_id)
    
    def create_user(
            self,
            data: UserCreate
    ):
        user = User(
            email = data.email,
            password = data.password,
            nickname = data.nickname
        )
        
        return self.repo.create_user(user)
    
    def update_user(
            self,
            user_id: int,
            data: UserUpdate
    ):
        user = self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        if data.nickname is not None:
            user.nickname = data.nickname
        
        if data.password is not None:
            user.password = data.password

        return self.repo.update_user(user)
    
    def delete_user(
            self,
            user_id: int
    ):
        user = self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        self.repo.delete_user(user)