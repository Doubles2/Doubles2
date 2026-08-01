# 그림 규칙

## 대원칙

**남의 그림을 그대로 가져다 쓰지 않는다. 단, 유명 논문의 figure는 예외로 원본을 쓰고 출처를 남긴다.**

| 대상 | 처리 |
|---|---|
| 강의 슬라이드의 도식 | ❌ 캡처 금지 → 개념만 취해 **새로 그림** |
| 블로그·문서의 다이어그램 | ❌ 캡처 금지 → **새로 그림** |
| 유명 논문 / 참고할 만한 논문의 figure·plot | ✅ **원본 그대로 사용 + 출처 캡션 필수** |
| 공식 문서의 로고·UI 스크린샷 | ✅ 사용 가능 (본인이 직접 띄운 화면이면 더 좋음) |
| 본인이 실행한 터미널·웹 UI 화면 | ✅ 자유롭게 사용 |

"새로 그린다"는 **레이아웃을 바꾸고 본인 언어로 라벨을 다시 단다**는 뜻입니다.
색만 바꾸거나 글자만 한글로 바꾼 것은 재작성이 아닙니다.

## 도식 · 다이어그램 → HTML + 헤드리스 Chrome

`$SKILL_DIR/assets/diagram.html`을 복제해 내용을 채운 뒤 렌더합니다.

원본 HTML은 **글 폴더에 `fig-NN.html`로 남겨둡니다** — 나중에 그림을 수정하려면 이게 있어야 합니다.

```bash
SKILL_DIR=~/.claude/skills/tstory
python3 $SKILL_DIR/scripts/render.py \
  output/<슬러그>/fig-01.html output/<슬러그>/fig-01.png --width 1000 --height 900 --trim
```

- `--width 1000`이 본문 기본값입니다 (티스토리 본문 폭에 여유 있게 맞음)
- `--height`는 넉넉히 준 뒤 `--trim`으로 잘라내면 됩니다. 정확히 맞출 필요 없습니다
- `--scale 2`가 기본이라 출력은 2000px 폭 → 레티나에서 선명합니다

템플릿에 준비된 컴포넌트: `.flow`(가로 흐름) · `.steps`(번호 단계) · `.layers`(계층 스택) ·
`.box.accent`(강조 박스) · `.arrow`

라이트 테마인 이유: 본문이 흰 배경이라 다크 카드를 넣으면 읽기 흐름이 끊깁니다.
다크로 바꾸려면 `:root`의 `--d-*` 값만 썸네일 팔레트로 교체하세요.

## 수치 · 플롯 → matplotlib

```python
import os, sys; sys.path.insert(0, os.path.expanduser("~/.claude/skills/tstory/scripts"))
from plotstyle import apply_style, COLORS, save
import matplotlib.pyplot as plt

apply_style()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y, label="학습 손실")
ax.legend()
save(fig, "output/<슬러그>/fig-02.png")
```

`apply_style()`이 블로그 팔레트·한글 폰트·격자 스타일을 한 번에 적용합니다.
첫 계열 색은 브랜드 코랄(`#e0795a`)입니다.

**데이터를 지어내지 마세요.** 자료에 실제 수치가 있을 때만 플롯을 그립니다.
없으면 개념 도식으로 대체하고, 예시 수치라면 캡션에 "예시"라고 밝힙니다.

## 논문 figure를 원본으로 쓸 때

1. 논문이 실제로 그 그림을 담고 있는지 확인 (기억으로 인용하지 말 것)
2. 이미지 바로 아래 출처 캡션 (`attribution.md` 참조)
3. 라이선스 확인 — arXiv 논문 다수는 재배포 조건이 있습니다. 애매하면 **링크만 걸고
   본인이 그린 도식으로 대체**하는 편이 안전합니다

## 파일 규칙

- 이름: `fig-01.png`, `fig-02.png` … 본문 등장 순서. 원본은 같은 이름의 `.html`
- 위치: 글 폴더 (원본과 생성물이 나란히)
- 썸네일만 `thumbnail.png`
- `post.md`에는 `![설명](fig-01.png)`로 위치를 표시합니다 — 변환하면 삽입 위치 주석이 붙습니다

## 몇 장이 적당한가

본문 `h2` 2~3개당 1장. 글 하나에 2~4장이 보통입니다.
그림 없이 표로 충분한 내용은 표로 두세요 — 표가 편집도 쉽고 모바일에서도 잘 읽힙니다.
