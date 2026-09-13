# 교정 TSV(<work>/out2/*.tsv)를 <work>/segs_new.json에 적용 → <work>/segs_final.json (단어 타임스탬프 재배분)
# 사용: python3 apply_fix.py <work_dir>
import json, glob, os, sys, re
W = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
segs = json.load(open(os.path.join(W, 'segs_new.json'), encoding='utf-8'))
fixed = {}
for f in sorted(glob.glob(os.path.join(W, 'out2', 'c*.tsv'))):
    for line in open(f, encoding='utf-8'):
        if '\t' not in line: continue
        i, t = line.rstrip('\n').split('\t', 1)
        if i.isdigit(): fixed[int(i)] = t.strip()
applied = 0; dropped = 0
for i, s in enumerate(segs):
    if i not in fixed: continue
    t = fixed[i]
    if t == '':
        s['words'] = []; s['t'] = ''; dropped += 1; continue
    if t == s['t']: continue
    old = s['words']; new_tokens = t.split()
    if old and len(new_tokens) == len(old):
        for w, tok in zip(old, new_tokens): w['w'] = tok
    else:
        st = old[0]['s'] if old else s['s']; en = old[-1]['e'] if old else s['e']
        total = sum(len(x) for x in new_tokens) or 1; acc = 0.0; ws = []
        for tok in new_tokens:
            a = st + (en - st) * acc / total; acc += len(tok); b = st + (en - st) * acc / total
            ws.append({'w': tok, 's': round(a, 2), 'e': round(b, 2)})
        s['words'] = ws
    s['t'] = t; applied += 1
json.dump(segs, open(os.path.join(W, 'segs_final.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('fixed lines', len(fixed), 'applied', applied, 'dropped', dropped, 'coverage upto seg', max(fixed) if fixed else -1, 'time', segs[max(fixed)]['e'] if fixed else 0)
