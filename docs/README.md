# MetaDyn Docs Index

This is the fastest entry point for MetaDyn context in this workspace.

## Start Here

- `company/metadyn.md` — company identity, what MetaDyn is, and core framing
- `company/positioning.md` — positioning language and external-facing narrative
- `architecture/overview.md` — high-level architecture and mission context
- `architecture/collaboration-model.md` — human/agent orchestration model
- `ai-systems/jen.md` — Jen's role as the main orchestration layer
- `ai-systems/agent-orchestration-and-remote-subagents.md` — Jen control-plane model and proposed remote subagent API contract
- `ai-systems/remote-subagent-api-layer.md` — detailed remote subagent API layer spec with sample requests and reference code
- `infrastructure/topology.md` — current environment and infrastructure shape
- `infrastructure/nginx-ssl-proxy.md` — documented Cloudflare + nginx + SSL origin pattern

## Platform Docs

- `platforms/unity6/README.md` — overview of the Unity 6 platform doc set and recommended reading order
- `platforms/unity6/platform-overview.md` — platform definition and intended product shape
- `platforms/unity6/system-architecture.md` — major technical systems
- `platforms/unity6/core-systems.md` — implementation patterns and subsystem map
- `platforms/unity6/auth-identity.md` — web-first auth, Supabase identity, and cross-surface continuity direction
- `platforms/unity6/security-priority-fixes.md` — current Unity auth/identity trust failures and remediation sequence
- `platforms/unity6/multiplayer-social.md` — player/session model, presence, moderation, and social runtime
- `platforms/unity6/realtime-voice.md` — AI voice path, WebRTC player voice, and media scale direction
- `platforms/unity6/deployment-hosting.md` — deployment, Cloudflare, hosting, and delivery model
- `platforms/unity6/sdk-productization.md` — SDK boundary, updater direction, and productization gaps
- `platforms/unity6/platform-deep-dive.md` — strengths, gaps, and strategic direction
- `platforms/unity6/import-notes.md` — mapping from raw imported material into the normalized docs
- `platforms/immersive-spaces.md` — cross-platform immersive-space context outside Unity

## Operations, Runbooks, And Standards

- `operations/community-marketing-cadence.md` — weekly and monthly operating cadence for community + marketing
- `runbooks/repo-setup.md` — repo and local environment setup
- `runbooks/local-static-demo-server.md` — local static serving for LAN/testing
- `runbooks/cloudflare-jen-tunnel.md` — recommended HTTPS ingress pattern for `jen.metadyn.xyz`
- `runbooks/grafana-supabase-monitoring.md` — Grafana deployment pattern for Supabase reporting at `monitor.metadyn.xyz`
- `runbooks/metadyn-unity-webgl-site-deployment.md` — nginx + Unity WebGL site deployment pattern for `*.metadyn.xyz`
- `runbooks/gitlab-ce-nginx-proxy-handoff.md` — sanitized GitLab CE handoff for the MetaDyn nginx proxy host
- `runbooks/umami-analytics-nginx-proxy-handoff.md` — sanitized Umami analytics handoff for the MetaDyn nginx proxy host
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
