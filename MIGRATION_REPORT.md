# Google Sites to Quarto migration report

## What was built

A complete first version of Matthew D. Webb's academic website was built as a Quarto project for `https://mattdwebb.github.io/`. The site uses a restrained, responsive academic design, has no analytics or unnecessary JavaScript, and is designed to be maintained through Git and structured JSON data.

The implementation includes:

- a homepage with the current photograph, professional introduction, research interests, current-research highlights, research-software summary, and latest research video;
- current and published research generated from `data/research.json`;
- a method-first software index generated from `data/software.json`, with implementation-level authorship, registry, documentation, repository, and installation information;
- a lightweight video library generated from `data/videos.json` and linked to the YouTube channel;
- teaching, conferences, hockey, and CV pages;
- the supplied current CV at `files/webb_CV.pdf`;
- a GitHub Actions workflow that renders and deploys the site from `main` after review and merge;
- an internal-link checker and maintenance instructions in `README.md`.

## Final site structure

- Home
- Research
  - Current Research
    - AI, Machine Learning, and Economic Measurement
    - Econometric Methods and Inference
    - Applied Microeconomics
  - Published Research
- Software
- Teaching
- Videos
- CV
- More
  - Conferences
  - Hockey

The navigation also includes restrained links to Google Scholar, GitHub, YouTube, and email.

## Major content changes from the Google Site

- Replaced the stale current-research list with CV-based statuses and verified public links.
- Made `Representation Risk in Pretrained Image Encoders` and `Images as Covariates: Incorporating Missing Information from Structured Data` prominent, distinct current projects. The anonymous ICLR submission PDF is not published.
- Kept econometric inference central through CSDID cluster-jackknife work, DID-INT, UN-DID, two-way clustering, and the publication archive.
- Replaced the repository-oriented code page with a method-oriented software guide.
- Added transparent student/research-assistant implementation credit based on fork provenance, repository history, README material, and contributor metadata.
- Rebuilt the videos page as a curated knowledge-mobilization library rather than a generic embedded feed.
- Updated teaching and conference material from the CV and removed stale language about old items being current.
- Preserved the hockey page under **More**, including its contact purpose and the note that the CEA does not organize the games.
- Replaced the older website CV with the supplied PDF without editing the PDF itself.

## Software families and language implementations identified

| Method/package family | Implementations shown |
|---|---|
| `summclust` | Stata — Matthew D. Webb |
| `logitjack` | Stata — Matthew D. Webb |
| `twowayjack` | Stata — Matthew D. Webb |
| `mnwsvt` | Stata — Matthew D. Webb; R (`MNW`) — Tonghui Tian |
| CSDID cluster-jackknife inference | Stata (`csdidjack`) and R (`didjack`) — Yunhan Liu |
| DID-INT | Julia (`DiDInt.jl`) — Eric Jamieson |
| UN-DID | Stata (`undid`), R (`undidR`), Julia (`Undid.jl`), and Python (`undidPyjl`) — Eric Jamieson |

## Attribution decisions

- The CV's Software Packages section was treated as authoritative for Matthew D. Webb's original Stata implementations.
- GitHub repositories identified as forks were not attributed to Matthew Webb as code author.
- `MNW` links to Tonghui Tian's upstream repository and credits Tonghui Tian for the R implementation.
- `didjack` and `csdidjack` link to Yunhan Liu's upstream repositories and credit Yunhan Liu for both implementations.
- `Undid.jl`, `undidR`, `DiDInt.jl`, `undid`, and `undidPyjl` link to Eric Jamieson's upstream repositories and credit Eric Jamieson for the implementations.
- Matthew Webb's relationship to these student-written implementations is described only through the associated research/method context and research-assistant role, not through code authorship.

No displayed student-written fork is attributed to Matthew Webb.

## Registry registrations verified

The following claims were checked against official registry records or primary distribution records before display:

- `summclust` — SSC
- `logitjack` — SSC
- `undid` — SSC
- `undidR` — CRAN
- `undidPyjl` — PyPI
- `DiDInt.jl` — Julia General Registry

The following are conservatively labelled **GitHub only** because a relevant official registration was not found:

- `twowayjack`
- `mnwsvt`
- `MNW`
- `csdidjack`
- `didjack`
- `Undid.jl`

## Uncertain software attribution requiring review

No implementer in the displayed software families remains unidentified. The attribution evidence is strong enough to use the names above, but Matthew Webb should review the role wording for Tonghui Tian, Yunhan Liu, and Eric Jamieson before public launch.

The wider GitHub profile contains additional experimental, replication, and older code repositories. They were not automatically promoted to software families because their public-support status, relationship to a current method, or preferred citation was not sufficiently clear.

## Documentation gaps

- `mnwsvt` is a significant research package but currently uses the repository as its documentation landing page; a dedicated documentation page would improve discoverability.
- `twowayjack`, the CSDID implementations, `DiDInt.jl`, `Undid.jl`, and `undidPyjl` also rely primarily on README/help-file documentation. The website links to those sources without modifying the package repositories.
- `undidR` already has a clean documentation site and is linked directly.

## Missing paper or arXiv links

- `Representation Risk in Pretrained Image Encoders`: add the public arXiv URL when available. The anonymous ICLR 2027 submission PDF is intentionally not linked.
- `Images as Covariates: Incorporating Missing Information from Structured Data`: add the current public manuscript URL when available. The older curb-appeal preprint is intentionally not used as the current-paper link.
- `The Many Misspellings of Albuquerque`: no verified public manuscript link was found.
- The accepted JPE Microeconomics comment does not yet have a verified public article/preprint link in the structured data.

The data model already supports adding these URLs without changing the page layout.

## Missing video links

No clearly corresponding public channel video was found for the two current AI/image papers, DID-INT, or UN-DID, so none was invented. Each research and software record supports an optional video field that can be populated later.

## Broken or stale links found on the old website

- The old website's CV navigation depended on an older GitHub/nbviewer copy rather than the supplied current PDF.
- Several old code links pointed to retired Google Code-era downloads or beta-package locations and are not suitable as current installation instructions.
- The old conference page labelled dated meetings and calls as current.
- The old UN-DID arXiv text/link was truncated (`2403.1591`); the current site uses `2403.15910`.
- The older firearm-paper Google Drive link was replaced by the current public arXiv paper and replication repository.
- The old WordPress PDF for `Pitfalls when Estimating Treatment Effects Using Clustered Data` returned 404; it was replaced with the Society for Political Methodology article page.
- The older image paper title and curb-appeal framing no longer describe the authoritative 2026 project and were not carried forward as current content.

## Items intentionally not migrated

- private course files or non-public course materials;
- stale Google Code downloads and unverified beta installation instructions;
- the anonymous ICLR submission PDF;
- the old curb-appeal preprint as the current version of the image-covariates project;
- obsolete current-conference notices and calls for papers;
- a complete historical presentation/talk archive that would duplicate the CV without improving navigation;
- decorative download counters, CI badges, analytics, tracking, and multi-iframe video embeds;
- unverified software registry claims or repositories without a clear maintained-method role.

## Quality-control results

- A complete Quarto render succeeds for all eight pages.
- The generated site passes `python scripts/check_links.py _site`; every internal navigation target and local asset resolves.
- The external-link check found **0 confirmed broken links** among 84 unique URLs. Sixty-nine responded directly; 15 journal/profile URLs rejected the automated checker or had a local certificate-chain warning and were retained because their DOI or primary-source destination was independently verified.
- The rendered CV file is present and byte-for-byte matches `files/webb_CV.pdf`.
- Desktop and 390-pixel mobile layouts were tested in a browser. The homepage, dense software page, research, videos, teaching, conferences, hockey, and CV pages have no horizontal overflow.
- The homepage photograph has meaningful alt text.
- Structured data and generated pages contain no placeholder personal information.
- Registry labels and student/RA authorship were audited before display.

On this Windows/Dropbox checkout, Dropbox occasionally locks Quarto's generated `.quarto` cache. The clean final verification build was therefore run from a fresh temporary copy outside Dropbox. This affects only local generated files; it does not affect the repository source or the Linux GitHub Actions build.

## GitHub Pages configuration still required

After the pull request is reviewed and merged:

1. Open the repository on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Merge the `site-migration` pull request into `main` when ready.
5. The `Publish Quarto website` workflow will render, check internal links, and deploy `_site`.
6. Confirm the completed deployment at `https://mattdwebb.github.io/`.

The workflow only deploys on `main` (or a manual workflow dispatch), so pushing `site-migration` does not replace the public site.

## Repository handoff status

All work is committed locally on the `site-migration` branch. The final push was attempted, but this checkout has no usable GitHub HTTPS credentials and non-interactive Git reported that it could not read a username. Consequently, the branch and pull request have not been created on GitHub.

After authenticating Git for this repository, run:

```powershell
git push -u origin site-migration
gh pr create --base main --head site-migration --title "Migrate academic website to Quarto" --body "Builds the first complete Quarto version of the academic website. See MIGRATION_REPORT.md for content, provenance, quality-control results, and post-merge Pages configuration."
```

Do not merge the pull request until the site content and attribution notes have been reviewed.

## Local preview command

From the repository root on this computer:

```powershell
& "C:\Program Files\RStudio\resources\app\bin\quarto\bin\quarto.exe" preview
```

With standalone Quarto on the path:

```powershell
quarto preview
```

If Dropbox locks generated cache files, copy the repository to a temporary non-synced directory and run the same command there. Edit and commit only the source repository.

## Exact deployment process

1. Edit content on a feature branch.
2. Preview with Quarto and run `quarto render`.
3. Run `python scripts/check_links.py _site`.
4. Commit and push the branch.
5. Open and review a pull request to `main`.
6. Merge only after review.
7. GitHub Actions renders from source, uploads `_site` as a Pages artifact, and deploys it.

Generated `_site` files should not be committed or maintained manually.

## Recommended next changes

1. Add public arXiv links for the two image/AI manuscripts when they become available.
2. Confirm coauthor lines for those manuscripts before adding author metadata publicly.
3. Review the student/RA role wording and software-family selection.
4. Add a public link for `The Many Misspellings of Albuquerque` if one is available.
5. Consider dedicated documentation sites for the mature GitHub-only packages, beginning with `mnwsvt`.
6. Add related videos for DID-INT, UN-DID, and the image/AI work when suitable videos exist.
7. Update publication links as accepted/forthcoming papers receive final journal pages.

## Questions for Matthew Webb

1. What author order should be displayed for `Representation Risk in Pretrained Image Encoders` and `Images as Covariates: Incorporating Missing Information from Structured Data` when their public versions launch?
2. Are the research-assistant role descriptions for Tonghui Tian, Yunhan Liu, and Eric Jamieson the preferred public wording?
3. Is there a public manuscript link for `The Many Misspellings of Albuquerque` or the accepted JPE Microeconomics comment?
4. Are there any additional maintained software families from the GitHub profile that should be promoted to the curated Software page?

## CV updates suggested but NOT performed

- Update the GitHub-hosted CV to the September 2026 version.
- Consider changing **Research Interests** to: **Applied Microeconometrics, Causal Inference, Machine Learning and AI for Economic Measurement, Empirical Microeconomics**.
- Consider adding the CSDID Stata/R implementations, DID-INT Julia implementation, and UN-DID multi-language implementation family to the CV's software section, while explicitly crediting Yunhan Liu and Eric Jamieson as the implementation authors.
- Consider noting the R implementation of `mnwsvt` (`MNW`) while explicitly crediting Tonghui Tian.

The CV PDF itself was not edited, and the separate CV repository was not modified.
