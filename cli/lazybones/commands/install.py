"""lazy install — install an Agent Skill."""

import asyncio
from pathlib import Path

import typer
import yaml

from ..client import LazybonesClient

INSTALL_DIR = Path.home() / ".lazybones" / "skills"


def install(name: str):
    """Install a Skill by name."""

    async def _run():
        client = LazybonesClient()
        try:
            skill = await client.get_skill(name)
        except Exception:
            typer.echo(
                f"Error: Skill '{name}' not found or API unavailable.", err=True
            )
            raise typer.Exit(code=1)

        target = INSTALL_DIR / name
        target.mkdir(parents=True, exist_ok=True)

        with open(target / "skill.yaml", "w") as f:
            yaml.dump(skill, f)

        typer.echo(f"✅ Installed {name} v{skill['version']}")
        typer.echo(f"   Location: {target}")

    asyncio.run(_run())
