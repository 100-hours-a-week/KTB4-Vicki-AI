from fastapi import HTTPException

from repositories.comments import CommentRepository
from models import Comment
from schemas import CommentCreate, CommentUpdate, CommentResponse

class CommentService:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    def get_comment(
            self,
            comment_id: int
    ):
        comment = self.repo.get_comment_by_id(comment_id)

        if not comment:
            raise HTTPException(
                status_code=404,
                detail="Comment not found"
            )
        
        return comment
    
    def get_post_comment(
            self,
            post_id: int
    ):
        return self.repo.get_comment_by_post_id(post_id)
    
    def create_comment(
            self,
            data: CommentCreate
    ):
        comment = Comment(
            user_id = data.user_id,
            post_id = data.post_id,
            content = data.content
        )

        return self.repo.create_comment(comment)
    
    def update_comment(
            self,
            comment_id: int,
            data: CommentUpdate
    ):
        comment = self.repo.get_comment_by_id(comment_id)

        if not comment:
            raise HTTPException(
                status_code=404,
                detail="Comment not found"
            )
        
        if data.content is not None:
            comment.content = data.content

        return self.repo.update_comment(comment)
    
    def delete_comment(
            self,
            comment_id: int
    ):
        comment = self.repo.get_comment_by_id(comment_id)

        if not comment:
            raise HTTPException(
                status_code=404,
                detail="Comment not found"
            )
        
        self.repo.delet_comment(comment)