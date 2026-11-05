import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import io

P=Path(__file__).resolve().parents[1]/'scripts/ports_install.py'
spec=importlib.util.spec_from_file_location('ports_install', P)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class PortsInstaller(unittest.TestCase):
    def test_missing_application_stops_without_commands(self):
        with tempfile.TemporaryDirectory() as d, patch.object(m,'ROOT',Path(d)), patch.object(m,'BASE',Path(d)/'absent'), patch.object(m.subprocess,'run') as run:
            m.finished=False; m.success=False; m.install()
            self.assertTrue(m.finished); self.assertFalse(m.success)
            run.assert_not_called()
            self.assertIn('Missing application ZIP',(Path(d)/'install.log').read_text())

    def test_existing_environment_is_preserved(self):
        with tempfile.TemporaryDirectory() as d, patch.object(m,'ROOT',Path(d)), patch.object(m,'BASE',Path(d)/'base'), patch.object(m.subprocess,'run') as run:
            m.BASE.mkdir(); marker=m.BASE/'keep'; marker.write_text('preserve')
            m.install(); self.assertEqual(marker.read_text(),'preserve'); run.assert_not_called()

    def test_download_commits_complete_file(self):
        with tempfile.TemporaryDirectory() as d, patch.object(m,'ROOT',Path(d)), patch.object(m.urllib.request,'urlopen',return_value=io.BytesIO(b'complete')):
            target=m.download('SHA256SUMS')
            self.assertEqual(target.read_bytes(),b'complete')
            self.assertFalse(target.with_name('SHA256SUMS.part').exists())

    def test_failed_download_never_commits_target(self):
        class Broken(io.BytesIO):
            def read(self,*args): raise OSError('interrupted')
        with tempfile.TemporaryDirectory() as d, patch.object(m,'ROOT',Path(d)), patch.object(m.urllib.request,'urlopen',return_value=Broken()):
            with self.assertRaises(OSError): m.download('SHA256SUMS')
            self.assertFalse((Path(d)/'downloads/SHA256SUMS').exists())
