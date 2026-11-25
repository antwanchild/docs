# docs

Source for my personal wiki and blog, both built with [Zensical](https://zensical.org/) and served via Docker + nginx.

| Site | URL |
|------|-----|
| Wiki | [wiki.anthonychild.com](https://wiki.anthonychild.com) |
| Blog | [blog.anthonychild.com](https://blog.anthonychild.com) |

## Structure

```
docs/
├── wiki/           # Wiki site (Markdown source + config)
├── blog/           # Blog site (Markdown source + config)
├── Dockerfile.wiki
├── Dockerfile.blog
└── .github/
    └── workflows/  # CI/CD pipelines
```

## How it works

Each site is built independently:

1. **Lint & spellcheck** — markdownlint and pyspelling run against the content directory
2. **Docker build** — Zensical builds the static site, nginx serves it; the image is pushed to GHCR
3. **Release** — a versioned Git tag (`wiki-YYYY.MM` / `blog-YYYY.MM`) is created when the site changelog contains an eligible dated release section; that section supplies the release notes
4. **Link check** — lychee scans all outbound links
5. **Notify** — a Discord notification is sent on completion

Pushing to `main` triggers the workflow for whichever site was changed (`wiki/**` or `blog/**`). Changes to shared dependencies, helpers, or the reusable build workflow trigger both pipelines. The two pipelines are independent.

## Changelogs and releases

The [wiki changelog](wiki/CHANGELOG.md) and [blog changelog](blog/CHANGELOG.md)
contain curated, reader-facing descriptions of notable changes. Update the
appropriate `Unreleased` section alongside each meaningful change. Use `Added`,
`Changed`, `Fixed`, `Removed`, `Deprecated`, or `Security` as needed; omit empty
categories and minor typo corrections. Record shared changes in both changelogs
when they affect both sites.

Wiki releases are automatic. Merge notable changes with entries under
`wiki/CHANGELOG.md` → `Unreleased`. After the wiki image build and checks succeed
on the latest `main` revision, CI chooses the next version (`wiki-2026.11`, then
`wiki-2026.11.1`, `.2`, and so on), archives those entries in a dated changelog
section, and publishes the tag and GitHub release notes. No release PR or manual
approval is needed. An empty `Unreleased` section produces no new release.

CI commits only the changelog archive to `main`; repository rules must allow
`github-actions[bot]` to push that commit. The push uses `GITHUB_TOKEN`, so the
archive commit does not trigger another push build. A concurrent update to main
is never overwritten: the newer revision's build handles the pending release.
The version tag points at the revision whose image passed the build checks.
**Actions → Release Wiki** remains available to retry the build manually.

The blog retains one release per month. Move pending entries into a heading such
as `## [blog-2026.11] - 2026-11-24`, leaving an empty `Unreleased` section above it.
A successful blog build publishes that month's section if its tag does not
already exist. The blog's manual `force_release` input requires nonempty curated
notes; it cannot bypass an existing tag. Posts still publish with ordinary builds.

The changelogs summarize monthly releases from Git history and GitHub release
records. Earlier daily and test releases remain in GitHub Releases.

## Deploying published images

Build workflows publish images to GHCR. After a successful build, update the
containers on the server from the directory containing the Compose file:

```bash
docker compose pull
docker compose up -d
```

Then open **Actions → Verify Published Sites → Run workflow** in GitHub.
Choose `both`, `wiki`, or `blog`. Leave `expected_sha` blank to verify the selected
branch or tag revision, or enter the full commit SHA of the image you deployed.
The workflow waits for the live sites to report that revision. Verification runs
separately, so manual deployment does not delay or fail image publication.
An Anubis redirect is reported as blocked verification in the run summary.

## Running locally

**Prerequisites:** Python 3, pip, Docker (optional)

```bash
# Install dependencies (Python 3.12 recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.wiki.txt -r requirements.blog.txt

# Serve one site at a time, from the repository root
zensical serve -f wiki/zensical.toml
zensical serve -f blog/zensical.toml

# Build either site
zensical build --strict -f wiki/zensical.toml
zensical build --strict -f blog/zensical.toml
```

Both sites default to `http://localhost:8000`. Builds write to `wiki/site/` and `blog/site/`. Both sites use native `zensical.toml` configuration and the modern theme.

## Tests

With the virtual environment activated, install the test dependencies and browser once:

```bash
pip install -r requirements.test.txt
python -m playwright install chromium
```

Run the complete suite from the repository root:

```bash
python -m pytest
```

For just the Python macro tests, use `python -m pytest -m "not browser"`.
Lint the test code with `python -m pylint --persistent=n --source-roots=. --ignore-patterns='^\._' tests`.
Browser tests build temporary copies of both sites without loading local
`.env` files, then check search, themes, mobile navigation, wiki rendering,
recipe metadata, and existing blog URLs. Mermaid and MathJax checks require
access to the sites' existing CDN resources. Failure screenshots are saved
in `test-results/` and uploaded by PR CI. To use an installed Chrome instead
of Playwright's Chromium, set `BROWSER_EXECUTABLE` to its executable path.

The Plex token generator tests simulate PIN creation, authorization, polling,
profile lookup, and errors. They also check input validation, timeout/retry,
clipboard copying, and resetting the form. All Plex requests are intercepted;
no real Plex account or credentials are used. Run just these tests with
`python -m pytest tests/test_plex_token.py`.

The generator's markup is in `wiki/docs/plex-token.html`, with styles in
`wiki/docs/css/plex-token.css` and behavior in
`wiki/docs/javascripts/plex-token.js`. nginx revalidates these custom assets
so updates reach visitors without waiting for the general one-year asset cache.

## CI tooling

GitHub Actions uses uv with cached downloads and Python 3.12 environments to
install the existing requirements files. Local pip instructions and Docker builds
remain supported. Dependabot continues to manage dependency updates.

Code Lint runs Pylint, yamllint, and ShellCheck directly. Actionlint checks workflow
syntax and embedded shell scripts. Workflow Security runs zizmor and uploads
findings to GitHub's Security → Code scanning view. GitHub can mark its separate
code-scanning check as failed when changed lines introduce findings, even when
the scanner job succeeds. New findings should be resolved before merging.
The first scan includes existing workflow findings, including action pinning and
permission scope. These tools run on GitHub Actions without an additional hosted
service subscription. The pinning policy permits release tags for setup-uv,
with an exact uv tool version; other actions retain the SHA-pinning policy.

Run the focused checks locally with:

```bash
python -m pylint --persistent=n --source-roots=. --ignore-patterns='^\._' tests
python -m pylint --persistent=n --disable=duplicate-code mkdocs_env.py wiki/main.py blog/main.py
PYTHONPATH=.github/scripts python -m pylint --persistent=n .github/scripts/*.py
git ls-files -z '*.yml' '*.yaml' | xargs -0 yamllint -c .yamllint.yml
actionlint
zizmor --offline .github
```

Install yamllint from `requirements.test.txt`; actionlint, ShellCheck, and zizmor
are separate command-line tools. On macOS-mounted filesystems, exclude untracked
`._*` metadata files when scanning directories locally.

## Contributing

Open an [issue](https://github.com/antwanchild/docs/issues) to suggest content or report a bug.

To report a security vulnerability, see [SECURITY.md](SECURITY.md).

## License

- **Code** (Dockerfiles, workflows, configs) — [MIT](LICENSE)
- **Wiki content** (`wiki/docs/`) — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Blog content** (`blog/docs/`) — © Anthony Child, all rights reserved
