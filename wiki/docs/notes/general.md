# :material-note-text: General Notes

A catch-all for random thoughts, reminders, life hacks, and anything that doesn’t fit elsewhere.

!!! tip ":material-brain: How I Use This Page"
    This is my digital brain dump — quick ideas, reminders, and “I’ll forget this later” notes go here!

-----

## :material-checkbox-marked-circle: Daily/Weekly Reminders

### Daily Checks

- [ ] Check [Homepage dashboard]({{ service_url("homepage") }}) for service status
- [ ] Review any alerts in [Notifiarr]({{ service_url("notifiarr") }})
- [ ] Glance at [Tautulli]({{ service_url("tautulli") }}) for media activity

### Weekly Tasks

- [ ] Run homelab updates: `./update-all.sh --sync-env`
- [ ] Review [CrowdSec bans]({{ service_url("traefik") }}) in Traefik dashboard 🛡️
- [ ] Check disk space: `df -h`
- [ ] Review [Dozzle logs]({{ service_url("dozzle") }}) for errors

### Monthly Tasks

- [ ] Verify backups are running 💾
- [ ] Test backup restore on non-critical service
- [ ] Review and clean up old Docker images
- [ ] Update mobile apps (Plex, Immich, etc.) 📱
- [ ] Check for security updates
- [ ] Review CrowdSec metrics

### As Needed

- [ ] Clear browser cache when Homepage widgets act up 🌐
- [ ] Review long-running containers before restarting them
- [ ] Review and update documentation

-----

## :material-flash: Quick Commands I Always Forget

### Homelab Updates

```bash
# Standard update
./update-all.sh

# Full update with env sync
./update-all.sh --sync-env

# Complete update including docs
./update-all.sh --sync-env --docs
```

### Documentation

```bash
# Rebuild/restart the documentation services from the current utilities stack
cd 6-utilities
docker compose restart

# View documentation stack logs
docker compose logs -f
```

### Docker Cleanup

```bash
# See Docker disk usage first
docker system df

# Remove stopped containers
docker container prune

# Remove dangling images
docker image prune
```

!!! warning ":material-delete-alert: Prune Carefully"
    Inspect what Docker considers unused before pruning. Avoid routine volume or full-system pruning unless you have verified exactly what will be removed.

### Monitoring

```bash
# View all container resource usage
docker stats

# Check disk usage
df -h
docker system df

# Find what's using disk space
du -h /var/lib/docker | sort -rh | head -20
```

### Quick Restarts

```bash
# Restart a specific service from its stack directory
docker compose restart <service-name>

# Restart the current stack
docker compose restart

# Inspect a container before changing it
docker inspect <container-name>
```

-----

## :material-lightbulb-on: Things I’ve Learned

### Docker Tips

- Prefer explicit image versions or intentional release channels over an accidental `:latest` dependency
- Set restart policies intentionally for each service
- Use `.env` files or other appropriate secret/config handling for environment-specific values
- Name your containers clearly for easier management
- Check logs before restarting or changing configuration

### Networking

- Connect services only to the networks they need
- Use `docker network inspect` when troubleshooting connectivity
- Containers sharing the required network can use container names as hostnames
- Prefer container-name routing over fixed Docker IP addresses
- Traefik labels are case-sensitive!
- Joining the shared `proxy` network does not by itself make a service public

### Backup Wisdom

- The best backup is one you’ve tested restoring
- Automate backups or they won’t happen
- Store backups off-site (or at least off-server)
- Document your backup process
- Keep multiple versions (not just the latest)

### Troubleshooting

- Check logs first: `docker logs <container>`
- Check container health before restarting it
- Always check disk space when things act weird
- Clear browser cache for web UI issues
- Time sync issues can cause weird authentication problems

-----

## :material-thought-bubble: Random Ideas & Future Experiments

### Might Try Someday

- [ ] Set up automated testing for backup restores
- [ ] Implement monitoring with Prometheus/Grafana
- [ ] Try different media metadata tools
- [ ] Experiment with container orchestration (Kubernetes? Nomad?)
- [ ] Set up home automation integration
- [ ] Add more monitoring and alerting
- [ ] Create a staging environment for testing

### Services to Explore

- [ ] Paperless-ngx for document management
- [ ] Vaultwarden for password management
- [ ] Nextcloud for file sync
- [ ] Uptime Kuma for uptime monitoring
- [ ] Frigate for security cameras
- [ ] Home Assistant for smart home

-----

## :material-bookmark: Useful Links I Don’t Want to Lose

### Documentation

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Traefik Docs](https://doc.traefik.io/traefik/)
- [Authentik Docs](https://docs.goauthentik.io/)
- [Zensical Docs](https://zensical.org/docs/)

### Communities

- [r/selfhosted](https://www.reddit.com/r/selfhosted/)
- [r/homelab](https://www.reddit.com/r/homelab/)
- [Awesome Selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)

### Tools

- [Webhook.site](https://webhook.site/) - Test webhooks
- [Regex101](https://regex101.com/) - Test regex patterns
- [CyberChef](https://gchq.github.io/CyberChef/) - Data manipulation
- [JWT.io](https://jwt.io/) - Decode JWT tokens

-----

## :material-wrench: Common Fixes

### Homepage Widget Not Updating

```bash
# Clear browser cache, then restart Homepage from the monitoring stack
docker compose restart homepage
```

### Plex Not Seeing New Media

```bash
# Restart Plex from the media-server stack if a restart is actually needed
docker compose restart plex

# Or via Plex UI: Settings → Library → Scan Library Files
```

### Authentik Login Loop

1. Clear browser cookies for `.anthonychild.com`
1. Try incognito/private mode
1. Check Authentik logs: `docker logs authentik`

### Traefik / HTTPS Issue

1. Check Traefik logs before changing certificate state.
1. Confirm the router, service, middleware, and shared `proxy` network are correct.
1. Confirm the Cloudflare Tunnel route reaches Traefik.
1. Back up certificate state before making any ACME-related changes.

### Container Using Too Much Memory

```bash
# Check what's using memory
docker stats

# Inspect the container and its logs before restarting it
docker inspect <container-name>
docker logs --tail 200 <container-name>
```

-----

## :material-calendar: Seasonal Tasks

### Spring (March-May)

- [ ] Review and update all documentation
- [ ] Clean up old backups
- [ ] Test disaster recovery procedures

### Summer (June-August)

- [ ] Check cooling/temperatures
- [ ] Review power consumption
- [ ] Plan infrastructure upgrades

### Fall (September-November)

- [ ] Prepare for increased media usage (holiday season)
- [ ] Review storage capacity
- [ ] Update emergency contacts/procedures

### Winter (December-February)

- [ ] Year-end backup verification
- [ ] Review annual costs
- [ ] Plan next year’s improvements

-----

## :material-account-voice: Things People Ask Me

### “Why self-host?”

- Privacy and control over my data
- Learning experience
- Cost savings long-term
- It’s fun!

### “Isn’t it complicated?”

- At first, yes. But documentation helps
- Modular approach makes it manageable
- Automation reduces daily work
- Once it’s running, it’s pretty stable

### “What if something breaks?”

- That’s what backups are for
- Documentation helps me remember how to fix things
- Logs usually point me toward the real problem
- I learn something new each time

### “How much does it cost?”

- Initial hardware investment
- ~$15/year for domain
- Electricity (varies)
- Most of the software is free/open source

-----

## :material-pencil: Notes to Self

!!! note "Remember"
    - Document as you go, not after
    - If you think “I’ll remember this,” you won’t
    - Simple solutions are usually best
    - Automate the boring stuff
    - Back up before making major changes
    - Test in staging when possible
    - Sleep on big decisions
    - It’s okay to break things in homelab

!!! quote "Favorite Quote"
    “The best time to start was yesterday. The second best time is now.”

-----

## :material-format-list-checks: Quick Reference

|Task                   |Command/Link                               |
|-----------------------|-------------------------------------------|
|Check all services     |[Homepage]({{ service_url("homepage") }})  |
|View logs              |[Dozzle]({{ service_url("dozzle") }})      |
|Plex analytics         |[Tautulli]({{ service_url("tautulli") }})  |
|Request media          |[Seerr]({{ service_url("seerr") }})        |
|Manage auth            |[Authentik]({{ service_url("authentik") }})|
|Update containers      |`./update-all.sh`                           |
|Check disk space       |`df -h`                                     |
|View container stats   |`docker stats`                              |
|Network troubleshooting|`docker network inspect proxy`              |

-----

<div class="center" markdown>

**Keep adding to this page!** :material-plus-circle:

*Life’s too short to remember everything. Write it down.*

</div>
