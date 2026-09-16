# NW-A55, firmware 1.02, with Wampy and Cinder — device map

Collected 2026-09-16 over adb with Cinder's `tools/device_map/device_map.py` (read-only; scrubbed
and leak-checked — see the repository README). Start with [`SUMMARY.md`](SUMMARY.md).

The player was not stock when mapped, which matters for a few files:

* **Wampy** was installed: its init edits are in `init/`, and `LD_PRELOAD` lines appear on the
  SoundServiceFw and MediaStore/PlayerService processes in `processes/processes.txt`.
* **Cinder** was the Home app, and its mono library (`libcinder_mono.so`) sat in Wampy's preload
  slot on SoundServiceFw, so that process maps both libraries.
* Bluetooth was off and nothing was playing, so no A2DP stream socket was open.

| Folder | Contents |
|---|---|
| `system/` | `getprop`, `/proc` tables (cpuinfo, meminfo, interrupts, iomem, devices, partitions, mounts, modules, emmc, dumchar_info …), build and default properties |
| `kernel/` | `config.txt` (from `/proc/config.gz`), `dmesg.txt`, `sysctl.txt`, `lsmod.txt` |
| `storage/` | `df`, `/dev/block`, eMMC and SD attributes (no CID or serial) |
| `fs/` | recursive listings of the firmware trees (`/system`, `/sbin`, `/opt1..3` …); top-level names only for `/data`, `/var`, `/db`, `/cache` |
| `init/` | the init scripts as booted |
| `processes/` | `ps`, and per process: status, capabilities, `LD_*` variables, mapped files, descriptors |
| `ipc/` | `/proc/net/unix` and `netstat` with owning processes |
| `sysfs/` | class and bus maps; values from power_supply, switch, thermal, leds, backlight, graphics, rtc, android_usb, input, sound, misc, cpu, power, module parameters; I2C and SPI device names |
| `alsa/` | `/proc/asound`, `amixer -c0 contents`, `aplay -l/-L` |
| `input/` | `getevent -p`, `/proc/bus/input` |
