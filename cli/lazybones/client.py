"""HTTP client for the lazybones API."""

from typing import Any, Dict

import httpx


class LazybonesClient:
    """Async client for the oh-my-lazybones REST API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

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
