# oh-my-lazybones

<p align="center"><em>Laziness, automated.</em></p>

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
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue" alt="License"></a>
  <a href="https://pypi.org/project/oh-my-lazybones/"><img src="https://img.shields.io/pypi/v/oh-my-lazybones?cacheSeconds=3600" alt="PyPI"></a>
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
pip install oh-my-lazybones[server]
lazy serve
# → http://localhost:9527 (REST + MCP + Web UI)
```

### 📦 Tier 2: Docker (2 minutes)

Pre-built image at `ghcr.io/samuel-lzyb/oh-my-lazybones`.

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
- **Agent-native** — MCP Server endpoint for programmatic discovery

---

## For Agents

Connect any MCP-compatible Agent to discover Skills programmatically:

```python
from mcp import ClientSession
from mcp.client.sse import sse_client

async with sse_client("http://localhost:9527/mcp/sse") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()

        # Search for Skills
        result = await session.call_tool("search_skills", {"query": "image"})

        # Install a Skill
        await session.call_tool("install_skill", {"name": "comfyui-skill"})
```

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

const client = new Client({ name: "my-agent", version: "1.0.0" });
await client.connect(new SSEClientTransport(
  new URL("http://localhost:9527/mcp/sse")
));
const result = await client.callTool({
  name: "search_skills",
  arguments: { query: "email digest" }
});
```

Available tools: `search_skills`, `get_skill`, `list_categories`, `install_skill`, `remove_skill`, `publish_skill`.

---

## Architecture

```
lazybone.club (Vue 3 SPA)
  │ REST /api/v1   │ SSE /mcp/sse (Agent-native)
api.lazybone.club (FastAPI + MCP Server)
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
| M5 | Agent-friendly API | ✅ |
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

Apache 2.0 © [Samuel-lzyb](https://github.com/Samuel-lzyb)
