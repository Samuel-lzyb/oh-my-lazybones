"""Tests for MCP Server module — unit + integration smoke tests."""

import pytest


def test_mcp_module_imports():
    """MCP module imports without errors."""
    from server.mcp import create_mcp_app  # noqa: F401


def test_mcp_app_creates():
    """create_mcp_app returns a valid ASGI app."""
    from server.mcp import create_mcp_app

    app = create_mcp_app()
    assert app is not None
    assert hasattr(app, "routes")


def test_mcp_tools_register():
    """All 6 tools register without errors."""
    from mcp.server.fastmcp import FastMCP

    from server.mcp.tools import register_tools

    mcp = FastMCP("test")
    register_tools(mcp)
    tool_names = {t.name for t in mcp._tool_manager._tools.values()}
    assert tool_names == {
        "search_skills",
        "get_skill",
        "list_categories",
        "install_skill",
        "remove_skill",
        "publish_skill",
    }


def test_mcp_endpoint_mounted():
    """/mcp route is mounted on FastAPI app."""
    from server.main import app

    routes = [r.path for r in app.routes if hasattr(r, "path")]
    assert any("/mcp" in r for r in routes)
