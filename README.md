# docs

Source for my personal wiki and blog, both built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and served via Docker + nginx.

| Site | URL |
|------|-----|
| Wiki | [wiki.anthonychild.com](https://wiki.anthonychild.com) |
| Blog | [blog.anthonychild.com](https://blog.anthonychild.com) |

## Structure

```
docs/
├── wiki/           # Wiki site (MkDocs source + config)
├── blog/           # Blog site (MkDocs source + config)
├── Dockerfile.wiki
├── Dockerfile.blog
└── .github/
    └── workflows/  # CI/CD pipelines
```

## How it works

Each site is built independently:

1. **Lint & spellcheck** — markdownlint and pyspelling run against the content directory
2. **Docker build** — MkDocs builds the static site, nginx serves it; the image is pushed to GHCR
3. **Release** — a versioned Git tag (`wiki-YYYY.MM` / `blog-YYYY.MM`) is created when new content is detected; release notes are generated with [git-cliff](https://git-cliff.org/)
4. **Link check** — lychee scans all outbound links
5. **Notify** — a Discord notification is sent on completion

Pushing to `main` triggers the workflow for whichever site was changed (`wiki/**` or `blog/**`). The two pipelines are independent.

## Running locally

**Prerequisites:** Python 3, pip, Docker (optional)

```bash
# Install dependencies
pip install mkdocs-material \
    mkdocs-macros-plugin \
    mkdocs-open-in-new-tab \
    mkdocs-glightbox \
    mkdocs-minify-plugin \
    python-dotenv

# Serve the wiki
cd wiki && mkdocs serve

# Serve the blog
cd blog && mkdocs serve
```

Both sites default to `http://localhost:8000`.

## Contributing

Open an [issue](https://github.com/antwanchild/docs/issues) to suggest content or report a bug.

To report a security vulnerability, see [SECURITY.md](SECURITY.md).

## License

- **Code** (Dockerfiles, workflows, configs) — [MIT](LICENSE)
- **Wiki content** (`wiki/docs/`) — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Blog content** (`blog/docs/`) — © Anthony Child, all rights reserved
