import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('linker', ROOT / 'scripts/link-skills.py')
linker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(linker)


class InstallTests(unittest.TestCase):
    def test_links_are_live_and_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'skills'
            links = linker.install(ROOT, target)
            expected = {path.parent.resolve() for path in (ROOT / 'skills').glob('*/SKILL.md')}
            self.assertTrue(expected)
            self.assertEqual({link.resolve() for link in links}, expected)
            self.assertEqual(linker.install(ROOT, target), links)
            for link in links:
                self.assertTrue(link.is_symlink())
                self.assertTrue((link / 'SKILL.md').is_file())

    def test_conflict_preflight_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            conflict = target / 'technical-learning-profile'
            conflict.write_text('existing')
            with self.assertRaises(ValueError):
                linker.install(ROOT, target)
            self.assertEqual(conflict.read_text(), 'existing')
            self.assertFalse((target / 'mechanism-first-research').exists())
