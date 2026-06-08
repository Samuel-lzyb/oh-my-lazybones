# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2] — 2026-06-08

### Fixed
- `lazy serve` clarifies it requires source tree (server/ not in pip package)
- README: Tier 1 now `git clone + pip install -e cli/`, Docker is recommended path
- `setup.py`: uvicorn added to core deps (needed for `lazy serve` import)

## [0.4.1] — 2026-06-08

### Fixed
- `lazy serve` crashes with `ModuleNotFoundError: No module named 'fastapi'` when server deps not installed
- Added `[project.optional-dependencies] server` extras — `pip install oh-my-lazybones[server]`
- Graceful error message: "Run: pip install oh-my-lazybones[server]"

## [0.4.0] — 2026-06-08

### Added
- **Phase 1: Hierarchical exception system**
  - `LazybonesError` base + `SkillNotFoundError` (with Did-you-mean), `SkillConflictError`, `ValidationError`, `SearchBackendError`
  - Global exception handler: typed errors → HTTP JSON responses
  - `suggest_name()`: difflib fuzzy matching for skill names
- **Phase 2: Skill DSL**
  - `depends_on` field: declare Skill dependencies
  - `actions` field: declarative install steps (pip, env, etc.)
  - `freeze()` method: immutable after creation
- **Phase 2: CLI refactor**
  - `lazy skill install <name>` / `lazy skill info <name>` subcommands
  - Old `lazy search` / `lazy install` hidden (backward compatible)
- **Phase 3: Tap system stubs**
  - `TapInfo`, `TapSkill`, `TapRegistry` dataclasses
  - Architecture for M7 Federation (Git-based third-party repos)
- **CI: MCP smoke test** — automated 6-step MCP validation in CI
- **CI: Python 3.10 + 3.12 matrix** — multi-version testing
- **CI: pip-audit** — separate dependency vulnerability scanning
- MCP tools expanded to 6: `get_skill`, `publish_skill`, `remove_skill`
- `scripts/test_full.py`: comprehensive local full-stack test
- **Docker publish workflow** — auto-build + push to ghcr.io on tag
- README slogan: "Laziness, automated."

### Changed
- MCP tools: `ValueError` → typed exceptions with suggestions
- Code audit: DRY fixes, engine reuse, single UPDATE, import cleanup (net -21 lines)
- CI: regression + mcp-smoke failures fixed

### Security
- pip-audit job separated from test (no more silent ignores)

## [0.3.0] — 2026-06-07

### Added
- **M5: MCP Server** — Agent-native skill discovery via SSE
  - `search_skills` tool — programmatic skill search
  - `install_skill` tool — programmatic skill installation
  - `list_categories` tool — discover available categories
  - Mounted at `/mcp/sse` on every deployment (REST + `lazy serve`)
- README: "For Agents" section with Python + TypeScript examples

### Changed
- License: MIT → Apache 2.0 (patent grant + attribution + trademark protection)
- Roadmap updated: M5 = Agent-friendly API, M6 = Auth, M7 = Federation

## [0.2.0] — 2026-06-07

### Added
- Vue 3 SPA (Home, Search, Skill Detail, Publish pages)
- Chill-Geek dark-mode design system
- Responsive layout (mobile/tablet/desktop)
- Auto-label PR workflow
- Test coverage gate (70% threshold)
- Dependency audit (pip-audit, npm audit)
- Production API smoke test in regression
- Hermes cron jobs: issue patrol, stale manager, weekly digest
- 6 seed skills on production marketplace
- GitHub Releases for v0.1.0 and v0.2.0
- Proper CHANGELOG.md (Keep a Changelog format)
- **M4: Self-hosted deployment**
  - `lazy serve` — zero-dependency server (SQLite, no Meilisearch needed)
  - SQLiteSearchService — LIKE-based search fallback
  - Auto-detect search backend (Meilisearch if configured, SQLite otherwise)
  - Multi-stage Dockerfile (Node build + Python runtime)
  - All-in-one Docker Compose with `--profile full` (API + Web + MySQL + Meilisearch)
  - `.env.example` configuration template

### Changed
- Python requirement lowered to 3.10+ (from 3.12)
- Review rules phase bumped to m2
- Stats router uses Repository instead of raw SQL
- Search doc building extracted to `_skill_to_doc()`
- Skill model gained `to_dict()` method
- Search method refactored with early returns
- Self-hosted port standardized to 9527

### Fixed
- CI regression missing `PYTHONPATH=.`
- Favicon file permissions (403)
- Package name changed from `lazybones` to `oh-my-lazybones`
- labeler.yml v5 format

## [0.1.0] — 2026-06-07

### Added
- FastAPI server with health check
- Skill CRUD API (4 endpoints)
- CLI (`lazy search`, `lazy install`) published on PyPI
- Meilisearch integration with abstract SearchService
- Repository pattern with generic base class
- 35 tests (schema, repository, service, API)
- 4-job CI pipeline (lint, test, security, secret-scan)
- Issue and PR templates
- Branch protection on main
- Review rules framework (M1-M4 phases)
- Production deployment: systemd + nginx + Docker

[0.2.0]: https://github.com/Samuel-lzyb/oh-my-lazybones/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Samuel-lzyb/oh-my-lazybones/releases/tag/v0.1.0
