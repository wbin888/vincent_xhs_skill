#!/usr/bin/env python3
"""Lint e-commerce copy for China Advertising Law risk words.

Usage:
  lint_copy.py "文案..."             # inline text
  lint_copy.py -f plan.md            # file (e.g. approval table / prompts)
  lint_copy.py -f plan.md --category cosmetics|food|health|baby|medical

Exit code: 0 = clean, 1 = risk words found.
Not legal advice; keep in sync with references/compliance.md.
"""
import argparse
import re
import sys

ABSOLUTE = ["最佳", "最好", "最优", "最强", "最高级", "最高", "最低", "最大", "最小", "最新", "最先进", "最便宜",
            "最受欢迎", "最安全", "第一", "唯一", "首个", "首选", "顶级", "极致", "极品", "国家级", "世界级",
            "全网第一", "销量第一", "NO.1", "No.1", "TOP1", "Top1", "万能", "永久", "绝对", "史无前例",
            "遥遥领先", "王牌", "领导品牌", "填补国内空白", "独家", "全球首发", "全国首发", "100%", "百分百",
            "零风险", "无敌", "完美", "神器", "秒杀全网", "军工级", "航天级", "军用级"]
ENDORSE = ["国家认证", "专家推荐", "医生推荐", "明星同款", "驰名商标", "质量免检", "万人好评", "权威认证",
           "官方推荐", "央视推荐"]
CATEGORY = {
    "cosmetics": ["治疗", "消炎", "抗菌", "杀菌", "祛痘", "祛斑", "生发", "防脱", "修复受损", "药妆", "医学护肤",
                  "换肤", "排毒", "抗敏", "处方"],
    "food": ["预防", "治疗", "降血压", "降血糖", "降血脂", "排毒", "抗癌", "防癌", "增强免疫力", "减肥", "治愈", "药效"],
    "health": ["治疗", "治愈", "根治", "药效", "替代药物", "无副作用", "抗癌"],
    "baby": ["最安全", "无任何刺激", "100%无害", "零添加（无证明）", "母乳级", "替代母乳"],
    "medical": ["治愈率", "根治", "保证治愈", "无副作用", "立竿见影"],
}
# "最" followed by an adjective-like char is broadly risky; catch remaining cases.
ZUI = re.compile(r"最[\u4e00-\u9fa5]")


def scan(text, words):
    hits = []
    for w in words:
        for m in re.finditer(re.escape(w), text):
            hits.append((m.start(), w))
    return hits


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", nargs="?")
    ap.add_argument("-f", "--file")
    ap.add_argument("--category", choices=sorted(CATEGORY))
    a = ap.parse_args()
    if not a.text and not a.file:
        ap.error("需要文本或 -f 文件")
    text = open(a.file, encoding="utf-8").read() if a.file else a.text

    groups = [("绝对化用语", ABSOLUTE), ("无依据背书", ENDORSE)]
    if a.category:
        groups.append((f"类目禁用({a.category})", CATEGORY[a.category]))
    found = []
    covered = set()
    hits = [(pos, w, name) for name, words in groups for pos, w in scan(text, words)]
    for pos, w, name in sorted(hits, key=lambda h: -len(h[1])):  # longest match wins
        span = set(range(pos, pos + len(w)))
        if span <= covered:
            continue
        found.append((line_of(text, pos), name, w))
        covered |= span
    for m in ZUI.finditer(text):
        if m.start() not in covered:
            found.append((line_of(text, m.start()), "疑似极限词", m.group()))

    if not found:
        print("✅ 未发现风险词")
        return 0
    for ln, name, w in sorted(set(found)):
        print(f"❌ 第{ln}行 [{name}] {w}")
    print("\n提示：改写为可观察、可证明的具体事实；有真实证据的背书请在交付中附来源。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
