#!/usr/bin/env python3
import json, re, sys, urllib.request
from pathlib import Path

RPC_URL = 'https://wiki.metadyn.xyz/lib/exe/jsonrpc.php'
TOKEN_SOURCE = Path('/home/jza/.openclaw/agents/main/sessions/a15a9f34-81d8-4e43-9c6d-b6c13f59754f.jsonl.reset.2026-04-17T05-46-11.840Z')


def load_token() -> str:
    text = TOKEN_SOURCE.read_text()
    m = re.search(r"token='([^']+)'", text)
    if not m:
        raise SystemExit('Could not find wiki bearer token in known transcript source')
    return m.group(1)


def md_to_dokuwiki(md: str, title: str) -> str:
    lines = md.splitlines()
    out = [f'====== {title} ======', '']
    for line in lines:
        if line.startswith('### '):
            out += [f'==== {line[4:].strip()} ====', '']
        elif line.startswith('## '):
            out += [f'===== {line[3:].strip()} =====', '']
        elif line.startswith('# '):
            continue
        elif re.match(r'^- ', line):
            out.append('  * ' + line[2:])
        else:
            out.append(line)
    return '\n'.join(out).rstrip() + '\n'


def put_page(page: str, body: str, summary: str):
    token = load_token()
    payload = json.dumps({
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'wiki.putPage',
        'params': [page, body, {'sum': summary}],
    }).encode()
    req = urllib.request.Request(
        RPC_URL,
        data=payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.load(resp)
    if 'error' in res:
        raise SystemExit(f"RPC error for {page}: {res['error']}")
    print(f"UPDATED {page}: {res.get('result')}")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        raise SystemExit('usage: publish_wiki_page.py <page> <title> <source_md_path> <summary>')
    page, title, source_path, summary = sys.argv[1:]
    md = Path(source_path).read_text()
    body = md_to_dokuwiki(md, title)
    put_page(page, body, summary)
