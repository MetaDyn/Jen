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


def convert_table(block_lines):
    rows = []
    for line in block_lines:
        raw = line.strip()
        if not raw.startswith('|'):
            return block_lines
        cells = [c.strip() for c in raw.strip('|').split('|')]
        rows.append(cells)
    if len(rows) >= 2 and all(re.fullmatch(r':?-{3,}:?', c) for c in rows[1]):
        header = rows[0]
        body = rows[2:]
    else:
        header = None
        body = rows
    out = []
    if header:
        out.append('^ ' + ' ^ '.join(header) + ' ^')
    for row in body:
        out.append('| ' + ' | '.join(row) + ' |')
    return out


def md_to_dokuwiki(md: str, title: str) -> str:
    lines = md.splitlines()
    out = [f'====== {title} ======', '']
    i = 0
    in_code = False
    code_lang = None
    code_buf = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        m = re.match(r'^```\s*([A-Za-z0-9_-]+)?\s*$', stripped)
        if m:
            if not in_code:
                in_code = True
                code_lang = (m.group(1) or '').lower()
                code_buf = []
            else:
                if code_lang == 'mermaid':
                    out.append('<mermaid>')
                    out.extend(code_buf)
                    out.append('</mermaid>')
                    out.append('')
                elif code_lang:
                    out.append(f'<code {code_lang}>')
                    out.extend(code_buf)
                    out.append('</code>')
                    out.append('')
                else:
                    out.append('<code>')
                    out.extend(code_buf)
                    out.append('</code>')
                    out.append('')
                in_code = False
                code_lang = None
                code_buf = []
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if stripped.startswith('### '):
            out += [f'==== {stripped[4:].strip()} ====', '']
            i += 1
            continue
        if stripped.startswith('## '):
            out += [f'===== {stripped[3:].strip()} =====', '']
            i += 1
            continue
        if stripped.startswith('# '):
            i += 1
            continue

        if re.match(r'^\|.*\|\s*$', stripped):
            block = []
            while i < len(lines) and re.match(r'^\|.*\|\s*$', lines[i].strip()):
                block.append(lines[i])
                i += 1
            out.extend(convert_table(block))
            out.append('')
            continue

        if re.match(r'^- ', stripped):
            out.append('  * ' + stripped[2:])
            i += 1
            continue

        out.append(line)
        i += 1

    if in_code:
        out.append('<code>')
        out.extend(code_buf)
        out.append('</code>')
        out.append('')

    body = '\n'.join(out)
    body = re.sub(r'\n{3,}', '\n\n', body).rstrip() + '\n'
    return body


def rpc(method: str, params: list):
    token = load_token()
    payload = json.dumps({
        'jsonrpc': '2.0',
        'id': 1,
        'method': method,
        'params': params,
    }).encode()
    req = urllib.request.Request(
        RPC_URL,
        data=payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        res = json.load(resp)
    if 'error' in res:
        raise SystemExit(f"RPC error for {method}: {res['error']}")
    return res.get('result')


def put_page(page: str, body: str, summary: str):
    res = rpc('wiki.putPage', [page, body, {'sum': summary}])
    print(f"UPDATED {page}: {res}")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        raise SystemExit('usage: publish_wiki_page.py <page> <title> <source_md_path> <summary>')
    page, title, source_path, summary = sys.argv[1:]
    md = Path(source_path).read_text()
    body = md_to_dokuwiki(md, title)
    put_page(page, body, summary)
