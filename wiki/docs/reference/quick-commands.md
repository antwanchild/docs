---
search:
    boost: 10
hide:
    - toc
---
# :material-flash: Quick Commands

**Your daily driver** - the commands you actually use every day. No fluff, just copy-paste.

=== "Updates"
    **Daily routine:**
    ```bash
    ./update-all.sh
    ```

    **With env sync:**
    ```bash
    ./update-all.sh --sync-env
    ```

    **Full update + docs:**
    ```bash
    ./update-all.sh --sync-env --docs
    ```

=== "Docker"
    **Status checks:**
    ```bash
    docker ps              # Running containers
    docker stats           # Resource usage
    ```

    **Logs:**
    ```bash
    docker logs -f <container>
    ```

    **Restart:**
    ```bash
    docker restart <container>
    ```

    **Stack operations:**
    ```bash
    cd docker/[stack-name]
    docker compose restart
    docker compose up -d --force-recreate
    ```

=== "Cleanup"
    **Safe cleanup:**
    ```bash
    docker container prune -f
    docker image prune -a -f
    ```

    **Nuclear option:**
    ```bash
    docker system prune -a --volumes -f
    ```

=== "Logs"
    **Follow logs:**
    ```bash
    docker logs -f <container>
    docker compose logs -f
    ```

    **Search logs:**
    ```bash
    docker logs <container> | grep error
    ```

=== "Network"
    **Check connectivity:**
    ```bash
    docker network inspect proxy
    docker exec <container> ping <other>
    ```

    **Tailscale:**
    ```bash
    tailscale status
    tailscale ping <device>
    ```

=== "Traefik"
    **Force cert renewal:**
    ```bash
    cd docker/1-networking
    docker compose stop traefik
    rm acme.json
    touch acme.json && chmod 600 acme.json
    docker compose up -d traefik
    ```

=== "Media"
    **Plex scan:**
    ```bash
    # Settings → Manage → Libraries → Scan
    ```

    **Restart *arr apps:**
    ```bash
    cd docker/4-media-download
    docker compose restart sonarr radarr prowlarr
    ```

=== "Security"
    **CrowdSec bans:**
    ```bash
    docker exec crowdsec cscli decisions list
    docker exec crowdsec cscli decisions delete --ip <ip>
    ```

    **Authentik backup:**
    ```bash
    cd docker/2-security
    docker compose exec authentik-db pg_dump -U authentik > backup.sql
    ```

-----

**Need more detail?** Check the [Cheatsheet](../reference/cheatsheet.md) or [Tech Tips](../notes/tech-tips.md)
