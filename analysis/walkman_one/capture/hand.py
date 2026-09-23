"""Hand-driven UI capture: do one action, look at the result, save it with its link.

  hand.py do ACT [ACT ...]            perform actions, write look.png (half size) to view
  hand.py save ID "Title" AREA [SRC "how you get there"]
                                      save the screen now showing as screens/ID.png, record a link
  hand.py page ID                     save the screen now showing as the next page of ID (scrolled)
  hand.py state ID "what"             save the screen now showing as another state of ID
  hand.py link SRC "how" DST          record a link between two saved screens

ACT: tap:X,Y  swipe:left|right|up|down  scroll  top  back  np  lib  opt  wait:S
"""
import json, os, sys, time
import numpy as np
from PIL import Image
import dev2

UI = "/home/sony/cinder-sony-analysis/ui/walkman_one"
SHOTS = os.path.join(UI, "screens")
DB = os.path.join(UI, "screens.json")
SP = os.path.dirname(os.path.abspath(__file__))
os.makedirs(SHOTS, exist_ok=True)


def load():
    if os.path.exists(DB):
        return json.load(open(DB))
    return {"screens": {}, "order": [], "links": []}


def dump(db):
    json.dump(db, open(DB, "w"), indent=1, ensure_ascii=False)


def is_usb_screen(a):
    """The USB Mass Storage screen: its button's top and bottom edges are full white lines."""
    m = a.max(axis=2)
    return (m[666, 90:390] > 150).mean() > 0.9 and (m[727, 90:390] > 150).mean() > 0.9


def ensure_awake():
    """A wake re-enumerates USB and stock lands on the USB screen; Back returns to where it was."""
    if dev2.backlight() == 0:
        print("screen off -> one power press")
        dev2.wake()
        h, a = dev2.grab()
        if is_usb_screen(a):
            dev2.tap(55, 780, h)
            print("left the USB screen")


def grab():
    ensure_awake()
    return dev2.grab()


def act(a, h):
    k, _, arg = a.partition(":")
    if k == "tap":
        x, y = map(int, arg.split(","))
        return dev2.tap(x, y, h, quiet=500, timeout=1500)
    if k == "swipe":
        v = {"left": (420, 400, 60, 400), "right": (60, 400, 420, 400),
             "up": (240, 450, 240, 120), "down": (240, 120, 240, 450)}[arg]
        return dev2.swipe(*v, h, dur=250, hold=150)
    if k == "scroll":
        return dev2.swipe(240, 690, 240, 300, h, dur=350, hold=500)
    if k == "drag":                               # drag:X0,Y0,X1,Y1 — a scroll that starts where you say
        x0, y0, x1, y1 = map(int, arg.split(","))
        return dev2.swipe(x0, y0, x1, y1, h, dur=350, hold=500)
    if k == "top":
        return dev2.swipe(240, 250, 240, 740, h, dur=120, hold=0)
    if k == "back":
        return dev2.tap(55, 780, h)
    if k == "np":
        return dev2.tap(180, 780, h)
    if k == "lib":
        return dev2.tap(300, 780, h)
    if k == "opt":
        return dev2.tap(420, 780, h)
    if k == "wait":
        time.sleep(float(arg))
        return (False,) + dev2.grab()
    raise SystemExit(f"bad action {a}")


def look(a):
    Image.fromarray(a).resize((240, 400), Image.LANCZOS).save(os.path.join(SP, "look.png"))


def main():
    cmd, args = sys.argv[1], sys.argv[2:]
    db = load()
    if cmd == "do":
        h, a = grab()
        for x in args:
            try:
                ch, h, a2 = act(x, h)
            except dev2.ScreenOff:
                print(f"{x}: screen went off")
                ensure_awake()
                h, a2 = dev2.grab()
                ch = True
            if a2 is None:
                h, a2 = dev2.grab()
            a = a2
            print(f"{x}: {'changed' if ch else 'no change'}")
        look(a)
        return
    h, a = grab()
    if cmd == "save":
        sid, title, area = args[0], args[1], args[2]
        fn = f"{sid}.png"
        dev2.save(a, os.path.join(SHOTS, fn))
        s = db["screens"].setdefault(sid, {"title": title, "area": area, "images": [], "states": []})
        s.update(title=title, area=area)
        if fn not in s["images"]:
            s["images"].insert(0, fn)
        if sid not in db["order"]:
            db["order"].append(sid)
        if len(args) >= 5:
            db["links"].append({"src": args[3], "via": args[4], "dst": sid})
        print(f"saved {fn}")
    elif cmd == "page":
        sid = args[0]
        s = db["screens"][sid]
        fn = f"{sid}_p{len(s['images']) + 1}.png"
        dev2.save(a, os.path.join(SHOTS, fn))
        s["images"].append(fn)
        print(f"saved {fn}")
    elif cmd == "state":
        sid, what = args[0], args[1]
        s = db["screens"][sid]
        fn = f"{sid}__s{len(s['states']) + 1}.png"
        dev2.save(a, os.path.join(SHOTS, fn))
        s["states"].append({"image": fn, "what": what})
        print(f"saved {fn}")
    elif cmd == "link":
        db["links"].append({"src": args[0], "via": args[1], "dst": args[2]})
    else:
        raise SystemExit(__doc__)
    look(a)
    dump(db)


if __name__ == "__main__":
    main()
