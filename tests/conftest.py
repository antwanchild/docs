"""Build isolated sites and serve them to the browser tests."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from threading import Thread

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    """Keep successful HTTP requests out of the test output."""

    def log_message(self, format, *args):
        pass


@pytest.fixture(scope="session")
def built_sites(tmp_path_factory):
    """Build from copied sources, without copying local secrets or caches."""
    root = tmp_path_factory.mktemp("sites")
    shutil.copy2(ROOT / "mkdocs_env.py", root / "mkdocs_env.py")
    env = {**os.environ, "DOMAIN": "example.test", "AUTHOR": "Test Author",
           "EMAIL": "contact@example.test"}
    for site in ("wiki", "blog"):
        project = root / site
        shutil.copytree(
            ROOT / site / "docs", project / "docs",
            ignore=shutil.ignore_patterns("._*", ".DS_Store"),
        )
        for filename in ("zensical.toml", "main.py"):
            shutil.copy2(ROOT / site / filename, project / filename)
        subprocess.run(
            [sys.executable, "-m", "zensical", "build", "--strict"],
            cwd=project, env=env, check=True,
        )
    return root


@pytest.fixture(scope="session")
def site_urls(built_sites):
    servers = []
    urls = {}
    for site in ("wiki", "blog"):
        handler = partial(QuietHandler, directory=str(built_sites / site / "site"))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        servers.append((server, thread))
        urls[site] = f"http://127.0.0.1:{server.server_port}"
    yield urls
    for server, thread in servers:
        server.shutdown()
        server.server_close()
        thread.join()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        options = {}
        if os.getenv("BROWSER_EXECUTABLE"):
            options["executable_path"] = os.environ["BROWSER_EXECUTABLE"]
        instance = playwright.chromium.launch(**options)
        yield instance
        instance.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"report_{call.when}", outcome.get_result())


@pytest.fixture
def page(browser, request):
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    instance = context.new_page()
    instance.set_default_timeout(20000)
    errors = []
    instance.on("pageerror", lambda error: errors.append(str(error)))
    yield instance
    report = getattr(request.node, "report_call", None)
    if (report and report.failed) or errors:
        output = ROOT / "test-results"
        output.mkdir(exist_ok=True)
        name = re.sub(r"[^A-Za-z0-9_-]", "_", request.node.nodeid)
        instance.screenshot(path=str(output / f"{name}.png"), full_page=True)
    context.close()
    assert not errors, f"Uncaught browser exceptions: {errors}"
