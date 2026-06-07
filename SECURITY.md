# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in oh-my-lazybones,
please **DO NOT** open a public issue.

Email: security@lazybones.club

We will respond within 48 hours.

## Sensitive Data Policy

- All secrets (passwords, API keys, tokens) MUST be stored in `.env`, never in code
- `.env` MUST be in `.gitignore`
- Use `.env.example` as the documented template
- Pre-commit hooks scan for accidentally committed secrets