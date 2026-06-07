#!/usr/bin/env python3
"""Comprehensive local full-stack test — REST + MCP + CLI.

Starts lazy serve, seeds sample skills, runs REST and MCP tests, verifies CLI.
Usage: python scripts/test_full.py
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

import httpx
from mcp import ClientSession
from mcp.client.sse import sse_client

BASE = "http://localhost:19527"
MCP_URL = f"{BASE}/mcp/sse"
FAILURES = 0


def check(name: str, condition: bool, detail: str = ""):
    global FAILURES
    if condition:
        print(f"  ✅ {name}")
    else:
        print(f"  ❌ {name}  {detail}")
        FAILURES += 1


# ═══════════════════════════════════════════════════════
# Phase 1: Seed sample skills via REST
# ═══════════════════════════════════════════════════════

SAMPLE_SKILLS = [
    {
        "name": "daily-email-digest",
        "version": "1.2.0",
        "author": "alice",
        "description": "Summarize today's emails into a digest",
        "tags": ["email", "productivity"],
    },
    {
        "name": "comfyui-image-gen",
        "version": "2.0.0",
        "author": "bob",
        "description": "Generate images via ComfyUI Stable Diffusion",
        "tags": ["image", "ai"],
    },
    {
        "name": "code-review-assistant",
        "version": "0.5.0",
        "author": "carol",
        "description": "AI-powered code review suggestions",
        "tags": ["code", "ai"],
    },
    {
        "name": "weather-reporter",
        "version": "1.0.0",
        "author": "dave",
        "description": "Fetch and format weather reports",
        "tags": ["data", "utility"],
    },
    {
        "name": "slack-notifier",
        "version": "0.3.1",
        "author": "eve",
        "description": "Send notifications to Slack channels",
        "tags": ["notification", "productivity"],
    },
]


async def seed_skills():
    print("\n📦 Phase 1: Seed sample skills via REST")
    async with httpx.AsyncClient(base_url=BASE) as client:
        for s in SAMPLE_SKILLS:
            r = await client.post("/api/v1/skills", json=s)
            check(
                f"POST {s['name']}",
                r.status_code in (201, 409),
                f"status={r.status_code}",
            )

    # Verify stats
    r = await client.get("/api/v1/stats")
    data = r.json()
    check("Stats: skills > 0", data["skills"] > 0, str(data))
    check("Stats: authors > 0", data["authors"] > 0, str(data))
    print(f"  📊 {data['skills']} skills, {data['authors']} authors, {data['installs']} installs")


# ═══════════════════════════════════════════════════════
# Phase 2: REST API verification
# ═══════════════════════════════════════════════════════


async def test_rest():
    print("\n🌐 Phase 2: REST API")
    async with httpx.AsyncClient(base_url=BASE) as client:
        # Health
        r = await client.get("/api/v1/health")
        data = r.json()
        check("Health: status=ok", data["status"] == "ok")
        check("Health: version present", "version" in data)

        # Search
        r = await client.get("/api/v1/skills", params={"q": "email"})
        data = r.json()
        check("Search: returns results", data["total"] > 0, f"total={data['total']}")
        check("Search: pagination", "page" in data and "limit" in data)

        # Get single
        r = await client.get("/api/v1/skills/daily-email-digest")
        check("GET skill: found", r.status_code == 200, f"status={r.status_code}")
        data = r.json()
        check("GET skill: has tags", len(data.get("tags", [])) > 0)

        # Get nonexistent
        r = await client.get("/api/v1/skills/nonexistent-xyz-12345")
        check("GET nonexistent: 404", r.status_code == 404, f"status={r.status_code}")

        # Delete
        r = await client.post(
            "/api/v1/skills",
            json={"name": "tmp-delete-test", "author": "test"},
        )
        skill_name = "tmp-delete-test"
        r = await client.delete(f"/api/v1/skills/{skill_name}")
        check("DELETE: 204", r.status_code == 204, f"status={r.status_code}")
        r = await client.get(f"/api/v1/skills/{skill_name}")
        check("DELETE verify: 404", r.status_code == 404)

        # Stats
        r = await client.get("/api/v1/stats")
        data = r.json()
        check("Stats: has skills", "skills" in data)
        check("Stats: has authors", "authors" in data)
        check("Stats: has installs", "installs" in data)


# ═══════════════════════════════════════════════════════
# Phase 3: MCP tools verification
# ═══════════════════════════════════════════════════════


async def test_mcp():
    print("\n🤖 Phase 3: MCP tools (Agent simulation)")
    async with sse_client(MCP_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 3.1 List tools
            tools = await session.list_tools()
            names = {t.name for t in tools.tools}
            check("MCP: 6 tools", len(names) == 6, f"got {names}")

            # 3.2 search_skills
            r = await session.call_tool("search_skills", {"query": "image"})
            data = json.loads(r.content[0].text)
            check("search_skills: results", len(data) > 0, f"found {len(data)}")

            # 3.3 search_skills with tag
            r = await session.call_tool(
                "search_skills", {"query": "ai", "tags": ["ai"]}
            )
            data = json.loads(r.content[0].text)
            check("search_skills tag filter", len(data) > 0)

            # 3.4 get_skill
            r = await session.call_tool("get_skill", {"name": "daily-email-digest"})
            data = json.loads(r.content[0].text)
            check("get_skill: found", data["name"] == "daily-email-digest")
            check("get_skill: has version", data["version"] == "1.2.0")
            check("get_skill: has tags", len(data["tags"]) > 0)

            # 3.5 get_skill nonexistent
            try:
                r = await session.call_tool("get_skill", {"name": "nope-xyz"})
                check("get_skill nonexistent: error", r.isError, f"got {r.content}")
            except Exception:
                check("get_skill nonexistent: raises", True)  # ValueError → MCP error

            # 3.6 install_skill
            r = await session.call_tool("install_skill", {"name": "weather-reporter"})
            data = json.loads(r.content[0].text)
            check("install_skill: installed", data.get("action") == "installed", str(data))

            # 3.7 list_categories
            r = await session.call_tool("list_categories", {})
            data = json.loads(r.content[0].text)
            check("list_categories: result", len(data["categories"]) > 0, str(data["categories"]))

            # 3.8 publish_skill
            r = await session.call_tool(
                "publish_skill",
                {
                    "name": "test-agent-skill",
                    "version": "0.1.0",
                    "author": "test-agent",
                    "description": "Published by mock agent during full test",
                    "tags": ["test", "mock"],
                },
            )
            data = json.loads(r.content[0].text)
            check("publish_skill: published", data.get("action") == "published", str(data))

            # 3.9 publish_skill duplicate
            try:
                r = await session.call_tool(
                    "publish_skill",
                    {"name": "test-agent-skill", "author": "test-agent"},
                )
                check("publish_skill duplicate: error", r.isError, str(r.content))
            except Exception:
                check("publish_skill duplicate: raises", True)

            # 3.10 remove_skill
            r = await session.call_tool("remove_skill", {"name": "test-agent-skill"})
            data = json.loads(r.content[0].text)
            check("remove_skill: removed", data.get("action") == "removed")

            # 3.11 remove_skill nonexistent
            try:
                r = await session.call_tool("remove_skill", {"name": "test-agent-skill"})
                check("remove_skill gone: error", r.isError, str(r.content))
            except Exception:
                check("remove_skill gone: raises", True)


# ═══════════════════════════════════════════════════════
# Phase 4: CLI verification
# ═══════════════════════════════════════════════════════


def test_cli():
    print("\n🖥️  Phase 4: CLI")
    env = {"LAZY_API_URL": BASE, "PATH": "/usr/local/bin:/usr/bin:/bin"}

    r = subprocess.run(["lazy", "--version"], capture_output=True, text=True, env=env)
    check("lazy --version", "oh-my-lazybones" in r.stdout, r.stdout.strip())

    r = subprocess.run(
        ["lazy", "search", "email"], capture_output=True, text=True, env=env
    )
    check("lazy search email", "daily-email-digest" in r.stdout, r.stdout.strip())

    r = subprocess.run(
        ["lazy", "search", "nonexistent-xyz"], capture_output=True, text=True, env=env
    )
    check("lazy search no results", "No skills found" in r.stdout or r.returncode == 0)


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════


async def main():
    global FAILURES

    # Wait for server to be ready
    print("⏳ Waiting for server...")
    for _ in range(10):
        try:
            async with httpx.AsyncClient() as c:
                r = await c.get(f"{BASE}/api/v1/health", timeout=2)
                if r.status_code == 200:
                    break
        except Exception:
            pass
        time.sleep(1)
    else:
        print("❌ Server did not start")
        sys.exit(1)

    await seed_skills()
    await test_rest()
    await test_mcp()
    test_cli()

    print(f"\n{'='*50}")
    if FAILURES:
        print(f"❌ {FAILURES} test(s) FAILED")
        sys.exit(1)
    else:
        print("✅ All tests PASSED")
        print(f"   REST: ✅ | MCP: ✅ | CLI: ✅")
        print(f"   {len(SAMPLE_SKILLS)} skills seeded, 6 MCP tools verified")


if __name__ == "__main__":
    asyncio.run(main())
