# Walkman One, as it exists on a running player

Read off an NW-A55 with **Walkman One** installed, 2026-09-21. Read-only adb; nothing on the player
was written. The write-up that explains these files is Cinder's
`analysis/RE_walkmanone_extract.md`.

Walkman One is MrWalkman's modified stock firmware for the NW-A50 series. Files here are his or
Sony's, kept for reference so the mechanism can be studied without installing it.

| file | what it is |
|---|---|
| `settings.txt` | The mod's own settings file, as generated on the player. **This is the complete feature list** — eight keys, documented in place by its own comments |
| `boot_log_excerpt.txt` | The settings processor's log for the first boots after installation: what it read, what it applied, and how the external tuning was installed |
| `ui_delta/qml_stock_vs_w1.diff` | Every QML difference between the stock player binary and Walkman One's. Twelve blobs, and every difference is a size |
| `ui_delta/poweroff_*.png` | The one embedded image out of 796 that Walkman One changes |
| `ui_capture.sh` | The adb helper used to drive and capture the UI (tap / swipe / key / framebuffer grab) |

The named NVP zone map from the same player is at
[`../../device/nw-a55/fw-3.02-walkmanone/nvp/zone_map.txt`](../../device/nw-a55/fw-3.02-walkmanone/nvp/zone_map.txt),
and a full read-only map of that firmware running is the rest of
[`fw-3.02-walkmanone/`](../../device/nw-a55/fw-3.02-walkmanone/).

## The short version

* **The model swap is a flashed NVP image.** `/etc/.mod/conf_{a,b,c}` are 15,728,640-byte images of
  `mmcblk0p22` (`/emmc@nvp`); `/opt2/stock/conf_bk` and `nv_bk` are the player's originals.
* **All three carry the same KAS** — `e8d171a5…` (`nw-wm1a`) — so the update key does not depend on
  which sound signature is chosen.
* **`kas` and `fpi` are rewritten to different models.** `kas` = nw-wm1a (what the updater decrypts
  with), `fpi` = `NW-WM1Z` (what Sony's own packages check against). Setting `fpi` is what lets a
  WM1Z-targeted package install on an A55.
* **The UI is Sony's, tightened.** Same binary size, one recoloured logo, twelve metric tweaks.
* **The external tuning packages still cannot be opened host-side**, with the player's own key or
  any other. What is new is that their installed *result* sits on the player.
