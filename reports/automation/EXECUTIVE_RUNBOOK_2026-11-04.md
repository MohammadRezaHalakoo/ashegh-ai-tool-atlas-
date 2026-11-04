# AI Tool Atlas executive automation runbook — 2026-11-04

Base main SHA: 8272fb8763a4dc7cdd3540a56e62341f52d6f2e2. Working branch: automation/executive-cycle-20261104.

## Daily cycle
1. Read current main, PRs, Issues, workflow runs, README, catalog, CLAUDE.md and AGENTS.md; check branch SHA before writing.
2. Inspect upstream official releases/advisories for agency-agents, wshobson/agents, claude-quickstarts, agent-skills, Lexmount/moli, and Jakeschincariol/instagram-agent-skill. Deduplicate by repo + SHA/release/advisory.
3. Check source license, attribution, risk and compatibility; keep new candidates UNREVIEWED until independent acceptance.
4. Apply only reversible small changes to working branch. Run actual non-destructive tests where environment permits; report exit codes, logs and unknowns.
5. Update CLAUDE.md, AGENTS.md and dated reports; commit and create Draft PR. No automatic promotion to reviewed, main merge or public release without valid gates.
6. Observe discovery→metadata→Pages scheduled chain and 7-day reliability from actual runs, not assumptions.

## Acceptance gates
- Current baseline/head SHA, CI and reviewer status captured.
- One complete safe edit→test→commit→Draft PR cycle demonstrated (not yet proven by this documentation-only change).
- No secrets, private research or personal inventory copied to public repo.
- Rollback is closing draft PR and reverting branch commits; main remains untouched.

## Current snapshot
- GitHub plugin full_access; repository push/admin available. Main SHA above.
- Previous CLAUDE.md/AGENTS.md reported scheduled discovery/metadata chain and seven-day uptime unverified; retain this warning until actual run evidence.
