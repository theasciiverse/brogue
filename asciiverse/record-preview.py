#!/usr/bin/env python3
"""Records asciiverse/brogue.cast, Brogue's catalog preview (hub/RECORDING.md).
Brogue's screen is fixed at 100x34, taller than the 100x30 preview, so this
records at 100x34 and the manifest crops (RECORDING.md, "Record big, crop to
100x30"). It shows the title's flames, then a new game played by a simple
pilot that reads the screen (pyte): it auto-explores (x), walks into any
monster that comes next to it (resting so hunters come), and takes the stairs (>) when a level is done.
After about 35 s it quits (Q, y) to show the gravestone. Needs pyte. Runs
the game in a scratch folder so saves and scores stay out of the repo.
Usage, from the repo root after building bin/brogue:
    python3 asciiverse/record-preview.py"""
import os, pty, re, struct, fcntl, select, shutil, tempfile, termios, time
import pyte

COLS, ROWS = 100, 34
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cast = os.path.join(root, "asciiverse", "brogue.cast")
env = dict(os.environ, TERM="xterm-256color", COLORTERM="truecolor", LANG="C.UTF-8")


# ncurses draws runs of one character with REP (CSI n b), which pyte lacks
class Screen(pyte.Screen):
    last = " "
    def draw(self, data):
        if data: self.last = data[-1]
        super().draw(data)
    def rep(self, n=1, *args, **kwargs):
        self.draw(self.last * max(n, 1))

class Stream(pyte.ByteStream):
    csi = dict(pyte.ByteStream.csi, b="rep")

screen = Screen(COLS, ROWS)
stream = Stream(screen)

work = tempfile.mkdtemp()
shutil.copy(os.path.join(root, "bin", "brogue"), work)
pid, fd = pty.fork()
if pid == 0:
    os.chdir(work)      # saves go here; the recording shows no local paths
    os.execvpe("asciinema", ["asciinema", "rec", "--overwrite", "-q", "-i", "2",
        "--window-size", f"{COLS}x{ROWS}", "--capture-env", "TERM,COLORTERM,LANG",
        "-c", "./brogue", cast], env)
fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", ROWS, COLS, 0, 0))

done = False
def alive():
    global done
    if not done and os.waitpid(pid, os.WNOHANG)[0]: done = True
    return not done

def pump(t):
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.01)
        if r:
            try: stream.feed(os.read(fd, 65536))
            except OSError: return

def key(k, wait=0.0):
    os.write(fd, k); pump(wait)

def text():
    return "\n".join(screen.display)

def wait_for(s, limit=10.0):
    end = time.time() + limit
    while time.time() < end and alive() and s not in text():
        pump(0.1)
    return s in text()

# The sidebar is the left 20 columns, the map the rest, between the three
# message lines at the top and the location line and buttons at the bottom.
MAP_X, MAP_Y0, MAP_Y1 = 21, 3, 31
STEP = {(-1, -1): b"y", (0, -1): b"k", (1, -1): b"u", (-1, 0): b"h",
        (1, 0): b"l", (-1, 1): b"b", (0, 1): b"j", (1, 1): b"n"}

def find(ch):
    """Map cells holding ch on its own (not part of a word)."""
    out = []
    for y in range(MAP_Y0, MAP_Y1):
        row = screen.display[y]
        for x in range(MAP_X, COLS):
            if row[x] == ch and not row[x - 1].isalpha() and \
                    (x + 1 >= COLS or not row[x + 1].isalpha()):
                out.append((x, y))
    return out

def monsters():
    """Letters of the monsters the sidebar lists ("r: Rat")."""
    return [m.group(1) for line in screen.display
            for m in [re.match(r"([A-Za-z]): \w", line[:20])] if m]

wait_for("New Game")
pump(4.0)                       # the title's flames
for _ in range(5):              # New Game; the welcome messages
    key(b"n", 1.0)
    if wait_for("Depth", 3.0): break
pump(2.0)
end = time.time() + float(os.environ.get("PLAY_SECONDS", 34))
waited = 0
while time.time() < end and alive():
    t = text()
    if "--MORE--" in t.upper() or "(y/n)" in t:
        key(b"\x1b", 0.5); continue
    if "Killed by" in t or "You die" in t:
        break
    me = find("@")
    foes = [(x, y) for m in monsters() for x, y in find(m)]
    if me and foes:
        mx, my = me[0]
        fx, fy = min(foes, key=lambda f: max(abs(f[0] - mx), abs(f[1] - my)))
        if max(abs(fx - mx), abs(fy - my)) == 1:
            key(STEP[(fx - mx, fy - my)], 0.3)  # walking into it attacks
            waited = 0
            continue
        if waited < 12:         # let it come (hunting monsters do)
            key(b"z", 0.3); waited += 1
            continue
    waited = 0
    if "Explored" in t or "explored" in t or "no path" in t:
        key(b">", 4.0)          # travel to the stairs and go down
        continue
    key(b"x", 1.5)              # explore until something happens
pump(1.0)
if alive():
    key(b"Q", 1.0)              # quit the game ...
    key(b"y")
    pump(5.0)                   # ... the gravestone
    key(b" ", 1.0)
    if wait_for("Save recording", 3.0):
        key(b"\x1b", 1.0)       # don't save a recording
    wait_for("New Game", 5.0)
    pump(3.0)                   # back to the flames
    key(b"q", 1.0)              # title: Quit
for _ in range(30):
    if not alive(): break
    pump(0.2)
shutil.rmtree(work, ignore_errors=True)
