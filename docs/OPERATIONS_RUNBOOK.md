# Atlas operations runbook

## Daily schedule (UTC / Tehran)
- 05:30 / 09:00 — discover candidates into unreviewed queue
- 06:15 / 09:45 — refresh public source metadata
- 06:45 / 10:15 — rebuild and publish Pages
- 08:30 / 12:00 — audit workflow freshness and site availability

Schedules are best-effort and may be delayed. First scheduled executions have not yet been independently verified.

## Health incidents
The health workflow opens one deduplicated GitHub issue if no successful workflow run exists in 48 hours or the directory cannot be reached. It closes the issue after recovery. Check Actions logs; GitHub issue notifications require account notification settings.

## Promotion review
Run `python scripts/evaluate_candidates.py` after a discovery run. The resulting `data/promotion_audit.json` records rejection reasons and items requiring editorial review. The workflow never publishes unreviewed candidates. GitHub stars and license metadata do not establish security, compatibility or license clearance.

## Benchmark evidence
Publish performance comparisons only with reproducible commands, pinned dependencies, datasets and permissions, hardware, multiple trials, latency, memory, accuracy, and uncertainty. No invented benchmark results.

## Operational boundaries
The site, discovery, metadata and alerting are automatic after successful GitHub schedules. Editorial approvals, real-world reputation and 7-day uninterrupted reliability are not yet verified.
