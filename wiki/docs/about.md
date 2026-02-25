---
hide:
  - navigation
---
# :material-home-heart: About This Homelab

Built and maintained with ❤️ by **Anthony Child** since 2024.

!!! sucdcess ":material-check-all: Current Status"
    Fully operational, automated, and secured! 🚀  
    28 containers running smoothly as of December 2025.

-----

## :material-chart-box: Quick Stats

|Category            |Details                                                                                     |
|--------------------|--------------------------------------------------------------------------------------------|
|**Domain**          |anthonychild.com                                                                            |
|**Primary Focus**   |Media streaming, photo backup, personal tools                                               |
|**Platform**        |Docker + Docker Compose                                                                     |
|**Stacks**          |6 modular stacks (networking, security, monitoring, media-download, media-server, utilities)|
|**Total Containers**|28 active services                                                                          |
|**Networks**        |5 isolated Docker networks                                                                  |
|**Ingress**         |Traefik + Cloudflare Tunnel                                                                 |
|**Remote Access**   |Tailscale VPN 🌐                                                                             |
|**Authentication**  |Authentik SSO 🔐                                                                             |
|**Security**        |CrowdSec IPS 🛡️ + Cloudflare Protection                                                      |
|**Documentation**   |This site (MkDocs with Material theme) 📚                                                    |

-----

## :material-lightbulb: Philosophy

**Guiding Principles:**

- :material-view-module: **Modular Design**:   Everything in separate Docker stacks for easy management, updates, and troubleshooting. One stack down doesn’t affect the others.
- :material-robot: **Automation First**:   Let the machines do the work. *arr stack for media, Kometa for metadata, automated backups, and health checks.
- :material-shield-lock: **Security by Design**:   Nothing exposed without authentication. Multiple layers of security with SSO, IPS, and zero-trust networking.
- :material-file-document-multiple: **Document Everything**:   If it’s not documented, it doesn’t exist. This wiki ensures I (and you) can understand and replicate everything.
- :material-test-tube: **Always Learning**:   The homelab is a playground for experimentation. Breaking things is how we learn to fix them better.
- :material-heart: **Fun is Required**:   Because tinkering, optimizing, and seeing it all work together is the best part! 😄

!!! quote "My Homelab Mantra"
    “The best setup is the one that just works… until you make it better.”  
    — Anthony Child

-----

## :material-star-shooting: What Makes This Special

### :material-network: Network Architecture

- **Segmented networks** for isolation (proxy, media-backend, monitoring-net, security-net, utils-net)
- **Zero open ports** on firewall thanks to Cloudflare Tunnel
- **Tailscale VPN** for secure admin access from anywhere

### :material-shield-account: Security Stack

- **Authentik SSO** protecting all services with one login
- **CrowdSec** watching for threats and auto-banning bad actors
- **Cloudflare Bouncer** syncing bans to edge network
- **MFA support** for critical services

### :material-movie: Media Excellence

- **Fully automated** media acquisition (Sonarr, Radarr, Prowlarr, SABnzbd)
- **Request system** for users via Seerr
- **Custom metadata** with Kometa collections and overlays
- **Episode title cards** generated automatically
- **Library optimization** with Unmanic transcoding

### :material-monitor-dashboard: Observability

- **Homepage dashboard** showing all service status
- **Real-time logs** via Dozzle
- **Plex analytics** with Tautulli
- **Discord notifications** for important events

-----

## :material-timeline: Evolution Timeline

**2024** - Initial Setup
:   - Started with basic Plex server
:   - Added Sonarr and Radarr for automation
:   - Implemented Traefik for reverse proxy

**Early 2025** - Security Hardening
:   - Deployed Authentik for SSO
:   - Added CrowdSec for intrusion prevention
:   - Implemented Cloudflare Tunnel

**Mid 2025** - Monitoring & Automation
:   - Added Homepage dashboard
:   - Deployed Kometa for metadata management
:   - Implemented automated backups

**Late 2025** - Documentation & Refinement
:   - Created this comprehensive wiki
:   - Optimized network segmentation
:   - Fine-tuned automation workflows

-----

## :material-server: Technology Stack

### Core Infrastructure

- **Operating System:** [Your OS - Linux/Ubuntu/Debian/etc.]
- **Containerization:** Docker + Docker Compose
- **Reverse Proxy:** Traefik v3
- **Tunnel:** Cloudflare Tunnel
- **VPN:** Tailscale

### Security & Authentication

- **SSO:** Authentik
- **IPS:** CrowdSec
- **Edge Protection:** Cloudflare
- **Database:** PostgreSQL

### Media Services

- **Server:** Plex Media Server
- **TV Automation:** Sonarr
- **Movie Automation:** Radarr
- **Indexer Manager:** Prowlarr
- **Downloader:** SABnzbd
- **Requests:** Overseerr/Seerr
- **Metadata:** Kometa
- **Transcoding:** Unmanic

### Monitoring & Management

- **Dashboard:** Homepage
- **Logs:** Dozzle
- **Analytics:** Tautulli
- **Notifications:** Notifiarr

### Utilities

- **Photos:** Immich
- **Filebrowsing:** Filebrowser Quantum
- **Pastebin:** Privatebin
- **Documentation:** MkDocs with Material theme

-----

## :material-target: Goals

### Completed ✅

- [x] Fully automated media acquisition
- [x] Single Sign-On across all services
- [x] Zero-trust network architecture
- [x] Comprehensive documentation
- [x] Monitoring and alerting
- [x] Secure remote access

### In Progress 🚧

- [ ] Automated backup testing
- [ ] High availability for critical services
- [ ] Enhanced media organization
- [ ] Performance optimization

### Future Plans 🎯

- [ ] Expanded photo management
- [ ] Home automation integration
- [ ] Network storage expansion
- [ ] Additional monitoring tools

See the full [Wishlist](planning/wishlist.md) for details.

-----

## :material-school: What I’ve Learned

Building this homelab has taught me:

- **Docker networking** - How to properly segment and secure containerized services
- **Reverse proxies** - Traefik configuration, middleware, and SSL automation
- **Authentication** - Implementing enterprise-grade SSO for home use
- **Security** - Layered security approach, threat detection, and response
- **Automation** - Writing scripts, setting up workflows, and reducing manual tasks
- **Documentation** - The importance of documenting everything clearly
- **Troubleshooting** - Reading logs, debugging issues, and finding root causes

And most importantly: **When to rebuild vs. when to patch** 😄

-----

## :material-information: About the Documentation

This wiki is built with:

- **[MkDocs](https://www.mkdocs.org/)** - Static site generator
- **[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)** - Beautiful, feature-rich theme
- **[Docker](https://www.docker.com/)** - Containerized deployment
- **Version Control** - Git for tracking changes

**Features:**

- Full-text search
- Dark/light mode toggle
- Mobile-responsive design
- Code syntax highlighting
- Mermaid diagrams
- Tabbed content
- Admonitions and callouts

The docs are automatically rebuilt and deployed whenever changes are made.

-----

## :material-frequently-asked-questions: FAQ

??? question "How much does this cost to run?"
    The hardware was a one-time investment. Ongoing costs are minimal:

    - Domain registration (~$15/year)
    - Electricity (varies by hardware)
    - Internet (already paying for it)
    - Cloudflare is free tier
    - All software is open source and free

??? question "How much time does maintenance take?"
    :   - **Daily:** ~5 minutes checking dashboards
    :   - **Weekly:** ~30 minutes for updates and monitoring
    :   - **Monthly:** ~2 hours for major updates and improvements

    Automation handles most of the work!

??? question "What happens if something breaks?"
    That’s why I have:

    - Comprehensive documentation (this site)
    - Regular backups
    - Modular architecture (one stack failure doesn't affect others)
    - Monitoring and alerts
    - Remote access via Tailscale for emergency fixes


??? question "Can I copy your setup?"
    Absolutely! That’s partly why this documentation exists. Everything here is reproducible. Check out the [Services](homelab/services.md), [Networking](homelab/networking.md), and [Stacks](homelab/stacks.md) pages for details.

??? question "Why self-host instead of using cloud services?"
    - **Privacy:** My data stays on my hardware
    - **Control:** I decide how everything works
    - **Learning:** Hands-on experience with real infrastructure
    - **Cost:** After initial investment, minimal ongoing costs
    - **Fun:** Because I enjoy it! 😊

-----

## :material-account: About Me

I’m Anthony, a tech enthusiast who believes in:

- Self-hosting over cloud dependency
- Open source software
- Privacy and security
- Learning by doing
- Documenting the journey

This homelab started as a simple Plex server and evolved into a comprehensive self-hosted infrastructure. It’s been an incredible learning experience and continues to be a playground for new ideas.

-----

## :material-email: Get in Touch

!!! tip ":material-chat: Contact"
    - Have questions about the setup? 
    - Want to share your own homelab?
    - Found an issue in the docs?

    {{ email_link("Feel free to reach out!") }}


-----

## :material-hand-wave: Acknowledgments

Big thanks to the open source community and all the amazing projects that make this possible:

- The developers of Docker, Traefik, Authentik, Plex, and all the *arr apps
- The MkDocs and Material for MkDocs teams
- The homelab community for inspiration and troubleshooting help
- Everyone who creates and maintains open source software

-----

<div class="center" markdown>

**Thanks for visiting my digital garden!** :material-sprout:

*Last updated: January 2026*

</div>