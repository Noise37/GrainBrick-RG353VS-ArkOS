#!/bin/bash
# Community installer v0.2.2. Does not upgrade ArkOS or modify its graphics libraries.
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
BASE=/home/ark/grainbrick-arkos
APP='grainbrick beta 1.0.1'
usage() {
  echo 'Usage: bash install.sh GRAINBRICK.zip ubuntu-base-24.04.5-base-arm64.tar.gz SHA256SUMS /roms2/ports'
  echo 'Verify archives only: bash install.sh --verify-only GRAINBRICK.zip UBUNTU.tar.gz SHA256SUMS'
}
verify_only=0
if [[ ${1:-} == --verify-only ]]; then verify_only=1; shift; fi
if [[ $verify_only == 1 ]]; then [[ $# == 3 ]] || { usage; exit 2; }
else [[ $# == 4 ]] || { usage; exit 2; }; fi
python3 "$HERE/scripts/verify_inputs.py" "$1" "$2" "$3"
[[ $verify_only == 0 ]] || exit 0
[[ $(id -un) == ark && $EUID != 0 ]] || { echo 'Run as the normal ark user, without sudo.'; exit 1; }
[[ $(uname -m) == aarch64 ]] || { echo 'Requires ARM64 ArkOS.'; exit 1; }
[[ -r /proc/device-tree/model ]] || { echo 'Cannot verify handheld model.'; exit 1; }
model=$(tr -d '\0' < /proc/device-tree/model)
case ${model,,} in *rg353v*) ;; *) echo "Model not recognized as RG353V/VS: $model"; exit 1;; esac
# Some VS images use the RG353V device-tree name. This is not validation on RG353V.
[[ -d /opt && -d /roms && -f /etc/os-release ]] || exit 1
ports=$(realpath -e -- "$4")
case "$ports" in /roms/ports|/roms2/ports) ;; *) echo 'Choose /roms/ports or /roms2/ports.'; exit 1;; esac
[[ -w "$ports" ]] || { echo 'Ports directory is not writable.'; exit 1; }
for launcher in "$ports/GrainBrick.sh" "$ports/GrainBrick Community.sh"; do
  [[ ! -e "$launcher" && ! -L "$launcher" ]] || {
    echo "Launcher already exists: $launcher; no files overwritten."; exit 1;
  }
done
[[ ! -e "$BASE" && ! -L "$BASE" ]] || {
  echo "$BASE already exists. Installer refuses to overwrite data; see docs/TROUBLESHOOTING.md."; exit 1;
}
[[ $(findmnt -n -o FSTYPE -T /home/ark) == ext4 ]] || {
  echo 'This release requires ext4 at /home/ark. Do not extract the rootfs onto FAT32.'; exit 1;
}
for tool in sudo unshare chroot tar unzip cp cmp ln flock realpath findmnt; do
  command -v "$tool" >/dev/null || { echo "Missing host tool: $tool"; exit 1; }
done
free_kb=$(df -Pk /home/ark | awk 'NR==2 {print $4}')
(( free_kb >= 2097152 )) || { echo 'Need at least 2 GiB free; 3 GiB recommended.'; exit 1; }
S=/usr/lib/aarch64-linux-gnu
M=libmali-bifrost-g52-g2p0-gbm.so
for file in "$S/$M" "$S/libEGL.so.1" "$S/libGLESv2.so.2" /lib/aarch64-linux-gnu/libdrm.so.2; do
  [[ -f "$file" ]] || { echo "Missing tested host graphics file: $file"; exit 1; }
done
cmp "$S/$M" "$S/libEGL.so.1"
cmp "$S/$M" "$S/libGLESv2.so.2"
sudo -n -k true || { echo "ArkOS passwordless sudo is required."; exit 1; }
sudo -n unshare --mount --propagation private /bin/true || {
  echo 'Passwordless launch is unavailable. Do not change sudoers blindly; see troubleshooting.'; exit 1;
}
mkdir -m 755 "$BASE"
touch "$BASE/INSTALL_INCOMPLETE"
R=$BASE/rootfs
mkdir "$R"
# No existing destination is reused; the Ubuntu archive passed its checksum check.
sudo tar -xpf "$2" -C "$R"
sudo unshare --mount --propagation private /bin/bash "$HERE/scripts/setup-rootfs.sh" "$R"
mkdir "$BASE/unpacked"
unzip -q "$1" -d "$BASE/unpacked"
sudo mkdir -p "$R/userdata/roms/ports" "$R/opt/arkos-gpu" "$R/home/ark"
sudo cp -a "$BASE/unpacked/$APP" "$R/userdata/roms/ports/"
P="$R/userdata/roms/ports/$APP"
sudo mkdir -p "$P/samples" "$P/projects" "$P/recordings"
# Use one physical driver file with aliases, NOT separate copies of identical Mali files.
D="$R/opt/arkos-gpu"
sudo cp -L "$S/$M" "$D/$M"
sudo cp -L /lib/aarch64-linux-gnu/libdrm.so.2 "$D/libdrm.so.2"
for alias in libEGL.so.1 libGLESv2.so.2 libgbm.so.1; do
  sudo ln -s "$M" "$D/$alias"
done
sudo cp -an "$P/demo-samples/." "$P/samples/"
sudo cp -an "$P/demo-projects/." "$P/projects/"
sudo chown -R "$(id -u):$(id -g)" "$P" "$R/home/ark"
python3 "$HERE/scripts/apply_controller_fix.py" "$P"
cp "$HERE/scripts/run-rootfs.sh" "$BASE/run-rootfs.sh"
chmod 755 "$BASE/run-rootfs.sh"
# Verify the native engine libraries and bundled NumPy without grabbing audio or display.
sudo chroot "$R" /usr/bin/env LD_LIBRARY_PATH="/opt/arkos-gpu:/userdata/roms/ports/$APP" \
  python3 -c 'import ctypes,sys; p="/userdata/roms/ports/grainbrick beta 1.0.1"; sys.path.insert(0,p+"/_vendor"); import numpy,pygame; assert numpy.__version__=="1.26.4"; assert int(numpy.sum([1,2,3]))==6; ctypes.CDLL(p+"/libSoundTouch.so.1"); ctypes.CDLL("/opt/arkos-gpu/libgbm.so.1"); print("Runtime load checks passed")'
mv "$BASE/INSTALL_INCOMPLETE" "$BASE/INSTALL_COMPLETE"
cp "$HERE/scripts/GrainBrick.sh" "$ports/GrainBrick.sh"
chmod +x "$ports/GrainBrick.sh"
echo 'Installed. Restart EmulationStation, then open Ports > GrainBrick.'
echo 'See docs/TESTING.md for confirmed tests and remaining release checks.'
