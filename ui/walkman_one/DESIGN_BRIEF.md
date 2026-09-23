# Design brief: the stock Walkman UI, rebuilt for Cinder, made accessible

**For:** a Claude Design session that has this folder but not the player.
**Goal:** screens that look like the stock Sony UI on an NW-A55 (the same grid, type, black
background and hairlines), carry Cinder's extra features, and are easier to reach and read than
stock.

## What is in this folder

| file | what it is |
|---|---|
| [`map.html`](map.html) | **Start here.** Every stock screen as a card: screenshots, how you reach it, what it opens. One self-contained file. |
| [`MAP.md`](MAP.md) | The same map as Markdown, with a flowchart of how the areas connect. |
| [`map.json`](map.json) | The same data as JSON: areas → screens → images, `reached_from`, `opens`, `states`. |
| [`screens.json`](screens.json) | The raw capture log the three files above are built from. |
| `screens/*.png` | The screenshots: real framebuffer captures at 480 × 800, 1×, taken by hand and checked one by one. |
| [`../../analysis/ui_assets/UI_DESIGN_SPEC.md`](../../analysis/ui_assets/UI_DESIGN_SPEC.md) | The measured design tokens (grid, type, colour, row heights), taken from Sony's own QML. |
| [`../../analysis/ui_assets/labels_en.json`](../../analysis/ui_assets/labels_en.json) | Sony's 729 English UI strings, for exact wording. |

The screenshots come from a player running Walkman One 3.02. Its UI is the stock A50 UI: the only
differences are 12 row heights, one recoloured logo and an icon tint. Treat the captures as the
stock look.

## The device

- **Screen:** 480 × 800 portrait on a 3.1" panel, about 300 px per inch. So **1 mm ≈ 12 px**. Design at 1×.
- **Input:** touch only for navigation. **There is no d-pad and no select/back key.** The hardware
  keys are Play/Pause, Previous, Next, Volume ± and Power, plus a Hold switch.
- **Drawing:** Cinder draws every pixel itself in Rust (no web view, no Qt) on a Cortex-A7 CPU.
  Flat fills, 1–2 px rules, text and PNG icons are cheap. Blur, drop shadows, gradients and
  layered translucency are not. The one exception is a flat dim behind a dialog or sheet.
- **Handoff format:** screens are rebuilt in code, not imported from images, so every element
  needs its **x, y, width, height**, colour token and type size, not just a picture.

## Keep: the stock look

These tokens come from Sony's QML and live captures. Full detail is in `UI_DESIGN_SPEC.md` §2–§5.

| token | value |
|---|---|
| Canvas | 480 × 800. Side gutter **20**, so the content is 440 wide |
| Vertical stack | status strip (0–80), screen title (80–150), **2 px hairline at y 152, `#9C9A9C`**, content, bottom bar (~730–800) |
| Bottom bar | four targets: **Back** (x ≈ 55), **Now Playing** (≈ 180), **Library** (≈ 300), **Option menu** (≈ 420) |
| Rows | 88 px (84 alt); item dividers are inset 20 px, section dividers run full width |
| Type | Sony SST: light and wide, never bold or italic. Sizes 16 / 26 / 28 / 32, plus one 150 px numeral |
| Colour | black background; text `#ffffff`, secondary `#cccccc` / `#999999`, raised surfaces `#282828` / `#202020`, rare accent `#c0a565` (muted gold) |
| Overlays | Option menus are small popups at the bottom right over a dimmed screen (see the Option menu cards); confirmations are centred dialogs with Cancel on the left and OK on the right |

Cinder can load the player's own SST fonts at runtime (it already does for non-Latin text). In a
mockup tool, a light, wide sans-serif is a fair stand-in.

### Stock features the redesign must still offer

- **Four Now Playing styles** (Option › Change Playback Screen): Standard (art), Spectrum Analyzer,
  Analog Level Meter, Digital Peak Meter. All four are in the map, captured while playing.
- **A customisable Library home:** Select Items to Display hides tiles, and tap-and-hold reorders them.
- **Equalizer *or* Tone Control** (bass / middle / treble): one replaces the other, switched from the
  sound panel's Option menu.
- **Three Saved Sound Settings slots**, and a lyrics overlay.
- **Every context menu** (the ⋯ on a row) offers Add to Bookmark List and Add to Playlist, both through a
  "Select List to Add to" picker.

## Fix: what the map shows is hard in stock

1. **Four screens are reachable only by a swipe on Now Playing.** Nothing on screen shows it; only a help
   overlay (Option › View Help) draws the map.
   Swipe right opens the Play Queue, left the Bookmark List, up the sound panel (five pages:
   Equalizer, DSEE HX, DC Phase Linearizer, Dynamic Normalizer, Vinyl Processor) and down the Library. Keep the swipes as shortcuts, but
   **give each a visible tap target.**
2. **Sound settings are split.** The swipe-up panel shows one effect per page, five pages deep,
   with small page dots as the only sign there are more. Its Option menu hides *Saved Sound
   Settings* and *Tone Control*, and output settings are in Settings. **Put every effect on one Sound screen**, as rows with
   the On/Off state visible inline and the detail one tap behind.
3. **"Direct" is easy to hit and hard to notice.** A small switch in the sound panel's title strip
   turns *every* sound setting off. The only feedback is a full-screen "Direct Source: On" page
   inside that panel. **Show Direct Source's state everywhere** (for example a status-strip chip)
   and put its switch where it cannot be hit by accident.
4. **One flat Settings list** mixes things changed daily with things changed once. **Surface the
   frequent ones** (Bluetooth, sleep timer, brightness, sound) and leave the rest in Settings.
5. **The Library home spends a whole screen on an icon grid** that the bottom bar partly repeats.
6. **Surprises:** the SensMe™ Channels tile starts playing at once (behind a "songs not analysed"
   notice), and the Library's DAC and phone buttons sit where a thumb lands, each one tap from a mode
   change. Make actions that change what plays, or switch modes, look different from navigation.

## Add: what Cinder has that stock doesn't

Place each one. None of them has a stock screen to copy, so match the stock look.

| feature | notes for the design |
|---|---|
| **Up Next queue** | Replaces stock's Play Queue. Add *Play next*, drag to reorder, remove, and a play history. Reachable by a tap from Now Playing. |
| **Shelf** | Cinder's bottom sheet: pin the current place to one of 3 slots, jump back later, undo. **Keep its behaviour and layout as they are.** The owner uses it daily, so a restyle needs their OK. |
| **Quick settings pull-down** | **Optional, off by default** (a Settings row turns it on). Drag down from the status strip for large toggles: brightness (5 levels), Bluetooth, BLE remote, night theme, and a sleep timer (off / 15 / 30 / 60). It is a separate sheet from the Shelf. |
| **Sound** | Sony's own effects, driven by Cinder: DSEE HX, VPT, DC Phase Linearizer, Vinyl Processor, 10-band EQ with Clear Bass, tone control, **Mono** (for single-sided hearing). One screen; see Fix 2. |
| **USB-DAC with LDAC out** | Use the player as a PC sound card *and* send the audio on to Bluetooth headphones at the same time. Stock blocks this with a dialog (in the map). Show the input format and which output is live. |
| **FM radio** | With a real signal meter. |
| **Lyrics** | `.lrc` files or embedded tags, shown on Now Playing; one tap to open. |
| **Library search, SensMe™ channels, liked songs, playlists made on the player** | Playlists are named with Cinder's on-screen keyboard. |
| **Scrobbler** | Writes `.scrobbler.log`. A Settings row with on/off and a count. |
| **Palettes, night mode, UI scale** | Night mode darkens the palette *and* dims the backlight. UI scale runs 80–140 %. |
| **Walkman One tunings** | When Cinder runs on Walkman One, W1's settings (sound signature and the rest) become Settings rows, not a text file edited over USB. |
| **Keylock** | The **Hold switch** locks: touch is ignored, the hardware keys still work, and only the Hold switch unlocks (never Power). Show the locked state clearly. |

## Screens this capture cannot show

Walkman One makes Sony's app believe the player is a WM1Z, and that app hides what a WM1Z lacks:
**FM radio, VPT, ClearAudio+, Language Study, noise cancelling and line-out**. So none of them are in
`map.html`. Cinder has FM and VPT, so design them in the same style. Their stock geometry is in the
carved QML under [`../../analysis/ui_assets/qml_src/`](../../analysis/ui_assets/qml_src/).

## Accessibility: requirements

| # | requirement | why, with numbers |
|---|---|---|
| 1 | **Every tap target is at least 80 × 80 px (≈ 7 mm); nothing is under 64 px.** Rows stay 88 px, with 8 px or more between neighbouring targets. | Phone guidelines use about 7 mm. Stock's title-strip switches and the ⋯ row buttons are smaller than that. |
| 2 | **Contrast:** readable text at least **4.5 : 1** against its background; text 24 px and larger, icons, switch states and dividers at least **3 : 1**. | On black, `#999999` is 7.4 : 1, `#cccccc` 13 : 1 and the gold 8.8 : 1, all fine. Stock's `#686868` (3.8 : 1) and `#646464` (3.5 : 1) are only fit for large text and disabled states. |
| 3 | **Text:** body 26 px, nothing readable under 20 px (stock's 16 px captions go). Layouts hold at **140 % UI scale**: long titles wrap to two lines or scroll, and never cut off a control. | Cinder already has a UI-scale setting. |
| 4 | **No swipe-only paths.** Every swipe has a visible tap equivalent. | See Fix 1. Swipes and drags are hard with limited dexterity. |
| 5 | **State is never shown by colour alone.** Switches carry On/Off text; the playing row carries an icon as well as a colour. | Stock already labels its switches "Off". Keep that everywhere. |
| 6 | **No time limits:** anything to be read stays until dismissed, or at least 5 s. | |
| 7 | **Every palette keeps these ratios**, night mode and any high-contrast palette included. | Palettes are user-loadable. The design sets the rules they are checked against. |
| 8 | **Hardware keys work on every screen, locked or not.** | Touch-free control is the only kind the device can offer. **There is no screen reader**, so size and contrast carry the rest. |
| 9 | **Primary actions sit in the lower two-thirds;** the title strip holds titles, not small controls. | Reachable one-handed, and nothing lands under a thumb by accident (see Fix 3). |

## What to deliver

1. **A token sheet:** colours (default dark, night, and one high-contrast palette), type sizes, spacing, row heights, target sizes.
2. **Screens at 480 × 800, 1×**, with every tap target outlined and measured:
   - Now Playing (with the lyrics and queue entry points), Library home, a song list, an album, Up Next, Search
   - Sound (flattened) and EQ detail
   - Settings root, one settings detail, Bluetooth, USB-DAC, FM, Quick settings
   - a confirm dialog, an Option popup, the locked state
3. **A navigation map in the same form as `MAP.md`:** for each screen, how it is reached by tap (swipes listed as shortcuts) and what it opens.
4. **A contrast and target-size check** per screen: a short table is enough.

## Out of scope

- Hardware Cinder does not have: no d-pad designs, and no new physical buttons.
- Changing the Shelf's behaviour.
- A light theme as the default: the stock look is dark. A light palette may exist as an option.
