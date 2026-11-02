#!/usr/bin/env python3
"""
vincent-studio-poster renderer
把一份海报 JSON 规格渲染成 3:4 / 9:16 / 1:1 / 16:9 四种规格的 PNG（及可编辑 HTML）。

只依赖 Python 3.8+ 标准库 + 本机 Chrome / Chromium / Edge（无头截图）。

用法：
  python3 render_poster.py spec.json                     # 渲染 spec 中 ratios 指定的规格
  python3 render_poster.py spec.json --ratios 3:4,1:1    # 覆盖规格
  python3 render_poster.py spec.json --style aura        # 覆盖风格
  python3 render_poster.py spec.json --sheet             # 额外输出四规格总览图
  python3 render_poster.py spec.json --html-only         # 只生成 HTML（无 Chrome 时）
  python3 render_poster.py --list-styles
  python3 render_poster.py --doctor                      # 检查 Chrome 与中文字体
"""
import argparse
import html
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.request import pathname2url

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

RATIOS = {
    "3:4": {"size": (1242, 1656), "cls": "ra-portrait", "slug": "3x4"},
    "9:16": {"size": (1080, 1920), "cls": "ra-tall", "slug": "9x16"},
    "1:1": {"size": (1080, 1080), "cls": "ra-square", "slug": "1x1"},
    "16:9": {"size": (1920, 1080), "cls": "ra-wide", "slug": "16x9"},
}

STYLES = {
    "linen": "晨光亚麻·自然疗愈（瑜伽/冥想/阴瑜伽/工作坊）",
    "quiet": "静奢极简·Quiet Luxury（普拉提/高端私教/会员制）",
    "power": "能量大字报（健身房/特训营/限时促销/双11）",
    "pop": "多巴胺派对（店庆/团课/开业/儿童亲子/夏日活动）",
    "aura": "疗愈光晕（心身灵/音乐疗愈/颂钵/冥想之夜/满月）",
    "festive": "东方节庆（春节/元旦/中秋/国庆/端午；variant: red|moon|jade）",
    "clinic": "专业康复（运动康复/体态评估/产后修复/理疗）",
    "editorial": "杂志周年刊（店庆/周年庆/品牌升级/年度回顾）",
}
VARIANTS = {"festive": ["red", "moon", "jade"], "pop": ["sunny", "berry", "mint"], "aura": ["night", "dawn"]}

CHROME_CANDIDATES = [
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "microsoft-edge", "msedge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

FIT_JS = r"""
(function(){
  var P=document.querySelector('.poster');
  function over(el){return el.scrollHeight>el.clientHeight+2||el.scrollWidth>el.clientWidth+2;}
  function fitTitle(){
    var t=P.querySelector('.title'); if(!t) return;
    var v=getComputedStyle(t).writingMode.indexOf('vertical')===0;
    var o=function(){return v?t.scrollHeight>t.clientHeight+2:t.scrollWidth>t.clientWidth+2;};
    var tk=1; t.style.setProperty('--tk',tk);
    while(o()&&tk>0.4){tk-=0.025;t.style.setProperty('--tk',tk);}
  }
  function overflow(){
    var cs=getComputedStyle(P);
    function sum(list,gap,a,b){var t=list.split(' ').map(parseFloat).filter(function(x){return !isNaN(x);});
      return t.reduce(function(x,y){return x+y;},0)+(parseFloat(gap)||0)*Math.max(0,t.length-1)+parseFloat(a)+parseFloat(b);}
    if(sum(cs.gridTemplateRows,cs.rowGap,cs.paddingTop,cs.paddingBottom)>P.clientHeight+2) return true;
    if(sum(cs.gridTemplateColumns,cs.columnGap,cs.paddingLeft,cs.paddingRight)>P.clientWidth+2) return true;
    var kids=P.children;
    for(var i=0;i<kids.length;i++){
      var el=kids[i], c=el.classList;
      if(c.contains('deco')||c.contains('photo')||c.contains('headline')) continue;
      if(el.scrollWidth>el.clientWidth+Math.max(6,el.clientWidth*0.02)) return true;
    }
    return false;
  }
  function run(){
    var k=1;
    for(var i=0;i<60;i++){P.style.setProperty('--k',k); fitTitle(); if(!overflow()) break; k-=0.02; if(k<0.5) break;}
    document.body.setAttribute('data-fit',k.toFixed(2));
    if(k<0.75) console.warn('POSTER_DENSE '+k.toFixed(2));
  }
  run();
  window.addEventListener('load',run);
})();
"""


def die(msg):
    print("✗ " + msg, file=sys.stderr)
    sys.exit(1)


def esc(s):
    return html.escape(str(s), quote=True)


def rich(s):
    """Escape text; **x** -> <em>x</em>; newline -> <br>."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<em>\1</em>", s)
    return s.replace("\n", "<br>")


def resolve_src(value, base_dir):
    if not value:
        return None
    v = str(value)
    if re.match(r"^(https?:|data:|file:)", v):
        return v
    p = Path(os.path.expanduser(v))
    if not p.is_absolute():
        p = (base_dir / p).resolve()
    if not p.exists():
        print(f"⚠ 找不到素材文件：{p}（已忽略）", file=sys.stderr)
        return None
    return "file:" + pathname2url(str(p))


def build_html(spec, ratio, base_dir):
    r = RATIOS[ratio]
    w, h = r["size"]
    unit = min(w, h) / 100.0
    style = spec.get("style", "linen")
    if style not in STYLES:
        die(f"未知风格 {style}，可选：{', '.join(STYLES)}")
    variant = spec.get("variant") or (VARIANTS.get(style, [None])[0])

    # per-ratio overrides: {"by_ratio": {"1:1": {"subtitle": null}}}
    data = dict(spec)
    for k, v in (spec.get("by_ratio", {}).get(ratio, {}) or {}).items():
        data[k] = v

    brand = data.get("brand") or {}
    points = [p for p in (data.get("points") or []) if p][:4]
    offers = [o for o in (data.get("offers") or []) if o][:3]
    hero = data.get("hero") or None
    photo = resolve_src(data.get("photo"), base_dir)
    logo = resolve_src(brand.get("logo"), base_dir)
    qr = resolve_src(data.get("qr"), base_dir)

    classes = ["poster", f"st-{style}", r["cls"], "has-photo" if photo else "no-photo"]
    if variant:
        classes.append(f"v-{variant}")
    for key, present in (("points", points), ("offers", offers), ("hero", hero), ("qr", qr)):
        classes.append(f"{'has' if present else 'no'}-{key}")

    parts = []
    ticker = data.get("ticker") or " · ".join(x for x in [brand.get("name_en"), data.get("eyebrow")] if x) or brand.get("name", "")
    ticker_html = esc((ticker + "   ✦   ") * 12)
    parts.append(f'<div class="deco"><i class="d1"><span>{ticker_html}</span></i><i class="d2"></i><i class="d3"></i><i class="d4"></i><i class="d5"></i></div>')

    # brand
    if brand.get("name") or logo:
        b = '<header class="brand">'
        if logo:
            b += f'<img class="logo" src="{logo}" alt="logo">'
        if brand.get("name") or brand.get("name_en"):
            b += '<div class="bname">'
            if brand.get("name"):
                b += f'<b>{esc(brand["name"])}</b>'
            if brand.get("name_en"):
                b += f'<small>{esc(brand["name_en"])}</small>'
            b += "</div>"
        if brand.get("tagline"):
            b += f'<span class="btag">{rich(brand["tagline"])}</span>'
        b += "</header>"
        parts.append(b)

    # headline
    title = str(data.get("title", "")).replace("|", "\n")
    lines = "".join(f'<span class="l">{rich(l)}</span>' for l in title.split("\n") if l.strip())
    hd = '<div class="headline">'
    if data.get("eyebrow"):
        hd += f'<p class="eyebrow">{rich(data["eyebrow"])}</p>'
    hd += f'<h1 class="title">{lines}</h1>'
    if data.get("subtitle"):
        hd += f'<p class="subtitle">{rich(data["subtitle"])}</p>'
    hd += "</div>"
    parts.append(hd)

    if hero:
        hh = '<div class="hero">'
        hh += f'<span class="hv">{esc(hero.get("value", ""))}</span>'
        if hero.get("unit"):
            hh += f'<span class="hu">{esc(hero["unit"])}</span>'
        if hero.get("label"):
            hh += f'<span class="hl">{rich(hero["label"])}</span>'
        hh += "</div>"
        parts.append(hh)

    if points:
        items = "".join(f'<li><i>{i:02d}</i><span>{rich(p)}</span></li>' for i, p in enumerate(points, 1))
        parts.append(f'<ul class="points" style="--n:{len(points)}">{items}</ul>')

    if offers:
        cards = ""
        for o in offers:
            c = '<div class="offer">'
            if o.get("tag"):
                c += f'<span class="otag">{esc(o["tag"])}</span>'
            if o.get("name"):
                c += f'<p class="on">{rich(o["name"])}</p>'
            if o.get("price") not in (None, ""):
                price = str(o["price"])
                cur = o.get("currency", "¥")
                if re.match(r"^[\d.,]+$", price):
                    c += f'<p class="op"><small>{esc(cur)}</small>{esc(price)}</p>'
                else:
                    c += f'<p class="op">{esc(price)}</p>'
            if o.get("original"):
                c += f'<p class="oo">{esc(o["original"])}</p>'
            if o.get("note"):
                c += f'<p class="onote">{rich(o["note"])}</p>'
            c += "</div>"
            cards += c
        parts.append(f'<div class="offers" style="--n:{len(offers)}">{cards}</div>')

    focus = esc(data.get("photo_focus", "50% 30%"))
    if photo:
        parts.append(f'<figure class="photo" style="--focus:{focus}"><div class="frame"><img src="{photo}" alt=""></div></figure>')
    else:
        parts.append('<figure class="photo ph"><div class="frame"></div></figure>')

    info = '<footer class="info"><div class="meta">'
    for key in ("date", "location", "contact"):
        if data.get(key):
            info += f'<p class="{key}">{rich(data[key])}</p>'
    info += "</div>"
    if data.get("cta"):
        info += f'<span class="cta">{rich(data["cta"])}</span>'
    if qr:
        info += f'<div class="qr"><img src="{qr}" alt="QR"><small>{esc(data.get("qr_label", "扫码预约"))}</small></div>'
    info += "</footer>"
    parts.append(info)

    if data.get("footnote"):
        parts.append(f'<p class="fine">{rich(data["footnote"])}</p>')

    # palette overrides
    pal = data.get("palette") or {}
    pal_css = ";".join(f"--{esc(k)}:{esc(v)}" for k, v in pal.items())

    css = (ASSETS / "base.css").read_text(encoding="utf-8")
    css += "\n" + (ASSETS / "styles" / f"{style}.css").read_text(encoding="utf-8")
    custom = data.get("custom_css")
    if custom:
        cp = Path(os.path.expanduser(custom))
        if not cp.is_absolute():
            cp = base_dir / cp
        css += "\n" + (cp.read_text(encoding="utf-8") if cp.suffix == ".css" and cp.exists() else str(custom))

    return f"""<!doctype html>
<html lang="zh-CN" style="font-size:{unit:.3f}px">
<head><meta charset="utf-8"><meta name="viewport" content="width={w},height={h}">
<title>{esc(data.get('title', 'poster'))} · {ratio}</title>
<style>
{css}
html,body{{width:{w}px;height:{h}px}}
</style></head>
<body><div class="{' '.join(classes)}" style="{pal_css}">
{''.join(parts)}
</div>
<script>{FIT_JS}</script>
</body></html>"""


def find_chrome(explicit=None):
    for c in [explicit, os.environ.get("CHROME_PATH")] + CHROME_CANDIDATES:
        if not c:
            continue
        p = shutil.which(c) or (c if os.path.isfile(c) else None)
        if p:
            return p
    return None


def _run_chrome(chrome, html_path, size, scale, action):
    w, h = size
    with tempfile.TemporaryDirectory() as prof:
        cmd = [
            chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
            "--no-first-run", "--no-default-browser-check", "--allow-file-access-from-files",
            f"--user-data-dir={prof}", f"--force-device-scale-factor={scale}",
            f"--window-size={w},{h}", "--virtual-time-budget=4000",
            *action, "file:" + pathname2url(str(html_path)),
        ]
        if platform.system() == "Linux" and hasattr(os, "geteuid") and os.geteuid() == 0:
            cmd.insert(1, "--no-sandbox")
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120)


def screenshot(chrome, html_path, png_path, size, scale=1):
    res = _run_chrome(chrome, html_path, size, scale, [f"--screenshot={png_path}"])
    if not Path(png_path).exists():
        die(f"Chrome 截图失败：\n{res.stderr[-1500:]}")


def measure_fit(chrome, html_path, size):
    """Return the auto-fit factor (1.0 = no shrink) computed by the page script."""
    try:
        res = _run_chrome(chrome, html_path, size, 1, ["--dump-dom"])
        m = re.search(r'data-fit="([0-9.]+)"', res.stdout)
        return float(m.group(1)) if m else None
    except Exception:
        return None


def build_sheet(chrome, outputs, out_dir, name):
    """Lay all rendered sizes side by side at a common height of 720px."""
    H, gap, pad = 720, 48, 48
    cells, total_w = "", pad
    for ratio, png in outputs:
        w, h = RATIOS[ratio]["size"]
        dw = round(w * H / h)
        total_w += dw + gap
        src = "file:" + pathname2url(str(png))
        cells += (f'<figure><img src="{src}" style="width:{dw}px;height:{H}px">'
                  f'<figcaption>{ratio} · {w}×{h}</figcaption></figure>')
    total_w += pad - gap
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{total_w}px;height:{H + 2 * pad + 44}px;overflow:hidden}}
body{{background:#E9E7E3;font-family:sans-serif;display:flex;gap:{gap}px;padding:{pad}px;box-sizing:border-box}}
figure{{margin:0;display:flex;flex-direction:column;gap:12px}} img{{box-shadow:0 12px 40px rgba(0,0,0,.18)}}
figcaption{{font-size:22px;color:#555;letter-spacing:.05em}}</style></head><body>{cells}</body></html>"""
    sp = out_dir / f"{name}_sheet.html"
    sp.write_text(page, encoding="utf-8")
    png = out_dir / f"{name}_sheet.png"
    if png.exists():
        png.unlink()
    screenshot(chrome, sp, png, (total_w, H + 2 * pad + 44))
    sp.unlink()
    return png


def doctor():
    chrome = find_chrome()
    print(f"Chrome/Chromium/Edge: {chrome or '未找到（可设置环境变量 CHROME_PATH）'}")
    if shutil.which("fc-list"):
        out = subprocess.run(["fc-list", ":lang=zh", "family"], capture_output=True, text=True).stdout
        fams = sorted({l.split(",")[0] for l in out.splitlines() if l.strip()})
        good = [f for f in fams if re.search(r"Noto|Source Han|PingFang|Songti|HarmonyOS|YaHei|Hei|Song", f)]
        print("中文字体：", ", ".join(good[:8]) or "未检测到；建议安装 Noto Sans/Serif CJK SC（思源黑体/宋体）")
    elif platform.system() == "Darwin":
        print("中文字体：macOS 自带 PingFang SC / Songti SC，可直接使用")
    else:
        print("中文字体：Windows 自带 Microsoft YaHei / SimSun；推荐安装思源黑体、思源宋体获得更好效果")
    return 0 if chrome else 1


def main():
    ap = argparse.ArgumentParser(description="Render studio event posters (3:4 / 9:16 / 1:1 / 16:9)")
    ap.add_argument("spec", nargs="?", help="poster spec JSON")
    ap.add_argument("--out", help="output dir (default: <spec dir>/output)")
    ap.add_argument("--ratios", help="comma list, e.g. 3:4,9:16,1:1,16:9")
    ap.add_argument("--style", help="override style")
    ap.add_argument("--variant", help="override variant")
    ap.add_argument("--scale", type=float, default=1, help="device scale factor, 2 = retina")
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument("--sheet", action="store_true", help="also render an overview sheet of all sizes")
    ap.add_argument("--chrome", help="path to Chrome/Chromium/Edge")
    ap.add_argument("--list-styles", action="store_true")
    ap.add_argument("--doctor", action="store_true")
    ap.add_argument("--no-check", action="store_true", help="skip the density (fit) check")
    a = ap.parse_args()

    if a.list_styles:
        for k, v in STYLES.items():
            extra = f"  variants: {'/'.join(VARIANTS[k])}" if k in VARIANTS else ""
            print(f"{k:10s} {v}{extra}")
        return
    if a.doctor:
        sys.exit(doctor())
    if not a.spec:
        ap.print_help()
        sys.exit(1)

    spec_path = Path(a.spec).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if a.style:
        spec["style"] = a.style
    if a.variant:
        spec["variant"] = a.variant
    ratios = [x.strip() for x in (a.ratios or ",".join(spec.get("ratios") or RATIOS.keys())).split(",") if x.strip()]
    for x in ratios:
        if x not in RATIOS:
            die(f"不支持的规格 {x}，可选：{', '.join(RATIOS)}")

    out_dir = Path(a.out).resolve() if a.out else spec_path.parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    name = spec.get("output_name") or spec_path.stem
    chrome = None if a.html_only else find_chrome(a.chrome)
    if not a.html_only and not chrome:
        print("⚠ 未找到 Chrome/Chromium/Edge，只输出 HTML（用浏览器打开后可截图，或设置 CHROME_PATH）", file=sys.stderr)

    outputs = []
    for ratio in ratios:
        slug = RATIOS[ratio]["slug"]
        hp = out_dir / f"{name}_{slug}.html"
        hp.write_text(build_html(spec, ratio, spec_path.parent), encoding="utf-8")
        if chrome:
            png = out_dir / f"{name}_{slug}.png"
            if png.exists():
                png.unlink()
            screenshot(chrome, hp, png, RATIOS[ratio]["size"], a.scale)
            outputs.append((ratio, png))
            fit = None if a.no_check else measure_fit(chrome, hp, RATIOS[ratio]["size"])
            note = ""
            if fit is not None:
                note = f"  fit={fit:.2f}"
                if fit < 0.75:
                    note += "  ⚠ POSTER_DENSE：内容过多被明显缩小，建议用 by_ratio 精简"
            print(f"✓ {ratio:5s} → {png}{note}")
        else:
            print(f"✓ {ratio:5s} → {hp}")
    if a.sheet and chrome and outputs:
        print(f"✓ sheet → {build_sheet(chrome, outputs, out_dir, name)}")


if __name__ == "__main__":
    main()
