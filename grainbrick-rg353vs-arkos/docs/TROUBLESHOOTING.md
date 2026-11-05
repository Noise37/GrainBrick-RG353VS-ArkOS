# Troubleshooting, data and removal

## Locations

Community environment: `/home/ark/grainbrick-arkos/rootfs`

App, samples, projects and recordings are beneath:

```
/home/ark/grainbrick-arkos/rootfs/userdata/roms/ports/grainbrick beta 1.0.1/
```

Latest log: `/home/ark/grainbrick-arkos/grainbrick.log`
Previous log: `/home/ark/grainbrick-arkos/grainbrick.previous.log`

Anthony's original manual installation uses `/home/ark/grainbrick-test` instead.
The package does not automatically import that data or use its old Ports entry.

## Installation stops

Do not delete or rerun blindly. Keep the terminal error and identify whether
`INSTALL_INCOMPLETE` or `INSTALL_COMPLETE` exists in the community directory.
The installer intentionally refuses an existing destination. A partial installation
contains no preexisting community data, but inspect it before moving it aside with
a new name for a retry. Never move a running/mounted rootfs. A full reboot after
closing the app clears transient mount namespaces. Source archives are not modified.

If `sudo -n` fails after a reboot, the launcher cannot obtain required privileges.
The installer does not edit sudoers or disable password checks. Ask an ArkOS maintainer
how that image expects privileged port launchers to run rather than adding broad rules.

If an archive hash fails, stop. Re-download from the official sources and confirm
version. Do not replace the expected hash just to bypass the check.

## Blank screen

The original failure came from mismatched/duplicated graphics files. Preserve
`/opt/arkos-gpu` links: `libEGL.so.1`, `libGLESv2.so.2` and `libgbm.so.1` must resolve
to the same Mali file. Do not copy separate physical versions of that driver under
each alias. Ubuntu SDL is intentionally used instead of the older ArkOS SDL because
Ubuntu's Pygame rejects the older SDL at import. Do not globally replace host libraries.

## Silent audio

Keep `SDL_AUDIODRIVER=dummy` in the launcher. This stops Pygame from holding the
physical PCM device; GrainBrick's `aplay` output is separate and must be installed.
With GrainBrick open, `sudo fuser -v /dev/snd/*` can identify a sound-device owner.
Do not kill EmulationStation, all Python processes, or M8 indiscriminately.
Load a sample and test actual playback. Grain state alone does not prove audible output.
USB/HDMI card ordering and mixer settings may differ from the tested internal card 0.

## Project save quirks

The tested owner found X followed by Y saved from the filename dialog despite labels
suggesting Y cancels. Reopening the project confirmed persistence. Cause is unknown;
this is not proof that all global X/Y mappings should be swapped.
Keep the app directory owned by `ark` and check disk space if save fails. Never apply
`chmod -R 777` to fix an unknown problem. Photos of the save screen and a fresh log help.

## Exit fallback

The project has no hardcoded guessed controller-exit shortcut. Use GrainBrick's own
exit action once established on your device. If stuck, this SSH command requests a
normal termination of the exact main command used by this launcher:

```bash
pkill -TERM -u ark -f '^/usr/bin/python3 -B gb_launch[.]py$'
```

Run only when you mean to close GrainBrick, and do not run simultaneous manual/test
copies. Verify the Ports menu returns. SIGTERM allows the app to handle shutdown,
but save your named project first; unsaved changes are not guaranteed to survive.
Do not use power-off as the normal way to exit.

## Personal backup

Close GrainBrick first. To back up all its app files and user data in this installation:

```bash
tar -czf /home/ark/GrainBrick-personal-backup.tar.gz \
  -C /home/ark/grainbrick-arkos/rootfs/userdata/roms/ports \
  'grainbrick beta 1.0.1'
```

For Anthony's existing manual setup substitute `grainbrick-test` for `grainbrick-arkos`.
Copy that personal archive to your PC using SCP. It includes third-party binaries and
possibly private recordings: keep it private, not in the GitHub integration repository.

## Remove without deleting projects

Close the app, reboot normally if necessary, and remove only the
`GrainBrick.sh` entry from your selected Ports folder. This disables launch
while retaining the environment and all data. Only after a verified private backup
should you manually remove the dedicated `/home/ark/grainbrick-arkos` directory.
No automated destructive uninstall is provided. Do not remove the original manual
setup or M8 folders as part of this operation.
