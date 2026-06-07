# Changelog

## [0.2.0] - 2026-06-07

### Added
- **Web UI**: Vue 3 + Vite + Tailwind CSS dark-mode marketplace
  - Home page with search, stats, popular/recent skill cards
  - Search page with infinite scroll and sort options
  - Skill detail page with copy-to-clipboard install command
  - Publish page with live preview
  - Responsive layout (mobile/tablet/desktop)
  - Mobile bottom navigation bar
- **Design system**: Chill Geek brand (amber on deep dark, Outfit/Inter fonts, no emojis)
- `/api/v1/stats` endpoint (skills count, authors, total installs)
- Frontend CI workflow (`frontend-ci.yml`)
- DigiCert SSL certificate for lazybone.club

### Changed
- Nginx config: lazybone.club serves Vue SPA, `/api/` proxies to FastAPI
- Review rules: english-only upgraded to error-level, added design-before-code and test-spec-before-code rules

## [0.1.0] - 2026-06-07

### Added
- FastAPI server skeleton with health check endpoint
- CLI skeleton (`lazy` command) with subcommand routing
- CI pipeline: lint (ruff), test (pytest), security (CodeQL), secret scanning
- Issue templates (bug report, feature request)
- Pull request template with AI self-review checklist
- Branch protection rules on `main`
- CODE_OF_CONDUCT.md, SECURITY.md, CONTRIBUTING.md
- MIT license
- Skill CRUD API (POST/GET list/GET detail/DELETE)
- `lazy search` and `lazy install` CLI commands
- Meilisearch integration with abstract SearchService
- Repository pattern (AbstractRepository base class)
- 35 tests (schema, repository, service, API)
- Production deployment: systemd + nginx + Docker (MySQL + Meilisearch)
- Let's Encrypt SSL for api.lazybone.club
- Review rules framework (M1→M4 phased)

[0.2.0]: https://github.com/Samuel-lzyb/oh-my-lazybones/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Samuel-lzyb/oh-my-lazybones/releases/tag/v0.1.0
