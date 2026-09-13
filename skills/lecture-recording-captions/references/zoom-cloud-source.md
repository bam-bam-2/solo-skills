# 줌 클라우드 녹화본을 소스로 쓸 때 (2026-09-07 실측)

기수 세션은 대부분 줌 클라우드에 남는다. 맥으로 따로 화면기록을 하지 않았어도 여기서 다 꺼낼 수 있고, **전사본까지 같이 준다.**

## 받는 경로 — API가 브라우저보다 낫다

브라우저로 받으면 맥북 `~/Downloads`에 떨어져서 맥미니로 또 옮겨야 한다. **API로 맥미니에서 직접 받는다.**

자격증명은 맥미니 `~/Projects/getback/pipeline/.env`의 `ZOOM_ACCOUNT_ID` / `ZOOM_CLIENT_ID` / `ZOOM_CLIENT_SECRET`. Server-to-Server OAuth 방식이다.

```python
# 토큰
basic = base64.b64encode(f"{CID}:{CSEC}".encode()).decode()
url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={quote(AID)}"
# 조회 (회의 ID는 공백 없이)
GET https://api.zoom.us/v2/meetings/{MEETING_ID}/recordings
# 다운로드
download_url + "?access_token=" + token
```

**함정: `.env`의 자격증명이 옛날 앱 것일 수 있다.** 2026-09-07에 `invalid_client / The app has been disabled by the developer`가 났는데, 앱이 꺼진 게 아니라 **저장된 값이 폐기된 앱 것**이었다. 마켓플레이스(`marketplace.zoom.us/user/build` → 앱 → App Credentials)에서 현재 값을 읽어 갱신하면 된다. Client Secret은 눈 아이콘을 눌러야 보이고, DOM에서는 `input.value`로 읽힌다.

## 받는 파일

| recording_type | 쓰임 |
|---|---|
| `shared_screen_with_speaker_view` | 메인 소스. 발표자 웹캠이 우상단에 박혀 있다 |
| `shared_screen_with_gallery_view` | 참가자 타일이 보이는 버전. 보통 안 쓴다 |
| `audio_only` (m4a) | 렌더의 오디오 트랙 |
| `audio_transcript` (WEBVTT) | **전사 단계를 건너뛰게 해주는 파일** |
| `timeline`, `chat_file` | 참고용 |

## 규격 맞추기

줌 녹화는 **1760x900 25fps**로 나온다. 1920x1080 30fps로 올려야 스킬 파이프라인에 맞는다.

```bash
ffmpeg -i shared_screen_with_speaker_view.mp4 \
  -vf "scale=1920:-2:flags=lanczos,pad=1920:1080:0:(oh-ih)/2:black,fps=30" \
  -c:v h264_videotoolbox -b:v 3500k -an base.mp4
```

111분짜리가 **약 8분, 2.7GB**로 나온다. 인코딩 중에 파일 크기가 계속 늘어나므로 `pgrep -f h264_videotoolbox`로 끝났는지 보고, 끝나기 전에 `ffprobe`를 걸면 `moov atom not found`가 난다.

## 전사본 쓰기

줌 WEBVTT는 문장 단위라 그대로는 못 쓴다. 두 단계를 거친다.

1. `scripts/vtt_to_segs.py <transcript> segs_final.json`
2. `scripts/add_words.py segs_final.json` — 어절 타임스탬프 생성 (**필수**)

그 사이에 고유명사를 고친다. 줌도 브랜드명은 틀린다.

```python
FIX = [
 (r"갯백|갯배|겟배(?!커)", "겟백"),
 (r"겟백\s*칠\s*기|칠\s*기(?=[에을를로와과의는은])", "겟백 7기"),
 (r"펜을\s*공짜", "팬을 공짜"),
]
```

2026-09-07 실측: 830큐 → 1,124세그먼트 → 8,637어절. 교정된 세그먼트 22개.

## 개인정보 확인은 반드시

기수 세션은 **뒤쪽에 자기소개·질의응답이 붙는다.** 2026-09-07 7기 OT는 130분 중 뒤 60분이 참가자 자기소개였고, 실명·직업·매출·건강 정보가 그대로 나왔다.

전사본을 서브에이전트에 넘겨 **민감 구간을 타임스탬프와 함께 뽑게 한 뒤 밤밤에게 보고한다.** 판단은 밤밤이 한다 — 7기 OT는 "멤버만 보고 링크도 7일 뒤 사라진다"는 이유로 전체 유지를 택했다. 자를 거면 강의 구간만 잘라내는 게 간단하다.
