#!/usr/bin/env python3
"""HTML -> PNG renderer using headless Chrome.

Shared by thumbnail.py and by body-diagram rendering. Deterministic size:
the output is exactly ``width * scale`` by ``height * scale`` pixels.

Usage:
    python3 render.py card.html out.png --width 1200 --height 630 --scale 2

Requires Google Chrome (macOS default location, or set CHROME_PATH).
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DEFAULT_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CANDIDATES = [
    DEFAULT_CHROME,
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]


def find_chrome() -> str:
    env = os.environ.get("CHROME_PATH")
    if env:
        if not Path(env).exists():
            sys.exit(f"CHROME_PATH is set but does not exist: {env}")
        return env
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    for name in ("google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit(
        "Chrome not found. Install Google Chrome, or set CHROME_PATH to a "
        "Chromium-based browser binary."
    )


def render(
    html_path: Path,
    out_path: Path,
    width: int,
    height: int,
    scale: int,
    timeout: float = 60.0,
) -> Path:
    """Render ``html_path`` to ``out_path``. Returns the output path.

    Headless Chrome writes the screenshot and then, on some macOS setups, fails
    to exit on its own. So rather than waiting for the process, poll for the PNG
    to appear and stop growing, then terminate Chrome ourselves.
    """
    if not html_path.exists():
        sys.exit(f"Input HTML not found: {html_path}")
    out_path = out_path.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()

    with tempfile.TemporaryDirectory() as profile:
        cmd = [
            find_chrome(),
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--no-first-run",
            "--no-default-browser-check",
            "--virtual-time-budget=5000",
            f"--user-data-dir={profile}",
            f"--force-device-scale-factor={scale}",
            f"--window-size={width},{height}",
            f"--screenshot={out_path}",
            html_path.resolve().as_uri(),
        ]
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        try:
            deadline = time.monotonic() + timeout
            stable_size = -1
            while time.monotonic() < deadline:
                if out_path.exists():
                    size = out_path.stat().st_size
                    # two consecutive equal, non-zero sizes means the write is done
                    if size > 0 and size == stable_size:
                        break
                    stable_size = size
                elif proc.poll() is not None:
                    break  # Chrome exited without producing anything
                time.sleep(0.25)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)

    if not out_path.exists() or out_path.stat().st_size == 0:
        stderr = (proc.stderr.read() if proc.stderr else "") or ""
        sys.exit(
            f"Chrome did not produce {out_path}.\nstderr:\n{stderr[-2000:]}"
        )
    return out_path


def trim(path: Path, pad: int = 0) -> Path:
    """Crop vertical slack, leaving ``pad`` device pixels above and below.

    Body diagrams rarely fill the window height exactly, so this removes the
    leftover space instead of making you hand-tune --height. Width is left
    alone: you chose it deliberately, and figures read better at one consistent
    width down the post.
    """
    from PIL import Image, ImageChops

    with Image.open(path) as im:
        im = im.convert("RGB")
        bg = Image.new("RGB", im.size, im.getpixel((0, 0)))
        box = ImageChops.difference(im, bg).getbbox()
        if box is None:
            return path  # fully uniform image; nothing to trim
        _, top, _, bottom = box
        top = max(0, top - pad)
        bottom = min(im.height, bottom + pad)
        im.crop((0, top, im.width, bottom)).save(path)
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description="Render an HTML file to PNG via headless Chrome.")
    ap.add_argument("html", type=Path, help="input HTML file")
    ap.add_argument("out", type=Path, help="output PNG file")
    ap.add_argument("--width", type=int, default=1200, help="CSS pixel width (default 1200)")
    ap.add_argument("--height", type=int, default=630, help="CSS pixel height (default 630)")
    ap.add_argument("--scale", type=int, default=2, help="device pixel ratio (default 2)")
    ap.add_argument(
        "--trim",
        nargs="?",
        type=int,
        const=48,
        default=None,
        metavar="PAD",
        help="crop uniform margins, keeping PAD device px (default 48). "
        "Use for body diagrams; never for thumbnails.",
    )
    args = ap.parse_args()

    out = render(args.html, args.out, args.width, args.height, args.scale)
    if args.trim is not None:
        trim(out, args.trim)

    try:
        from PIL import Image

        with Image.open(out) as im:
            print(f"{out}  {im.width}x{im.height}")
    except ImportError:
        print(out)


if __name__ == "__main__":
    main()
