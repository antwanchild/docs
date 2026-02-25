---
search:
  boost: 7
---
# :material-home-analytics: Homelab Overview

Single-server self-hosted infrastructure running on Docker with modular stacks for easy management and updates.

**Last Updated:** February 2026

-----

## :material-shield-check: Core Principles

- :material-view-module: **Modularity**:   One stack per logical group with separate directories and Docker networks
- :material-lock: **Security**:   Authentik SSO, CrowdSec protection, Cloudflare tunneling, and Tailscale VPN
- :material-robot: **Automation**:   *arr stack for media acquisition, Kometa/Posterizarr for metadata, ImageMaid for cleanup
- :material-monitor-eye: **Monitoring**:   Homepage dashboard, Tautulli analytics, Dozzle log viewer, Notifiarr notifications
- :material-book-open-variant: **Documentation**:   This wiki! Everything documented and version controlled

!!! success ":material-check-all: All Systems Operational"
    The lab is stable, backed up, and running smoothly!

-----

## :material-server: Hardware

|Component  |Specification                     |
|-----------|----------------------------------|
|**Server** |[Your server model]               |
|**CPU**    |[Processor details]               |
|**RAM**    |[Memory amount]                   |
|**Storage**|[e.g., 4× HDD in RAID + SSD cache]|
|**Network**|[Network setup]                   |

**Remote Access:**

- :material-vpn: Tailscale mesh VPN
- :material-cloud: Cloudflare Tunnel

-----

## :material-layers: Infrastructure Stacks

### :material-network: Networking Stack

**Purpose:** Ingress routing and secure tunneling

|Service    |Role               |
|-----------|-------------------|
|Traefik    |Reverse proxy & SSL|
|Cloudflared|Cloudflare Tunnel  |
|Tailscale  |VPN mesh network   |

**Status:** ✅ Active

-----

### :material-shield-lock: Security Stack

**Purpose:** Authentication and threat protection

|Service             |Role                   |
|--------------------|-----------------------|
|Authentik           |SSO & identity provider|
|Authentik PostgreSQL|Authentication database|
|CrowdSec            |Intrusion prevention   |
|Cloudflare Bouncer  |Edge-level blocking    |

**Status:** 🔒 Secure

-----

### :material-monitor-dashboard: Monitoring Stack

**Purpose:** Dashboards, logging, and oversight

|Service  |Role                |
|---------|--------------------|
|Homepage |Unified dashboard   |
|Dozzle   |Real-time log viewer|
|Tautulli |Plex analytics      |
|Notifiarr|Notification hub    |

**Status:** 👁️ Watching

-----

### :material-download: Media Download Stack

**Purpose:** Automated media acquisition

|Service   |Role              |
|----------|------------------|
|Prowlarr  |Indexer manager   |
|Radarr    |Movie automation  |
|Sonarr    |TV show automation|
|SABnzbd   |Usenet downloader |
|Seerr     |Request interface |
|Notifiarr |Notifications     |
|Starrproxy|API proxy         |

**Status:** 📥 Running

-----

### :material-plex: Media Server Stack

**Purpose:** Media streaming and management

|Service         |Role                |
|----------------|--------------------|
|Plex            |Media server        |
|Kometa          |Metadata manager    |
|Title Card Maker|Custom episode cards|
|Unmanic         |Media transcoding   |
|Posterizarr     |Poster management   |
|ImageMaid       |Image cleanup       |

**Status:** ▶️ Streaming

-----

### :material-tools: Utilities Stack

**Purpose:** Miscellaneous tools and services

|Service   |Role              |
|----------|------------------|
|Immich    |Photo management  |
|Privatebin|Encrypted pastebin|
|These Docs|Documentation wiki|

**Status:** 🔧 Ready

-----

## :material-chart-box: Stack Summary

|Stack             |Services|Networks             |Public Endpoints              |
|------------------|--------|---------------------|------------------------------|
|**networking**    |3       |proxy                |traefik.anthonychild.com      |
|**security**      |4       |security-net, proxy  |auth.anthonychild.com         |
|**monitoring**    |4       |monitoring-net, proxy|home, logs, tautulli          |
|**media-download**|7       |media-backend, proxy |prowlarr, radarr, sonarr, etc.|
|**media-server**  |6       |media-backend, proxy |plex, titlecards, unmanic     |
|**utilities**     |3       |utils-net, proxy     |photos, paste, docs           |

**Total Containers:** 28 | **Active Networks:** 5 | **SSL Certificates:** Auto-managed by Traefik

-----

## :material-file-tree: Directory Structure

```
/opt/homelab/
├── networking/
│   ├── traefik/
│   ├── cloudflared/
│   └── tailscale/
├── security/
│   ├── authentik/
│   └── crowdsec/
├── monitoring/
│   ├── homepage/
│   ├── dozzle/
│   └── tautulli/
├── media-download/
│   ├── prowlarr/
│   ├── radarr/
│   ├── sonarr/
│   └── sabnzbd/
├── media-server/
│   ├── plex/
│   ├── kometa/
│   └── unmanic/
└── utilities/
    ├── immich/
    ├── privatebin/
    └── docs/
```

-----

## :material-link-variant: Quick Links

!!! info "Essential Services"
    - **[Homepage Dashboard]({{ service_url("homepage") }})** - Central hub for all services
    - **[Traefik Dashboard]({{ service_url("traefik") }})** - Routing and SSL status
    - **[Plex]({{ service_url("plex") }})** - Media streaming
    - **[Seerr]({{ service_url("seerr") }})** - Request movies & TV shows

!!! tip "Administration"
    - **[Authentik]({{ service_url("authentik") }})** - Manage users and SSO
    - **[Dozzle]({{ service_url("dozzle") }})** - View container logs
    - **[These Docs]({{ service_url("docs") }})** - You are here!

-----

## :material-file-document-multiple: Documentation

|Page                                                  |Description                            |
|------------------------------------------------------|---------------------------------------|
|**[Services](services.md)**                           |Complete inventory of all 28 containers|
|**[Networking](networking.md)**                       |Network architecture and topology      |
|**[Stacks](stacks.md)**                               |Docker compose stack details           |
|**[Quick Commands](../reference/quick-commands.md)**  |Useful commands reference              |
|**[Troubleshooting](../reference/troubleshooting.md)**|Common issues and fixes                |

-----

## :material-lightbulb-on: Design Decisions

??? question "Why Docker Compose instead of Kubernetes?"
    **Simplicity for single-server setups.** Docker Compose provides all the orchestration needed without the complexity of K8s. Perfect for homelab scale.

??? question "Why separate networks for each stack?"
    **Security through isolation.** Keeps services segmented - media apps can’t directly access security services, monitoring is separate from production, etc.

??? question "Why Authentik over other SSO solutions?"
    **Feature-rich and self-hosted.** Supports LDAP, OAuth2, SAML, has great UI, and integrates well with all services.

??? question "Why Cloudflare Tunnel + Tailscale?"
    **Defense in depth.** Cloudflare Tunnel for public web access with DDoS protection, Tailscale for secure admin access without exposing anything.

-----

## :material-trending-up: Future Plans

See the **[Wishlist](../planning/wishlist.md)** for:

- Planned upgrades
- New services to try
- Infrastructure improvements
- Automation enhancements

-----

## :material-help-circle: Getting Help

!!! tip "Troubleshooting Resources"
    1. Check **[Dozzle logs]({{ service_url("dozzle") }})** for container errors
    2. Review **[Troubleshooting guide](../reference/troubleshooting.md)**
    3. Search this documentation (Press ++f++)
    4. Check service-specific docs in [Services](services.md)

-----

<div class="center" markdown>

**Happy homelabbing!** :material-server-network:

</div>
