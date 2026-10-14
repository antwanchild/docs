# Zensical follow-up: completed

The modern theme and TOML configuration changes are complete. Both Docker
images were published, and the site owner confirmed container refresh and
live checks on October 13, 2026 (America/Boise).

## Modern theme — PR #61

[PR #61](https://github.com/antwanchild/docs/pull/61) adopted the reviewed
modern appearance for both sites while retaining YAML configuration.
All 34 HTML paths and article text matched the classic baseline. Strict
builds, desktop/mobile browser checks, container builds, nginx checks,
lint, and outbound-link validation passed.

No custom CSS changes were needed to adopt the modern theme. Browser
checks covered search, light/dark switching, mobile navigation, Mermaid,
MathJax, recipes, custom 404s, and external links without exceptions.

Rollback: restore `variant = "classic"` under `[project.theme]` in both
current TOML configurations, then rebuild and refresh the containers.

## TOML configuration — PR #62

[PR #62](https://github.com/antwanchild/docs/pull/62) replaced both YAML
configurations with native `zensical.toml` files. Docker, CI, and local
commands were updated; the reusable workflow input is now `project_dir`.

Zensical resolved YAML and TOML to identical settings. Generated output
was byte-for-byte identical: 35 wiki files and 24 blog files, including
all 34 HTML paths, assets, and search data. Browser checks, flattened
Docker layouts, actual container/nginx checks, lint, and outbound-link
validation passed. No visual or content changes were introduced.

Rollback: revert PR #62 to restore YAML files and corresponding build
commands. The modern theme is independent of this conversion.

## Final state

Both sites use the modern theme and native TOML configuration. Existing
URLs and content were preserved. Automated checks and owner verification
of the live sites passed; no migration tasks remain.
