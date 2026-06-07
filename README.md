# oh-my-lazybones

<p align="center">
  <img src="https://raw.githubusercontent.com/Samuel-lzyb/oh-my-lazybones/main/assets/logo.svg" alt="lazybones sloth logo" width="96" />
</p>

<p align="center">
  <strong>The marketplace for Agent Skills — discover, install, and share.</strong>
</p>

<p align="center">
  <a href="https://github.com/Samuel-lzyb/oh-my-lazybones/actions/workflows/ci.yml"><img src="https://github.com/Samuel-lzyb/oh-my-lazybones/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://lazybone.club"><img src="https://img.shields.io/badge/web-lazybone.club-amber" alt="Web"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
  <a href="https://pypi.org/project/oh-my-lazybones/"><img src="https://img.shields.io/pypi/v/oh-my-lazybones" alt="PyPI"></a>
</p>

---

## Why

Everyone is building AI Agents. But there's one fundamental problem:

> **"I know an Agent can do this for me — but I have no idea where to find the Skill that does it."**

oh-my-lazybones solves this: **discover, install, and share Agent Skills — like npm for Agents.**

---

## Quick Start

```bash
pip install oh-my-lazybones
lazy search "email digest"
lazy install daily-email-digest
```

Or browse at [lazybone.club](https://lazybone.club).

---

## Self-Hosting

Three ways to run your own instance — pick your level:

### 🚀 Tier 1: `lazy serve` (30 seconds)

Zero dependencies beyond Python 3.10. Uses SQLite.

```bash
pip install oh-my-lazybones
lazy serve
# → http://localhost:9527
```

### 📦 Tier 2: Docker (2 minutes)

Pre-built image coming soon to `ghcr.io/samuel-lzyb/oh-my-lazybones`.

```bash
docker pull ghcr.io/samuel-lzyb/oh-my-lazybones:latest
docker run -p 9527:9527 ghcr.io/samuel-lzyb/oh-my-lazybones:latest
```

### 🏭 Tier 3: Docker Compose (5 minutes)

Full production stack with MySQL + Meilisearch.

```bash
git clone https://github.com/Samuel-lzyb/oh-my-lazybones.git
cd oh-my-lazybones
cp .env.example .env
docker compose --profile full up -d
# → http://localhost:9527
```

See `.env.example` for configuration options.

---

## Features

- **Search** — Find Agent Skills by what they do
- **One-command install** — `lazy install <skill>` provisions the Skill locally
- **Web UI** — Browse, search, and publish at lazybone.club
- **Self-hostable** — `lazy serve`, Docker, or Docker Compose
- **Free & Paid** — Community Skills are free; premium Skills coming

---

## Architecture

```
lazybone.club (Vue 3 SPA)
  │ REST /api/v1
api.lazybone.club (FastAPI)
  ├─ MySQL 8.0
  └─ Meilisearch v1.10
```

---

## Roadmap

| Milestone | Focus | Status |
|-----------|-------|--------|
| M1 | Repo scaffold + CI + Docs | ✅ |
| M2 | Skill CRUD API + CLI | ✅ |
| M3 | Web UI + Marketplace | ✅ |
| M4 | Self-hosted deployment | ✅ |
| M5 | Agent-friendly API | 📋 Planned |
| M6 | User Auth + Paid Skills | 📋 Planned |
| M7 | Federation + Community | 📋 Planned |

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Built entirely by AI Agents — see [AI_README.md](./AI_README.md).

- [Bug reports](https://github.com/Samuel-lzyb/oh-my-lazybones/issues/new?template=bug_report.yml)
- [Feature requests](https://github.com/Samuel-lzyb/oh-my-lazybones/issues/new?template=feature_request.yml)
- [Security policy](./SECURITY.md)
- Contact: lzymaster@lazybone.club

## License

MIT © [Samuel-lzyb](https://github.com/Samuel-lzyb)
