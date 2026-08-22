---
name: discord-agent-fleet
description: "디스코드에 상주하는 대화형 AI 봇을 여러 개 만들고 운영한다. 상시 구동 머신에서 겪는 함정(절전 모드, 설정파일 자동로딩, 사용량 한도)을 함께 정리했다."
---

# 원격 머신 에이전트 무리

사용자의 원격 머신(`ssh remote-host`)에 대화형 디스코드 봇이 셋 상주한다. 전부 같은 뼈대를 쓴다.

| 봇 | 폴더 | 아는 것 | launchd |
|---|---|---|---|
| 지식봇 | `~/Projects/<프로젝트>/` | 지식봇 8기수 기록 + 원자료 55개 | `com.bambam.daolab-agent` |
| 스터디봇 | `~/Projects/<프로젝트>/` | 지피터스 글 2,000건 + 지난 아티클 + 사용자 스킬·메모리 | `com.bambam.gpters-agent` |
| 커뮤니티봇 | `~/Projects/<프로젝트>/discord_bot/` | 커뮤니티 커뮤니티 운영(길드·슬래시명령 등) | `com.getback.bamnyangi` |

파이썬은 셋 다 `~/Projects/<프로젝트>/.venv/bin/python` 를 공유한다.
서버는 **ai공작실**(`1492202577700458797`) 하나. 허용 계정은 사용자 `483902030243692546`, 커뮤니티 `1407565803242520586`.

## 공통 뼈대

- `bot.py` — 디스코드 게이트웨이. DM은 전체 지식, 공개 채널은 멘션받을 때만
- `answer.py` — 인격+기억+자료를 조립해 LLM 호출
- `store.py` — 단기 대화를 SQLite 에 영구 저장 (재시작·재부팅에도 유지)
- `persona.md` — 인격·말투. **매 응답마다 읽으므로 고치면 재시작 없이 반영**
- `memory.md` — 장기기억. 응답에 `MEMORY:` 줄을 쓰면 자동 적립

기억이 두 층이라는 게 핵심이다. 단기(대명사 받기) + 장기(세션 끊어도 남는 사실).
`초기화`는 단기만 끊고 장기는 남긴다.

## ⚠️ 이 기기의 함정 세 가지

### 1. 저전력 모드가 KeepAlive 자동 재시작을 막는다

원격 머신에 `lowpowermode = 1` 이 켜져 있으면, 프로세스가 죽어도 launchd 가 되살리지 않는다.

```
state = not running
pended nondemand spawn = inefficient
```

"요청 없이 스스로 재기동하는 건 비효율적"이라며 **무기한 보류**한다. plist 에 `KeepAlive` 가 제대로 있어도 소용없고 `ProcessType` 을 바꿔도 안 통한다. 40초를 기다려도 안 풀리는 걸 실측했다.

- **배포·재시작할 때는 항상 `launchctl kickstart -k` 를 명시적으로 쓴다.** `bootstrap` 만으로는 프로세스가 안 뜬다. kickstart 는 명시적 요청이라 보류 정책을 우회한다.
- 근본 해결은 `sudo pmset -a lowpowermode 0` 인데 비번 없는 sudo 가 안 걸려 있어 SSH 로는 못 한다. 사용자가 직접 쳐야 한다.
- 이건 지식봇만의 문제가 아니라 **이 기기의 모든 launchd 상주 작업에 적용된다.**

### 2. CLAUDE.md 가 모든 CLI 호출에 자동으로 딸려간다

`claude` CLI 는 실행 디렉터리에 `CLAUDE.md` 가 없으면 **상위 폴더로 거슬러 올라가며 찾아서** 프롬프트에 넣는다.

커뮤니티봇가 호출당 14만 토큰을 쓰던 원인이 이거였다. 밤집사가 실제로 만드는 프롬프트는 4,766자인데, `discord_bot/` 한 칸 위의 `~/Projects/<프로젝트>/CLAUDE.md`(당시 170KB)가 매번 통째로 붙고 있었다. 2026-08-16 에 밤알바생·옛 작업이력을 `docs/CLAUDE-archive-*.md` 로 옮겨 **1만 4천 자(92% 감소)** 로 줄였다.

- 새 봇을 만들 때는 `subprocess` 에 **`cwd` 를 그 봇 폴더로 고정**하고, 그 폴더에 큰 `CLAUDE.md` 를 두지 않는다
- 토큰이 예상보다 크면 **프롬프트 코드부터 의심하지 말고 상위 폴더의 CLAUDE.md 크기를 먼저 재라**
- `~/.claude/CLAUDE.md`(전역, 약 5KB)는 항상 붙는다. 이건 어쩔 수 없다

### 3. launchd PATH 에는 homebrew 가 없다 — 절대경로만으론 부족하다

launchd 는 PATH 를 `/usr/bin:/bin:/usr/sbin:/sbin` 으로만 준다. 그래서 CLI 를 절대경로로 불러도, **그 CLI 자체가 node 스크립트면 죽는다.**

```
Codex rc=127: env: node: No such file or directory
```

`codex` 는 `/opt/homebrew/lib/node_modules/@openai/codex/bin/codex.js` 로 가는 심링크이고 셔뱅이 `#!/usr/bin/env node` 다. PATH 에 `/opt/homebrew/bin` 이 없으면 node 를 못 찾는다. `claude` 는 네이티브 Mach-O 바이너리라 이 문제가 없다 — **그래서 claude 는 멀쩡한데 codex 폴백만 조용히 죽어 있는 상태가 만들어진다.** 2026-08-16 프로젝트 조사봇이 주간 한도에 걸렸을 때 폴백도 같이 실패해 15시간 리포트가 끊긴 원인이 이거였다.

두 겹으로 막는다.

1. **plist 에 PATH 를 박는다** (근본)
   ```xml
   <key>EnvironmentVariables</key>
   <dict>
     <key>PATH</key>
     <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
   </dict>
   ```
2. **스크립트에서도 env 를 보강한다** (수동 실행 대비). `subprocess.run(..., env=_tool_env())` 로 `/opt/homebrew/bin` 을 PATH 앞에 끼운다.

**진단 코드도 같이 봐라.** `subprocess.run` 은 셔뱅 실패(rc=127)에 예외를 안 던진다. `try/except` 만으로 점검하면 **죽은 CLI 를 OK 로 찍는다.** 프로젝트 조사봇 `--check` 가 정확히 이 버그였고, 그래서 폴백이 몇 달 고장난 걸 아무도 몰랐다. 반드시 `returncode` 를 확인할 것.

검증은 launchd 환경을 재현해서 한다.
```bash
ssh remote-host 'cd ~/ops/<봇> && env -i HOME=$HOME PATH=/usr/bin:/bin:/usr/sbin:/sbin /opt/homebrew/bin/python3 followup.py --check'
```

## LLM 호출은 구독으로만

**API 키(`ANTHROPIC_API_KEY`)를 쓰지 않는다.** 사용자가 명시적으로 금지했다.
`~/Projects/<프로젝트>/agents/llm_cli.py` 가 공용 호출 모듈이다. `claude -p --output-format text` 를 stdin 으로 부르고, `CLAUDE_CODE_OAUTH_TOKEN` 을 넘긴다. PATH 가 없는 launchd 환경 대비로 `/opt/homebrew/bin/claude` 하드코딩 폴백이 있다.

사용량 한도(`weekly limit`) 문구가 나올 때만 Codex 로 한 번 재실행한다. 일반 오류로는 넘어가지 않는다. 자세한 규칙은 `claude-codex-fallback` 스킬.

모델은 `--model` 을 안 줘서 CLI 기본값(2026-08 기준 `claude-sonnet-5`)을 쓴다. 고정하려면 `--model sonnet|opus|fable`.

## 자주 하는 일

```bash
# 상태
ssh remote-host 'for S in com.bambam.daolab-agent com.bambam.gpters-agent com.getback.bamnyangi; do echo "=== $S ==="; launchctl print gui/$(id -u)/$S 2>/dev/null | grep -iE "^\s+(state|pid) "; done'

# 재시작 (kickstart 필수)
ssh remote-host 'launchctl kickstart -k gui/$(id -u)/com.bambam.daolab-agent'

# 로그 — 실제 로그는 bot.error.log 에 쌓인다 (bot.log 는 비어있는 경우가 많다)
ssh remote-host 'tail -30 ~/Projects/<프로젝트>/bot.error.log'

# 디스코드 안 거치고 답변 엔진만 시험
ssh remote-host 'cd ~/Projects/<프로젝트> && set -a && . ./.env && set +a && ~/Projects/<프로젝트>/.venv/bin/python answer.py "질문"'
```

**코드는 로컬에서 쓰고 `scp` 로 보낸다.** 히어독으로 원격에 파이썬을 직접 쓰면 따옴표·한글 이스케이프가 깨진다(실제로 깨졌다).

## 새 봇을 만들 때

`daolab-agent` 를 통째로 복사하고 `answer.py` 의 지식 소스만 바꾸는 게 가장 빠르다. `store.py`·`bot.py`·`persona.md` 는 거의 그대로 간다.

만들기 전에 확인할 것:
- **어느 계정으로 DM 하는가** — 봇은 자기와 같은 서버에 있는 사람하고만 DM 이 열린다
- **공개 채널에도 둘 것인가** — 그렇다면 지식 범위를 나눈다. 지식봇은 DM 에선 사용자판(대외비 포함), 채널에선 지식봇판(내부 데이터 없음)을 쓴다. 규칙으로 막지 말고 **자료를 안 주는 방식**으로 분리한다
- **봇끼리 무한루프** — 사람이 안 끼어든 연속 봇 응답이 3회 넘으면 침묵하게 한다
- 응답에 식별 접두어를 붙인다(`📓 [지식봇]` 등)
- `allowed_mentions=discord.AllowedMentions.none()` 로 멘션 사고를 막는다
