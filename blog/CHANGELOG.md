# Changelog

All notable changes to the blog are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Releases use the `blog-YYYY.MM` calendar version format.

History below summarizes changes between monthly release tags, checked against
Git history. Dates use the GitHub release publication date (UTC). Earlier daily
and test releases remain in [GitHub Releases](https://github.com/antwanchild/docs/releases).

## [Unreleased]

### Added

- Add a dedicated changelog with curated release notes for the blog.

### Changed

- Use cached uv installs in CI, replace Super-Linter with focused lint commands,
  and report GitHub Actions security findings with zizmor.
- Complete and publish "Long Time No See...", with reading time displayed.
- Add deployment revision reporting and a separate manual workflow to verify
  published sites, including reporting when Anubis blocks verification.
- Recover missed site builds and standardize Discord build and release alerts.
- Publish monthly GitHub release notes from curated changelog sections.

## [blog-2026.10] - 2026-10-27

### Added

- Enable native social cards, RSS feeds, and redirects.
- Introduce the draft of "Long Time No See...", dated September 21.

### Changed

- Migrate from MkDocs to Zensical with the modern theme and native TOML configuration.
- Refresh the Discord Cleanup Bot article and standardize the lasagna, chile verde,
  and pozole recipes.
- Enable privacy features for external assets.

### Fixed

- Disable unstable instant navigation.

## [blog-2026.07] - 2026-07-20

### Changed

- Share environment loading between both sites and split shared and site dependencies.
- Refine site macros and correct recipe table formatting.

### Fixed

- Include the shared environment helper in Docker builds and correct its import paths.

## [blog-2026.04] - 2026-04-01

### Added

- Add the Discord Cleanup Bot article.
- Add Docker health checks for the served site.

### Changed

- Update category URL formatting and the custom 404 page.

### Fixed

- Correct the Discord Cleanup Bot article and its links.

### Removed

- Remove the custom favicon.

## [blog-2026.03] - 2026-03-03

### Changed

- Exercise the monthly release workflow with temporary test posts; this release
  contains no notable reader-facing additions.

[blog-2026.10]: https://github.com/antwanchild/docs/releases/tag/blog-2026.10
[blog-2026.07]: https://github.com/antwanchild/docs/releases/tag/blog-2026.07
[blog-2026.04]: https://github.com/antwanchild/docs/releases/tag/blog-2026.04
[blog-2026.03]: https://github.com/antwanchild/docs/releases/tag/blog-2026.03
