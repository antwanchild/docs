"""Contracts for the custom site macros, independent of Zensical internals."""

import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

import mkdocs_env

ROOT = Path(__file__).resolve().parents[1]


# This test double implements only the macro registration hook.
class MacroEnvironment:  # pylint: disable=too-few-public-methods
    """Capture functions registered by the public define_env hook."""

    def __init__(self, meta=None):
        """Initialize the minimal registration and page metadata interface."""
        self.variables = {}
        self.macros = {}
        self.page = SimpleNamespace(meta=meta or {})

    def macro(self, function):
        """Register a macro and preserve decorator behavior."""
        self.macros[function.__name__] = function
        return function


@pytest.fixture(name="define_env")
def macro_loader_fixture(monkeypatch):
    """Load site macros without reading developer environment files."""
    # Importing the real modules must never load the developer's .env.
    monkeypatch.setattr(mkdocs_env, "load_site_env", lambda: None)
    for name in ("DOMAIN", "AUTHOR", "EMAIL"):
        monkeypatch.delenv(name, raising=False)

    def load(site, meta=None):
        """Create a fresh site macro environment for each test."""
        spec = importlib.util.spec_from_file_location(
            f"test_{site}_macros", ROOT / site / "main.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        env = MacroEnvironment(meta)
        module.define_env(env)
        return env

    return load


@pytest.mark.parametrize("site", ["wiki", "blog"])
def test_site_defaults(define_env, site):
    """Site defaults."""
    env = define_env(site)
    assert env.variables["domain"] == "anthonychild.com"
    assert env.variables["author"] == "Anthony Child"
    assert 'mailto:anthony@anthonychild.com' in env.macros["email_link"]()


@pytest.mark.parametrize("site", ["wiki", "blog"])
def test_environment_overrides(define_env, monkeypatch, site):
    """Environment overrides."""
    monkeypatch.setenv("DOMAIN", "example.test")
    monkeypatch.setenv("AUTHOR", "Example Author")
    monkeypatch.setenv("EMAIL", "hello@example.test")
    env = define_env(site)
    assert env.variables["domain"] == "example.test"
    assert env.variables["author"] == "Example Author"
    link = env.macros["email_link"]("Write to me")
    assert '<a href="mailto:hello@example.test">Write to me</a>' in link
    assert 'tset.elpmaxe@olleh' in link


@pytest.mark.parametrize("service, subdomain", [
    ("DOCS", "wiki"), ("dozzle", "logs"), ("immich", "photos"),
    ("radarr", "movies"), ("MyService", "myservice"),
])
def test_service_links_use_aliases_and_custom_domain(
    define_env, monkeypatch, service, subdomain,
):
    """Service links use aliases and custom domain."""
    monkeypatch.setenv("DOMAIN", "example.test")
    env = define_env("wiki")
    assert env.macros["service_url"](service) == f"https://{subdomain}.example.test"


def test_recipe_optional_metadata(define_env):
    """Recipe optional metadata."""
    env = define_env("blog", {
        "prep_time": "15 minutes", "cook_time": "45 minutes", "servings": 6,
        "yield": "one pan", "difficulty": "Easy", "contributor": "Recipe Contributor",
        "recipe_author": "Fallback Author",
    })
    result = env.macros["recipe_header"]()
    for text in (
        "**Prep Time:** 15 minutes", "**Cook Time:** 45 minutes",
        "**Servings:** 6", "**Yield:** one pan", "**Difficulty:** Easy",
        "**Recipe by:** Recipe Contributor",
    ):
        assert text in result
    assert "Fallback Author" not in result


@pytest.mark.parametrize("meta, expected", [
    ({"recipe_author": "Fallback Author"}, "**Recipe by:** Fallback Author"),
    ({"prep_time": None, "cook_time": "", "servings": None}, None),
    ({}, None),
])
def test_recipe_missing_fields_and_author_fallback(define_env, meta, expected):
    """Recipe missing fields and author fallback."""
    result = define_env("blog", meta).macros["recipe_header"]()
    if expected:
        assert expected in result
    else:
        assert "**Recipe by:**" not in result
    assert "**Prep Time:**" not in result
    assert "**Cook Time:**" not in result
    assert "**Servings:**" not in result
    assert "None" not in result


def test_dotenv_preserves_existing_environment(tmp_path, monkeypatch):
    """Dotenv preserves existing environment."""
    monkeypatch.setenv("DOMAIN", "existing.test")
    monkeypatch.delenv("AUTHOR", raising=False)
    path = tmp_path / ".env"
    path.write_text("DOMAIN=file.test\nAUTHOR=From file\n")
    mkdocs_env.load_site_env(str(path))
    assert os.environ["DOMAIN"] == "existing.test"
    assert os.environ["AUTHOR"] == "From file"


def test_missing_dotenv_is_optional(tmp_path):
    """Missing dotenv is optional."""
    mkdocs_env.load_site_env(str(tmp_path / "missing.env"))
