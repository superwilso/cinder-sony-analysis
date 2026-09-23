# Hand-driven UI capture

The tools that made [`../../../ui/walkman_one/`](../../../ui/walkman_one/). Stock player, cable in,
adb up. Gotchas are in [`../../ui_assets/UI_DESIGN_SPEC.md`](../../ui_assets/UI_DESIGN_SPEC.md) §9.

| file | what it does |
|---|---|
| `fbtool.c` | On-device helper: framebuffer grab (live pan offset), protocol-A taps and swipes on `event1`. Build: `arm-linux-musleabihf-gcc -O2 -static -Wall -Wextra -o fbtool fbtool.c`, push to `/tmp/fbtool`. |
| `dev2.py` | Host side of `fbtool`: `grab()`, `tap()`, `swipe()`, `backlight()`, and a guarded `wake()` (one Power press, never two within 15 s). |
| `hand.py` | One step at a time: `do ACT…` acts and writes `look.png`; `save`, `page`, `state`, `link` record what is on screen into `screens.json`. |
| `build_map.py` | `screens.json` + `screens/*.png` → `MAP.md`, `map.json`, `map.html`. |

```
python hand.py do np swipe:right            # look.png shows the result
python hand.py save play_queue "Play Queue" "Now Playing" now_playing "swipe right"
python hand.py do scroll && python hand.py page play_queue
python build_map.py
```

`hand.py do` actions: `tap:X,Y`, `swipe:left|right|up|down`, `scroll`, `drag:X0,Y0,X1,Y1`, `top`,
`back`, `np`, `lib`, `opt`, `wait:S`. Redact MAC addresses before committing a capture.
