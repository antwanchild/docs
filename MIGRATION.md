# Zensical migration

## Completed

The migration and follow-up work are complete:

- [PR #60](https://github.com/antwanchild/docs/pull/60) migrated both sites
  from Material for MkDocs to Zensical.
- [PR #61](https://github.com/antwanchild/docs/pull/61) adopted the modern theme.
- [PR #62](https://github.com/antwanchild/docs/pull/62) converted both sites
  to native `zensical.toml` configuration.

All three changes passed validation and published new Docker images.
The site owner confirmed that both containers were refreshed and both live
sites were verified on October 13, 2026 (America/Boise).

Both sites now use Zensical 0.0.70, the modern theme, and TOML configuration.
The original migration initially retained YAML and the classic theme;
those were replaced by the subsequent PRs. See
[ZENSICAL-FOLLOWUP.md](ZENSICAL-FOLLOWUP.md) for follow-up validation.

## Validation completed

- MkDocs strict baseline builds passed with Material 9.7.7.
- Zensical strict clean builds passed in a fresh Python 3.12 environment
  containing only `requirements.shared.txt` and its dependencies.
- Both builds also passed with the flattened source layout used by the
  Docker builder, including the shared environment helper.
- All baseline HTML paths were preserved: 21 wiki pages and 13 blog pages,
  including post, category, archive, author, and tag pages.
- Generated pages contained no missing local link or asset targets.
- Wiki article text matched the baseline. Blog article differences were
  tag placement and tag listing permalink symbols.
- Service links, email links, dates, recipe contributor metadata, custom
  404 content, and generated search assets were verified in the output.
- Workflow YAML parsed successfully, and `git diff --check` passed.
- Chrome checks passed for both sites: matching search results, light/dark
  theme switching, mobile navigation, and custom 404 content. Wiki checks
  also verified three rendered Mermaid diagrams, two MathJax expressions,
  and external link attributes; blog checks verified recipe metadata.
  No browser exceptions occurred. Desktop/mobile screenshots were captured
  at `/private/tmp/docs-browser-validation`.
- PR validation passed for both sites on GitHub Actions: strict site builds,
  Markdown lint, actual Docker builds, nginx configuration, homepage/search
  and script serving, custom 404 status/content, health-check commands,
  and outbound links. Workflow lint also passed.

## Compatibility notes

Zensical places blog tags below posts, and tag listings omit the previous
heading permalink symbols. These differences were reviewed during migration.
Local file-target checks did not validate anchor fragments; CI also ran
outbound link checks using the existing lychee configuration.

## Deployment and rollback

A push to `main` runs the existing image publication workflows. Shared
build changes trigger both sites. Refresh the homelab containers to pick
up new images unless an automatic updater handles this.

The image references below are historical rollback points from before
PR #60, not the currently running Zensical images.

The pre-migration wiki and blog publication runs were on July 19,
2026 (America/Boise), with the tag `2026.07.19`. Their manifest digests
provide fixed rollback references even if tags are overwritten:

- Wiki: `ghcr.io/antwanchild/wiki@sha256:aa637975e7ddd4bc5d5ff723b387075f7255352174f3d135cf6daad38afa5c7f`
- Blog: `ghcr.io/antwanchild/blog@sha256:ab332a34cbf0e3b905d951c023ed53b05ae9444144f57d8ebd793140fcbdb6fc`

Sources: [wiki build](https://github.com/antwanchild/docs/actions/runs/29714406146)
and [blog build](https://github.com/antwanchild/docs/actions/runs/29714397196).
These references were recovered from build logs, not verified against
running production containers or pulled from the private registry.

If needed, configure the homelab deployment to use these image references
and recreate the containers. Revert the migration changes to restore the
MkDocs build pipeline. Theme and TOML conversion were delivered in separate PRs.
