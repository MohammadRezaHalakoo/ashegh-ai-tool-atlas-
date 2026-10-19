"""Refresh public GitHub metadata only. No code execution, no private registry access."""
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/public_examples.json"
DEST = ROOT / "data/source_metadata.json"
API = "https://api.github.com/repos/"
HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "ashegh-ai-tool-atlas-public-metadata"}
if os.environ.get("GITHUB_TOKEN"):
    HEADERS["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]

def snapshot(repo_id):
    slug = repo_id.removeprefix("github:")
    req = urllib.request.Request(API + slug, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        d = json.load(response)
    return {
        "id": repo_id,
        "canonical_url": d.get("html_url"),
        "stars": d.get("stargazers_count"),
        "forks": d.get("forks_count"),
        "archived": d.get("archived"),
        "last_push": d.get("pushed_at"),
        "license_spdx": (d.get("license") or {}).get("spdx_id") or "UNKNOWN",
        "license_note": "GitHub-reported SPDX metadata only; not a legal review",
        "source": API + slug,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "review_status": "METADATA_ONLY_NOT_AUDITED",
    }

def main():
    catalog = json.loads(SOURCE.read_text(encoding="utf-8"))
    existing = {}
    if DEST.exists():
        existing = {x["id"]: x for x in json.loads(DEST.read_text(encoding="utf-8")).get("items", [])}
    errors = []
    for item in catalog["items"]:
        key = item["id"]
        try:
            existing[key] = snapshot(key)
            print("Updated", key)
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            errors.append(key + ": " + str(exc))
            print("Unavailable", key, exc)
        time.sleep(0.2)
    if not existing:
        raise SystemExit("No verified source metadata available; refusing empty output")
    output = {"schema_version": "1.0", "source": "GitHub REST public repository metadata", "items": [existing[k] for k in sorted(existing)]}
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if errors:
        print("Partial metadata refresh:", len(errors), "errors; old snapshots retained if present")
    print("Snapshots:", len(output["items"]))

if __name__ == "__main__":
    main()
