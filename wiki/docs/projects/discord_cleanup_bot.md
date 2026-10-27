# Discord Cleanup Bot

!!! info "Project Status"
    Active and deployed in Docker on the Ubuntu homelab. Source lives in `antwanchild/discord_cleanup`; an Unraid community application template remains available for Unraid users.

A self-hosted Discord bot that automatically deletes messages from configured channels on a schedule. Built from scratch as a homelab project, it grew from a simple cleanup script into a fully featured bot with slash commands, statistics tracking, scheduled reports, and an automated CI/CD pipeline.

## What It Does

At its core, the bot runs on a configurable schedule and purges messages from Discord channels based on retention rules defined in a YAML config file. Channels can be managed individually or as entire categories, with per-channel retention overrides, exclusions, and optional deep clean for messages older than 14 days, which Discord's bulk delete API will not touch.

Every cleanup run is logged to a date-stamped file and summarized in a Discord embed posted to a designated log channel, complete with per-channel message counts and color-coded outcomes.

## Features

### Channel Management

- Clean entire Discord **categories** or individual channels
- Per-channel **retention overrides**
- **Exclusions** for channels that should never be cleaned
- **Deep clean** mode for messages older than 14 days using individual deletes
- **Purge** command for on-demand channel wipes

### Scheduling

- Multiple configurable run times per day
- Timezone-aware scheduling via the `TZ` environment variable
- Missed-run detection
- Schedule management through slash commands with live rescheduling
- Discord notifications when schedules change

### Statistics

- All-time, rolling 30-day, and current-month statistics
- Per-channel breakdowns
- Monthly comparison reports
- Scheduled weekly or monthly reports
- On-demand statistics slash commands

### Configuration

- Settings managed through `/cleanup config` slash commands
- Schedule changes applied in memory and persisted
- Export and import support for configuration files
- Status command for configuration, uptime, next run, and channel information

## Architecture

The bot is built on **discord.py** with `discord.ext.tasks` handling scheduling. Configuration and persistent data live in the `/config` Docker volume.

| File | Purpose |
| --- | --- |
| `cleanup_bot.py` | Entry point, bot setup, task scheduling |
| `config.py` | Environment loading, defaults, logging setup |
| `cleanup.py` | Cleanup logic and channel resolution |
| `commands.py` | Top-level slash commands |
| `commands_config.py` | Configuration and schedule commands |
| `commands_stats.py` | Statistics commands |
| `notifications.py` | Discord notifications and deploy changelog |
| `stats.py` | Statistics persistence and updates |
| `utils.py` | Health, uptime, scheduling helpers, and config updates |

## CI/CD Pipeline

The GitHub Actions release pipeline handles secret scanning, workflow linting, Python validation, Ruff checks, versioning, changelog generation, Docker publishing, vulnerability scanning, and releases.

The published image includes multiple traceability paths:

- semantic version tags
- `latest` for the current release
- a short-SHA image tag for an exact build
- the full commit SHA in the OCI `org.opencontainers.image.revision` label

!!! tip ":material-source-commit: Exact Build Traceability"
    The SHA tag and OCI revision make it possible to connect a running image back to the exact source commit that produced it.

Trivy HIGH and CRITICAL findings are release-blocking while unfixed vulnerabilities remain excluded from the gate.

### Versioning

Commit-message tags control the bump type:

| Tag | Result |
| --- | --- |
| `#major` | next major version |
| `#minor` | next minor version |
| _(none)_ | next patch version |

## Deployment

The current homelab deployment runs in the **6-utilities** stack on Ubuntu using Docker Compose. Persistent configuration is mounted at `/config`, and `TZ` controls scheduling behavior.

The repository also includes a `discord_cleanup.xml` Unraid community application template for users who deploy the bot on Unraid. That template is an alternative deployment method, not the environment used by this homelab.

A Docker health check monitors the bot's health marker and reports the container unhealthy if it becomes stale.

## Development Notes

- Deep clean uses individual deletes because Discord does not bulk-delete messages older than 14 days.
- Full Git history is required for accurate changelog generation in CI.
- Schedule changes are applied without requiring a container restart.
- Statistics use channel IDs so channel renames do not break historical tracking.

*Part of the antwanchild homelab. Built with discord.py, Docker, and GitHub Actions.*
