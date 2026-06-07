"""oh-my-lazybones API Server."""

from contextlib import asynccontextmanager
from importlib.metadata import version as _package_version

from fastapi import FastAPI

from .config import settings

VERSION = _package_version("oh-my-lazybones")


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[arg-type]
    """Startup: create tables, init search index. Shutdown: no-op."""
    from .database import engine
    from .dependencies import get_search_service
    from .models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Initialize Meilisearch index (best-effort, won't block startup)
    try:
        search = get_search_service()
        await search.ensure_index()
    except Exception:
        pass  # Meilisearch unavailable — search will be a no-op

    yield


app = FastAPI(
    title="oh-my-lazybones API",
    version=VERSION,
    lifespan=lifespan,
)

from .routers import skills, stats  # noqa: E402
from .mcp import create_mcp_app  # noqa: E402

app.include_router(skills.router)
app.include_router(stats.router)
app.mount("/mcp", create_mcp_app())


@app.get("/api/v1/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": VERSION, "environment": settings.environment}
