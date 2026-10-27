# :material-calendar-star: Planning & Wishlist 🌟

Future ideas and upgrades for the homelab. This page is intentionally a planning board, not a statement of what is currently deployed. 🧭

!!! info ":material-source-branch: Current State"
    For deployed services, use the [Homelab Overview](../homelab/overview.md) and current `ubuntu_Desktop` Compose configuration as the source of truth. 🐳

## :material-clock-fast: Near-Term Ideas 🚀

### Infrastructure 🖥️

- [ ] Strengthen automated offsite backups ☁️
- [ ] Add automated backup-restore testing 💾
- [ ] Expand external uptime monitoring ⏱️
- [ ] Continue improving container health checks and alerting 🩺
- [ ] Create a safer staging path for infrastructure changes 🧪

### Dashboard & Automation 🎛️

- [ ] Continue developing custom Homepage widgets 🧩
- [ ] Improve notification signal-to-noise 🔔
- [ ] Expand useful automation around routine maintenance 🤖
- [ ] Improve monitoring coverage where it provides actionable information 📊

## :material-calendar: Services to Evaluate 🔎

These are candidates, not commitments:

- [ ] **Vaultwarden** - password management 🔐
- [ ] **Paperless-ngx** - document management 📄
- [ ] **Mealie** - recipe management 🍲
- [ ] **Actual Budget** - personal finance 💰
- [ ] **Audiobookshelf** - audiobook hosting 🎧
- [ ] **Stirling-PDF** - PDF utilities 📑
- [ ] **Home Assistant** - home automation 🏠
- [ ] **Frigate** - local NVR and camera analysis 📹

## :material-flask: Technical Experiments 🧪

- GitOps workflows 🔁
- Infrastructure as Code 🏗️
- Container security scanning 🛡️
- Better automated deployment validation ✅
- Local AI integrations where they solve a real problem 🧠
- Multi-node orchestration if the homelab eventually outgrows a single-server design 🕸️

## :material-star-shooting: Long-Term Ideas 🌠

- More resilient backups with an off-site recovery path ☁️
- Better energy and power monitoring ⚡
- Home automation integration 🏠
- A secondary host or failover strategy if the additional complexity becomes worthwhile 🖥️
- More proactive monitoring and anomaly detection 📈

## :material-trophy: Milestones 🏆

### 2026

- [x] Organize the Ubuntu homelab into six modular Docker Compose stacks 🐳
- [x] Migrate the wiki and blog to Zensical 📚
- [x] Refresh homelab documentation against the current Compose configuration 📝
- [x] Improve documentation CI/CD validation and build traceability 🔍
- [x] Add newer monitoring and security tooling to the documented architecture 🛡️

### 2025

- [x] Build out the original documentation site 📖
- [x] Expand Authentik SSO and CrowdSec protection 🔐
- [x] Establish Cloudflare Tunnel and Tailscale remote-access patterns 🌐
- [x] Expand media automation and metadata tooling 🎬

!!! tip ":material-lightbulb-on: Planning Rule"
    Keep experiments here until they are actually deployed. Once something becomes part of the homelab, document it in the appropriate Homelab page and let Compose describe the exact implementation. 💡
