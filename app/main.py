from fastapi import FastAPI, Depends
from sqlmodel import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.core.config import settings
from app.api.auth import router as auth_router
import redis.asyncio as redis

app = FastAPI(title=settings.PROJECT_NAME)

# Include Routers
app.include_router(auth_router, prefix="/api")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

@app.get("/api/db-test")
async def db_test(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(text("SELECT 1"))
        return {"db_connection": "ok"}
    except Exception as e:
        return {"db_connection": f"failed: {str(e)}"}

@app.get("/api/redis-test")
async def redis_test():
    try:
        r = redis.from_url(settings.REDIS_URL)
        await r.set("test_key", "ok", ex=10)
        value = await r.get("test_key")
        return {"redis_connection": value.decode() if value else "failed"}
    except Exception as e:
        return {"redis_connection": f"failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
