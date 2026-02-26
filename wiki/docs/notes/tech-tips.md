---
search:
    boost: 5
---
# :material-lightbulb: Tech Tips & Knowledge Base

**Detailed explanations with context** - understand the “why” behind the commands.

!!! tip "Purpose of This Page"
    Learn the concepts, understand the tools, discover advanced techniques. For quick commands, see [Quick Commands](../reference/quick-commands.md).

---

## :material-docker: Docker Deep Dive

### Understanding Exit Codes

When a container stops, it returns an exit code that tells you why:

|Exit Code|Meaning           |Common Cause              |
|---------|------------------|--------------------------|
|0        |Clean exit        |Normal shutdown           |
|1        |Application error |Config issue, missing file|
|137      |OOMKilled         |Out of memory             |
|139      |Segmentation fault|Corrupted binary          |
|143      |SIGTERM           |Manual stop               |

{% raw %}
Check with: `docker inspect <container> --format '{{.State.ExitCode}}'`
{% endraw %}

### Container Networking Explained

Containers on the same Docker network can communicate using **container names as hostnames**:

```bash
# From sonarr container, you can reach radarr:
curl http://radarr:7878/api/v3/system/status
```

This only works if both are on the same network (e.g., `media-backend`).

### Volume vs Bind Mount

**Bind Mount:** Maps host directory directly

```yaml
volumes:
  - /host/path:/container/path
```

*Use for:* Config files you edit directly

**Named Volume:** Docker-managed storage

```yaml
volumes:
  - volume_name:/container/path
```

*Use for:* Database files, app data

### Resource Limits

Prevent one container from eating all resources:

```yaml
services:
  myservice:
    deploy:
      resources:
        limits:
          cpus: '0.5'      # 50% of one CPU
          memory: 512M     # Max 512MB RAM
        reservations:
          memory: 256M     # Guaranteed 256MB
```

-----

## :material-router: Traefik Architecture

### How Traefik Routing Works

  1. **Entrypoints** - Listen on ports (80, 443)
  1. **Routers** - Match requests by hostname/path
  1. **Services** - Forward to container
  1. **Middlewares** - Transform requests (auth, headers, etc.)

Example flow:

```text
Request to plex.anthonychild.com
  → Entrypoint (443)
  → Router (matches Host rule)
  → Middleware (Authentik SSO)
  → Service (forwards to plex:32400)
```

### Dynamic Configuration via Labels

Traefik reads Docker labels to auto-configure:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.app.rule=Host(`app.anthonychild.com`)"
  - "traefik.http.routers.app.entrypoints=websecure"
  - "traefik.http.routers.app.tls.certresolver=letsencrypt"
```

No need to edit config files - just restart the container!

### Certificate Storage

Let’s Encrypt certificates are stored in `acme.json`:

- One file contains ALL certificates
- Must have `600` permissions (owner read/write only)
- Backing this up = backing up all your certs

-----

## :material-network: Network Segmentation Strategy

### Why Multiple Networks?

**Security through isolation:**

- Media apps can’t access security services
- Monitoring is separate from production
- Database only accessible to app that needs it

**Our setup:**

- `proxy` - Public-facing via Traefik
- `media-backend` - *arr apps + Plex communication
- `monitoring-net` - Dashboards and logs
- `security-net` - Authentik + CrowdSec
- `utils-net` - Miscellaneous services

### Multi-Network Containers

Some containers need multiple networks:

```yaml
services:
  plex:
    networks:
      - proxy          # For web access
      - media-backend  # For *arr communication
```

Plex can:

- Be accessed via web (proxy network)
- Receive updates from Sonarr/Radarr (media-backend network)

-----

## :material-shield-lock: Security Concepts

### How SSO Works (Authentik)

1. User visits `plex.anthonychild.com`
1. Traefik middleware checks authentication
1. If not authenticated, redirects to Authentik
1. User logs in once
1. Authentik returns token
1. Token valid for all services (Single Sign-On)

### CrowdSec Decision Flow

1. CrowdSec reads Traefik logs
1. Detects patterns (brute force, scanning, etc.)
1. Makes “decision” to ban IP
1. Cloudflare Bouncer syncs ban to Cloudflare
1. Traffic blocked at edge (never reaches your server)

### Zero Trust with Tailscale

Traditional: “Trust everything inside the network”
Zero Trust: “Verify every connection, even internal”

Tailscale creates encrypted peer-to-peer connections:

- Each device has unique identity
- ACLs control who can reach what
- No open ports on firewall
- Works from anywhere

-----

## :material-database: Database Management

### PostgreSQL Maintenance

**Why databases need maintenance:**

- Vacuuming removes dead rows
- Analyzing updates query planner statistics
- Reindexing optimizes lookups

**Authentik database care:**

```bash
# Check database size
docker exec authentik-db psql -U authentik -c "SELECT pg_size_pretty(pg_database_size('authentik'));"

# Vacuum and analyze
docker exec authentik-db psql -U authentik -c "VACUUM ANALYZE;"

# Check for bloat
docker exec authentik-db psql -U authentik -c "SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) FROM pg_tables ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC LIMIT 10;"
```

### Backup Strategy

**3-2-1 Rule:**

- **3** copies of data
- **2** different media types
- **1** off-site copy

For Docker volumes:

```bash
# Backup
docker run --rm -v volume_name:/data -v $(pwd):/backup alpine tar -czf /backup/volume.tar.gz /data

# Restore
docker run --rm -v volume_name:/data -v $(pwd):/backup alpine tar -xzf /backup/volume.tar.gz -C /
```

-----

## :material-video: Media Stack Optimization

### Plex Transcoding

**Direct Play** - No transcoding (best quality, low CPU)

**Direct Stream** - Container conversion only

**Transcode** - Full re-encode (high CPU usage)

To minimize transcoding:

- Use compatible formats (H.264, AAC)
- Match client capabilities
- Pre-optimize with Unmanic

### *arr App Quality Profiles

**Quality profile strategy:**

1. Set minimum quality (e.g., 1080p)
1. Set maximum size (e.g., 15GB for movies)
1. Enable automatic upgrades
1. Set cutoff (stop upgrading at this quality)

This prevents:

- Downloading low-quality releases
- Wasting space on 4K when 1080p is fine
- Endless upgrade cycles

### Kometa Collections

Kometa uses YAML configs to auto-create collections:

```yaml
collections:
  Top Rated Movies:
    tmdb_list: https://www.themoviedb.org/movie/top-rated
    sort_title: "+001_Top Rated"
```

This automatically:

- Creates the collection
- Adds matching movies
- Updates daily
- Adds posters/art

-----

## :material-speedometer: Performance Tuning

### When Containers Use Too Much Memory

**Symptoms:**

- System slowdown
- OOMKilled exits
- Swap usage high

**Solutions:**

1. **Find the hog:**

    ```bash
    docker stats --no-stream | sort -k4 -rh
    ```

1. **Set limits:**

    ```yaml
    mem_limit: 2g
    ```

1. **Optimize the app:**
    - Check for memory leaks in logs
    - Reduce cache sizes
    - Update to newer version

### Disk I/O Bottlenecks

**Identify I/O problems:**

```bash
iostat -x 1
```

Look for:

- High `%util` (disk busy)
- High `await` (wait time)

**Solutions:**

- Move to SSD
- Use separate disks for different workloads
- Enable caching in applications

-----

## :material-text-search: Log Analysis

### Reading Docker Logs Effectively

**Timestamps help correlate events:**

```bash
docker logs -t <container> | grep "error"
```

**Filter by time range:**

```bash
# Last 10 minutes
docker logs --since 10m <container>

# Between times
docker logs --since 2024-01-01T00:00:00 --until 2024-01-01T12:00:00 <container>
```

**Follow multiple containers:**

```bash
docker compose logs -f service1 service2
```

### Common Log Patterns

**Connection refused:**

- Service not started yet
- Wrong port
- Network not connected

**Permission denied:**

- Volume ownership wrong
- SELinux blocking
- Read-only filesystem

**Out of memory:**

- Need to increase limits
- Memory leak in app
- Too many containers on small system

-----

## :material-timer: Time Sync Importance

### Why Time Matters

**Authentication depends on time:**

- JWT tokens have expiration
- OAuth2 checks timestamps
- SSL certificates have validity periods

If time is off by >5 minutes:

- SSO fails
- Certificates rejected
- API calls fail

**Check time sync:**

```bash
timedatectl
```

Should show: `System clock synchronized: yes`

**Force sync:**

```bash
sudo systemctl restart systemd-timesyncd
```

-----

## :material-code-json: Configuration Management

### Environment Variables Best Practices

**Never commit secrets to git:**

```yaml
# Bad
environment:
  - API_KEY=abc123secret

# Good
environment:
  - API_KEY=${API_KEY}
```

Use `.env` file (add to `.gitignore`):

```text
API_KEY=abc123secret
```

### Docker Compose Overrides

Base config: `docker-compose.yml`
Local overrides: `docker-compose.override.yml` (gitignored)

This lets you:

- Share base config
- Keep local secrets/ports private
- Test different configs

-----

## :material-wrench: Advanced Techniques

### One-Liners Worth Knowing

**Stop all containers with pattern:**

```bash
docker ps --filter "name=media" -q | xargs docker stop
```

**View all container IPs:**

```bash
{% raw %}
docker ps -q | xargs -n 1 docker inspect --format '{{.Name}} {{range.NetworkSettings.Networks}}{{.IPAddress}}'
{% endraw %}
```

**Cleanup old images but keep latest:**

```bash
docker images | grep -v "latest" | awk '{print $3}' | xargs docker rmi
```

### Debugging Techniques

**Network connectivity:**

```bash
# Can container reach internet?
docker exec <container> ping 8.8.8.8

# Can it resolve DNS?
docker exec <container> nslookup google.com

# Can it reach other container?
docker exec <container> curl http://other-container:port
```

**File system issues:**

```bash
# Check permissions
docker exec <container> ls -la /config

# Check disk space inside container
docker exec <container> df -h

# Find what's using space
docker exec <container> du -h / | sort -rh | head -20
```

-----

## :material-school: Learning Resources

### Understanding the Stack

To really understand your homelab:

1. **Read the docs** - Official documentation explains design decisions
1. **Check the logs** - Logs tell you what’s actually happening
1. **Experiment** - Break things in a safe way to learn how they work
1. **Document** - Writing it down cements understanding

### Recommended Reading

- Docker networking: https://docs.docker.com/network/
- Traefik concepts: https://doc.traefik.io/traefik/getting-started/concepts/
- Authentik SSO flow: https://goauthentik.io/docs/flow/
- Linux file permissions: https://wiki.archlinux.org/title/File_permissions_and_attributes

-----

<div class="center" markdown>

**Understanding > Memorizing** :material-brain:

*For quick reference, see [Cheatsheet](../reference/cheatsheet.md)*

</div>
