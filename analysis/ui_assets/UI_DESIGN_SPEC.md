# The stock Walkman UI, as a design spec

**Audience: whoever is designing Cinder's Walkman-One-parity skin** — including a Claude design
session that has this repository but not the player.

This describes the UI that ships on the NW-A50 series (`HgrmMediaPlayerApp`, Sony's Qt/QML player)
and, because Walkman One changes almost nothing about it, the Walkman One UI as well. It is written
from three sources, all in this repository:

| source | what it gives | where |
|---|---|---|
| Carved PNG assets (796) | every icon and full-screen image, at native size | [`hgrm_player/`](hgrm_player/) |
| Carved QML (180 screens) | real geometry — heights, margins, anchors — and the screen inventory | [`qml_src/`](qml_src/), indexed in [`QML_INDEX.md`](QML_INDEX.md) |
| Live framebuffer captures | what it actually looks like composited | [`screens_w1/`](screens_w1/) |

English UI strings are in [`labels_en.json`](labels_en.json). The Walkman One delta is in
[`../walkman_one/ui_delta/`](../walkman_one/ui_delta/).

---

## 1. Canvas

| | |
|---|---|
| Panel | 480 × 800, portrait, 32bpp |
| Framebuffer | `/dev/graphics/fb0`, **BGRA**, 1,536,000 bytes visible (`virtual_size` says 480×2400 — three buffers) |
| Touch | `himax-hx8526-icx`, raw range **960 × 1600** — exactly 2× the screen |
| Input | **No d-pad.** Touch, plus hardware Play/FF/REW/Vol±/Power and the Hold switch |

Everything is designed for a thumb on a 3.1" screen, so hit targets are generous relative to the
pixel count. Treat 480 × 800 as the design canvas at 1×.

## 2. Grid

| token | value | evidence |
|---|---|---|
| Screen width | 480 | 39 QML `width: 480` |
| Content width | 440 | 13 QML `width: 440` |
| **Side gutter** | **20** | (480 − 440) / 2; title text measured starting at x = 22 |
| Title-bar rule | 2 px hairline at **y = 152**, `#9C9A9C` | measured off a live capture |
| Bottom bar | icons span x 43…439, baseline around y = 778 | measured |

So the vertical stack is: status strip → screen title → **hairline** → scrolling content → bottom
bar. The hairline under the title is the single strongest visual signature of this UI.

## 3. Type

Sony's own **SST** family (`family: "SST_Fixed"` and a `viewstyle` singleton that the carve did not
reach; the device's font chain is documented in Cinder's `analysis/RE_sony_fonts.md`).

Sizes that appear literally in the QML: **16, 26, 28, 32**, and **150** for the one giant numeral.
Read those as: caption 16, body 26, row/title 28, emphasis 32.

Weight is light-to-regular and letterforms are wide. Nothing is bold. Nothing is italic.

## 4. Colour

Near-monochrome on black. The full set of literal colours across 180 screens:

| role | value |
|---|---|
| Background | `black` / `#000000` |
| Primary text, icons | `#ffffff` |
| Secondary text | `#cccccc`, `#999999` |
| Disabled / tertiary | `#686868`, `#646464` |
| Rules, dividers | `#9C9A9C` (measured), `#333333` |
| Raised surfaces | `#282828`, `#202020` |
| Accent (rare) | `#c0a565` — a muted gold |
| Alert | `red` / `#ff0000` |
| Brand | Walkman orange, in the logo art only |

There is **no colour-coded navigation**. Colour carries state (on/off, selected, disabled) and
almost nothing else. Walkman One adds one runtime tint for Home-screen icons — `COL` in its
settings file: `#DDDDDD` (default), `#FFD2B0`, `#FF6757`, `#B1CFE5`, `#AED1B3`.

## 5. Components and their real heights

Taken from the QML, so these are the numbers the stock app actually lays out with.

| component | stock height | Walkman One |
|---|---|---|
| List row (primary) | **88** | 78 |
| List row (alt) | **84** | 89 |
| Compact row | 72 | 40 |
| Settings row | 56 | 40 |
| Section label | 28 | 12 / 20 |
| Status-bar block | 80 | 70 |
| Menu bottom spacing | 106 | 90 |
| Small inline glyph | 22 × 18 | 15 × 12 |

Other recurring sizes: 120 (headers), 62, 50, 46, 40, 36, 32, 26, 20, 18, 6 (rules and spacers);
240 (half-screen art); 361 × 88/90 (the wide button/banner art in `hgrm_player/`).

**Walkman One is the same layout, tightened.** Its only structural change is making rows and the
status block shorter so more fits on screen.

## 6. Screen inventory

[`QML_INDEX.md`](QML_INDEX.md) lists all 180 carved screens sorted by how much English text they
carry, which is a good proxy for how much of the product they are. The ones that matter for a
parity skin:

* **Home** — the icon grid (this is what `COL` tints)
* **Library** browsers — Album / Artist / Genre / Folder / Playlist / Year, all the same row list
* **Now Playing** — art, transport, progress rail, the `sound_quality_info` block (codec, rate,
  bit depth) that sits in the status area
* **Sound Settings** — the big one: equaliser (six-band, incl. Clear Bass), DSEE HX, DC Phase
  Linearizer, Dynamic Normalizer, Vinyl Processor, VPT, tone control
* **Bluetooth / audio device connection**, including wireless playback quality
* **USB Mass Storage / USB Connection Settings**
* **Clock Settings**, **Language Study Settings**, **Ambient Sound Mode**, **High Gain Output**
* **Reset / Format** (`allSettingIint`)
* **Initial setup wizard**

## 7. Walkman One's complete visual delta

Measured 2026-09-21 by carving both player binaries — they are **the same 9,055,736 bytes**, an
in-place patch rather than a rebuild.

* **796 PNGs each; 741 share an md5; exactly one differs** — the 480×800 Power Off screen, whose
  WALKMAN logo is white in stock and orange in Walkman One. Both are in
  [`../walkman_one/ui_delta/`](../walkman_one/ui_delta/).
* **239 QML blobs each; 12 differ, and every difference is a size.** Full diff:
  [`qml_stock_vs_w1.diff`](../walkman_one/ui_delta/qml_stock_vs_w1.diff).
* One runtime icon tint (`COL`).

Nothing else. No added screen, no removed screen, no new icon, no font change, no colour change
outside the logo and the tint.

**The practical consequence:** a skin that reproduces the stock A50 look reproduces the Walkman One
look. There is no separate "Walkman One design" to chase.

## 8. What this UI is bad at — the brief for "tweaks"

Worth stating plainly, because it is the reason to redesign anything at all rather than clone:

1. **Sound Settings is deep.** Reaching the equaliser is several taps down a tree, and the effects
   that people actually toggle (DSEE HX, DC Phase, Clear Bass) each sit on their own leaf screen.
2. **No queue, no shelf.** Absent from the product, not just hidden.
3. **The Home icon grid spends a whole screen on navigation** that the bottom bar largely repeats.
4. **Settings that are changed often and settings that are changed once share one flat list**, with
   no favourites, no recents and no search.

A parity skin should keep §2–§5 exactly — the grid, the type, the near-monochrome palette, the
hairline under the title — and spend its freedom on §8. That is the "same UI, easier to reach"
brief.

## 9. Reproducing the captures

The screen map in [`../../ui/walkman_one/`](../../ui/walkman_one/) (`map.html`, `MAP.md`,
`map.json`) was captured by hand, **with the cable in**, using the tools in
[`../walkman_one/capture/`](../walkman_one/capture/): `hand.py do …` performs one action and writes
a preview, `hand.py save|page|state|link …` records what is on screen, and `build_map.py` turns
`screens.json` into the three map files. An automatic crawler was tried first and dropped: it could
not tell a popup from the screen under it reliably, and it flipped switches it should not have. The
older [`../walkman_one/ui_capture.sh`](../walkman_one/ui_capture.sh) still works for single shots.

Things that cost an hour if you rediscover them:

* **Touch is protocol A.** A contact is `ABS_MT_TOUCH_MAJOR`, `ABS_MT_WIDTH_MAJOR`,
  `ABS_MT_POSITION_X`, `ABS_MT_POSITION_Y`, then `SYN_MT_REPORT`, then `SYN_REPORT`, at **2×**
  screen coordinates on `/dev/input/event1`. A tap built from `ABS_MT_POSITION_*` + `BTN_TOUCH`
  alone is accepted by the kernel and **ignored by the app**.
* **The USB screen is not a dead end.** With the cable in, the player parks on "USB Mass Storage".
  Tapping the bottom-bar Back arrow at (55, 780) leaves it, and the rest of the UI works over adb.
* **fb0 is triple-buffered.** Read the live buffer from `/sys/class/graphics/fb0/pan`, or a capture
  is sometimes one frame stale.
* **Injected taps work but never count as user activity.** The panel dims (backlight 25 → 2) and
  then goes off on its own timer. A dim panel still takes taps normally; do not send a "wake" tap
  first, because there is no spot that is safe on every screen (one hit the Equalizer panel's Direct
  switch, another the Library's USB-DAC button). When the panel is off, one short press of Power
  (`event0`, code 116) wakes it. **Power toggles:** a second press while the first wake is under
  way puts the player to sleep, adb drops, and only a human can press it back.
* **Now Playing hides four screens behind swipes:** right opens the Play Queue, left the Bookmark
  List, up the five-page sound panel and down the Library.
