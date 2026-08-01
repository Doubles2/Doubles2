#!/bin/bash
# 글 폴더에 복사해 쓰는 템플릿. 썸네일 옵션과 그림 목록을 이 글에 맞게 채우세요.
# 이 글의 모든 산출물을 다시 만듭니다. 수정 후 이걸 돌리면 됩니다.
#   fig-NN.html  → fig-NN.png
#   아래 옵션    → thumbnail.png
set -e
cd "$(dirname "$0")"
SKILL_DIR=~/.claude/skills/tstory

# --- 썸네일 -------------------------------------------------------------
python3 $SKILL_DIR/scripts/thumbnail.py \
  --series   "{{시리즈명}}" \
  --word     "{{주제 단어}}" \
  --title    "{{제목}}" \
  --subtitle "{{부제}}" \
  --number   "{{회차}}" \
  --out      thumbnail.png

# --- 본문 그림 (없으면 이 블록 삭제) ------------------------------------
python3 $SKILL_DIR/scripts/render.py fig-01.html fig-01.png --width 1000 --height 900 --trim

# --- 원고 검사 ----------------------------------------------------------
python3 $SKILL_DIR/scripts/check_md.py post.md
