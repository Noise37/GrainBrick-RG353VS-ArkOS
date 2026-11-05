#!/bin/bash
# Called as root inside a private mount namespace by install.sh.
set -euo pipefail
R=$1
mount --rbind /dev "$R/dev"
mount -t proc proc "$R/proc"
mount --rbind /sys "$R/sys"
# R is a new verified Ubuntu extraction, never the host root.
cp --remove-destination -L /etc/resolv.conf "$R/etc/resolv.conf"
printf '#!/bin/sh\nexit 101\n' > "$R/usr/sbin/policy-rc.d"
chmod 755 "$R/usr/sbin/policy-rc.d"
chroot "$R" /bin/bash -c '
set -euo pipefail
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  python3 python3-pygame libstdc++6 libegl1 libgles2 libgl1-mesa-dri alsa-utils
apt-get clean
python3 -c "import sys, pygame; assert sys.version_info[:2] == (3,12); print(pygame.version.ver)"
command -v aplay
command -v arecord
'
