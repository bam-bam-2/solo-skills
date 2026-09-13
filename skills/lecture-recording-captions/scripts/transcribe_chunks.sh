#!/bin/bash
# 긴 오디오를 10분 청크로 잘라 mlx_whisper(단어 타임스탬프)로 전사. 맥미니에서 실행.
# 사용: transcribe_chunks.sh <audio.m4a> <출력디렉터리> ["초기 프롬프트(고유명사 목록)"]
set -e
export PATH=/opt/homebrew/bin:$PATH
A="$1"; OUT="$2"; PROMPT="${3:-}"
CH=${CHUNK_SEC:-600}
mkdir -p "$OUT/chunks" "$OUT/tr"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$A" | cut -d. -f1)
i=0; s=0
while [ $s -lt $DUR ]; do
  n=$(printf %02d $i); f="$OUT/chunks/a$n.wav"
  [ -s "$f" ] || ffmpeg -y -v error -ss $s -t $CH -i "$A" -ac 1 -ar 16000 "$f"
  if [ ! -s "$OUT/tr/a$n.json" ]; then
    mlx_whisper "$f" --model mlx-community/whisper-large-v3-turbo --language ko --task transcribe \
      --output-dir "$OUT/tr" --output-format json --word-timestamps True --condition-on-previous-text False \
      --temperature 0 --hallucination-silence-threshold 2 ${PROMPT:+--initial-prompt "$PROMPT"} > "$OUT/tr/a$n.log" 2>&1
  fi
  echo "chunk $i done"; i=$((i+1)); s=$((s+CH))
done
echo RETRANS_DONE
