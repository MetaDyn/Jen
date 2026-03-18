# MetaDyn Docs Index

This is the fastest entry point for MetaDyn context in this workspace.

## Start Here

- `company/metadyn.md` — company identity, what MetaDyn is, and core framing
- `company/positioning.md` — positioning language and external-facing narrative
- `architecture/overview.md` — high-level architecture and mission context
- `architecture/collaboration-model.md` — human/agent orchestration model
- `ai-systems/jen.md` — Jen's role as the main orchestration layer
- `infrastructure/topology.md` — current environment and infrastructure shape
- `infrastructure/nginx-ssl-proxy.md` — documented Cloudflare + nginx + SSL origin pattern

## Platform Docs

- `platforms/unity6/README.md` — overview of the Unity 6 platform doc set
- `platforms/unity6/platform-overview.md` — platform definition and intended product shape
- `platforms/unity6/system-architecture.md` — major technical systems
- `platforms/unity6/core-systems.md` — implementation patterns and subsystems
- `platforms/unity6/deployment-hosting.md` — deployment, Cloudflare, hosting, and delivery model
- `platforms/unity6/platform-deep-dive.md` — strengths, gaps, and strategic direction
- `platforms/unity6/import-notes.md` — mapping from raw imported material into the normalized docs
- `platforms/immersive-spaces.md` — cross-platform immersive-space context outside Unity

## Operations, Runbooks, And Standards

- `operations/community-marketing-cadence.md` — weekly and monthly operating cadence for community + marketing
- `runbooks/repo-setup.md` — repo and local environment setup
- `runbooks/local-static-demo-server.md` — local static serving for LAN/testing
- `runbooks/cloudflare-jen-tunnel.md` — recommended HTTPS ingress pattern for `jen.metadyn.xyz`
- `runbooks/ubuntu-server-bootstrap-checklist.md` — baseline Ubuntu host setup for Cloudflare + nginx origin workloads
- `standards/documentation.md` — documentation conventions for this workspace

## Raw Imported Source

Use these when the normalized docs are missing detail or when you need the original source phrasing.

- `/home/jza/.openclaw/workspace/import/unity6-docs/.claude/Quick Reference/`
- `/home/jza/.openclaw/workspace/import/unity6-docs/.claude/Planning/`
- `/home/jza/.openclaw/workspace/import/unity6-docs/.claude/session_notes/`
- `/home/jza/.openclaw/workspace/import/unity6-docs/.claude/skills/`
- `/home/jza/.openclaw/workspace/import/assets/images/` — branding and shared image assets

## Working Rule

Prefer the normalized docs in this `docs/` tree first. Drop into `import/unity6-docs/.claude/` only when you need source-detail, missing rationale, or imported artifacts that have not been curated yet.
