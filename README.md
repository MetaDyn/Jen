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

MetaDyn is building an advanced, connected digital fabric described as the metaverse. That work spans:
- identity across platforms
- persistent presence across digital environments
- advanced AI avatars on multiple platforms
- unified, persistent memory across experiences and systems

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
- `docs/infrastructure/` — hosting, topology, environments, and deployment surfaces
- `docs/platforms/` — platform-specific implementation notes
  - `docs/platforms/unity6/` — MetaDyn Unity 6 platform documentation
- `docs/ai-systems/` — Jen, OpenClaw, Codex, memory, and orchestration docs
- `docs/runbooks/` — operational procedures and setup guides
- `docs/standards/` — naming, conventions, security, and documentation practices

## Notes

This repo should contain curated documentation, safe operational context, and automation helpers.

Do not commit:
- credentials
- secrets
- API keys
- tokens
- raw sensitive operational data unless intentionally sanitized
