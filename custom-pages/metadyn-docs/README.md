# MetaDyn Docs Hub

Browser-facing documentation landing page for end users, partners, and collaborators.

## Purpose

- provide a clean HTML entry point into the MetaDyn documentation set
- summarize the company, platform, operations, and AI/control-plane docs
- point people toward the curated docs tree instead of the raw imported sources

## Files

- `index.html`
- `styles.css`

## Serving

Best served from the `custom-pages` directory so both the dashboard and docs hub can coexist under one static root.

```bash
cd /home/jza/.openclaw/workspace/custom-pages
python3 -m http.server 8081 --bind 0.0.0.0
```

Then open:

- `http://<host-ip>:8081/metadyn-dashboard/`
- `http://<host-ip>:8081/metadyn-docs/`
