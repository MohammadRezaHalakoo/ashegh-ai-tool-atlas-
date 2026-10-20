"""Discover public GitHub candidates without publishing unreviewed claims."""
import json, os, urllib.request, urllib.parse, urllib.error, time
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"data/public_examples.json"
OUT=ROOT/"data/discovery_candidates.json"
QUERIES={
 "Agent Frameworks":"topic:ai-agents",
 "MCP, Skills & Plugins":"topic:mcp-server",
 "RAG & Search":"topic:retrieval-augmented-generation",
 "Serving & MLOps":"topic:llm-inference",
 "Speech & Audio":"topic:speech-recognition",
 "Evaluation & Observability":"topic:llm-evaluation",
 "Agent Memory":"topic:agent-memory",
 "Automation & Integration":"topic:workflow-automation",
 "Foundation Models":"topic:transformers",
 "Local Inference":"topic:local-llm",
 "Interfaces":"topic:llm-ui",
 "Document Processing":"topic:document-ai",
 "Computer Vision":"topic:computer-vision",
 "Multimodal AI":"topic:multimodal",
 "AI Coding":"topic:ai-coding-assistant",
 "Data Engineering":"topic:data-engineering",
 "Model Training":"topic:fine-tuning",
 "Model Optimization":"topic:quantization",
 "AI Safety":"topic:ai-safety",
 "Research Tools":"topic:machine-learning-research",
 "Knowledge Graphs":"topic:knowledge-graph",
 "Synthetic Data":"topic:synthetic-data",
 "Robotics":"topic:robotics",
 "AI Infrastructure":"topic:mlops"
}
HEADERS={"Accept":"application/vnd.github+json","User-Agent":"ashegh-atlas-public-discovery"}
if os.environ.get("GITHUB_TOKEN"):HEADERS["Authorization"]="Bearer "+os.environ["GITHUB_TOKEN"]
def main():
    existing={x["id"].lower() for x in json.loads(CATALOG.read_text())["items"]}
    found={}
    failures=[]
    for category,query in QUERIES.items():
        url="https://api.github.com/search/repositories?"+urllib.parse.urlencode({"q":query+" archived:false","sort":"updated","order":"desc","per_page":30})
        try:
            items=None
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=25) as response:
                        items=json.load(response)["items"]
                    break
                except (urllib.error.URLError,TimeoutError):
                    if attempt==2:raise
                    time.sleep(3*(attempt+1))
        except Exception as exc:
            failures.append({"category":category,"reason":type(exc).__name__})
            continue
        time.sleep(2)
        for item in items:
            key="github:"+item["full_name"].lower()
            if key in existing or key in found:continue
            found[key]={"id":"github:"+item["full_name"],"name":item["name"],"url":item["html_url"],"proposed_category":category,
             "description":item.get("description") or "No public description supplied",
             "stars_snapshot":item.get("stargazers_count"),"archived":item.get("archived"),
             "license_spdx":(item.get("license") or {}).get("spdx_id") or "UNKNOWN",
             "review_status":"DISCOVERED_UNREVIEWED","source_query":query}
    if len(failures)>len(QUERIES)//4:raise SystemExit("Discovery quality gate: too many GitHub search failures; preserve previous queue")
    result={"schema_version":"1.0","checked_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
      "note":"Candidate queue only; not published to the public tool catalogue without source review.",
      "expected_queries":len(QUERIES),"successful_queries":len(QUERIES)-len(failures),"failed_queries":failures,
      "items":sorted(found.values(),key=lambda x:x["id"].lower())}
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print("Candidate queue:",len(found),"successful searches:",result["successful_queries"])
if __name__=="__main__":main()
