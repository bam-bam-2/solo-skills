# -*- coding: utf-8 -*-
"""강의 녹화본 자막판 조립기. config.json 하나로 ASS 자막 + ffmpeg 렌더 스크립트를 만든다.
사용: python3 make_video.py config.json   → <work>/sub*.ass, render.sh 생성. 실제 렌더는 bash render.sh (맥미니, ffmpeg-full).

config 예시는 ../references/example-config.json. 시간 단위는 전부 '전사(오디오) 타임라인 초'.
"""
import json, os, sys
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
W = os.path.abspath(cfg['work_dir']); J = lambda *p: os.path.join(W, *p)
FF = cfg.get('ffmpeg', 'ffmpeg')
ENC = cfg.get('encode', "-c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -ar 48000 -ac 2")
sub = cfg.get('subtitle', {})
FONT = sub.get('font', 'NanumGothic ExtraBold'); SIZE1 = sub.get('size', 64); SIZE2 = sub.get('size_phase2', 60)
SUNG = sub.get('sung', '&H00FF2F7B'); UNSUNG = sub.get('unsung', '&H00FFFFFF'); BOX = sub.get('box', '&H96000000')
MAXCH = sub.get('max_chars', 24); MAXSPAN = sub.get('max_span', 4.2); GAP = sub.get('gap', 0.9)
CARDFONT = cfg.get('card_font', 'BM JUA')

def ts(t):
    t = max(0.0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return '%d:%02d:%05.2f' % (h, m, s)
def dlg(s, e, style, text, layer=0): return 'Dialogue: %d,%s,%s,%s,,0,0,0,,%s' % (layer, ts(s), ts(e), style, text)

# ---------- 자막 라인 ----------
segs = json.load(open(J(cfg['segments']), encoding='utf-8'))
words = sorted([w for s in segs for w in s['words'] if w['w']], key=lambda w: w['s'])
lines, cur = [], []
for w in words:
    if cur:
        gap = w['s'] - cur[-1]['e']; span = w['e'] - cur[0]['s']; chars = sum(len(x['w']) + 1 for x in cur)
        if gap > GAP or span > MAXSPAN or chars + len(w['w']) > MAXCH or cur[-1]['w'][-1] in '.?!': lines.append(cur); cur = []
    cur.append(w)
if cur: lines.append(cur)
subs = [{'s': L[0]['s'], 'e': max(L[-1]['e'] + 0.15, L[0]['s'] + 0.8), 'words': L} for L in lines]
for i in range(len(subs) - 1):
    if subs[i]['e'] > subs[i+1]['s'] - 0.05: subs[i]['e'] = max(subs[i]['s'] + 0.5, subs[i+1]['s'] - 0.05)
def karaoke(L):
    out = ''
    for i, w in enumerate(L):
        nxt = L[i+1]['s'] if i + 1 < len(L) else w['e']
        out += '{\\k%d}%s ' % (max(5, int(round((nxt - w['s']) * 100))), w['w'])
    return out.strip()

HEAD = ('[Script Info]\nScriptType: v4.00+\nWrapStyle: 2\nScaledBorderAndShadow: yes\nPlayResX: 1920\nPlayResY: 1080\n\n[V4+ Styles]\n'
 'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
 f'Style: Pop,{FONT},{SIZE1},{SUNG},{UNSUNG},&H00000000,{BOX},0,0,0,0,100,100,0,0,4,12,0,2,100,100,96,1\n'
 f'Style: Pop2,{FONT},{SIZE2},{SUNG},{UNSUNG},&H00000000,{BOX},0,0,0,0,100,100,0,0,4,12,0,2,100,100,50,1\n'
 f'Style: Card,{CARDFONT},62,&H00000000,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,7,0,0,0,1\n'
 f'Style: Kicker,{CARDFONT},30,&H001A1212,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,6,0,1,0,0,7,0,0,0,1\n'
 'Style: LimeBar,Arial,40,&H0000F0D4,&H000000FF,&H0000F0D4,&H0000F0D4,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1\n'
 f'Style: Tag,{CARDFONT},36,&H0000F0D4,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,0,0,7,0,0,0,1\n'
 f'Style: End,{CARDFONT},70,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1\n'
 'Style: End2,Apple SD Gothic Neo,30,&H00B9B4C0,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1\n'
 '\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')

def title_card(ev, t0, kicker, title, dur=4.0):
    bw = min(1500, 60 + len(title) * 58)
    ev.append(dlg(t0, t0 + dur, 'LimeBar', '{\\an7\\move(-1600,120,110,120,0,650)\\fad(0,350)\\p1}m 0 0 l %d 0 %d 132 0 132{\\p0}' % (bw, bw), 1))
    ev.append(dlg(t0 + 0.5, t0 + dur, 'Kicker', '{\\an7\\pos(150,140)\\fad(250,300)}%s' % kicker, 2))
    ev.append(dlg(t0 + 0.7, t0 + dur, 'Card', '{\\an7\\pos(150,176)\\fad(280,300)}%s' % title, 2))

parts = []; cmds = []
# ---------- 1부: 슬라이드 + PIP + 줌 + 일러스트 ----------
p1 = cfg.get('phase1')
if p1:
    P1S, P1E = p1.get('start', 0.0), p1['end']
    runs = [tuple(r) for r in p1['runs']]; titles = {int(k): v for k, v in p1.get('titles', {}).items()}
    zoom = {int(k): v for k, v in p1.get('zoom', {}).items()}; ill = {int(k): v for k, v in p1.get('illustrations', {}).items()}
    ev = []
    for st, en, sl in runs:
        if sl in titles and titles[sl][1]: title_card(ev, st + 0.8, titles[sl][0], titles[sl][1])
    for sb in subs:
        if sb['e'] <= P1S or sb['s'] >= P1E: continue
        ev.append(dlg(max(sb['s'], P1S) - P1S, min(sb['e'], P1E) - P1S, 'Pop', '{\\fad(80,80)}' + karaoke(sb['words'])))
    open(J('sub1.ass'), 'w', encoding='utf-8').write(HEAD + '\n'.join(ev))
    # zoompan: 값은 팬 범위 내 비율(0=왼쪽/위 끝, 1=오른쪽/아래 끝)
    zs, xs, ys = '1', '(iw-iw/zoom)/2', '(ih-ih/zoom)/2'; zparts = []
    for st, en, sl in runs:
        if sl in zoom: d, du, z, fx, fy = zoom[sl]; zparts.append((st - P1S + d, st - P1S + d + du, z, fx, fy))
    for a, b, z, fx, fy in sorted(zparts, reverse=True):
        zz = z - 1
        zs = "if(between(T,%.2f,%.2f),if(lt(T,%.2f),1+%.3f*(T-%.2f)/1.2,if(gt(T,%.2f),1+%.3f*(%.2f-T)/1.2,%.3f)),%s)" % (a, b, a + 1.2, zz, a, b - 1.2, zz, b, z, zs)
        xs = "if(between(T,%.2f,%.2f),%.4f*(iw-iw/zoom),%s)" % (a, b, fx, xs); ys = "if(between(T,%.2f,%.2f),%.4f*(ih-ih/zoom),%s)" % (a, b, fy, ys)
    zs, xs, ys = [e.replace('T', '(on/30)') for e in (zs, xs, ys)]
    inputs = ['-i %s' % J(p1['base']), '-i %s' % J(p1['face']['path']) if p1.get('face') else '-f lavfi -i color=c=black:s=16x16:r=30',
              '-loop 1 -i %s' % J(p1['freeze']['image']) if p1.get('freeze') else '-f lavfi -i color=c=black:s=1920x1080:r=30',
              '-i %s' % J(cfg['audio'])]
    fc = "[0:v]"
    if p1.get('freeze'): fc += "[2:v]overlay=0:0:enable='gte(t,%.2f)'[b0];[b0]" % (p1['freeze']['from'] - P1S)
    fc += "zoompan=z='%s':x='%s':y='%s':d=1:s=1920x1080:fps=30,setsar=1[zoomed];" % (zs, xs, ys)
    chain = '[zoomed]'; k = 0
    for st, en, sl in runs:
        if sl not in ill: continue
        d, du, f = ill[sl]; a = st - P1S + d; b = a + du; idx = 4 + k
        inputs.append('-loop 1 -i %s' % J(f))
        fc += "[%d:v]format=rgba,fade=t=in:st=%.2f:d=0.5:alpha=1,fade=t=out:st=%.2f:d=0.5:alpha=1[il%d];" % (idx, a, b - 0.5, k)
        fc += "%s[il%d]overlay=x=1920-620-70:y=420:enable='between(t,%.2f,%.2f)'[o%d];" % (chain, k, a, b, k); chain = '[o%d]' % k; k += 1
    if p1.get('face'):
        fc += "[1:v]scale=400:-2,setsar=1,pad=iw+8:ih+8:4:4:0x0F0F12[pip];%s[pip]overlay=x=W-w-44:y=40:enable='gte(t,%.2f)'[wp];" % (chain, p1['face'].get('valid_from', 0) - P1S); chain = '[wp]'
    fc += "%sass=%s[v]" % (chain, J('sub1.ass'))
    cmds.append('%s -y -v warning -stats %s -ss %.2f -t %.2f -filter_complex "%s" -map "[v]" -map 3:a %s %s' % (FF, ' '.join(inputs), P1S, P1E - P1S, fc, ENC, J('out_p1.mp4')))
    parts.append('out_p1.mp4')
# ---------- 2부: 웹캠 + 자막 ----------
p2 = cfg.get('phase2')
if p2:
    P2S, P2E = p2['start'], p2['end']; D = P2E - P2S
    ev2 = []; t0 = p2.get('card_at', 1.0)
    if p2.get('title'): title_card(ev2, t0, p2['title'][0], p2['title'][1], 4.5)
    if p2.get('tag'): ev2.append(dlg(t0 + 5.5, D, 'Tag', '{\\an7\\pos(110,44)}%s' % p2['tag'], 1))
    for sb in subs:
        if sb['e'] <= P2S or sb['s'] >= P2E: continue
        ev2.append(dlg(max(sb['s'], P2S) - P2S, min(sb['e'], P2E) - P2S, 'Pop2', '{\\fad(80,80)}' + karaoke(sb['words'])))
    open(J('sub2.ass'), 'w', encoding='utf-8').write(HEAD + '\n'.join(ev2))
    inputs = ['-i %s' % J(p2['cam'])]; cam_len = p2.get('cam_until', P2E) - P2S
    fc = "color=c=0x101014:s=1920x1080:r=30[bg];[0:v]trim=0:%.2f,setpts=PTS-STARTPTS,setsar=1[c0];" % cam_len
    if p2.get('tail'):
        t = p2['tail']; inputs.append('-i %s' % J(t['path']))
        fc += "[1:v]trim=%.2f:%.2f,setpts=PTS-STARTPTS,setsar=1[c1x];[c0][c1x]concat=n=2:v=1:a=0[cam];" % (t['trim_from'], t['trim_from'] + (P2E - p2['cam_until']))
        ai = 2
    else: fc += "[c0]null[cam];"; ai = 1
    inputs.append('-ss %.2f -t %.2f -i %s' % (P2S, D, J(cfg['audio'])))
    fc += "[bg][cam]overlay=x=240:y=90:shortest=1[c0b];"
    if p2.get('cover'):
        inputs.append('-loop 1 -i %s' % J(p2['cover']['image'])); fc += "[c0b][%d:v]overlay=0:0:enable='lt(t,%.2f)'[c0c];" % (ai + 1, p2['cover']['until'] - P2S)
    else: fc += "[c0b]null[c0c];"
    fc += "[c0c]fade=t=out:st=%.2f:d=1.5[c1];[c1]ass=%s[v]" % (D - 1.6, J('sub2.ass'))
    cmds.append('%s -y -v warning -stats %s -filter_complex "%s" -map "[v]" -map %d:a -t %.2f -af "afade=t=out:st=%.2f:d=1.5" %s %s' % (FF, ' '.join(inputs), fc, ai, D, D - 1.6, ENC, J('out_p2.mp4')))
    parts.append('out_p2.mp4')
# ---------- 엔드카드 ----------
ec = cfg.get('endcard')
if ec:
    L = ec['lines']; ev3 = [dlg(0.3, ec.get('duration', 10), 'End', '{\\an5\\pos(960,470)\\fad(400,400)}%s' % L[0])]
    for i, l in enumerate(L[1:]): ev3.append(dlg(0.8 + 0.4 * i, ec.get('duration', 10), 'End2', '{\\an5\\pos(960,%d)\\fad(400,400)}%s' % (560 if i == 0 else 900, l)))
    open(J('sub3.ass'), 'w', encoding='utf-8').write(HEAD + '\n'.join(ev3))
    cmds.append('%s -y -v warning -f lavfi -i color=c=0x101014:s=1920x1080:r=30 -f lavfi -i anullsrc=r=48000:cl=stereo -t %.1f -vf "ass=%s" %s %s' % (FF, ec.get('duration', 10), J('sub3.ass'), ENC, J('out_p3.mp4')))
    parts.append('out_p3.mp4')
open(J('concat.txt'), 'w').write(''.join("file '%s'\n" % J(p) for p in parts))
cmds.append('%s -y -v warning -f concat -safe 0 -i %s -c copy -movflags +faststart %s' % (FF, J('concat.txt'), J(cfg.get('output', 'final.mp4'))))
open(J('render.sh'), 'w').write('#!/bin/bash\nset -e\ncd %s\n' % W + '\n'.join('%s\necho STEP%d_DONE' % (c, i + 1) for i, c in enumerate(cmds)) + '\necho ALLDONE\n')
print('subtitle lines', len(subs), 'parts', parts, '→', J('render.sh'))
