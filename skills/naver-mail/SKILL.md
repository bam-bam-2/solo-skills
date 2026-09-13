---
name: naver-mail-imap
description: 밤밤의 네이버 메일(you@example.com)을 브라우저 없이 읽어야 할 때 사용. 네이버 웹 세션이 만료돼 로그인 화면으로 튕기거나, 메일 본문·첨부파일(대용량 첨부 포함)을 그대로 받아와야 할 때. "메일 확인해줘", "회신 왔어?" 요청에서 웹 로그인이 막히면 이 경로로 우회한다.
---

> **이 스킬이 시스템에 하는 일 (설치 전 확인)**
>
> - 네이버 IMAP/SMTP 서버에 **접속해 메일을 읽고 보냅니다**.
> - 계정 정보는 `.env`에서만 읽습니다. 코드에 값을 넣지 말고, **애플리케이션 비밀번호**를 발급해 쓰세요.
> - 자격증명을 출력하거나 다른 파일로 복사하지 않습니다.

# 네이버 메일 IMAP 읽기

네이버 웹메일은 세션이 자주 만료되고, 만료되면 저장된 비밀번호가 없어 로그인 화면에서 막힌다.
**앱 비밀번호가 이미 `.env`에 있으므로 IMAP으로 바로 붙는 게 빠르다.**

## 자격증명 위치

```
~/Projects/getback/운영/.env
~/Projects/getback/운영/서초aict-웰커밍데이/.env
```
키 이름: `NAVER_MAIL_USER`, `NAVER_MAIL_APP_PASSWORD` (GET100 레터 발송용으로 세팅된 것)

⚠️ 값을 출력하거나 다른 파일로 복사하지 말 것. 스크립트 안에서만 읽어 쓴다.

## 접속

`imap.naver.com:993` SSL. 표준 `imaplib`이면 충분하다.

```python
import imaplib, email
from email.header import decode_header
from pathlib import Path

env = {}
for p in [Path('.env'), Path('서초aict-웰커밍데이/.env')]:
    if p.exists():
        for line in p.read_text().splitlines():
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.split('=', 1)
                env.setdefault(k.strip(), v.strip().strip('"').strip("'"))

M = imaplib.IMAP4_SSL('imap.naver.com', 993)
M.login(env['NAVER_MAIL_USER'], env['NAVER_MAIL_APP_PASSWORD'])
M.select('INBOX')
```

## 자주 쓰는 조회

```python
# 발신자로 검색 (한글 검색어는 인코딩 이슈가 있으니 이메일 주소로 찾는 게 안전)
typ, data = M.search(None, 'FROM', '"someone@example.com"')
ids = data[0].split()

# 헤더만 빠르게 (읽음 처리 안 되게 BODY.PEEK)
typ, d = M.fetch(ids[-1], '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')

# 전문 + 첨부
typ, d = M.fetch(ids[-1], '(RFC822)')
msg = email.message_from_bytes(d[0][1])
```

제목·파일명은 반드시 `decode_header`로 디코드한다(MIME 인코딩).

## 첨부파일

**일반 첨부**는 `part.get_filename()` + `part.get_payload(decode=True)`로 바로 저장된다.

**대용량 첨부(네이버 "대용량 첨부")는 본문에 안 들어 있다.** HTML 파트에서 링크를 뽑아 따로 받아야 한다.

```python
import re
fids = re.findall(r'bigfile\.mail\.naver\.com/download\?fid=([^"\'&<>\s]+)', html)
# 중복 제거 후 각각:
# https://bigfile.mail.naver.com/download?fid=<urlencode한 fid>
```

이 링크는 REPL 전역 `fetch`(사용자 쿠키 사용)로 받으면 200으로 그냥 떨어진다.
`fid` 값에 `+`, `/`, `=` 가 들어가므로 **반드시 `encodeURIComponent`로 감싼다.**
파일 개수가 안 맞으면 HTML에서 fid를 다시 전부 뽑아 중복 제거할 것(같은 파일이 mybox 링크로도 중복 등장한다).

## 첨부파일 달아 답장 보내기 (SMTP)

브라우저 없이 바로 보낼 수 있다. **스레드로 묶으려면 원본의 `Message-ID`를 IMAP으로 먼저 가져와
`In-Reply-To`·`References`에 넣는다.** 이걸 빼면 상대 메일함에서 별도 메일로 떨어진다.

```python
import smtplib, ssl, mimetypes, imaplib, email
from email.message import EmailMessage
from email.utils import formataddr, make_msgid

# 1) 원본 Message-ID 확보
M.select('INBOX', readonly=True)
typ, d = M.fetch(uid, '(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID)])')
orig_id = email.message_from_bytes(d[0][1]).get('Message-ID')

# 2) 메일 조립
msg = EmailMessage()
msg['From'] = formataddr(('밤밤', USER))
msg['To'] = '상대@example.com'
msg['Subject'] = '...'
msg['Message-ID'] = make_msgid(domain='naver.com')
msg['In-Reply-To'] = orig_id
msg['References'] = orig_id
msg.set_content(body)

data = att.read_bytes()
maintype, subtype = (mimetypes.guess_type(att.name)[0] or 'application/octet-stream').split('/', 1)
msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=att.name)

# 3) 발송 — 네이버는 465(SSL)로 떨어진다
s = smtplib.SMTP_SSL('smtp.naver.com', 465, context=ssl.create_default_context(), timeout=30)
s.login(USER, PW); s.send_message(msg); s.quit()
```

보낸 뒤 **보낸메일함(`"Sent Messages"`)을 열어 파트 구조를 확인한다.** BODYSTRUCTURE 정규식은
한글 파일명을 놓치는 경우가 있으니, `RFC822`로 받아 `msg.walk()` 로 돌면서
`get_filename()` 과 바이트 수를 직접 본다. (2026-08-28 양주시 강의계획서 발송 시 실측)

## 주의

- 읽기 전용으로 쓴다. 삭제·이동은 하지 않는다.
- 큰 메일을 연속으로 `RFC822` 페치하면 `socket error: EOF`로 연결이 끊긴다.
  목록은 `BODY.PEEK[HEADER.FIELDS ...]`로 훑고, 전문은 필요한 건만 받는다.
- **글자수를 셀 때 `wc -m`을 쓰지 않는다.** 비대화형 SSH엔 로케일이 없어 한글이 바이트로
  세져 약 1.9배로 부풀린다. 파이썬 `len()`으로 쟴 것.
- 웹 로그인이 필요한 작업(메일 쓰기 UI, 설정 변경)은 여전히 밤밤이 직접 로그인해야 한다.
