import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/mechanism-first-research/scripts/evidence.py'


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.db = self.root / 'evidence.sqlite'
        self.run_cli('init')

    def run_cli(self, *args, code=0):
        proc = subprocess.run([sys.executable, str(SCRIPT), '--db', str(self.db), *args], capture_output=True, text=True)
        self.assertEqual(proc.returncode, code, proc.stderr or proc.stdout)
        return json.loads(proc.stdout) if proc.stdout else None

    def add(self, **overrides):
        record = {'claim': 'One application per fleet', 'assessment': 'supported',
                  'source_url': 'https://example.org/fleets', 'passage': 'A fleet runs one application.'}
        record.update(overrides)
        path = self.root / 'record.json'
        path.write_text(json.dumps(record))
        source = self.root / 'source.txt'
        source.write_text('Documentation\nA fleet runs\n one application.\n')
        return self.run_cli('add', '--record', str(path), '--snapshot', str(source))['id']

    def test_capture_survives_source_deletion_and_exports(self):
        self.add()
        (self.root / 'source.txt').unlink()
        self.assertEqual(self.run_cli('check')['issues'], [])
        exported = self.run_cli('export')
        self.assertIn('Documentation', exported[0]['snapshot'])
        self.assertEqual(exported[0]['retrieval_time_basis'], 'entry_time')
        self.assertEqual(len(self.run_cli('find', 'FLEET')), 1)
        self.assertNotIn('snapshot', self.run_cli('list')[0])

    def test_unsupported_quote_and_questions_are_flagged(self):
        self.add(passage='Not in source', assessment='disputed', open_question='Does this apply to version 2?')
        issues = self.run_cli('check', code=1)['issues'][0]['issues']
        self.assertIn('passage not found in snapshot', issues)
        self.assertIn('assessment: disputed', issues)
        self.assertTrue(any('open question' in x for x in issues))

    def test_correction_preserves_history(self):
        original = self.add()
        replacement = self.add(claim='Qualified claim', supersedes=original)
        self.assertEqual([r['id'] for r in self.run_cli('list')], [replacement])
        self.assertEqual(len(self.run_cli('list', '--all')), 2)
        self.assertEqual(len(self.run_cli('export')), 2)
        path = self.root / 'bad.json'
        path.write_text(json.dumps({'claim': 'Another', 'assessment': 'supported', 'supersedes': original}))
        self.run_cli('add', '--record', str(path), code=2)
        self.assertEqual(len(self.run_cli('export')), 2)

    def test_invalid_record_does_not_write(self):
        path = self.root / 'bad.json'
        for value in ['not json', json.dumps({'claim': 'x', 'assessment': 'certain'}),
                      json.dumps({'claim': 'x', 'assessment': 'supported', 'retrieved_at': '2026-01-01'})]:
            path.write_text(value)
            self.run_cli('add', '--record', str(path), code=2)
        self.assertEqual(self.run_cli('list'), [])

    def test_missing_evidence_retained_as_unresolved(self):
        path = self.root / 'question.json'
        path.write_text(json.dumps({'claim': 'Unknown mechanism', 'assessment': 'unresolved'}))
        self.run_cli('add', '--record', str(path))
        self.assertEqual(len(self.run_cli('check', code=1)['issues'][0]['issues']), 4)

    def test_missing_db_does_not_silently_create(self):
        self.db.unlink()
        self.run_cli('list', code=2)
        self.assertFalse(self.db.exists())


if __name__ == '__main__':
    unittest.main()
