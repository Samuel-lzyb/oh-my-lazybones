"""MCP Server for oh-my-lazybones — Agent-native skill discovery."""

from .server import create_mcp_app, create_streamable_http_app

__all__ = ["create_mcp_app", "create_streamable_http_app"]
