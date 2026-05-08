from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class ArticleBase(SQLModel):
    title: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    summary: Optional[str] = Field(default=None)
    category: str = Field(default="General", index=True)
    tags: Optional[str] = Field(default=None) # Stored as comma-separated string for simplicity
    file_path: str = Field(index=True) # Relative path in the content directory
    author_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    is_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Article(ArticleBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class ArticleCreate(ArticleBase):
    pass

class ArticleRead(ArticleBase):
    id: UUID
