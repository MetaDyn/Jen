# Jen

Jen is the operational and documentation hub for MetaDyn's metaverse systems.

## Purpose

This repository serves as the control-plane workspace for:
- architecture documentation
- infrastructure documentation
- AI orchestration notes
- platform/system runbooks
- environment standards and operating conventions

## High-Level Context

MetaDyn — short for **Metaverse Dynamix** — is a metaverse builder creating both the connective fabric across platforms and the immersive spaces that run on it.

MetaDyn is both:
- **MetaDyn, LLC**, registered in Missouri, United States
- a vibrant open-source-oriented builder community centered primarily around Discord

Its work serves:
- brands
- enterprises
- creators

The broader mission spans:
- identity across platforms
- persistent presence across digital environments
- immersive spaces across multiple runtimes
- advanced AI avatars on multiple platforms
- unified, persistent memory across experiences and systems

MetaDyn brings more than 20 years of cumulative experience, with especially heavy metaverse-platform work over the last 3 years, including substantial work on Spatial.io and its Unity toolkit. Spatial is no longer a strong fit for MetaDyn or its clients, so MetaDyn is building a next-generation alternative.

Jen runs on OpenClaw using GPT Codex 5.4 and acts as the main orchestrator for this environment.

## Infrastructure Shape

Current infrastructure is hybrid and distributed across:
- on-premise systems
- cloud infrastructure
- multiple VPS/providers
- primarily AWS for hosted immersive experiences

Hosted experience platforms currently include:
- Unity WebGL
- ThreeJS
- Hyperfy immersive spaces

## Repository Layout

- `docs/architecture/` — system concepts, orchestration, and high-level design
- `docs/company/` — company identity, mission, and top-level positioning
  - `docs/company/positioning.md` — canonical positioning drafts and mission language
- `docs/infrastructure/` — hosting, topology, environments, and deployment surfaces
- `docs/platforms/` — platform-specific implementation notes
  - `docs/platforms/unity6/` — MetaDyn Unity 6 platform documentation
- `docs/ai-systems/` — Jen, OpenClaw, Codex, memory, and orchestration docs
  - `docs/ai-systems/agent-orchestration-and-remote-subagents.md` — Jen control-plane model and proposed remote subagent API contract
  - `docs/ai-systems/remote-subagent-api-layer.md` — detailed remote subagent API layer spec with sample requests and reference code
- `docs/runbooks/` — operational procedures and setup guides
  - `docs/runbooks/local-static-demo-server.md` — workaround for serving LAN-accessible static demos when gateway approvals fail
- `docs/standards/` — naming, conventions, security, and documentation practices

## Notes

This repo should contain curated documentation, safe operational context, and automation helpers.

Do not commit:
- credentials
- secrets
- API keys
- tokens
- raw sensitive operational data unless intentionally sanitized
