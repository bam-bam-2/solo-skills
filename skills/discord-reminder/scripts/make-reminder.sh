#!/bin/bash
# 일회성 리마인더를 launchd에 등록한다.
#
#   ./make-reminder.sh <이름> "2026-09-02 10:00" "보낼 메시지"
#
# 지정한 시각에 디스코드 DM이 한 번 발송되고, 잡은 스스로 정리된다.
# 필요한 것: DISCORD_BOT_TOKEN, DISCORD_USER_ID 환경변수
#
# ⚠️ 이 기기의 함정: StartInterval(N초마다)은 저전력 모드에서
# "pended nondemand spawn" 상태로 멈춘다. 반드시 StartCalendarInterval을 쓴다.

set -euo pipefail

NAME="${1:?이름을 지정하세요}"
WHEN="${2:?시각을 지정하세요 (예: \"2026-09-02 10:00\")}"
MSG="${3:?메시지를 지정하세요}"

: "${DISCORD_BOT_TOKEN:?DISCORD_BOT_TOKEN 환경변수 필요}"
: "${DISCORD_USER_ID:?DISCORD_USER_ID 환경변수 필요}"

DIR="$HOME/reminders"
mkdir -p "$DIR"

Y=$(date -j -f "%Y-%m-%d %H:%M" "$WHEN" "+%Y")
M=$(date -j -f "%Y-%m-%d %H:%M" "$WHEN" "+%-m")
D=$(date -j -f "%Y-%m-%d %H:%M" "$WHEN" "+%-d")
H=$(date -j -f "%Y-%m-%d %H:%M" "$WHEN" "+%-H")
MIN=$(date -j -f "%Y-%m-%d %H:%M" "$WHEN" "+%-M")

LABEL="reminder-$NAME"
SH="$DIR/$NAME.sh"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

cat > "$SH" <<SCRIPT
#!/bin/bash
# Cloudflare가 기본 curl UA를 막으므로 User-Agent를 반드시 넣는다.
DM=\$(curl -s -X POST "https://discord.com/api/v10/users/@me/channels" \\
  -H "Authorization: Bot \$DISCORD_BOT_TOKEN" \\
  -H "Content-Type: application/json" \\
  -H "User-Agent: DiscordBot (https://example.com, 1.0)" \\
  -d '{"recipient_id":"'"\$DISCORD_USER_ID"'"}' | sed -n 's/.*"id":"\([0-9]*\)".*/\1/p' | head -1)

curl -s -X POST "https://discord.com/api/v10/channels/\$DM/messages" \\
  -H "Authorization: Bot \$DISCORD_BOT_TOKEN" \\
  -H "Content-Type: application/json" \\
  -H "User-Agent: DiscordBot (https://example.com, 1.0)" \\
  -d "\$(printf '{"content":%s}' "\$(printf '%s' "$MSG" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')")"

# 한 번 쏘고 스스로 내린다
launchctl bootout "gui/\$(id -u)/$LABEL" 2>/dev/null || true
rm -f "$PLIST"
SCRIPT
chmod +x "$SH"

cat > "$PLIST" <<PLI
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>Label</key><string>$LABEL</string>
<key>ProgramArguments</key><array><string>/bin/bash</string><string>$SH</string></array>
<key>EnvironmentVariables</key><dict>
  <key>DISCORD_BOT_TOKEN</key><string>$DISCORD_BOT_TOKEN</string>
  <key>DISCORD_USER_ID</key><string>$DISCORD_USER_ID</string>
</dict>
<key>StartCalendarInterval</key><dict>
  <key>Year</key><integer>$Y</integer><key>Month</key><integer>$M</integer>
  <key>Day</key><integer>$D</integer><key>Hour</key><integer>$H</integer><key>Minute</key><integer>$MIN</integer>
</dict>
<key>StandardOutPath</key><string>$DIR/$NAME.log</string>
<key>StandardErrorPath</key><string>$DIR/$NAME.log</string>
</dict></plist>
PLI

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo "등록 완료: $LABEL"
echo "  발송 예정: $WHEN"
echo "  확인: launchctl print gui/$(id -u)/$LABEL | grep state"
