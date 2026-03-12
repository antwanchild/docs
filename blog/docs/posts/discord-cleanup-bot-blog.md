---
date: 2026-03-12
authors:
  - antwanchild
categories:
  - homelab
tags:
  - technology
  - coding
readtime: 8
draft: false
---

# I Built a Discord Bot and It Got Out of Hand

<!-- more -->

It started simple enough. I wanted a bot that would clean up my Discord server automatically — delete old messages from certain channels on a schedule so I didn't have to do it manually. A weekend project. A quick script. Nothing crazy.

That was several versions ago.

What I ended up with is a fully-featured self-hosted Discord bot with slash commands, statistics tracking, scheduled reports, a config export/import system, and a GitHub Actions CI/CD pipeline that handles versioning, changelogs, Docker builds, vulnerability scanning, and Discord deploy notifications. Oh, and it writes a changelog into the Docker image itself so users get notified of what changed when they pull a new version.

So yeah. It got out of hand. In the best way.

---

## How It Started

The initial idea was dead simple — delete messages older than X days from a list of channels. Run it on a cron. Done.

The first real decision was whether to use a simple cron job running a script or an actual persistent Discord bot. I went with the bot approach because I wanted slash commands eventually, and it opened the door to things like on-demand runs and status checks without SSH'ing into the server.

From there it was Python and [discord.py](https://discordpy.readthedocs.io/), running in Docker on Unraid. Configuration lives in a `/config` volume — a `channels.yml` for channel rules and a `.env` file for everything else. That separation turned out to be a good call as the config grew more complex.

---

## The Features That Crept In

Once the basic cleanup loop was working, features started suggesting themselves.

**Category support** came first — instead of listing every channel individually, you could point at a Discord category and clean everything under it. Overrides still worked at the channel level. Exclusions too, for channels you wanted to skip entirely.

**Deep clean** showed up when I realized Discord's bulk delete API has a 14-day limit. Messages older than that have to be deleted one at a time, which is slower but necessary. Deep clean mode handles that automatically.

**Stats** were next. I wanted to know how many messages were being deleted and from which channels. That turned into three separate stat buckets — all-time, rolling 30-day, and monthly — with per-channel breakdowns and monthly diff reports so you could see how this month compared to last.

**Slash commands** for everything. Run cleanup manually, check status, view stats, manage schedule, tweak config — all through Discord without touching config files. Schedule changes even apply live without a restart.

And then the one I'm most pleased with: **config export and import**. `/cleanup export` sends you both config files as Discord attachments. `/cleanup import` accepts a file upload and applies it immediately. It even knows which settings take effect right away versus which ones need a restart.

---

## The CI/CD Pipeline

This is where things got genuinely interesting from a devops perspective.

The GitHub Actions pipeline (`docker-publish.yml`) does a lot:

1. Scans for secrets with **Gitleaks**
2. Lints the workflow itself with **actionlint**
3. Syntax checks all Python files
4. Runs **ruff** with both lint and security rules (replacing separate bandit runs)
5. Bumps the version based on commit message tags (`#major`, `#minor`, or patch by default)
6. Builds and pushes to **GHCR** with versioned and `latest` tags
7. Scans the built image with **Trivy** for CRITICAL and HIGH CVEs
8. Creates a **GitHub Release** on minor and major bumps
9. Prunes old releases and untagged images to keep things tidy

A separate notify workflow fires on completion and posts a success or failure embed to Discord with the version, actor, branch, commit message, duration, and a link to the run.

The versioning is commit-message driven. Tag your commit with `#minor` and you get a minor bump. `#major` for a major bump. Anything else is a patch. Simple and it works well in practice.

---

## The Changelog Problem

The most interesting engineering challenge was the changelog system.

The goal: bake a changelog into the Docker image so the bot can post "here's what changed since your last pull" when it starts up after an update. Per-user, based on what version they were last running.

The tricky part is that the pipeline itself adds a commit — the auto version bump. So by the time the Docker build runs, HEAD is the bump commit, not the real commit that triggered the build.

The solution was to walk git history and pair each auto-bump commit with the commit that immediately preceded it (`SHA~1`). That gives you the real commit message for each version. The triggering commit for the current build gets added manually since it hasn't been paired with a bump commit yet.

This required `fetch-depth: 0` in the checkout step — something that bit me hard. Without full git history the workflow could only see one or two commits and the changelog came out empty every time.

On the bot side, each user's last seen version is stored in `/config/data/last_version`. On startup after a deploy, the bot reads the changelog, filters to only show entries newer than that version, and posts them as a Discord embed. Clean and genuinely useful.

---

## What I Learned

A few things stick out from this project:

**Circular imports are a real problem in larger Python bots.** The fix was a `get_bot()` accessor registered at startup rather than importing the bot instance directly. Ugly but effective.

**Discord's API has more gotchas than you'd expect.** The 14-day bulk delete limit. Rate limits that vary by endpoint. Message fetch limits. Each one required a specific workaround.

**shellcheck and actionlint will find things you didn't know were wrong.** The workflow went through several rounds of fixes for style warnings, bad line breaks, and indentation issues that the linters caught. Annoying in the moment, good in the long run.

**Iterative is the right approach for homelab projects.** Every version added something real. Nothing was built speculatively. The feature list grew because each thing I added made me want the next thing.

---

## Where It Lives

The bot runs in Docker. Config persists in a mounted volume. A healthcheck monitors a timestamped file the bot updates every minute — if it goes stale, Docker knows something's wrong.

Source is at [github.com/antwanchild/discord_cleanup](https://github.com/antwanchild/discord_cleanup) and there's fuller documentation over at [wiki.anthonychild.com](https://wiki.anthonychild.com).

---

It's one of those projects where I'm genuinely glad I kept going past the point where it "worked." The extra miles were worth it.
