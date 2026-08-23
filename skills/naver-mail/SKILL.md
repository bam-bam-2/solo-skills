---
name: naver-mail
description: "네이버 메일을 브라우저 없이 IMAP으로 읽는다. 웹 세션이 만료돼 로그인 화면으로 튕길 때, 본문과 대용량 첨부까지 그대로 받아오는 우회 경로."
---

# 네이버 메일 IMAP 읽기

네이버 웹메일은 세션이 자주 만료되고, 만료되면 저장된 비밀번호가 없어 로그인 화면에서 막힌다.
**앱 비밀번호가 이미 `.env`에 있으므로 IMAP으로 바로 붙는 게 빠르다.**

## 바로 쓰는 스크립트

[`scripts/send_naver_mail.py`](scripts/send_naver_mail.py) — 네이버 SMTP 발송기입니다. 첨부파일을 지원합니다.

```bash
python scripts/send_naver_mail.py \
  --to someone@example.com --subject "제목" \
  --body-file body.txt --attach report.pdf
```

계정 정보는 코드에 넣지 말고 `.env`에 둡니다. 네이버는 **애플리케이션 비밀번호**를 따로 발급받아야 합니다.

## 자격증명 위치

```
~/Projects/<프로젝트>/운영/.env
~/Projects/<프로젝트>/운영/서초aict-웰커밍데이/.env
```
키 이름: `NAVER_MAIL_USER`, `NAVER_MAIL_APP_PASSWORD` (커뮤니티 레터 발송용으로 세팅된 것)

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

## 주의

- 읽기 전용으로 쓴다. 삭제·이동은 하지 않는다.
- 발송은 IMAP이 아니라 SMTP(`smtp.naver.com`)이며, 같은 `.env`에 `NAVER_SMTP_SERVER/PORT`가 있다.
  다만 스레드 문맥이 필요한 답장은 브라우저에서 "답장"으로 쓰는 편이 안전하다.
- 웹 로그인이 필요한 작업(메일 쓰기 UI, 설정 변경)은 여전히 사용자가 직접 로그인해야 한다.
