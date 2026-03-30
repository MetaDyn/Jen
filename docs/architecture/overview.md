# Architecture Overview

## Mission Context

MetaDyn — Metaverse Dynamix — is a metaverse builder creating a connected digital fabric that links identity, presence, immersive environments, and advanced AI avatars into a persistent metaverse ecosystem.

It builds both:
- the connective layer across platforms
- and immersive spaces for brands, enterprises, and creators

MetaDyn is also both:
- **MetaDyn, LLC**, registered in Missouri, United States
- an open-source-oriented builder community with its primary social gravity on Discord

This direction is grounded in more than 20 years of cumulative experience, with especially heavy metaverse-platform work over the last 3 years, including substantial work on Spatial.io and its Unity toolkit. Spatial is no longer a good fit for MetaDyn or its clients, which is a key reason MetaDyn is building a next-generation alternative.

## Core Architecture Themes

### 1. Identity
Users, agents, and avatars must maintain recognizable identity across multiple platforms and surfaces.

### 2. Presence
Presence should persist across environments and platforms, allowing continuity of interaction rather than isolated, one-off sessions.

### 3. Intelligence
AI avatars and orchestration agents should be capable, context-aware, and available across the ecosystem.

### 4. Memory
A unified, persistent memory model should support continuity across platforms, environments, and interactions.

### 5. Immersive Delivery
Experiences are deployed across multiple immersive/web-native stacks including Unity WebGL, ThreeJS, and Hyperfy.

## Control Plane

Jen serves as the central orchestrator for documentation, context management, operational coordination, and system-level assistance through OpenClaw running on GPT Codex 5.4.

The intended operating model is collaborative and multi-agent:
- several human collaborators work alongside Jen
- Jen acts as the main orchestrator
- a set of roughly 6 subordinate agents can operate beneath Jen
- those agents may have both individual specialties and composable/compounded skills

This implies that the architecture should eventually document not just platform systems, but also:
- orchestration hierarchy
- agent roles and boundaries
- skill ownership
- delegation patterns
- memory/context-sharing rules
- human-in-the-loop control points

## To Be Expanded

Future revisions should document:
- identity model
- presence model
- memory model
- orchestration flows
- platform integration boundaries
- data ownership and synchronization patterns
- environment boundaries between local, VPS, and cloud systems
