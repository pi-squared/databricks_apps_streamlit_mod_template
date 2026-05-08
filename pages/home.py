import base64
import re
from pathlib import Path

import streamlit as st

st.title("Home")

_repo_root = Path(__file__).resolve().parents[1]
_md_text = (_repo_root / "README.md").read_text(encoding="utf-8")


def _data_uri(path: str) -> str | None:
    img_file = _repo_root / path
    if not img_file.exists():
        return None
    ext = img_file.suffix.lstrip(".")
    mime = "image/svg+xml" if ext == "svg" else f"image/{ext}"
    return f"data:{mime};base64," + base64.b64encode(img_file.read_bytes()).decode()


def _embed_md_image(match: re.Match) -> str:
    alt, path = match.group(1), match.group(2)
    uri = _data_uri(path)
    if uri is None:
        return match.group(0)
    return f'<img alt="{alt}" src="{uri}" style="max-width:100%">'


def _embed_html_image(match: re.Match) -> str:
    attrs = match.group(1)
    src = re.search(r'src="([^"]+)"', attrs)
    if not src:
        return match.group(0)
    uri = _data_uri(src.group(1))
    if uri is None:
        return match.group(0)
    return "<img " + re.sub(r'src="[^"]+"', f'src="{uri}"', attrs) + ">"


_md_text = re.sub(r"<img\s+([^>]+?)\s*/?>", _embed_html_image, _md_text)
_md_text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _embed_md_image, _md_text)

st.markdown(_md_text, unsafe_allow_html=True)
