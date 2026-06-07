"""oh-my-lazybones API Server."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[arg-type]
    """Startup: create tables, init search index. Shutdown: no-op."""
    from .database import engine
    from .models import Base  # noqa: F811 — imported here to avoid circular import

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="oh-my-lazybones API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/api/v1/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0", "environment": settings.environment}
