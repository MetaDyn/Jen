# Startup Summary

Minimal startup context for MetaDyn agents. Load this first, then load only the domain docs required by the task.

**Last Updated:** 2026-03-12
**Purpose:** Reduce startup context cost while preserving access to deeper `.claude/Quick Reference/` docs on demand.

---

## Must Know

- Follow user directions exactly.
- Do only what the user asked.
- Do not expand scope without permission.
- Do not run extra validation, adjacent investigation, or helpful side tasks unless asked.
- Update `.claude/CHANGELOG.md` for significant changes.
- Update `.claude/DECISIONS.md` only for real architectural decisions/tradeoffs.

---

## Core Platform Snapshot

- Project: MetaDyn Pavilion / MetaDyn platform
- Engine: Unity 6000.0.62f1 (Unity 6)
- Rendering: URP 17.0.4
- Networking: Photon Fusion 2.0.9 Stable
- Network mode: Shared Mode
- Primary target: WebGL
- Secondary target: Native
- Session scale target: up to 50 users, voice bandwidth-dependent

---

## Read By Default

1. `/.claude/Quick Reference/STARTUP_SUMMARY.md`
2. `/.claude/CHANGELOG.md`

Optional by task size:
- `Assets/Docs/Project_Evaluation.md` only for major feature/refactor work

Do not preload the full quick-reference set unless the task actually touches those systems.

---

## Domain Routing

- `QUICK_REFERENCE.md`
  - Broad project map: key files, patterns, controls, current status
  - Use when you need general repo orientation

- `AUTH_SYSTEM.md`
  - Supabase auth, dashboard redirect flow, cookie SSO, Unity/Hyperfy SSO planning
  - Load for login, profile, dashboard, token, avatar persistence work

- `AI_EMBODIMENT.md`
  - AI perception, eye, movement, memory, voice-controller integration
  - Load for Aurora/AI/avatar intelligence work

- `AI_SYSTEM_INSTRUCTIONS.md`
  - Aurora persona/system prompt behavior
  - Load only when changing AI behavior/instructions

- `INFRASTRUCTURE.md`
  - Cloudflare, WebRTC voice, hosting/network constraints, deployment behavior
  - Load for production hosting, network, performance, voice infra tasks

- `DEPLOYMENT_ARCHITECTURE.md`
  - Self-hosted vs shared-hosted model, per-space build rule, SDK deployment role
  - Load for deployment workflow, hosting model, routing, provisioning changes

- `SDK_DEVELOPMENT.md`
  - Standards for SDK/runtime/editor features and required documentation
  - Load when adding/updating MetaDyn SDK systems

- `SDK_TOOLKIT_INVENTORY.md`
  - Current boundary of what counts as SDK/update scope
  - Load for packaging, extraction, transfer, or SDK update planning

- `SDK_UPDATE_MANIFEST.md`
  - Planned updater manifest shape and canonical update paths
  - Load for dashboard updater/version-management work

- `VOICE_CONTROLLER_MODEL_SPLIT_PLAN.md`
  - Future planning note for splitting chat/vision/analysis models
  - Load only if touching `MetaDynVoiceController` model selection

---

## Fast Task Mapping

- General repo orientation
  - Read `QUICK_REFERENCE.md`

- Auth, login, dashboard, profile, cookie/token flow
  - Read `AUTH_SYSTEM.md`

- AI agent, Aurora, perception, memory, movement, vision
  - Read `AI_EMBODIMENT.md`
  - Also read `AI_SYSTEM_INSTRUCTIONS.md` if behavior/prompt changes

- Voice/WebRTC/network/performance/Cloudflare
  - Read `INFRASTRUCTURE.md`

- Deployment, provisioning, hosting model, routing
  - Read `DEPLOYMENT_ARCHITECTURE.md`
  - Usually also `INFRASTRUCTURE.md`

- SDK feature/editor tooling/package/update work
  - Read `SDK_DEVELOPMENT.md`
  - Add `SDK_TOOLKIT_INVENTORY.md` if file scope matters
  - Add `SDK_UPDATE_MANIFEST.md` if updater/version logic matters

---

## Canonical Notes

- Quick reference docs live under `/.claude/Quick Reference/`
- The canonical startup quick-reference path is `/.claude/Quick Reference/STARTUP_SUMMARY.md`
- The canonical broad reference path is `/.claude/Quick Reference/QUICK_REFERENCE.md`
- Historical references to `/.claude/QUICK_REFERENCE.md` may still exist in old changelog entries but should not be used for startup

