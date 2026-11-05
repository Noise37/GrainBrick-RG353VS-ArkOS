# Publish this on GitHub — beginner guide

## What you are publishing

Suggested repository name: **grainbrick-rg353vs-arkos**.
Suggested description: **Unofficial experimental GrainBrick 1.0.1 installer and launcher for Anbernic RG353VS running ArkOS.**

Your repository holds the readable installer/launcher code. A Release ZIP gives users
a convenient download. These are not GrainBrick's closed-source synthesizer code or
an official developer-supported ArkOS port. Source code is already included in this ZIP.
You do not need to compile it into a Windows EXE.

## Create the repository

1. Sign into your own account at https://github.com/.
2. Use **New repository** (normally under the + menu).
3. Enter the suggested name and description. Choose Public if you want anyone to see it.
4. Do not have GitHub create a README or license: this package already has both.
5. Create the repository.

## Upload the source files

1. Extract the supplied ZIP on Windows.
2. On the new repository's page use the **uploading an existing file** link, or
   **Add file > Upload files** once the repository has content.
3. Upload the **contents** of `grainbrick-rg353vs-arkos`, preserving the `scripts`,
   `docs` and `tests` folders. README.md should be at the repository's top level.
   If your browser hides dotfiles, add `.gitignore` and `.gitattributes` individually.
4. Do not upload the original ZIP as your only source file. Do not upload GrainBrick's
   binary ZIP, Ubuntu archives, runtime folders, private projects, logs or screenshots.
5. Enter a commit message such as `Add experimental RG353VS ArkOS integration` and commit.

A commit is a saved revision. A repository is the project folder plus its history.
A release is a named version that users can download.

## Make a downloadable prerelease

1. Open your repository's **Releases** area and choose **Draft a new release**.
2. Create tag **v0.1.0** and title **RG353VS ArkOS integration v0.1.0 — experimental**.
3. Paste the text from `docs/RELEASE-NOTES.md` into the release description.
4. Attach the supplied source/installer ZIP as a release asset.
5. Mark **This is a pre-release**. Publish only when you are ready for public testers.

GitHub also provides automatic Source code ZIP/TAR downloads for the tag. Those hold
the committed source. Your attached ZIP is the curated download with the same scripts.
There is no full runtime/application ZIP in this project.

## Before asking other people to install

Test on a spare SD card, follow `docs/TESTING.md`, and record the exact ArkOS version.
The scripts were assembled after the manual setup succeeded; a clean install has not
yet been demonstrated. Keep that limitation in the README and release notes until it is.
Ask testers to report model, ArkOS version, last install output, and whether graphics,
audio, save/reload and exit worked. Ask them to remove personal filenames from logs.

## Updating later

Edit the source, describe what changed, and commit it. For a new download make a new
tag such as v0.1.1; don't silently replace a release advertised as tested.
To regenerate the ZIP on a computer with Python 3:

```bash
python3 build_release.py
```

The output is written to `dist/`, which is excluded from the source repository.
For a hosted GitHub workflow later, add automated checks only after you understand
the manual release process. No GitHub account, repository, or public release was
created by preparing these files.
