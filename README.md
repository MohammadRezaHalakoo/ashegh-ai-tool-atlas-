# Ashegh AI Tool Atlas

**Discover, compare, and evaluate the open AI tooling ecosystem.**

A community-oriented catalogue of AI agent frameworks, MCP servers, LLM infrastructure, RAG tools, speech, computer vision, automation, and more.

## Why this exists
AI tooling changes quickly. This project aims to make discovery reproducible and transparent, rather than treating stars or popularity as proof of safety.

## Coverage
24 public example tools spanning multiple categories, with source links and a searchable dashboard. A broader taxonomy exists in private research, but is not published here. The private research repository is **not** part of this public distribution.

## Important limitations
- Discovery is not a security audit, endorsement, or compatibility guarantee.
- Popularity metrics are snapshots and can be outdated.
- New candidates are unreviewed until evidence-based assessment.
- No external software is automatically installed or executed.

## Getting started
A source-verified public sample dataset and searchable dashboard are available. Inclusion is not a security, license or performance audit. The source research catalogue remains private.

## Contributing
Please propose tools with canonical source URLs, use cases, licenses and evidence. Avoid unverifiable claims.

## Roadmap
- [ ] Public-safe curated data export
- [x] Searchable static dashboard
- [x] Criteria-based comparison guides (not benchmark rankings)
- [x] Daily metadata refresh and Pages rebuild; new candidates remain review-gated
- [ ] Community contribution workflow

Maintained by [MohammadRezaHalakoo](https://github.com/MohammadRezaHalakoo).

## Public demo
A self-contained [searchable HTML demo](index.html) and [public example dataset](data/public_examples.json) are available. The public demo contains 24 independently selected public repositories and is intentionally not a copy of the private research registry. To view the demo, download `index.html` and open it locally; GitHub Pages is enabled and has been deployed successfully. More public records require review before release.

## Comparison guides
- [Agent frameworks](compare/agent-frameworks.html)
- [RAG & search](compare/rag-search.html)
- [MCP](compare/mcp.html)
- [LLM serving](compare/llm-serving.html)

See [comparison methodology](docs/COMPARISON_METHODOLOGY.md) for evidence limitations.

## Daily automation (UTC / Tehran)
- 05:30 UTC / 09:00 Tehran: discover public GitHub candidate repositories into `data/discovery_candidates.json`, **not the public catalogue**.
- 06:15 UTC / 09:45 Tehran: refresh public GitHub metadata for existing catalogue entries.
- 06:45 UTC / 10:15 Tehran: rebuild and deploy static public site.
- GitHub scheduled workflows are best-effort and can be delayed or fail. Check Actions for real results. No guarantee of new published tools every day; review is required before publishing new candidates.

