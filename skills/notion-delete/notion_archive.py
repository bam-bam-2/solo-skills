#!/usr/bin/env python3
"""
노션 페이지 삭제(아카이브) 스크립트
사용법: python notion_archive.py <page_id_or_url> [page_id2 ...]
"""

import sys
import os
import re
import json
import urllib.request
import urllib.error

# 토큰 우선순위: 환경변수 → 하드코딩 fallback
NOTION_TOKEN = (
    os.environ.get("NOTION_TOKEN")
    or _load_from_env_files()
)

def _load_from_env_files():
    """프로젝트 .env 파일들에서 NOTION_TOKEN 탐색"""
    candidates = [
        os.path.expanduser("~/Projects/getback/운영/pipeline/.env"),
        os.path.expanduser("~/Projects/getback/운영/discord_bot/.env"),
        os.path.expanduser("~/.env"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("NOTION_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

# 재정의 (함수 호출 시점 문제 해결)
def get_token():
    token = os.environ.get("NOTION_TOKEN")
    if token:
        return token
    candidates = [
        os.path.expanduser("~/Projects/getback/운영/pipeline/.env"),
        os.path.expanduser("~/Projects/getback/운영/discord_bot/.env"),
        os.path.expanduser("~/.env"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("NOTION_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

def extract_page_id(input_str):
    """URL 또는 ID에서 페이지 ID 추출"""
    clean = input_str.strip().replace("-", "")
    if re.match(r'^[0-9a-f]{32}$', clean, re.I):
        return clean
    match = re.search(r'([0-9a-f]{32})(?:[?#]|$)', input_str.replace("-", ""), re.I)
    if match:
        return match.group(1)
    raise ValueError(f"유효한 페이지 ID 또는 URL이 아닙니다: {input_str}")

def archive_page(page_id, token):
    page_id_clean = extract_page_id(page_id)
    url = f"https://api.notion.com/v1/pages/{page_id_clean}"
    data = json.dumps({"archived": True}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="PATCH",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
    )
    try:
        with urllib.request.urlopen(req) as res:
            result = json.loads(res.read())
            title = ""
            props = result.get("properties", {})
            for prop in props.values():
                if prop.get("type") == "title":
                    items = prop.get("title", [])
                    title = "".join(t.get("plain_text", "") for t in items)
                    break
            print(f"✅ 삭제 완료: {title or page_id_clean}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ 오류 ({e.code}): {body}")
        return False

if __name__ == "__main__":
    token = get_token()
    if not token:
        print("❌ NOTION_TOKEN을 찾을 수 없습니다.")
        print("   환경변수 또는 ~/Projects/getback/운영/pipeline/.env에 설정하세요.")
        sys.exit(1)
    if len(sys.argv) < 2:
        print("사용법: python notion_archive.py <page_id_or_url> [page_id2 ...]")
        sys.exit(1)
    success = all(archive_page(arg, token) for arg in sys.argv[1:])
    sys.exit(0 if success else 1)
