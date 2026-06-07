# oh-my-lazybones 🦴

<p align="center">
  <strong>The GitHub for Agent Skills — turn "I don't want to do this" into "Agent already did it."</strong>
</p>

<p align="center">
  <a href="https://github.com/Samuel-lzyb/oh-my-lazybones/actions/workflows/ci.yml"><img src="https://github.com/Samuel-lzyb/oh-my-lazybones/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://api.lazybone.club/api/v1/health"><img src="https://img.shields.io/badge/api-live-green" alt="API"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
</p>

---

## Why

Everyone is building AI Agents. But there's one fundamental problem:

> **"I know an Agent can do this for me — but I have no idea where to find the Skill that does it."**

| What I want | Current reality | Pain |
|-------------|-----------------|------|
| Daily email digest to Slack | Write prompt → debug → wire MCP → deploy | 3 hours minimum |
| Weekly training report from my watch data | Google → copy prompt → wrong data source → give up | No reusable template |
| Auto-reply to Telegram when I'm focused | Someone built this, but where? | Fragmented ecosystem |
| Share my Agent Skill with others | GitHub gist → nobody finds it | No distribution |

oh-my-lazybones solves this: **discover, install, and share Agent Skills — like npm for Agents.**

---

## Quick Start

```bash
# Install
pip install lazybones

# Search for a Skill
lazy search "email digest"

# Install and run in one shot
lazy install daily-email-digest
# → Your Agent now sends a daily email digest every morning at 8 AM
```

**Live API**: `https://api.lazybone.club/api/v1/health`

---

## Features

- 🔍 **Search** — Find Agent Skills by what they do, not by filename
- 📦 **One-command install** — `lazy install <skill>` provisions the Skill locally
- 🆓 **Free & Paid** — Community Skills are free; premium Skills can charge (coming soon)
- 🤖 **AI-native** — Skills are designed for AI Agents (MCP-compatible, self-documenting)
- 🏠 **Self-hostable** — Run your own Skill registry with Docker Compose

---

## Architecture

```
┌──────────────────────────────────────────────┐
│                    CLI                        │
│  lazy search | lazy install                  │
└──────────────────┬───────────────────────────┘
                   │ REST
┌──────────────────▼───────────────────────────┐
│              API Server (FastAPI)             │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │  Search  │  │  Skills  │  │  Health     │  │
│  │ Meilisearch│ │  CRUD   │  │  Check      │  │
│  └──────────┘  └──────────┘  └────────────┘  │
└──────────────────┬───────────────────────────┘
                   │
┌──────────────────▼───────────────────────────┐
│           Storage Layer                       │
│  SQLite (dev) / MySQL 8.0 (prod)             │
└──────────────────────────────────────────────┘
```

---

## Roadmap

| Milestone | Focus | Status |
|-----------|-------|--------|
| M1 | Repo scaffold + CI + Docs | ✅ Done |
| M2 | Skill CRUD API + CLI search/install | ✅ Done |
| M3 | Web UI + Skill publishing | 🚧 Next |
| M4 | Paid Skills + Federation | 📋 Planned |
| M5 | Community + Discord | 📋 Planned |

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for setup and guidelines.

- 🐛 [Bug reports](https://github.com/Samuel-lzyb/oh-my-lazybones/issues/new?template=bug_report.yml)
- 💡 [Feature requests](https://github.com/Samuel-lzyb/oh-my-lazybones/issues/new?template=feature_request.yml)
- 🔒 [Security policy](./SECURITY.md)
- 📧 Contact: lzymaster@lazybone.club

---

## License

MIT © [Samuel-lzyb](https://github.com/Samuel-lzyb)
