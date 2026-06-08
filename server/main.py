"""oh-my-lazybones API Server."""

from contextlib import asynccontextmanager
from importlib.metadata import version as _package_version

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .config import settings
from .exceptions import LazybonesError, SkillConflictError, SkillNotFoundError

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
from .mcp import create_mcp_app, create_streamable_http_app  # noqa: E402

app.include_router(skills.router)
app.include_router(stats.router)
# MCP: SSE (primary, backward compatible)
app.mount("/mcp", create_mcp_app())
# MCP: StreamableHTTP (Hermes-compatible)
app.mount("/mcp/http", create_streamable_http_app())


@app.exception_handler(LazybonesError)
async def lazybones_exception_handler(request: Request, exc: LazybonesError):
    """Convert LazybonesError hierarchy to HTTP responses."""
    if isinstance(exc, SkillNotFoundError):
        status_code = 404
    elif isinstance(exc, SkillConflictError):
        status_code = 409
    else:
        status_code = 400
    return JSONResponse(
        status_code=status_code,
        content={"code": type(exc).__name__, "message": str(exc)},
    )


@app.get("/api/v1/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": VERSION, "environment": settings.environment}
