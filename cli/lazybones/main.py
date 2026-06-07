"""oh-my-lazybones CLI — lazy command."""

import typer

app = typer.Typer(name="lazy", help="oh-my-lazybones CLI")

# Register commands
from .commands.search import search  # noqa: E402
from .commands.install import install  # noqa: E402

app.command()(search)
app.command()(install)


def main():
    """Entry point for console_scripts."""
    app()


if __name__ == "__main__":
    main()
