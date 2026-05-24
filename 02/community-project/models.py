from datetime import datetime
from typing import List
from typing_extensions import Annotated

from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

str30 = Annotated[str,30]
str255 = Annotated[str,255]

class Base(DeclarativeBase):
    type_annotation_map = {
        str30: String(30),
        str255: String(255),
        datetime: TIMESTAMP(timezone=True)
    }

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at_type = Annotated[datetime, mapped_column(insert_default=func.now())]

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[intpk]
    email: Mapped[str30] = mapped_column(unique=True)
    password: Mapped[str255]
    nickname: Mapped[str30]
    created_at: Mapped[created_at_type]

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

class Post(Base):
    __tablename__ = "post"

    post_id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    title: Mapped[str255]
    content: Mapped[str]
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[created_at_type]

    user: Mapped[User] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

class Comment(Base):
    __tablename__ = "comment"
    comment_id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.post_id"))
    content: Mapped[str]
    created_at: Mapped[created_at_type]

    user: Mapped[User] = relationship(back_populates="comments")
    post: Mapped[Post] = relationship(back_populates="comments")