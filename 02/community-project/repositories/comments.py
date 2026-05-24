from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Comment

class CommentRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_comment_by_id(
            self,
            comment_id: int
    ) -> Comment | None:
        stmt = select(Comment).where(Comment.comment_id == comment_id)

        return self.db.scalar(stmt)
    
    def get_comment_by_post_id(
            self,
            post_id: int
    ):
        print("도착",post_id)
        stmt = select(Comment).where(Comment.post_id == post_id)

        return self.db.scalars(stmt).all()
    
    def create_comment(
            self,
            comment: Comment
    ) -> Comment:
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        return comment
    
    def update_comment(
            self,
            comment: Comment
    ) -> Comment:
        self.db.commit()
        self.db.refresh(comment)

        return comment
    
    def delet_comment(
            self,
            comment: Comment
    ) -> None:
        self.db.delete(comment)
        self.db.commit()