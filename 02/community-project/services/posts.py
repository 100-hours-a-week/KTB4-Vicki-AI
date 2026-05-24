from fastapi import HTTPException

from services.ai_service import AIService
from repositories.posts import PostRepository
from models import Post
from schemas import PostCreate, PostUpdate, SummaryResponse


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    def get_post(
            self,
            post_id: int
    ):
        
        post = self.repo.get_post_by_id(post_id)

        if not post:
            raise HTTPException(
                status_code=404,
                detail="Post not found"
            )
        
        self.repo.increase_view_count(post)

        return post
    
    def get_all_posts(self):
        return self.repo.get_all_posts()
    
    def create_post(
            self,
            data: PostCreate
    ):
        post = Post(
            user_id = data.user_id,
            title = data.title,
            content = data.content
        )

        return self.repo.create_post(post)
    
    def update_post(
            self,
            post_id: int,
            data: PostUpdate
    ):
        post = self.repo.get_post_by_id(post_id)

        if not post:
            raise HTTPException(
                status_code=404,
                detail="Post not found"
            )

        if data.title is not None:
            post.title = data.title

        if data.content is not None:
            post.content = data.content

        return self.repo.update_post(post)
    
    def delete_post(
            self,
            post_id: int
    ):
        post = self.repo.get_post_by_id(post_id)

        if not post:
            raise HTTPException(
                status_code=404,
                detail="Post not found"
            )
        
        self.repo.delete_post(post)

    async def summarize_post(
            self,
            post_id: int
    ):
        post = self.get_post(post_id)

        if not post:
            raise HTTPException(
                status_code=404,
                detail="Post not found"
            )
        
        summary = await AIService.summarize(
            post.content
        )

        return SummaryResponse(summary=summary)
        

        
