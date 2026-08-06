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
- `ai-systems/metadyn-crm-integration.md` — Twenty CRM integration, local helper commands, approval rules, task/note/opportunity support, and stdio MCP bridge details
- `infrastructure/topology.md` — current environment and infrastructure shape
- `infrastructure/local-inference.md` — local LM Studio + OpenClaw inference path, Gemma model notes, and current private-network setup
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
- `platforms/unity6/open-sdk-and-hosting-model-2026-05-25.md` — open-source SDK stance, self-host vs MetaDyn-hosted model, and optional ecosystem-connected value
- `platforms/unity6/platform-deep-dive.md` — strengths, gaps, and strategic direction
- `platforms/unity6/import-notes.md` — mapping from raw imported material into the normalized docs
- `platforms/immersive-spaces.md` — cross-platform immersive-space context outside Unity

## Planning

- `planning/Runtime_Avatar_Upload_And_Rigging_Plan.md` — runtime GLB avatar upload, Supabase persistence, auto-rigging, NGO sync, and the verified owner-authoritative animation fix.
- `planning/MetaDyn_UGS_SDK_Production_PunchList.md` — production readiness punch-list for the UGS/NGO SDK baseline, including validation, hardening, migration, social, economy, and creator tooling priorities.

## Project Workspaces

- `projects/README.md` — index for active project-specific working memory
- `projects/pavilion/README.md` — Pavilion project snapshot and active implementation context
- `projects/netflix-house/README.md` — Netflix House project workspace
- `projects/seaworld/README.md` — SeaWorld project workspace
- `projects/vitl-medical/README.md` — VITL Medical project workspace

## Operations, Runbooks, And Standards

- `operations/community-marketing-cadence.md` — weekly and monthly operating cadence for community + marketing
- `runbooks/repo-setup.md` — repo and local environment setup
- `runbooks/openclaw-openai-codex-oauth-refresh.md` — fix `openai-codex` OAuth token refresh failures in main OpenClaw chat
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
