# MetaDyn Dashboard

Simple static dashboard intended as the first page under a future `Custom Pages` section in the OpenClaw control UI.

## Purpose
- provide a high-level MetaDyn dashboard
- offer drill-down starting points into company, platform, and network/infrastructure views
- act as a prototype for internal custom pages that may later be hosted externally

## Files
- `index.html`
- `styles.css`

Related end-user documentation page:
- `../metadyn-docs/index.html`

## Serve locally
```bash
cd /home/jza/.openclaw/workspace/custom-pages/metadyn-dashboard
python3 -m http.server 8081 --bind 0.0.0.0
```

Then open:
- `http://<host-ip>:8081/`

If serving from `/home/jza/.openclaw/workspace/custom-pages`, the docs hub is also available at:
- `http://<host-ip>:<port>/metadyn-docs/`
