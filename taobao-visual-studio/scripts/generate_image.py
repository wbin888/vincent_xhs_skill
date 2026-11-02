#!/usr/bin/env python3
"""Generate one image through any OpenAI-compatible Images API (stdlib only).

Env:
  IMAGE_API_KEY   (or OPENAI_API_KEY)  required
  IMAGE_API_BASE  default https://api.openai.com/v1
  IMAGE_MODEL     default gpt-image-1

Usage:
  generate_image.py --prompt-file prompts/主图-01.txt --size 1024x1024 --out 主图/01.png [--image product.png ...]
  generate_image.py --prompt "..." --out a.png --dry-run      # print request only

With --image, calls /images/edits (multipart) so the product photo is the identity reference.
Exit: 0 ok / 1 API error / 2 bad args / 3 missing key / 4 network.
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import uuid


def multipart(fields, files):
    boundary = uuid.uuid4().hex
    body = bytearray()
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, path in files:
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            data = f.read()
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; "
                 f"filename=\"{os.path.basename(path)}\"\r\nContent-Type: {mime}\r\n\r\n").encode()
        body += data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return bytes(body), f"multipart/form-data; boundary={boundary}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--quality", default="high")
    ap.add_argument("--image", action="append", default=[], help="参考图，可重复")
    ap.add_argument("--model")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    prompt = a.prompt or open(a.prompt_file, encoding="utf-8").read().strip()
    for p in a.image:
        if not os.path.isfile(p):
            print(f"参考图不存在: {p}", file=sys.stderr)
            return 2
    base = os.environ.get("IMAGE_API_BASE", "https://api.openai.com/v1").rstrip("/")
    model = a.model or os.environ.get("IMAGE_MODEL", "gpt-image-1")
    key = os.environ.get("IMAGE_API_KEY") or os.environ.get("OPENAI_API_KEY")
    endpoint = f"{base}/images/edits" if a.image else f"{base}/images/generations"
    fields = {"model": model, "prompt": prompt, "size": a.size, "quality": a.quality, "n": "1"}

    if a.dry_run:
        print(json.dumps({"endpoint": endpoint, "fields": fields, "images": a.image}, ensure_ascii=False, indent=2))
        return 0
    if not key:
        print("未配置 IMAGE_API_KEY / OPENAI_API_KEY；请改为交付 Prompt 包。", file=sys.stderr)
        return 3

    if a.image:
        name = "image[]" if len(a.image) > 1 else "image"
        data, ctype = multipart(fields, [(name, p) for p in a.image])
    else:
        fields["n"] = 1
        data, ctype = json.dumps(fields).encode(), "application/json"
    req = urllib.request.Request(endpoint, data=data, method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": ctype})
    try:
        with urllib.request.urlopen(req, timeout=a.timeout) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        print(f"API 错误 {e.code}: {e.read().decode(errors='replace')[:800]}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"网络错误: {e}", file=sys.stderr)
        return 4

    item = (resp.get("data") or [{}])[0]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    if item.get("b64_json"):
        with open(a.out, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
    elif item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=a.timeout) as r, open(a.out, "wb") as f:
            f.write(r.read())
    else:
        print(f"响应中没有图片: {json.dumps(resp)[:500]}", file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "file": os.path.abspath(a.out), "model": model}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
