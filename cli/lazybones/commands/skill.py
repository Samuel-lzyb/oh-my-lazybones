"""lazy skill — manage Agent Skills (install, info, search)."""

import asyncio

import typer

from ..client import LazybonesClient

skill_app = typer.Typer(help="Manage Agent Skills")


@skill_app.command(name="install")
def skill_install(name: str):
    """Install a Skill by name."""
    async def _run():
        client = LazybonesClient()
        try:
            skill = await client.get_skill(name)
            typer.echo(f"Installed {skill['name']} v{skill['version']}")
        except Exception:
            typer.echo(f"Error: Skill '{name}' not found.", err=True)
            raise typer.Exit(code=1)
    asyncio.run(_run())


@skill_app.command(name="info")
def skill_info(name: str):
    """Show detailed information about a Skill."""
    async def _run():
        client = LazybonesClient()
        try:
            skill = await client.get_skill(name)
            typer.echo(f"  {skill['name']}  v{skill['version']}")
            typer.echo(f"  Author: {skill.get('author', '')}")
            typer.echo(f"  Downloads: {skill.get('downloads', 0)}")
            if skill.get('description'):
                typer.echo(f"  {skill['description']}")
            if skill.get('tags'):
                typer.echo(f"  Tags: {', '.join(skill['tags'])}")
            if skill.get('depends_on'):
                typer.echo(f"  Depends on: {', '.join(skill['depends_on'])}")
        except Exception:
            typer.echo(f"Error: Skill '{name}' not found.", err=True)
            raise typer.Exit(code=1)
    asyncio.run(_run())
