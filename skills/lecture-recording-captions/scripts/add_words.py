#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""문장 단위 세그먼트에 어절 단위 타임스탬프를 만들어 붙인다.

스킬의 make_video.py는 어절 하이라이트(가라오케)를 위해 s['words'] = [{w, s, e}]를 요구한다.
줌 전사본은 문장 단위라, 글자 수 비례로 어절 시간을 배분한다.
"""
import json, sys

SRC = sys.argv[1]
segs = json.load(open(SRC, encoding="utf-8"))

out = 0
for s in segs:
    text = s["text"].strip()
    toks = [t for t in text.split() if t]
    if not toks:
        s["words"] = []
        continue
    dur = max(0.4, s["end"] - s["start"])
    total = sum(len(t) for t in toks)
    t = s["start"]
    words = []
    for tok in toks:
        share = dur * (len(tok) / total)
        words.append({"w": tok, "s": round(t, 3), "e": round(t + share, 3)})
        t += share
    s["words"] = words
    out += len(words)

json.dump(segs, open(SRC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"세그먼트 {len(segs)}개 · 어절 {out}개 생성")
print("샘플:", json.dumps(segs[1]["words"][:4], ensure_ascii=False))
