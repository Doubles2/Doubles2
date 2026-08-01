#!/usr/bin/env python3
"""matplotlib theme matching the blog's body figures.

Light theme on purpose — the post body is a white page with #333 text, so plots
should sit in the reading flow rather than interrupt it. The coral accent is the
one thing shared with the dark thumbnail.

Usage:
    import os, sys; sys.path.insert(0, os.path.expanduser("~/.claude/skills/tstory/scripts"))
    from plotstyle import apply_style, COLORS, save

    apply_style()
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(x, y, color=COLORS[0])
    save(fig, "output/<slug>/fig-01.png")
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager

# Categorical sequence: coral first (the brand accent), then hues that stay
# distinguishable in greyscale and for the common colour-vision deficiencies.
COLORS = ["#e0795a", "#3b6ea5", "#4c9a7a", "#b08b4f", "#7b6ca8", "#8c8f95"]

ACCENT = "#e0795a"
TEXT = "#24292f"
MUTED = "#6b7280"
LINE = "#dee2e6"
PANEL = "#f8f9fa"

# Korean-capable fonts present on macOS, best first.
_KO_CANDIDATES = [
    "Pretendard",
    "Apple SD Gothic Neo",
    "AppleGothic",
    "Noto Sans CJK KR",
    "NanumGothic",
]


def _pick_font() -> str:
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in _KO_CANDIDATES:
        if name in available:
            return name
    return matplotlib.rcParams["font.sans-serif"][0]


def apply_style() -> None:
    """Install the blog theme into the global matplotlib rcParams."""
    font = _pick_font()
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [font, "DejaVu Sans"],
            "axes.unicode_minus": False,  # keep the Korean font from eating minus signs
            "figure.facecolor": "#ffffff",
            "axes.facecolor": "#ffffff",
            "savefig.facecolor": "#ffffff",
            "text.color": TEXT,
            "axes.labelcolor": TEXT,
            "axes.edgecolor": LINE,
            "axes.titlecolor": TEXT,
            "axes.titlesize": 17,
            "axes.titleweight": "bold",
            "axes.titlepad": 14,
            "axes.labelsize": 13,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": LINE,
            "grid.linewidth": 0.9,
            "grid.alpha": 0.8,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "legend.frameon": False,
            "legend.fontsize": 12,
            "lines.linewidth": 2.4,
            "lines.markersize": 6,
            "patch.edgecolor": "none",
            "figure.dpi": 100,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.25,
            "axes.prop_cycle": plt.cycler(color=COLORS),
        }
    )


def save(fig, path) -> Path:
    """Save ``fig`` to ``path``, creating parent directories."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    print(f"figure: {path}")
    return path


if __name__ == "__main__":
    # smoke test: renders a sample chart with Korean labels
    import numpy as np

    apply_style()
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x), label="학습 손실")
    ax.plot(x, np.cos(x), label="검증 손실")
    ax.set_title("한글 제목 렌더링 확인 (음수 눈금 -1.0 ~ 1.0)")
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("에폭")
    ax.set_ylabel("손실")
    ax.legend()
    save(fig, "_plotstyle_smoketest.png")
