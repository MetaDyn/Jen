# OpenClaw UI Rebrand

Use this after OpenClaw updates or any time the Control UI branding gets overwritten.

Command:

```bash
python3 /home/jza/.openclaw/workspace/scripts/rebrand_openclaw_ui.py
```

What it reapplies:

- sidebar top-left logo
- connect/login screen logo
- sidebar brand title
- connect/login title
- browser page title
- icon links in `index.html`

Current source logo:

- `/home/jza/.openclaw/workspace/import/assets/images/metadyn_alphastax_logo_400.png`

If you want to change the brand later, edit these constants in:

- `/home/jza/.openclaw/workspace/scripts/rebrand_openclaw_ui.py`

Values to change:

- `SOURCE_LOGO`
- `TARGET_LOGO_NAME`
- `BRAND_NAME`
- `CONTROL_TITLE`
