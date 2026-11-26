#!/usr/bin/env python3
"""책 공부 항목 폴더를 찾는다.

사용: find_item.py <책 이름 일부> <번호 또는 폴더 앞부분>
  find_item.py 실용 7          → …/내용/1장 실용주의 철학_Topic07_소통하라!
  find_item.py 파이썬 21       → …/내용/3장_함수_BetterWay21_…
  find_item.py 머니 2          → …/내용/2장_한국 증시의 기회와 도전
  find_item.py 결정 3          → …/내용/1부_입을 열기 전에 할 일_3장_…
  find_item.py 카네기 3부_1장  → …/내용/3부_…_1장_논쟁을 피하라
  find_item.py 카네기 0부_들어가며  → 앞부분이 일치하는 폴더

숫자면 먼저 _Topic07_ / _BetterWay21_ 를 찾고, 없을 때만 "2장_" 같은 장 번호로 찾는다.
경계(_)까지 맞춰 7과 70을 혼동하지 않는다.
macOS 파일 이름은 NFD라서 비교 전에 NFC로 맞춘다.
"""

import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(os.environ.get("BOOK_ROOT", "/Users/soonwon/study/책"))


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def find_book(part: str) -> Path:
    books = [p for p in ROOT.iterdir() if p.is_dir() and nfc(p.name).startswith("공부_") and nfc(part) in nfc(p.name)]
    if len(books) != 1:
        names = "\n  ".join(nfc(p.name) for p in books) or "(없음)"
        raise SystemExit(f"책 폴더가 {len(books)}개 맞음: {part}\n  {names}")
    return books[0] / "내용"


def item_patterns(key: str) -> list[re.Pattern]:
    """앞의 패턴부터 시도한다. 숫자는 항목 번호(Topic·BetterWay)가 장 번호보다 먼저다."""
    key = nfc(key)
    if key.isdigit():
        return [re.compile(rf"_Topic0*{key}_|_BetterWay{key}_"), re.compile(rf"(^|_){key}장[ _]|^{key}_")]
    part = re.fullmatch(r"(\d+)부_(\d+)장", key)
    if part:  # 부마다 장 번호가 다시 시작하는 책(카네기)
        return [re.compile(rf"^{part[1]}부_(.*_)?{part[2]}장_")]
    return [re.compile("^" + re.escape(key))]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    content = find_book(sys.argv[1])
    dirs = [p for p in content.iterdir() if p.is_dir()]
    matches = []
    for pattern in item_patterns(sys.argv[2]):
        matches = sorted(p for p in dirs if pattern.search(nfc(p.name)))
        if matches:
            break
    if not matches:
        raise SystemExit(f"맞는 항목 없음: {sys.argv[2]} (in {nfc(str(content))})")
    for path in matches:
        print(nfc(str(path)))


if __name__ == "__main__":
    main()
