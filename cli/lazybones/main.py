"""oh-my-lazybones CLI — lazy command."""

import typer

app = typer.Typer(name="lazy", help="oh-my-lazybones CLI")

# Register commands
from .commands.search import search  # noqa: E402
from .commands.install import install  # noqa: E402
from .commands.serve import serve  # noqa: E402

app.command()(search)
app.command()(install)
app.command()(serve)


def _check_version() -> None:
    """Check PyPI for newer version, warn if available. Non-blocking."""
    try:
        import httpx
        from . import __version__

        resp = httpx.get(
            "https://pypi.org/pypi/oh-my-lazybones/json",
            timeout=3.0,
            follow_redirects=True,
        )
        if resp.status_code != 200:
            return
        latest = resp.json()["info"]["version"]
        if latest != __version__:
            typer.echo(
                f"⚠️  oh-my-lazybones v{latest} is available "
                f"(you have v{__version__}). "
                f"Run: pip install --upgrade oh-my-lazybones",
                err=True,
            )
    except Exception:
        pass  # never block the CLI


@app.callback(invoke_without_command=True)
def version_callback(
    version: bool = typer.Option(
        False, "--version", "-V", help="Show version and exit"
    ),
) -> None:
    """oh-my-lazybones — the marketplace for Agent Skills."""
    if version:
        from . import __version__

        typer.echo(f"oh-my-lazybones v{__version__}")
        _check_version()
        raise typer.Exit()


def main():
    """Entry point for console_scripts."""
    _check_version()
    app()
