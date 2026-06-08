"""Embedded server for lazy serve command.

Mounts frontend static files on FastAPI so one uvicorn process serves everything.
Requires server dependencies: pip install oh-my-lazybones[server]
"""

from pathlib import Path

_MISSING_DEPS_MSG = (
    "Server dependencies not installed. "
    "Run: pip install oh-my-lazybones[server]"
)

try:
    from fastapi.staticfiles import StaticFiles
except ImportError:
    raise ImportError(_MISSING_DEPS_MSG) from None

try:
    from server.main import app
except ImportError:
    raise ImportError(_MISSING_DEPS_MSG) from None

dist_dir = Path(__file__).parent / "frontend_dist"
if dist_dir.exists():
    app.mount(
        "/", StaticFiles(directory=str(dist_dir), html=True), name="frontend"
    )
