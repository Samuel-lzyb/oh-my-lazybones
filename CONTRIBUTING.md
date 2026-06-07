# Contributing to oh-my-lazybones

Thanks for your interest in contributing! This guide will help you get set up.

---

## Development Setup

```bash
# Clone the repo
git clone git@github.com:Samuel-lzyb/oh-my-lazybones.git
cd oh-my-lazybones

# Create a .env file (copy from template)
cp .env.example .env

# Install dependencies
pip install -r server/requirements.txt
pip install -e cli/

# Run tests to verify your setup
pytest -v
```

---

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add skill search by category
fix: Correct MCP config path on install
docs: Update README with architecture diagram
refactor: Extract search logic into separate module
test: Add integration tests for skill install
chore: Update ruff configuration
```

---

## Pull Request Process

1. **Fork** the repository
2. Create a **feature branch** from `main` (`git checkout -b feat/my-feature`)
3. Write your code — include **tests** for new functionality
4. Run the full check locally:

   ```bash
   ruff check server/ cli/
   pytest -v
   ```

5. Commit following the [convention](#commit-convention)
6. Push and open a **Pull Request** using the PR template
7. Ensure **CI is green** (lint + test + security scan)
8. Wait for review — an AI will do a first-pass, then a maintainer will merge

---

## Code Style

- **Python**: Formatted with [ruff](https://docs.astral.sh/ruff/)
- **Line length**: 100 characters
- **Type hints**: Required for all public functions
- **Docstrings**: Google style for public APIs
- **Language**: All code, comments, and docs are in **English**

---

## Project Structure

```
oh-my-lazybones/
├── cli/                    # CLI tool (lazy command)
│   ├── lazybones/          # Python package
│   │   ├── commands/       # CLI subcommands
│   │   ├── main.py         # Entry point
│   │   └── __init__.py
│   ├── setup.py
│   └── pyproject.toml
├── server/                 # FastAPI backend
│   ├── main.py             # App entry point
│   └── requirements.txt
├── tests/                  # Test suite
├── .github/                # CI + Issue/PR templates
│   ├── workflows/ci.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
└── README.md
```

---

## Questions?

Open a [GitHub Discussion](https://github.com/Samuel-lzyb/oh-my-lazybones/discussions) or check existing issues.
