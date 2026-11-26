#!/usr/bin/env bash
# 항목 폴더의 원본 사진을 읽기 좋은 크기로 줄여 복사한다. 원본은 건드리지 않는다.
# 사용: prep_photos.sh <항목 폴더> [출력 폴더]
#   출력 폴더 기본값: ${TMPDIR}/book-study/<항목 폴더 이름>  (세션 scratchpad를 주면 그곳에)
# 출력: 파일명 순서(= 읽은 순서)대로 01.jpg, 02.jpg ... 경로를 한 줄씩 출력.
set -euo pipefail
SIZE="${PHOTO_SIZE:-1600}"
[ $# -ge 1 ] || { echo "사용: $0 <항목 폴더> [출력 폴더]" >&2; exit 2; }
item="${1%/}"
src="$item/원본"
[ -d "$src" ] || { echo "원본 폴더 없음: $src" >&2; exit 1; }
out="${2:-${TMPDIR:-/tmp}/book-study/$(basename "$item")}"
mkdir -p "$out"

i=0
while IFS= read -r f; do
  i=$((i+1))
  dst="$out/$(printf '%02d' "$i").jpg"
  sips -Z "$SIZE" -s format jpeg "$f" --out "$dst" >/dev/null
  echo "$dst"
done < <(find "$src" -maxdepth 1 -type f \( -iname '*.jp*g' -o -iname '*.png' -o -iname '*.heic' \) | sort)
[ "$i" -gt 0 ] || { echo "사진 없음: $src" >&2; exit 1; }
