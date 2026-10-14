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

Baseline build artifacts are temporarily available at
`/private/tmp/docs-baseline-wiki` and `/private/tmp/docs-baseline-blog` on
the development machine. Migration builds are in `wiki/site/` and
`blog/site/` (ignored by Git).

## Review before deployment

- Zensical places blog post tags below the article rather than above it.
  Tag listings also omit the previous heading permalink symbols.
- Check desktop and mobile navigation, theme switching, search, custom
  CSS, lightboxes, Mermaid, MathJax, and external/download link behavior
  in a browser. Screenshots have not been captured.
- Run the Docker builds and preview through nginx. Docker and nginx
  were unavailable in the development environment; the flattened build
  check does not replace a container build.
- Run CI lint, spellcheck, and outbound link checks. Local link validation
  checked file targets, not remote availability or anchor fragments.

## Deployment and rollback

Review the branch and validation results before merging. A push to `main`
triggers the existing deployment pipelines; shared build changes now
trigger both sites. No merge, push, or deployment has been performed.

Retain the current production image versions before deployment. If needed,
restore those images and revert the migration changes to return to the
MkDocs build. Keep TOML conversion and modern theme adoption separate.
