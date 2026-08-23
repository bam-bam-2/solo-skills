"""네이버 SMTP로 메일 발송 (첨부파일 지원).

사용:
    python send_naver_mail.py \
        --to someone@example.com \
        --subject "제목" \
        --body-file body.txt \
        --attach file1.pdf --attach file2.pdf

또는 코드에서 직접:
    from send_naver_mail import send
    send(to=..., subject=..., body=..., attachments=[...])
"""
from __future__ import annotations
import argparse, os, smtplib, ssl, sys
from email.message import EmailMessage
from pathlib import Path


def load_env(path: Path):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip().lstrip("\ufeff")
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def send(to: list[str] | str, subject: str, body: str,
         attachments: list[Path] | None = None,
         cc: list[str] | None = None,
         html: bool = False):
    load_env(Path(__file__).resolve().parent.parent / ".env")

    user = os.environ["NAVER_MAIL_USER"]
    pw = os.environ["NAVER_MAIL_APP_PASSWORD"]
    server = os.environ.get("NAVER_SMTP_SERVER", "smtp.naver.com")
    port = int(os.environ.get("NAVER_SMTP_PORT", "465"))

    if isinstance(to, str):
        to = [to]

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    msg["Subject"] = subject
    if html:
        msg.set_content("HTML 메일입니다. HTML을 지원하는 클라이언트에서 열어주세요.")
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)

    for a in attachments or []:
        p = Path(a)
        data = p.read_bytes()
        # guess mime
        ext = p.suffix.lower()
        maintype, subtype = {
            ".pdf": ("application", "pdf"),
            ".png": ("image", "png"),
            ".jpg": ("image", "jpeg"),
            ".jpeg": ("image", "jpeg"),
            ".zip": ("application", "zip"),
        }.get(ext, ("application", "octet-stream"))
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=p.name)

    recipients = list(to) + (cc or [])
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(server, port, context=ctx) as s:
        s.login(user, pw)
        s.send_message(msg, from_addr=user, to_addrs=recipients)
    print(f"OK sent to {recipients}  subject={subject!r}  attachments={len(attachments or [])}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", action="append", required=True)
    ap.add_argument("--cc", action="append", default=[])
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body", help="inline body text")
    ap.add_argument("--body-file", type=Path, help="read body from file")
    ap.add_argument("--html", action="store_true", help="body is HTML")
    ap.add_argument("--attach", action="append", default=[], type=Path)
    args = ap.parse_args()

    if args.body_file:
        body = args.body_file.read_text()
    elif args.body:
        body = args.body
    else:
        sys.exit("need --body or --body-file")

    send(to=args.to, cc=args.cc, subject=args.subject, body=body,
         attachments=args.attach, html=args.html)


if __name__ == "__main__":
    main()
