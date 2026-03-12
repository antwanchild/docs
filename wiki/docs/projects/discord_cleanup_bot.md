# Discord Cleanup Bot

!!! info "Project Status"
    Active — currently at v4.9.x. Hosted on Unraid via Docker, source on GitHub at `antwanchild/discord_cleanup`.

A self-hosted Discord bot that automatically deletes messages from configured channels on a schedule. Built from scratch as a homelab project, it grew from a simple cleanup script into a fully-featured bot with slash commands, statistics tracking, scheduled reports, and a complete CI/CD pipeline.

---

## What It Does

At its core, the bot runs on a configurable schedule and purges messages from Discord channels based on retention rules defined in a YAML config file. Channels can be managed individually or as entire categories, with per-channel retention overrides, exclusions, and optional deep clean for messages older than 14 days (which Discord's bulk delete API won't touch).

Every cleanup run is logged to a date-stamped file and summarised in a Discord embed posted to a designated log channel — complete with per-channel message counts, color-coded by outcome.

---

## Features

### Channel Management

- Clean entire Discord **categories** or individual channels
- Per-channel **retention overrides** — different rules for different channels
- **Exclusions** — mark channels to skip entirely
- **Deep clean** mode for messages older than 14 days using individual deletes
- **Purge** command for on-demand channel wipes

### Scheduling

- Multiple run times per day, fully configurable
- Timezone-aware scheduling via `TZ` environment variable
- Missed run detection — alerts if a scheduled run fires more than 15 minutes late
- Schedule management via slash commands (`/cleanup schedule add`, `remove`, `list`) with live rescheduling, no restart needed
- Discord notification on any schedule change

### Statistics

- Three stat buckets tracked independently: **all-time**, **rolling 30-day**, and **this month**
- Per-channel breakdown with channel names
- Monthly diff reports showing change vs previous month
- Scheduled stat reports posted to a dedicated channel (monthly, weekly, or both)
- `/cleanup stats view` and `/cleanup stats channel` for on-demand lookups
- Stats reset per bucket with confirmation prompt

### Configuration

- All settings managed via `/cleanup config` slash commands
  - Default retention, log level, warn unconfigured, report frequency
- Schedule changes apply immediately in memory and persist to `.env`
- **Export** — `/cleanup export` sends `channels.yml` and `.env.discord_cleanup` as file attachments
- **Import** — `/cleanup import` accepts a file upload and applies changes immediately (token and channel ID changes require restart)
- **Status** — `/cleanup status` shows full config snapshot, uptime, next run time, and channel list

### Notifications

- Deploy notifications on startup showing what changed since the last version the container was running
- Changelog filtering per-user — only shows commits newer than your last pull
- Startup notifications for first run after a fresh deploy
- Missed run alerts
- Schedule change notifications
- Color-coded embeds throughout: green for success, red for errors, purple for stats, blue for info

---

## Architecture

The bot is built on **discord.py** with `discord.ext.tasks` handling scheduling. Configuration lives in `/config` mounted as a Docker volume — `channels.yml` for channel rules and `.env.discord_cleanup` for environment settings. Stats are stored as JSON in `/config/data/`. Logs rotate daily in `/config/logs/`.

The codebase is split into focused modules:

| File | Purpose |
|------|---------|
| `cleanup_bot.py` | Entry point, bot setup, task scheduling |
| `config.py` | Environment loading, default file creation, logging setup |
| `cleanup.py` | Core cleanup logic, bulk/individual delete, channel resolution |
| `commands.py` | Top-level slash commands (`/cleanup run`, `status`, `export`, `import`, etc.) |
| `commands_config.py` | Config and schedule slash commands |
| `commands_stats.py` | Stats slash commands |
| `notifications.py` | All Discord embed notifications including deploy changelog |
| `stats.py` | Stats load, save, update, reset |
| `utils.py` | Health file, uptime, next run time, env file updates, channel reload |

A circular import pattern is handled by a `get_bot()` accessor registered at startup via `register_task()` in `utils.py`.

---

## CI/CD Pipeline

The GitHub Actions pipeline (`docker-publish.yml`) runs on every push to `main` and handles the full release cycle automatically.

### What the pipeline does

1. **Secret scanning** — Gitleaks scans for accidentally committed secrets
2. **Workflow linting** — actionlint checks the workflow file itself
3. **Syntax check** — `py_compile` validates all Python files
4. **Lint and security** — ruff runs with `F` (pyflakes) and `S` (bandit-equivalent security) rule sets
5. **Version bump** — reads the commit message for `#major`, `#minor`, or defaults to patch. Writes the new version, commits it back, and pushes
6. **Changelog generation** — walks git history since the last tag, pairs each auto-bump commit with the commit that triggered it, and writes a `CHANGELOG` file baked into the Docker image
7. **Docker build and push** — builds and pushes to GHCR with `latest` and versioned tags
8. **Vulnerability scan** — Trivy scans the built image for CRITICAL and HIGH CVEs
9. **GitHub Release** — created automatically on minor and major bumps
10. **Cleanup** — old releases and untagged GHCR images pruned to keep the last 10

A separate `notify-discord.yml` workflow fires on completion and posts a success or failure embed to a Discord webhook with version, actor, branch, commit message, duration, and SHA.

### Versioning

Commit message tags control the bump type:

| Tag | Result |
|-----|--------|
| `#major` | `x+1.0.0` |
| `#minor` | `x.y+1.0` |
| _(none)_ | `x.y.z+1` |

---

## Deployment

The bot runs in Docker on Unraid. A `discord_cleanup.xml` Unraid community application template is included in the repo for easy setup through the Unraid UI. Required volumes are `/config` for persistent config and data, and the `TZ` environment variable for correct scheduling.

A `HEALTHCHECK` in the Dockerfile monitors a `/tmp/health` file that the bot updates every minute — if it goes stale, Docker marks the container unhealthy.

---

## Development Notes

This project was built iteratively over many sessions, with each version adding meaningful functionality rather than just refactoring. A few things worth noting for future reference:

- **Circular imports** are avoided by using a `get_bot()` accessor pattern rather than importing the bot instance directly
- **Deep clean** uses individual message deletes rather than bulk delete because Discord's API won't bulk-delete messages older than 14 days
- **Changelog generation** in CI required `fetch-depth: 0` — without full git history the workflow could only see 1-2 commits and the changelog came out empty
- **Schedule rescheduling** uses `discord.ext.tasks` `change_interval()` to apply new times in memory immediately, with the change also persisted to `.env` for restarts
- **Stats migration** moved from channel names to channel IDs as keys to survive channel renames

---

_Part of the antwanchild homelab. Built with discord.py, Docker, and GitHub Actions._
