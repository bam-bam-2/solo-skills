# 노션 에이전트 — Notion DB 세팅

Notion MCP 도구를 사용해 커뮤니티 운영에 필요한 DB를 생성한다.

---

## 생성할 DB 목록

### DB 1. 멤버 관리 DB

**Properties:**

| 속성명 | 타입 | 옵션 |
|--------|------|------|
| 이름 | title | |
| 기수 | select | 1기, 2기, 3기… |
| 상태 | select | 활성, 비활성, 수료 |
| 가입일 | date | |
| 결제 금액 | number | ₩ |
| 연락처 | text | |
| 신청서 링크 | url | |
| 메모 | text | |

### DB 2. 콘텐츠 캘린더 DB

**Properties:**

| 속성명 | 타입 | 옵션 |
|--------|------|------|
| 제목 | title | |
| 채널 | multi-select | 스레드, 카카오, 인스타, 디스코드 |
| 상태 | select | 초안, 검토중, 발행완료 |
| 발행일 | date | |
| 담당자 | person | |
| 내용 | text | |

### DB 3. 세션/활동 DB

**Properties:**

| 속성명 | 타입 | 옵션 |
|--------|------|------|
| 세션 이름 | title | |
| 날짜 | date | |
| 형태 | select | 줌 세션, 오프라인, 과제, 챌린지 |
| 참석자 수 | number | |
| 녹화 링크 | url | |
| 요약 | text | |

---

## 생성 방법

노션 MCP `notion-create-database` 도구 사용:

```
parent: 사용자가 제공한 페이지 ID 또는 워크스페이스
title: DB 이름
properties: 위 스키마 적용
```

노션 페이지 ID가 없으면 먼저 `notion-search`로 적절한 상위 페이지를 찾는다.

---

## 생성 후 확인사항

- [ ] 3개 DB 모두 생성 완료
- [ ] 각 DB에 샘플 행 1개씩 추가 (멤버: "테스트멤버", 콘텐츠: "테스트글", 세션: "OT")
- [ ] 생성된 DB URL 호스트에게 전달
