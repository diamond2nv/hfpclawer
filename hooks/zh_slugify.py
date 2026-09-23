"""Keep CJK characters in heading anchors.

Why: python-markdown's default slugifier folds non-ASCII away, so a Chinese heading like
"三个典型用法" becomes an anchor named `_1`, `_2`, … — meaningless in a URL, useless when shared.
This hook installs a slugifier that keeps word characters (including CJK) and normalises
whitespace/punctuation to the separator, so anchors stay readable in both languages.
"""

from __future__ import annotations

import re

_KEEP = re.compile(r"[^\w\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af-]+")


def zh_slugify(value: str, separator: str, case: str | None = None) -> str:
    """Slugify keeping CJK; ``case`` is accepted for API compatibility with python-markdown."""
    text = (value or "").strip().lower()
    slug = _KEEP.sub(separator, text)
    return separator.join(part for part in slug.split(separator) if part)


def on_config(config):
    """Install the slugifier for the toc extension."""
    config.mdx_configs.setdefault("toc", {})["slugify"] = zh_slugify
    return config
