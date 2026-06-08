"""FastMCP Server — SSE + StreamableHTTP transports for Agent tool calling."""

from mcp.server.fastmcp import FastMCP

from .tools import register_tools


def create_mcp_app():
    """Create an ASGI app for the MCP SSE endpoint."""
    mcp = FastMCP("oh-my-lazybones")
    register_tools(mcp)
    return mcp.sse_app()


def create_streamable_http_app():
    """Create an ASGI app for the MCP StreamableHTTP endpoint."""
    mcp = FastMCP("oh-my-lazybones")
    register_tools(mcp)
    return mcp.streamable_http_app()
