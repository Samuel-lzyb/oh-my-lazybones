"""API integration tests."""

import pytest


@pytest.mark.asyncio
class TestAPI:
    async def test_health(self, client):
        resp = await client.get("/api/v1/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    async def test_create_skill(self, client):
        resp = await client.post(
            "/api/v1/skills",
            json={"name": "api-test", "author": "dev", "tags": ["api"]},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "api-test"
        assert data["id"] is not None

    async def test_create_duplicate_409(self, client):
        await client.post(
            "/api/v1/skills",
            json={"name": "api-dup", "author": "dev"},
        )
        resp = await client.post(
            "/api/v1/skills",
            json={"name": "api-dup", "author": "dev"},
        )
        assert resp.status_code == 409

    async def test_create_invalid_422(self, client):
        resp = await client.post(
            "/api/v1/skills",
            json={"name": "BAD", "author": "dev"},
        )
        assert resp.status_code == 422

    async def test_get_skill(self, client):
        await client.post(
            "/api/v1/skills",
            json={"name": "api-get", "author": "dev"},
        )
        resp = await client.get("/api/v1/skills/api-get")
        assert resp.status_code == 200
        assert resp.json()["name"] == "api-get"

    async def test_get_skill_404(self, client):
        resp = await client.get("/api/v1/skills/nonexistent")
        assert resp.status_code == 404

    async def test_search(self, client):
        await client.post(
            "/api/v1/skills",
            json={"name": "search-me", "author": "dev", "description": "find me"},
        )
        resp = await client.get("/api/v1/skills", params={"q": "find"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 1

    async def test_delete(self, client):
        await client.post(
            "/api/v1/skills",
            json={"name": "api-del", "author": "dev"},
        )
        resp = await client.delete("/api/v1/skills/api-del")
        assert resp.status_code == 204

        resp2 = await client.get("/api/v1/skills/api-del")
        assert resp2.status_code == 404

    async def test_list_pagination(self, client):
        await client.post(
            "/api/v1/skills",
            json={"name": "page-1", "author": "dev"},
        )
        await client.post(
            "/api/v1/skills",
            json={"name": "page-2", "author": "dev"},
        )
        resp = await client.get("/api/v1/skills", params={"limit": 1})
        data = resp.json()
        assert data["limit"] == 1
        assert len(data["items"]) == 1
