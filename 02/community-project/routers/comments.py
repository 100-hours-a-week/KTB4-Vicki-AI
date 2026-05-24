from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories.comments import CommentRepository
from services.comments import CommentService
from schemas import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(
    prefix="/comments",
    tags=["comment"]
)

@router.get("/{comment_id}")
def get_comment(
    comment_id: int,
    db: Session=Depends(get_db)
):
    repo = CommentRepository(db)
    service = CommentService(repo)

    return service.get_comment(comment_id)


@router.post("/", status_code=201)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    repo = CommentRepository(db)
    service = CommentService(repo)

    return service.create_comment(comment)

@router.patch("/{comment_id}")
def update_comment(
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db)
):
    repo = CommentRepository(db)
    service = CommentService(repo)

    return service.update_comment(comment_id, data)

@router.delete("/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int,
    db: Session=Depends(get_db)
):
    repo = CommentRepository(db)
    service = CommentService(repo)

    return service.delete_comment(comment_id)
