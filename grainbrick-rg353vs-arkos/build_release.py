#!/usr/bin/env python3
from pathlib import Path
import zipfile, stat
root=Path(__file__).resolve().parent
out=root/'dist'; out.mkdir(exist_ok=True)
with zipfile.ZipFile(out/'grainbrick-rg353vs-ports-v0.2.2.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ('Install GrainBrick.sh','START-HERE.txt','README.md'):
        z.write(root.parent/name,name)
    for f in sorted(root.rglob('*')):
        if f.is_file() and not any(x in f.relative_to(root).parts for x in ('dist','__pycache__','downloads')) and f.name not in ('FILE-CHECKSUMS.txt','install.log','installer-screen.log'):
            z.write(f, 'grainbrick-rg353vs-arkos/'+f.relative_to(root).as_posix())
print(out/'grainbrick-rg353vs-ports-v0.2.2.zip')
