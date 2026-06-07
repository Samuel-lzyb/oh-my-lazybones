"""Tests for MCP Server module — Agent-native skill discovery."""

import pytest


def test_mcp_module_imports():
    """T0: MCP module imports without errors."""
    from server.mcp import create_mcp_app  # noqa: F401


def test_mcp_app_creates():
    """T0: create_mcp_app returns a valid ASGI app."""
    from server.mcp import create_mcp_app

    app = create_mcp_app()
    assert app is not None
    assert hasattr(app, "routes")


def test_mcp_tools_register():
    """T0: Tools register without errors."""
    from mcp.server.fastmcp import FastMCP

    from server.mcp.tools import register_tools

    mcp = FastMCP("test")
    register_tools(mcp)
    # Verify tools are registered by checking the tool store
    assert len(mcp._tool_manager._tools) == 3


def test_mcp_endpoint_mounted():
    """T11: /mcp route is mounted on FastAPI app."""
    from server.main import app

    routes = [r.path for r in app.routes]
    assert any("/mcp" in r for r in routes)
