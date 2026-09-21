# Live framebuffer captures — NW-A55 running Walkman One

Grabbed 2026-09-21 straight off `/dev/graphics/fb0` (480×800, BGRA) with
[`../../walkman_one/ui_capture.sh`](../../walkman_one/ui_capture.sh). No emulator, no mockup — this
is what the panel was showing.

| file | screen |
|---|---|
| `usb_msc_active.png` | USB Mass Storage, active — the state the player parks in with a cable attached |
| `usb_connected.png` | USB Mass Storage off, "you can operate this player while charging" |
| `creating_database.png` | The library rescan that follows turning MSC off. Note the status strip: **`FLAC 44.1 kHz / 16 bit`** — the `sound_quality_info` block, which is Sony's, not Walkman One's |

**Why there are only three.** With the cable connected the player parks on the USB screen and that
screen is modal: the four bottom icons are a legend rather than targets, there is no back gesture
out of it, and MSC re-arms itself after an idle. Capturing the rest of the UI means a detached
on-device capture loop with the cable out, collected afterwards.

For geometry, type, colour and the component inventory, use
[`../UI_DESIGN_SPEC.md`](../UI_DESIGN_SPEC.md) — it is built from the carved QML, which carries the
real numbers, rather than from measuring these images.
