"""Embedded server for lazy serve command.

Mounts frontend static files on FastAPI so one uvicorn process serves everything.
"""

from pathlib import Path

from fastapi.staticfiles import StaticFiles

from server.main import app

dist_dir = Path(__file__).parent / "frontend_dist"
if dist_dir.exists():
    app.mount("/", StaticFiles(directory=str(dist_dir), html=True), name="frontend")
