from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories.users import UserRepository
from services.users import UserService
from schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

# 유저 조회
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id:int,
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    return service.get_user(user_id)

# 유저 등록
@router.post(
        "/", 
        response_model=UserResponse, 
        status_code=201
)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    return service.create_user(data)

# 유저 정보 수정
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    data: UserUpdate,
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    return service.update_user(user_id, data)

# 유저 삭제
@router.delete(
        "/{user_id}",
        status_code=204
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    return service.delete_user(user_id)
