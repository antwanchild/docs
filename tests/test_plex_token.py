"""Exercise the standalone token generator with simulated Plex responses."""

from dataclasses import dataclass, field
import re
from urllib.parse import parse_qs, urlsplit

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.browser
TEST_TOKEN = "synthetic-token-for-browser-tests"


@dataclass
class PlexResponses:
    """Control simulated API responses and record outgoing requests."""

    calls: list = field(default_factory=list)
    unexpected: list = field(default_factory=list)
    poll_result: dict = field(default_factory=lambda: {"authToken": None})
    fail_pin: bool = False
    fail_next_poll: bool = False
    fail_user: bool = False

    def route(self, route, local_origin):
        """Fulfill simulated Plex endpoints and block unexpected external traffic."""
        request = route.request
        url = urlsplit(request.url)
        if request.url.startswith(local_origin + "/"):
            route.continue_()
            return
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        }
        if url.hostname == "plex.tv" and request.method == "OPTIONS":
            route.fulfill(status=204, headers=headers)
            return
        self.calls.append({"url": request.url, "method": request.method,
                           "headers": request.headers})
        if url.hostname == "app.plex.tv" and url.path == "/auth":
            route.fulfill(content_type="text/html", body="<title>Simulated Plex login</title>")
        elif url.hostname == "plex.tv" and url.path == "/api/v2/pins":
            if self.fail_pin:
                route.abort("failed")
            else:
                route.fulfill(json={"id": 42, "code": "TEST-PIN"}, headers=headers)
        elif url.hostname == "plex.tv" and url.path == "/api/v2/pins/42":
            failure = self.fail_next_poll
            self.fail_next_poll = False
            self.respond(route, self.poll_result, headers, failure)
        elif url.hostname == "plex.tv" and url.path == "/api/v2/user":
            if self.fail_user:
                route.abort("failed")
            else:
                route.fulfill(json={
                    "username": "test-user", "email": "test-user@example.test", "id": 123,
                    "subscription": {"active": True, "plan": "lifetime"},
                    "joinedAt": 1609502400,
                }, headers=headers)
        else:
            self.unexpected.append(request.url)
            route.abort("blockedbyclient")

    @staticmethod
    def respond(route, payload, headers, failure):
        """Deliver a polling response or simulate a transport failure."""
        if failure:
            route.abort("failed")
        else:
            route.fulfill(json=payload, headers=headers)


@pytest.fixture(name="plex")
def plex_fixture(page, site_urls):
    """Open the generator with intercepted Plex requests and a controllable clock."""
    responses = PlexResponses()
    # Intercept every request, including new tabs, before visiting the page.
    # Only the local server is contacted; no request reaches a Plex service.
    page.context.route("**/*", lambda route: responses.route(route, site_urls["wiki"]))
    page.clock.install()
    response = page.goto(site_urls["wiki"] + "/plex-token.html")
    assert response.status == 200
    expect(page.get_by_role("heading", name="Plex Token Generator")).to_be_visible()
    expect(page.locator("#result-container")).to_be_hidden()
    yield responses
    assert not responses.unexpected, responses.unexpected


def start(page, app="Homepage"):
    """Select an app and request its simulated authorization PIN."""
    page.locator("#app-select").select_option(app)
    page.get_by_role("button", name="Authenticate with Plex").click()
    expect(page.locator("#pin-display")).to_have_text("TEST-PIN")
    expect(page.locator("#pin-container")).to_be_visible()


def authorize(page, plex):
    """Return a synthetic token on the next polling interval."""
    plex.poll_result = {"authToken": TEST_TOKEN}
    page.clock.fast_forward(2000)
    expect(page.locator("#result-container")).to_be_visible()
    expect(page.locator("#token-box")).to_have_text(TEST_TOKEN)


@pytest.mark.parametrize("selection, custom, message", [
    (None, None, "Please select an app before continuing."),
    ("other", "", "Please enter an app name."),
    ("other", "   ", "Please enter an app name."),
])
def test_invalid_app_does_not_contact_plex(page, plex, selection, custom, message):
    """Invalid app does not contact plex."""
    if selection:
        page.locator("#app-select").select_option(selection)
        expect(page.locator("#custom-app-name")).to_be_visible()
        page.locator("#custom-app-name").fill(custom)
    page.get_by_role("button", name="Authenticate with Plex").click()
    expect(page.locator("#status-message")).to_have_text(message)
    expect(page.locator("#auth-btn")).to_be_enabled()
    expect(page.locator("#pin-container")).to_be_hidden()
    assert not plex.calls


@pytest.mark.parametrize("app", ["Homepage", "Kometa", "Unmanic", "My App & Tools"])
def test_pin_request_and_authorization_link(page, plex, app):
    """Pin request and authorization link."""
    if app == "My App & Tools":
        page.locator("#app-select").select_option("other")
        page.locator("#custom-app-name").fill("  " + app + "  ")
        page.get_by_role("button", name="Authenticate with Plex").click()
        expect(page.locator("#pin-display")).to_have_text("TEST-PIN")
    else:
        start(page, app)
    pin = next(call for call in plex.calls if call["method"] == "POST")
    assert parse_qs(urlsplit(pin["url"]).query) == {"strong": ["true"]}
    assert pin["headers"]["x-plex-product"] == app
    client = pin["headers"]["x-plex-client-identifier"]
    uuid_pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
    assert re.fullmatch(uuid_pattern, client)
    link = page.get_by_role("link", name="Authorize with Plex")
    url = urlsplit(link.get_attribute("href"))
    assert (url.scheme, url.netloc, url.path) == ("https", "app.plex.tv", "/auth")
    params = parse_qs(url.fragment.lstrip("?"))
    assert params["clientID"] == [client]
    assert params["code"] == ["TEST-PIN"]
    assert params["context[device][product]"] == [app]
    with page.expect_popup() as popup:
        link.click()
    popup.value.wait_for_load_state()
    expect(popup.value).to_have_title("Simulated Plex login")
    popup.value.close()
    expect(page.locator("#result-container")).to_be_hidden()


def test_authorized_token_profile_clipboard_and_reset(page, plex, site_urls):
    """Authorized token profile clipboard and reset."""
    page.context.grant_permissions(["clipboard-read", "clipboard-write"], origin=site_urls["wiki"])
    start(page, "Kometa")
    authorize(page, plex)
    expect(page.locator("#initial-view")).to_be_hidden()
    expect(page.locator("#app-label")).to_have_text("Kometa")
    expect(page.locator("#username")).to_have_text("test-user")
    expect(page.locator("#email")).to_have_text("test-user@example.test")
    expect(page.locator("#userid")).to_have_text("123")
    expect(page.locator("#plexpass")).to_have_text("Lifetime ✓")
    expect(page.locator("#joinedat")).to_have_text("January 1, 2021")
    user_request = next(call for call in plex.calls if call["url"].endswith("/user"))
    poll_request = next(call for call in plex.calls if call["url"].endswith("/pins/42"))
    assert poll_request["method"] == "GET"
    assert user_request["method"] == "GET"
    client = plex.calls[0]["headers"]["x-plex-client-identifier"]
    assert poll_request["headers"]["x-plex-client-identifier"] == client
    assert user_request["headers"]["x-plex-token"] == TEST_TOKEN
    assert user_request["headers"]["x-plex-client-identifier"] == client
    page.get_by_title("Copy to clipboard").click()
    expect(page.locator("#copy-status")).to_be_visible()
    assert page.evaluate("navigator.clipboard.readText()") == TEST_TOKEN
    page.clock.fast_forward(3000)
    expect(page.locator("#copy-status")).to_be_hidden()
    page.get_by_role("button", name="Generate Another Token").click()
    expect(page.locator("#result-container")).to_be_hidden()
    expect(page.locator("#auth-btn")).to_be_visible()
    expect(page.locator("#auth-btn")).to_be_enabled()
    expect(page.locator("#app-select")).to_have_value("")
    expect(page.locator("#custom-app-name")).to_have_value("")
    expect(page.locator("#pin-container")).to_be_hidden()
    calls = len(plex.calls)
    page.clock.fast_forward(4000)
    assert len(plex.calls) == calls  # Successful authorization stops polling.


def test_timeout_stops_polling_and_allows_retry(page, plex):
    """Timeout stops polling and allows retry."""
    start(page)
    page.clock.fast_forward(300000)
    expect(page.locator("#status-message")).to_have_text(
        "Authentication timed out. Please try again.",
    )
    expect(page.locator("#pin-container")).to_be_hidden()
    expect(page.locator("#auth-btn")).to_be_enabled()
    calls = len(plex.calls)
    page.clock.fast_forward(4000)
    assert len(plex.calls) == calls
    start(page, "Unmanic")
    authorize(page, plex)
    expect(page.locator("#app-label")).to_have_text("Unmanic")


def test_pin_network_failure_can_be_retried(page, plex):
    """Pin network failure can be retried."""
    plex.fail_pin = True
    page.locator("#app-select").select_option("Homepage")
    page.get_by_role("button", name="Authenticate with Plex").click()
    expect(page.locator("#status-message")).to_contain_text("Failed to contact Plex")
    expect(page.locator("#auth-btn")).to_be_enabled()
    expect(page.locator("#pin-container")).to_be_hidden()
    plex.fail_pin = False
    start(page)
    authorize(page, plex)


def test_transient_polling_failure_keeps_waiting(page, plex):
    """Transient polling failure keeps waiting."""
    plex.fail_next_poll = True
    start(page)
    with page.expect_event("requestfailed"):
        page.clock.fast_forward(2000)
    expect(page.locator("#pin-container")).to_be_visible()
    expect(page.locator("#result-container")).to_be_hidden()
    authorize(page, plex)


def test_profile_failure_preserves_the_token(page, plex):
    """Profile failure preserves the token."""
    plex.fail_user = True
    start(page)
    authorize(page, plex)
    expect(page.locator("#username")).to_have_text("Authenticated")
    for field_name in ("email", "userid", "plexpass", "joinedat"):
        expect(page.locator("#" + field_name)).to_have_text("N/A")
    expect(page.locator("#token-box")).to_have_text(TEST_TOKEN)


def test_clipboard_rejection_uses_fallback(page, plex):
    """Clipboard rejection uses fallback."""
    start(page)
    authorize(page, plex)
    page.evaluate("""() => {
      Object.defineProperty(navigator, 'clipboard', {
        value: {writeText: () => Promise.reject(new Error('Simulated denial'))}
      });
      document.execCommand = command => {
        if (command === 'copy') window.fallbackCopy = document.querySelector('textarea').value;
        return true;
      };
    }""")
    page.get_by_title("Copy to clipboard").click()
    expect(page.locator("#copy-status")).to_be_visible()
    assert page.evaluate("window.fallbackCopy") == TEST_TOKEN
    expect(page.locator("textarea")).to_have_count(0)
