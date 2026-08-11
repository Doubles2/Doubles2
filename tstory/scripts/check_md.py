#!/usr/bin/env python3
"""Validate an annotated post.md manuscript.

The manuscript is typed into the Tistory editor by hand, so mistakes are only
caught when the author is already halfway through typing. Check them up front:
bad block tags, missing attribution, image references that point at files that
don't exist (or figures sitting in the folder that nobody references).

Usage:
    python3 check_md.py output/<slug>/post.md
"""

import argparse
import re
import sys
from pathlib import Path

# tag name -> expected trailing spec (informational; only the name is enforced)
# 티스토리 기본모드 툴바에 실제로 있는 것만. 크기(pt/px) 입력칸은 없고
# 스타일 프리셋이 크기를 정한다. 서체는 기본서체 고정이라 태그에 쓰지 않는다.
TAGS = {
    "제목1": "스타일 → 제목1  (h2 / size26)",
    "제목2": "스타일 → 제목2  (h3 / size23)",
    "제목3": "스타일 → 제목3  (h4 / size20) — #146 계열은 소단원에 이걸 씁니다",
    "본문2": "기본값, 조작 불필요  (p / size16)",
    "인용구": "인용구 → 스타일2",
    "인용문": "인용구 → 스타일1 + 서체 본명조 (남의 말)",
    "표 헤더": "기울임 — 표 바로 위 한 줄",
    "목록": "불릿 목록 버튼",
    "번호목록": "번호 목록 버튼",
    "표": "표 버튼 (데이터 행만)",
    "코드블록": "코드블록 버튼",
    "구분선": "구분선 → 스타일5",
    "태그 칸 입력용": "본문 아님 — 티스토리 태그 입력칸",
}

# 이 블로그에서 쓰지 않는 프리셋 — 실수로 쓰면 알려준다
UNUSED_PRESETS = {"본문1", "본문3"}

TAG_RE = re.compile(r"^\(([^)·]+?)(?:\s*·\s*[^)]*)?\)\s*$")
IMG_RE = re.compile(r"^\((?P<file>[^)\s]+\.png)\s+삽입\)(?:\s*—\s*(?P<cap>.*))?$")


def check(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    folder = path.parent
    errors: list[str] = []
    warns: list[str] = []

    referenced: list[str] = []
    tag_counts: dict[str, int] = {}

    for no, line in enumerate(lines, 1):
        s = line.strip()
        if not s.startswith("("):
            continue

        m = IMG_RE.match(s)
        if m:
            f = m.group("file")
            referenced.append(f)
            if not (folder / f).exists():
                errors.append(f"line {no}: {f} 를 참조하는데 글 폴더에 그 파일이 없습니다")
            elif not m.group("cap"):
                warns.append(f"line {no}: {f} 에 설명이 없습니다 (— 뒤에 무슨 그림인지)")
            continue

        m = TAG_RE.match(s)
        if m:
            name = m.group(1)
            if name in UNUSED_PRESETS:
                errors.append(
                    f"line {no}: ({name})은 이 블로그에서 쓰지 않는 프리셋입니다 "
                    f"— 제목1·제목2·본문2만 씁니다"
                )
            elif name not in TAGS:
                errors.append(
                    f"line {no}: 알 수 없는 블록 태그 ({name}) — "
                    f"쓸 수 있는 것: {', '.join(TAGS)}"
                )
            else:
                tag_counts[name] = tag_counts.get(name, 0) + 1
            continue

        # a parenthesised line that is neither a tag nor an image is likely a typo
        if re.match(r"^\([^)]{1,40}\)$", s):
            warns.append(f"line {no}: 태그처럼 보이는데 형식이 안 맞습니다 — {s}")

    # 표: 마크다운 헤더 구분선은 티스토리에서 재현되지 않는다
    for no, line in enumerate(lines, 1):
        if re.fullmatch(r"\|(\s*:?-{2,}:?\s*\|)+", line.strip()):
            errors.append(
                f"line {no}: 표에 마크다운 구분선(| --- |)이 있습니다 — "
                f"티스토리 표엔 헤더가 없습니다. 헤더는 (표 헤더) 한 줄로 위에 쓰세요"
            )

    # figures present but never referenced
    for png in sorted(folder.glob("fig-*.png")):
        if png.name not in referenced:
            warns.append(f"{png.name} 이 글 폴더에 있는데 원고에서 참조하지 않습니다")

    # structure
    if not lines or not lines[0].startswith("# "):
        errors.append("첫 줄이 '# 제목'이 아닙니다 (티스토리 제목 칸에 넣을 제목)")

    tips = text.count("💡")
    if tips < 3:
        warns.append(f"💡 블록이 {tips}개 — 이 블로그 톤에는 3개 이상 필요합니다")
    if text.count("📎") < 2:
        errors.append("📎 출처 문구는 상단·하단 두 번 들어가야 합니다")

    h2 = tag_counts.get("제목1", 0)
    hr = tag_counts.get("구분선", 0)
    if h2 and hr < h2:
        warns.append(f"구분선 {hr}개 / 제목1 {h2}개 — 제목1 앞마다 구분선을 넣습니다")

    tail = text.rsplit("📎", 1)[-1]
    if len(re.findall(r"#[^\s#]+", tail)) < 5:
        errors.append("맨 아래 해시태그 줄이 없습니다 (하단 출처 다음, 8~10개)")
    elif "(태그 칸 입력용)" not in text:
        warns.append(
            "해시태그 앞에 (태그 칸 입력용) 태그가 없습니다 "
            "— 본문이 아니라 태그 입력칸에 넣는다는 표시가 필요합니다"
        )

    if not (folder / "thumbnail.png").exists():
        warns.append("thumbnail.png 이 글 폴더에 없습니다")

    return errors, warns


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path, help="post.md to check")
    args = ap.parse_args()
    if not args.path.exists():
        sys.exit(f"not found: {args.path}")

    errors, warns = check(args.path)
    for e in errors:
        print(f"ERROR   {e}")
    for w in warns:
        print(f"WARN    {w}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warns)} warning(s)")
        sys.exit(1)
    print(f"\nOK — 원고 형식 이상 없음. {len(warns)} warning(s)")


if __name__ == "__main__":
    main()
