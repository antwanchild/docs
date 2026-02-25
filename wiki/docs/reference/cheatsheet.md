---
search:
  boost: 8
hide: 
  - toc
---
# :material-clipboard-text: Cheatsheet

**Quick reference lookup** - scan, find, copy. No explanations, just what you need.

---

## :material-update: Updates

|Task              |Command                                             |
|------------------|----------------------------------------------------|
|Standard update   |`./update-all.sh`                                   |
|Update + sync env |`./update-all.sh --sync-env`                        |
|Full update + docs|`./update-all.sh --sync-env --docs`                 |
|Full update + blog|`./update-all.sh --sync-env --blog`                 |
|Full update + both|`./update-all.sh --sync-env --all`
|Rebuild docs      |`cd docker/6-utilities && docker compose restart docs`|

!!! info "Sync Docs without .env"
    If you want to just update the "docs" without .env file, then remove the `--sync-env` from your command

-----

## :material-docker: Docker Essentials

|Task        |Command                           |
|------------|----------------------------------|
|List running|`docker ps`                       |
|List all    |`docker ps -a`                    |
|Stats       |`docker stats`                    |
|Start       |`docker start <container>`        |
|Stop        |`docker stop <container>`         |
|Restart     |`docker restart <container>`      |
|Logs        |`docker logs -f <container>`      |
|Shell access|`docker exec -it <container> bash`|

-----

## :material-layers: Stack Operations

|Task           |Command                                |
|---------------|---------------------------------------|
|Start stack    |`docker compose up -d`                 |
|Stop stack     |`docker compose down`                  |
|Restart stack  |`docker compose restart`               |
|Restart service|`docker compose restart <service>`     |
|View logs      |`docker compose logs -f`               |
|Recreate       |`docker compose up -d --force-recreate`|

-----

## :material-trash-can: Cleanup

|Task                     |Command                              |
|-------------------------|-------------------------------------|
|Remove stopped containers|`docker container prune -f`          |
|Remove unused images     |`docker image prune -a -f`           |
|Remove unused volumes    |`docker volume prune -f`             |
|Full cleanup             |`docker system prune -a --volumes -f`|
|Check disk usage         |`docker system df`                   |

-----

## :material-network: Networking

|Task             |Command                           |
|-----------------|----------------------------------|
|List networks    |`docker network ls`               |
|Inspect network  |`docker network inspect <network>`|
|Test connectivity|`docker exec <c1> ping <c2>`      |
|Check ports      |`ss -tuln`                        |
|Tailscale status |`tailscale status`                |
|Tailscale ping   |`tailscale ping <device>`         |

-----

## :material-file-document: System

|Task            |Command                        |
|----------------|-------------------------------|
|Disk space      |`df -h`                        |
|Find large files|`du -h / | sort -hr | head -20`|
|Check open ports|`ss -tuln`                     |
|System load     |`htop`                         |
|Disk I/O        |`sudo iotop -o`                |

-----

## :material-shield-check: Security

|Task            |Command                                                                                   |
|----------------|------------------------------------------------------------------------------------------|
|CrowdSec bans   |`docker exec crowdsec cscli decisions list`                                               |
|Unban IP        |`docker exec crowdsec cscli decisions delete --ip <ip>`                                   |
|Ban IP          |`docker exec crowdsec cscli decisions add --ip <ip>`                                      |
|Authentik backup|`cd docker/2-security && docker compose exec authentik-db pg_dump -U authentik > backup.sql`|

-----

## :material-certificate: Traefik

|Task              |Steps                                                                                                                                                                         |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Force cert renewal|1. `cd docker/1-networking` <br> 2. `docker compose stop traefik` <br> 3. `rm acme.json` <br> 4. `touch acme.json && chmod 600 acme.json` <br> 5. `docker compose up -d traefik`|
|View routes       |Visit [Traefik Dashboard]({{ service_url("traefik") }}) → HTTP → Routers                                                                                                      |

-----

## :material-movie: Media Stack

|Task                      |Command/Location                                                           |
|--------------------------|---------------------------------------------------------------------------|
|Plex scan                 |Settings → Manage → Libraries → Scan                                       |
|Restart *arr apps         |`cd docker/4-media-download && docker compose restart sonarr radarr prowlarr`|
|Kometa run                |`cd docker/5-media-server && docker compose run --rm kometa`                 |
|Clear Radarr/Sonarr failed|History → Select → Remove                                                  |

-----

## :material-wrench: Common Fixes

|Problem               |Quick Fix                                                  |
|----------------------|-----------------------------------------------------------|
|Container won’t start |`docker logs <container>` then `docker restart <container>`|
|Service not in Traefik|Check labels: `docker inspect <container> | grep traefik`  |
|Network issue         |`docker network inspect proxy`                             |
|Homepage widget broken|Clear browser cache, restart homepage                      |
|Out of disk space     |`docker system prune -a --volumes -f`                      |

-----

**Need more context?** See [Tech Tips](../notes/tech-tips.md) for detailed explanations.