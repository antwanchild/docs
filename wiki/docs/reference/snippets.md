---
search:
    boost: 6
---
# :material-content-copy: Common Snippets

**Copy-paste ready configurations** for quick deployment. All tested and working!

!!! tip ":material-rocket: Quick Deploy"
    These snippets are ready to use - just replace the placeholders with your values!

-----

## :material-docker: Docker Compose Templates

### Basic Service Template

```yaml
version: '3.8'

services:
  myservice:
    image: myimage:latest
    container_name: myservice
    restart: unless-stopped
    networks:
      - proxy
    volumes:
      - ./config:/config
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.myservice.rule=Host(`myservice.anthonychild.com`)"
      - "traefik.http.routers.myservice.entrypoints=websecure"
      - "traefik.http.routers.myservice.tls.certresolver=letsencrypt"
      - "traefik.http.services.myservice.loadbalancer.server.port=8080"

networks:
  proxy:
    external: true
```

### Service with Database

```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    container_name: myapp
    restart: unless-stopped
    depends_on:
      - db
    networks:
      - proxy
      - backend
    environment:
      - DB_HOST=db
      - DB_NAME=myapp
      - DB_USER=myapp
      - DB_PASSWORD=${DB_PASSWORD}
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.myapp.rule=Host(`myapp.anthonychild.com`)"
      - "traefik.http.routers.myapp.entrypoints=websecure"
      - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
  
  db:
    image: postgres:16
    container_name: myapp-db
    restart: unless-stopped
    networks:
      - backend
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=myapp
      - POSTGRES_PASSWORD=${DB_PASSWORD}

networks:
  proxy:
    external: true
  backend:
    driver: bridge

volumes:
  db-data:
```

### Service with Authentik SSO

```yaml
version: '3.8'

services:
  myservice:
    image: myimage:latest
    container_name: myservice
    restart: unless-stopped
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.myservice.rule=Host(`myservice.anthonychild.com`)"
      - "traefik.http.routers.myservice.entrypoints=websecure"
      - "traefik.http.routers.myservice.tls.certresolver=letsencrypt"
      # Authentik forward auth
      - "traefik.http.routers.myservice.middlewares=authentik@docker"
      - "traefik.http.services.myservice.loadbalancer.server.port=8080"

networks:
  proxy:
    external: true
```

-----

## :material-router: Traefik Labels

### Basic HTTPS with Let’s Encrypt

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`myapp.anthonychild.com`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
  - "traefik.http.services.myapp.loadbalancer.server.port=8080"
```

### With Authentik SSO

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`myapp.anthonychild.com`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
  - "traefik.http.routers.myapp.middlewares=authentik@docker"
  - "traefik.http.services.myapp.loadbalancer.server.port=8080"
```

### With Basic Auth

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`myapp.anthonychild.com`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
  - "traefik.http.routers.myapp.middlewares=basic-auth"
  - "traefik.http.services.myapp.loadbalancer.server.port=8080"
  # Create password with: htpasswd -nb user password
  - "traefik.http.middlewares.basic-auth.basicauth.users=user:$$apr1$$hash"
```

### Multiple Domains

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`myapp.anthonychild.com`) || Host(`app.example.com`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
  - "traefik.http.services.myapp.loadbalancer.server.port=8080"
```

### With Path Prefix

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`anthonychild.com`) && PathPrefix(`/myapp`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.routers.myapp.tls.certresolver=letsencrypt"
  - "traefik.http.services.myapp.loadbalancer.server.port=8080"
  # Strip prefix before forwarding
  - "traefik.http.middlewares.myapp-strip.stripprefix.prefixes=/myapp"
  - "traefik.http.routers.myapp.middlewares=myapp-strip"
```

-----

## :material-shield-account: Authentik Provider Configs

### OAuth2/OIDC Application

**In Authentik UI:**

1. **Applications → Create**

- Name: `My Service`
- Slug: `myservice`
- Provider: Create new OAuth2/OIDC Provider

1. **Provider Settings:**

- Client ID: `generated-by-authentik`
- Client Secret: `generated-by-authentik`
- Redirect URIs: `https://myservice.anthonychild.com/oauth/callback`
- Scopes: `openid profile email`

**In your application:**

```yaml
environment:
  - OAUTH_CLIENT_ID=your-client-id
  - OAUTH_CLIENT_SECRET=your-client-secret
  - OAUTH_AUTHORIZE_URL=https://auth.anthonychild.com/application/o/authorize/
  - OAUTH_TOKEN_URL=https://auth.anthonychild.com/application/o/token/
  - OAUTH_USERINFO_URL=https://auth.anthonychild.com/application/o/userinfo/
```

### Forward Auth (for services without native SSO)

**Traefik middleware:**

```yaml
# In Authentik docker-compose.yml
labels:
  - "traefik.http.middlewares.authentik.forwardauth.address=http://authentik-server:9000/outpost.goauthentik.io/auth/traefik"
  - "traefik.http.middlewares.authentik.forwardauth.trustForwardHeader=true"
  - "traefik.http.middlewares.authentik.forwardauth.authResponseHeaders=X-authentik-username,X-authentik-groups,X-authentik-email,X-authentik-name,X-authentik-uid"
```

-----

## :material-variable: Common Environment Variables

### Standard User/Group IDs

```yaml
environment:
  - PUID=1000
  - PGID=1000
  - UMASK=022
```

### Timezone

```yaml
environment:
  - TZ=America/New_York
```

### PostgreSQL Database

```yaml
environment:
  - POSTGRES_DB=myapp
  - POSTGRES_USER=myapp
  - POSTGRES_PASSWORD=${DB_PASSWORD}  # From .env file
  - POSTGRES_HOST=db
  - POSTGRES_PORT=5432
```

### Redis Cache

```yaml
environment:
  - REDIS_HOST=redis
  - REDIS_PORT=6379
  - REDIS_PASSWORD=${REDIS_PASSWORD}
```

-----

## :material-script-text: Useful Scripts

### Update All Stacks

```bash
#!/bin/bash
# update-all.sh

STACKS=("networking" "security" "monitoring" "media-download" "media-server" "utilities")

for stack in "${STACKS[@]}"; do
  echo "=== Updating $stack ==="
  cd docker/$stack || exit
  docker compose pull
  docker compose up -d
  cd ../..
  echo ""
done

echo "✅ All stacks updated!"
```

### Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d)

# Backup docker volumes
docker run --rm \
  -v authentik-data:/data \
  -v $BACKUP_DIR:/backup \
  alpine tar -czf /backup/authentik-$DATE.tar.gz /data

# Backup Authentik database
cd docker/security
docker compose exec -T authentik-db pg_dump -U authentik > $BACKUP_DIR/authentik-db-$DATE.sql

echo "✅ Backup completed: $DATE"
```

### Check Container Health

```bash
#!/bin/bash
# health-check.sh
{% raw %}
echo "=== Container Health Check ==="
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -v "Up"

echo ""
echo "=== Resource Usage ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
{% endraw %}
```

-----

## :material-network: Network Creation

### Create Standard Networks

```bash
# Create all standard networks
docker network create --driver bridge --subnet 172.20.0.0/16 --gateway 172.20.0.1 proxy
docker network create --driver bridge --subnet 172.21.0.0/16 --gateway 172.21.0.1 media-backend
docker network create --driver bridge --subnet 172.22.0.0/16 --gateway 172.22.0.1 monitoring-net
docker network create --driver bridge --subnet 172.23.0.0/16 --gateway 172.23.0.1 security-net
docker network create --driver bridge --subnet 172.24.0.0/16 --gateway 172.24.0.1 utils-net
```

-----

## :material-file-code: .env Template

```bash
# Database passwords
DB_PASSWORD=change-me-to-secure-password
POSTGRES_PASSWORD=change-me-to-secure-password
REDIS_PASSWORD=change-me-to-secure-password

# API Keys
PLEX_TOKEN=your-plex-token
TMDB_API_KEY=your-tmdb-key

# Authentik
AUTHENTIK_SECRET_KEY=generate-random-50-char-string
AUTHENTIK_POSTGRESQL_PASSWORD=change-me-to-secure-password

# Domain
DOMAIN=anthonychild.com

# Timezone
TZ=America/New_York

# User/Group IDs
PUID=1000
PGID=1000
```

-----

## :material-bug: Debug Snippets

### View Container Logs

```bash
# Follow logs
docker logs -f <container-name>

# Last 100 lines
docker logs --tail=100 <container-name>

# With timestamps
docker logs -t <container-name>

# From last 10 minutes
docker logs --since 10m <container-name>
```

### Inspect Container

```bash
# Full details
docker inspect <container-name>
{% raw %}
# Just IP address
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}' <container-name>
{% endraw %}
# Environment variables
docker inspect <container-name> | grep -A 20 Env

# Networks
docker inspect <container-name> | grep -A 10 Networks
```

### Network Troubleshooting

```bash
# Test connectivity between containers
docker exec <container1> ping <container2>

# Check DNS resolution
docker exec <container> nslookup <hostname>

# Test HTTP connection
docker exec <container> curl http://<other-container>:port
{% raw %}
# Check which containers on network
docker network inspect proxy --format '{{range .Containers}}{{.Name}}'
{% endraw %}
```

-----

## :material-folder: Directory Structure

### Standard Stack Layout

```text
docker/
└── stack-name/
    ├── docker-compose.yml
    ├── .env
    ├── service1/
    │   ├── config/
    │   └── data/
    ├── service2/
    │   ├── config/
    │   └── data/
    └── README.md
```

-----

## :material-star: Pro Tips

!!! tip "Use .env files"
    Keep secrets in `.env` files (and add to `.gitignore`):
    `yaml environment: - API_KEY=${API_KEY}  # From .env`

!!! tip "Version pinning"
    Use specific versions in production:
    `yaml image: postgres:16  # Not :latest`

!!! tip "Resource limits"
    Set limits to prevent resource hogging:
    `yaml deploy: resources: limits: cpus: '0.5' memory: 512M`

!!! tip "Health checks"
    Add health checks for critical services:
    `yaml healthcheck: test: ["CMD", "curl", "-f", "http://localhost:8080/health"] interval: 30s timeout: 10s retries: 3`

-----

<div class="center" markdown>

**Copy, customize, deploy!** :material-rocket:

*For full examples, see [Services](../homelab/services.md)*

</div>
