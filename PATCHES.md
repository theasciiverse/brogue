# Changes from upstream

This is the Asciiverse packaging of Brogue: Community Edition 1.15.1
(AGPL-3.0-or-later), Brian Walker's roguelike as kept by the Brogue CE
team (github.com/tmewett/BrogueCE). `main` starts at upstream's `v1.15.1`
tag, with upstream's history; the `upstream` remote points there.

We ship the terminal (ncurses) version only: built with `TERMINAL=YES
GRAPHICS=NO`, it needs no SDL and no data files, and starts in terminal
mode without `-t`.

## The game

Unchanged. No file under `src/` differs from `v1.15.1`.

## Packaging (new files)

- `asciiverse/brogue`: the start script, for the av archive and for the
  system packages. Brogue keeps saves, recordings, high scores and
  `keymap.txt` in the current directory; the script runs it from
  `${XDG_DATA_HOME:-~/.local/share}/Brogue`, the folder upstream's
  `linux/brogue-multiuser.sh` suggests, and copies the commented
  `keymap.txt` there on first run.
- `asciiverse/build.sh`: static Linux build in Alpine, macOS builds per
  architecture, through upstream's Makefile with its options and link
  libraries set on make's command line.
- `asciiverse/stage.sh`: the av archive (start script, `lib/brogue`,
  keymap template).
- `asciiverse/nfpm.yaml`: .deb, .rpm, .apk and Arch packages:
  `/usr/bin/brogue` (the start script), `/usr/lib/brogue/brogue`,
  `/usr/share/brogue/keymap.txt`.
- `asciiverse/record-preview.py`: records the catalog preview at 100x34
  with a pilot that reads the screen through pyte; the kept take is
  `asciiverse/brogue.cast`.
- `.github/workflows/release.yml`: builds all of it on a tag. Upstream's
  own workflows are left as they are.
- `.gitignore`: `stage/` and `dist/`.

## Not changed

- The screen is a fixed 100x34. In a smaller terminal Brogue asks the
  window to grow (xterm's resize sequence) and otherwise waits, showing
  the size it needs.
- No graphical (SDL) version, no tiles.
- No Windows build.
