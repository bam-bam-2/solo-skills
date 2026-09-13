# -*- coding: utf-8 -*-
"""슬라이드 크롭 영상(base.mp4)의 프레임을 슬라이드 PNG와 대조해 '어느 슬라이드가 언제 떠 있었는지' 구간표를 만든다.
사용: python3 slide_runs.py <base.mp4> <slides_dir(s-01.png ...)> <out.json> [--step 2] [--thresh 60]
결과는 [[start,end,slide], ...]. slide 0 = 판별 불가. **어두운 슬라이드끼리는 오판이 잦으니 반드시 프레임을 뽑아 눈으로 대조하고 손으로 고칠 것.**
"""
import subprocess, sys, os, glob, json, re, argparse
ap = argparse.ArgumentParser(); ap.add_argument('base'); ap.add_argument('slides'); ap.add_argument('out')
ap.add_argument('--step', type=float, default=2.0); ap.add_argument('--thresh', type=float, default=60); ap.add_argument('--ffmpeg', default='ffmpeg')
a = ap.parse_args()
W, H = 48, 27; N = W * H * 3
tmp = a.out + '.frames.rgb'
subprocess.run([a.ffmpeg, '-y', '-v', 'error', '-i', a.base, '-vf', f'fps=1/{a.step},scale={W}:{H}', '-pix_fmt', 'rgb24', '-f', 'rawvideo', tmp], check=True)
fr = open(tmp, 'rb').read(); n = len(fr) // N
tpl = {}
for f in sorted(glob.glob(os.path.join(a.slides, 's-*.png'))):
    i = int(re.search(r's-(\d+)\.png', f).group(1))
    t = f + '.rgb'
    subprocess.run([a.ffmpeg, '-y', '-v', 'error', '-i', f, '-vf', f'crop=iw:ih*0.96:0:0,scale={W}:{H}', '-pix_fmt', 'rgb24', '-f', 'rawvideo', t], check=True)
    tpl[i] = open(t, 'rb').read(); os.remove(t)
def d3(x, y): return sum(abs(p - q) for p, q in zip(x, y)) / N
runs = []; cur = None
for k in range(n):
    f = fr[k*N:(k+1)*N]; best = min(tpl, key=lambda i: d3(f, tpl[i])); d = d3(f, tpl[best])
    b = best if d <= a.thresh else 0; t = k * a.step
    if cur and cur[1] == b: cur[2] = t
    else:
        if cur: runs.append(cur)
        cur = [t, b, t]
runs.append(cur); os.remove(tmp)
runs = [[r[0], r[2] + a.step, r[1]] for r in runs if r[2] - r[0] >= 3 * a.step or r[1] == 0]
json.dump(runs, open(a.out, 'w'), ensure_ascii=False)
for r in runs: print('%7.1f-%7.1f slide %2d' % tuple(r))
