from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.article import ArticleCreate, ArticleRead
from app.services.article import article_service
from app.api.auth import get_current_user_obj

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/", response_model=List[ArticleRead])
async def list_articles(limit: int = 100, offset: int = 0):
    return await article_service.list_articles(limit=limit, offset=offset, published_only=True)

@router.get("/{slug}", response_model=ArticleRead)
async def get_article(slug: str):
    article = await article_service.get_article_by_slug(slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not article.is_published:
        # Require auth to view unpublished articles
        raise HTTPException(status_code=403, detail="Article is not published")
    return article

@router.post("/", response_model=ArticleRead)
async def create_article(payload: ArticleCreate, current_user=Depends(get_current_user_obj)):
    # Only admins or specific roles might be allowed to create, but for now we link the author
    if current_user.role not in ["admin", "author"]:
        raise HTTPException(status_code=403, detail="Not authorized to create articles")
    
    payload.author_id = current_user.id
    
    existing = await article_service.get_article_by_slug(payload.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
        
    article = await article_service.create_article(payload)
    return article
