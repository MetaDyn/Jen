# Custom Pages / Canvas Entry Pattern

## Purpose
Custom pages should not exist as isolated HTML files with no discoverable path. They need a stable landing page so Dashboard/Canvas has a single obvious place to start.

## Current entry point
- Landing page: `/home/jza/.openclaw/workspace/custom-pages/index.html`
- Current page: `/home/jza/.openclaw/workspace/custom-pages/beta-testers-dashboard.html`

## Pattern
- Put every Canvas-friendly static page inside `custom-pages/`
- Add a link to it from `custom-pages/index.html`
- If there is a demo/launcher page in `canvas-demo/`, include a visible link there too
- Prefer build-free HTML/CSS/JS for quick internal Dashboard pages

## Current beta page
The beta tester breakdown page is linked from:
- `custom-pages/index.html`
- `canvas-demo/index.html`

## Next improvement
Once the Dashboard shell/custom-page registry is identified, wire `custom-pages/index.html` directly into that menu so it appears as a first-class navigation item rather than only a filesystem path.
