---
search:
    boost: 8
---
# :material-tools: Troubleshooting Guide

**Problem-solving workflows only** - symptoms → diagnosis → solution.

!!! warning ":material-alert: Start Here"
    Before diving into specific issues, try these first:

    1. Check [Dozzle logs]({{ service_url("dozzle") }})
    2. Verify service is running: `docker ps`
    3. Try restarting: `docker restart <container>`

---

## :material-web-off: Service Not Loading

**Symptom:** Can’t access service via browser

**Quick checks:**

```bash
# Is it running?
docker ps | grep <service>

# Check Traefik dashboard
# Visit: traefik.anthonychild.com
```

**Diagnosis:**

|Check             |Command                       |Expected Result        |
|------------------|------------------------------|-----------------------|
|Container running?|`docker ps`                   |Should be listed       |
|On proxy network? |`docker network inspect proxy`|Container should appear|
|Traefik sees it?  |Check Traefik dashboard       |Route should exist     |
|Certificate valid?|Check browser SSL info        |Should be valid        |

**Solutions:**

=== "Container Not Running"
    `bash docker logs <container>  # Check why it stopped docker restart <container> `

=== "Not on Proxy Network"
    `bash docker network connect proxy <container> `

=== "Traefik Labels Wrong"
    `bash docker inspect <container> | grep traefik # Fix in docker-compose.yml, then: docker compose up -d --force-recreate `

=== "Certificate Issue"
    See [Certificate Problems](#certificate-problems) below

-----

## :material-restart: Container Keeps Restarting

**Symptom:** Container status shows "Restarting"

**Diagnosis:**

```bash
# Check exit code
{% raw %}
docker inspect <container> --format '{{.State.ExitCode}}'
{% endraw %}
# View logs
docker logs --tail=50 <container>
```

**Exit Code Meanings:**

|Code|Cause             |Solution                             |
|----|------------------|-------------------------------------|
|1   |Config error      |Check logs for missing files/vars    |
|137 |Out of memory     |Increase memory limit or reduce usage|
|139 |Segmentation fault|Update to newer image                |
|143 |Manual stop       |Check who stopped it                 |

**Solutions:**

=== "Memory Issue (137)"
    ```bash
    # Check memory usage
    docker stats
    ```
    ```
    # Add limit to docker-compose.yml
    mem_limit: 2g
    ```

=== "Config Error (1)"
    ```bash
    # View detailed logs
    docker logs <container>
    ```
    ```bash
    # Check environment variables
    docker inspect <container> | grep -A 20 Env
    ```
    ```bash
    # Verify volume mounts
    docker inspect <container> | grep -A 10 Mounts
    ```

=== "Permission Error"
    `bash # Fix permissions (most services use 1000:1000) sudo chown -R 1000:1000 /path/to/config `

-----

## :material-network-off: Network Problems

**Symptom:** Container can’t reach other containers

**Diagnosis:**

```bash
# Are they on same network?
docker network inspect <network-name>

# Test connectivity
docker exec <container1> ping <container2>

# Check DNS resolution
docker exec <container1> nslookup <container2>
```

**Solutions:**

=== "Not on Same Network"
    `bash docker network connect <network> <container> `

=== "DNS Not Working"
    ```bash
    # Restart Docker daemon
    sudo systemctl restart docker
    ```
    ```bash
    # Or recreate containers
    cd docker/[stack]
    docker compose down
    docker compose up -d
    ```

=== "Port Already in Use"
    ```bash
    # Find what’s using port
    sudo netstat -tulpn | grep <port>
    ```
    ```bash
    # Stop conflicting service
    sudo systemctl stop <service>
    ```
    ```bash
    # Or change port in docker-compose.yml
    ```

-----

## :material-certificate-outline: Certificate Problems

**Symptom:** "Your connection is not private" warning

**Diagnosis:**

```bash
# Check Traefik logs
docker logs traefik | grep -i acme

# View stored certs
docker exec traefik ls -la /letsencrypt/
```

**Solutions:**

=== "Force Renewal"
    ```bash
    cd docker/1-networking
    docker compose stop traefik
    
    # Backup
    cp acme.json acme.json.backup

    # Reset
    rm acme.json
    touch acme.json
    chmod 600 acme.json

    # Restart
    docker compose up -d traefik

    # Watch logs
    docker logs -f traefik
    ```

=== "DNS Not Propagated"
    ```bash
    # Check DNS
    nslookup service.anthonychild.com

    # Wait for propagation (can take hours)
    # Or update Cloudflare DNS manually
    ```

-----

## :material-shield-alert: Authentication Issues

**Symptom:** Login loop or can’t authenticate

**Diagnosis:**

```bash
# Check Authentik logs
docker logs authentik | grep -i error

# Verify time sync
timedatectl
```

**Solutions:**

=== "Login Loop"
    1. Clear browser cookies for `.anthonychild.com`
    2. Try incognito/private mode
    3. Check Authentik logs
    4. Verify time is synced

=== "CrowdSec Blocking"
    ```bash
    # Check if IP is banned
    docker exec crowdsec cscli decisions list | grep <your-ip>
    ```
    ```bash
    # Unban
    docker exec crowdsec cscli decisions delete --ip <your-ip>
    ```

=== "Forward Auth Failing"
    ```bash
    # Check Traefik middleware
    docker logs traefik | grep -i auth
    ```
    ```bash
    # Restart Authentik
    cd docker/security
    docker compose restart authentik
    ```

-----

## :material-plex: Plex Specific

**Symptom:** Various Plex issues

=== "Can’t Claim Server"
    **Solution:**
    SSH tunnel method `ssh -L 32400:localhost:32400 user@server`

    Then visit: http://localhost:32400/web

=== "Library Not Updating"
    **Solutions:**

    1. Force scan: Settings → Library → Scan
    2. Check permissions: `ls -la /media`
    3. Fix if needed: `sudo chown -R 1000:1000 /media`
    4. Restart Plex: `docker restart plex`

=== "Transcoding Fails"
    **Diagnosis:**
    ```bash
    # Check transcode logs
    docker exec plex cat /config/Library/Application\ Support/Plex\ Media\ Server/Logs/Plex\ Media\ Server.log | grep Transcode
    ```
    ```bash
    # Check disk space
    docker exec plex df -h /transcode
    ```

-----

## :material-harddisk: Disk Space

**Symptom:** "No space left on device" errors

**Diagnosis:**

```bash
# Check disk usage
df -h

# Docker usage
docker system df

# Find large files
du -h /var/lib/docker | sort -rh | head -20
```

**Solutions:**

=== "Clean Docker"
    ```bash
    # Safe cleanup
    docker container prune -f
    docker image prune -a -f
    ```
    ```bash
    # Nuclear option (removes volumes!)
    docker system prune -a --volumes -f
    ```

=== "Clean Logs"
    ```bash
    # Find large logs
    find /var/lib/docker/containers -name "*.log" -size +100M
    ```
    ```bash
    # Truncate (be careful!)
    truncate -s 0 /var/lib/docker/containers/<id>/<id>-json.log
    ```

=== "Configure Log Rotation"
    Add to docker-compose.yml:
    ```yaml 
    logging: 
        driver: "json-file" 
        options: max-size: "10m" 
        max-file: "3" 
    ```

-----

## :material-database-alert: Database Issues

**Symptom:** Database connection errors

**Diagnosis:**

```bash
# Check if DB is running
docker ps | grep postgres

# Check DB logs
docker logs authentik-db

# Test connection
docker exec authentik-db pg_isready -U authentik
```

**Solutions:**

=== "DB Not Responding"
    ```bash
    # Restart DB (will cause brief outage)
    cd docker/2-security
    docker compose restart authentik-db
    ```
    ```bash
    # Wait 30 seconds
    sleep 30

    # Restart app
    docker compose restart authentik
    ```

=== "Connection Refused"
    ```bash
    # Verify both on same network
    docker network inspect security-net
    ```
    ```
    # Check environment variables
    docker inspect authentik | grep -i db
    ```

-----

## :material-cloud-off: Cloudflare Tunnel Down

**Symptom:** Can’t access services from internet

**Diagnosis:**

```bash
# Check tunnel logs
docker logs cloudflared

# Check Cloudflare dashboard
# Visit: dash.cloudflare.com → Zero Trust → Tunnels
```

**Solutions:**

=== "Tunnel Not Connected"
    ```bash
    # Restart tunnel
    cd docker/1-networking
    docker compose restart cloudflared
    ```
    ```
    # Check logs
    docker logs -f cloudflared
    ```

=== "Credentials Invalid"
    ```bash 
    # Re-authenticate tunnel 
    # Follow Cloudflare docs to get new credentials 
    # Update docker-compose.yml 
    docker compose up -d cloudflared
    ```

-----

## :material-speedometer: Performance Issues

**Symptom:** Services running slow

**Diagnosis:**

```bash
# Check system resources
docker stats
htop

# Check disk I/O
sudo iotop -o

# Check network
sudo nethogs
```

**Solutions:**

=== "High CPU"
    ```bash
    # Find the hog
    docker stats –no-stream | sort -k3 -rh
    ```
    ```
    # Restart heavy container
    docker restart <container>

    # Set CPU limits if needed
    ```

=== "High Memory"
    ```bash
    # Check swap usage
    free -h
    ```
    ```
    # Restart memory hog
    docker restart <container>

    # Add memory limit to docker-compose.yml
    ```

=== "Disk I/O Wait"
    ```bash
    # Check disk usage
    iostat -x 1
    ```
    ```
    # May need:
    # - Move to SSD
    # - Reduce log sizes
    # - Optimize database
    ```

-----

## :material-timer-alert: Time Sync

**Symptom:** Authentication fails, certificates rejected

**Diagnosis:**

```bash
# Check system time
timedatectl

# Check container time
docker exec <container> date
```

**Solution:**

```bash
# Force time sync
sudo systemctl restart systemd-timesyncd
sudo timedatectl set-ntp true

# Verify
timedatectl
# Should show: "System clock synchronized: yes"
```

-----

## :material-help-circle: Still Stuck?

If none of these solutions work:

1. **Check service-specific logs in [Dozzle]({{ service_url("dozzle") }})**
1. **Review [Services documentation](../homelab/services.md)**
1. **Search this wiki** (Press ++f++)
1. **Check [Tech Tips](../notes/tech-tips.md)** for more detailed explanations

!!! tip "Document Your Fix"
    When you solve something new, add it here for next time!

-----

<div class="center" markdown>

**Most problems are solved by restarting** :material-restart:

*For commands, see [Quick Commands](quick-commands.md)*

</div>