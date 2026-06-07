"""FastMCP Server — SSE transport for Agent tool calling."""

from mcp.server.fastmcp import FastMCP

from .tools import register_tools

mcp = FastMCP("oh-my-lazybones")


def create_mcp_app():
    """Create an ASGI app for the MCP SSE endpoint.

    Returns a Starlette app that can be mounted on FastAPI.
    """
    register_tools(mcp)
    return mcp.sse_app()
