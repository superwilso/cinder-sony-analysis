# Cinder — Sony reference files

Files taken from Sony's NW-A50-series Walkman firmware while building
[Cinder](https://github.com/superwilso/Cinder), a replacement music player for that device:

- `analysis/ui_assets/` — the images, QML screens and English labels of Sony's music player
  (HgrmMediaPlayerApp), with an index and a gallery page over them.
- `analysis/F_appmgr_home/*.c`, `analysis/G_player_ipc/player.c` and
  `analysis/G_bt_nfc/decomp_BtCommonServiceClient.txt` — Ghidra decompilations of Sony libraries,
  made to learn how to talk to the firmware's services.

They moved here from Cinder's repository in September 2026. What was learned from them is written up
in Cinder's own documentation; Cinder does not need these files to build or run.

These files are Sony's. Cinder's MIT license does not cover them and no license is granted for them
here. They are kept for interoperability research.
