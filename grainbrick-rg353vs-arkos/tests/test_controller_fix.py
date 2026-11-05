import importlib.util
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

path=Path(__file__).resolve().parents[1]/'scripts/apply_controller_fix.py'
spec=importlib.util.spec_from_file_location('controller_fix',path)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ControllerFix(unittest.TestCase):
    def test_backup_patch_and_repeat(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'gb_launch.py'; original="import importlib\nimportlib.import_module('main')\n";p.write_text(original)
            m.apply(d)
            self.assertEqual((Path(d)/'gb_launch.community-original.py').read_text(),original)
            self.assertEqual(p.read_text().count(m.MARKER),1)
            updated=p.read_text();m.apply(d);self.assertEqual(p.read_text(),updated)

    def test_unexpected_launcher_unchanged(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'gb_launch.py';p.write_text('unexpected')
            with self.assertRaises(RuntimeError):m.apply(d)
            self.assertEqual(p.read_text(),'unexpected')
            self.assertFalse((Path(d)/'gb_launch.community-original.py').exists())

    def test_only_target_xy_changes(self):
        class Pad:
            def __init__(self,name):
                self.name=name;self.mapping={'a':'b0','b':'b1','x':'b2','y':'b3','start':'b9','leftx':'a0'};self.changes=0
            def get_mapping(self):return dict(self.mapping)
            def set_mapping(self,value):self.mapping=value;self.changes+=1
        pads=[Pad('retrogame_joypad'),Pad('Other Controller')]
        before=dict(pads[0].mapping);other=dict(pads[1].mapping)
        controller=types.SimpleNamespace(init=lambda:None,get_count=lambda:3,is_controller=lambda i:i<2,Controller=lambda i:pads[i])
        module=types.ModuleType('pygame._sdl2');module.controller=controller
        with patch.dict(sys.modules,{'pygame._sdl2':module}):exec(m.PATCH,{})
        self.assertEqual(pads[0].mapping,dict(before,x='b3',y='b2'))
        self.assertEqual(pads[1].mapping,other);self.assertEqual(pads[1].changes,0)
