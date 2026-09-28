# Matthew D. Webb academic website

This repository contains the source for <https://mattdwebb.github.io/>, built with [Quarto](https://quarto.org/) and deployed by GitHub Actions.

## Local preview

With Quarto installed:

```powershell
quarto preview
```

If Dropbox temporarily locks Quarto's generated `.quarto` cache, copy the repository to a temporary non-synced directory for preview. Source files should still be edited and committed in this repository.

## Content workflow

Three pages are generated from structured JSON by `scripts/generate_pages.py`. Quarto runs the generator automatically before every render.

### Add a new paper

1. Edit `data/research.json`.
2. Add the paper to `current` or `published` with only verified status and links.
3. Run `python scripts/generate_pages.py` or preview the site.

To update publication status, edit the relevant `status` or `venue` field. Move a completed paper from `current` to `published` when appropriate.

### Add a software package family

1. Add one family object to `data/software.json`.
2. Put every language implementation inside that family's `implementations` array.
3. Record the implementation author, role, verified registry, upstream repository, documentation, and install command.
4. Never label an R package CRAN, a Stata package SSC, a Python package PyPI, or a Julia package registered without checking the official registry.

To add another language, append an implementation to the existing family. Forks should link to their upstream author and must not be attributed to Matthew Webb unless the code history supports that claim.

### Add a video

Add a record to `data/videos.json` with the YouTube video ID, verified title, concise description, and one related paper or software link. Thumbnails are generated from the stable YouTube thumbnail URL pattern.

### Change the CV

Update `webb_CV.pdf` in the `mattdwebb/cv` repository; the website CV link then automatically uses the new file.

## Build and checks

```powershell
quarto render
python scripts/check_links.py _site
python scripts/check_external_links.py _site
```

The external checker reports journal/profile sites that block automated requests
separately from confirmed 404/410 responses. Because those checks depend on
third-party services, they are a release check rather than a deployment gate.

The rendered `_site` directory is ignored by Git and should not be maintained manually.

## Deployment

The workflow in `.github/workflows/publish.yml` renders and deploys on pushes to `main`. In GitHub, set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. A pull request from `site-migration` should be reviewed and merged before public deployment; do not deploy this migration branch directly.
Website
