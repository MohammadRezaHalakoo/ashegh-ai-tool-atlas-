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
    def test_generated_tool_profiles(self):
        import subprocess
        import sys
        subprocess.run([sys.executable, str(ROOT/'scripts/build_tool_pages.py')], check=True)
        catalog=json.loads((ROOT/'data/public_examples.json').read_text())
        for item in catalog['items']:
            slug=item['id'].removeprefix('github:').replace('/','--').lower()
            page=(ROOT/'tools'/f'{slug}.html')
            self.assertTrue(page.is_file(),slug)
            self.assertIn(item['url'],page.read_text())
            self.assertIn('tools/'+slug+'.html',(ROOT/'sitemap.xml').read_text())
        listing=(ROOT/'tools'/'index.html').read_text()
        self.assertIn('class="grid"',listing)
        self.assertIn('id="search"',listing)
        self.assertIn('id="category"',listing)
        self.assertIn('id="sort"',listing)
        self.assertIn('../data/public_examples.json',listing)
        self.assertIn('No matching tools',listing)
        self.assertIn('aria-live="polite"',listing)
        self.assertIn('noopener noreferrer',listing)
        self.assertIn('cp -r tools _site/tools',(ROOT/'.github/workflows/pages.yml').read_text())
    def test_daily_discovery_is_review_gated(self):
        collector=(ROOT/'scripts/discover_candidates.py').read_text()
        workflow=(ROOT/'.github/workflows/daily-discovery.yml').read_text()
        self.assertIn('DISCOVERED_UNREVIEWED',collector)
        self.assertIn('data/discovery_candidates.json',workflow)
        self.assertNotIn('git add data/public_examples.json',workflow)
        self.assertIn("cron: '30 5 * * *'",workflow)
        self.assertIn("cron: '15 6 * * *'",(ROOT/'.github/workflows/source-metadata.yml').read_text())
        self.assertIn("cron: '45 6 * * *'",(ROOT/'.github/workflows/pages.yml').read_text())
    def test_review_gate_and_health_workflow(self):
        from importlib.util import spec_from_file_location, module_from_spec
        spec=spec_from_file_location('candidate_evaluator',ROOT/'scripts/evaluate_candidates.py')
        mod=module_from_spec(spec);spec.loader.exec_module(mod)
        sample={'id':'github:sample/tool','url':'https://github.com/sample/tool',
          'review_status':'DISCOVERED_UNREVIEWED','archived':False,'stars_snapshot':200,
          'license_spdx':'MIT','proposed_category':'Agent Frameworks',
          'description':'A public repository with a documented example implementation.'}
        self.assertTrue(mod.eligible(sample)[0])
        self.assertFalse(mod.eligible({**sample,'url':'https://evil.example/tool'})[0])
        self.assertFalse(mod.eligible({**sample,'license_spdx':'UNKNOWN'})[0])
        self.assertIn('HUMAN_REVIEW_REQUIRED_FOR_PUBLICATION',(ROOT/'scripts/evaluate_candidates.py').read_text())
        self.assertIn('scripts/evaluate_candidates.py',(ROOT/'.github/workflows/daily-discovery.yml').read_text())
        health=(ROOT/'.github/workflows/operations-health.yml').read_text()
        self.assertIn('scripts/check_health.py',health)
        self.assertIn('issues: write',health)
    def test_no_private_registry_export(self):
        self.assertFalse((ROOT/'registry/tools.json').exists())
if __name__=='__main__': unittest.main()
