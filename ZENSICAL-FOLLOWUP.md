# Zensical follow-up plan

## Current progress

The modern-theme preview on `preview-modern-theme` has been reviewed and
approved for adoption.
Both strict builds pass. All 34 HTML paths and article text match the
classic builds. Chrome checks passed for search, theme switching, mobile
navigation, Mermaid, MathJax, recipe metadata, custom 404 content, and
external link behavior, with no browser exceptions.

Screenshots are in `/private/tmp/docs-modern-preview`, including desktop
and mobile views of both sites. No CSS adjustments were needed for the
reviewed views. The theme change proceeds through a separate PR and the existing site
validation workflow. TOML conversion remains a separate follow-up.

## 1. Preview the modern theme

- Work on `preview-modern-theme`, retaining the YAML configuration.
- Save the classic build as a comparison baseline and enable `modern` on
  both sites.
- Build both sites in strict mode and compare page URLs and article text.
- Check desktop/mobile layout, navigation, search, palettes, wiki CSS,
  diagrams, math, recipe metadata, custom 404s, and external links.
- Capture screenshots for review. Decide whether to adopt the modern
  appearance after reviewing the preview.
- If adopted, open a theme-only PR, run container/CI checks, and merge.
  Roll back by restoring `variant: classic`.

## 2. Convert configuration to TOML separately

- Branch from the chosen theme baseline so visual changes are isolated.
- Convert both `mkdocs.yml` files to `zensical.toml`, preserving project
  settings, navigation, palettes, features, extensions, plugins, and assets.
- Translate Python callable references using Zensical's supported TOML
  representation and verify custom macro loading.
- Update Dockerfile config copies, build/preview commands, workflow inputs,
  validation commands, and README instructions.
- Compare normalized configuration, HTML URLs, article text, search data,
  blog-generated pages, and representative browser views against YAML.
- Verify both flattened Docker builder layouts and run PR container,
  nginx, lint, and link checks before merging.
- Remove the superseded YAML files only after parity is established.
  Roll back by reverting the configuration conversion PR.

## Completion criteria

Both sites retain existing URLs and content. Strict builds, browser checks,
container checks, and CI pass. The chosen appearance is reviewed before
deployment. TOML conversion introduces no additional visual changes.

Estimated effort: 2–4 hours for theme adoption and 1–3 hours for TOML
conversion, with additional time if preview or compatibility issues arise.
