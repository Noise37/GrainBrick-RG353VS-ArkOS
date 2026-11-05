# GrainBrick for Anbernic RG353VS

**Add GrainBrick to your existing ArkOS setup without formatting your cards or removing your games.**

This is an **unofficial ArkOS installer** for GrainBrick, created and tested by Anthony Jackson with AI-assisted packaging. GrainBrick itself is by **ETRNLIAM and its contributors**.

## Download

Open **Releases** on this repository and download **`grainbrick-rg353vs-ports-v0.2.2.zip`** from the release's **Assets** section.

Use that installer ZIP, rather than GitHub's automatically generated **Source code** downloads.

## Before you start

- You need an **Anbernic RG353VS running ARM64 ArkOS**, a Windows PC, an SD card reader, and Wi-Fi.
- Back up your cards and game saves first.
- Installation needs **at least 2 GiB free on the system partition**. Free space on the games partition alone is not enough. The installer checks this automatically.
- Keep power connected during installation.
- **No PowerShell or SSH is needed** for a normal installation.
- Already have GrainBrick? This installer is **not an upgrade tool**. It stops rather than overwriting an existing launcher or its own installation. Back up your projects and ask for migration help first.

## 1. Choose the correct SD card

**Shut down your handheld completely before removing a card.**

| Your setup | Which card goes into your PC? |
| --- | --- |
| Two cards | The **games card from TF2**. Leave the ArkOS card from TF1 alone. |
| One card | The card from **TF1/OS**. |

1. Insert the correct card into your Windows PC.
2. Open **File Explorer → This PC**.
3. Open the card's games partition. It may be named **EASYROMS**.
4. Open its existing **`ports`** folder. You may recognize files from other installed ports.

**If Windows asks you to format a partition, click Cancel. Do not format the card.**

## 2. Download and extract the installer

1. Download **`grainbrick-rg353vs-ports-v0.2.2.zip`** from this repository's release page.
2. Find it in your Windows **Downloads** folder.
3. Right-click it and select **Extract All**.
4. Click **Extract** and open the extracted folder.

You should find:

| Item | What it is |
| --- | --- |
| `Install GrainBrick.sh` | The installer menu entry |
| `grainbrick-rg353vs-arkos` | A folder containing installer files |
| `START-HERE.txt` | An offline installation guide |
| `README.md` | This GitHub-formatted guide |

If another enclosing folder appears first, open it until you see these items.

## 3. Copy two items into `ports`

Copy **both** of these items from the extracted download:

| Copy this | Put it here |
| --- | --- |
| `Install GrainBrick.sh` | Games card → **ports** |
| Entire `grainbrick-rg353vs-arkos` folder | Games card → **ports** |

**The `.sh` file and the folder must sit beside each other.**

- Do not copy the outer `grainbrick-rg353vs-ports-v0.2.2` folder into `ports`.
- Do not put `Install GrainBrick.sh` inside `grainbrick-rg353vs-arkos`.
- You do not need to copy `README.md` or `START-HERE.txt` onto the card.
- If Windows asks to replace existing files, stop and check whether you already have an earlier installation.

## 4. Add the original GrainBrick application

1. Open the [original creator's GrainBrick release page](https://github.com/ETRNLIAM/GrainBrick/releases/tag/v1.0.1-beta.2).
2. Expand **Assets** if needed.
3. Download **`grainbrick.beta.1.0.1.zip`**. Choose the application ZIP, **not “Source code.”**
4. **Leave this ZIP compressed. Do not extract it.**
5. Copy it into **Games card → ports → grainbrick-rg353vs-arkos**.

Inside that folder, these items should now be together:

| Item | Type |
| --- | --- |
| `grainbrick.beta.1.0.1.zip` | Compressed original application |
| `install.sh` | Installer script |
| `scripts` | Folder |
| `docs` | Folder |
| Other included files | Leave them in place |

The application ZIP belongs **beside `install.sh`**, not inside `scripts` or `docs`.

You can reuse an existing copy of that exact original application ZIP. The installer checks its hash and refuses a different or repacked version.

**You do not need to download Ubuntu separately.** The installer handles its required downloads.

## 5. Return the card to the handheld

1. Safely eject the card from Windows.
2. Return it to the **same slot it came from**:
   - **Two cards:** games card in TF2, original ArkOS card in TF1.
   - **One card:** card in TF1/OS.
3. Power on.
4. Confirm your Wi-Fi connection under **Options → WiFi**.
5. Keep power connected.

## 6. Install and launch

1. Open **Ports → Install GrainBrick**.
2. Read the installer screen.
3. Press a face button to begin.
4. Wait while the required files download and install. This can take several minutes. **Do not power off or remove the card.**
5. Wait for **Installation complete**.
6. Press a button to return to the menu.
7. Restart EmulationStation using its menu, or shut down normally and boot again.
8. Open **Ports → GrainBrick**.

## 7. Check everything works

1. Load a sample and start playback. Raise the volume gradually.
2. Test the D-pad, face buttons and shoulder buttons.
3. In the project filename dialog, check that **physical X saves** and **Y cancels**.
4. Save a named project, close GrainBrick, reopen it, and load that project.
5. Fully reboot and check sound, controls and project loading again.
6. Check that your existing games still launch normally.

The installer creates a separate GrainBrick environment. It does not automatically migrate projects from an older GrainBrick installation.

## Troubleshooting

### The installer does not appear in Ports

Restart EmulationStation. Check that **`Install GrainBrick.sh` is directly inside `ports`**, beside the `grainbrick-rg353vs-arkos` folder.

Make sure Windows has not added `.txt` to the filename. To show extensions:

- **Windows 11:** File Explorer → View → Show → File name extensions.
- **Windows 10:** File Explorer → View → File name extensions.

### Installation stops, or its screen does not open

Do not format the card or delete game folders. Shut down normally, insert the games card into your PC, and find:

| Log | Location |
| --- | --- |
| `install.log` | Games card → ports → grainbrick-rg353vs-arkos |
| `installer-screen.log` | Games card → ports → grainbrick-rg353vs-arkos |

Send whichever logs exist, the error message, your model, and your ArkOS version when asking for help. A partial installation is retained for diagnosis; automatic resume is not supported.

## Compatibility and test status

| Setup | Reported result |
| --- | --- |
| RG353VS / ArkOS 2.0 (10162023), existing games setup | Owner reports v0.2.2 installation and testing working |
| RG353VS / ArkOS 2.0 (02092025) | Earlier v0.2.0 installation plus the manually applied SDL fix worked, including after reboot |

The exact combined v0.2.2 ZIP has not been separately confirmed on a fully clean 02092025 installation. Other handheld models, dArkOS, USB recording and extended stability remain untested. Do not assume support for every Anbernic handheld.

## Source and credits

The **integration installer and launcher source** are in this directory. GrainBrick's proprietary synthesizer source, application binaries, samples, Ubuntu files and GPU binaries are not included in this release ZIP.

- **GrainBrick:** ETRNLIAM and its contributors.
- **ArkOS adaptation and device testing:** Anthony Jackson.
- **Packaging and documentation:** AI-assisted.
- The included MIT license covers this integration project's code and documentation only. Third-party components retain their own rights and licenses.
