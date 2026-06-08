"""Embedded server for lazy serve command.

Mounts frontend static files on FastAPI so one uvicorn process serves everything.

NOTE: lazy serve requires the full oh-my-lazybones source (server/ package).
For pip-installed users, use Docker instead: docker pull ghcr.io/samuel-lzyb/oh-my-lazybones
"""

from pathlib import Path

_MISSING_DEPS_MSG = (
    "Server dependencies not installed. "
    "Run: pip install oh-my-lazybones[server]"
)

_MISSING_SERVER_MSG = (
    "lazy serve requires the full source tree (server/ module not found).\n"
    "Options:\n"
    "  1. Docker:  docker pull ghcr.io/samuel-lzyb/oh-my-lazybones\n"
    "              docker run -p 9527:9527 ghcr.io/samuel-lzyb/oh-my-lazybones\n"
    "  2. Source:  git clone https://github.com/Samuel-lzyb/oh-my-lazybones\n"
    "              cd oh-my-lazybones && pip install -e cli/ && lazy serve"
)

try:
    from fastapi.staticfiles import StaticFiles
except ImportError:
    raise ImportError(_MISSING_DEPS_MSG) from None

try:
    from server.main import app
except ImportError:
    raise ImportError(_MISSING_SERVER_MSG) from None

dist_dir = Path(__file__).parent / "frontend_dist"
if dist_dir.exists():
    app.mount(
        "/", StaticFiles(directory=str(dist_dir), html=True), name="frontend"
    )
