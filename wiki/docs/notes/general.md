# :material-note-text: General Notes

A compact scratchpad for homelab reminders and commands that are useful often enough to keep close at hand.

!!! info ":material-source-branch: Exact Configuration"
    Use the current `ubuntu_Desktop` Compose files for exact stack paths, service names, image tags, mounts, and network membership. These notes intentionally avoid duplicating details that change frequently.

## :material-flash: Quick Checks

```bash
# Running containers
docker ps

# Resource usage
docker stats

# Docker disk usage
docker system df

# Host disk usage
df -h

# Shared proxy network
docker network inspect proxy
```

## :material-docker: Docker Reminders

- Prefer explicit image versions or intentional release channels over an accidental `latest` dependency.
- Use container names for service-to-service routing when containers share the required network.
- Check logs before restarting or changing configuration.
- Keep secrets and environment-specific values outside committed Compose files.
- Inspect what Docker considers unused before running prune commands.
- Test backups by restoring them, not merely by confirming that backup files exist.

## :material-network: Networking Reminders

- Traefik is the web ingress layer for selected applications.
- Cloudflare Tunnel provides the external path without conventional inbound port forwarding.
- Tailscale is the private remote-access path for administration and home-network access.
- Joining the `proxy` network does not itself make a service public. Routing and middleware determine exposure.
- Prefer container-name routing over fixed Docker IP addresses.

See **[Networking](../homelab/networking.md)** for the architecture and **[Stacks](../homelab/stacks.md)** for the current stack model.

## :material-shield-check: Security Reminders

- Keep middleware ordering intentional.
- Protect administrative interfaces with the appropriate authentication and access controls.
- Review CrowdSec, Anubis, Authentik, Traefik, and Cloudflare configuration as a layered system rather than independent switches.
- Avoid publishing host ports when Traefik or private Docker networking is sufficient.
- Apply least privilege to networks, mounts, permissions, and credentials.

## :material-lifebuoy: Troubleshooting Order

1. Confirm the container is running and healthy.
2. Read the container logs.
3. Check disk space and host resources.
4. Verify Docker network membership and name resolution.
5. Check Traefik routing and middleware for web-access problems.
6. Check the upstream application itself before changing infrastructure.
7. Compare the running deployment with the current Compose configuration.

```bash
# Recent logs
docker logs --tail 200 <container>

# Follow logs
docker logs -f <container>

# Inspect network membership
docker inspect <container> --format '{{json .NetworkSettings.Networks}}'
```

## :material-backup-restore: Backup Reminders

- Keep important backups off the primary server when practical.
- Retain multiple recovery points.
- Document the restore procedure alongside the backup procedure.
- Periodically perform a real restore test on non-production data or an isolated service.
- Back up configuration and application data according to the needs of each service rather than assuming one strategy fits everything.

## :material-bookmark: Useful References

- [Docker Compose](https://docs.docker.com/compose/)
- [Traefik](https://doc.traefik.io/traefik/)
- [Authentik](https://docs.goauthentik.io/)
- [Zensical](https://zensical.org/docs/)
- [Awesome Selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)

The larger collection lives on the **[Bookmarks](../bookmarks.md)** page.

## :material-pencil: Notes to Self

!!! note "Remember"
    - Document important decisions while they are fresh.
    - Prefer simple, reversible changes.
    - Back up before risky changes.
    - Validate configuration before deploying it.
    - If a note becomes permanent architecture, move it to the appropriate wiki page.
