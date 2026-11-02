# Cinder — Sony reference files

Reference material for reverse-engineering Sony's NW-A50-series Walkman (NW-A55/A56/A57), gathered
while building [Cinder](https://github.com/superwilso/Cinder), a replacement music player for that
device. Most of it is meant to let you work on the firmware **without owning the player**, and
without downloading and unpacking the firmware yourself.

## What is here

| Folder | What it is | Answers questions like |
|---|---|---|
| [`device/nw-a55/`](device/nw-a55/) | Read-only maps of a running player, taken over adb — one per firmware: stock 1.02 with Cinder (`fw-1.02-cinder`, the newest, with `player-map/`), stock 1.02 with Wampy and Cinder, and Walkman One 3.02 | Which process hosts which Sony service? Which libraries does SoundServiceFw actually load? What is on the I2C buses? What does the ALSA mixer offer? What are the partitions, input devices, kernel config? |
| [`firmware/`](firmware/) | Catalogues of extracted firmware images: every file with size, mode and SHA-256, library dependencies, and every symbol Sony's binaries export (demangled) | Which library exports `SetEq6BandValue`? What does `libSoundServiceFw.so` link against? Is my extracted image the same as yours? |
| [`analysis/clear_bass/`](analysis/clear_bass/) | Clear Bass on the NW-A50 and NW-ZX100: decoded coefficient tables and Ghidra decompilations | How does Sony's Clear Bass filter work, and where is it in the A50's firmware? |
| `analysis/ui_assets/` | Images, QML screens and English labels of Sony's own player (HgrmMediaPlayerApp), with an index, a gallery and a design spec | What does the stock UI show, what are its strings called, and what are its real grid, type and colour values? |
| [`analysis/walkman_one/`](analysis/walkman_one/) | Walkman One as it exists on a running player: its settings file, its boot log, and its complete UI delta against stock | What does Walkman One actually change? What is its feature list? |
| `analysis/F_appmgr_home/`, `analysis/G_player_ipc/`, `analysis/G_bt_nfc/` | Ghidra decompilations of Sony service clients | How does a client talk to the app manager, the player service, the Bluetooth service? |

The write-ups that explain these files live in Cinder's repository, under `analysis/RE_*.md` and
`docs/` — for example `analysis/RE_clear_bass.md` for the Clear Bass folder.

## Working without a device

* **Start with `device/nw-a55/<firmware>/SUMMARY.md`.** It lists every Sony service process with
  the libraries it mapped and the sockets it holds, the partitions, mounts, ALSA PCMs, input
  devices, I2C chips and kernel modules. The raw files beside it are what the summary was built from.
* **To find a function, grep `firmware/nw-a50/1.02/system/symbols/`.** One file per Sony binary,
  demangled. `prototypes.txt` holds the C++ prototypes Sony's libraries keep as strings, which often
  carry parameter names the symbols lack.
* **To check an image you extracted yourself**, compare against `manifest.tsv` (SHA-256 per file).
* **Kernel questions:** `device/…/kernel/config.txt` is the running kernel's own configuration
  (`/proc/config.gz`), and `kernel/dmesg.txt` is a boot log.
* **The init system as it actually boots:** `device/…/init/`. On the mapped player that includes
  Wampy's edits; the stock ramdisk is catalogued in `firmware/nw-a50/1.02/ramdisk/`.

## How the device map was made, and what it leaves out

Cinder's `tools/device_map/device_map.py` pushes a collector (`collect.sh`) to the player's RAM disk,
runs it, pulls the result and deletes it again. The collector only reads. It does not touch
`/proc/regmon`, `/dev/mem`, debugfs contents, the backlight PWM node or `wakeup_count`, because on
this player those can hang, reprogram hardware or panic the kernel.

Because the map is published, it is scrubbed before it is written:

* **Not collected:** the owner's music and playlists (`/contents`, `/data`, `/db` contents), logcat
  (track titles, device names), Bluetooth pairing data, the USB serial.
* **Replaced:** the serial number, every MAC address (including the Bluetooth address in any
  spelling), serial-like properties, and paths of the owner's files in open descriptors.
* **Checked:** a leak check searches every output file for the raw identifiers and for the names in
  the player's paired-device list, and refuses to write the map if any survived.

If you map your own player, run the same tool and read `SUMMARY.md` before publishing it anyway: a
scrubber only removes what it was told about.

Newer maps also have `player-map/fs/`: the value of every sysfs and procfs file Cinder's source
reads, stored at its device path. Cinder's off-device harness boots on it
(`CINDER_HARNESS_MAP=<map>/player-map cinder-home/harness/run.sh real-player`) and lists every path
Cinder opened that the player does not have.

## Map your own player — NW-A40, NW-A30 and others

Cinder runs on the NW-A50 series. A map of another model on the same platform (NW-A45, NW-A35,
ZX300, WM1A/Z) is the first step towards running it there: it shows what that player's kernel and
Sony services really are, and where they differ from the A55.

You need a player with **adb** (Walkman One turns it on at boot; stock firmware on these models
usually does not), a computer with `adb`, Python 3 and bash (on Windows, use WSL), and a copy of
[Cinder](https://github.com/superwilso/Cinder). Then, with the player connected:

```sh
cd Cinder
python3 tools/device_map/device_map.py
```

It takes about fifteen minutes and writes `device-map-<model>-<firmware>/` in the current folder.
It only reads: nothing on the player changes, and its temporary files (in the player's RAM disk) are removed afterwards.
Read `SUMMARY.md` in that folder, then zip the folder and attach it to an issue on Cinder, or open a
pull request here adding it as `device/<model>/<firmware>/`.

## How the firmware catalogues were made

Cinder's `tools/firmware_catalogue.py`, run on root filesystems extracted with Rockbox's `upgtool`
from Sony's own updaters (`NW-A50_V1_02.exe`, `NW-ZX100_V1_11.exe`). They contain no firmware
binaries: only names, sizes, modes, hashes, ELF metadata, exported symbols, prototypes, and the
plain-text init scripts and property files. Firmware-wide key and certificate files appear by name
and hash only, never by content.

To add a model, unpack its updater and run:

```sh
python3 tools/firmware_catalogue.py <extracted-rootfs> firmware/<model>/<version>/<part> --label "<model> <version>"
```

## Whose files these are

The UI assets and the decompilations are derived from Sony's firmware, and the catalogues and maps
describe it. Cinder's licence (PolyForm Noncommercial 1.0.0) does not cover Sony's material, and
no licence is granted for it here. Everything is kept for interoperability research.
