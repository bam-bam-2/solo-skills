# 외부 서비스 감지 키워드

Phase 4.5에서 사용자 답변을 분석할 때 참조합니다.
실제 설정 가이드는 Phase 6에서 Context7로 실시간 조사하여 생성합니다.

---

## 연동 방식 결정 기준

**핵심 질문: 단방향인가, 양방향인가?**

| 패턴 | 설명 | 권장 방식 |
|------|------|----------|
| **단방향** | 발송, 업로드, 저장만 (출력) | 스크립트 |
| **양방향** | 읽기+쓰기, 검색+수정, CRUD | MCP |
| **CLI 존재** | gh, vercel 등 공식 CLI가 있음 | CLI |

**워크샵 인터뷰 시 추천 포함 질문**:
> "[현재 워크플로 요약]이니까, [추천 방식]으로 충분할 것 같아요! 맞죠?"

---

## 감지 키워드 → 서비스 매핑

### 이메일 & 커뮤니케이션

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| 이메일, 메일, Gmail, 지메일 | Gmail | 중간 | 스크립트 | `GMAIL_APP_PASSWORD` | 발송만 시. 검색/분류 필요시 MCP |
| 아웃룩, Outlook, 회사 메일, MS 메일 | Outlook (Microsoft 365) | 중간 | 스크립트 | `OUTLOOK_CLIENT_ID`, `OUTLOOK_CLIENT_SECRET` | 발송만 시 |
| 슬랙, Slack, 채널, 워크스페이스 | Slack | 중간 | 스크립트 | `SLACK_BOT_TOKEN` | 발송만 시. 검색 필요시 MCP |
| 디스코드, Discord, 서버 | Discord | 중간 | 스크립트 | `DISCORD_BOT_TOKEN` | 봇 메시지 발송 |
| 텔레그램, Telegram, 봇 | Telegram | 중간 | 스크립트 | `TELEGRAM_BOT_TOKEN` | 봇 메시지 발송 |
| 팀즈, Teams, MS Teams | Microsoft Teams | 중간 | 스크립트 | `TEAMS_WEBHOOK_URL` | 메시지 발송 |
| 카카오톡, 카톡, KakaoTalk | KakaoTalk | 어려움 | 스크립트 | `KAKAO_API_KEY`, `KAKAO_SENDER_KEY` | 알림톡 발송 |

### 파일 저장 & 문서

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| 드라이브, Drive, 구글 드라이브 | Google Drive | 중간 | 스크립트 | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | 업로드만 시. 검색/정리 필요시 MCP |
| 원드라이브, OneDrive, MS 드라이브 | OneDrive (Microsoft 365) | 중간 | 스크립트 | `ONEDRIVE_CLIENT_ID`, `ONEDRIVE_CLIENT_SECRET` | 업로드만 시 |
| 드롭박스, Dropbox | Dropbox | 쉬움 | 스크립트 | `DROPBOX_ACCESS_TOKEN` | 업로드만 시 |
| 노션, Notion, 페이지, 위키 | Notion | 쉬움 | **MCP** | `NOTION_API_KEY` | CRUD 많음, 페이지 탐색 |
| 컨플루언스, Confluence | Confluence | 중간 | 스크립트 | `CONFLUENCE_API_TOKEN`, `CONFLUENCE_DOMAIN` | 페이지 생성만 시 |
| 구글 독스, Google Docs, 문서 | Google Docs | 중간 | 스크립트 | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | 문서 생성만 시 |

### 일정 & 미팅

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| 캘린더, Calendar, 일정, 스케줄 | Google Calendar | 중간 | 스크립트 | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | 일정 생성만 시. 조회 필요시 MCP |
| 아웃룩 캘린더, Outlook Calendar | Outlook Calendar | 중간 | 스크립트 | `OUTLOOK_CLIENT_ID`, `OUTLOOK_CLIENT_SECRET` | 일정 생성만 시 |
| 줌, Zoom, 화상회의, 미팅, 녹화 | Zoom | 어려움 | 스크립트 | `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET` | 미팅 생성만 시 |
| 구글 밋, Google Meet, 미트 | Google Meet | 중간 | 스크립트 | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | 미팅 생성만 시 |

### 프로젝트 관리 & 이슈 트래킹

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| 리니어, Linear, 이슈, 티켓 | Linear | 쉬움 | **MCP** | `LINEAR_API_KEY` | 이미 MCP 있음, 복잡한 조합 |
| 지라, Jira, 스프린트 | Jira | 중간 | 스크립트 | `JIRA_API_TOKEN`, `JIRA_DOMAIN`, `JIRA_EMAIL` | 이슈 생성만 시. 스프린트 관리 MCP |
| 아사나, Asana, 태스크 | Asana | 쉬움 | 스크립트 | `ASANA_ACCESS_TOKEN` | 태스크 생성만 시 |
| 트렐로, Trello, 보드, 카드 | Trello | 쉬움 | 스크립트 | `TRELLO_API_KEY`, `TRELLO_TOKEN` | 카드 생성만 시 |
| 먼데이, Monday, monday.com | Monday.com | 쉬움 | 스크립트 | `MONDAY_API_KEY` | 아이템 생성만 시 |
| 클릭업, ClickUp | ClickUp | 쉬움 | 스크립트 | `CLICKUP_API_KEY` | 태스크 생성만 시 |

### 데이터 & 스프레드시트

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| 에어테이블, Airtable | Airtable | 쉬움 | **MCP** | `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID` | CRUD 필수, 양방향 |
| 구글 시트, Google Sheets, 스프레드시트 | Google Sheets | 중간 | **MCP** | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | CRUD 필수, 양방향 |
| 엑셀, Excel, MS 엑셀 | Excel (Microsoft 365) | 중간 | **MCP** | `ONEDRIVE_CLIENT_ID`, `ONEDRIVE_CLIENT_SECRET` | CRUD 필수, 양방향 |

### 개발 & 버전관리

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| 깃헙, GitHub, 레포, 커밋, PR | GitHub | 쉬움 | **CLI** | `GH_TOKEN` (선택) | `gh` CLI 사용, `gh auth login`으로 인증 |
| 깃랩, GitLab | GitLab | 쉬움 | **CLI** | `GITLAB_TOKEN` (선택) | `glab` CLI 사용 |
| 버셀, Vercel, 배포 | Vercel | 쉬움 | **CLI** | `VERCEL_TOKEN` (선택) | `vercel` CLI 사용 |

### 콘텐츠 & 미디어

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| 유튜브, YouTube, 영상, 비디오 | YouTube | 쉬움 | 스크립트 | `YOUTUBE_API_KEY` | 업로드만 시 |
| 피그마, Figma, 디자인 | Figma | 쉬움 | 스크립트 | `FIGMA_ACCESS_TOKEN` | 파일 정보 조회 |
| 캔바, Canva | Canva | 쉬움 | 스크립트 | `CANVA_API_KEY` | API 제한적 |

### 자동화 플랫폼

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| 재피어, Zapier, 자동화 | Zapier | 쉬움 | 스크립트 | `ZAPIER_WEBHOOK_URL` | 웹훅 트리거 |
| 메이크, Make, Integromat | Make | 쉬움 | 스크립트 | `MAKE_WEBHOOK_URL` | 웹훅 트리거 |
| n8n | n8n | 중간 | 스크립트 | `N8N_WEBHOOK_URL` | 웹훅 트리거 |

### AI & 외부 API

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| ChatGPT, GPT, OpenAI | OpenAI | 쉬움 | 스크립트 | `OPENAI_API_KEY` | API 호출 |
| 클로드, Claude, Anthropic | Anthropic | 쉬움 | 스크립트 | `ANTHROPIC_API_KEY` | API 호출 |
| 퍼플렉시티, Perplexity | Perplexity | 쉬움 | 스크립트 | `PERPLEXITY_API_KEY` | API 호출 |

### 데이터베이스

| 감지 키워드 | 서비스명 | 복잡도 | 권장 방식 | 환경변수 | 비고 |
|-------------|----------|--------|----------|----------|------|
| 수파베이스, Supabase | Supabase | 중간 | **MCP** | `SUPABASE_URL`, `SUPABASE_ANON_KEY` | CRUD 필수, 양방향 |
| 파이어베이스, Firebase | Firebase | 중간 | **MCP** | `FIREBASE_PROJECT_ID`, `FIREBASE_API_KEY` | CRUD 필수, 양방향 |
| 포스트그레스, PostgreSQL, DB | PostgreSQL | 어려움 | **MCP** | `DATABASE_URL` | CRUD 필수, 양방향 |

---

## 복잡도 기준

| 레벨 | 의미 | 예상 시간 | 사전 준비 |
|------|------|-----------|-----------|
| **쉬움** | API 키만 필요 | 10-15분 | 당일 가능 |
| **중간** | OAuth 설정 필요 | 20-30분 | 사전 권장 |
| **어려움** | 앱 등록 + 승인 필요 | 30-40분 | 사전 필수 |

---

## 권장 방식 요약

| 방식 | 서비스 |
|------|--------|
| **MCP** | Linear, Notion, Airtable, Sheets, Excel, Supabase, Firebase, PostgreSQL |
| **CLI** | GitHub (gh), GitLab (glab), Vercel (vercel) |
| **스크립트** | 나머지 (단방향 발송/업로드) |

---

## 환경변수 자동 설정

Phase 6에서 설계서 생성 시, 필요한 환경변수를 사용자에게 안내하고 자동으로 설정해줍니다.

### 워크플로우

1. **감지**: Phase 4.5에서 필요한 서비스 파악
2. **안내**: 필요한 환경변수 목록과 발급 방법 안내
3. **입력**: 사용자가 키 입력 (예: "슬랙 토큰은 xoxb-xxxx야")
4. **저장**: 스킬 폴더의 `.env` 파일에 자동 저장
5. **예시 생성**: `.env.example` 파일에 변수명만 기록 (배포용)

### 저장 위치

```
{스킬폴더}/
├── .env              # 실제 값 (gitignore)
├── .env.example      # 예시 형식 (배포용)
└── ...
```

### 안내 예시

```
이 스킬에는 Slack 연동이 필요해요!

📋 필요한 환경변수: SLACK_BOT_TOKEN

🔑 발급 방법:
1. https://api.slack.com/apps 접속
2. "Create New App" → "From scratch" 선택
3. Bot Token Scopes에 chat:write 추가
4. "Install to Workspace" 클릭
5. Bot User OAuth Token 복사 (xoxb-로 시작)

토큰을 알려주시면 제가 .env 파일에 설정해드릴게요!
```

### .env.example 형식

```bash
# Slack Bot Token
# 발급: https://api.slack.com/apps
SLACK_BOT_TOKEN=xoxb-your-token-here

# Notion API Key
# 발급: https://www.notion.so/my-integrations
NOTION_API_KEY=secret_your-key-here
```

---

## Phase 6에서의 가이드 생성

실제 설정 가이드는 Phase 6에서 다음 절차로 동적 생성:

1. **서비스 확정**: Phase 4.5에서 감지된 서비스 목록
2. **방식 결정**: 권장 방식 컬럼 참조 (MCP / CLI / 스크립트)
3. **Context7로 조사**: 방식에 맞는 설정 방법 검색
4. **가이드 생성**: 비개발자 친화적으로 정리하여 설계서에 포함

### 조사 프롬프트 (방식별)

**MCP 방식**:
```
"{서비스명} MCP 서버 설정 방법을 찾아줘.
- 설치 명령어
- 필요한 API 키/토큰 종류
- 인증 설정 단계
- 비개발자도 따라할 수 있게 정리"
```

**CLI 방식**:
```
"{CLI명} 설치 및 인증 방법을 찾아줘.
- 설치 명령어 (brew, npm 등)
- 로그인/인증 방법
- 기본 사용법"
```

**스크립트 방식**:
```
"{서비스명} API로 {작업} 하는 방법을 찾아줘.
- 필요한 API 키/토큰
- Python/Node.js 예시 코드
- 비개발자도 복붙해서 쓸 수 있게"
```
