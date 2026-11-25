# Changelog

All notable changes to the wiki are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Releases use `wiki-YYYY.MM`, followed by `.1`, `.2`, and so on for further
releases in the same month.

History below summarizes changes between monthly release tags, checked against
Git history. Dates use the GitHub release publication date (UTC). Earlier daily
and test releases remain in [GitHub Releases](https://github.com/antwanchild/docs/releases).
`Unreleased` means changes since the latest tagged release; some may already be
available in published Docker images.

## [Unreleased]

## [wiki-2026.11.1] - 2026-11-24

### Changed

- Use cached uv installs in CI, replace Super-Linter with focused lint commands,
  and report GitHub Actions security findings with zizmor.

## [wiki-2026.11] - 2026-11-24

### Added

- Add a dedicated changelog with curated release notes for the wiki.
- Enable AI-friendly exports and redirects.
- Add automated browser coverage for navigation, search, themes, rendering, and
  the Plex token generator.

### Changed

- Automatically release notable wiki changes after successful builds, choosing
  the next available monthly version and archiving pending changelog entries.

- Migrate from MkDocs to Zensical with the modern theme and native TOML configuration.
- Refresh homelab networking, Compose stacks, service inventory, and overview pages.
- Update the Discord Cleanup Bot deployment guide, bookmarks, projects, general
  notes, and planning wishlist.
- Extract the Plex token generator's styles and script into separate assets.
- Load MathJax only on pages containing mathematical notation.
- Enable privacy features for external assets.
- Add deployment revision reporting and a separate manual workflow to verify
  published sites, including reporting when Anubis blocks verification.
- Recover missed site builds and standardize Discord build and release alerts.
- Publish monthly GitHub release notes from curated changelog sections.

### Fixed

- Disable unstable instant navigation.
- Prevent Jinja from parsing a Docker format expression in the stack guide.
- Revalidate custom Plex token generator assets so visitors receive updates promptly.

### Security

- Harden Docker provenance and vulnerability scanning, and update runtime packages
  to address scanner findings.

## [wiki-2026.07] - 2026-07-20

### Changed

- Share environment loading between both sites and split shared and site dependencies.
- Refine wiki macros.

### Fixed

- Include the shared environment helper in Docker builds and correct its import paths.
- Correct the Docker Compose bookmark.
- Stop passing the GitHub token as a Docker build argument.

## [wiki-2026.04] - 2026-04-01

### Added

- Add a custom 404 page.
- Add Docker health checks for the served site.

### Fixed

- Correct the link checker's base URL and consolidate site build workflows.

## [wiki-2026.03] - 2026-03-13

### Added

- Add the Discord Cleanup Bot project page.

### Changed

- Reorganize wiki navigation and update networking documentation.

### Removed

- Remove the custom favicon.

[wiki-2026.07]: https://github.com/antwanchild/docs/releases/tag/wiki-2026.07
[wiki-2026.04]: https://github.com/antwanchild/docs/releases/tag/wiki-2026.04
[wiki-2026.03]: https://github.com/antwanchild/docs/releases/tag/wiki-2026.03

[wiki-2026.11]: https://github.com/antwanchild/docs/releases/tag/wiki-2026.11

[wiki-2026.11.1]: https://github.com/antwanchild/docs/releases/tag/wiki-2026.11.1
