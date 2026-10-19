# Maintainer runbook

## Boundaries
This is a public showcase and **not** the private research registry. Never sync the private JSON, private project notes, unpublished evaluations, or secrets automatically.

## CI and releases
Public CI validates data IDs, URLs, and safe site defaults. Weekly automation opens a public issue for review from this repository's own public data only. It does not spam other projects or fabricate engagement.

GitHub Pages deployment is defined in .github/workflows/pages.yml. A site becomes available only after GitHub Pages is enabled in repository settings and a deployment succeeds. Do not claim that Pages is live until verified.

## Review gates
Before expanding the public dataset: verify public origin, attribution, license of any copied content, metadata quality, and that the content is safe to disclose. Stars and inclusion are not endorsements.

## Suggested growth
Make reproducible comparisons, publish useful examples, respond to community contributions, and release human-reviewed changelogs. Avoid mass automated outreach, purchased followers, or automated stars.

## 2026-10-19 deployment check
PR #1 was squash-merged and CI passed on main. Pages deploy failed because Pages was not enabled. A subsequent attempt using `actions/configure-pages@v5` with `enablement: true` also failed: `Resource not accessible by integration` on Pages site creation. **One-time manual step required:** Repository Settings → Pages → Build and deployment → Source: GitHub Actions. Then re-run the Pages workflow. Do not claim the website is live before a successful deployment.
