#!/bin/bash
set -euo pipefail
BASE=/home/ark/grainbrick-arkos
[[ -f "$BASE/INSTALL_COMPLETE" ]] || { echo 'Run the community installer first.'; exit 1; }
exec 9>"$BASE/session.lock"
flock -n 9 || { echo 'GrainBrick is already running.'; exit 1; }
# Keep a previous session for troubleshooting, without accumulating huge logs.
if [[ -f "$BASE/grainbrick.log" ]]; then
  mv -f "$BASE/grainbrick.log" "$BASE/grainbrick.previous.log"
fi
sudo -n unshare --mount --propagation private /bin/bash "$BASE/run-rootfs.sh" \
  > "$BASE/grainbrick.log" 2>&1
