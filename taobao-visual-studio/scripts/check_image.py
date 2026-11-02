#!/usr/bin/env python3
"""Check product images against Chinese marketplace specs (Taobao by default).

Usage:
  check_image.py IMG [IMG...] --role main|white|detail [--platform taobao] [--fix] [--json]

Exit code: 0 = all pass, 1 = violations found, 2 = usage/IO error.
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("需要 Pillow：pip install Pillow", file=sys.stderr)
    sys.exit(2)

# Keep in sync with references/taobao-specs.md
SPECS = {
    "taobao": {"main_min": 800, "main_ratios": [(1, 1), (3, 4)], "main_max_mb": 3.0,
               "detail_width": 750, "detail_max_h": 2000, "detail_max_mb": 2.0,
               "white_export": 800, "main_export": 800},
    "tmall": {"main_min": 800, "main_ratios": [(1, 1), (3, 4)], "main_max_mb": 3.0,
              "detail_width": 790, "detail_max_h": 2000, "detail_max_mb": 2.0,
              "white_export": 800, "main_export": 800},
    "jd": {"main_min": 800, "main_ratios": [(1, 1)], "main_max_mb": 3.0,
           "detail_width": 750, "detail_max_h": 2000, "detail_max_mb": 2.0,
           "white_export": 800, "main_export": 800},
    "pdd": {"main_min": 750, "main_ratios": [(1, 1)], "main_max_mb": 3.0,
            "detail_width": 750, "detail_max_h": 1500, "detail_max_mb": 1.0,
            "white_export": 800, "main_export": 800},
    "douyin": {"main_min": 600, "main_ratios": [(1, 1), (3, 4)], "main_max_mb": 3.0,
               "detail_width": 750, "detail_max_h": 2000, "detail_max_mb": 2.0,
               "white_export": 800, "main_export": 800},
}

WHITE_TOL = 250  # channel value >= this counts as white
BORDER = 0.04    # border band (fraction of size) that must be pure white


def ratio_ok(w, h, ratios, tol=0.02):
    return any(abs(w / h - a / b) <= tol for a, b in ratios)


def nearest_ratio(w, h, ratios):
    return min(ratios, key=lambda r: abs(w / h - r[0] / r[1]))


def white_stats(img):
    small = img.convert("RGB").resize((300, 300))
    px = small.load()
    n = 300
    b = max(1, int(n * BORDER))
    border_total = border_white = 0
    fg = 0
    minx, miny, maxx, maxy = n, n, -1, -1
    for y in range(n):
        for x in range(n):
            r, g, bl = px[x, y]
            is_white = r >= WHITE_TOL and g >= WHITE_TOL and bl >= WHITE_TOL
            if x < b or y < b or x >= n - b or y >= n - b:
                border_total += 1
                border_white += is_white
            if not is_white:
                fg += 1
                minx, miny = min(minx, x), min(miny, y)
                maxx, maxy = max(maxx, x), max(maxy, y)
    bbox = None if maxx < 0 else ((maxx - minx + 1) / n, (maxy - miny + 1) / n)
    touches_edge = maxx >= 0 and (minx == 0 or miny == 0 or maxx == n - 1 or maxy == n - 1)
    return border_white / border_total, fg / (n * n), bbox, touches_edge


def check(path, role, spec):
    v, info = [], {}
    size_mb = os.path.getsize(path) / 1024 / 1024
    img = Image.open(path)
    w, h = img.size
    info.update(width=w, height=h, size_mb=round(size_mb, 2), format=img.format)
    if img.format not in ("JPEG", "PNG"):
        v.append(f"格式 {img.format} 不是 JPG/PNG")

    if role in ("main", "white"):
        ratios = [(1, 1)] if role == "white" else spec["main_ratios"]
        if not ratio_ok(w, h, ratios):
            v.append(f"比例 {w}x{h} 不符合 {['%d:%d' % r for r in ratios]}")
        if min(w, h) < spec["main_min"]:
            v.append(f"短边 {min(w, h)}px < {spec['main_min']}px（无法放大镜/可能被拒）")
        if size_mb > spec["main_max_mb"]:
            v.append(f"文件 {size_mb:.2f}MB > {spec['main_max_mb']}MB")
    if role == "white":
        bw, fg, bbox, edge = white_stats(img)
        info.update(border_white=round(bw, 3), foreground=round(fg, 3), bbox=bbox)
        if bw < 0.98:
            v.append(f"背景非纯白（边缘纯白像素仅 {bw:.0%}，需 #FFFFFF）")
        if edge:
            v.append("主体触碰画面边缘（可能被裁切，需四周留白）")
        if bbox and max(bbox) < 0.55:
            v.append(f"主体偏小（外框最大边占 {max(bbox):.0%}，建议 60%-80%）")
        if bbox and max(bbox) > 0.92:
            v.append(f"主体过大（外框占 {max(bbox):.0%}，建议 ≤80%-90%）")
        if fg < 0.02:
            v.append("几乎没有检测到主体")
    if role == "detail":
        if w != spec["detail_width"]:
            v.append(f"宽度 {w}px ≠ {spec['detail_width']}px（可用 --fix 导出）")
        scaled_h = h * spec["detail_width"] / w
        if scaled_h > spec["detail_max_h"]:
            v.append(f"按 {spec['detail_width']} 宽计算高度 {scaled_h:.0f}px > {spec['detail_max_h']}px，建议切片")
        if size_mb > spec["detail_max_mb"]:
            v.append(f"文件 {size_mb:.2f}MB > {spec['detail_max_mb']}MB")
    return v, info


def fix(path, role, spec):
    img = Image.open(path)
    w, h = img.size
    if role in ("main", "white"):
        ratios = [(1, 1)] if role == "white" else spec["main_ratios"]
        a, b = nearest_ratio(w, h, ratios)
        if abs(w / h - a / b) > 0.02:  # center-crop to ratio
            if w / h > a / b:
                nw = int(h * a / b)
                img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
            else:
                nh = int(w * b / a)
                img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        base = spec["white_export"] if role == "white" else spec["main_export"]
        tw = base if (a, b) == (1, 1) else 750
        target = (tw, int(tw * b / a))
    else:
        tw = spec["detail_width"]
        target = (tw, round(h * tw / w))
    img = img.convert("RGB").resize(target, Image.LANCZOS)
    root, _ = os.path.splitext(path)
    out = f"{root}-{target[0]}x{target[1]}.jpg"
    img.save(out, "JPEG", quality=90, optimize=True)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("images", nargs="+")
    ap.add_argument("--role", choices=["main", "white", "detail"], required=True)
    ap.add_argument("--platform", choices=sorted(SPECS), default="taobao")
    ap.add_argument("--fix", action="store_true", help="导出符合尺寸的 JPG 副本后再检查")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    spec = SPECS[a.platform]
    results, failed = [], False
    for p in a.images:
        try:
            target = fix(p, a.role, spec) if a.fix else p
            v, info = check(target, a.role, spec)
        except Exception as e:  # noqa: BLE001
            print(f"读取失败 {p}: {e}", file=sys.stderr)
            sys.exit(2)
        failed |= bool(v)
        results.append({"file": target, "ok": not v, "violations": v, "info": info})
    if a.json:
        print(json.dumps({"platform": a.platform, "role": a.role, "results": results}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            mark = "✅" if r["ok"] else "❌"
            i = r["info"]
            print(f"{mark} {r['file']}  {i['width']}x{i['height']} {i['size_mb']}MB")
            for x in r["violations"]:
                print(f"   - {x}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
