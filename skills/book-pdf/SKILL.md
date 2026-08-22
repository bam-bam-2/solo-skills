---
name: book-pdf
description: "마크다운 원고를 진짜 책처럼 보이는 PDF·EPUB 전자책으로 만든다. 표지, 판권 페이지, 실제 쪽번호가 달린 목차, 장별 러닝헤더까지 갖춘다. Paged.js 사용."
---

# 마크다운 → 진짜 책 PDF/EPUB

일반 `page.pdf()` + 마크다운→HTML 변환만으로는 "리포트를 인쇄한 것"처럼 보인다.
실제 책이려면 최소 이 6가지가 있어야 한다: **표지(풀블리드) · 타이틀 페이지 · 판권 페이지 · 실제 쪽번호가 달린 목차 · 장 시작마다 새 페이지 · 쪽마다 러닝헤더/쪽번호**.

이 스킬은 [Paged.js](https://pagedjs.org)(MIT, `https://unpkg.com/pagedjs/dist/paged.polyfill.js`)를 브라우저에 스크립트 태그로 로드해 CSS Paged Media 기능(러닝헤더, 목차 쪽번호 자동생성)을 구현한다. Chromium이 네이티브로 지원 안 하는 기능이라 이 폴리필이 필요하다.

## 이 환경(Aside REPL)의 알려진 함정

1. **`page.pdf({width, height})` 파라미터가 무시된다.** 항상 US Letter로 나온다. 반드시 `preferCSSPageSize: true`를 주고 CSS `@page { size: 148mm 210mm; }`로 크기를 지정할 것. `format: 'A5'` 같은 심볼릭 사이즈도 마찬가지로 무시되니 쓰지 말 것.
2. **`page.setViewportSize()`가 없다.** 뷰포트 크기를 못 바꾸므로 표지 등 개별 이미지를 만들 때 `page.screenshot({fullPage:true})`로 큰 캔버스를 찍으면 타일링 버그가 난다. 대신 `page.pdf()` + `pdftoppm`으로 원하는 크기를 렌더링할 것.
3. **`page.addScriptTag()`가 없다.** 외부 스크립트(Paged.js 등)는 `document.write()`로 쓰는 HTML 문자열 안에 `<script src="https://unpkg.com/...">` 태그를 직접 넣어야 로드된다.
4. **구글 폰트 `@import`/`<link>`가 `document.write()` 직후엔 타이밍 문제로 반영 안 될 때가 있다.** 커스텀 세리프 폰트를 꼭 써야 하면 woff2를 직접 fetch해서 base64로 인라인 `@font-face`에 박아넣을 것. 급하면 시스템 폰트(`-apple-system`, `'Apple SD Gothic Neo'`)로 타협.
5. **`target-counter()`로 목차 쪽번호를 만들 때 한글 슬러그 id가 깨질 수 있다.** pandoc이 자동 생성하는 `id="1장-시작과-실패"` 같은 한글 id 대신 `ch-01`, `part-1`, `app-a` 같은 ASCII id로 바꿔서 앵커를 걸 것.
6. **CSS `page:` (named page) 속성을 제목 요소에만 주고 바로 다음 형제 요소에는 안 주면, 그 둘 사이에 강제 페이지베이크가 생긴다.** 단순히 `break-before: page`로 장/부 시작만 제어하고 싶을 때는 `page: main;` 같은 명명 페이지 지정을 쓰지 말거나, 쓴다면 본문 전체에 동일하게 적용해야 한다 — 이건 "장 제목 바로 뒤에 이미지를 넣었는데 이미지가 다음 페이지로 밀리며 압도적인 빈 공백 페이지가 생기는" 증상으로 나타난다. 페이지 구성이 이상하면 가장 먼저 이 속성부터 의심할 것.
7. **트림 사이즈로 A5(148x210mm)를 쓰지 말 것.** A5와 A4는 비율이 동일해(1:1.414, ISO 시리즈) 화면에서 보면 "작은 A4 문서"처럼 보인다. 한국 단행본 표준판형인 **신국판(152x225mm, 비율 1:1.48)**을 쓰면 "진짜 책" 느낌이 명확하게 산다.
8. **Paged.js 렌더링은 비동기라 완료 시점을 폴링해야 한다.** `document.querySelectorAll('.pagedjs_page').length`가 N초 연속 안 바뀔 때까지 기다린 다음 `page.pdf()`를 호출할 것. 문서가 크면(80~150쪽) 완료까지 30초~1분 걸릴 수 있다.

## 절차

1. **원고를 pandoc으로 HTML 변환**: `pandoc manuscript.md -f markdown -t html5 --wrap=none -o body_raw.html`. `\newpage` 같은 LaTeX 지시자는 HTML에서 무시되니 CSS `break-before`로 대체한다.
2. **제목(`h1`/`h2`)에 ASCII id를 다시 부여**하면서 장/부 디바이더 구조로 감싼다 (예: `<h1>` → `<div class="part-divider" data-run="PART 1. ...">`). 이때 **원본 문서에 등장하는 순서를 한 번의 스캔으로 그대로 따라가는 배열**을 만들어 목차 데이터로 쓴다 — h1 전체를 먼저 훑고 h2 전체를 나중에 훑는 식으로 두 번 나눠 처리하면 목차 순서가 깨진다(장이 전부 나온 뒤 부가 나오는 식).
3. **목차 HTML**은 `<a class="toc-entry" href="#ch-01">...</a>` 형태로, CSS에서 `.toc-entry::after { content: target-counter(attr(href url), page); }`로 쪽번호를 자동 채운다.
4. **러닝헤더**: 장/부 요소에 `string-set: runninghead attr(data-run);`, `@page`의 `@top-center { content: string(runninghead); }`로 받는다.
5. **표지는 별도 `@page cover { margin:0; }` + `page: cover;`로 풀블리드**, 그 외 프론트매터(타이틀/판권/목차)는 쪽번호·러닝헤더를 끈 `@page front`로 분리한다.
6. **Paged.js 로드 + 렌더 대기 + PDF 출력**:
   ```js
   const html = `<!DOCTYPE html><html><head>
     <script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
     <style>${css}</style></head><body>${frontMatter}${bodyContent}</body></html>`;
   await page.evaluate((h) => { document.open(); document.write(h); document.close(); }, html);
   // 안정화 폴링
   let last = -1, stable = 0;
   for (let i = 0; i < 60; i++) {
     await sleep(1000);
     const n = await page.evaluate(() => document.querySelectorAll('.pagedjs_page').length);
     if (n === last) { if (++stable >= 3) break; } else stable = 0;
     last = n;
   }
   const pdf = await page.pdf({ printBackground: true, preferCSSPageSize: true });
   ```
7. **검수는 `aside.pdf.renderPages()`로 표지/타이틀/판권/목차/본문 몇 쪽을 실제로 렌더링해서 눈으로 확인**한다. `pdfinfo`로 최종 `Page size`가 의도한 트림 사이즈(A5 등)인지 꼭 재확인한다 (함정 1번 재발 여부 체크).
8. **EPUB은 별도로 pandoc이 이미 잘 만든다**: `pandoc manuscript.md -t epub3 --css=epub.css --epub-cover-image=cover.jpg --toc --toc-depth=2 -o book.epub`. EPUB은 리플로우 포맷이라 쪽번호/러닝헤더 개념이 없고 nav.xhtml 목차만 있으면 충분하다.

## 어색한 쪽 분리(내용이 잘려서 다음 페이지로 넘어가는 현상) 방지

표/인용문/코드블록이 문장 중간에서 맥려서 다음 페이지로 이어지는 건 CSS에 깨짐 방지 규칙이 없어서다. 다음을 기본값으로 넣을 것:

```css
p { orphans: 3; widows: 3; }
table, blockquote, pre, img, figure { break-inside: avoid; page-break-inside: avoid; }
h2, h3 { break-after: avoid; page-break-after: avoid; } /* 소제목이 페이지 맨아래 혼자 남지 않게 */
```

이렇게 하면 문단/표/인용문이 한 페이지에 다 안 들어갈 때 그 블록 전체가 다음 페이지로 밀린다(사용자가 "앞 단락을 뒤로 밀어버려라"라고 표현하는 바로 그 동작). 부작용으로 강제 페이지보맜(장 시작 직전) 앞에 짧은 내용만 단독으로 낙은 거의-빈 페이지가 가끔 생기는데, 이건 실제 책에서도 흔한 자연스러운 현상이라 문제가 아니다. 적용 후반드시 **처음부터 끝까지 순차적으로 모든 페이지를 렌더링해서 육안으로 확인**할 것 — 하나만 집어서 보고 넘어가면 높은 확률로 놓친다.

## flexbox를 부/장 오프너에 쓰지 말 것

제목+삽화를 한 덩어리로 묶어서 같은 페이지에 있게 하려고 `display:flex`를 쓨다면, Paged.js가 flex 컨테이너 내부 높이 계산을 제대로 못 해서 **예상과 달리 자식 요소가 다음 페이지로 통째로 밀려나간다** (제목만 남고 삽화는 혼자 다음 장으로 가는 식). 한 페이지에 여러 요소를 묶을 때는 **평범한 블록 흐름(margin/padding)만으로** 레이아웃하고 flexbox/grid는 피할 것. 또한 제목과 그 바로 뒤에 오는 이미지 문단을 따로 처리하지 말고, 한 번의 정규식으로 단락(제목 헤딩 + 바로 뒤 이미지 단락)을 함께 매칭해서 **하나의 div로 합쳐넣으면** 둘이 한 덩어리로 취급되어 분리될 확률이 줄어든다.

## 스타일 참고

색은 절제된 포인트 컬러 1개(골드/앰버 등)만 쓰고, 여백을 넉넉히 준다. 장 오프너는 "CH.01" 같은 뱃지 + 큰 제목, 인용구는 왼쪽 세로선 + 이탤릭으로 처리하면 무난하게 "책스럽다".
