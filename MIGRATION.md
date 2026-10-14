# Zensical migration

The `migrate-zensical` branch replaces Material for MkDocs with Zensical
0.0.70 for both sites. It retains `mkdocs.yml`, the classic theme, existing
content, custom macros, and nginx serving configuration.

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

Baseline build artifacts are temporarily available at
`/private/tmp/docs-baseline-wiki` and `/private/tmp/docs-baseline-blog` on
the development machine. Migration builds are in `wiki/site/` and
`blog/site/` (ignored by Git).

## Review before deployment

- Zensical places blog post tags below the article rather than above it.
  Tag listings also omit the previous heading permalink symbols.
- Review the captured screenshots and the successful PR checks.
- The latest successful production build logs provide the rollback image
  references below. These are the last published images; the running
  containers were not inspected directly. GHCR requires authentication.
- The local file-target check did not validate anchor fragments; the PR
  also ran the existing lychee outbound-link configuration.

## Deployment and rollback

Review the branch and validation results before merging. A push to `main`
triggers the existing deployment pipelines; shared build changes now
trigger both sites. The migration is reviewed in PR #60. Merging publishes new images through
the existing production workflows.

The latest successful wiki and blog publication runs were on July 19,
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
MkDocs build pipeline. Keep TOML conversion and modern theme adoption
separate.
