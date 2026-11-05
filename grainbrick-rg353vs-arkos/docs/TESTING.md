# Test status — v0.2.2

## Reported hardware evidence

RG353VS, ArkOS 2.0 (02092025), Linux 4.19.172 ARM64, spare 128 GB card.
User reported v0.2.0 Ports install working. Subsequent SSH diagnostics found
retrogame_joypad, raw and Pygame joystick X=2/Y=3, SDL mapping x:b2/y:b3.
JSON binding edits and JOYBUTTON-only interception failed to fix the dialog.
The SDL Controller.set_mapping fix x:b3/y:b2 succeeded: physical X saves.
User then confirmed all buttons working, rebooted the console, and reported
that everything remained working. Sound and project saving/reopening had
also been reported working earlier in the session.

## v0.2.2 existing-system installation — owner reported success

On November 4, 2026, the owner tested the v0.2.2 procedure on the original
RG353VS card with ArkOS 2.0 (10162023) and existing games (two-card setup).
Old GrainBrick launchers were moved out of Ports; its earlier manual environment
was retained separately. The owner then reported: "After testing everything is
working." This is evidence for installing into an existing system. The earlier
manual environment means it is not evidence for a fully erased OS baseline.
No new SSH button patch was requested during this installation test.

## Remaining coverage

A fully clean installation of the combined v0.2.2 on the newer 02092025 image
has not been separately confirmed. The earlier 02092025 evidence is for
v0.2.0 followed by a manually applied controller fix.
Exact long-session duration and individual game/M8 tests were not reported;
do not infer those from the general success report.
Test 20+ minute playback and game operation before/after installation.
Other hardware/OS variants, USB audio/recording and long-session stability
remain untested. Do not advertise universal Anbernic compatibility.

## Local validation

Archive safety and installer failure handling have automated coverage.
Controller patch tests check target-only changes, preservation of other controls,
backup creation, repeat invocation and refusal of unexpected launcher text.
SDL installer rendering/button navigation previously passed dummy-video testing.
Local tests do not replace hardware acceptance of the combined ZIP.
