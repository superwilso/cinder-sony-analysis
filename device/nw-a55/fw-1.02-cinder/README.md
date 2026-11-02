# NW-A55, Sony stock firmware 1.02, with Cinder — device map

Collected 2026-11-02 over adb with Cinder's `tools/device_map/device_map.py` (read-only; scrubbed
and leak-checked — see the repository README). Start with [`SUMMARY.md`](SUMMARY.md).

Sony's own 1.02 firmware, without Wampy or Walkman One. Two things on it are Cinder's, and they show
in a few files:

* **Cinder's `preload` option** was installed: Cinder's small wrapper stands in front of Sony's
  `hagodaemon` (the real one is `hagodaemon.real`, which every Sony service process maps), and
  `libcinder_mono.so` is loaded into the two processes it serves. See `processes/processes.txt`.
* **Cinder** was the Home app, on the dev channel (so adb was on), and the player was on the USB
  cable to a computer while it was mapped: `player-map/` reads the USB supply as online.

Same folders as [`../fw-1.02-wampy-cinder/`](../fw-1.02-wampy-cinder/README.md), plus one:

| Folder | Contents |
|---|---|
| `player-map/fs/` | the value of every sysfs and procfs file Cinder's source reads, stored at its device path (`tools/map_player.sh --public`). Cinder's off-device harness boots on it: `CINDER_HARNESS_MAP=<this folder>/player-map cinder-home/harness/run.sh real-player`. Per-process `/proc` files are left out. |
