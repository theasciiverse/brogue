#!/bin/sh
# Lays out the av archive in stage/: the start script at the top, the
# binary in lib/, and the keymap template it copies to the player's folder.
set -eu
rm -rf stage && mkdir -p stage/lib
cp bin/brogue stage/lib/brogue
cp asciiverse/brogue stage/brogue
cp bin/keymap.txt stage/keymap.txt
cp LICENSE.txt README.md CHANGELOG.md PATCHES.md stage/
