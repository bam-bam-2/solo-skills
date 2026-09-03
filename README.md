# solo-skills

### 1인 사업가 생산성 키트

[![stars](https://img.shields.io/github/stars/bam-bam-2/solo-skills?style=social)](https://github.com/bam-bam-2/solo-skills/stargazers)
[![license](https://img.shields.io/badge/license-MIT-black)](LICENSE)
[![follow](https://img.shields.io/github/followers/bam-bam-2?style=social&label=Follow)](https://github.com/bam-bam-2)

[English README](README.en.md)


**직원 없이 49개를 자동화했습니다.**

커뮤니티를 6기까지 운영하면서 제품 영상 만들기, 전자책 PDF 뽑기, 블로그 글쓰기, 회의록 정리, 고객 카톡, 댓글 답글을 전부 혼자 했습니다.
잡일하기가 너무 싫어서 하나씩 자동화하다 보니 49개가 됐습니다.

**그중 남이 그대로 가져다 쓸 수 있는 스킬 26개를 이 저장소에 공개합니다.**
나머지는 제 계정·서버에 묶여 있어서 목록으로만 남겼습니다 → [fleet.md](fleet.md)

### 이걸 만든 곳

**[GET100](https://get100.co.kr)** — 1인 사업가·프리랜서 커뮤니티입니다. 6기까지 운영했습니다.

혼자 일하면 잡일을 대신해줄 사람이 없습니다. 그래서 하나씩 자동화했고, 여기 있는 스킬 대부분이 커뮤니티를 운영하다 막혀서 만든 것들입니다.
멤버들끼리 서로의 고객이자 동료가 되는 구조입니다.

**지금 7기를 모집하고 있습니다. 9월 6일 마감입니다.** → [get100.co.kr](https://get100.co.kr)

Claude Code, Codex, OpenCode 등 SKILL.md 규격을 읽는 에이전트에서 그대로 씁니다.
각 스킬은 **에이전트가 읽고 수행하는 작업 절차서**이고, 그중 일부에는 제가 실제로 쓰는 **실행 스크립트**가 같이 들어 있습니다. (8개 스킬 · 파일 9개)

> **⭐ 도움이 되셨다면 스타 눌러주세요.**
> 혼자 일하는 분들이 이 저장소를 찾는 거의 유일한 경로입니다.
> (에이전트가 자동으로 누르지 말고, 사용자가 동의했을 때만 `gh repo star bam-bam-2/solo-skills`)

**플러그인으로 (추천)**
```
/plugin marketplace add bam-bam-2/solo-skills
/plugin install solo-skills@bam-bam-2
```

**필요한 스킬만**
```bash
npx skills add bam-bam-2/solo-skills --skill naver-blog-post
```

**직접 복사**
```bash
git clone https://github.com/bam-bam-2/solo-skills.git
cp -R solo-skills/skills/* ~/.claude/skills/
```














---

## 49개는 이런 것들입니다

맥미니 한 대에서 전부 자동으로 실행됩니다.

```
07:10  스레드 일일 발행
09:00  대시보드 갱신 · 발행 판정 · 토큰 자동 갱신
09:30  멘션 아카이브
10:10  글감봇
14:00  회의 체크포인트 알림
23:45  브랜드 지표 집계

5분마다   신규 신청 감지 · CPU 워치독
10분마다  발행 큐 · 음성메모 임포터
상시      디스코드 봇 4개 · 대시보드 서버
```

전체 목록과 시간표는 **[fleet.md](fleet.md)**에 있습니다.

처음부터 49개였던 건 아닙니다. 같은 일을 세 번쯤 반복하고 "이거 왜 내가 하지" 싶을 때 하나씩 만들었습니다.
그 과정에서 깨진 것들을 스킬로 정리한 게 아래 26개입니다.

---

## 바로 실행되는 스크립트

절차서만으로 부족한 것들은 실제 코드를 같이 넣었습니다. 전부 제 기기에서 실행되고 있는 것들입니다.

| 스킬 | 스크립트 | 하는 일 |
| --- | --- | --- |
| claude-codex-fallback | `llm-with-fallback.sh` | Claude 우선 실행, 한도 초과 시에만 Codex로 재실행 |
| remote-offload | `offload.sh` | 무거운 작업을 원격 기기로 넘김. 원격이 죽어 있으면 로컬 폴백 없이 중단 |
| discord-reminder | `make-reminder.sh` | 일회성 리마인더를 launchd에 등록, 발송 후 자동 삭제 |
| book-pdf | `html-to-pdf.py` | Paged.js 조판 HTML을 PDF로 굽기 |
| threads-reply | `publish-thread.mjs` | Threads 타래 발행. 기본 dry-run, `--go`로만 실제 발행 |
| naver-mail | `send_naver_mail.py` | 네이버 SMTP 발송, 첨부파일 지원 |

나머지는 실행 코드가 제 계정·서버에 묶여 있어서 절차와 함정만 정리했습니다.

---

## 공개한 스킬 26개

49개를 만들면서 쓴 절차 중, 남의 환경에서도 그대로 작동하는 것만 골랐습니다.

> **2일차 업데이트** — 반응이 좋아서 창고를 다시 뒤졌습니다. 스킬 폴더가 두 군데로 나뉘어 있었고, 처음엔 그중 한쪽만 공개했습니다. 나머지에서 공개 가능한 것을 추가했습니다. (Anthropic 공식 스킬과 겹치는 `skill-creator`·`slack-gif-creator`는 제 것이 아니라 제외했습니다.)


## 만들기 — 영상·전자책·이미지

### 🎬 web-demo-video — 화면 녹화 없이 제품 데모 영상

**무엇을 하나**
SNS에 올릴 제품 소개 영상을 만듭니다. 1:1(인스타·카톡), 9:16(릴스·쇼츠·스레드), 16:9(유튜브·랜딩) 세 비율 대응.

**어떻게 작동하나** — OBS도 화면 녹화도 쓰지 않습니다

1. 대상 사이트를 로컬 서버로 띄웁니다
2. "무대" 페이지를 만들고 그 안에 `<iframe>`으로 사이트를 넣습니다. 맥 브라우저 창 목업(신호등 3개 + URL 바) 안에 들어갑니다
3. 가짜 커서 SVG를 움직이면서 **진짜 클릭 이벤트를 iframe 내부에 쏩니다.** 클릭할 때 하이라이트 원이 퍼집니다
4. `window.__tick(프레임번호)` 함수 하나가 그 시점의 화면 상태를 만듭니다. **결정론적이라 몇 번을 다시 뽑아도 같은 영상이 나옵니다**
5. 프레임을 한 장씩 캡처해 ffmpeg로 합칩니다
6. 엔딩 카드(제품명 / 한 줄 설명 / 셀링포인트 3개 / URL)를 붙입니다

**함정**
무대 페이지와 대상 사이트는 **반드시 같은 오리진**이어야 합니다. 포트가 다르면 `iframe.contentDocument` 접근이 막혀서 조작 자체가 불가능합니다. 그래서 무대 파일을 프로젝트 폴더 안에 임시로 두고 끝나면 반드시 빼냅니다. 안 그러면 다음 배포에 딸려 올라갑니다.

**같이 들어있는 것** 무대 템플릿 HTML 2종
**필요한 것** ffmpeg
**에이전트에게** "이 사이트로 9:16 데모 영상 만들어줘"


### 📖 book-pdf — 마크다운을 진짜 책처럼

**무엇을 하나**
마크다운 원고를 실제 책처럼 보이는 PDF와 EPUB으로 만듭니다. 전자책을 팔려고 만들었습니다.

**들어가는 것**
표지 / 타이틀 페이지 / 판권(콜로폰) 페이지 / **실제 쪽번호가 박힌 목차** / 장마다 바뀌는 러닝헤더

**함정**
- 문단이 어중간하게 잘려 다음 페이지로 넘어가는 현상을 막는 규칙이 따로 있습니다
- **부·장 오프너에 flexbox를 쓰면 안 됩니다.** 페이지 분할 계산이 깨집니다

**필요한 것** Node, Paged.js
**에이전트에게** "이 원고로 전자책 PDF 만들어줘"


### 🖼 measured-ui-callouts — 좌표를 측정해서 강조 박스 얹기
[`measured-ui-callouts`](skills/measured-ui-callouts/)

강조 박스를 눈대중으로 그리지 않습니다. **대상 요소의 렌더링 좌표를 실제로 측정해서** 그 위치에 박스를 만듭니다.

개인정보(실명·주소·전화·결제 정보) 모자이크 체크리스트와, 제목이 캔버스 밖으로 잘리지 않았는지 확인하는 최종 검수 항목이 붙어 있습니다.

### 🎨 multi-method-image-generation — 모든 경로로 만들어 비교
[`multi-method-image-generation`](skills/multi-method-image-generation/)

이미지 생성 API, HTML·CSS 렌더링, 보유 사진, 기존 웹 자산을 전부 시도해서 나란히 놓고 고릅니다.

## 쓰고 발행하기 — 블로그·SNS

### ✍️ naver-blog-post — 검색으로 유입되는 글 쓰기
[`naver-blog-post`](skills/naver-blog-post/)

"완벽 가이드", "총정리", "꿀팁 Zip" 같은 제목은 금지입니다. 네이버가 낚시성 제목을 스팸으로 명시하고 있어서요.

대신 상위 노출 중인 글들을 먼저 측정하고, 롱테일 키워드를 제목 앞쪽에 배치하고, 분량과 이미지 개수를 실측 기준에 맞춥니다.

### 💬 threads-reply — 내 말투를 역산해서 답글 쓰기
[`threads-reply`](skills/threads-reply/)

문체를 감으로 정하지 않습니다. **내가 쓴 답글을 대량으로 긁어서 역산합니다.**

한 달치 한 줄 답글 492건을 실측했더니 느낌표 31% / 물음표 7.5%가 나왔고, 이전에 만들어둔 기준표(느낌표 11% / 물음표 22%)와 정반대였습니다. 그 낡은 표를 믿고 쓴 초안은 반려됐습니다. 그래서 **배치를 시작할 때마다 문체표를 다시 잰다**는 규칙이 들어 있습니다.

댓글과 답글을 짝으로 봐야 하는 이유, 통계만 맞추면 왜 훈수형 문장이 나오는지도 실패 기록으로 적어뒀습니다.

## 사람 상대하기 — 회의·메시지·메일

### 📝 meeting-minutes — 회의 끝나면 회의록이 올라가 있기

**무엇을 하나**
전사록을 넣으면 회의록으로 정리해 노션 DB에 등록하고 디스코드에 공지까지 합니다.

**사고 대응 절차가 같이 있습니다**
전사가 유실됐을 때 **지어내지 않습니다.** 회의록 상단에 "전사 유실 · 무엇을 근거로 썼는지"를 명시하고 참석자에게 보완을 요청합니다. 실제로 회의 본론이 통째로 날아간 적이 있어서 넣었습니다.

**유실이면 발행보다 사본 요청이 먼저입니다.** 주변 텍스트에 남는 건 회의 직후 후속 논의지 회의 그 자체가 아닙니다.

**외부 mp3 녹취를 받았을 때**
- 전사 프롬프트에 **고유명사를 미리 넣으면 정확도가 크게 오릅니다**(사람 이름, 공간명, 도메인 용어)
- 세그먼트 시작 시각에 녹음 시작 시각을 더해 **절대 시각**으로 바꿔 적으면 대조가 쉽습니다
- 개인 녹취는 화자 분리가 없습니다. 역할로 판별합니다
- 녹음 시작이 회의 시작보다 늦으면 **앞부분이 빠졌다고 명시**하고 물어봅니다

**필요한 것** 노션 토큰
**에이전트에게** "이 전사록으로 회의록 만들어서 올려줘"


### 📱 kakaotalk-cli — 맥에서 카카오톡 보내고 읽기

**막혔던 세 가지**
1. **한글을 `keystroke`로 넣으면 `ㅁㅁㅁ`으로 깨집니다**
2. **SSH로 들어가면 `pbcopy`가 GUI 페이스트보드에 안 붙습니다**
3. **화면에 렌더링되지 않은 채팅방은 목록에서 못 찾습니다.** 아래로 밀린 방이 안 잡힙니다

세 가지를 다 겪고 나서 찾은 경로가 적혀 있습니다.

**안전 규칙**
- 보내기 전 `--dry-run`으로 수신자 확인
- 처음 보내는 상대이거나 내용이 길면 **나에게 먼저 연습 발송**해서 서식 확인
- 단톡방은 특히 연습 발송 필수
- **AI가 대신 보낸 메시지에는 그렇다고 표시**합니다
- 메타데이터 재수집(`harvest`) 실행 금지 — 방 이름이 전부 `(unknown)`으로 덮어써진 사고가 있었습니다

**필요한 것** macOS, 카카오톡 앱, [kmsg](https://github.com/channprj/kmsg)
**에이전트에게** "○○님한테 카톡 보내줘"


### 📬 naver-mail — 브라우저 없이 네이버 메일 읽기
[`naver-mail`](skills/naver-mail/)

웹 세션이 만료돼 로그인 화면으로 튕길 때 IMAP으로 우회합니다. 본문과 대용량 첨부까지 그대로 받아옵니다.

## 봇 만들고 운영하기

### 🤖 daily-brief-bot — 매일 아침 관심 주제 브리핑
[`daily-brief-bot`](skills/daily-brief-bot/)

정해진 시각에 아티클을 모아 요약해서 디스코드로 보냅니다. 톤·길이·발송 시각을 나중에 조정하는 방법까지 포함.

### 🛠 discord-agent-fleet — 상주 봇 여러 개 운영하기
[`discord-agent-fleet`](skills/discord-agent-fleet/)

상시 구동 머신에서 대화형 봇을 여러 개 돌릴 때 밟는 함정을 정리했습니다. 절전 모드로 봇이 조용히 죽는 문제, 설정 파일이 자동 로딩되며 생기는 충돌, 사용량 한도 터졌을 때 대응까지.

### ⏰ discord-reminder — 리마인더를 cron에 걸고 DM으로 받기
[`discord-reminder`](skills/discord-reminder/)

유료 자동화 서비스의 슬롯을 쓰지 않고, 상시 구동 머신의 launchd/cron으로 처리합니다.

### 💻 remote-offload — 무거운 작업 다른 머신에 넘기기
[`remote-offload`](skills/remote-offload/)

저사양 노트북에서 에이전트를 실행하면 메모리가 계속 부족합니다. 스크래핑·인코딩·빌드·대량 API 수집은 SSH로 보조 머신에 던지는 패턴.

### 🔁 claude-codex-fallback — 한도 걸리면 다른 CLI로
[`claude-codex-fallback`](skills/claude-codex-fallback/)

자동화가 한도 때문에 멈추지 않게 하는 폴백.

## 물건 찾기

### 🥕 daangn-search — 당근을 구·시·전국 단위로
[`daangn-search`](skills/daangn-search/)

당근 웹 검색은 **동 하나로만** 됩니다. 그래서 넓게 찾으려면 지역코드를 순회해야 합니다. 대형가전이나 노트북처럼 한 동네에 매물이 없는 물건을 찾을 때 씁니다.

---

## 글 다듬기 — 문체·윤문

### 🧹 humanize-korean — AI가 쓴 한글을 사람 글로 되돌리기
`~가 아니라` 대조 구문, `여정`, `굴러가다` 같은 AI 특유의 표현을 잡아냅니다.

**제가 만든 게 아닙니다.** 뼈대는 한국 번역학계의 번역투 연구(이영옥 2001 이후 8대 유형)와
KatFish 정량 보고서의 지표를 가져와 세웠고, 제 경험은 그 위에 금지어 몇 개를 얹은 정도입니다.
학술 출처 전문은 [`references/scholarship.md`](skills/humanize-korean/references/scholarship.md)에 논문·연도·저널·페이지까지 그대로 적어뒀습니다.

### 🧬 voice-dna-creator — 문체를 수치로 뽑아내기
길이·줄바꿈·어미·인칭 분포를 재서, 다음 글을 그 범위 안에서 쓰게 합니다. 감으로 쓰다가 "네 문체가 아니다"라는 말을 듣고 만들었습니다.

### ✒️ style-skill-creator — 문체를 가르치는 스킬 만들기
특정 문체를 학습시키는 스킬 자체를 만들어냅니다.

## 모임 운영하기 — 회의·워크숍·행사

### 🗂 meeting-summary — 회의록에서 결정과 할 일만 남기기
요약이 아니라 **추출**입니다. 안건별 논의 과정은 버리고 "누가 언제까지 뭘"만 남깁니다.

### 🎓 workshop-prep — 워크숍 한 건 통째로 준비하기
커리큘럼 설계, 준비물, 당일 진행표까지 한 번에 나옵니다.

### 🎟 event-sales-script — 행사 판매 멘트 만들기
같은 행사라도 채널마다 톤이 달라야 해서, 채널별로 따로 뽑습니다.

### 🚀 community-launch — 커뮤니티 기수 열기
모집부터 온보딩까지의 절차입니다. 6기까지 운영하면서 굳어진 순서입니다.

## 에이전트 운영하기

### 🎛 orchestration — 여러 에이전트에 일 나눠 맡기기
일을 쪼개서 맡기고 결과를 다시 합치는 절차입니다.

### 🧰 harness — 전문 에이전트와 그 스킬까지 만들어내기
에이전트를 정의하면 그 에이전트가 쓸 스킬까지 같이 만들어주는 메타 스킬입니다.

### 🖱 computer-use — 화면 보고 직접 조작하기
API가 없는 프로그램을 다뤄야 할 때 씁니다.

### 🗑 notion-delete — 노션 페이지 안전하게 지우기
바로 지우지 않고 대상 목록을 먼저 보여준 뒤 확인받습니다. 잘못 지우면 되돌릴 수 없어서 이렇게 만들었습니다.



[전체 자동화 49개 보기 →](fleet.md)

---

## 설치 상세

```bash
git clone https://github.com/bam-bam-2/solo-skills.git
mkdir -p ~/.claude/skills
cp -R solo-skills/skills/* ~/.claude/skills/
```

프로젝트 단위로만 쓰려면 `.claude/skills/`에 넣으면 됩니다.
필요한 것만 골라 복사해도 됩니다. 스킬끼리 서로 의존하지 않습니다.

```bash
cp -R solo-skills/skills/book-pdf ~/.claude/skills/
```

설치 후 에이전트에게 이렇게 말하면 됩니다.

> 이 마크다운 원고로 전자책 PDF 만들어줘

---

## 이 키트의 기준

**실제로 써본 것만 넣었습니다.** 직접 하다가 깨진 지점이 그대로 적혀 있습니다.

성공한 방법만 적으면 다음 사람이 같은 데서 또 막힙니다. 그래서 실패한 경로와 그 이유를 같이 남겼습니다. 위에서 본 한글 자모 깨짐, 문체표 오판, 전사 유실 같은 것들이요.

**한국에서 일하는 사람 기준입니다.** 네이버 블로그, 카카오톡, 당근마켓, 스레드처럼 국내에서 실제로 쓰는 도구를 다룹니다.

---

## 크레딧

이 키트는 다른 분들이 만든 도구 위에 서 있습니다. 스킬은 그 도구를 **어떻게 쓰는지에 대한 문서**입니다.

| 도구 | 만든 곳 | 쓰는 스킬 |
| --- | --- | --- |
| [kmsg](https://github.com/channprj/kmsg) | channprj | kakaotalk-cli (발송·읽기 정본 도구) |
| [kakaocli](https://github.com/silver-flight-group/kakaocli) | silver-flight-group | kakaotalk-cli (DB 조회·발송 검증) |
| [Paged.js](https://pagedjs.org) | Paged.js | book-pdf (페이지네이션·목차·러닝헤더) |
| [ffmpeg](https://ffmpeg.org) | FFmpeg | web-demo-video (프레임 합성) |
| [Playwright](https://playwright.dev) | Microsoft | web-demo-video, daangn-search |
| Whisper | OpenAI | meeting-minutes (전사) |
| pandoc | John MacFarlane | book-pdf (마크다운 변환) |
| Puppeteer | Google | measured-ui-callouts (렌더링 측정) |

### 연구·자료 출처

문서로 된 지식도 남의 것을 가져온 게 있습니다.

| 스킬 | 가져온 것 |
| --- | --- |
| humanize-korean | **한국 번역학계 번역투 연구 8대 유형** (이영옥 2001 외 다수) + **KatFish 정량 보고서**의 수치 임계값. 분류 체계의 뼈대 자체가 여기서 왔습니다. 논문·연도·저널·페이지는 [`scholarship.md`](skills/humanize-korean/references/scholarship.md)에 원문 그대로 있습니다 |

내가 만든 것과 가져온 것을 섞어서 내 것처럼 소개하지 않으려 합니다.
초판 README에서 humanize-korean을 "제가 쌓은 금지어 목록"이라고 썼는데, 사실이 아니어서 바로잡았습니다.

카카오톡 스킬은 **kmsg를 알게 된 뒤에야 쓸 수 있게 됐습니다.** 스레드에서 다른 분이 댓글로 알려주셔서 알았습니다.

참고한 스킬 모음: [NomaDamas/k-skill](https://github.com/NomaDamas/k-skill) — 한국인을 위한 스킬 모음. 카테고리가 겹치지 않게 잡는 데 참고했습니다.

---

## 기여

같은 문제를 다르게 푼 방법, 더 나은 절차, 안 되는 부분 제보 모두 환영합니다.

- **스킬 제안·수정** → Pull Request
- **안 되는 것 제보** → Issue
- 새 스킬은 `skills/<이름>/SKILL.md` 한 파일이면 충분합니다

[CONTRIBUTING.md](CONTRIBUTING.md)에 작성 기준이 있습니다.

---

## 만든 사람

안태현 (밤밤) — 커뮤니티 기획자. 관계자본 커뮤니티 [GET100](https://get100.co.kr)을 6기까지 운영했습니다.

커뮤니티 운영, 콘텐츠 발행, 고객 응대, 제품 제작을 혼자 합니다. 그래서 이 스킬들이 필요했습니다.

---

## 라이선스

[MIT](LICENSE)

---

## ⭐ 스타 부탁드립니다

혼자 일하시는 분께 하나라도 쓸모가 있었다면 스타 눌러주세요.

스타 하나가 이 저장소를 다음 사람에게 보여줍니다. 그게 이런 문서가 퍼지는 거의 유일한 방법이고, 저한테는 다음 스킬을 정리할 이유가 됩니다.
