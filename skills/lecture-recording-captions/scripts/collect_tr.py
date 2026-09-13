# 재전사 청크(json, 10분 단위) → 절대시간 세그먼트/단어 + 교정용 TSV
# 사용: python3 collect_tr.py <tr_dir> <work_dir>   (CHUNK_SEC 환경변수로 청크 길이 변경, 기본 600)
import json, glob, os, re, sys
TR = sys.argv[1]  # tr dir
OUT = sys.argv[2]
segs = []
for f in sorted(glob.glob(os.path.join(TR, 'a*.json'))):
    i = int(re.search(r'a(\d+)\.json', f).group(1)); off = i * int(os.environ.get('CHUNK_SEC', 600))
    d = json.load(open(f, encoding='utf-8'))
    for s in d['segments']:
        t = s['text'].strip()
        if not t: continue
        core = re.sub(r'[\s.,!?~]', '', t)
        if len(core) >= 3 and len(set(core)) <= 2: continue          # 하하하 류
        if s.get('no_speech_prob', 0) > 0.85 and len(core) < 6: continue
        if s.get('compression_ratio', 0) > 2.6: continue
        words = [{'w': w['word'].strip(), 's': round(w['start'] + off, 2), 'e': round(w['end'] + off, 2)} for w in s.get('words', []) if w['word'].strip()]
        segs.append({'s': round(s['start'] + off, 2), 'e': round(s['end'] + off, 2), 't': t, 'words': words})
segs.sort(key=lambda x: x['s'])
# 인접 중복(청크 경계 반복) 제거
dedup = []
for s in segs:
    if dedup and s['t'] == dedup[-1]['t'] and s['s'] - dedup[-1]['e'] < 3: continue
    dedup.append(s)
json.dump(dedup, open(os.path.join(OUT, 'segs_new.json'), 'w', encoding='utf-8'), ensure_ascii=False)
os.makedirs(os.path.join(OUT, 'chunks2'), exist_ok=True)
for f in glob.glob(os.path.join(OUT, 'chunks2', '*')): os.remove(f)
N = 120
for i in range(0, len(dedup), N):
    with open(os.path.join(OUT, 'chunks2', f'c{i//N:02d}.tsv'), 'w', encoding='utf-8') as fh:
        for j, x in enumerate(dedup[i:i+N]): fh.write(f"{i+j}\t{x['t']}\n")
print('segments', len(dedup), 'last', dedup[-1]['e'], 'chunks', (len(dedup)+N-1)//N, 'chars', sum(len(x['t']) for x in dedup))
