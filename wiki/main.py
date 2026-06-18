import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".env")
SERVICE_SUBDOMAINS = {
    "authentik": "authentik",
    "blog": "blog",
    "docs": "wiki",
    "dozzle": "logs",
    "files": "files",
    "homepage": "home",
    "immich": "photos",
    "notifiarr": "notifiarr",
    "plex": "plex",
    "posterizarr": "posterizarr",
    "privatebin": "bin",
    "prowlarr": "manager",
    "radarr": "movies",
    "sabnzbd": "sabnzb",
    "seerr": "requests",
    "sonarr": "series",
    "starr": "starr",
    "tautulli": "tautulli",
    "titlecards": "cards",
    "traefik": "traefik",
    "unmanic": "transcode",
}

if env_path.exists():
    load_dotenv(dotenv_path=env_path)

def define_env(env):

    domain = os.getenv("DOMAIN", "anthonychild.com")
    env.variables["domain"] = domain

    author = os.getenv("AUTHOR", "Anthony Child")
    env.variables["author"] = author

    env.variables["current_year"] = str(datetime.now().year)

    @env.macro
    def service_url(service: str) -> str:
        subdomain = SERVICE_SUBDOMAINS.get(service.lower(), service.lower())
        url = f"https://{subdomain}.{domain}"
        return url

    @env.macro
    def email_link(text: str = "Contact Me") -> str:
        email = os.getenv("EMAIL", "anthony@anthonychild.com")
        display = email[::-1]
        return f'<a href="mailto:{email}">{text}</a> <small>(reverse: {display})</small>'
