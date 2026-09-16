# Clear Bass — NW-A50 and NW-ZX100

The write-up is Cinder's `analysis/RE_clear_bass.md`. In short: Clear Bass is band 0 of Sony's
six-band EQ, and the whole implementation ships in the NW-A50's `libSoundServiceFw.so` as
`CB_6bandEQ_*`. On the NW-ZX100 the same EQ runs on a Renesas SPXK7 DSP.

## `nw-a50/`

| File | What |
|---|---|
| `CB_6bandEQ_iir_coef.csv` | bands 1–5 (400 Hz … 16 kHz): 6 sample rates × 5 bands × 21 levels (−10..+10 dB). Biquad `[b0, b1, b2, a1, a2]` with b1 = 0, b2 = −b0 and the feedback terms stored for `y = b0·x + b1·x1 + b2·x2 + a1·y1 + a2·y2`. Each band is added to the dry signal. |
| `CB_6bandEQ_geq_coef.csv` | band 0, Clear Bass: 6 sample rates × 2 stages × 21 levels, `(g, c1, c2)`. The NEON routine doubles all three: `y = 2g·(x − x2) + 2c1·y1 + 2c2·y2`, added to the signal, stage 2 applied to stage 1's result. |
| `CB_6bandEQ_chsep_coef.txt` | the 64-entry channel-separation table |
| `decomp_CB_6bandEQ.txt` | Ghidra: the effect entry points, `CB_6bandEQ_core`, `CB_6bandEQ_eq`, the limiter |
| `decomp_UpdateProcCond_ConvPresetToGains.txt` | Ghidra: when each chain filter processes, and preset → gains |

Sample-rate order: 44.1, 48, 88.2, 96, 176.4, 192 kHz. Level rows run +10 → −10; level 0 is all zeros.

## `nw-zx100/`

| File | What |
|---|---|
| `decomp_SpiderApp_eq_trace.txt` | Ghidra: every function that references the EQ/ALC/DSP log strings in `SpiderApp`, with callers |
| `decomp_SpiderApp_alc.txt` | Ghidra: the volume-step ALC and Clear Bass threshold path, including the `ct_cb` derivation |
| `decomp_cxd3774gf_tone.txt` | Ghidra (with DWARF types): the CXD3774GF codec driver's tone-control and ALC table handling |
