# AI_README.md — Agent Onboarding

<p align="center">
  <img src="https://raw.githubusercontent.com/Samuel-lzyb/oh-my-lazybones/main/assets/logo.svg" alt="lazybones sloth logo" width="72" />
</p>

> **Read this first.** Every AI Agent must read this before touching any code.

---

## What is oh-my-lazybones?

**The marketplace for Agent Skills.** Think `npm` for AI Agents.

| URL | What |
|-----|------|
| `https://lazybone.club` | Web UI (Vue 3 SPA) |
| `https://api.lazybone.club/api/v1/health` | REST API (FastAPI) |
| `http://localhost:9527/mcp/sse` | MCP Server (Agent-native) |

---

## Project Phase

**Current: M5 ✅ → M6 (User Auth + Paid Skills) next.**

| Phase | Goal | Status |
|-------|------|:--:|
| M1 | Repo scaffold + CI + Docs | ✅ |
| M2 | Skill CRUD API + CLI | ✅ |
| M3 | Web UI + Marketplace | ✅ |
| M4 | Self-hosted deployment (`lazy serve`) | ✅ |
| M5 | Agent-friendly API (MCP Server) | ✅ |
| M6 | User Auth + Paid Skills | 📋 |
| M7 | Federation + Community | 📋 |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vite + TypeScript + Tailwind CSS |
| Backend | FastAPI + SQLAlchemy 2.0 |
| MCP | FastMCP SSE Server (Agent-native tool calling) |
| DB (dev) | SQLite (aiosqlite) |
| DB (prod) | MySQL 8.0 (Docker) |
| Search | Meilisearch v1.10 (Docker) or SQLite LIKE fallback |
| CI | GitHub Actions (lint + test + security + secret-scan) |
| Deploy | `lazy serve` (self-hosted) / systemd + nginx (production) |
| License | Apache 2.0 |

---

## Development Iron Laws

| # | Law |
|---|------|
| 1 | Design first. No `design.md` → no approval. |
| 2 | Test spec first. No `test_spec.md` → don't know "done". |
| 3 | Plan first. No `plan.md` → don't know what files to touch. |
| 4 | Minimal PR. One semantic change per PR (≤300 lines). |
| 5 | AI self-review. Every PR includes AI self-review report. |
| 6 | No duplication. Pattern 3× → extract shared module. |
| 7 | Read this file. First action every session. |
| 8 | Regression required. Every feature needs a regression test. |
| 9 | **Update AI_README every milestone.** Part of Definition of Done. |

## Design Philosophy (Frontend)

```
Chill Geek: dark mode (#0D0D1A), amber accents (#F59E0B), Outfit/Inter fonts.
No emojis. No modals. No pagination. No toasts. No registration walls.
Content IS the interface.
```

---

## Project Structure

```
frontend/        Vue 3 SPA (pages + components)
server/
  mcp/           MCP Server (FastMCP + SSE + 3 tools)
  models/        SQLAlchemy ORM models
  schemas/       Pydantic request/response schemas
  repositories/  Data access layer
  services/      Business logic + search (Meilisearch / SQLite)
  routers/       FastAPI route handlers
cli/             Typer CLI (lazy search, lazy install, lazy serve)
deploy/          Docker Compose (MySQL + Meilisearch) + nginx + certs
tests/           pytest (39 tests)
Dockerfile       Multi-stage build (Node + Python)
.env.example     Self-hosted configuration template
```

## Code Conventions

- **ruff** (line length: 100)
- **Type hints** on all public functions
- **English only** — code, comments, docs, commits
- **Conventional Commits**: `feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`
- **Test**: `PYTHONPATH=. pytest -v` (backend), `npm run build` (frontend)
- **Version bump**: Update `__init__.py` + `pyproject.toml` + `setup.py` together

## Key Patterns

### Service instantiation outside FastAPI
MCP tools run outside FastAPI's request context. Use direct service creation, not `Depends()`:
```python
from ..database import engine
from ..repositories.skill import SkillRepository
from sqlalchemy.ext.asyncio import async_sessionmaker

async def _make_registry():
    db = async_sessionmaker(engine)()
    return SkillRegistry(SkillRepository(db), _get_search_service())
```

### Coverage exclusion
Files requiring live server (e.g., MCP tools) are excluded via `.coveragerc`.

---

## Agent Roles

| Agent | Responsibility |
|-------|---------------|
| omb-architect | Architecture, PR approval, planning, milestone review |
| omb-backend | FastAPI, MySQL, Meilisearch, MCP Server |
| omb-cli | `lazy` command, pip packaging, version check |
| omb-frontend | Vue 3, Tailwind, design system |
| omb-guardian | Code review against review-rules.yml |

## Deployment

### Self-hosted (`lazy serve`)
```bash
pip install oh-my-lazybones
lazy serve
# → http://localhost:9527 (REST + MCP + Web UI)
```

### Production
```bash
# API update
git pull && source .venv/bin/activate && pip install -r server/requirements.txt -q
sudo systemctl restart lazybones-api
curl -s https://api.lazybone.club/api/v1/health

# Frontend update
cd frontend && NODE_ENV=development npm install && npm run build
sudo cp -r dist/* /var/www/lazybones-web/
sudo systemctl reload nginx
```

## Environment Notes

- `NODE_ENV=production` on host skips devDependencies → use `NODE_ENV=development npm install`
- DigiCert SSL cert for lazybone.club at `/etc/ssl/certs/lazybone.club.crt`
- API cert (Let's Encrypt) auto-renews via certbot timer
- Self-hosted mode auto-detects: SQLite if no Meilisearch, Meilisearch if configured

---

> The process is the product. Follow the workflow. Keep this file up to date.
