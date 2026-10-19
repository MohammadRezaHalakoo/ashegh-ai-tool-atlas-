# Source metadata and review policy

Public source snapshots are retrieved from GitHub REST API and refreshed by a scheduled workflow on Mondays (06:15 UTC), or on manual dispatch. The workflow never installs or executes third-party repositories.

## Displayed fields
GitHub-reported stars, forks, archive status, last push time, SPDX license metadata, source URL, and the UTC timestamp when the record was checked.

## Interpretation
- **License metadata is not legal review.** UNKNOWN or NOASSERTION must not be interpreted as permission to reuse.
- **Stars and activity are not quality or security scores.**
- A successful metadata refresh does not prove a tool works, is maintained, is safe, or is compatible.
- Failed source fetches retain previous snapshots, with their original check timestamps; no fabricated updates.
- The static site can render without snapshots; metadata is an optional enrichment.

## Next review gate
Add documentation-backed capability claims and reproducible benchmark results only after human or verifiable evidence review. Do not sync the private research registry into this public repository.
