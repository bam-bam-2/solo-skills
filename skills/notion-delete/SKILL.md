---
name: notion-delete
description: "노션 페이지를 삭제(아카이브)한다. '노션에서 삭제해줘', '이 페이지 지워줘', '/notion-delete' 트리거. 페이지 ID 또는 노션 URL을 받아 Notion API로 즉시 아카이브."
type: user-invocable
---

# 노션 페이지 삭제 스킬

노션 MCP에 삭제 도구가 없어서 Notion API를 직접 호출하는 방식으로 구현.
페이지 ID 또는 URL을 받아 즉시 아카이브(휴지통으로 이동)한다.

## 실행 방법

```bash
python3 ~/.claude/skills/notion-delete/notion_archive.py "<page_id_or_url>"
```

여러 페이지 한번에:
```bash
python3 ~/.claude/skills/notion-delete/notion_archive.py "page_id_1" "page_id_2" "page_id_3"
```

## 토큰 탐색 순서

1. `NOTION_TOKEN` 환경변수
2. `~/Projects/getback/운영/pipeline/.env`
3. `~/Projects/getback/운영/discord_bot/.env`
4. `~/.env`

## 트리거 예시

- "스레드 #5 노션에서 삭제해줘"
- "이 페이지 지워: https://www.notion.so/..."
- "콘텐츠 DB에서 초안대기 빈 페이지들 다 삭제해줘"
- `/notion-delete`

## 주의사항

- 삭제 = 아카이브 (노션 휴지통으로 이동, 30일 내 복구 가능)
- 완전 영구삭제는 노션 앱에서 휴지통 비우기 필요
- DB 페이지 삭제 시 해당 DB 접근 권한 있어야 함
