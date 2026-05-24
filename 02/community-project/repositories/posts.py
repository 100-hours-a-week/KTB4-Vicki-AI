from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Post

class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_post_by_id(
            self,
            post_id: int
    ) -> Post | None:
        stmt = select(Post).where(
            Post.post_id == post_id
        )

        return self.db.scalar(stmt)
    
    def increase_view_count(
            self,
            post: Post
    ):
        post.view_count += 1
        self.db.commit()
        self.db.refresh(post)
    
    def get_all_posts(self):
        stmt = select(Post)

        return self.db.scalars(stmt).all()
    
    def create_post(
            self,
            post: Post
    ) -> Post:
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        return post
    
    def update_post(
            self,
            post: Post
    ) -> Post:
        self.db.commit()
        self.db.refresh(post)

        return post
    
    def delete_post(
            self,
            post: Post
    ) -> None:
        self.db.delete(post)
        self.db.commit()
