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

---

## Project Phase

**Current: M4 (User Auth + Paid Skills)** — Starting soon.

| Phase | Goal | Status |
|-------|------|:--:|
| M1 | Repo scaffold + CI + Docs | ✅ |
| M2 | Skill CRUD API + CLI | ✅ |
| M3 | Web UI + Marketplace | ✅ |
| M4 | User Auth + Paid Skills | 📋 |
| M5 | Federation + Community | 📋 |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue 3 + Vite + TypeScript + Tailwind CSS |
| Backend | FastAPI + SQLAlchemy 2.0 |
| DB (dev) | SQLite (aiosqlite) |
| DB (prod) | MySQL 8.0 (Docker) |
| Search | Meilisearch v1.10 (Docker) |
| CI | GitHub Actions (lint + test + CodeQL + frontend build) |
| Deploy | systemd (API) + nginx (SPA) + Docker (infra) |

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
server/          FastAPI (models, schemas, repositories, services, routers)
cli/             Typer CLI (lazy search, lazy install)
deploy/          Docker Compose (MySQL + Meilisearch) + nginx + certs
tests/           pytest (35 tests)
```

## Code Conventions

- **ruff** (line length: 100)
- **Type hints** on all public functions
- **English only** — code, comments, docs, commits
- **Conventional Commits**: `feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`
- **Test**: `PYTHONPATH=. pytest -v` (backend), `npm run build` (frontend)

---

## Agent Roles

| Agent | Responsibility |
|-------|---------------|
| omb-architect | Architecture, PR approval, planning |
| omb-backend | FastAPI, MySQL, Meilisearch |
| omb-cli | lazy command, pip packaging |
| omb-frontend | Vue 3, Tailwind, design system |
| omb-guardian | Code review against review-rules.yml |

## Deployment

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

---

> The process is the product. Follow the workflow. Keep this file up to date.
