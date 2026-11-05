import importlib.util
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('verify_inputs', Path(__file__).resolve().parents[1] / 'scripts/verify_inputs.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class ArchiveSafety(unittest.TestCase):
    def make_zip(self, extra=None):
        f = Path(self.tmp.name) / 'app.zip'
        with zipfile.ZipFile(f, 'w') as z:
            for n in ('gb_launch.py', 'main.cpython-312-aarch64-linux-gnu.so', 'libSoundTouch.so.1'):
                z.writestr(v.APP_NAME + '/' + n, b'test fixture, never executed')
            if extra:
                z.writestr(extra, b'payload')
        return f

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_valid_layout(self):
        v.validate_zip(self.make_zip())

    def test_parent_traversal_rejected(self):
        with self.assertRaises(ValueError):
            v.validate_zip(self.make_zip('../outside'))

    def test_absolute_path_rejected(self):
        with self.assertRaises(ValueError):
            v.validate_zip(self.make_zip('/etc/evil'))

    def test_windows_separator_rejected(self):
        with self.assertRaises(ValueError):
            v.validate_zip(self.make_zip('..\\outside'))

    def test_symlink_rejected(self):
        item = zipfile.ZipInfo('link')
        item.create_system = 3
        item.external_attr = (stat.S_IFLNK | 0o777) << 16
        with self.assertRaises(ValueError):
            v.validate_zip(self.make_zip(item))

    def test_unexpected_release_hash_rejected_before_extraction(self):
        with self.assertRaisesRegex(ValueError, 'differs'):
            v.verify(self.make_zip(), Path('unused'), Path('unused'))

if __name__ == '__main__':
    unittest.main()
