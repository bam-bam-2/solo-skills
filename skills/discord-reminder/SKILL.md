---
name: discord-reminder
description: "일회성·반복 리마인더를 상시 구동 머신의 launchd/cron에 걸고 디스코드 DM으로 받는다. 유료 자동화 슬롯을 쓰지 않는 방법."
---

# Mac-mini Discord reminder

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
