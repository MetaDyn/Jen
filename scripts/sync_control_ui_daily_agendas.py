#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

WORKSPACE = Path('/home/jza/.openclaw/workspace')
ARCHIVE_ROOT = WORKSPACE / 'docs/operations/daily-agendas'
BUNDLE = Path('/home/jza/.nvm/versions/node/v25.8.1/lib/node_modules/openclaw/dist/control-ui/assets/index-UvgeZ3yV.js')


def month_label(dir_name: str) -> str:
    return dir_name.replace('-', ' ')


def read_summary(content: str, fallback: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith('**Date:** '):
            return stripped
    return fallback


def make_doc_obj(path: str, title: str, summary: str, content: str) -> dict:
    return {
        'id': path.replace('/', '-').replace('.', '-'),
        'title': title,
        'path': path,
        'summary': summary,
        'content': content,
    }


def build_month_object(month_dir: Path) -> str:
    readme_path = month_dir / 'README.md'
    readme_content = readme_path.read_text()
    docs = [
        make_doc_obj(
            f'operations/daily-agendas/{month_dir.name}/README.md',
            f'{month_label(month_dir.name)} MetaDyn Daily Agendas',
            f'Daily agenda archive for {month_label(month_dir.name)}.',
            readme_content,
        )
    ]

    for agenda_path in sorted(month_dir.glob('*-metadyn-daily-agenda.md')):
        content = agenda_path.read_text()
        docs.insert(
            0,
            make_doc_obj(
                f'operations/daily-agendas/{month_dir.name}/{agenda_path.name}',
                'MetaDyn Daily Agenda',
                read_summary(content, f'**File:** {agenda_path.name}'),
                content,
            ),
        )

    obj = {
        'id': f'operations-daily-agendas-{month_dir.name.lower()}',
        'path': f'operations/daily-agendas/{month_dir.name}',
        'label': f'Operations / Daily Agendas / {month_label(month_dir.name)}',
        'docs': docs,
    }
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))


def build_root_object() -> str:
    readme_path = ARCHIVE_ROOT / 'README.md'
    readme_content = readme_path.read_text()
    obj = {
        'id': 'operations-daily-agendas',
        'path': 'operations/daily-agendas',
        'label': 'Operations / Daily Agendas',
        'docs': [
            make_doc_obj(
                'operations/daily-agendas/README.md',
                'MetaDyn Daily Agendas',
                'This folder tracks Josh\'s daily MetaDyn agendas over time.',
                readme_content,
            )
        ],
    }
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))


def replace_object(text: str, path: str, replacement: str) -> str:
    pattern = re.compile(r'\{"id":"[^\"]+","path":"' + re.escape(path) + r'","label":"[^"]+","docs":\[(?:.|\n)*?\]\}')
    new_text, count = pattern.subn(lambda _m: replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f'Failed to replace embedded object for {path}; matched {count} blocks')
    return new_text


def main() -> None:
    text = BUNDLE.read_text()
    text = replace_object(text, 'operations/daily-agendas', build_root_object())
    for month_dir in sorted(p for p in ARCHIVE_ROOT.iterdir() if p.is_dir() and re.match(r'^[A-Za-z]+-\d{4}$', p.name)):
        text = replace_object(text, f'operations/daily-agendas/{month_dir.name}', build_month_object(month_dir))
    BUNDLE.write_text(text)
    print(f'Synced embedded daily agenda docs in {BUNDLE}')


if __name__ == '__main__':
    main()
