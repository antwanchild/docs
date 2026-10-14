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
3. **Release** — a versioned Git tag (`wiki-YYYY.MM` / `blog-YYYY.MM`) is created when new content is detected; release notes are generated with [git-cliff](https://git-cliff.org/)
4. **Link check** — lychee scans all outbound links
5. **Notify** — a Discord notification is sent on completion

Pushing to `main` triggers the workflow for whichever site was changed (`wiki/**` or `blog/**`). Changes to shared dependencies, helpers, or the reusable build workflow trigger both pipelines. The two pipelines are independent.

## Running locally

**Prerequisites:** Python 3, pip, Docker (optional)

```bash
# Install dependencies (Python 3.12 recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.wiki.txt -r requirements.blog.txt

# Serve one site at a time, from the repository root
zensical serve -f wiki/mkdocs.yml
zensical serve -f blog/mkdocs.yml

# Build either site
zensical build --strict -f wiki/mkdocs.yml
zensical build --strict -f blog/mkdocs.yml
```

Both sites default to `http://localhost:8000`. Builds write to `wiki/site/` and `blog/site/`. The existing `mkdocs.yml` configuration format and classic Material appearance are retained.

## Contributing

Open an [issue](https://github.com/antwanchild/docs/issues) to suggest content or report a bug.

To report a security vulnerability, see [SECURITY.md](SECURITY.md).

## License

- **Code** (Dockerfiles, workflows, configs) — [MIT](LICENSE)
- **Wiki content** (`wiki/docs/`) — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Blog content** (`blog/docs/`) — © Anthony Child, all rights reserved
