"""Read-only operational check for public GitHub Actions and Pages."""
import json,os,urllib.request
from datetime import datetime,timezone,timedelta
REPO=os.environ.get('REPOSITORY','MohammadRezaHalakoo/ashegh-ai-tool-atlas-')
TOKEN=os.environ.get('GH_TOKEN','')
HEAD={'Accept':'application/vnd.github+json','User-Agent':'atlas-health-check'}
if TOKEN:HEAD['Authorization']='Bearer '+TOKEN
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=HEAD),timeout=25) as r:return json.load(r)
def main():
    now=datetime.now(timezone.utc)
    failures=[]
    for workflow in ['daily-discovery.yml','source-metadata.yml','pages.yml']:
        url=f'https://api.github.com/repos/{REPO}/actions/workflows/{workflow}/runs?per_page=12'
        runs=get(url).get('workflow_runs',[])
        recent=[x for x in runs if x.get('conclusion')=='success' and datetime.fromisoformat(x['created_at'].replace('Z','+00:00'))>now-timedelta(hours=48)]
        if not recent:failures.append(workflow+': no successful run in last 48h')
        print(workflow,'successful recent runs',len(recent))
    try:
        with urllib.request.urlopen('https://mohammadrezahalakoo.github.io/ashegh-ai-tool-atlas-/tools/',timeout=20) as r:
            if r.status!=200:failures.append('Public directory HTTP '+str(r.status))
    except Exception as exc:failures.append('Public directory unreachable: '+type(exc).__name__)
    if failures:raise SystemExit('\n'.join(failures))
    print('Atlas operations healthy')
if __name__=='__main__':main()
