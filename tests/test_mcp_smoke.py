"""MCP smoke test — verifies real SSE connection to a live server.

Run with: lazy serve --port 19527 & && sleep 3 && python tests/test_mcp_smoke.py
"""

import asyncio
import json
import sys

from mcp import ClientSession
from mcp.client.sse import sse_client

MCP_URL = "http://localhost:19527/mcp/sse"


async def main():
    failures = 0

    async with sse_client(MCP_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. List tools — expect 6
            tools = await session.list_tools()
            tool_names = {t.name for t in tools.tools}
            expected = {
                "search_skills", "get_skill", "list_categories",
                "install_skill", "remove_skill", "publish_skill",
            }
            if tool_names == expected:
                print(f"  PASS tools/list: {len(tool_names)} tools")
            else:
                print(f"  FAIL tools/list: got {tool_names}")
                failures += 1

            # 2. Search
            result = await session.call_tool("search_skills", {"query": "test", "limit": 1})
            if len(result.content) > 0:
                print("  PASS search_skills")
            else:
                print("  FAIL search_skills: empty result")
                failures += 1

            # 3. Get skill
            result = await session.call_tool("get_skill", {"name": "selfhosted-test"})
            data = json.loads(result.content[0].text)
            if data.get("name") == "selfhosted-test":
                print("  PASS get_skill")
            else:
                print(f"  FAIL get_skill: {data}")
                failures += 1

            # 4. Categories
            result = await session.call_tool("list_categories", {})
            data = json.loads(result.content[0].text)
            if "categories" in data:
                print(f"  PASS list_categories: {len(data['categories'])} cats")
            else:
                print("  FAIL list_categories")
                failures += 1

            # 5. Publish
            result = await session.call_tool(
                "publish_skill",
                {"name": "smoke-test-mcp", "author": "ci", "description": "MCP smoke test"},
            )
            data = json.loads(result.content[0].text)
            if data.get("action") == "published":
                print("  PASS publish_skill")
            else:
                print(f"  FAIL publish_skill: {data}")
                failures += 1

            # 6. Remove
            result = await session.call_tool("remove_skill", {"name": "smoke-test-mcp"})
            data = json.loads(result.content[0].text)
            if data.get("action") == "removed":
                print("  PASS remove_skill")
            else:
                print(f"  FAIL remove_skill: {data}")
                failures += 1

    if failures:
        print(f"\n{failures} test(s) FAILED")
        sys.exit(1)
    else:
        print("\nAll 6 smoke tests PASSED")


if __name__ == "__main__":
    asyncio.run(main())
