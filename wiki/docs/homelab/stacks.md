# :material-layers: Docker Stacks

The homelab is organized into six numbered Docker Compose stacks. Each stack has a root `docker-compose.yml` plus service-specific Compose fragments.

!!! info ":material-source-branch: Source of Truth"
    Service membership below is based on the current `ubuntu_Desktop` repository. Exact image tags and runtime state belong in Compose rather than being duplicated here.

## :material-view-list: Stack Overview

| Stack | Directory | Primary responsibility |
| --- | --- | --- |
| **Networking** | `1-networking/` | Reverse proxy, tunnels, remote access |
| **Security** | `2-security/` | Authentication and threat protection |
| **Monitoring** | `3-monitoring/` | Dashboards, logs, analytics, update monitoring |
| **Media Download** | `4-media-download/` | Requests, indexers, download automation |
| **Media Server** | `5-media-server/` | Plex, metadata, artwork, transcoding |
| **Utilities** | `6-utilities/` | Personal apps, photos, files, docs |

## :material-network: 1-networking

**Current Compose fragments:**

- `proxy.traefik.yml`
- `app.cloudflared.yml`
- `app.tailscaleUbuntu.yml`
- `app.errorpages.yml`
- `app.whoami.yml`

Traefik provides reverse proxy routing, Cloudflared connects selected services through Cloudflare Tunnel, and Tailscale provides private remote access.

## :material-shield-lock: 2-security

**Current Compose fragments:**

- `app.authentik.yml`
- `app.crowdsec.yml`
- `app.anubis.yml`

Authentik handles identity and SSO, CrowdSec analyzes malicious traffic, and Anubis provides bot protection for selected routes.

## :material-monitor-dashboard: 3-monitoring

**Current Compose fragments:**

- `app.beszel.yml`
- `app.dockwatch.yml`
- `app.dozzle.yml`
- `app.homepage.yml`
- `app.tautulli.yml`
- `app.tracearr.yml`

This stack provides the main dashboard, system monitoring, container update visibility, log viewing, and Plex playback analytics.

## :material-download: 4-media-download

**Current Compose fragments:**

- `app.notifiarr.yml`
- `app.prowlarr.yml`
- `app.radarr.yml`
- `app.sabnzbd.yml`
- `app.seerr.yml`
- `app.sonarr.yml`
- `app.starrproxy.yml`

These services cover requests, indexer management, movie and TV automation, Usenet downloads, notifications, and supporting *arr API traffic.

## :material-plex: 5-media-server

**Current Compose fragments include:**

- `app.plex.yml`
- `app.pmm.yml`
- `app.quickstart-pmm.yml`
- `app.imagemaid.yml`
- `app.mediainfo.yml`
- `app.ppm.yml`
- `app.tcm.yml`
- `app.unmanic.yml`

This stack centers on Plex and the tools that manage metadata, artwork, title cards, media information, and library optimization.

## :material-tools: 6-utilities

**Current Compose fragments include:**

- `app.coordinator.yml`
- `app.cutco.yml`
- `app.discord_cleanup.yml`
- `app.filebrowser.yml`
- `app.immich.yml`
- `app.private-bin.yml`
- `app.mkdocs-builder.yml`
- `app.mkdocs-nginx.yml`
- `app.mkdocs.yml`

This stack holds personal applications and general-purpose services, including the infrastructure used to build and serve the wiki and blog.

## :material-console: Managing a Stack

Run Compose commands from the stack directory so its includes and environment are resolved in the same context used by the deployment.

```bash
cd 3-monitoring
docker compose pull
docker compose up -d --remove-orphans
docker compose ps
docker compose logs -f
```

The root `update-all.sh` script can update all six stacks in sequence and optionally rebuild the documentation or locally built images.

!!! warning ":material-file-key: Environment Files"
    Real `.env` files contain deployment-specific configuration and are intentionally excluded from version control. Keep secrets out of Compose files and documentation.

## :material-help-circle: Troubleshooting

If a stack fails to update:

1. Run `docker compose config` from that stack directory.
2. Check `docker compose ps` for unhealthy or exited containers.
3. Inspect the affected service with `docker compose logs -f <service>`.
4. Check Dozzle for cross-stack log inspection.
5. Review the [Troubleshooting guide](../reference/troubleshooting.md).

??? question "Why separate stacks instead of one big Compose file?"
    Isolation and maintainability. Related services can be updated or troubleshot together without turning the entire homelab into one enormous configuration file.
