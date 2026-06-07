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
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
</p>

---

## Why

Everyone is building AI Agents. But there's one fundamental problem:

> **"I know an Agent can do this for me — but I have no idea where to find the Skill that does it."**

oh-my-lazybones solves this: **discover, install, and share Agent Skills — like npm for Agents.**

---

## Quick Start

```bash
pip install lazybones
lazy search "email digest"
lazy install daily-email-digest
```

Or browse at [lazybone.club](https://lazybone.club).

---

## Features

- **Search** — Find Agent Skills by what they do
- **One-command install** — `lazy install <skill>` provisions the Skill locally
- **Web UI** — Browse, search, and publish at lazybone.club
- **Free & Paid** — Community Skills are free; premium Skills coming
- **Self-hostable** — Docker Compose, single-host deploy

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
| M4 | User Auth + Paid Skills | 📋 Next |
| M5 | Federation + Community | 📋 Planned |

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Built entirely by AI Agents — see [AI_README.md](./AI_README.md).

- [Bug reports](https://github.com/Samuel-lzyb/oh-my-lazybones/issues/new?template=bug_report.yml)
- [Feature requests](https://github.com/Samuel-lzyb/oh-my-lazybones/issues/new?template=feature_request.yml)
- [Security policy](./SECURITY.md)
- Contact: lzymaster@lazybone.club

## License

MIT © [Samuel-lzyb](https://github.com/Samuel-lzyb)
