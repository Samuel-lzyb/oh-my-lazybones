"""HTTP client for the lazybones API."""

import os
from typing import Any, Dict

import httpx

DEFAULT_API_URL = "http://localhost:8000"


class LazybonesClient:
    """Async client for the oh-my-lazybones REST API."""

    def __init__(self, base_url: str | None = None):
        resolved = base_url or os.getenv("LAZY_API_URL") or DEFAULT_API_URL
        self.base_url = resolved.rstrip("/")

    async def search(self, query: str) -> Dict[str, Any]:
        """Search for skills by keyword."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/api/v1/skills", params={"q": query}
            )
            resp.raise_for_status()
            return resp.json()

    async def get_skill(self, name: str) -> Dict[str, Any]:
        """Get a single skill by name."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/api/v1/skills/{name}"
            )
            resp.raise_for_status()
            return resp.json()
