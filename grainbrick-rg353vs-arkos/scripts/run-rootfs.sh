#!/bin/bash
# Called through sudo/unshare; transient mounts vanish with the namespace.
set -euo pipefail
BASE=/home/ark/grainbrick-arkos
R=$BASE/rootfs
P='/userdata/roms/ports/grainbrick beta 1.0.1'
[[ -f "$BASE/INSTALL_COMPLETE" ]] || { echo 'Installation incomplete.'; exit 1; }
[[ -f "$R$P/gb_launch.py" ]] || exit 1
mount --rbind /dev "$R/dev"
mount -t proc proc "$R/proc"
mount --rbind /sys "$R/sys"
uid=$(id -u ark)
gid=$(id -g ark)
groups=$(id -G ark | tr ' ' ',')
# Dummy applies only to SDL/Pygame audio. GrainBrick aplay still uses ALSA.
exec chroot --userspec="$uid:$gid" --groups="$groups" "$R" \
  /usr/bin/env -C "$P" \
  HOME=/home/ark PYTHONUNBUFFERED=1 OPENBLAS_NUM_THREADS=1 \
  GRAINBRICK_ROOT="$P" GRAINBRICK_DISPLAY_FILTER=smooth \
  LD_LIBRARY_PATH="/opt/arkos-gpu:$P" \
  SDL_VIDEODRIVER=kmsdrm SDL_AUDIODRIVER=dummy \
  /usr/bin/python3 -B gb_launch.py
