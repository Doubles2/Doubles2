# 썸네일 규격

`assets/thumbnail.html`의 근거 문서입니다. 값은 발행된 썸네일 PNG를
픽셀 단위로 측정해 얻었습니다 (추측 아님).

## 사양

- 프레임 **1200×630 CSS px**, `--scale 2`로 렌더 → **2400×1260 PNG** (블로그 기존 썸네일과 동일)
- 전면 배경(full bleed). 여백 테두리나 안쪽 카드 없음
- 좌측에 세로 액센트 바 11px

## 팔레트 (실측 hex)

| 역할 | Hex |
|---|---|
| 배경 | `#0e1320` |
| 회차 워터마크 | `#1a2233` |
| 3×3 모티프 비활성 타일 | `#222c40` |
| 액센트 (좌측 바, 배지, rule, 활성 타일) | `#e0795a` |
| 주제 단어 · 제목 | `#f5f1eb` |
| 부제 · 블로그 주소 | `#aeb2b8` |

## 레이아웃 (1200×630 기준)

| 요소 | 위치 |
|---|---|
| 좌측 액센트 바 | x 0, 폭 11, 전체 높이 |
| 시리즈 배지 (주제) | x 93, y 132. 액센트 외곽선 pill |
| 주제 단어 | x 93, y 258. 116px / 800 |
| 액센트 rule | x 93, y 430. 84×4 |
| 제목 | x 93, y 462. 40px / 700 |
| 부제 | x 93, y 522. 28px / 400 |
| 블로그 주소 | x 93, y 590. 23px, opacity .72 |
| 회차 워터마크 `#N` | 우측 62, top −34. 290px / 800 |
| 3×3 모티프 | 우측 37, top 300. 타일 80×78, gap 20, radius 16. **윗줄만 액센트** |

요청서의 네 요소가 그대로 대응됩니다:
주제 → 배지 · 주제 단어 → 대형 텍스트 · 제목 → 제목줄 · 블로그 사이트 → 좌하단.

## 사용

```bash
SKILL_DIR=~/.claude/skills/tstory
python3 $SKILL_DIR/scripts/thumbnail.py \
  --series "MLflow 완전정복" \
  --word "MLflow" \
  --title "MLflow란 무엇인가?" \
  --subtitle "Tracking · Projects · Models · Registry" \
  --number 3 \
  --out output/mlflow-03/thumbnail.png
```

| 옵션 | 내용 |
|---|---|
| `--series` | 배지에 들어갈 시리즈/주제명 |
| `--word` | 대형 주제 단어. **영문 한 단어**가 가장 잘 맞습니다 |
| `--title` | 한글 제목 한 줄 |
| `--subtitle` | 키워드 나열 (선택). `·`로 구분 |
| `--number` | 회차. 생략하면 워터마크 없음 |
| `--site` | 기본 `doubles-won.tistory.com` |
| `--keep-html` | 중간 HTML도 남김 (미세 조정용) |

## 글자 수 가이드

길면 자동으로 한 단계 줄어들지만, 아래를 넘기지 않는 편이 보기 좋습니다.

| 요소 | 권장 |
|---|---|
| `--series` | 14자 이내 |
| `--word` | 영문 9자 이내 (13자까지 자동 축소) |
| `--title` | 20자 이내 |
| `--subtitle` | 30자 이내 |

`--word`를 한글로 넣어도 되지만, 발행된 12편은 전부 영문
(`MLflow`, `Quickstart`, `MLOps`, `Best Practices`)입니다.

## 폰트

`Pretendard → Apple SD Gothic Neo → Noto Sans KR` 순으로 지정돼 있습니다.
Pretendard는 이 맥에 없어서 실제로는 **Apple SD Gothic Neo**로 렌더되며,
이는 블로그 본문 폰트 스택의 2순위와 같습니다. 설치하면 자동으로 Pretendard가 잡힙니다.

## 변경 시 주의

`--trim`을 쓰면 안 됩니다. 썸네일은 정확히 2400×1260이어야 합니다.
`render.py`의 기본 동작(트림 없음)을 그대로 두세요.
