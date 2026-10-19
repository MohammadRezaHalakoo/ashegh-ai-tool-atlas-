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
    # Responsive, accessible public directory; uses only already-vetted public JSON.
    listing = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Browse and search 24 public AI tools by category, with source-linked profiles and transparent evidence limitations.">
<link rel="canonical" href="https://mohammadrezahalakoo.github.io/ashegh-ai-tool-atlas-/tools/">
<title>Browse AI tools | Ashegh AI Tool Atlas</title>
<style>
:root{color-scheme:dark;font:16px/1.55 system-ui,sans-serif;background:#0b1220;color:#edf3ff}
*{box-sizing:border-box}body{margin:0}.wrap{max-width:1100px;margin:auto;padding:clamp(16px,4vw,36px)}
a{color:#a0d2ff}a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #b9dbff;outline-offset:3px}
nav{display:flex;gap:18px;flex-wrap:wrap;padding:14px 0}header{padding:22px 0}
h1{font-size:clamp(2rem,5vw,3rem);line-height:1.16;margin:.3em 0}
.muted{color:#b7c5db}.note{border-left:3px solid #91b5e0;background:#182841;padding:14px;border-radius:0 8px 8px 0}
.filters{display:grid;grid-template-columns:minmax(0,2fr) repeat(2,minmax(0,1fr));gap:12px;margin:24px 0}
input,select{width:100%;min-width:0;border:1px solid #536984;border-radius:10px;background:#1a2b45;color:#f3f7ff;font:inherit;padding:13px}
input::placeholder{color:#a9b9d0}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,265px),1fr));gap:14px}
.card{border:1px solid #3b506e;background:#15243a;border-radius:14px;padding:18px;overflow-wrap:anywhere;display:flex;flex-direction:column;gap:12px}
.card h2{font-size:1.17rem;margin:0}.card p{margin:0;color:#c6d3e5;flex:1}
.tag{align-self:flex-start;background:#304966;color:#e5f0ff;border-radius:999px;font-size:.8rem;padding:5px 10px}
.actions{display:flex;gap:14px;flex-wrap:wrap}footer{margin:40px 0;color:#b7c5db}
@media(max-width:700px){.filters{grid-template-columns:1fr}.wrap{padding:18px}.grid{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<nav aria-label="Site navigation"><a href="../index.html">← Atlas home</a><a href="../compare/index.html">Comparison guides</a></nav>
<header><h1>Explore AI tools</h1><p class="muted">Browse public tool profiles, search by name, or narrow down by category.</p>
<div class="note">Source-linked examples only. Inclusion is not a security, license, performance or compatibility audit.</div></header>
<section class="filters" aria-label="Directory filters">
<input id="search" type="search" placeholder="Search tools or descriptions" aria-label="Search tools">
<select id="category" aria-label="Filter by category"><option value="">All categories</option></select>
<select id="sort" aria-label="Sort tools"><option value="name">Name A–Z</option><option value="category">Category A–Z</option></select>
</section><p id="count" aria-live="polite">Loading public tools…</p><main class="grid" id="cards"></main>
<noscript><p>JavaScript is required for interactive search. Browse the <a href="../index.html">public catalogue</a> instead.</p></noscript>
<footer>Have a suggestion? <a href="https://github.com/MohammadRezaHalakoo/ashegh-ai-tool-atlas-/issues">Open an issue</a>. Data is sourced from public GitHub repositories.</footer>
</div><script>
const q=document.getElementById('search'),category=document.getElementById('category'),sort=document.getElementById('sort'),cards=document.getElementById('cards'),count=document.getElementById('count');
let tools=[];
const profile=x=>'./'+x.id.slice(7).toLowerCase().replace('/','--')+'.html';
function render(){
const term=q.value.trim().toLowerCase();
const visible=tools.filter(x=>(!category.value||x.category===category.value)&&(!term||[x.name,x.category,x.description].join(' ').toLowerCase().includes(term))).sort((a,b)=>String(a[sort.value]).localeCompare(String(b[sort.value])));
count.textContent=visible.length+' results · '+tools.length+' public tools';cards.replaceChildren();
for(const x of visible){
const article=document.createElement('article');article.className='card';
const h=document.createElement('h2'),link=document.createElement('a');link.href=profile(x);link.textContent=x.name;h.append(link);
const tag=document.createElement('span');tag.className='tag';tag.textContent=x.category;
const p=document.createElement('p');p.textContent=x.description;
const actions=document.createElement('div');actions.className='actions';
const source=document.createElement('a');source.href=x.url;source.target='_blank';source.rel='noopener noreferrer';source.textContent='GitHub source ↗';
actions.append(source);article.append(h,tag,p,actions);cards.append(article);
}
if(!visible.length){const empty=document.createElement('p');empty.textContent='No matching tools. Try another search or category.';cards.append(empty)}
}
async function start(){try{const r=await fetch('../data/public_examples.json',{cache:'no-store'});if(!r.ok)throw Error('HTTP '+r.status);const data=await r.json();if(!Array.isArray(data.items))throw Error('Invalid catalogue');tools=data.items;
for(const name of [...new Set(tools.map(x=>x.category))].sort()){const option=document.createElement('option');option.value=name;option.textContent=name;category.append(option)}render()
}catch(e){count.textContent='Public directory unavailable. Please refresh and try again.'}}
for(const el of [q,category,sort])el.addEventListener('input',render);start();
</script></body></html>"""
    (OUT / "index.html").write_text(listing + "\n", encoding="utf-8")
    # Preserve comparison pages while generating a deterministic sitemap from public content.
    routes = ["", "compare/", "compare/agent-frameworks.html", "compare/rag-search.html", "compare/mcp.html", "compare/llm-serving.html", "tools/"]
    routes += ["tools/" + slug(x) + ".html" for x in entries]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"  <url><loc>{BASE}{route}</loc></url>" for route in routes) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("Generated", len(entries), "tool profiles and", len(routes), "sitemap URLs")

if __name__ == "__main__":
    build()
