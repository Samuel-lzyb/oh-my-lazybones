"""lazy search — find Agent Skills."""

import asyncio

import typer

from ..client import LazybonesClient


def search(query: str):
    """Search for Agent Skills by keyword or description."""

    async def _run():
        client = LazybonesClient()
        try:
            result = await client.search(query)
        except Exception:
            typer.echo("Error: Could not connect to the API server.", err=True)
            raise typer.Exit(code=1)

        items = result.get("items", [])
        if not items:
            typer.echo(f"No skills found for '{query}'.")
            return

        for skill in items:
            typer.echo(
                f"  {skill['name']}  v{skill['version']}"
                f"  ↓{skill.get('downloads', 0)}"
            )
            desc = skill.get("description", "")
            if desc:
                typer.echo(f"  {desc[:100]}")
            typer.echo("")

    asyncio.run(_run())
