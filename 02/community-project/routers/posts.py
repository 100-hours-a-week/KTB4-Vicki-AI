from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories.posts import PostRepository
from repositories.comments import CommentRepository
from services.posts import PostService
from services.comments import CommentService
from services.ai_service import AIService
from schemas import PostCreate, PostUpdate, PostResponse
from schemas import SummaryResponse

router = APIRouter(
    prefix="/posts",
    tags=["post"]
)

@router.get("/")
def get_all_post(
    db: Session = Depends(get_db)
):
    repo = PostRepository(db)
    service = PostService(repo)
    return service.get_all_posts()

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    repo = PostRepository(db)
    service = PostService(repo)

    return service.get_post(post_id)

@router.get("/{post_id}/comments")
def get_post_comment(
    post_id: int,
    db: Session = Depends(get_db)
):
    repo = CommentRepository(db)
    service = CommentService(repo)

    return service.get_post_comment(post_id)

@router.post("/", status_code=201)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db)
):
    repo = PostRepository(db)
    service = PostService(repo)

    return service.create_post(post)

@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db)
):
    repo = PostRepository(db)
    service = PostService(repo)
    
    return service.update_post(post_id, data)

@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    repo = PostRepository(db)
    service = PostService(repo)

    return service.delete_post(post_id)

@router.get("/{post_id}/summarize", response_model=SummaryResponse)
async def summarize_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    repo = PostRepository(db)
    service = PostService(repo)

    return await service.summarize_post(post_id)

