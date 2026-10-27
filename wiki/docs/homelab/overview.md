---
search:
  boost: 7
---
# :material-home-analytics: Homelab Overview

Single-server self-hosted infrastructure running on Ubuntu with Docker Compose and six modular stacks for straightforward management and updates.

!!! info ":material-source-branch: Source of Truth"
    The live Compose configuration in `ubuntu_Desktop` is the source of truth for deployed services. This page intentionally avoids hard-coded container totals so it does not drift as services are added or removed.

## :material-shield-check: Core Principles

- :material-view-module: **Modularity:** One stack per logical group with separate directories and Docker networks
- :material-lock: **Security:** Authentik SSO, CrowdSec protection, Anubis bot protection, Cloudflare tunneling, and Tailscale VPN
- :material-robot: **Automation:** *arr services for media acquisition, Kometa and related tools for metadata and artwork, plus automated maintenance utilities
- :material-monitor-eye: **Monitoring:** Homepage, Beszel, Dockwatch, Dozzle, Tautulli, Tracearr, and Notifiarr
- :material-book-open-variant: **Documentation:** The wiki and blog are version controlled and built with Zensical

## :material-server: Platform

| Component | Current setup |
| --- | --- |
| **Operating system** | Ubuntu |
| **Container runtime** | Docker + Docker Compose |
| **Reverse proxy** | Traefik |
| **External access** | Cloudflare Tunnel |
| **Private remote access** | Tailscale |
| **Authentication** | Authentik |
| **Threat protection** | CrowdSec + Anubis |
| **Documentation** | Zensical wiki + blog |

## :material-layers: Infrastructure Stacks

### :material-network: 1 · Networking

Ingress, routing, tunneling, and remote access. The current stack includes Traefik, Cloudflared, Tailscale, error pages, and a Whoami test service.

### :material-shield-lock: 2 · Security

Authentication and threat protection. The current stack includes Authentik, CrowdSec, and Anubis.

### :material-monitor-dashboard: 3 · Monitoring

Dashboards, logs, analytics, update monitoring, and service health. The current stack includes Beszel, Dockwatch, Dozzle, Homepage, Tautulli, and Tracearr.

### :material-download: 4 · Media Download

Media acquisition and request handling. The current stack includes Notifiarr, Prowlarr, Radarr, SABnzbd, Seerr, Sonarr, and StarrProxy.

### :material-plex: 5 · Media Server

Media serving, metadata, artwork, and optimization. The current configuration includes Plex, Kometa/PMM tooling, ImageMaid, MediaInfo, Poster/Title Card tooling, and Unmanic.

### :material-tools: 6 · Utilities

Personal applications and supporting services. The current configuration includes Coordinator, Cutco Vault, Discord Cleanup, File Browser Quantum, Immich, PrivateBin, and the wiki/blog deployment services.

## :material-file-tree: Repository Structure

```text
ubuntu_Desktop/
├── 1-networking/
├── 2-security/
├── 3-monitoring/
├── 4-media-download/
├── 5-media-server/
└── 6-utilities/
```

Each stack has a root `docker-compose.yml` and service-specific Compose fragments, making individual services easier to maintain without turning the deployment into one giant Compose file.

## :material-link-variant: Quick Links

!!! info "Essential Services"
    - **[Homepage Dashboard]({{ service_url("homepage") }})** - Central hub for services
    - **[Traefik Dashboard]({{ service_url("traefik") }})** - Routing and TLS status
    - **[Plex]({{ service_url("plex") }})** - Media streaming
    - **[Seerr]({{ service_url("seerr") }})** - Media requests

!!! tip "Administration"
    - **[Authentik]({{ service_url("authentik") }})** - Identity and SSO
    - **[Dozzle]({{ service_url("dozzle") }})** - Container logs
    - **[These Docs]({{ service_url("docs") }})** - Wiki

## :material-file-document-multiple: Documentation

| Page | Description |
| --- | --- |
| **[Services](services.md)** | Service inventory and purpose |
| **[Networking](networking.md)** | Network architecture and topology |
| **[Stacks](stacks.md)** | Docker Compose stack details |
| **[Quick Commands](../reference/quick-commands.md)** | Useful commands reference |
| **[Troubleshooting](../reference/troubleshooting.md)** | Common issues and fixes |

## :material-lightbulb-on: Design Decisions

??? question "Why Docker Compose instead of Kubernetes?"
    Docker Compose provides the orchestration this single-server homelab needs without adding Kubernetes complexity.

??? question "Why separate stacks instead of one giant Compose file?"
    Separate stacks keep related services together and make updates, restarts, and troubleshooting more targeted.

??? question "Why use both Cloudflare Tunnel and Tailscale?"
    They solve different access problems: Cloudflare Tunnel handles selected web services, while Tailscale provides private administrative access to the home network.

## :material-trending-up: Future Plans

See the **[Wishlist](../planning/wishlist.md)** for planned upgrades, services to evaluate, infrastructure improvements, and automation ideas.

## :material-help-circle: Getting Help

!!! tip "Troubleshooting Resources"
    1. Check **[Dozzle]({{ service_url("dozzle") }})** for container errors.
    2. Review the **[Troubleshooting guide](../reference/troubleshooting.md)**.
    3. Search this documentation.
    4. Check service-specific information in **[Services](services.md)**.

<div class="center" markdown>

**Happy homelabbing!** :material-server-network:

</div>
