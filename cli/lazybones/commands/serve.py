"""lazy serve — start a self-hosted lazybones server."""

import subprocess
import sys
from pathlib import Path

import typer


def serve(port: int = typer.Option(9527, help="Port to listen on")):
    """Start a self-hosted lazybones server with embedded frontend.

    This command starts a single uvicorn process that serves both
    the REST API and the Web UI. No Docker, MySQL, or Meilisearch needed.
    """
    # Check if dist exists
    dist_dir = Path(__file__).parent.parent / "frontend_dist"
    if not (dist_dir / "index.html").exists():
        typer.echo("Building frontend...")
        frontend_dir = Path(__file__).parent.parent.parent.parent / "frontend"
        if frontend_dir.exists():
            subprocess.run(["npm", "ci"], cwd=frontend_dir, check=False)
            subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=False)
            import shutil
            shutil.copytree(frontend_dir / "dist", dist_dir, dirs_exist_ok=True)
        else:
            typer.echo(
                "Frontend not found. Run from the oh-my-lazybones repo root, "
                "or install the full package with 'pip install oh-my-lazybones'.",
                err=True,
            )
            raise typer.Exit(1)

    # Set defaults for self-hosted mode
    import os
    os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///lazybones.db")
    os.environ.setdefault("MEILI_URL", "")  # empty → SQLite search
    os.environ.setdefault("ENVIRONMENT", "selfhosted")

    typer.echo(f"Starting oh-my-lazybones on http://localhost:{port}")
    typer.echo("Press Ctrl+C to stop.")

    # Ensure server package is importable
    repo_root = str(Path(__file__).parent.parent.parent.parent)
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    import uvicorn
    uvicorn.run(
        "lazybones.server:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
