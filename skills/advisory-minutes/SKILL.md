---
name: advisory-minutes
description: 겟백 1:1 자문 세션(A 대표·B 원장)이 끝난 뒤 줌 녹화 전사록을 받아 노션 코칭 대시보드에 회의록을 올리고, 할 일 보드 등록·대시보드 문구 갱신·클라이언트 카톡 통보까지 처리할 때 읽을 것. "B 원장님 자문했어 노션에 올려줘", "자문 회의록 정리해줘" 같은 요청을 처리한다.
---

> **이 스킬이 시스템에 하는 일 (설치 전 확인)**
>
> - 전사록을 읽어 **노션 페이지를 생성·수정합니다.** 노션 API 키가 필요합니다.
> - 클라이언트에게 메신저 통보를 보내는 단계가 있습니다. 기본값은 발송 전 확인입니다.
> - DB ID는 플레이스홀더입니다. 본인 워크스페이스 값으로 바꿔야 합니다.

# 자문 회의록 파이프라인

밤밤의 1:1 자문 세션은 줌으로 하고, 기록 정본은 **노션 클라이언트별 코칭 대시보드**다. 세션이 끝나면 이 순서로 처리한다.

## 0. 먼저 읽을 것

- `~/Projects/getback/자문/CLAUDE.md` — 노션 ID 표, 대시보드 규칙, 톤, 회차 산정 기준(계약 회차 기준이며 로컬 파일명의 "N차미팅"과 다르다)
- 직전 회차 회의록 페이지 — 형식을 그대로 잇는다

⚠️ 대시보드는 **클라이언트에게 공유되는 페이지**다. 밤밤이 전달을 지시·승인한 것만 올린다. 밤밤의 내부 판단(수임료, 클라이언트 소속 병원과의 관계, 경쟁자 실명 해부, 협찬 부탁 같은 사담)은 회의록에서 걷어낸다.

## 1. 줌 전사록 받기

`~/Projects/getback/운영/pipeline/.env`의 `ZOOM_ACCOUNT_ID / ZOOM_CLIENT_ID / ZOOM_CLIENT_SECRET`(S2S OAuth).

```
POST https://zoom.us/oauth/token   grant_type=account_credentials&account_id=...
     Authorization: Basic base64(client_id:client_secret)
GET  https://api.zoom.us/v2/users/me/recordings?from=YYYY-MM-DD&to=YYYY-MM-DD
```

**⚠️ 가장 큰 함정 — 다운로드는 액세스 토큰이 따로다.** `download_url`에 일반 Bearer 토큰을 붙이면 `401 {"errorCode":124,"Forbidden"}`이 난다. 반드시:

```
GET https://api.zoom.us/v2/meetings/{URL인코딩된 uuid}/recordings?include_fields=download_access_token&ttl=3600
→ 응답의 download_access_token 을 download_url 뒤에 ?access_token=... 로 붙여서 curl -L
```

- 계정 표시명이 **"레코드 나우"**라 회의 제목만으로는 누구와 한 세션인지 알 수 없다. **전사록의 화자 이름으로 확인**한다.
- `start_time`은 UTC다. **한국 시각은 +9** — 밤 늦게 시작한 세션은 날짜가 하루 넘어간다(밤밤 자문은 자정 넘겨 시작하는 경우가 잦다). 회의록 날짜는 실제 시작 시각 기준으로 적고, 밤밤에게 한 줄로 알린다.
- VTT는 화자별로 잘게 쪼개져 있으니 같은 화자 연속 발화를 합쳐서 읽는다(96KB → 26KB로 줄어든다).
- 전사 품질 주의: 고유명사·숫자가 자주 깨진다. 숫자·비율은 회의록에 옮기기 전에 의심하고, 애매하면 밤밤에게 확인한다.
- 원본은 로컬 `~/Projects/getback/자문/클라이언트/{이름}/YYYY-MM-DD_N차미팅_전사록.txt|.vtt`로 저장한다.

## 2. 회의록 작성

`클라이언트/{이름}/`에 세션 노트 md를 먼저 쓰고(정본 소스), 그걸 노션에 올린다. 고정 형식:

```
> 📌 일시 YYYY.MM.DD(요일) HH:MM · 약 N분  |  참석 밤밤(자문) · {클라이언트}  |  주제 ... (N회차)
> 🎯 한 줄 결론 — ...
## 🎯 핵심 결론      (quote 한 문단)
## 🔑 핵심 논의 흐름  (굵은 소제목 + 불릿, 중요한 건 ⭐)
## ✅ 결정사항        (번호 목록)
## 📌 액션 아이템     (체크박스, (예지)/(밤밤) 담당 표기)
## 🗓️ 다음 단계
```

톤은 **프리미엄 존댓말**(밤밤 캐주얼 SNS체 아님). 밤밤의 발언을 클라이언트가 읽을 문장으로 다시 쓴다.

## 3. 노션에 올리기 — MCP 말고 REST

**⚠️ 노션 MCP `create-pages`는 숫자 프로퍼티를 문자열로 보내서 400을 낸다**(`Invalid number value for property 회차: 4`). 회차 같은 number 필드가 있으면 처음부터 REST API로 만든다.

토큰: `~/Projects/getback/운영/discord_bot/.env`의 `NOTION_TOKEN`(integration "claude", 이 페이지 트리에 공유됨).
`POST https://api.notion.com/v1/pages` + `Notion-Version: 2022-06-28`, 마크다운을 블록으로 변환해 `children`에 넣는다(quote / heading_2 / bulleted_list_item / numbered_list_item / to_do / paragraph, `**굵게**`는 annotations.bold). children은 요청당 100블록 제한.

DB ID는 `자문/CLAUDE.md` 표 참조. (B 원장: 회의록 `<NOTION_DB_ID>`, 할 일 `<NOTION_DB_ID>`, 대시보드 `<NOTION_DB_ID>`)

## 4. 이어지는 3가지

1. **할 일 보드**에 액션 아이템 등록 — 담당(고객/밤밤), 기한, 상태=할 일, ✅=false
2. **대시보드 상단 "🎯 지금 가장 먼저" quote**를 이번 회차 기준으로 교체 (노션 MCP `update-page` + `update_content` 검색치환이 편하다)
3. **작업물 DB**는 밤밤이 "전달했다"고 확인한 산출물만 등록 — 작업 중인 초안은 올리지 않는다

## 5. 클라이언트에게 카톡 통보

`kmsg`로 보낸다(줄바꿈 보존됨). 방 이름은 `kmsg chats --json`으로 확인 — B 원장님은 `B 원장 (겟백 5기 지원)`.

```
ssh -o BatchMode=yes localhost 'export PATH=/opt/homebrew/bin:$PATH; kmsg send "<방>" "<본문>"'
```

본문은 짧은 업무 확인체로. 회의록 링크는 `https://www.notion.so/<하이픈 없는 페이지 id>`.
**끝에 반드시 한 줄**: `— 이 메시지는 밤밤을 대신해 AI가 정리해서 보냈습니다`
보낸 뒤 `kmsg read "<방>" --limit 3`으로 실제 전송을 확인한다.
