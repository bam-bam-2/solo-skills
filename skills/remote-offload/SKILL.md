---
name: remote-offload
description: "무거운 작업(스크래핑, 인코딩, 빌드, 대량 API 수집)을 SSH로 보조 머신에 넘긴다. 저사양 노트북에서 에이전트를 돌릴 때 메모리 부족을 피하는 패턴."
---

# 원격 머신 오프로딩

## 바로 쓰는 스크립트

[`scripts/offload.sh`](scripts/offload.sh) — 무거운 작업을 원격 기기로 넘깁니다.

```bash
./scripts/offload.sh "python heavy_scraper.py"
./scripts/offload.sh --dir ~/Projects/app "npm run build"
./scripts/offload.sh --bg "ffmpeg -i in.mov -c:v libx264 out.mp4"   # 백그라운드
```

원격이 죽어 있으면 **로컬로 폴백하지 않고 그냥 멈춥니다.** 메모리 부족으로 노트북이 죽는 걸 막기 위해서입니다.

## 왜

| | Aside 돌아가는 기기 | 오프로딩 대상 |
|---|---|---|
| 기기 | MacBook Air, Apple M1 | Mac mini, Apple M4 |
| 램 | **8 GB** (상시 부족, 압축 2.6GB / 여유 70MB 수준) | **16 GB** |
| 절전 | 사용자가 덮으면 멈춤 | `pmset sleep 0` — 안 잠듦 |
| 디스크 여유 | 200 GB | 54 GB |

맥북에어는 램이 모자라 크로미움이 백그라운드 탭을 강제 종료한다. 로컬에서 무거운 걸 돌리면
사용자의 탭이 죽는다. **무거운 건 원격 머신로 넘기는 게 기본값이다.**

## 접속

```bash
ssh remote-host          # Tailscale (REMOTE_IP) — 기본으로 이걸 쓴다
ssh remote-host-lan      # 같은 LAN일 때 (remote-host.local)
```

비대화형에서는 `-o BatchMode=yes -o ConnectTimeout=10`을 붙인다.
PATH가 필요한 명령(brew 설치물 등)은 `ssh remote-host 'bash -lc "..."'`로 로그인 셸을 태운다.

## 작업공간 규약

```
~/Projects/<프로젝트>/offload/
├── run.sh          러너 (아래 참조)
├── jobs/           실행할 스크립트를 여기로 scp
├── out/            산출물 (이미지, csv, json 등)
├── logs/           <JOB_ID>.log / .pid / .cmd.sh
└── node_modules/   playwright 설치됨
```

기존 프로젝트 작업은 `~/Projects/<repo>`에서 그대로 하고, 일회성 오프로딩만 여기를 쓴다.

## 판단 기준

**넘긴다**
- 헤드리스 스크래핑, 특히 여러 페이지 순회 (로그인 불필요한 공개 페이지)
- ffmpeg 인코딩, GIF 생성, 이미지 대량 변환
- `npm install`, `next build`, 대형 저장소 clone
- 대량 API 수집 (수백~수천 건 페이지네이션)
- 수십 MB 이상 파일 파싱/집계
- 30초 넘게 걸릴 것 같은 CPU 작업 전부
- 긴 문서/영상 스크립트 읽고 요약 (아래 `claude -p` 레시피)

**안 넘긴다**
- 사용자의 로그인 세션·쿠키가 필요한 브라우징 → Aside 브라우저에서 해야 함
- 사용자가 화면으로 확인해야 하는 UI 조작
- 몇 초 안에 끝나는 단순 조회 (ssh 왕복이 더 느림)
- 사용자 개인 파일이 맥북에어에만 있는 경우 (전송 비용 판단 후 결정)

## 표준 패턴: 스크립트를 보내서 실행

ssh + bash -lc + heredoc을 중첩하면 따옴표가 반드시 깨진다.
**로컬에 파일로 쓰고 scp로 보낸 뒤 실행한다.**

```bash
TMP=<세션 tmp 디렉토리>
cat > "$TMP/job.js" <<'EOF'
... 스크립트 ...
EOF
scp -q "$TMP/job.js" remote-host:~/Projects/<프로젝트>/offload/jobs/job.js
ssh remote-host 'cd ~/Projects/<프로젝트>/offload && node jobs/job.js'
```

## 긴 작업: run.sh

ssh 세션이 끊겨도 살아남아야 하는 작업은 러너로 띄운다.

```bash
R=~/Projects/<프로젝트>/offload/run.sh
ssh remote-host "$R start 'node jobs/scrape.js' scrape"   # -> JOB_ID=scrape-20260811-124757
ssh remote-host "$R status scrape-20260811-124757"        # running (pid=...) 또는 ### EXIT=0
ssh remote-host "$R tail   scrape-20260811-124757"        # 마지막 40줄
ssh remote-host "$R log    scrape-20260811-124757"        # 전체 로그
ssh remote-host "$R list"                                 # 최근 20개 작업
```

작업이 오래 걸리면 붙잡고 기다리지 말고, 그동안 로컬에서 다른 일을 하다가 `status`로 확인한다.

## 산출물 회수

```bash
scp remote-host:~/Projects/<프로젝트>/offload/out/result.csv <세션 artifacts 디렉토리>/
scp -r remote-host:~/Projects/<프로젝트>/offload/out/frames  <세션 tmp 디렉토리>/
```

사용자에게 보여줄 결과물은 artifacts 디렉토리로, 중간 확인용은 tmp로 가져온다.

## 레시피

### 헤드리스 브라우징 (playwright)

```js
const { chromium } = require('playwright');   // ~/Projects/<프로젝트>/offload 에서 실행
(async () => {
  const b = await chromium.launch({ headless: true });
  const p = await b.newPage();
  await p.goto(url, { waitUntil: 'domcontentloaded' });
  // ...
  await p.screenshot({ path: 'out/shot.png' });
  await b.close();
})();
```
워밍업 후 페이지 로드 0.3초 수준. 전역에 `puppeteer`도 있지만 playwright를 기본으로 쓴다.

### 미디어

`ffmpeg`는 `/opt/homebrew/bin/ffmpeg`. 인코딩·GIF 변환은 전부 원격 머신에서 한다.
`web-demo-video` 스킬의 프레임 합성 단계도 여기로 넘길 수 있다.

### 긴 문서 읽기를 CLI로 위임

메인 컨텍스트에 원문을 쌓지 않으면서 긴 자료를 요약할 때:

```bash
ssh remote-host 'bash -lc "cat ~/Projects/<프로젝트>/offload/jobs/doc.txt | claude -p --model claude-sonnet-4-5"'
```
사용량 한도가 걸리면 `claude-codex-fallback` 스킬의 판별 규칙을 따른다.
Codex CLI(`codex`)도 설치되어 있다.

## 설치된 도구

node v26 / npm 11 / python3.9 / uv / brew 6 / ffmpeg / rg / jq / git / gh 2.92 /
vercel / claude CLI 2.1 / codex CLI 0.147 / playwright(offload 로컬) / puppeteer(전역) /
Google Chrome

없는 게 필요하면 `ssh remote-host 'bash -lc "brew install <pkg>"'`로 설치하고 이 목록을 갱신한다.

## 주의

- 원격 머신는 이미 launchd 상주 작업이 여러 개 돈다 (`atlas-server`, `atlas-kakao-poll`,
  `threads-fetch`, `voicememoimporter`, 디스코드 채널 봇, 각종 리마인더). 코어를 다 쓰는
  작업을 걸기 전에 `run.sh list`와 `launchctl list | grep bambam`을 확인한다.
- 예약 실행(리마인더/크론)은 이 스킬이 아니라 `macmini-discord-reminder` 스킬을 따른다.
- 자격증명은 원격 머신에 있는 기존 `.env`에서 런타임에만 읽고, 값을 출력하지 않는다.
- 디스크 여유가 54GB뿐이다. 대용량 임시 파일은 작업 후 `out/`에서 정리한다.
- 파괴적 작업(대량 삭제 등)은 AGENTS.md의 안전 규칙을 그대로 적용한다.
