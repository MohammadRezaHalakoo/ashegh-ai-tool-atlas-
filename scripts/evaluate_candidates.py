"""Conservatively promote verifiable GitHub candidate metadata, not trust claims."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CANDIDATES=ROOT/'data/discovery_candidates.json'
CATALOG=ROOT/'data/public_examples.json'
AUDIT=ROOT/'data/promotion_audit.json'
SAFE=re.compile(r'^github:([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$')
def eligible(x):
    match=SAFE.fullmatch(x.get('id',''))
    if not match:return False,'invalid-id'
    expected='https://github.com/'+match[1]+'/'+match[2]
    if x.get('url','').lower()!=expected.lower():return False,'source-mismatch'
    if x.get('review_status')!='DISCOVERED_UNREVIEWED':return False,'unexpected-status'
    if x.get('archived') is not False:return False,'archived-or-unknown'
    if not isinstance(x.get('stars_snapshot'),int) or x['stars_snapshot']<100:return False,'insufficient-source-signal'
    if x.get('license_spdx') in (None,'UNKNOWN','NOASSERTION'):return False,'license-metadata-unavailable'
    if x.get('proposed_category') not in ('Agent Frameworks','MCP, Skills & Plugins','RAG & Search','Serving & MLOps','Speech & Audio','Evaluation & Observability','Agent Memory','Automation & Integration','Foundation Models','Local Inference','Interfaces','Document Processing','Computer Vision','Multimodal AI','AI Coding','Data Engineering','Model Training','Model Optimization','AI Safety','Research Tools','Knowledge Graphs','Synthetic Data','Robotics','AI Infrastructure'):return False,'unknown-category'
    desc=x.get('description','')
    if len(desc.strip())<20 or len(desc)>240:return False,'missing-description'
    return True,'metadata-gates-passed'
def main():
    if not CANDIDATES.exists():
        print('No candidate queue yet; no changes');return
    queue=json.loads(CANDIDATES.read_text())
    if queue.get('successful_queries',0)<int(queue.get('expected_queries',8)*0.75):
        raise SystemExit('Too few successful discovery queries; refusing promotion')
    catalog=json.loads(CATALOG.read_text())
    existing={x['id'].lower() for x in catalog['items']}
    decisions=[]
    for x in queue['items']:
        ok,reason=eligible(x)
        if x.get('id','').lower() in existing:continue
        # Metadata-only promotion is deliberately not automatic: source provenance
        # cannot establish project claims, safety or license compliance.
        decisions.append({'id':x.get('id'),'decision':'REVIEW_REQUIRED' if ok else 'REJECTED_BY_METADATA_GATE','reason':reason})
    AUDIT.write_text(json.dumps({'schema_version':'1.0','policy':'HUMAN_REVIEW_REQUIRED_FOR_PUBLICATION','decisions':decisions},indent=2)+'\n')
    print('Evaluated',len(decisions),'candidates; no unreviewed projects published')
if __name__=='__main__':main()
