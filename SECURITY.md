# Security Policy

## Supported Versions

This is a personal wiki and blog project. Only the latest version on the `main` branch is maintained.

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, report them privately via [GitHub's private vulnerability reporting](https://github.com/antwanchild/docs/security/advisories/new).

I'll respond as soon as reasonably possible for a personal project.

## Scope

This repository contains:
- Static site source files (MkDocs/Markdown)
- Docker build configurations
- GitHub Actions workflows

Credentials and secrets are **never committed** — they are managed via GitHub Actions secrets and local `.env` files excluded by `.gitignore`.
