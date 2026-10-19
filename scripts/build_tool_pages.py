"""Build 24 public-only static tool profiles. Never ingest private registry files."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/public_examples.json"
OUT = ROOT / "tools"
BASE = "https://mohammadrezahalakoo.github.io/ashegh-ai-tool-atlas-/"

def slug(item):
    return item["id"].removeprefix("github:").replace("/", "--").lower()

def build():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    entries = data["items"]
    ids = [x["id"].lower() for x in entries]
    assert len(ids) == len(set(ids)), "Duplicate repository IDs"
    assert len(entries) >= 24, "Unexpected public catalogue shrinkage"
    OUT.mkdir(exist_ok=True)
    links = []
    for x in entries:
        key = slug(x)
        assert re.fullmatch(r"[a-z0-9_.-]+--[a-z0-9_.-]+", key)
        name = html.escape(x["name"])
        description = html.escape(x["description"])
        category = html.escape(x["category"])
        url = x["url"]
        assert url.startswith("https://github.com/")
        source = html.escape(url, quote=True)
        canonical = BASE + "tools/" + key + ".html"
        page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{html.escape(x['description'][:150], quote=True)}">
<link rel="canonical" href="{canonical}"><title>{name} | Ashegh AI Tool Atlas</title>
<style>body{{font:16px/1.6 system-ui;background:#0b1220;color:#edf2ff;max-width:800px;margin:auto;padding:24px}}a{{color:#8fcaff}}.notice{{background:#1a2a42;border-left:3px solid #91b5e0;padding:14px}}</style></head>
<body><nav><a href="../index.html">← Atlas</a> · <a href="index.html">All tools</a> · <a href="../compare/index.html">Comparisons</a></nav>
<h1>{name}</h1><p><strong>Category:</strong> {category}</p><p>{description}</p>
<p><a href="{source}" rel="noopener noreferrer">Open public source repository ↗</a></p>
<div class="notice"><strong>Evidence level:</strong> Public repository source only. No reproduced benchmark, security audit or license review. GitHub metadata may be incomplete or stale.</div>
<h2>Due diligence checklist</h2><ul><li>Inspect current documentation and release notes.</li><li>Verify license terms directly before reuse.</li><li>Review dependencies and security advisories.</li><li>Benchmark with your own hardware and workloads.</li></ul>
<p id="metadata">Source metadata: not yet available.</p>
<script>
fetch('../data/source_metadata.json').then(r=>{{if(!r.ok)throw Error('unavailable');return r.json()}}).then(d=>{{const x=d.items.find(v=>v.id==={json.dumps(x['id'])});if(!x)return;document.getElementById('metadata').textContent='GitHub metadata checked: '+x.checked_at+' · Stars: '+(x.stars??'unknown')+' · SPDX metadata: '+(x.license_spdx||'UNKNOWN')+' · Archived: '+(x.archived??'unknown')+' (not independently audited)'}}).catch(()=>{{}});
</script></body></html>"""
        (OUT / (key + ".html")).write_text(page + "\n", encoding="utf-8")
        links.append(f'<li><a href="{key}.html">{name}</a> — {category}</li>')
    listing = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tool profiles | Ashegh AI Tool Atlas</title></head><body><h1>Public tool profiles</h1><p><a href="../index.html">Atlas home</a></p><ul>' + "".join(links) + '</ul></body></html>'
    (OUT / "index.html").write_text(listing + "\n", encoding="utf-8")
    # Preserve comparison pages while generating a deterministic sitemap from public content.
    routes = ["", "compare/", "compare/agent-frameworks.html", "compare/rag-search.html", "compare/mcp.html", "compare/llm-serving.html", "tools/"]
    routes += ["tools/" + slug(x) + ".html" for x in entries]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{BASE}{route}</loc></url>" for route in routes) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("Generated", len(entries), "tool profiles and", len(routes), "sitemap URLs")

if __name__ == "__main__":
    build()
