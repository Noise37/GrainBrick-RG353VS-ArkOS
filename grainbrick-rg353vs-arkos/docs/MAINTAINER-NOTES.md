# GrainBrick on Anbernic RG353VS / ArkOS — v0.2.2 experimental

Copy-to-Ports installer, launcher, and integration source for GitHub.
Read **START-HERE.txt** in the release ZIP or **docs/INSTALL-WINDOWS.md**.
No PowerShell or SSH is required for a normal installation.
This is not the proprietary GrainBrick synthesizer source.

## Hardware results

Anthony Jackson reports that the v0.2.0 Ports installation worked on a spare
card with RG353VS, ArkOS 2.0 (02092025), Linux 4.19.172 ARM64.
After applying the SDL controller fix now packaged in v0.2.2, all buttons worked,
physical X saved, and operation remained working after a full console restart.
Earlier testing also confirmed sound, saving projects and reopening them.

**The owner reports a successful v0.2.2 installation on the existing games setup
with ArkOS 2.0 (10162023), followed by testing with everything working.**
The earlier manual environment was retained and its launchers were backed up;
this validates the existing-system install path, not a fully erased OS baseline.
The simplified public installation guide is START-HERE.txt in the ZIP.
Other models, dArkOS, USB recording and extended-session stability are untested.

## What changed

`apply_controller_fix.py` inserts the hardware-tested SDL controller remapping
before the launcher imports GrainBrick. For `retrogame_joypad`, it maps SDL x to
b3 and y to b2. It keeps all other controls and controllers unchanged, and does
not edit the application button_mapping.json. No system-wide mapping is changed.
A copy of the original application launcher is retained.
Raw joystick numbers X=2/Y=3 alone were insufficient: editing application JSON
and swapping JOYBUTTON events did not fix the filename dialog.

## Requirements and downloads

- RG353VS, ARM64 ArkOS, working Wi-Fi, passwordless ArkOS sudo.
- At least 2 GiB free on /home/ark on ext4 (3 GiB recommended).
- Windows PC and card reader, or equivalent file-copy workflow.
- Existing ArkOS Mali G52 GBM driver and matching EGL/GLES aliases.
- Official application asset `grainbrick.beta.1.0.1.zip` from
  https://github.com/ETRNLIAM/GrainBrick/releases/tag/v1.0.1-beta.2
  Download it separately and keep it compressed beside install.sh.

Ubuntu Base 24.04.5 ARM64 and SHA256SUMS download automatically from Canonical.
Checksums verify integrity; the installer does not verify Canonical's GPG signature.
The original application archive is pinned to the previously tested SHA256.
No third-party application, operating system, GPU binaries or samples are bundled.

## Design

Ubuntu provides Python 3.12 and SDL 2.30 in a dedicated chroot. The host's Mali
and libdrm are copied locally; EGL/GLES/GBM aliases share one physical Mali file.
SDL_AUDIODRIVER=dummy keeps Pygame from occupying audio used by the aplay worker.
The launcher runs as ark with its groups in a private mount namespace.
This compatibility environment is not a security sandbox.
Existing games, M8 scripts and the earlier manual environment are not overwritten.
Existing community installations are deliberately not upgraded by install.sh.

## Source and licenses

The integration shell/Python source is included. build_release.py rebuilds the
ZIP when its parent folder contains Install GrainBrick.sh and START-HERE.txt.
The MIT license applies to this integration code/documentation only.
GrainBrick belongs to ETRNLIAM and its contributors; third-party rights remain.
Device adaptation/testing: Anthony Jackson. Packaging is AI-assisted.
The bitmap font's license is in docs/FONT-LICENSE.txt.
