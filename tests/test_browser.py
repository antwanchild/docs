"""Small smoke tests for the sites' custom behavior and important URLs."""

import re

import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.browser


def visit(page, base, path="/"):
    """Open a successful site page and wait for its JavaScript runtime."""
    response = page.goto(base + path, wait_until="domcontentloaded")
    assert response.status == 200
    expect(page.locator(".md-content")).to_be_visible()
    page.wait_for_function("typeof document$ !== 'undefined'")


def wait_for_instant_navigation(page):
    """Wait for Zensical instant navigation to finish replacing page content."""
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator(".md-content")).to_be_visible()


@pytest.mark.parametrize("site, query", [("wiki", "Plex"), ("blog", "Lasagna")])
def test_search_returns_matching_pages(page, site_urls, site, query):
    """Search returns matching pages."""
    visit(page, site_urls[site])
    page.locator(".md-search__button").click()
    page.get_by_role("combobox", name="Search").fill(query)
    result = page.get_by_role("dialog").locator("a[href]").filter(has_text=query).first
    expect(result).to_be_visible(timeout=20000)
    result.click()
    expect(page).not_to_have_url(site_urls[site] + "/")
    wait_for_instant_navigation(page)
    expect(page.locator(".md-content")).to_contain_text(query)


@pytest.mark.parametrize("site", ["wiki", "blog"])
def test_theme_switching(page, site_urls, site):
    """Theme switching."""
    visit(page, site_urls[site])
    schemes = set()
    for _ in range(4):
        schemes.add(page.locator("body").get_attribute("data-md-color-scheme"))
        toggle = page.locator('.md-header__option label[for^="__palette"]')
        toggle.filter(visible=True).first.click()
    assert {"default", "slate"} <= schemes


@pytest.mark.parametrize("site, target", [("wiki", "bookmarks"), ("blog", "tags")])
def test_mobile_navigation(page, site_urls, site, target):
    """Mobile navigation."""
    page.set_viewport_size({"width": 390, "height": 844})
    visit(page, site_urls[site])
    page.locator('.md-header label[for="__drawer"]').click()
    if site == "wiki":
        page.locator(".md-sidebar--primary label.md-nav__link").filter(
            has_text=re.compile(r"^\s*Resources\s*$"),
        ).click()
    link = page.locator(".md-sidebar--primary a[href]").filter(
        has=page.locator(f':scope[href$="/{target}/"], :scope[href="./{target}/"]'),
    )
    # Match by the resolved URL instead of assuming Zensical emits a specific
    # relative href form. Instant navigation may normalize sidebar links.
    candidates = page.locator(".md-sidebar--primary a[href]")
    target_link = candidates.filter(has_text=re.compile(rf"^\s*{target}\s*$", re.I)).first
    if target_link.count() == 0:
        target_link = page.locator(f'.md-sidebar--primary a[href$="/{target}/"]').first
    target_link.click()
    expect(page).to_have_url(re.compile(f"/{target}/$"))
    wait_for_instant_navigation(page)


def test_wiki_service_links_and_external_link_behavior(page, site_urls):
    """Wiki service links and external link behavior."""
    visit(page, site_urls["wiki"], "/homelab/services/")
    for host in ("wiki", "logs", "photos", "movies"):
        link = page.locator(f'.md-content a[href="https://{host}.example.test"]').first
        expect(link).to_have_attribute("target", "_blank")
        assert "noopener" in link.get_attribute("rel").split()
    internal = page.locator('.md-sidebar--primary a[href$="/bookmarks/"]').first
    expect(internal).not_to_have_attribute("target", "_blank")


def test_wiki_diagrams_math_and_example_block_styles(page, site_urls):
    """Wiki diagrams math and example block styles."""
    visit(page, site_urls["wiki"], "/fun/examples/")
    # Zensical renders SVGs inside closed shadow roots. Nonempty replacement
    # divs distinguish rendered diagrams from their source <pre> elements.
    page.wait_for_function(
        "[...document.querySelectorAll('div.mermaid')].filter("
        "e => e.getBoundingClientRect().height > 40).length === 3",
        timeout=30000,
    )
    expect(page.locator("mjx-container").first).to_be_visible(timeout=30000)
    seen = set()
    for _ in range(3):
        scheme = page.locator("body").get_attribute("data-md-color-scheme")
        expected = "rgb(240, 240, 240)" if scheme == "default" else "rgb(59, 66, 82)"
        actual = page.locator(".custom-block").evaluate(
            "el => getComputedStyle(el).backgroundColor",
        )
        assert actual == expected
        seen.add(scheme)
        toggle = page.locator('.md-header__option label[for^="__palette"]')
        toggle.filter(visible=True).first.click()
    assert {"default", "slate"} <= seen


@pytest.mark.parametrize("path, text", [
    ("/2026/02/05/lasagna---grandmas-recipe/", "Kim Avalos"),
    ("/category/recipe/", "Lasagna"),
    ("/archive/2026/", "Lasagna"),
    ("/author/antwanchild/", "Anthony Child"),
    ("/tags/", "italian"),
])
def test_blog_existing_urls_and_content(page, site_urls, path, text):
    """Blog existing urls and content."""
    visit(page, site_urls["blog"], path)
    expect(page.locator(".md-content")).to_contain_text(text)
    if "lasagna" in path:
        expect(page.locator(".admonition.info")).to_contain_text("Recipe by:")
        expect(page.locator(".admonition.info")).to_contain_text("Kim Avalos")


@pytest.mark.parametrize("site", ["wiki", "blog"])
def test_custom_404_content(page, site_urls, site):
    # Static serving checks the content; CI's nginx check verifies HTTP 404.
    """Custom 404 content."""
    visit(page, site_urls[site], "/404.html")
    expect(page.locator(".md-content")).to_contain_text(
        "This is not the page you're looking for.",
    )
