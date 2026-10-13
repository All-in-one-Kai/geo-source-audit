"""Synthetic fixtures. No credentials, provider calls, history writes or installs."""
import contextlib
import io
import json
import unittest
from unittest.mock import patch
import geo_source_audit as audit

PROJECT = {'label':'Synthetic demo','own_domains':['example.com'],'own_names':['Demo Brand']}

class OfflineTests(unittest.TestCase):
    def test_exact_host(self):
        self.assertTrue(audit.is_own('https://EXAMPLE.com/report', PROJECT))
    def test_subdomain(self):
        self.assertTrue(audit.is_own('https://docs.example.com/report', PROJECT))
    def test_www_port(self):
        self.assertTrue(audit.is_own('https://www.example.com:443/', PROJECT))
    def test_lookalike(self):
        self.assertFalse(audit.is_own('https://example.com.evil.test/', PROJECT))
    def test_query_is_not_source(self):
        self.assertFalse(audit.is_own('https://other.test/?next=example.com', PROJECT))
    def test_userinfo_is_rejected(self):
        self.assertFalse(audit.is_own('https://example.com@other.test/', PROJECT))
    def test_other_schemes(self):
        self.assertFalse(audit.is_own('javascript:example.com', PROJECT))
    def test_domain_normalization(self):
        self.assertEqual(audit.domain('https://www.Example.com./'), 'example.com')
    def test_brand_mention(self):
        self.assertTrue(audit.named('Try Demo Brand', PROJECT))
        self.assertFalse(audit.named('No recommendation', PROJECT))
    def test_foreign_targets(self):
        rows=[{'question':'Synthetic question','engine':'fixture','named':False,'cited':False,'domains':['example.com.evil.test','docs.example.com','other.test']}]
        text, summary=audit.report('demo', PROJECT, rows, [], {})
        self.assertEqual(summary['targets'], ['example.com.evil.test','other.test'])
        self.assertEqual(summary['n'], 1)
    def test_errors_hide_secrets(self):
        def fail(_): raise RuntimeError('https://provider.test/?key=SYNTHETIC-NOT-A-KEY')
        with patch.dict(audit.ENGINES, {'fixture':fail}), patch.object(audit.time,'sleep'):
            rows,errors=audit.audit('demo',{**PROJECT,'questions':['Synthetic']},['fixture'],'fixture')
        self.assertEqual(rows, [])
        self.assertNotIn('SYNTHETIC-NOT-A-KEY', '\n'.join(errors))
        self.assertNotIn('https://', '\n'.join(errors))
    def test_offline_demo(self):
        rows=[{'question':'Synthetic buyer question','engine':'fixture','named':True,'cited':True,'domains':['example.com','other.test']}]
        text, summary=audit.report('demo', PROJECT, rows, [], {})
        self.assertEqual((summary['named'],summary['cited'],summary['n']), (1,1,1))

if __name__=='__main__': unittest.main()
