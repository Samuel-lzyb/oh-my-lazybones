# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
