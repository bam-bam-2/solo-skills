---
name: iphone-sms-read
description: 밤밤의 아이폰 문자·아이메시지를 읽을 때 읽을 것. "문자 확인해줘", "○○한테 문자 왔어?", "인증번호 뭐야", "문자에서 찾아줘" 같은 요청을 처리한다. 읽기 전용이며 발송 기능은 없다.
---

> **이 스킬이 시스템에 하는 일 (설치 전 확인)**
>
> - **macOS 전용**이고 아이폰 문자 동기화가 켜져 있어야 합니다.
> - 로컬 메시지 DB(`~/Library/Messages/chat.db`)를 **읽습니다.** 전체 디스크 접근 권한이 필요합니다.
> - **읽기 전용입니다. 발송 기능이 없습니다.**
> - 메시지를 외부로 전송하지 않습니다. 전부 로컬에서 처리됩니다.

# 아이폰 문자 읽기

**정본 도구는 `~/bin/imsg`다.** 맥 메시지 앱이 아이폰과 동기화한
`~/Library/Messages/chat.db`를 읽기 전용으로 조회한다. 아이폰 문자 전달이 켜져 있어
SMS·RCS·iMessage가 모두 들어온다(2026-08-28 기준 SMS 24,034건, iMessage 1,976건).

## 반드시 SSH 루프백으로 실행할 것

`chat.db`는 TCC 보호 대상이라 Aside 샌드박스 안에서는 열리지 않는다.

```bash
# 샌드박스 안 → 실패
~/bin/imsg recent
# chat.db를 열 수 없습니다 (unable to open database file)

# SSH 루프백 → 성공
ssh -o BatchMode=yes localhost '~/bin/imsg recent -n 10'
```

`sshd`가 전체 디스크 접근 권한을 이미 갖고 있어서 루프백으로 나가면 읽힌다.
음성메모 파이프라인·카톡(`kmsg`)과 같은 구조다.

SSH 세션의 PATH에는 `~/bin`이 없다. **절대경로 `~/bin/imsg`로 호출**하거나
`export PATH=$HOME/bin:$PATH`를 앞에 붙인다.

## 명령

```bash
ssh localhost '~/bin/imsg recent -n 20'          # 최근 메시지
ssh localhost '~/bin/imsg chats -n 20'           # 최근 대화 상대 (건수 포함)
ssh localhost '~/bin/imsg read 포말 -n 30'        # 특정 상대와의 대화
ssh localhost '~/bin/imsg search 계약 -n 20'      # 본문 검색
ssh localhost '~/bin/imsg code -n 5 --days 3'    # 인증번호만 추출
```

공통 옵션: `--json` `--days N` `--me`(내가 보낸 것만) `--them`(받은 것만)

옵션은 서브커맨드 뒤에 붙여도 된다.

## 인증번호 추출

로그인·본인확인 중 문자 인증이 필요할 때 쓴다. 실측으로 국세청·당근페이·결제선생
문자에서 정확히 뽑는 것을 확인했다.

추출 우선순위는 대괄호 안 숫자 → "인증번호 XXXX" 패턴 → code/OTP 패턴 순이고,
그래도 없으면 6자리·4자리 순으로 고른다. 연도(20XX)와 휴대폰번호는 후보에서 제외한다.
`상품명·주문·배송·결제금액` 같은 단어가 있으면 광고로 보고 건너뛴다.

## 구현 메모

- 최신 macOS는 본문을 `message.text`에 넣지 않고 `attributedBody`(NSKeyedArchiver
  typedstream)에만 넣는 경우가 많다(최근 500건 중 298건). `pytypedstream`으로
  디코딩하고, 실패하면 `NSString` 마커 기반 휴리스틱으로 폴백한다.
- 시각은 Apple epoch(2001-01-01 기준 나노초)라 `date/1e9 + 978307200`으로 변환한다.
- 연락처 이름은 주소록
  `~/Library/Application Support/AddressBook/Sources/*/AddressBook-v22.abcddb`의
  `ZABCDPHONENUMBER` + `ZABCDRECORD`에서 가져온다. 번호는 `+82` → `0` 정규화 후
  뒤 10자리로 매칭한다.
- 파이썬 인터프리터는 `/Users/mac/Projects/getback/.venv/bin/python`을 shebang으로
  쓴다(`pytypedstream`이 여기 설치돼 있다).

## 하지 말 것

- **`chat.db`에 쓰기 금지.** 항상 `mode=ro`로 연다. 메시지 앱이 동시에 쓰고 있어
  잠금 충돌이나 손상 위험이 있다.
- **문자 내용을 대화창에 통째로 출력하지 말 것.** 금융·인증·개인 대화가 섞여 있다.
  필요한 건만 골라서 보여주고, 번호는 마스킹한다.
- 발송 기능은 없다. 문자 보내기는 지원하지 않는다(카톡은 `kakaotalk-send` 스킬).

## 참고

- 카톡 읽기·보내기: `kakaotalk-send` 스킬
- 같은 TCC/SSH 루프백 구조: `~/.aside/u/0/memory/agent/mac-mini-voice-memo-pipeline.md`
