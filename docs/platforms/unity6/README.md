# MetaDyn Unity 6 Platform

This section captures the imported documentation for the MetaDyn Pavilion / MetaDyn platform built on Unity 6.

## Scope

This documentation is focused primarily on the **platform portion** of MetaDyn:
- Unity 6 platform architecture
- multiplayer and identity foundations
- deployment and hosting model
- platform systems and SDK boundaries
- WebGL-first delivery model

This section intentionally avoids over-merging broader AI-specific documentation that will be added later.

## Platform Snapshot

- Engine: **Unity 6** (`6000.0.62f1`)
- Rendering: **URP 17.0.4**
- Networking: **Photon Fusion 2.0.9 Stable**
- Network Mode: **Shared Mode**
- Primary Target: **WebGL**
- Secondary Target: **Native builds**
- Auth Backend: **Supabase**
- Edge / DNS / SSL: **Cloudflare**
- Player Voice: **WebRTC**
- Avatar Ecosystem: **Ready Player Me** + Avatar SDK support

## What This Represents

MetaDyn is not just a Unity project. It is a platform product made of:
- a reusable Unity SDK/platform layer
- a starter space/template layer
- a hosted/self-hosted deployment model
- identity, presence, moderation, and voice systems

## Documents In This Section

- `platform-overview.md` — product/platform definition and purpose
- `system-architecture.md` — core technical architecture and major systems
- `core-systems.md` — platform subsystems and implementation patterns
- `deployment-hosting.md` — hosting, deployment, Cloudflare, and per-space delivery model
- `import-notes.md` — source import summary and mapping from imported `.claude` docs

## Source Basis

These docs were organized from imported platform material located under:
- `/import/unity6-docs/.claude/`

Primary source categories included:
- startup summary and quick reference docs
- changelog and decision logs
- infrastructure reference
- platform PRD and planning material
