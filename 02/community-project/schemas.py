from datetime import datetime

from pydantic import EmailStr
from pydantic import Field
from pydantic import ConfigDict
from pydantic import BaseModel

# User
class UserBase(BaseModel):
    email:EmailStr
    nickname: str = Field(min_length=2, max_length=30)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)

class UserUpdate(BaseModel):
    nickname: str | None = Field(default=None, min_length=2, max_length=30)
    password: str | None = Field(default=None, min_length=2, max_length=255)

class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Post
class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)

class PostCreate(PostBase):
    user_id: int

class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None, min_length=1)

class PostResponse(PostBase):
    post_id: int
    user_id: int
    view_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Comment
class CommentBase(BaseModel):
    content: str = Field(min_length=1)

class CommentCreate(CommentBase):
    post_id: int
    user_id: int

class CommentUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1)

class CommentResponse(CommentBase):
    comment_id: int
    post_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# AI

class SummaryResponse(BaseModel):
    summary: str