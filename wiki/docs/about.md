---
hide:
  - navigation
---
# :material-home-heart: About This Homelab

Built and maintained by **Anthony Child** since 2024.

This is a single-server Ubuntu homelab built around Docker Compose, modular service stacks, secure remote access, media automation, personal applications, and documentation that lives alongside the infrastructure it describes.

!!! info ":material-source-branch: Living Documentation"
    The homelab changes frequently. The `ubuntu_Desktop` Compose configuration is the source of truth for deployed services, while this wiki explains how the pieces fit together.

## :material-chart-box: Quick Stats

| Category | Details |
| --- | --- |
| **Domain** | anthonychild.com |
| **Operating system** | Ubuntu |
| **Platform** | Docker + Docker Compose |
| **Stacks** | 6 modular stacks |
| **Ingress** | Traefik + Cloudflare Tunnel |
| **Remote access** | Tailscale |
| **Authentication** | Authentik SSO |
| **Security** | CrowdSec + Anubis + Cloudflare |
| **Documentation** | Zensical wiki and blog |

## :material-lightbulb: Philosophy

- :material-view-module: **Modular design:** Related services live in separate Compose stacks for easier maintenance and troubleshooting.
- :material-robot: **Automation first:** Media management, metadata, notifications, updates, and maintenance should require as little repetitive work as practical.
- :material-shield-lock: **Security by design:** Public-facing services sit behind layered routing, authentication, and threat protection.
- :material-file-document-multiple: **Document everything:** Useful decisions, commands, architecture, and troubleshooting notes belong in version control.
- :material-test-tube: **Keep experimenting:** The homelab is both useful infrastructure and a place to learn new tools.

## :material-star-shooting: What Makes This Setup Useful

### :material-network: Network Architecture

Traefik handles reverse proxy routing, Cloudflare Tunnel provides selected external access without conventional inbound port forwarding, and Tailscale provides private remote access to the home network.

### :material-shield-account: Security

Authentik provides SSO, CrowdSec analyzes hostile traffic patterns, Anubis adds bot protection where appropriate, and Cloudflare provides the external edge.

### :material-movie: Media

Plex anchors the media environment, with Sonarr, Radarr, Prowlarr, SABnzbd, Seerr, Kometa, Unmanic, artwork tools, and supporting utilities automating much of the lifecycle.

### :material-monitor-dashboard: Observability

Homepage provides the central dashboard, while Beszel, Dockwatch, Dozzle, Tautulli, Tracearr, and Notifiarr cover system monitoring, image updates, logs, Plex activity, playback analysis, and notifications.

### :material-tools: Personal Services

The utilities stack also hosts projects and services such as Coordinator, Cutco Vault, Discord Cleanup, File Browser Quantum, Immich, PrivateBin, and this documentation.

## :material-timeline: Evolution

**2024 · Initial setup**
:   Plex and the first media automation services established the foundation of the homelab.

**2025 · Security and automation**
:   Traefik, Authentik, CrowdSec, Cloudflare Tunnel, Homepage, Kometa, and additional automation expanded the environment beyond a media server.

**2026 · Ubuntu and documentation modernization**
:   The current environment is organized as six numbered Docker Compose stacks on Ubuntu, with the wiki and blog migrated to Zensical and CI/CD increasingly focused on validation, security, and build traceability.

## :material-server: Technology Stack

### Core Infrastructure

- **Operating system:** Ubuntu
- **Containerization:** Docker + Docker Compose
- **Reverse proxy:** Traefik
- **Tunnel:** Cloudflare Tunnel
- **VPN:** Tailscale

### Security & Authentication

- **SSO:** Authentik
- **Threat detection:** CrowdSec
- **Bot protection:** Anubis
- **Edge protection:** Cloudflare

### Media Services

- **Media server:** Plex
- **TV automation:** Sonarr
- **Movie automation:** Radarr
- **Indexer management:** Prowlarr
- **Downloader:** SABnzbd
- **Requests:** Seerr
- **Metadata:** Kometa
- **Transcoding:** Unmanic

### Monitoring & Management

- **Dashboard:** Homepage
- **System monitoring:** Beszel
- **Container updates:** Dockwatch
- **Logs:** Dozzle
- **Plex analytics:** Tautulli and Tracearr
- **Notifications:** Notifiarr

### Utilities

- **Photos:** Immich
- **Files:** File Browser Quantum
- **Paste sharing:** PrivateBin
- **Personal projects:** Coordinator, Cutco Vault, Discord Cleanup
- **Documentation:** Zensical

## :material-information: About the Documentation

The wiki and blog are Markdown-based Zensical sites built and deployed through Docker and GitHub Actions. They support full-text search, responsive layouts, syntax highlighting, Mermaid diagrams, tabs, and admonitions.

The documentation is deliberately kept in Git so changes to the infrastructure and changes to its documentation can be reviewed and tracked.

## :material-frequently-asked-questions: FAQ

??? question "Why Docker Compose instead of Kubernetes?"
    The homelab is a single-server environment. Compose provides the orchestration needed without introducing infrastructure that would be more complex than the workloads it manages.

??? question "Why self-host?"
    Privacy, control, learning, and the ability to tailor services to the household instead of fitting everything into hosted products.

??? question "Can I copy the setup?"
    Absolutely. Start with the [Homelab Overview](homelab/overview.md), then explore [Services](homelab/services.md), [Networking](homelab/networking.md), and [Stacks](homelab/stacks.md).

## :material-account: About Me

I'm Anthony, a tech enthusiast who enjoys self-hosting, open source software, automation, infrastructure, and documenting the journey. What started as a Plex server has grown into a practical lab for learning, building, and running personal services.

## :material-email: Get in Touch

!!! tip ":material-chat: Contact"
    Found an issue in the docs, have a question about the setup, or want to compare homelab notes? {{ email_link("Feel free to reach out!") }}

<div class="center" markdown>

**Thanks for visiting my digital garden!** :material-sprout:

</div>
