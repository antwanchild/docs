---
search:
    boost: 7
---
# :material-server: Services Inventory

Complete inventory of all running containers with access information and purpose.

-----

## :material-view-dashboard: Quick Reference Table

|Service         |Purpose           |URL                             |Auth         |Status|
|----------------|------------------|--------------------------------|-------------|------|
|Authentik       |SSO Provider      |<{{ service_url("authentik") }}>  |Provider     |✅     |
|Authentik DB    |PostgreSQL Backend|Internal                        |None         |🗄️     |
|Cloudflared     |CF Tunnel         |Internal                        |CF Zero Trust|🔒     |
|CrowdSec        |IPS               |Internal                        |None         |🛡️     |
|Dozzle          |Log Viewer        |<{{ service_url("dozzle") }}>     |Authentik    |📜     |
|File Browser Quantum | Self Hosted File Browser|<{{ service_url("files") }}>| Authentik        | 🗄    |
|Homepage        |Dashboard         |<{{ service_url("homepage") }}>   |Authentik    |🏠     |
|ImageMaid       |Image Cleanup     |Internal                        |None         |🧹     |
|Immich          |Photos            |<{{ service_url("immich") }}>     |Immich       |📸     |
|Kometa          |Plex Metadata     |Internal/Scheduled              |None         |🎭     |
|Notifiarr       |Notifications     |<{{ service_url("notifiarr") }}>  |Authentik    |🔔     |
|Plex            |Media Server      |<{{ service_url("plex") }}>       |Plex         |🎬     |
|Posterizarr     |Poster Manager    |<{{ service_url("posterizarr") }}>|Authentik    |🖼️     |
|Privatebin      |Encrypted Paste   |<{{ service_url("privatebin") }}> |None         |🔐     |
|Prowlarr        |Indexer Manager   |<{{ service_url("prowlarr") }}>   |Authentik    |🔍     |
|Radarr          |Movie Manager     |<{{ service_url("radarr") }}>     |Authentik    |🍿     |
|SABnzbd         |Usenet Client     |<{{ service_url("sabnzbd") }}>    |Authentik    |📥     |
|Seerr           |Media Requests    |<{{ service_url("seerr") }}>      |Authentik    |🎟️     |
|Sonarr          |TV Manager        |<{{ service_url("sonarr") }}>     |Authentik    |📺     |
|Starrproxy      |*arr Proxy        |Internal                        |None         |🔗     |
|Tailscale       |VPN Mesh          |Internal                        |Tailscale    |🌐     |
|Tautulli        |Plex Analytics    |<{{ service_url("tautulli") }}>   |Authentik    |📊     |
|These Docs      |Wiki              |<{{ service_url("docs") }}>       |Authentik    |📚     |
|Title Card Maker|Custom Cards      |<{{ service_url("titlecards") }}> |Authentik    |🎴     |
|Traefik         |Reverse Proxy     |<{{ service_url("traefik") }}>    |Authentik    |🚦     |
|Unmanic         |Transcoder        |<{{ service_url("transcode") }}>  |Authentik    |⚙️     |

!!! success ":material-check-all: All Systems Operational"
    All services are running normally as of {{ now().strftime('%Y-%m-%d') }}

-----

## :material-shield-account: Infrastructure & Security

### :material-account-key: Authentik

**SSO authentication & identity provider**

- **URL:** <{{ service_url("authentik") }}>
- **Authentication:** Master login (protects all other services)
- **Purpose:** Single Sign-On for the entire homelab
- **Features:**
  - LDAP/OAuth2/SAML support
  - Multi-factor authentication
  - User & group management
  - Application proxy

!!! danger ":material-shield-alert: Master Auth System"
    This is your primary authentication - secure it with a strong password and enable MFA!

-----

### :material-database: Authentik PostgreSQL

**Database backend for Authentik**

- **Access:** Internal only
- **Purpose:** Stores Authentik configuration and user data
- **Backup:** Included in Docker volume backups

-----

### :material-cloud-lock: Cloudflared

**Cloudflare Tunnel for secure external access**

- **Access:** Internal daemon
- **Purpose:** Secure tunnel to Cloudflare without open ports
- **Authentication:** Cloudflare Zero Trust
- **Features:**
  - No inbound firewall rules needed
  - Automatic HTTPS
  - DDoS protection via Cloudflare

-----

### :material-shield: CrowdSec

**Collaborative intrusion prevention system**

- **Access:** Internal (no web UI)
- **Purpose:** Analyzes logs and blocks malicious IPs
- **Features:**
  - Community-driven threat intelligence
  - Real-time ban decisions
  - Integration with Cloudflare
  - Traefik log parsing

!!! info ":material-information: How It Works"
    CrowdSec reads Traefik logs, detects attacks, and automatically blocks threats at the edge via Cloudflare.

-----

### :material-router: Traefik

**Reverse proxy & ingress controller**

- **URL:** <{{ service_url("traefik") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Routes all web traffic and manages SSL certificates
- **Features:**
  - Automatic Let’s Encrypt certificates
  - Dynamic Docker label configuration
  - Dashboard for monitoring routes
  - Middleware for auth & rate limiting

!!! warning ":material-alert: Never Expose Unprotected"
    Always keep the Traefik dashboard behind authentication!

-----

### :material-vpn: Tailscale

**Mesh VPN for secure remote access**

- **Access:** Internal / Tailscale network
- **Authentication:** Tailscale account
- **Purpose:** Secure remote access without exposing services
- **Features:**
  - Zero-config VPN
  - Device-to-device encryption
  - ACLs for access control
  - Exit nodes

-----

## :material-monitor-dashboard: Monitoring & Management

### :material-view-dashboard: Homepage

**Unified homelab dashboard**

- **URL:** <{{ service_url("homepage") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Central hub for all services with status monitoring
- **Features:**
  - Service status widgets
  - System resource monitoring
  - Quick links to all apps
  - Custom integrations

-----

### :material-text-box-search: Dozzle

**Real-time Docker log viewer**

- **URL:** <{{ service_url("dozzle") }}>
- **Authentication:** Authentik SSO
- **Purpose:** View live logs from all containers
- **Features:**
  - Multi-container view
  - Search & filter
  - Log streaming
  - No database required

!!! tip ":material-lightbulb: Troubleshooting First Stop"
    Check Dozzle logs first when debugging any container issues!

-----

### :material-chart-line: Tautulli

**Plex media server analytics**

- **URL:** <{{ service_url("tautulli") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Monitor Plex usage and generate reports
- **Features:**
  - Watch history
  - User statistics
  - Play state monitoring
  - Newsletter generation
  - Discord/Slack notifications

-----

### :material-bell-ring: Notifiarr

**Unified notification hub**

- **URL:** <{{ service_url("notifiarr") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Centralized notifications for *arr apps and Plex
- **Features:**
  - Discord integration
  - Webhook support
  - Custom triggers
  - Health monitoring

-----

## :material-movie: Media Stack

### :material-plex: Plex

**Media streaming server**

- **URL:** <{{ service_url("plex") }}>
- **Authentication:** Plex account
- **Purpose:** Stream movies and TV shows
- **Features:**
  - Transcoding
  - Remote access
  - Mobile apps
  - User management
  - Live TV & DVR

-----

### :material-palette: Kometa

**Plex metadata & collection manager**

- **Access:** Scheduled runs (no web UI)
- **Purpose:** Automated Plex library management
- **Features:**
  - Smart collections
  - Metadata overlays
  - Poster management
  - Scheduled automation

-----

### :material-broom: ImageMaid

**Plex image optimization**

- **Access:** Scheduled runs (no web UI)
- **Purpose:** Clean up and optimize Plex library images
- **Features:**
  - Remove duplicate images
  - Optimize file sizes
  - Clean metadata cache

-----

### :material-card-text: Title Card Maker

**Custom episode title cards**

- **URL:** <{{ service_url("titlecards") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Generate custom title cards for TV episodes
- **Features:**
  - Template management
  - Automated generation
  - Integration with Plex

-----

### :material-image-frame: Posterizarr

**Poster management for *arr apps**

- **URL:** <{{ service_url("posterizarr") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Manage and sync posters across Sonarr/Radarr
- **Features:**
  - Bulk poster updates
  - Custom poster sources
  - Automated syncing

-----

## :material-download: Media Acquisition

### :material-ticket: Seerr

**Media request management**

- **URL:** <{{ service_url("seerr") }}>
- **Authentication:** Authentik SSO
- **Purpose:** User-facing media request interface
- **Features:**
  - Browse & request movies/TV
  - Approval workflow
  - Integration with Radarr/Sonarr
  - Discord notifications

-----

### :material-television: Sonarr

**TV show automation**

- **URL:** <{{ service_url("sonarr") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Automated TV episode management
- **Features:**
  - Episode monitoring
  - Quality profiles
  - Calendar view
  - Automatic upgrades

-----

### :material-movie: Radarr

**Movie automation**

- **URL:** <{{ service_url("radarr") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Automated movie management
- **Features:**
  - Movie monitoring
  - Quality profiles
  - Collection management
  - Import lists

-----

### :material-file-search: Prowlarr

**Indexer management**

- **URL:** <{{ service_url("prowlarr") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Centralized indexer configuration for *arr apps
- **Features:**
  - Sync to Sonarr/Radarr
  - Indexer testing
  - Statistics tracking
  - Category mapping

-----

### :material-download: SABnzbd

**Usenet downloader**

- **URL:** ><{{ service_url("sabnzbd") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Download and process Usenet content
- **Features:**
  - NZB queue management
  - Automatic unpacking
  - Category-based organization
  - Speed limiting

-----

### :material-api: Starrproxy

***arr API proxy**

- **Access:** Internal (no web UI)
- **Purpose:** Secure proxy for *arr application API calls
- **Features:**
  - API request filtering
  - Load balancing
  - Security layer

-----

## :material-tools: Utilities

### :material-image-multiple: Immich

**Self-hosted photo management**

- **URL:** <{{ service_url("immich") }}>
- **Authentication:** Immich account
- **Purpose:** Photo backup and management
- **Features:**
  - Mobile auto-backup
  - Facial recognition
  - Album management
  - Machine learning tagging
  - Sharing

!!! tip ":material-cellphone: Mobile App Available"
    Install the Immich mobile app for automatic photo backup from your phone!

-----

### :material-note-text-outline: Privatebin

**Encrypted pastebin**

- **URL:** <{{ service_url("privatebin") }}>
- **Authentication:** None (public)
- **Purpose:** Secure, temporary text/file sharing
- **Features:**
  - End-to-end encryption
  - Burn after reading
  - Password protection
  - Expiration times

!!! info ":material-information: Use Cases"
    Perfect for sharing passwords, config snippets, or sensitive information securely.

-----

### :material-video-box: Unmanic

**Media transcoding & optimization**

- **URL:** <{{ service_url("transcode") }}>
- **Authentication:** Authentik SSO
- **Purpose:** Automated media library transcoding
- **Features:**
  - Library optimization
  - Format conversion
  - Plugin system
  - Queue management

-----

### :material-book-open-page-variant: These Docs

**Homelab documentation**

- **URL:** <{{ service_url("docs") }}>
- **Authentication:** Authentik SSO
- **Purpose:** This wiki you’re reading!
- **Features:**
  - Markdown-based
  - Material theme
  - Full-text search
  - Version controlled

-----

## :material-information: Service Categories

### Backend Services (No Web UI)

These services run in the background without a web interface:

- **Authentik PostgreSQL** - Database
- **Cloudflared** - Tunnel daemon
- **CrowdSec** - Security monitor
- **ImageMaid** - Scheduled cleanup
- **Kometa** - Scheduled metadata
- **Starrproxy** - API proxy
- **Tailscale** - VPN daemon

### Public Access (No Auth Required)

These services are accessible without authentication:

- **Privatebin** - Encrypted paste sharing

!!! warning ":material-alert: Public Services"
    Only Privatebin is intentionally public. All other services require authentication.

### Protected by Authentik SSO

Most services use Authentik for single sign-on:

- Dozzle, Homepage, Notifiarr, Posterizarr, Prowlarr, Radarr, SABnzbd, Seerr, Sonarr, Tautulli, Title Card Maker, Traefik, Unmanic, These Docs

### Separate Authentication

These services have their own auth systems:

- **Plex** - Plex account
- **Immich** - Local Immich account
- **Tailscale** - Tailscale account

-----

## :material-plus-circle: Adding New Services

When deploying a new container:

!!! tip ":material-clipboard-check: Deployment Checklist"
    - [ ] Create docker-compose.yml
    - [ ] Add Traefik labels
    - [ ] Configure Authentik provider (if needed)
    - [ ] Test SSL certificate
    - [ ] Add to Homepage dashboard
    - [ ] Update this documentation
    - [ ] Configure backups

??? example "Docker Compose Template"
    ```yaml
    version: ‘3.8’

    services:
      myservice:
        image: myimage:latest  # (1)!
        container_name: myservice  # (2)!
        restart: unless-stopped  # (3)!
        networks:
          - proxy  # (4)!
        volumes:
          - ./config:/config  # (5)!
        environment:
          - TZ=America/New_York  # (6)!
        labels:
          - "traefik.enable=true"  # (7)!
          - "traefik.http.routers.myservice.rule=Host(`myservice.anthonychild.com`)"
          - "traefik.http.routers.myservice.entrypoints=websecure"
          - "traefik.http.routers.myservice.tls.certresolver=letsencrypt"
          - "traefik.http.services.myservice.loadbalancer.server.port=8080"  # (8)!

    networks:
      proxy:
        external: true
    ```

    1. Use specific version tags in production
    2. Clear naming for easy management
    3. Auto-restart policy
    4. Connect to Traefik's proxy network
    5. Persistent configuration storage
    6. Set timezone for logs
    7. Enable Traefik routing
    8. Internal container port
    ```
