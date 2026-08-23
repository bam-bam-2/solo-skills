#!/usr/bin/env python3
"""
HTML → PDF 변환 스크립트
사용법:
  python html-to-pdf.py 파일.html
  python html-to-pdf.py 파일.html --output 출력.pdf
  python html-to-pdf.py "chapters/*.html"  # 여러 파일 한 번에
"""

import argparse
import sys
from pathlib import Path


def html_to_pdf(input_path: Path, output_path: Path | None = None):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright 없음. 설치: pip install playwright && playwright install chromium")
        sys.exit(1)

    if output_path is None:
        output_path = input_path.with_suffix(".pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{input_path.resolve()}", wait_until="networkidle")
        page.pdf(
            path=str(output_path),
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()

    print(f"✓ {output_path.name}")


def main():
    parser = argparse.ArgumentParser(description="HTML → PDF 변환")
    parser.add_argument("inputs", nargs="+", help="변환할 HTML 파일 경로")
    parser.add_argument("--output", "-o", help="출력 PDF 경로 (파일 1개일 때만)")
    args = parser.parse_args()

    paths = [Path(p) for p in args.inputs]

    if args.output and len(paths) > 1:
        print("--output은 파일 1개일 때만 사용 가능합니다.")
        sys.exit(1)

    for path in paths:
        if not path.exists():
            print(f"파일 없음: {path}")
            continue
        out = Path(args.output) if args.output else None
        html_to_pdf(path, out)


if __name__ == "__main__":
    main()
