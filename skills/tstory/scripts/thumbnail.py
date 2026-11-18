#!/usr/bin/env python3
"""Generate a 1200x630 Tistory thumbnail matching doubles-won.tistory.com.

The card carries, top to bottom: the series badge (주제), the topic word
(주제 단어), the post title (제목), an optional subtitle, and the blog address
at the bottom left.

Usage:
    python3 thumbnail.py \
        --series "MLflow 완전정복" \
        --word "MLflow" \
        --title "MLflow란 무엇인가?" \
        --subtitle "Tracking · Projects · Models · Registry" \
        --number 3 \
        --out output/mlflow-03/thumbnail.png
"""

import argparse
import html
import tempfile
from pathlib import Path

from render import render

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "thumbnail.html"
SITE = "doubles-won.tistory.com"


def size_class(text: str, md: int, lg: int) -> str:
    """Pick a shrink class so long strings stay clear of the tile motif."""
    n = len(text)
    if n > lg:
        return "len-lg"
    if n > md:
        return "len-md"
    return ""


def build_html(series, word, title, subtitle, number, site) -> str:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    number_text = "" if number is None else f"#{number}"
    fields = {
        "SERIES": series,
        "WORD": word,
        "TITLE": title,
        "SUBTITLE": subtitle,
        "NUMBER": number_text,
        "SITE": site,
        "WORD_CLASS": size_class(word, 9, 13),
        # the title/subtitle only ever gets one shrink step
        "TITLE_CLASS": "len-lg" if len(title) > 20 else "",
        "SUBTITLE_CLASS": "len-lg" if len(subtitle) > 30 else "",
    }
    for key, value in fields.items():
        escaped = value if key.endswith("_CLASS") else html.escape(value)
        tpl = tpl.replace("{{" + key + "}}", escaped)
    return tpl


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--series", required=True, help="series badge text, e.g. 'MLflow 완전정복'")
    ap.add_argument("--word", required=True, help="large topic word, e.g. 'MLflow'")
    ap.add_argument("--title", required=True, help="post title line")
    ap.add_argument("--subtitle", default="", help="optional keyword line under the title")
    ap.add_argument("--number", default=None, help="issue number for the watermark, e.g. 3")
    ap.add_argument("--site", default=SITE, help=f"blog address (default {SITE})")
    ap.add_argument("--out", type=Path, default=Path("thumbnail.png"), help="output PNG path")
    ap.add_argument("--keep-html", action="store_true", help="also write the intermediate HTML next to --out")
    args = ap.parse_args()

    markup = build_html(
        args.series, args.word, args.title, args.subtitle, args.number, args.site
    )

    if args.keep_html:
        src = args.out.with_suffix(".html")
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(markup, encoding="utf-8")
        render(src, args.out, 1200, 630, 2)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "thumbnail.html"
            src.write_text(markup, encoding="utf-8")
            render(src, args.out, 1200, 630, 2)

    print(f"thumbnail: {args.out}")


if __name__ == "__main__":
    main()
