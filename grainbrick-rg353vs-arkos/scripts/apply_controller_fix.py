#!/usr/bin/env python3
"""Install the launcher-level SDL X/Y fix validated on RG353VS / ArkOS."""
from pathlib import Path
import shutil
import sys

MARKER = '# RG353VS controller mapping: change X/Y only.'
PATCH = '''
# RG353VS controller mapping: change X/Y only.
from pygame._sdl2 import controller as _rg353_controller
_rg353_controller.init()
_rg353_pads = []
for _i in range(_rg353_controller.get_count()):
    if _rg353_controller.is_controller(_i):
        _pad = _rg353_controller.Controller(_i)
        if _pad.name == "retrogame_joypad":
            _mapping = _pad.get_mapping()
            _mapping["x"] = "b3"
            _mapping["y"] = "b2"
            _pad.set_mapping(_mapping)
            print("RG353VS SDL X/Y mapping applied", flush=True)
        _rg353_pads.append(_pad)

'''


def apply(app):
    launcher = Path(app) / 'gb_launch.py'
    text = launcher.read_text()
    if MARKER in text:
        print('SDL X/Y fix already present.')
        return
    anchor = "importlib.import_module('main')"
    if text.count(anchor) != 1:
        raise RuntimeError('Unexpected launcher; no controller patch applied.')
    backup = launcher.with_name('gb_launch.community-original.py')
    if backup.exists():
        raise RuntimeError('Original launcher backup already exists; no overwrite.')
    updated = text.replace(anchor, PATCH + anchor)
    compile(updated, str(launcher), 'exec')
    shutil.copy2(str(launcher), str(backup))
    temporary = launcher.with_name('gb_launch.py.tmp')
    temporary.write_text(updated)
    temporary.chmod(launcher.stat().st_mode & 0o777)
    temporary.replace(launcher)
    print('Installed RG353VS SDL X/Y fix.')


if __name__ == '__main__':
    apply(sys.argv[1])
