---
name: discord-reminder
description: "일회성·반복 리마인더를 상시 구동 머신의 launchd/cron에 걸고 디스코드 DM으로 받는다. 유료 자동화 슬롯을 쓰지 않는 방법."
---

# Mac-mini Discord reminder

> **이 스킬이 시스템에 하는 일 (설치 전 확인)**
>
> - 사용자 홈에 실행 스크립트 하나(`~/Projects/<프로젝트>/<slug>.sh`, mode 700)를 만듭니다.
> - macOS **launchd 항목 하나**(`~/Library/LaunchAgents/com.bambam.reminder-<slug>.plist`)를 등록합니다.
> - **일회성 리마인더는 발송 직후 스스로 launchd에서 내려가고 plist를 지웁니다.** 상주하지 않습니다.
> - 반복 리마인더는 사용자가 지운 시점까지 유지됩니다. 목록은 `launchctl list | grep reminder`로 확인합니다.
> - 디스코드 토큰은 실행 시점에 `.env`에서만 읽고 출력하지 않습니다.
>
> 보안 스캐너는 이 동작을 `service_persistence`(영구 서비스 설치)로 분류합니다. 맞습니다. 다만 일회성 항목은 스스로 제거되고, 만드는 파일은 위 두 개뿐입니다.










Use the remote-host instead of Aside routine slots for scheduled reminders.

1. Resolve relative dates in Asia/Seoul and choose a concrete KST time. If the user gives no time, use 10:00 KST and state it.
2. Store the executable script at `~/Projects/<프로젝트>/<slug>.sh` on `remote-host` with mode `700`.
3. Load Discord credentials only at runtime from `~/Projects/<프로젝트>/discord_bot/.env`. Never print or copy token values.
4. Send the DM through Discord API v10 to `BAMBAM_USER_ID`. Include a non-empty `User-Agent` header to avoid Cloudflare blocking.
5. Store the LaunchAgent at `~/Library/LaunchAgents/com.bambam.reminder-<slug>.plist`.
   - One-time reminder: use `StartCalendarInterval` with `Year`, `Month`, `Day`, `Hour`, and `Minute`.
   - Recurring reminder: use only the requested recurring calendar fields.
   - **Never use `StartInterval` on this remote-host.** Verified 2026-08-16: every
     `StartInterval` LaunchAgent in the `gui/501` domain sits at
     `pended nondemand spawn = interval` and does not fire, including one that
     had previously run 2,429 times. `StartCalendarInterval` jobs fire normally.
     For an every-N-minutes job, list the minutes explicitly, e.g.
     `[{Minute: 0}, {Minute: 5}, ... {Minute: 55}]` for a 5-minute cadence.
6. Write stdout and stderr to `~/Projects/<프로젝트>/<slug>.log`.
7. Validate and load without firing the reminder immediately:
   - `plutil -lint <plist>`
   - `launchctl bootout gui/$(id -u)/<label>` if an old copy exists
   - `launchctl bootstrap gui/$(id -u) <plist>`
   - `launchctl print gui/$(id -u)/<label>`
   - `plutil -p <plist>` to verify the exact schedule
8. Confirm it actually fires. `launchctl print` showing the job loaded is not
   proof — watch `runs` increment across two scheduled ticks, or check the job's
   own log for two consecutive scheduled entries. A job can load cleanly and
   never spawn.
9. Do not test-send a real DM unless the user asks. Report the resolved date, time, timezone, delivery channel, and loaded label.

Use concise reminder text that says what happened, what the user should do next, and any account or product distinction needed to avoid a wrong action.

## 바로 쓰는 스크립트

[`scripts/make-reminder.sh`](scripts/make-reminder.sh) — 일회성 리마인더를 launchd에 등록합니다.

```bash
export DISCORD_BOT_TOKEN=... DISCORD_USER_ID=...
./scripts/make-reminder.sh cancel-check "2026-09-02 10:00" "구독 해지 확인하기"
```

지정한 시각에 DM이 한 번 가고 **잡이 스스로 내려갑니다.**
`StartInterval`이 아니라 `StartCalendarInterval`을 쓰는 이유는 아래 함정 항목을 보세요.
