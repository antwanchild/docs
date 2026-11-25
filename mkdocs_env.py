"""Load optional local environment settings for site macros."""

from pathlib import Path

from dotenv import load_dotenv


def load_site_env(env_filename: str = ".env") -> None:
    """Load the environment file when present."""
    env_path = Path(env_filename)
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
