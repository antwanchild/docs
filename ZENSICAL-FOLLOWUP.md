# Zensical follow-up plan

## Current progress

The modern theme was adopted in PR #61. Both sites now use native TOML
configuration on `convert-zensical-toml`; Docker, CI, and local commands
have been updated, and the superseded YAML files removed.

Both strict TOML builds pass. Zensical's resolved settings exactly match
those of the YAML baseline. All generated files are byte-for-byte identical
(35 wiki files and 24 blog files), including HTML, assets, and search data.
This conversion introduces no visual or content changes.

Browser checks passed for both sites with no exceptions. Both flattened
Docker builder layouts also build successfully. Actual container, nginx,
lint, and outbound-link checks run in the separate TOML PR.
Rollback by reverting that PR to restore YAML configurations and commands.

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
