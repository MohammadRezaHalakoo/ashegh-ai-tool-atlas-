"""Create a transparent review report from PUBLIC data only; no private credentials."""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
d=json.loads((Path(__file__).resolve().parents[1]/'data/public_examples.json').read_text())
items=d['items']
print('# Public catalogue weekly review')
print('Generated:',datetime.now(timezone.utc).date().isoformat())
print('\nOnly public examples are included; this report does not imply a security review.')
print('\nEntries:',len(items))
print('\n## Categories')
for k,v in sorted(Counter(x['category'] for x in items).items()): print('-',k+':',v)
print('\n## Review tasks')
print('- Verify each source URL, activity, license and documentation.')
print('- Identify relevant new public candidates and cite evidence.')
print('- Review proposed updates before publishing; never import the private registry wholesale.')
