#!/bin/bash
# LLM 실행기 (Claude 우선, 한도 초과 시 Codex 폴백)
# Claude Code를 우선 사용하고, 계정 사용량 한도 초과일 때만 Codex로 같은 프롬프트를 재실행한다.

export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
MAX_TURNS="${1:-80}"
CLAUDE_MODEL="${2:-opus}"
CLAUDE_BIN="${CLAUDE_BIN:-/opt/homebrew/bin/claude}"
CODEX_BIN="${CODEX_BIN:-/opt/homebrew/bin/codex}"
TOKEN_FILE="${CLAUDE_OAUTH_TOKEN_FILE:-$HOME/.config/llm/claude-oauth-token}"

PROMPT_FILE=$(mktemp)
CLAUDE_OUT=$(mktemp)
CLAUDE_ERR=$(mktemp)
cleanup() { rm -f "$PROMPT_FILE" "$CLAUDE_OUT" "$CLAUDE_ERR"; }
trap cleanup EXIT
chmod 600 "$PROMPT_FILE" "$CLAUDE_OUT" "$CLAUDE_ERR"
cat > "$PROMPT_FILE"

if [ -s "$TOKEN_FILE" ]; then
  export CLAUDE_CODE_OAUTH_TOKEN="$(cat "$TOKEN_FILE")"
fi

"$CLAUDE_BIN" -p "$(cat "$PROMPT_FILE")" \
  --model "$CLAUDE_MODEL" \
  --dangerously-skip-permissions \
  --max-turns "$MAX_TURNS" \
  >"$CLAUDE_OUT" 2>"$CLAUDE_ERR"
CLAUDE_RC=$?

# 단순 네트워크·인증 오류에는 모델을 바꾸지 않는다. 실제 사용량 한도 문구만 폴백한다.
if [ "$CLAUDE_RC" -ne 0 ] && grep -qiE \
  "weekly limit|usage limit|hit your (weekly )?limit|limit.*resets|resets.*Asia/Seoul" \
  "$CLAUDE_OUT" "$CLAUDE_ERR"; then
  echo "[llm-fallback] Claude 한도 감지 → Codex 전환" >&2
  "$CODEX_BIN" exec --dangerously-bypass-approvals-and-sandbox < "$PROMPT_FILE"
  exit $?
fi

cat "$CLAUDE_OUT"
cat "$CLAUDE_ERR" >&2
exit "$CLAUDE_RC"
