"""screens.json + screens/*.png -> MAP.md, map.json and a self-contained map.html.

  build_map.py [UI_DIR]      (default /home/sony/cinder-sony-analysis/ui/walkman_one)
"""
import base64, html, io, json, os, re, sys, time
from collections import defaultdict
from PIL import Image

UI = sys.argv[1] if len(sys.argv) > 1 else "/home/sony/cinder-sony-analysis/ui/walkman_one"
db = json.load(open(os.path.join(UI, "screens.json")))
S, links = db["screens"], db["links"]
AREAS = ["Now Playing", "Sound panel", "Library", "Settings", "System"]
AREA_NOTE = {
    "Now Playing": "The start screen. Four more screens hang off it by swipes only.",
    "Sound panel": "Swipe up on Now Playing: five effect pages side by side, with the Direct switch in the title strip.",
    "Library": "Swipe down on Now Playing, or the Library button in the bottom bar.",
    "Settings": "First item of every Option (toolbox) menu.",
    "System": "Screens the player shows on its own.",
}
order = [k for k in db["order"] if k in S]
by_area = defaultdict(list)
for k in order:
    by_area[S[k]["area"]].append(k)
inbound, outbound = defaultdict(list), defaultdict(list)
for l in links:
    if l["src"] in S and l["dst"] in S:
        inbound[l["dst"]].append(l)
        outbound[l["src"]].append(l)
n_pages = sum(len(s["images"]) for s in S.values())
n_states = sum(len(s["states"]) for s in S.values())
today = time.strftime("%Y-%m-%d")

# ── map.json ─────────────────────────────────────────────────────────────────────────────────────
out = dict(
    device="Sony NW-A55 running Walkman One 3.02 — Sony's stock player UI (HgrmMediaPlayerApp)",
    canvas=dict(width=480, height=800, scale=1, input="touch, plus hardware Play/Prev/Next/Vol/Power and a Hold switch; no d-pad"),
    captured=today,
    method="Driven by hand over adb (injected touches, framebuffer reads); every capture checked by eye.",
    bottom_bar=[dict(x=55, target="Back"), dict(x=180, target="Now Playing"),
                dict(x=300, target="Library"), dict(x=420, target="Option menu (toolbox)")],
    areas=[],
)
for a in AREAS:
    scr = []
    for k in by_area.get(a, []):
        s = S[k]
        scr.append(dict(
            id=k, title=s["title"], note=s.get("note", ""),
            images=[f"screens/{f}" for f in s["images"]],
            states=[dict(what=x["what"], image=f"screens/{x['image']}") for x in s["states"]],
            reached_from=[dict(screen=l["src"], action=l["via"]) for l in inbound[k]],
            opens=[dict(screen=l["dst"], action=l["via"]) for l in outbound[k]],
        ))
    out["areas"].append(dict(area=a, note=AREA_NOTE[a], screens=scr))
json.dump(out, open(os.path.join(UI, "map.json"), "w"), indent=1, ensure_ascii=False)

# ── MAP.md ───────────────────────────────────────────────────────────────────────────────────────
def mid(k):
    return re.sub(r"[^A-Za-z0-9_]", "_", k)


md = [f"# Stock Walkman UI — screen map\n",
      f"Captured {today} on an NW-A55 running Walkman One 3.02, which is Sony's own player UI (Walkman "
      f"One changes only row heights, the power-off logo and an icon tint). **{len(order)} screens, "
      f"{n_pages} page images and {n_states} captures of other states**, every one a real 480 × 800 "
      "framebuffer grab.\n",
      "Each screen lists how you reach it and what it opens. [`map.json`](map.json) holds the same "
      "data; [`map.html`](map.html) is one self-contained page with every image embedded. The brief "
      "for redesigning it is [`DESIGN_BRIEF.md`](DESIGN_BRIEF.md).\n",
      "**Bottom bar, on almost every screen:** Back (x 55) · Now Playing (x 180) · Library (x 300) · "
      "Option menu (x 420).\n",
      "## How the screens connect\n", "```mermaid", "flowchart LR"]
for a in AREAS:
    md.append(f'  subgraph {mid(a)}["{a}"]')
    for k in by_area.get(a, []):
        md.append(f'    {mid(k)}["{S[k]["title"].replace(chr(34), chr(39))}"]')
    md.append("  end")
for l in links:
    if l["src"] in S and l["dst"] in S:
        v = l["via"].replace('"', "'")
        v = v if len(v) <= 34 else v[:32] + "…"
        md.append(f'  {mid(l["src"])} -- "{v}" --> {mid(l["dst"])}')
md.append("```\n")
for a in AREAS:
    md.append(f"## {a}\n\n{AREA_NOTE[a]}\n")
    for k in by_area.get(a, []):
        s = S[k]
        md.append(f'### {s["title"]} <a id="{k}"></a>\n')
        if s.get("note"):
            md.append(s["note"] + "\n")
        md.append(" ".join(f'<img src="screens/{f}" width="160" alt="{html.escape(s["title"])}">'
                           for f in s["images"]) + "\n")
        if inbound[k]:
            md.append("- **Reached from:** " + "; ".join(
                f"[{S[l['src']]['title']}](#{l['src']}) — {l['via']}" for l in inbound[k]))
        if outbound[k]:
            md.append("- **Opens:** " + "; ".join(
                f"{l['via']} → [{S[l['dst']]['title']}](#{l['dst']})" for l in outbound[k]))
        for x in s["states"]:
            md.append(f"- **Other state:** [{x['what']}](screens/{x['image']})")
        md.append("")
open(os.path.join(UI, "MAP.md"), "w").write("\n".join(md) + "\n")


# ── map.html ─────────────────────────────────────────────────────────────────────────────────────
def b64(fn, w=240):
    im = Image.open(os.path.join(UI, "screens", fn)).convert("RGB")
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


e = html.escape
H = ["""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Walkman UI Map</title>
<style>
:root{--bg:#f5f5f2;--fg:#1a1a1a;--muted:#555;--card:#fff;--line:#d6d6d2;--chip:#ebebe6;--accent:#7a5f14}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0e0e0e;--fg:#eee;--muted:#aaa;--card:#191919;--line:#333;--chip:#252525;--accent:#c9ad6b}}
:root[data-theme="dark"]{--bg:#0e0e0e;--fg:#eee;--muted:#aaa;--card:#191919;--line:#333;--chip:#252525;--accent:#c9ad6b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}
header,main{max-width:1280px;margin:0 auto;padding:16px}
h1{font-size:24px;margin:8px 0 4px}
h2{font-size:19px;margin:32px 0 4px;padding-bottom:6px;border-bottom:1px solid var(--line)}
.lede,.areanote{color:var(--muted);max-width:80ch;margin:4px 0 12px}
nav{position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:1;border-bottom:1px solid var(--line)}
nav a{display:inline-block;margin:3px 6px 3px 0;padding:4px 10px;background:var(--chip);border-radius:14px;color:var(--fg);text-decoration:none;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;scroll-margin-top:56px}
.card:target{outline:2px solid var(--accent)}
.card h3{font-size:15px;margin:0 0 6px}
.note{font-size:13px;color:var(--muted);margin:0 0 8px}
.shots{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px}
figure{margin:0;flex:none;width:140px}
figure img{width:140px;height:auto;display:block;border-radius:6px;border:1px solid var(--line)}
figcaption{font-size:11px;color:var(--muted);margin-top:3px}
ul{padding-left:18px;margin:8px 0 0}li{margin:2px 0;font-size:13px}
a{color:var(--accent)}
.k{font-weight:600}
</style></head><body><header>"""]
H.append(f"<h1>Walkman UI Map</h1><p class='lede'>{len(order)} screens of Sony's stock player UI, captured "
         f"{today} on an NW-A55 running Walkman One 3.02. Each card shows the screen, how to reach it and "
         "what it opens. Screens are 480×800 and driven by touch; the hardware keys are transport and power "
         "only. Bottom bar on almost every screen: Back · Now Playing · Library · Option menu.</p></header>")
H.append("<nav aria-label='Areas'><div style='max-width:1280px;margin:0 auto;padding:0 16px'>")
for a in AREAS:
    H.append(f'<a href="#area-{mid(a)}">{e(a)} ({len(by_area.get(a, []))})</a>')
H.append("</div></nav><main>")
for a in AREAS:
    H.append(f'<h2 id="area-{mid(a)}">{e(a)}</h2><p class="areanote">{e(AREA_NOTE[a])}</p><div class="grid">')
    for k in by_area.get(a, []):
        s = S[k]
        H.append(f'<section class="card" id="{k}"><h3>{e(s["title"])}</h3>')
        if s.get("note"):
            H.append(f'<p class="note">{e(s["note"])}</p>')
        H.append('<div class="shots">')
        for i, f in enumerate(s["images"]):
            cap = "" if len(s["images"]) == 1 else f"page {i + 1}"
            H.append(f'<figure><img loading="lazy" src="{b64(f)}" alt="{e(s["title"])} {cap}">'
                     f'{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>')
        for x in s["states"]:
            H.append(f'<figure><img loading="lazy" src="{b64(x["image"])}" alt="{e(s["title"])}: {e(x["what"])}">'
                     f'<figcaption>{e(x["what"])}</figcaption></figure>')
        H.append("</div><ul>")
        for l in inbound[k]:
            H.append(f'<li><span class="k">From</span> <a href="#{l["src"]}">{e(S[l["src"]]["title"])}</a>: {e(l["via"])}</li>')
        for l in outbound[k]:
            H.append(f'<li><span class="k">Opens</span> <a href="#{l["dst"]}">{e(S[l["dst"]]["title"])}</a>: {e(l["via"])}</li>')
        H.append("</ul></section>")
    H.append("</div>")
H.append("</main></body></html>")
open(os.path.join(UI, "map.html"), "w").write("".join(H))
print(f"{len(order)} screens, {n_pages} pages, {n_states} states, {len(links)} links -> MAP.md, map.json, map.html")
