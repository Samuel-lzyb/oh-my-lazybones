"""lazy seed — populate the marketplace with sample Skills."""

import asyncio

import typer

from ..client import LazybonesClient

SEED_SKILLS = [
    {
        "name": "email-digest",
        "version": "1.0.0",
        "author": "lazybones",
        "description": "Summarize today's emails into a morning digest. Supports Gmail and Outlook.",
        "tags": ["email", "productivity"],
        "entrypoint": {"protocol": "shell", "command": "email-digest", "args_template": ["--provider", "{provider}"]},
    },
    {
        "name": "comfyui-image-gen",
        "version": "2.0.0",
        "author": "lazybones",
        "description": "Generate images via ComfyUI Stable Diffusion. MCP Server at http://localhost:8188/mcp.",
        "tags": ["image", "ai", "mcp"],
        "entrypoint": {"protocol": "mcp", "url": "http://localhost:8188/mcp"},
    },
    {
        "name": "code-review-assistant",
        "version": "0.5.0",
        "author": "lazybones",
        "description": "AI-powered code review: finds bugs, suggests improvements, checks style.",
        "tags": ["code", "ai"],
        "entrypoint": {"protocol": "shell", "command": "code-review", "args_template": ["--repo", "{repo_path}"]},
    },
    {
        "name": "weather-reporter",
        "version": "1.0.0",
        "author": "lazybones",
        "description": "Fetch and format weather reports for any city worldwide.",
        "tags": ["data", "utility"],
        "entrypoint": {"protocol": "rest", "url": "http://localhost:8080/api/v1/weather", "method": "GET"},
    },
    {
        "name": "slack-notifier",
        "version": "0.3.1",
        "author": "lazybones",
        "description": "Send rich notifications to Slack channels with custom formatting.",
        "tags": ["notification", "productivity"],
        "entrypoint": {"protocol": "shell", "command": "slack-notify", "args_template": ["--channel", "{channel}", "--message", "{message}"]},
    },
    {
        "name": "pdf-extractor",
        "version": "1.2.0",
        "author": "lazybones",
        "description": "Extract text, tables, and metadata from PDF files.",
        "tags": ["data", "document"],
        "entrypoint": {"protocol": "shell", "command": "pdf-extract", "args_template": ["--input", "{file_path}"]},
    },
    {
        "name": "web-scraper",
        "version": "0.8.0",
        "author": "lazybones",
        "description": "Scrape and extract clean content from any webpage. Returns Markdown.",
        "tags": ["data", "web"],
        "entrypoint": {"protocol": "shell", "command": "web-scrape", "args_template": ["--url", "{url}"]},
    },
]


def seed(base_url: str = typer.Option(None, help="API base URL (default: $LAZY_API_URL or http://localhost:8000)")):
    """Populate the marketplace with sample Skills."""

    async def _run():
        client = LazybonesClient(base_url)  # None → uses env var or default
        created = 0
        skipped = 0

        for skill in SEED_SKILLS:
            try:
                await client.get_skill(skill["name"])
                typer.echo(f"  ⏭  {skill['name']} (already exists)")
                skipped += 1
            except Exception:
                try:
                    await client.create_skill(skill)
                    typer.echo(f"  ✅ {skill['name']}")
                    created += 1
                except Exception as e:
                    typer.echo(f"  ❌ {skill['name']}: {e}", err=True)

        typer.echo(f"\nDone: {created} created, {skipped} skipped, {len(SEED_SKILLS)} total")

    asyncio.run(_run())
