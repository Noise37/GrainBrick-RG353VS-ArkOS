#!/usr/bin/env python3
"""Verify separately downloaded upstream archives; never execute their contents."""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import stat
import tarfile
import zipfile

GRAINBRICK_SHA256 = 'e2d985f7a99b8f123b0d39369b47bc8ed7b72be4a2296cc5f7ed2c8682518d7a'
UBUNTU_NAME = 'ubuntu-base-24.04.5-base-arm64.tar.gz'
APP_NAME = 'grainbrick beta 1.0.1'

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def validate_zip(path):
    total = 0
    with zipfile.ZipFile(path) as archive:
        for item in archive.infolist():
            p = PurePosixPath(item.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in item.filename:
                raise ValueError('Unsafe ZIP path: ' + item.filename)
            if stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError('ZIP symlinks are not accepted')
            total += item.file_size
        if total > 512 * 1024 * 1024:
            raise ValueError('Unexpectedly large GrainBrick archive')
        names = set(archive.namelist())
        for name in ('gb_launch.py', 'main.cpython-312-aarch64-linux-gnu.so', 'libSoundTouch.so.1'):
            if APP_NAME + '/' + name not in names:
                raise ValueError('Not the expected GrainBrick 1.0.1 application ZIP')
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC verification failed')

def verify(grainbrick, ubuntu, checksums):
    if digest(grainbrick) != GRAINBRICK_SHA256:
        raise ValueError('GrainBrick ZIP differs from the exact tested release; do not bypass this check')
    validate_zip(grainbrick)
    if ubuntu.name != UBUNTU_NAME:
        raise ValueError('Expected ' + UBUNTU_NAME)
    expected = []
    for line in checksums.read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].lstrip('*') == UBUNTU_NAME:
            expected.append(parts[0].lower())
    if len(expected) != 1 or digest(ubuntu) != expected[0]:
        raise ValueError('Ubuntu SHA256 verification failed')
    with tarfile.open(ubuntu, 'r:gz') as archive:
        for member in archive:
            p = PurePosixPath(member.name)
            if p.is_absolute() or '..' in p.parts:
                raise ValueError('Unsafe Ubuntu archive path')
    print('Both upstream archives verified.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('grainbrick', type=Path)
    parser.add_argument('ubuntu', type=Path)
    parser.add_argument('checksums', type=Path)
    args = parser.parse_args()
    try:
        verify(args.grainbrick, args.ubuntu, args.checksums)
    except (ValueError, OSError, zipfile.BadZipFile, tarfile.TarError) as error:
        parser.exit(1, 'Verification stopped: ' + str(error) + '\n')
