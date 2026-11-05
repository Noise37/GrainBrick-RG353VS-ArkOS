#!/usr/bin/env python3
"""Controller-operated installer. Python 3.7+ and the host SDL2; no pygame needed."""
import ctypes as C
import json
import os
from pathlib import Path
import subprocess
import threading
import time
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
BASE = Path('/home/ark/grainbrick-arkos')
APP = 'grainbrick.beta.1.0.1.zip'
UBUNTU = 'ubuntu-base-24.04.5-base-arm64.tar.gz'
URL = 'https://cdimage.ubuntu.com/ubuntu-base/releases/24.04/release/'
status = ['Ready', '']
finished = False
success = False


def download(name):
    target = ROOT / 'downloads' / name
    target.parent.mkdir(exist_ok=True)
    if target.is_file():
        return target
    partial = target.with_name(name + '.part')
    status[:] = ['Downloading', name]
    with urllib.request.urlopen(URL + name, timeout=60) as response, partial.open('wb') as out:
        total = 0
        while True:
            block = response.read(262144)
            if not block:
                break
            out.write(block)
            total += len(block)
            status[1] = '%s: %.1f MB' % (name[:24], total / 1048576)
    partial.replace(target)
    return target


def install():
    global finished, success
    log = ROOT / 'install.log'
    try:
        with log.open('w', buffering=1) as output:
            output.write('GrainBrick Ports installer v0.2.2\n')
            if (BASE / 'INSTALL_COMPLETE').is_file():
                raise RuntimeError('Already installed. Launch GrainBrick.')
            if BASE.exists():
                raise RuntimeError('Previous partial install. Send install.log for help.')
            if not (ROOT / APP).is_file():
                raise RuntimeError('Missing application ZIP. See START-HERE.txt.')
            # Fail before downloads when launch would need a password.
            subprocess.run(['sudo', '-n', '-k', 'true'], stdin=subprocess.DEVNULL,
                           stdout=output, stderr=output, check=True)
            ubuntu = download(UBUNTU)
            sums = download('SHA256SUMS')
            status[:] = ['Installing packages', 'Keep power and Wi-Fi connected.']
            cmd = ['bash', str(ROOT / 'install.sh'), str(ROOT / APP),
                   str(ubuntu), str(sums), str(ROOT.parent)]
            with subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, universal_newlines=True,
                                  env=dict(os.environ, DEBIAN_FRONTEND='noninteractive')) as proc:
                for line in proc.stdout:
                    output.write(line)
                    if line.strip():
                        status[1] = line.strip()[-48:]
                if proc.wait():
                    raise RuntimeError('Setup stopped. Send install.log for help.')
            success = True
            status[:] = ['Installation complete', 'Restart EmulationStation, then open Ports.']
    except Exception as exc:
        status[:] = ['Installation stopped', str(exc)]
        with log.open('a') as output:
            output.write('\nERROR: %s\n' % exc)
    finally:
        finished = True


def ui():
    s = C.CDLL('libSDL2-2.0.so.0')
    def bind(name, args, result=C.c_int):
        f = getattr(s, name); f.argtypes = args; f.restype = result; return f
    bind('SDL_Init', [C.c_uint])
    bind('SDL_CreateWindow', [C.c_char_p,C.c_int,C.c_int,C.c_int,C.c_int,C.c_uint], C.c_void_p)
    bind('SDL_CreateRenderer', [C.c_void_p,C.c_int,C.c_uint], C.c_void_p)
    bind('SDL_SetRenderDrawColor', [C.c_void_p,C.c_ubyte,C.c_ubyte,C.c_ubyte,C.c_ubyte])
    bind('SDL_RenderClear', [C.c_void_p]); bind('SDL_RenderDrawPoint', [C.c_void_p,C.c_int,C.c_int])
    bind('SDL_RenderPresent', [C.c_void_p], None)
    bind('SDL_PollEvent', [C.c_void_p]); bind('SDL_NumJoysticks', [])
    bind('SDL_JoystickOpen', [C.c_int], C.c_void_p)
    bind('SDL_DestroyRenderer', [C.c_void_p], None)
    bind('SDL_DestroyWindow', [C.c_void_p], None)
    bind('SDL_GetError', [], C.c_char_p)
    bind('SDL_Quit', [], None)
    if s.SDL_Init(0x20 | 0x200) != 0:
        raise RuntimeError(s.SDL_GetError().decode())
    window = s.SDL_CreateWindow(b'Install GrainBrick', 0, 0, 640, 480, 1)
    renderer = s.SDL_CreateRenderer(window, -1, 0) if window else None
    if not renderer:
        s.SDL_Quit(); raise RuntimeError('Cannot create installer display')
    sticks = [s.SDL_JoystickOpen(i) for i in range(s.SDL_NumJoysticks())]
    font = json.loads((ROOT / 'scripts/font.json').read_text())
    def text(line, y, color=(190,220,240)):
        s.SDL_SetRenderDrawColor(renderer,*color,255)
        for i,ch in enumerate(line[:49]):
            for x,dy in font.get(ch, font['?']):
                s.SDL_RenderDrawPoint(renderer, 24+i*12+x, y+dy)
    event = (C.c_uint32 * 16)()
    started = False
    entered = time.monotonic()
    done_at = None
    try:
        while True:
            if finished and done_at is None:
                done_at = time.monotonic()
            while s.SDL_PollEvent(C.byref(event)):
                kind = event[0]
                if kind == 0x100 and not started:
                    return
                if kind in (0x603, 0x300) and time.monotonic()-entered > 1:
                    if not started:
                        started = True
                        threading.Thread(target=install, daemon=False).start()
                    elif finished and time.monotonic()-done_at > 1:
                        return
            s.SDL_SetRenderDrawColor(renderer,15,22,35,255); s.SDL_RenderClear(renderer)
            text('GRAINBRICK - TEST INSTALLER v0.2.2',25,(255,190,80))
            if not started:
                lines=['RG353VS / ArkOS / Wi-Fi required',
                       'Creates a separate GrainBrick environment.',
                       'Needs 2 GiB free on the system partition.',
                       '', 'Keep power connected during installation.',
                       'Press any face button to begin.']
            else:
                lines=[status[0], '', status[1], '',
                       'Log: ports/grainbrick-rg353vs-arkos/install.log',
                       'Press a button to return.' if finished else 'Please wait. Do not power off.']
            for i,line in enumerate(lines): text(line,100+i*43)
            s.SDL_RenderPresent(renderer)
            time.sleep(.04)
    finally:
        s.SDL_DestroyRenderer(renderer); s.SDL_DestroyWindow(window); s.SDL_Quit()


if __name__ == '__main__':
    try:
        ui()
    except Exception as exc:
        with (ROOT / 'install.log').open('a') as log:
            log.write('Installer display error: %s\n' % exc)
        raise
