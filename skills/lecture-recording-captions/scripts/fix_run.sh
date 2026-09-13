#!/bin/bash
# 교정 청크(chunks2/*.tsv)를 claude -p로 돌려 out2/*.tsv 생성. 줄 수가 안 맞으면 3회 재시도. 맥미니에서 실행.
# 사용: fix_run.sh <작업디렉터리(fix_prompt.txt, chunks2/ 포함)>
cd "$1"; mkdir -p out2
for f in chunks2/c*.tsv; do
  b=$(basename $f .tsv); [ -s out2/$b.tsv ] && continue
  for try in 1 2 3; do
    { cat fix_prompt.txt; cat $f; } | claude -p --model sonnet > out2/$b.tmp 2> out2/$b.err
    n1=$(wc -l < $f); n2=$(grep -c $'^[0-9]\+\t' out2/$b.tmp)
    if [ "$n1" -eq "$n2" ]; then mv out2/$b.tmp out2/$b.tsv; echo "$b ok ($n2)"; break; else echo "$b mismatch $n1 vs $n2 try $try"; sleep 5; fi
  done
done
echo FIXDONE
