# Brogue CE (Asciiverse packaging)

Brogue: Community Edition 1.15.1, the terminal (ncurses) version, packaged
for the Asciiverse catalog and as system packages. Upstream is active
(github.com/tmewett/BrogueCE, remote `upstream`); `main` is their
`v1.15.1` tag plus our packaging. A classic: don't change the game; list
anything we do change in PATCHES.md, small enough to offer upstream.

- `origin` is to be github.com/theasciiverse/brogue.
- Release: tag `v<upstream version>-av.<n>` (first: `v1.15.1-av.1`) and
  push it. For a new upstream release, merge its tag into `main`.
- Local build: `sh asciiverse/build.sh` (needs libncurses-dev) leaves
  `bin/brogue`. Static build: `docker run --rm -v "$PWD":/src -w /src
  alpine:3.22 sh asciiverse/build.sh`.
- Saves and scores live where it runs; `asciiverse/brogue` runs it from
  ~/.local/share/Brogue.
- Needs 100x34. The preview is recorded at 100x34 and cropped to 100x30
  by the manifest (hub/RECORDING.md).
- Preview: `python3 asciiverse/record-preview.py` (needs pyte).
