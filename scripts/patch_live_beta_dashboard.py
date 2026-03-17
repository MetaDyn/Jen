#!/usr/bin/env python3
from pathlib import Path

BUNDLE = Path('/home/jza/.nvm/versions/node/v25.8.1/lib/node_modules/openclaw/dist/control-ui/assets/index-UvgeZ3yV.js')
LIVE_BETA = Path('/home/jza/.nvm/versions/node/v25.8.1/lib/node_modules/openclaw/dist/control-ui/beta-testers-dashboard.html')
SRC_BETA = Path('/home/jza/.openclaw/workspace/custom-pages/beta-testers-dashboard.html')
LIVE_INDEX = Path('/home/jza/.nvm/versions/node/v25.8.1/lib/node_modules/openclaw/dist/control-ui/metadyn-custom-pages.html')
SRC_INDEX = Path('/home/jza/.openclaw/workspace/custom-pages/index.html')

new_beta_section = """${t===`beta`?n`
              <div class=\"card\" style=\"padding:22px;display:grid;gap:16px\">
                <div style=\"display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap\">
                  <div>
                    <div class=\"eyebrow\">Beta</div>
                    <h3 style=\"margin:6px 0 0;font-size:22px\">Beta Tester Breakdown</h3>
                    <div style=\"margin-top:8px;color:var(--muted);max-width:900px\">This live Dashboard route now shows the comprehensive beta tester page with the full tester list and captured email addresses by loading the served beta dashboard artifact directly inside the app.</div>
                  </div>
                  <div style=\"display:flex;gap:10px;flex-wrap:wrap\">
                    <a class=\"btn\" href=\"./beta-testers-dashboard.html\" target=\"_blank\" rel=\"noopener noreferrer\">Open Full Beta Page</a>
                    <button class=\"btn\" @click=${()=>{e.dashboardSection=`home`,e.requestUpdate()}}>Back to Dashboard Home</button>
                  </div>
                </div>
                <div style=\"display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px\">
                  <div class=\"card\" style=\"padding:16px\"><div class=\"eyebrow\">Live content</div><div style=\"font-size:24px;font-weight:700;margin-top:6px\">Complete outreach roster</div><div style=\"color:var(--muted);margin-top:6px\">Full tester list rendered with direct email visibility.</div></div>
                  <div class=\"card\" style=\"padding:16px\"><div class=\"eyebrow\">Sections now visible</div><div style=\"font-size:24px;font-weight:700;margin-top:6px\">Email copy targets</div><div style=\"color:var(--muted);margin-top:6px\">Grouped outreach blocks plus the full roster email block.</div></div>
                  <div class=\"card\" style=\"padding:16px\"><div class=\"eyebrow\">Served asset</div><div style=\"font-size:18px;font-weight:700;margin-top:6px;word-break:break-word\">./beta-testers-dashboard.html</div><div style=\"color:var(--muted);margin-top:6px\">Dashboard tab delegates to the actual served artifact rather than a stale hardcoded summary.</div></div>
                </div>
                <div class=\"card\" style=\"padding:12px\">
                  <iframe title=\"MetaDyn Beta Tester Breakdown\" src=\"./beta-testers-dashboard.html\" style=\"width:100%;min-height:78vh;border:0;border-radius:14px;background:#0b1020\" loading=\"eager\"></iframe>
                </div>
              </div>
            `:i}"""


def main() -> None:
    if SRC_BETA.exists():
        LIVE_BETA.write_text(SRC_BETA.read_text())
    if SRC_INDEX.exists():
        LIVE_INDEX.write_text(SRC_INDEX.read_text())

    text = BUNDLE.read_text()
    start = text.index('${t===`beta`?n`')
    end = text.index('            `:i}\n\n            ${t===`company`?n`')
    text = text[:start] + new_beta_section + text[end:]
    BUNDLE.write_text(text)
    print('patched live bundle and copied served beta dashboard/html landing page')

if __name__ == '__main__':
    main()
