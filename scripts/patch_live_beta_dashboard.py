#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from collections import Counter, defaultdict
from pathlib import Path

BUNDLE = Path('/home/jza/.nvm/versions/node/v25.8.1/lib/node_modules/openclaw/dist/control-ui/assets/index-UvgeZ3yV.js')
LIVE_BETA = Path('/home/jza/.nvm/versions/node/v25.8.1/lib/node_modules/openclaw/dist/control-ui/beta-testers-dashboard.html')
SRC_BETA = Path('/home/jza/.openclaw/workspace/custom-pages/beta-testers-dashboard.html')
LIVE_INDEX = Path('/home/jza/.nvm/versions/node/v25.8.1/lib/node_modules/openclaw/dist/control-ui/metadyn-custom-pages.html')
SRC_INDEX = Path('/home/jza/.openclaw/workspace/custom-pages/index.html')
UPSTREAM_STATIC_DASH = Path('/home/jza/.openclaw/workspace/custom-pages/metadyn-dashboard/index.html')


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def esc_tpl(value: str) -> str:
    return esc(value).replace('`', '&#96;').replace('${', '&#36;{')


def load_testers() -> list[dict]:
    text = SRC_BETA.read_text()
    match = re.search(r"const testers = \[(.*?)\n    \];", text, re.S)
    if not match:
        raise RuntimeError('Could not locate testers array in beta-testers-dashboard.html')
    payload = '[' + match.group(1) + '\n]'
    import json
    import subprocess

    node_script = (
        "const vm=require('vm');"
        "const data=vm.runInNewContext(process.argv[1]);"
        "process.stdout.write(JSON.stringify(data));"
    )
    raw = subprocess.check_output(['node', '-e', node_script, payload], text=True)
    return json.loads(raw)


def lane_for(tester: dict) -> tuple[str, str, str]:
    interest = tester.get('interest', '')
    interview = tester.get('interview', '')
    self_host = tester.get('selfHost', '')
    challenges = (tester.get('challenges') or '').strip()
    if 'Enterprise' in interest or self_host.startswith('Yes'):
        return (
            'Enterprise / technical design partners',
            'Enterprise interest and/or clear self-host curiosity makes them strong early design collaborators.',
            'Send founder-style onboarding note with architecture preview + interview invite.',
        )
    if 'Professional/Business' in interest or interview.startswith('Yes'):
        return (
            'Professional operators',
            'Business workflow value and interview willingness make them useful for practical workflow validation.',
            'Email with operator workflow questions and scheduling link.',
        )
    if 'Art' in interest or 'Dev' in interest or 'creator' in challenges.lower():
        return (
            'Creator / mixed-use testers',
            'Strong fit for creative tooling, collaboration loops, and community-led testing.',
            'Invite into Discord feedback lane and ask for a first scenario walkthrough.',
        )
    return (
        'General beta cohort',
        'Good broad-user signal for onboarding, comfort, and written feedback loops.',
        'Send welcome email, lightweight survey, and first-access instructions.',
    )


def build_beta_section(testers: list[dict]) -> str:
    total = len(testers)
    email_count = sum(1 for t in testers if t.get('email'))
    interview_yes = sum(1 for t in testers if 'Yes' in (t.get('interview') or ''))
    challenge_count = sum(1 for t in testers if (t.get('challenges') or '').strip() and (t.get('challenges') or '').strip().lower() != 'nothing')
    self_host_count = sum(1 for t in testers if (t.get('selfHost') or '').startswith('Yes') or 'Perhaps' in (t.get('selfHost') or ''))
    os_counter = Counter(os for t in testers for os in t.get('os', []))

    lane_groups: dict[str, list[dict]] = defaultdict(list)
    for tester in testers:
        lane_groups[lane_for(tester)[0]].append(tester)

    roster_rows = []
    roster_cards = []
    lane_rows = []
    for tester in testers:
        lane, why, next_touch = lane_for(tester)
        name = esc_tpl(tester.get('name', 'Unknown'))
        email = esc_tpl(tester.get('email', '—'))
        interest = esc_tpl(tester.get('interest', '—'))
        interview = esc_tpl(tester.get('interview', '—'))
        self_host = esc_tpl(tester.get('selfHost', '—'))
        comfort = esc_tpl(tester.get('comfort', '—'))
        platforms = esc_tpl(', '.join(tester.get('os', [])) or '—')
        feedback = esc_tpl(', '.join(tester.get('feedback', [])) or '—')
        challenges = esc_tpl((tester.get('challenges') or 'No explicit challenge text provided.').strip())
        roster_rows.append(
            f"<tr><td><strong>{name}</strong><div style=\"color:var(--muted);font-size:12px\">{interest}</div></td><td><a href=\"mailto:{email}\">{email}</a></td><td>{esc_tpl(lane)}</td><td>{platforms}</td><td>{feedback}</td><td>{esc_tpl(next_touch)}</td></tr>"
        )
        roster_cards.append(
            f"<div class=\"card\" style=\"padding:16px;display:grid;gap:10px\"><div><div class=\"eyebrow\">{esc_tpl(lane)}</div><h4 style=\"margin:6px 0 0;font-size:18px\">{name}</h4><div style=\"color:var(--muted);margin-top:4px\"><a href=\"mailto:{email}\">{email}</a></div></div><div style=\"display:grid;gap:6px;font-size:14px\"><div><strong>Platforms:</strong> {platforms}</div><div><strong>Feedback:</strong> {feedback}</div><div><strong>Interview:</strong> {interview}</div><div><strong>Self-host:</strong> {self_host}</div><div><strong>Comfort:</strong> {comfort}/10</div><div><strong>Challenge:</strong> {challenges}</div><div><strong>Next touch:</strong> {esc_tpl(next_touch)}</div></div></div>"
        )
    for lane, members in lane_groups.items():
        _, why, _ = lane_for(members[0])
        who = esc_tpl(', '.join(f"{m.get('name')} <{m.get('email')}>" for m in members))
        lane_rows.append(f"<tr><td><strong>{esc_tpl(lane)}</strong></td><td>{who}</td><td>{esc_tpl(why)}</td></tr>")

    email_targets = []
    for lane, members in lane_groups.items():
        emails = '; '.join(m.get('email', '') for m in members if m.get('email'))
        email_targets.append(
            f"<div class=\"card\" style=\"padding:14px;display:grid;gap:8px\"><div class=\"eyebrow\">{esc_tpl(lane)}</div><div style=\"font-size:14px;word-break:break-word\">{esc_tpl(emails)}</div></div>"
        )

    os_summary = ''.join(
        f"<div class=\"card\" style=\"padding:14px\"><div class=\"eyebrow\">Platform coverage</div><div style=\"font-size:18px;font-weight:700;margin-top:6px\">{esc_tpl(name)}</div><div style=\"color:var(--muted);margin-top:4px\">{count} tester{'s' if count != 1 else ''}</div></div>"
        for name, count in os_counter.most_common()
    )

    email_rollup = ', '.join(f"{t.get('name')} <{t.get('email')}>" for t in testers)

    return f"""${{t===`beta`?n`
              <div class=\"card\" style=\"padding:22px;display:grid;gap:16px\">
                <div style=\"display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap\">
                  <div>
                    <div class=\"eyebrow\">Beta</div>
                    <h3 style=\"margin:6px 0 0;font-size:22px\">Beta Tester Breakdown</h3>
                    <div style=\"margin-top:8px;color:var(--muted);max-width:960px\">Native in-app route restored. This route now renders the comprehensive beta tester breakdown directly inside Control UI, with the full tester roster, direct emails, outreach lanes, and local-source verification — no iframe and no separate-page embed.</div>
                  </div>
                  <div style=\"display:flex;gap:10px;flex-wrap:wrap\">
                    <button class=\"btn\" @click=${{()=>{{e.dashboardSection=`home`,e.requestUpdate?.()}}}}>Back to Dashboard Home</button>
                    <a class=\"btn\" href=\"./beta-testers-dashboard.html\" target=\"_blank\" rel=\"noopener noreferrer\">Open standalone artifact</a>
                  </div>
                </div>

                <div style=\"display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px\">
                  <div class=\"card\" style=\"padding:16px\"><div class=\"eyebrow\">Total testers</div><div style=\"font-size:28px;font-weight:700;margin-top:6px\">{total}</div><div style=\"color:var(--muted);margin-top:6px\">Complete locally-present intake roster</div></div>
                  <div class=\"card\" style=\"padding:16px\"><div class=\"eyebrow\">Emails captured</div><div style=\"font-size:28px;font-weight:700;margin-top:6px\">{email_count}/{total}</div><div style=\"color:var(--muted);margin-top:6px\">Every current record includes direct email visibility</div></div>
                  <div class=\"card\" style=\"padding:16px\"><div class=\"eyebrow\">Interview ready</div><div style=\"font-size:28px;font-weight:700;margin-top:6px\">{interview_yes}</div><div style=\"color:var(--muted);margin-top:6px\">Explicit yes responses for calls/interviews</div></div>
                  <div class=\"card\" style=\"padding:16px\"><div class=\"eyebrow\">Self-host curious</div><div style=\"font-size:28px;font-weight:700;margin-top:6px\">{self_host_count}</div><div style=\"color:var(--muted);margin-top:6px\">Advanced operators and enterprise-leaning testers</div></div>
                  <div class=\"card\" style=\"padding:16px\"><div class=\"eyebrow\">Challenge text given</div><div style=\"font-size:28px;font-weight:700;margin-top:6px\">{challenge_count}</div><div style=\"color:var(--muted);margin-top:6px\">Records with concrete pain points or deployment asks</div></div>
                </div>

                <div class=\"card\" style=\"padding:18px;display:grid;gap:12px\">
                  <div>
                    <div class=\"eyebrow\">Data source traced</div>
                    <h4 style=\"margin:6px 0 0;font-size:18px\">Original in-app dashboard route, now rendering native content</h4>
                  </div>
                  <div style=\"color:var(--muted);display:grid;gap:6px\">
                    <div><strong>Control UI branch:</strong> <code>e.tab===&#96;dashboard&#96;</code> with <code>t===&#96;beta&#96;</code> in <code>assets/index-UvgeZ3yV.js</code></div>
                    <div><strong>Local beta data source:</strong> <code>custom-pages/beta-testers-dashboard.html</code> inline <code>const testers = [...]</code></div>
                    <div><strong>Email rollup:</strong> {esc_tpl(email_rollup)}</div>
                  </div>
                </div>

                <div style=\"display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px\">{os_summary}</div>

                <div class=\"card\" style=\"padding:18px;display:grid;gap:12px\">
                  <div class=\"section-title\"><div><h2 style=\"margin:0;font-size:20px\">Complete outreach roster</h2><div class=\"small\">Full tester list with direct emails rendered inside the app route</div></div></div>
                  <div style=\"overflow:auto\">
                    <table style=\"width:100%;border-collapse:collapse;font-size:14px\">
                      <thead>
                        <tr style=\"text-align:left;border-bottom:1px solid var(--color-border)\"><th style=\"padding:10px\">Name</th><th style=\"padding:10px\">Email</th><th style=\"padding:10px\">Lane</th><th style=\"padding:10px\">Platforms</th><th style=\"padding:10px\">Feedback</th><th style=\"padding:10px\">Next touch</th></tr>
                      </thead>
                      <tbody>{''.join(roster_rows)}</tbody>
                    </table>
                  </div>
                </div>

                <div style=\"display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px\">
                  <div class=\"card\" style=\"padding:18px;display:grid;gap:12px\">
                    <div class=\"section-title\"><div><h2 style=\"margin:0;font-size:20px\">Outreach lanes</h2><div class=\"small\">Grouped directly from the rendered in-app roster</div></div></div>
                    <div style=\"overflow:auto\">
                      <table style=\"width:100%;border-collapse:collapse;font-size:14px\"><thead><tr style=\"text-align:left;border-bottom:1px solid var(--color-border)\"><th style=\"padding:10px\">Lane</th><th style=\"padding:10px\">Who</th><th style=\"padding:10px\">Why</th></tr></thead><tbody>{''.join(lane_rows)}</tbody></table>
                    </div>
                  </div>
                  <div class=\"card\" style=\"padding:18px;display:grid;gap:12px\">
                    <div class=\"section-title\"><div><h2 style=\"margin:0;font-size:20px\">Email copy targets</h2><div class=\"small\">Direct outreach blocks visible inside the route</div></div></div>
                    <div style=\"display:grid;gap:10px\">{''.join(email_targets)}</div>
                  </div>
                </div>

                <div class=\"card\" style=\"padding:18px;display:grid;gap:12px\">
                  <div class=\"section-title\"><div><h2 style=\"margin:0;font-size:20px\">Full tester roster cards</h2><div class=\"small\">Each locally-present tester with raw intake detail and email shown in-app</div></div></div>
                  <div style=\"display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px\">{''.join(roster_cards)}</div>
                </div>
              </div>
            `:i}}"""


def patch_upstream_static_dashboard(testers: list[dict]) -> None:
    text = UPSTREAM_STATIC_DASH.read_text()
    iframe_block = '''        <div class="beta-frame-wrap">
          <iframe
            class="beta-frame"
            src="../beta-testers-dashboard.html"
            title="MetaDyn Beta Tester Dashboard"
            loading="eager"
          ></iframe>
        </div>'''
    replacement = '''        <div class="card" style="padding:18px;display:grid;gap:12px; margin-top: 16px;">
          <div>
            <strong>Inline dashboard summary restored</strong>
            <p style="margin:8px 0 0; color: rgba(226,232,240,0.8);">
              The iframe embed was removed. This panel now points people to the native Control UI beta route and the standalone artifact, while the actual in-app route renders the full roster directly.
            </p>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;">
            <div class="card" style="padding:14px;"><div class="label">Total testers</div><strong>''' + str(len(testers)) + '''</strong></div>
            <div class="card" style="padding:14px;"><div class="label">Emails captured</div><strong>''' + str(sum(1 for t in testers if t.get('email'))) + '''</strong></div>
          </div>
          <div class="hero-actions">
            <a class="button primary" href="../beta-testers-dashboard.html">Open standalone beta dashboard</a>
          </div>
        </div>'''
    if iframe_block in text:
        text = text.replace(iframe_block, replacement)
        UPSTREAM_STATIC_DASH.write_text(text)


def main() -> None:
    testers = load_testers()
    new_beta_section = build_beta_section(testers)

    if SRC_BETA.exists():
        LIVE_BETA.write_text(SRC_BETA.read_text())
    if SRC_INDEX.exists():
        LIVE_INDEX.write_text(SRC_INDEX.read_text())

    text = BUNDLE.read_text()
    start = text.index('${t===`beta`?n`')
    end = text.index('            `:i}\n\n            ${t===`company`?n`')
    text = text[:start] + new_beta_section + text[end:]
    BUNDLE.write_text(text)
    patch_upstream_static_dashboard(testers)
    print(f'patched live bundle with native beta route for {len(testers)} testers; iframe route removed from live dashboard branch')


if __name__ == '__main__':
    main()
