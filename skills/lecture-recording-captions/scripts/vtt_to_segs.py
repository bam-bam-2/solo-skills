#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""줌 WEBVTT 전사본 → 스킬의 segs_final.json 형식으로 변환.

스킬 파이프라인(전사·교정)을 건너뛰고 줌 자동 전사본을 그대로 자막 소스로 쓴다.
긴 발화는 읽기 좋게 나눈다.
"""
import json, re, sys, os

SRC = sys.argv[1]
OUT = sys.argv[2]
MAX_CHARS = 38          # 자막 한 줄 최대
MAX_DUR = 6.0           # 한 자막 최대 노출 시간


def ts(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(".")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


raw = open(SRC, encoding="utf-8").read().split("\n")
cues = []
i = 0
while i < len(raw):
    line = raw[i].strip()
    if "-->" in line:
        a, b = line.split(" --> ")
        start, end = ts(a.strip()), ts(b.strip())
        i += 1
        parts = []
        while i < len(raw) and raw[i].strip():
            parts.append(raw[i].strip())
            i += 1
        text = " ".join(parts)
        text = re.sub(r"^[^:]{1,12}:\s*", "", text)   # "밤밤: " 화자 표기 제거
        if text:
            cues.append({"start": start, "end": end, "text": text})
    i += 1

# 긴 큐를 문장 단위로 쪼갠다
segs = []
for c in cues:
    dur = c["end"] - c["start"]
    txt = c["text"]
    if len(txt) <= MAX_CHARS * 2 and dur <= MAX_DUR:
        segs.append(c)
        continue
    sents = re.split(r"(?<=[.?!])\s+|(?<=요)\s+(?=[가-힣])", txt)
    sents = [s.strip() for s in sents if s.strip()]
    if not sents:
        segs.append(c)
        continue
    total = sum(len(s) for s in sents)
    t = c["start"]
    for s in sents:
        share = dur * (len(s) / total)
        segs.append({"start": round(t, 2), "end": round(t + share, 2), "text": s})
        t += share

json.dump(segs, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"큐 {len(cues)}개 → 세그먼트 {len(segs)}개")
print(f"총 길이: {segs[-1]['end']/60:.1f}분")
print("샘플:")
for s in segs[:3]:
    print(f"  [{s['start']:.1f}~{s['end']:.1f}] {s['text'][:50]}")
