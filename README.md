# solo-skills

**혼자 다 하는 사람을 위한 AI 에이전트 스킬 모음**

디자이너도 개발자도 마케터도 없이 혼자 일하면, 하루가 잡일로 다 갑니다.
제품 소개 영상 만들기, 전자책 PDF 뽑기, 블로그 글쓰기, 회의록 정리, 고객 카톡, 댓글 답글.

이 저장소는 커뮤니티를 6기까지 운영하면서 **실제로 매일 쓰는 스킬**을 정리한 것입니다.
개발자용 스킬 모음은 많은데, 혼자 사업하는 사람이 쓸 스킬은 잘 없어서 만들었습니다.

Claude Code, Codex, OpenCode 등 SKILL.md 규격을 읽는 에이전트에서 그대로 씁니다.

---

## 어떤 걸 할 수 있나

| 스킬 | 할 수 있는 일 | 준비물 |
| --- | --- | --- |
| [web-demo-video](skills/web-demo-video/) | 화면 녹화 없이 제품 데모 영상 만들기 (1:1 / 9:16 / 16:9) | ffmpeg |
| [book-pdf](skills/book-pdf/) | 마크다운 원고 → 진짜 책 같은 PDF·EPUB 전자책 | Node |
| [measured-ui-callouts](skills/measured-ui-callouts/) | 화면 캡처에 좌표 측정 기반 강조 박스 + 개인정보 모자이크 | 없음 |
| [naver-blog-post](skills/naver-blog-post/) | 네이버 블로그 검색 유입용 정보성 글 작성 | 없음 |
| [threads-reply](skills/threads-reply/) | 내 답글을 역산해 문체 기준표 만들고 댓글 답글 쓰기 | 없음 |
| [meeting-minutes](skills/meeting-minutes/) | 전사록 → 회의록 → 노션 등록 → 디스코드 공지 | 노션 토큰 |
| [kakaotalk-cli](skills/kakaotalk-cli/) | macOS 카카오톡 메시지 읽기·보내기 | macOS |
| [naver-mail](skills/naver-mail/) | 브라우저 없이 네이버 메일 읽기 (IMAP) | 네이버 계정 |
| [daangn-search](skills/daangn-search/) | 당근마켓을 구·시·전국 단위로 훑기 | 없음 |
| [daily-brief-bot](skills/daily-brief-bot/) | 매일 아침 관심 주제 아티클 요약을 디스코드로 받기 | 디스코드 봇 |
| [discord-agent-fleet](skills/discord-agent-fleet/) | 디스코드 상주 대화형 AI 봇 여러 개 만들고 운영하기 | 디스코드 봇 |
| [discord-reminder](skills/discord-reminder/) | 리마인더를 cron에 걸고 디스코드 DM으로 받기 | 상시 구동 머신 |
| [remote-offload](skills/remote-offload/) | 무거운 작업을 SSH로 보조 머신에 넘기기 | SSH |
| [multi-method-image-generation](skills/multi-method-image-generation/) | 가용한 모든 경로로 이미지 만들어 비교하기 | 선택 |
| [claude-codex-fallback](skills/claude-codex-fallback/) | 사용량 한도 걸리면 다른 CLI로 자동 재실행 | 선택 |

---

## 설치

저장소를 통째로 받아서 에이전트가 읽는 스킬 폴더에 넣습니다.

```bash
git clone https://github.com/bam-bam-2/solo-skills.git
```

**Claude Code**
```bash
mkdir -p ~/.claude/skills
cp -R solo-skills/skills/* ~/.claude/skills/
```

**프로젝트 단위로만 쓰고 싶다면**
```bash
mkdir -p .claude/skills
cp -R solo-skills/skills/* .claude/skills/
```

필요한 스킬만 골라서 복사해도 됩니다. 각 스킬은 서로 의존하지 않습니다.

```bash
cp -R solo-skills/skills/book-pdf ~/.claude/skills/
```

설치 후 에이전트에게 이렇게 말하면 됩니다.

> 이 마크다운 원고로 전자책 PDF 만들어줘

---

## 이 스킬들의 기준

**실제로 써본 것만 넣었습니다.** 직접 하다가 깨진 지점이 그대로 적혀 있습니다.

예를 들어 `web-demo-video`에는 이런 줄이 있습니다.

> 무대 페이지와 대상 사이트는 반드시 같은 오리진이어야 한다.
> 포트가 다르면 `iframe.contentDocument` 접근이 막혀서 조작이 불가능하다.

`kakaotalk-cli`에는 실패한 경로도 같이 적어뒀습니다. 한글은 `keystroke`로 넣으면 자모가 깨지고, SSH에서 `pbcopy`는 GUI 페이스트보드에 붙지 않습니다. 그래서 어떤 방법을 쓰는지까지 이유와 함께 있습니다.

**한국에서 일하는 사람 기준입니다.** 네이버 블로그, 카카오톡, 당근마켓, 스레드처럼 국내에서 실제로 쓰는 도구를 다룹니다.

---

## 기여

같은 문제를 다르게 푼 방법, 더 나은 절차, 깨진 부분 제보 모두 환영합니다.

- **스킬 제안·수정** → Pull Request
- **안 되는 것 제보** → Issue
- 새 스킬은 `skills/<이름>/SKILL.md` 한 파일이면 충분합니다. 형식은 기존 스킬을 참고하세요.

[CONTRIBUTING.md](CONTRIBUTING.md)에 작성 기준을 정리해뒀습니다.

---

## 만든 사람

안태현 (밤밤) — 커뮤니티 기획자. 관계자본 커뮤니티 [GET100](https://get100.co.kr)을 6기까지 운영하고 있습니다.

- 커뮤니티 운영, 콘텐츠 발행, 고객 응대, 제품 제작을 혼자 합니다
- 그래서 이 스킬들이 필요했습니다

문의나 제안은 Issue 또는 [get100.co.kr](https://get100.co.kr)로 주세요.

---

## 라이선스

[MIT](LICENSE) — 자유롭게 쓰고 고치고 재배포하셔도 됩니다.

---

혼자 일하시는 분께 하나라도 도움이 됐다면 ⭐ 눌러주세요.
