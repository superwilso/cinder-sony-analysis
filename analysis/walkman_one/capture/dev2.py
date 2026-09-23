"""Host side of fbtool: one adb call per action, frames pulled RLE-compressed and cached by hash."""
import os, subprocess, time
import numpy as np
from PIL import Image

SP = os.path.dirname(os.path.abspath(__file__))
TOOL = "/tmp/fbtool"
RLE = "/tmp/fb.rle"
LOCAL = os.path.join(SP, "fb.rle")
W, H = 480, 800

_cache = {}          # hash -> RGB array
stats = {"adb": 0, "pull": 0, "t_adb": 0.0, "t_pull": 0.0}


class ScreenOff(Exception):
    pass


def sh(cmd, timeout=40):
    t = time.time()
    r = subprocess.run(["adb", "shell", cmd], capture_output=True, text=True, timeout=timeout)
    stats["adb"] += 1
    stats["t_adb"] += time.time() - t
    return r.stdout.replace("\r", "").strip()


def adb_up():
    r = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    return any(l.endswith("\tdevice") for l in r.stdout.splitlines())


def wait_adb(t=90):
    end = time.time() + t
    while time.time() < end:
        if adb_up():
            return True
        time.sleep(1)
    return False


def install():
    subprocess.run(["adb", "push", os.path.join(SP, "fbtool"), TOOL], capture_output=True)
    sh(f"chmod 755 {TOOL}")


def _decode(path):
    raw = open(path, "rb").read()
    assert raw[:4] == b"RLE1", raw[:8]
    n = int.from_bytes(raw[4:8], "little")
    runs = np.frombuffer(raw[8:8 + n * 6], dtype=[("n", "<u2"), ("p", "<u4")])
    px = np.repeat(runs["p"], runs["n"].astype(np.int64))
    assert px.size == W * H, px.size
    b = px.view(np.uint8).reshape(H, W, 4)
    return b[:, :, [2, 1, 0]].copy()


def fetch(h):
    """The frame whose hash is h: from the cache, or pulled (fbtool already wrote it)."""
    if h in _cache:
        return _cache[h]
    t = time.time()
    subprocess.run(["adb", "pull", RLE, LOCAL], capture_output=True)
    stats["pull"] += 1
    stats["t_pull"] += time.time() - t
    a = _decode(LOCAL)
    _cache[h] = a
    return a


def grab():
    """(hash, frame) of what is on screen now."""
    h = sh(f"{TOOL} grab {RLE}")
    if not h:
        raise RuntimeError("fbtool grab failed")
    if h in _cache:
        return h, _cache[h]
    return h, fetch(h)


def backlight():
    try:
        return int(sh("cat /sys/class/leds/lcd-backlight/brightness") or 0)
    except Exception:
        return -1


def _act_then_wait(act, base, quiet, timeout):
    out = sh(f"{act} && {TOOL} wait {base or '0'} {quiet} {timeout} {RLE}")
    last = out.splitlines()[-1] if out else ""
    if last == "off":
        raise ScreenOff()
    kind, _, h = last.partition(" ")
    if kind not in ("changed", "same"):
        raise RuntimeError(f"fbtool: {out!r}")
    if kind == "same":
        return False, h, _cache.get(h)
    return True, h, fetch(h)


def tap(x, y, base, quiet=450, timeout=1200):
    """Tap, then wait for the screen to change and settle. Returns (changed, hash, frame)."""
    return _act_then_wait(f"{TOOL} tap {int(x)} {int(y)}", base, quiet, timeout)


def swipe(x0, y0, x1, y1, base, dur=250, hold=0, quiet=400, timeout=1500):
    return _act_then_wait(f"{TOOL} swipe {x0} {y0} {x1} {y1} {dur} {hold}", base, quiet, timeout)


def key(code, dev="/dev/input/event4"):
    sh(f"{TOOL} key {dev} {code}")


_last_power = [0.0]


def wake():
    """Short power press. USB re-enumerates on wake, and stock lands on its USB screen.

    POWER TOGGLES. Pressed while a wake is already under way it switches the panel back OFF, the
    player suspends, and adb goes with it — nothing over USB can undo that (2026-09-23, a human had
    to press the button). So: re-read the backlight for ~1.5 s first, press only if it is still 0,
    and never press twice within 15 s."""
    for _ in range(3):
        if backlight() > 0:
            return
        time.sleep(0.5)
    if time.time() - _last_power[0] < 15:
        time.sleep(15 - (time.time() - _last_power[0]))
        if backlight() > 0:
            return
    _last_power[0] = time.time()
    try:
        sh(f"{TOOL} key /dev/input/event0 116", timeout=10)
    except Exception:
        pass
    time.sleep(3)
    wait_adb()
    time.sleep(2)
    install()   # /tmp survives, but be sure


def save(a, path):
    Image.fromarray(a).save(path)


def diff(a, b, y0=80, y1=800, x0=0, x1=472):
    return float(np.mean(np.any(a[y0:y1, x0:x1] != b[y0:y1, x0:x1], axis=2)))
