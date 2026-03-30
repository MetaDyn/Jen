#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path
import struct


OPENCLAW_ROOT = Path("/home/jza/.nvm/versions/node/v25.8.1/lib/node_modules/openclaw/dist/control-ui")
BUNDLE_PATH = OPENCLAW_ROOT / "assets/index-UvgeZ3yV.js"
INDEX_HTML_PATH = OPENCLAW_ROOT / "index.html"

SOURCE_LOGO = Path("/home/jza/.openclaw/workspace/import/assets/images/metadyn_alphastax_logo_400.png")
TARGET_LOGO_NAME = "metadyn_alphastax_logo_400.png"
TARGET_LOGO = OPENCLAW_ROOT / TARGET_LOGO_NAME

BRAND_NAME = "MetaDyn"
CONTROL_TITLE = "MetaDyn Control"


def replace_any(text: str, olds: list[str], new: str, label: str) -> str:
    for old in olds:
        if old in text:
            return text.replace(old, new, 1)
    if new in text:
        return text
    raise RuntimeError(f"Could not find expected {label} pattern")


def main() -> None:
    if not SOURCE_LOGO.exists():
        raise SystemExit(f"Logo file not found: {SOURCE_LOGO}")

    if not OPENCLAW_ROOT.exists():
        raise SystemExit(f"OpenClaw control-ui directory not found: {OPENCLAW_ROOT}")

    shutil.copy2(SOURCE_LOGO, TARGET_LOGO)
    png_bytes = SOURCE_LOGO.read_bytes()
    (OPENCLAW_ROOT / "favicon-32.png").write_bytes(png_bytes)
    (OPENCLAW_ROOT / "apple-touch-icon.png").write_bytes(png_bytes)
    ico_header = struct.pack("<HHH", 0, 1, 1)
    ico_entry = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(png_bytes), 6 + 16)
    (OPENCLAW_ROOT / "favicon.ico").write_bytes(ico_header + ico_entry + png_bytes)

    bundle = BUNDLE_PATH.read_text()
    bundle = replace_any(
        bundle,
        [
            '<img class="sidebar-brand__logo" src="${Vl(_)}" alt="OpenClaw" />',
            '<img class="sidebar-brand__logo" src="metadyn_alphastax_logo_400.png" alt="OpenClaw" />',
        ],
        f'<img class="sidebar-brand__logo" src="{TARGET_LOGO_NAME}" alt="{BRAND_NAME}" />',
        "sidebar logo helper",
    )
    bundle = replace_any(
        bundle,
        [
            '<img class="login-gate__logo" src=${t} alt="OpenClaw" />',
            '<img class="login-gate__logo" src="metadyn_alphastax_logo_400.png" alt="OpenClaw" />',
        ],
        f'<img class="login-gate__logo" src="{TARGET_LOGO_NAME}" alt="{BRAND_NAME}" />',
        "login logo helper",
    )
    bundle = replace_any(
        bundle,
        [
            '<div class="login-gate__title">OpenClaw</div>',
            '<div class="login-gate__title">MetaDyn</div>',
        ],
        f'<div class="login-gate__title">{BRAND_NAME}</div>',
        "login title",
    )
    bundle = replace_any(
        bundle,
        [
            '<span class="sidebar-brand__title">OpenClaw</span>',
            '<span class="sidebar-brand__title">MetaDyn</span>',
        ],
        f'<span class="sidebar-brand__title">{BRAND_NAME}</span>',
        "sidebar title",
    )
    BUNDLE_PATH.write_text(bundle)

    index_html = INDEX_HTML_PATH.read_text()
    index_html = replace_any(
        index_html,
        [
            "<title>OpenClaw Control</title>",
            "<title>MetaDyn Control</title>",
        ],
        f"<title>{CONTROL_TITLE}</title>",
        "page title",
    )
    index_html = replace_any(
        index_html,
        [
            '<link rel="icon" type="image/svg+xml" href="./favicon.svg" />',
            f'<link rel="icon" type="image/png" href="./{TARGET_LOGO_NAME}" />',
        ],
        f'<link rel="icon" type="image/png" href="./{TARGET_LOGO_NAME}" />',
        "svg favicon link",
    )
    index_html = replace_any(
        index_html,
        [
            '<link rel="icon" type="image/png" sizes="32x32" href="./favicon-32.png" />',
            f'<link rel="icon" type="image/png" sizes="32x32" href="./{TARGET_LOGO_NAME}" />',
        ],
        f'<link rel="icon" type="image/png" sizes="32x32" href="./{TARGET_LOGO_NAME}" />',
        "png favicon link",
    )
    index_html = replace_any(
        index_html,
        [
            '<link rel="apple-touch-icon" sizes="180x180" href="./apple-touch-icon.png" />',
            f'<link rel="apple-touch-icon" sizes="180x180" href="./{TARGET_LOGO_NAME}" />',
        ],
        f'<link rel="apple-touch-icon" sizes="180x180" href="./{TARGET_LOGO_NAME}" />',
        "apple touch icon link",
    )
    INDEX_HTML_PATH.write_text(index_html)

    print("Rebrand applied:")
    print(f"- logo: {TARGET_LOGO}")
    print(f"- brand name: {BRAND_NAME}")
    print(f"- title: {CONTROL_TITLE}")
    print("- icon assets: favicon.ico, favicon-32.png, apple-touch-icon.png")


if __name__ == "__main__":
    main()
