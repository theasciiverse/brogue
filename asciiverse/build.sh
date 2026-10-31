#!/bin/sh
# Builds Brogue's terminal version (ncurses, no SDL). Linux: run inside
# alpine:3.22 for a fully static binary; macOS: run on the runner with
# CC_ARCH set to x86_64 or arm64, linking the system's ncurses.
#   docker run --rm -v "$PWD":/src -w /src alpine:3.22 sh asciiverse/build.sh
# Leaves bin/brogue. Upstream's Makefile is used as is: options and the
# link libraries are set on make's command line. A terminal-only build
# needs no data files and starts in terminal mode without -t.
set -eu
if [ -f /etc/alpine-release ]; then
  apk add --no-cache build-base bash ncurses-dev ncurses-static >/dev/null
  libs="-lm -lncursesw" ldflags="-static"
else
  libs="-lm -lncurses" ldflags=""
fi
cc="cc${CC_ARCH:+ -arch $CC_ARCH}"
make -B -j4 TERMINAL=YES GRAPHICS=NO RELEASE=YES DATADIR=. \
  CC="$cc" LDFLAGS="$ldflags" libs="$libs" bin/brogue
strip bin/brogue
