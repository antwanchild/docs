---
search:
  boost: 7
---
# :material-server: Services Inventory

A practical inventory of the homelab services grouped by the six Compose stacks in `ubuntu_Desktop`.

!!! info ":material-source-branch: Source of Truth"
    Compose is authoritative for what is deployed. This page focuses on service purpose and access rather than volatile image versions, container counts, or a claim that every configured service is running at this exact moment.

## :material-network: Networking

| Service | Purpose | Access |
| --- | --- | --- |
| **Traefik** | Reverse proxy, routing, TLS, and middleware | Web dashboard / internal routing |
| **Cloudflared** | Cloudflare Tunnel connector | Internal |
| **Tailscale** | Private remote network access | Tailscale |
| **Error Pages** | Friendly proxy error responses | Internal |
| **Whoami** | Routing and middleware test target | Test route |

## :material-shield-lock: Security

| Service | Purpose | Access |
| --- | --- | --- |
| **Authentik** | Identity provider and SSO | <{{ service_url("authentik") }}> |
| **CrowdSec** | Threat detection and blocking decisions | Internal |
| **Anubis** | Bot/challenge protection for selected routes | Routed middleware/service |

!!! tip ":material-shield-check: Layered Protection"
    Traefik is the routing layer. CrowdSec, Anubis, and Authentik can then be applied according to the needs of each route rather than assuming every application has the same exposure model.

## :material-monitor-dashboard: Monitoring

The monitoring stack provides dashboards, logs, analytics, update visibility, and service health.

| Service | Purpose | Access |
| --- | --- | --- |
| **Beszel** | Lightweight system/container monitoring | Web UI |
| **Dockwatch** | Container image/update monitoring | Web UI / notifications |
| **Dozzle** | Live Docker logs | <{{ service_url("dozzle") }}> |
| **Homepage** | Homelab dashboard | <{{ service_url("homepage") }}> |
| **Tautulli** | Plex analytics and history | <{{ service_url("tautulli") }}> |
| **Tracearr** | Plex playback/session tracing and history | Web UI |

## :material-download: Media Download

| Service | Purpose | Access |
| --- | --- | --- |
| **Notifiarr** | Notifications and integrations | <{{ service_url("notifiarr") }}> |
| **Prowlarr** | Indexer management | <{{ service_url("prowlarr") }}> |
| **Radarr** | Movie automation | <{{ service_url("radarr") }}> |
| **SABnzbd** | Usenet downloading | <{{ service_url("sabnzbd") }}> |
| **Seerr** | Media requests | <{{ service_url("seerr") }}> |
| **Sonarr** | TV automation | <{{ service_url("sonarr") }}> |
| **StarrProxy** | Internal *arr proxy component | Internal |

## :material-plex: Media Server

The media-server stack contains Plex plus supporting metadata, artwork, inspection, and optimization tools.

| Service / tool | Purpose | Access |
| --- | --- | --- |
| **Plex** | Media server | <{{ service_url("plex") }}> |
| **Kometa / PMM tooling** | Plex metadata, collections, overlays, and automation | Scheduled/internal |
| **ImageMaid** | Plex image cleanup | Scheduled/internal |
| **MediaInfo** | Media inspection tooling | Internal |
| **Poster / title-card tooling** | Artwork generation and management | Web UI or scheduled, depending on service |
| **Unmanic** | Media transcoding and optimization | <{{ service_url("transcode") }}> |

!!! note ":material-flask: Experimental and Supporting Services"
    The Compose repository can contain supporting or experimental media fragments in addition to the primary services above. Check `5-media-server/` when you need the exact current set.

## :material-tools: Utilities

| Service | Purpose | Access |
| --- | --- | --- |
| **Coordinator** | Personal coordination/automation service | Internal or routed as configured |
| **Cutco Vault** | Cutco collection/catalog application | Web UI |
| **Discord Cleanup** | Scheduled Discord cleanup bot | Discord / internal |
| **File Browser Quantum** | Self-hosted file browser | <{{ service_url("files") }}> |
| **Immich** | Photo backup and management | <{{ service_url("immich") }}> |
| **PrivateBin** | Encrypted paste sharing | <{{ service_url("privatebin") }}> |
| **Wiki / Blog deployment** | Builds and serves the Zensical documentation sites | <{{ service_url("docs") }}> |

## :material-lock-check: Access Patterns

Rather than treating authentication as a single universal rule, services fall into a few patterns:

- **Authentik-protected routes:** browser applications where SSO is appropriate.
- **Application authentication:** services such as Plex or Immich that maintain their own accounts.
- **Internal-only services:** databases, workers, scheduled jobs, and supporting components with no reason to be publicly routed.
- **Middleware/security services:** Traefik, CrowdSec, Anubis, and Authentik participate in protecting other applications.
- **Private administration:** Tailscale provides access when publishing a web route is unnecessary.

## :material-plus-circle: Adding or Removing a Service

When the homelab changes:

1. Make the deployment change in `ubuntu_Desktop` first.
2. Verify the container and any Traefik route or middleware.
3. Add it to Homepage and monitoring where appropriate.
4. Update this page if the service is significant enough to document.
5. Keep exact image tags, ports, mounts, secrets, and network membership in Compose rather than duplicating them here.

## :material-book-open-variant: Related Documentation

- **[Homelab Overview](overview.md)** for the high-level architecture
- **[Networking](networking.md)** for ingress and remote access
- **[Docker Stacks](stacks.md)** for the Compose layout
- **[Quick Commands](../reference/quick-commands.md)** for operational commands
- **[Troubleshooting](../reference/troubleshooting.md)** for common problems

This inventory is intentionally descriptive rather than a second copy of the Compose repository. Fewer duplicated details means fewer stale details. :material-check-circle:
