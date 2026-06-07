def test_import():
    """Sanity: package is importable."""
    import lazybones  # noqa: F401


def test_version():
    """Sanity: package has a version."""
    from lazybones import __version__  # noqa: F401
