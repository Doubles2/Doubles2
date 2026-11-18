#!/bin/bash
# 이 글의 모든 산출물을 다시 만듭니다. 수정 후 이걸 돌리면 됩니다.
#   fig-NN.html  → fig-NN.png
#   아래 옵션    → thumbnail.png
set -e
cd "$(dirname "$0")"
SKILL_DIR=~/code/doubles2/skills/tstory

# --- 썸네일 -------------------------------------------------------------
python3 $SKILL_DIR/scripts/thumbnail.py \
  --series   "MLflow 완전정복" \
  --word     "ML Lifecycle" \
  --title    "10단계, 하나씩 뜯어보기" \
  --subtitle "문제 정의부터 유지보수 · 반복까지" \
  --number   "2-1" \
  --out      thumbnail.png

# --- 본문 그림 ----------------------------------------------------------
python3 $SKILL_DIR/scripts/render.py fig-01.html fig-01.png --width 1000 --height 900 --trim
python3 $SKILL_DIR/scripts/render.py fig-02.html fig-02.png --width 1000 --height 800 --trim

# --- 원고 검사 ----------------------------------------------------------
python3 $SKILL_DIR/scripts/check_md.py post.md
