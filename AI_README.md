# AI_README.md — Agent Onboarding

> **Read this first.** Every AI Agent working on this project must read this file before touching any code.

---

## What is oh-my-lazybones?

**The GitHub for Agent Skills.** Think `npm` + `Docker Hub` + `Homebrew` — but for AI Agent Skills.

- Users search for a Skill → `lazy search "email digest"`
- Users install it → `lazy install daily-email-digest`
- Their Agent runs it — every morning, automatically

### Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| CLI | Python (Typer) | `lazy` command, one-shot installs |
| API Server | FastAPI + SQLAlchemy + aiosqlite | Async, typed, lightweight |
| Search | Meilisearch v1.10 | Instant full-text search, self-hosted |
| Auth | python-jose (JWT) | Stateless, standard |
| CI/CD | GitHub Actions | Lint + Test + CodeQL + Regression |

### Project Phase

**Current: M1 (Skeleton)** — CLI + API scaffold, CI pipeline, English docs.

| Phase | Goal |
|-------|------|
| M1 | Scaffold: CLI + API + CI + Docs ✅ **Done** |
| M2 | Functional: Search + Install Skill (CLI + API) |
| M3 | Platform: Web UI + Skill Publishing |
| M4 | Mature: Paid Skills + Federation |
| M5 | Community: Discord + Ecosystem |

---

## Development Iron Laws

These are **non-negotiable**. Every PR is checked against them.

| # | Law | Enforced by |
|---|-----|-------------|
| 1 | **Design first.** No `design.md` → Architect rejects → no coding. | review-rules.yml |
| 2 | **Test spec first.** No `test_spec.md` → don't know what "done" means. | review-rules.yml |
| 3 | **Plan first.** No `plan.md` → don't know which files to touch. | review-rules.yml |
| 4 | **Minimal PR.** One semantic change per PR (≤300 lines). | review-rules.yml |
| 5 | **AI self-review.** Every PR includes an AI self-review report. | PR template |
| 6 | **No duplication.** Same pattern 3× → extract into shared module. | review-rules.yml |
| 7 | **Read this file.** New Agent's first action is reading AI_README.md. | You're doing it. |
| 8 | **Regression required.** Every feature shipped must have a regression test. | regression.yml |

---

## Development Workflow

```
1. PICK an issue (from GitHub Issues)
2. WRITE design.md (use .github/design-template.md)
3. WRITE test_spec.md (use .github/test-spec-template.md)
4. SUBMIT design + test_spec → Architect review
5. ARCHITECT approves → write plan.md → start coding
6. CREATE feat/xxx branch → code → tests → CI green
7. SELF-REVIEW → fill PR template → open PR
8. GUARDIAN review → CI → ACCEPTANCE → merge
9. REGRESSION suite runs automatically on main merge
```

---

## Code Conventions

### Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE`

### Structure
```
server/
├── main.py              # FastAPI app entry point
├── routers/             # API route modules
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic request/response schemas
├── services/            # Business logic
└── requirements.txt     # All dependencies (runtime + test)

cli/
├── lazybones/
│   ├── main.py          # Typer app entry point
│   └── commands/        # Subcommand modules
├── setup.py
└── pyproject.toml

tests/
├── test_*.py            # Unit tests (mirror source structure)
└── conftest.py          # Shared fixtures
```

### Style
- **ruff** for linting (line length: 100)
- **Type hints** on all public functions
- **Docstrings**: Google style for public APIs
- **English only**: code, comments, docs, commit messages
- **Conventional Commits**: `feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`

---

## Quality Gates (per PR)

Every PR must pass:

| Gate | Tool / Check |
|------|-------------|
| Lint | `ruff check server/ cli/` |
| Type check | `mypy` (M2+) |
| Unit tests | `pytest -v` |
| Coverage | `pytest --cov` (M2+) |
| Security scan | CodeQL |
| Secret scan | Git-secrets + `.env` check |
| Regression | `regression.yml` (on merge to main) |
| AI Review | Guardian reads `.github/review-rules.yml` |

---

## Refactoring Cadence

| Frequency | Trigger | Scope | Examples |
|-----------|---------|-------|----------|
| **Every PR** | Code written | Micro (≤30 min) | Extract helper, unify constant name |
| **Every 5 PRs** | Pattern appears 3× | Mini (≤2h) | Extract shared module (e.g., `error_types.py`) |
| **Per milestone** | M1/M2/M3/M4 end | Meso (≤1 day) | Architectural cleanup, API response format |
| **Only with reason** | Overwhelming need | Macro (≤1 week) | Subsystem rewrite, DB migration |

---

## Key Files (must read)

| File | What it is |
|------|-----------|
| `AI_README.md` | This file — start here |
| `.github/review-rules.yml` | Current review phase + rules |
| `.github/design-template.md` | Template for feature design docs |
| `.github/test-spec-template.md` | Template for test specifications |
| `CONTRIBUTING.md` | Dev setup + PR process |
| `README.md` | Public-facing project overview |
| `CHANGELOG.md` | Release history |

---

## Agent Roles

| Agent | Responsibility |
|-------|---------------|
| **omb-architect** | Architecture decisions, PR approval, milestone planning |
| **omb-backend** | FastAPI, Meilisearch, Auth, Database |
| **omb-cli** | `lazy` command, pip packaging, Skill installer |
| **omb-guardian** | Code review against review-rules.yml, security gate |
| **omb-docs** | README, API docs, CHANGELOG, AI_README updates |

---

> **Remember**: This project exists to prove that an open-source product can be built and maintained entirely by AI Agents. The process is the product. Follow the workflow, respect the gates, and keep AI_README.md up to date.
