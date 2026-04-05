# Security Policy

## Supported Versions

This is a personal wiki and blog project. Only the latest version on the `main` branch is maintained.

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, report them privately via [GitHub's private vulnerability reporting](https://github.com/antwanchild/docs/security/advisories/new).

I'll acknowledge reports within **7 days** and aim to resolve valid issues within **30 days**. Once fixed, findings will be disclosed publicly in the release notes.

## In Scope

- Secrets or credentials accidentally committed to the repository
- GitHub Actions workflow vulnerabilities (e.g. script injection, privilege escalation)
- Misconfigurations that expose sensitive data in the built Docker images
- Security issues in the deployed sites (wiki.anthonychild.com, blog.anthonychild.com)

## Out of Scope

- Automated scanner reports with no demonstrated real-world impact
- Vulnerabilities in upstream dependencies (report those to the upstream project directly)
- Issues that require physical access to my infrastructure
- Self-XSS or attacks that require the victim to take unlikely actions

## Notes

Credentials and secrets are **never committed** — they are managed via GitHub Actions secrets and local `.env` files excluded by `.gitignore`.
