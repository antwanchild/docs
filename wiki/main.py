import os
from pathlib import Path
from dotenv import load_dotenv

print("Loading main.py – macros plugin found this file!")

# Load .env from the utilities folder (one level up from docs/)
env_path = Path("/docs/.env") #/ ".." / ".env"
print(f"Looking for .env at: {env_path}")

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print("✅ .env file FOUND and loaded")
else:
    print("⚠️ .env file NOT FOUND – using fallback values")

def define_env(env):
    print("define_env called – setting variables and macros")

    # Public variables with fallbacks
    domain = os.getenv("DOMAIN", "anthonychild.com")
    env.variables["domain"] = domain
    print(f"Domain set to: {domain}")

    author = os.getenv("AUTHOR", "Anthony Child")
    env.variables["author"] = author
    # print(f"Author set to: {author}")    

    current_year = os.getenv("CURRENT_YEAR", "2025")
    env.variables["current_year"] = current_year

    # Service URL macro
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
            "seerr": "flix",
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

    # Email link macro
    @env.macro
    def email_link(text: str = "Contact Me") -> str:
        email = os.getenv("EMAIL", "anthony@anthonychild.com")
        display = email[::-1]  # Light anti-spam
        return f'<a href="mailto:{email}">{text}</a> <small>(reverse: {display})</small>'

    print("All variables and macros defined successfully")