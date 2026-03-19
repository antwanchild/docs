import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".env")

if env_path.exists():
    load_dotenv(dotenv_path=env_path)

def define_env(env):

    domain = os.getenv("DOMAIN", "anthonychild.com")
    env.variables["domain"] = domain

    author = os.getenv("AUTHOR", "Anthony Child")
    env.variables["author"] = author

    current_year = os.getenv("CURRENT_YEAR", "2026")
    env.variables["current_year"] = current_year

    @env.macro
    def service_url(service: str) -> str:
        subdomains = {
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
        subdomain = subdomains.get(service.lower(), service.lower())
        url = f"https://{subdomain}.{domain}"
        return url

    @env.macro
    def email_link(text: str = "Contact Me") -> str:
        email = os.getenv("EMAIL", "anthony@anthonychild.com")
        display = email[::-1]
        return f'<a href="mailto:{email}">{text}</a> <small>(reverse: {display})</small>'
