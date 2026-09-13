# -*- coding: utf-8 -*-
"""주아체 정보 카드 일러스트(620x400, 투명 배경, 겟백 팔레트) 생성.
사용: python3 illust_card.py --out 두갈래.png --title "리더의 수입은 두 갈래" --line "1. 멤버의 성장을 돕고 번다" --line "2. 멤버의 트래픽을 관리하고 번다" --warn "멤버끼리의 거래에는 손대지 않는다" --note "출처나 한 줄 설명"
글리프 주의: 주아체에 ①② · → 같은 기호가 없다. 숫자는 "1." 형식, 가운뎃점은 쉼표로.
"""
import argparse, subprocess, os
ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True); ap.add_argument('--title', required=True)
ap.add_argument('--line', action='append', default=[]); ap.add_argument('--warn', default=''); ap.add_argument('--note', default='')
ap.add_argument('--font', default=os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'BMJUA_ttf.ttf'))
ap.add_argument('--magick', default='/opt/homebrew/bin/magick')
a = ap.parse_args()
F = os.path.abspath(a.font)
cmd = [a.magick, '-size', '620x400', 'xc:none', '-fill', '#12121aE6', '-stroke', '#D4F000', '-strokewidth', '3',
       '-draw', 'roundrectangle 4,4 616,396 20,20', '-stroke', 'none', '-font', F,
       '-fill', '#D4F000', '-pointsize', '34', '-draw', "text 40,72 '%s'" % a.title.replace("'", "")]
y = 130
if a.line:
    cmd += ['-stroke', '#D4F000', '-strokewidth', '6', '-draw', 'line 70,%d 70,%d' % (y - 20, y + 90 * (len(a.line) - 1) + 20)]
    for i, _ in enumerate(a.line): cmd += ['-draw', 'line 70,%d 140,%d' % (y + 90 * i, y + 90 * i)]
    cmd += ['-stroke', 'none', '-fill', '#ffffff', '-pointsize', '32']
    for i, l in enumerate(a.line): cmd += ['-draw', "text 160,%d '%s'" % (y + 90 * i + 12, l.replace("'", ""))]
    y += 90 * len(a.line)
if a.warn:
    cmd += ['-stroke', '#ff6b6b', '-strokewidth', '5', '-draw', 'line 70,%d 140,%d' % (y, y), '-stroke', 'none',
            '-fill', '#ff9d9d', '-pointsize', '28', '-draw', "text 160,%d '%s'" % (y + 10, a.warn.replace("'", ""))]
    y += 60
if a.note:
    cmd += ['-fill', '#b9b4c0', '-pointsize', '24', '-draw', "text 40,%d '%s'" % (min(y + 30, 372), a.note.replace("'", ""))]
cmd.append(a.out)
subprocess.run(cmd, check=True); print('wrote', a.out)
