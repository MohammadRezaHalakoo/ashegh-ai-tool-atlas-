import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PublicTests(unittest.TestCase):
    def test_schema_and_unique_urls(self):
        d=json.loads((ROOT/'data/public_examples.json').read_text())
        self.assertEqual(d['schema_version'],'1.0')
        self.assertGreaterEqual(len(d['items']),20)
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
    def test_comparison_pages_and_sitemap(self):
        pages=['agent-frameworks','rag-search','mcp','llm-serving']
        sitemap=(ROOT/'sitemap.xml').read_text()
        for slug in pages:
            html=(ROOT/'compare'/f'{slug}.html').read_text()
            self.assertIn('public_examples.json',html)
            self.assertIn(f'compare/{slug}.html',sitemap)
        self.assertIn('compare/index.html',(ROOT/'index.html').read_text())
        workflow=(ROOT/'.github/workflows/pages.yml').read_text()
        self.assertIn('cp -r compare _site/compare',workflow)
        self.assertIn('cp sitemap.xml robots.txt _site/',workflow)
    def test_metadata_pipeline_contract(self):
        script=(ROOT/'scripts/refresh_source_metadata.py').read_text()
        workflow=(ROOT/'.github/workflows/source-metadata.yml').read_text()
        self.assertIn('api.github.com/repos/',script)
        self.assertIn('METADATA_ONLY_NOT_AUDITED',script)
        self.assertIn('workflow_dispatch:',workflow)
        self.assertIn('source_metadata.json',(ROOT/'index.html').read_text())
        self.assertIn('source_metadata.json',(ROOT/'.github/workflows/pages.yml').read_text())
    def test_no_private_registry_export(self):
        self.assertFalse((ROOT/'registry/tools.json').exists())
if __name__=='__main__': unittest.main()
