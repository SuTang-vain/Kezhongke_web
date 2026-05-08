from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from app.models.article import Article, ArticleCreate, ArticleRead
from app.db.session import AsyncSessionLocal
from typing import List

class ArticleService:
    async def create_article(self, article_create: ArticleCreate) -> Article:
        async with AsyncSessionLocal() as session:
            article = Article(**article_create.model_dump())
            session.add(article)
            await session.commit()
            await session.refresh(article)
            return article

    async def get_article_by_id(self, article_id: UUID) -> Article | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Article).where(Article.id == article_id))
            return result.scalar_one_or_none()

    async def get_article_by_slug(self, slug: str) -> Article | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Article).where(Article.slug == slug))
            return result.scalar_one_or_none()

    async def list_articles(self, limit: int = 100, offset: int = 0, published_only: bool = True) -> List[Article]:
        async with AsyncSessionLocal() as session:
            query = select(Article)
            if published_only:
                query = query.where(Article.is_published == True)
            query = query.order_by(desc(Article.created_at)).offset(offset).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

article_service = ArticleService()
