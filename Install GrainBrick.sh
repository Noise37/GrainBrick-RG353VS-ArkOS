#!/bin/bash
# Extract beside the grainbrick-rg353vs-arkos folder inside EASYROMS/ports.
set -euo pipefail
PORTS=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT="$PORTS/grainbrick-rg353vs-arkos"
exec 9>"$ROOT/installer.lock"
flock -n 9 || exit 0
# The installer uses host SDL; it never opens an audio device.
unset LD_LIBRARY_PATH SDL_VIDEODRIVER SDL_RENDER_DRIVER LIBGL_ALWAYS_SOFTWARE
export SDL_AUDIODRIVER=dummy
python3 "$ROOT/scripts/ports_install.py" >> "$ROOT/installer-screen.log" 2>&1
