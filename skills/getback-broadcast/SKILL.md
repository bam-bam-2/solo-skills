---
name: getback-broadcast
description: 겟백(GET100) 커뮤니티 채널에 콘텐츠를 발행할 때 읽을 것 — 디스코드 공지(밤냥이 봇), 스레드 @get100.official 발행 큐, 카톡, 노션 운영본부 API 접근 경로.
---

> **이 스킬이 시스템에 하는 일 (설치 전 확인)**
>
> - **공개 채널에 글을 실제로 게시합니다.** 봇 토큰이 필요합니다.
> - 토큰은 환경변수·`.env`에서만 읽습니다. 스킬에는 값이 들어 있지 않습니다.
> - 게시 후 다시 읽어서 검증하는 단계가 포함돼 있습니다.

# 겟백 채널 발행 (getback-broadcast)

겟백 커뮤니티에 뭔가를 "뿌릴" 때의 검증된 경로. 인프라는 전부 mac-mini(SSH alias `mac-mini`)에 있다.

## 채널별 발행 방법

### 1. 디스코드 #공지 (밤냥이 봇 명의)

- 봇 토큰/채널 ID: mac-mini `~/Projects/getback/discord_bot/.env` (`DISCORD_TOKEN`, `CHANNEL_공지=<DISCORD_ID>`, `GUILD_ID=<DISCORD_ID>`)
- **함정: urllib 기본 User-Agent는 Cloudflare가 403(error code 1010)으로 차단.** 반드시 `User-Agent: DiscordBot (https://get100.co.kr, 1.0)` 헤더를 넣을 것.
- 멤버 멘션 롤: `<@&<DISCORD_ID>>` + `allowed_mentions: {"parse":["roles"]}`
- 공지 톤: 밤냥이 해요체, `**볼드 섹션 헤더**` + 절제된 이모지 1개, 서명 `— 운영진 (운영진)`. 과거 공지를 1~2개 읽고 톤 맞출 것.
- 게시 후 `GET /channels/{id}/messages?limit=1`로 반드시 검증.

### 1-b. 디스코드 DM + 파일 첨부 (밤떑이 봇 명의)

길드장·운영진 개인에게 자료(PDF 등)를 보낼 때. 카톡은 `kmsg`로 텍스트·이미지만 되고 **PDF는 못 보낸다** — 문서 전달은 디스코드 DM이 정답.

```js
// 1) DM 채널 생성 (상대 디스코드 유저 ID 필요 — 노션 길드 DB의 "길드장 디스코드 ID" 등)
POST /users/@me/channels  { recipient_id }
// 응답의 recipients[0].username 으로 대상을 반드시 검증할 것

// 2) multipart 로 본문 + 파일
const fd = new FormData();
fd.append('payload_json', JSON.stringify({ content: body }));
fd.append('files[0]', new Blob([buf], {type:'application/pdf'}), 'NAME.pdf');
POST /channels/{dmId}/messages   // headers 에 Authorization + User-Agent 둘 다
```

- **파일명은 ASCII로.** 한글 파일명을 넣으면 디스코드가 날려버린다(`네트워킹길드_긴급회의_0817.pdf` → `0817.pdf`).
- 사이즈 제한 8MB. 막 보낸 걸 고칠 때는 `DELETE /channels/{id}/messages/{msgId}` 후 재전송하되, 상대가 이미 읽었을 시간이면 지우지 말고 정정 메시지를 덧붙인다.
- 봇 명의라 AI임이 드러나므로 카톡용 AI 서명은 붙이지 않는다. 밤백 대신 전달할 땐 "밤백님이 ~하셨어요"로 주체를 분리해 쓴다.

### 2. 스레드 @get100.official (겟천 파이프라인)

- 큐 파일: mac-mini `~/Projects/getback/마케팅/threads-1000/queue.json`. 러너(launchd, 10분 간격)가 `status=pending` + `scheduled_at` 지난 항목을 자동 발행. **LLM 무관 순수 파이썬이라 큐에 올바른 스키마로 넣기만 하면 됨.**
- 항목 스키마: `id`(수동 주입은 `d{MMDD}-{NN}`), `scheduled_at`(KST ISO), `mode`("single"), `kind`(운영일지/뉴스 코멘터리/참여형 질문), `text`, `comment`(null), `images`([]), `status`("pending"), `permalink`/`published_at`/`error`(null), `created_at`, `fact_source`(근거 명시), `craft_experiment`(null)
- 발행 전 린트 필수: `/usr/bin/python3 ~/Projects/getback/운영/scripts/caption_lint.py --channel threads --kind text --file <파일>` (줄당 35자, em-dash 금지, 최상급·거래톤 금지, 멤버 실명 금지, 아라비아 숫자)
- 밤냥이 페르소나: 짧은 줄바꿈, 캐주얼 존대, 숫자는 결론이 아니라 경과로, 솔직한 build-in-public 톤. 최근 발행글 2~3개 읽고 맞출 것.
- 큐 쓰기는 tmp 파일 → `shutil.move`로 원자적으로. 발행 확인은 큐 재조회(`status`, `permalink`).

### 3. 카톡 단톡방/오픈채팅

- **전송 가능해짐 (2026-08-15).** `kmsg`를 `ssh localhost` 경유로 실행하면 방 이름만으로 발송된다. 한글·줄바꿈 보존. 절차는 `~/.aside/u/0/skills/user/kakaotalk-send/SKILL.md` 참고.
- 밤밤 명의로 나가므로 본문 끝에 `— 이 메시지는 밤밤을 대신해 AI가 정리해서 보냈습니다` 서명을 붙인다.
- (구정보) "KakaoTalk.app 깨짐"은 오진이었다. Aside 샌드박스가 GUI 실행·프로세스 조회를 막아서 생긴 착각이다.

### 4. 구독자 이메일 (네이버 SMTP, GET100 명의)

- 크리덤션: 맥북 `~/Projects/getback/.env`의 `NAVER_MAIL_USER`/`NAVER_MAIL_APP_PASSWORD`/`NAVER_SMTP_SERVER`/`NAVER_SMTP_PORT` (사이트 레포 `.env.local`은 베르셀 암호화 변수라 빈 값 — 쓰지 말 것). nodemailer 없으므로 python3 smtplib로 발송.
- 구독자 DB `<NOTION_DB_ID>` 읽기·쓰기는 맥미니 discord_bot의 `NOTION_TOKEN`으로 curl (Aside 노션 클라이언트 토큰은 이 DB에 401).
- 발송 후 반드시 해당 row 메모에 `[YYYY-MM-DD 어드민] … 발송` 마커 append (어드민의 발송/미발송 필이 이 마커를 읽음). 수신거부 링크는 `api/lead.js`의 `unsubUrl()` HMAC(기본값 시크릿)과 동일하게 생성.
- 톤: 담백한 확인·안내 ("신청 확인했습니다. 오픈하면 알려드릴게요"). 사람인 척 연출 금지, 서명은 "GET100 드림". 여러 명이면 무조건 1통씩 개별 발송. 실제 발송은 어드민 화면이 아니라 이 경로로 (밤밤 확정 원칙).

### 4-b. 기수 모집 대량 발송 (2026-08-26 실전 확립)

발송 스크립트: `mac-mini:~/Projects/getback/scripts/get100_letter_7gi.py` (레터), `get100_7gi_notify.py` (사전알림·리마인드).
둘 다 `--dry-run` 으로 대상부터 확인하고, `--preview-to <메일>` 로 실물 1통 받아본 뒤 발송한다.

**대상 선별 규칙 (구독자 DB `<NOTION_DB_ID>`)**
- **광고성 수신 동의 O + 구독 상태가 '수신 거부'/'반송' 아님** — 미동의자 발송은 정보통신망법 위반이다. 118명 중 동의자는 69명뿐이었다.
- 명단 구분 `뉴스레터 구독`만 보낼지, 동의자 전체로 확대할지는 **밤밤이 정한다**. DB 설명란의 "행사 신청자를 레터 명단에 섞지 말 것"은 정기 레터 기준이고, 모집 안내는 별도 판단이었다(2026-08-26에는 확대 선택).
- 수신 근거 문구를 대상에 맞춘다. 행사 신청자에게 "레터를 구독하신 분께"라고 쓰면 사실과 다르다 → "신청 과정에서 광고성 정보 수신에 동의하신 분께".
- 제목 앞에 **(광고)** 를 붙이고 본문에 수신거부 링크·문의처를 넣는다(법정 표기).

**반드시 걸리는 함정 두 개**
- **네이버 SMTP는 한 연결에서 명령이 많아지면 `452 Too many commands`로 끊는다.** 36통째에 끊겨 7명이 실패했다. **15통마다 `s.quit()` 후 재연결**하고, 실패 시에도 재연결 후 이어간다.
- **노션 메모 필드는 1,900자 상한.** 발송 마커를 메모에 append하는 방식은 이력이 긴 사람에게서 조용히 실패한다. 발송 후 반드시 **마커 개수와 보낸편지함 통수를 대조**한다.

**발송 후 검증 4종** — ① 스크립트 성공/실패 카운트 ② IMAP `Sent Messages` 수신자 대조(중복 없는지) ③ 노션 마커 개수 ④ 반송 스캔(`get100_bounce_watch.py`, 2시간마다 자동).

**중복 방지** — 노션 메모 마커로 건다. 사전알림 안내를 이미 받은 사람은 레터에서 자동 제외, 이미 신청서를 낸 사람은 리마인드에서 자동 제외(기수 신청 DB 이메일 대조).

**열람 추적** — `api/track.js` 가 이미 구현돼 있다. 오픈 픽셀 `<img src="https://get100.co.kr/api/track?e=<email>&t=<sig>&v=<호수>">`, 클릭은 같은 URL에 `&u=<대상URL>`. 서명은 수신거부와 동일한 `HMAC(UNSUB_SECRET, email)` 앞 20자. **오픈율은 이미지 차단 때문에 과소집계되니 클릭 수를 지표로 본다.**

### 4-c. 신청 즉시 알림 (2026-08-26 구축)

폼 접수 서버 `api/lead.js` 가 노션에 행을 쓰자마자 밤냥이 봇으로 밤밤에게 DM한다(제출→DM 1초). Vercel 환경변수 `DISCORD_TOKEN`·`BAMBAM_USER_ID` 사용.
맥미니의 `com.get100.notion-form-watch`(5분 폴러, 5개 DB 감시)는 백업으로 남아 있으므로, **즉시 DM에 성공하면 노션 행에 `[즉시알림 발송됨]` 마커를 남겨 폴러가 건너뛰게 한다.** 이 장치가 없으면 실제로 DM이 2통 간다.

⚠️ **모집 기수를 바꿀 때 두 곳을 같이 고친다** — `api/lead.js` 의 `CURRENT_COHORT` 와 `apply.html` 의 `<input type="hidden" name="cohort">`. 7기 모집 중에 기본값이 "6기"로 남아 있어 신청이 6기로 기록되던 버그가 있었다.

### 5. 노션 (운영본부 기록)

- Aside 노션 클라이언트의 쓰기(`addRow`/`addNew`)가 404로 실패할 수 있음 (2026-08-03 확인). 우회 2가지:
  - **디스코드 봇의 노션 통합 토큰** (mac-mini `.env`의 `NOTION_TOKEN`, 공식 API): Get100 운영본부 전체 접근 가능. 회의록 DB `<NOTION_DB_ID>`, 길드 DB `<NOTION_DB_ID>`, 길드 지원 이력 DB `<NOTION_DB_ID>`
  - **브라우저 UI + 합성 paste**: 본문은 `DataTransfer`에 text/html 담아 `new ClipboardEvent('paste', {clipboardData})` 디스패치 (시스템 클립보드는 샌드박스에서 pbcopy/osascript 모두 실패)

## 전파 내용 가공 원칙 (2026-08-03 확립)

- 운영진 회의 내용 중 멤버 전파는 **선별**한다: PM 보수·에어비앤비 재무·VIP 조율·전환율 진단 같은 운영진 전용 내용 제외. 제도 변경은 "폐지"가 아니라 멤버 입장에서 "새로 생기는 것"으로 프레이밍.
- 문안 톤 지적을 받으면 원안을 버리지 말고 수정안과 나란히 비교 제시 (feedback_tone_revision_keep_original).
