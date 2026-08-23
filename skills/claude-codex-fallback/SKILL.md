---
name: claude-codex-fallback
description: "CLI 자동화에서 기본 모델을 쓰다가 사용량 한도에 걸리면 다른 CLI로 자동 재실행하는 폴백을 구현한다."
---

# Claude 우선, Codex 조건부 폴백

1. 같은 프롬프트를 안전한 임시파일에 저장한다.
2. Claude Code를 먼저 실행한다. 자동화에 필요한 모델, 권한, 턴 상한을 기존 작업과 동일하게 유지한다.
3. Claude가 실패했을 때 stdout과 stderr에서 실제 사용량 한도 문구만 판별한다.
   - 예: `weekly limit`, `usage limit`, `hit your limit`, `limit ... resets`
   - 일반 네트워크 오류, 인증 오류, 파싱 오류, 단순 rate limit은 자동 모델 전환 근거로 쓰지 않는다.
4. 사용량 한도가 확정된 경우에만 같은 프롬프트를 Codex CLI로 한 번 재실행한다.
5. Codex도 실패하면 원래 오류와 폴백 오류를 함께 기록하고 정상 산출물처럼 발송하지 않는다.
6. 인증 토큰 값은 로그나 응답에 출력하지 않는다. Claude OAuth와 Codex ChatGPT 인증은 각 CLI의 기존 저장소를 사용한다.
7. 배포 전에 세 경로를 각각 검증한다.
   - Claude 정상 성공: Codex 미호출
   - Claude 사용량 한도: Codex 호출 및 성공
   - Claude 일반 오류: Codex 미호출
8. 실제 운영 환경에서 무발송 또는 읽기 전용 프롬프트로 한도 감지와 폴백 성공 로그를 확인한다.

## 바로 쓰는 스크립트

[`scripts/llm-with-fallback.sh`](scripts/llm-with-fallback.sh) — 실제로 매일 돌고 있는 실행기입니다.

```bash
echo "이번 주 지표 요약해줘" | ./scripts/llm-with-fallback.sh 80 opus
```

Claude를 먼저 쓰고, **사용량 한도 초과일 때만** 같은 프롬프트를 Codex로 재실행합니다.
프롬프트는 임시파일에 `chmod 600`으로 두고 종료 시 지웁니다.
