#!/bin/bash
# 무거운 작업을 원격 기기로 넘겨서 실행한다.
#
#   ./offload.sh "python heavy_scraper.py"
#   ./offload.sh --dir ~/Projects/myapp "npm run build"
#   ./offload.sh --bg "ffmpeg -i in.mov -c:v libx264 out.mp4"   # 백그라운드
#
# 노트북 메모리가 8GB라 스크래핑·인코딩·빌드를 돌리면 죽는다.
# 그런 작업은 전부 원격 기기로 넘긴다.
#
# 필요한 것: ~/.ssh/config 에 대상 호스트 등록 (기본값 REMOTE_HOST=mac-mini)

set -euo pipefail

HOST="${REMOTE_HOST:-mac-mini}"
WORKDIR=""
BG=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir) WORKDIR="$2"; shift 2 ;;
    --bg)  BG=1; shift ;;
    --host) HOST="$2"; shift 2 ;;
    *) break ;;
  esac
done

CMD="${1:?실행할 명령을 지정하세요}"

# 원격에 살아있는지 먼저 확인. 죽어있으면 로컬에서 돌리지 말고 그냥 멈춘다.
if ! ssh -o BatchMode=yes -o ConnectTimeout=10 "$HOST" 'echo ok' >/dev/null 2>&1; then
  echo "원격($HOST)에 접속할 수 없습니다. 로컬 실행은 메모리 부족으로 위험하니 중단합니다." >&2
  exit 1
fi

PREFIX=""
[[ -n "$WORKDIR" ]] && PREFIX="cd $WORKDIR && "

if [[ $BG -eq 1 ]]; then
  # 세션이 끊겨도 계속 돌게 nohup + 로그 파일
  LOG="/tmp/offload-$(date +%s).log"
  ssh -o BatchMode=yes "$HOST" "${PREFIX}nohup bash -lc '$CMD' > $LOG 2>&1 & echo \$!" \
    | sed "s/^/원격 PID: /"
  echo "로그: ssh $HOST 'tail -f $LOG'"
else
  # -l 로 로그인 셸을 써야 homebrew PATH가 잡힌다
  ssh -o BatchMode=yes "$HOST" "${PREFIX}bash -lc '$CMD'"
fi
