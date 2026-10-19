import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PublicTests(unittest.TestCase):
    def test_schema_and_unique_urls(self):
        d=json.loads((ROOT/'data/public_examples.json').read_text())
        self.assertEqual(d['schema_version'],'1.0')
        ids=set()
        for x in d['items']:
            self.assertTrue(re.fullmatch(r'github:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',x['id']))
            self.assertTrue(x['url'].startswith('https://github.com/'))
            self.assertNotIn(x['id'].lower(),ids)
            ids.add(x['id'].lower())
    def test_site_safe_defaults(self):
        site=(ROOT/'index.html').read_text()
        self.assertIn('Ashegh AI Tool Atlas',site)
        self.assertIn('noopener noreferrer',site)
        self.assertNotIn('ashegh-universal-agent-intelligence',site)
    def test_no_private_registry_export(self):
        self.assertFalse((ROOT/'registry/tools.json').exists())
if __name__=='__main__': unittest.main()
