# MetaDyn Product Requirements Document

**Status:** Working PRD  
**Last Updated:** 2026-03-03  
**Owner:** MetaDyn  
**Document Type:** Reverse-derived PRD from current system + confirmed planning decisions

---

## 1. Purpose

This PRD defines the current and forward product requirements for MetaDyn as a deployable metaverse platform, Unity SDK, and hosted/self-hosted space system.

This document is intentionally written **after significant implementation already exists**.

That means:
- some sections describe current implemented reality
- some sections define forward requirements based on decisions already made
- some sections identify gaps between current implementation and intended product state

This PRD should become the main working product document moving forward.

---

## 2. Product Vision

MetaDyn is a creator-first metaverse platform that combines:

- a Unity-based SDK
- reusable platform infrastructure
- embodied AI systems
- deployable WebGL spaces
- authentication, identity, and hosting workflows
- optional managed/shared hosting and self-hosting models

MetaDyn should enable creators, studios, and enterprise teams to:
- build immersive multi-user spaces
- deploy those spaces to the web
- integrate AI, voice, avatars, and platform services
- operate either in self-hosted or MetaDyn-managed environments

The long-term product goal is to offer:
- Spatial-style ease of use
- stronger openness and platform control
- enterprise-grade flexibility
- a modern SDK-driven creator experience

---

## 3. Product Definition

MetaDyn is made of three distinct but related product layers:

### 3.1 MetaDyn SDK

MetaDyn-owned reusable platform/runtime/editor systems installable into Unity projects.

Includes:
- runtime systems
- editor tooling
- deployment tooling
- auth integration
- AI embodiment systems
- WebGL bridges
- networking/dependency integration

### 3.2 MetaDyn Starter Space Template

A separate MetaDyn-owned Unity starter project/template that includes:
- the MetaDyn SDK
- a basic starter environment
- ready-to-build starter world setup

### 3.3 MetaDyn Hosted Platform

The runtime and hosting layer that powers deployed spaces.

Includes:
- WebGL deployment model
- auth/session handling
- hosting models
- dashboard/backend integration
- shared hosting and self-hosting support

---

## 4. Target Users

### 4.1 Primary Users

- Unity creators building immersive spaces
- indie teams and studios
- agencies building branded activations
- enterprise innovation teams

### 4.2 Secondary Users

- studios delivering spaces on behalf of clients
- technical partners integrating AI/avatar systems
- platform admins and moderators
- community organizers and event hosts

### 4.3 Internal/Strategic Users

- MetaDyn platform team
- deployment/ops users
- strategic partners such as immersive studios and enterprise delivery partners

---

## 5. Product Goals

### 5.1 Core Goals

1. Enable creators to build and deploy multi-user WebGL spaces with minimal platform friction.
2. Provide a reusable Unity SDK that carries the MetaDyn platform layer into each space.
3. Make deployment a first-class SDK capability, not a disconnected ops workflow.
4. Deliver embodied AI as a native differentiator.
5. Support both self-hosted and shared-hosted deployment models.
6. Create a sustainable commercial structure around the open platform.

### 5.2 Product Experience Goals

1. Unity-native workflow
2. clear deployment path
3. strong auth/session continuity
4. high-quality voice/avatar interaction
5. enterprise-capable but creator-friendly platform model

---

## 6. Non-Goals

MetaDyn is not currently trying to be:
- a generic no-code site builder
- a mobile-first gaming platform
- a pure marketplace product without platform ownership
- a single-scene one-off demo stack
- a platform where deployment tooling is external to the SDK

---

## 7. Core Product Pillars

### 7.1 Unity SDK Platform Layer

The SDK is the reusable product foundation.

Requirements:
- installable into existing Unity projects
- carries platform runtime/editor/deployment systems
- includes MetaDyn-owned platform logic required by spaces
- supports versioning and update flow

### 7.2 Space Deployment

Each space is its own build.

Requirements:
- WebGL deployment pipeline
- per-space runtime config
- deploy from Unity editor
- support self-hosting and shared hosting

### 7.3 Identity and Access

Requirements:
- web-first auth
- session continuity across spaces/subdomains
- profile and avatar persistence
- owner/admin identification

### 7.4 Embodied AI

Requirements:
- voice input/output
- spatial awareness
- vision support
- movement/gaze
- persistent memory

### 7.5 Social / Multiplayer

Requirements:
- Photon Fusion-based multiplayer
- user list / moderation
- voice communication
- synchronized identity and presence

---

## 8. Current Confirmed Technical Foundation

Current documented stack:

- `Unity 6` (`6000.0.62f1` documented baseline)
- `URP 17.0.4`
- `Photon Fusion 2.0.9 Stable`
- `WebGL` primary target
- `Supabase` auth/profile backend
- `Cloudflare` CDN/DNS/SSL/edge
- `WebRTC` player voice
- `OpenRouter`, `Whisper`, `ElevenLabs`
- `Ready Player Me`
- browser `jslib` bridge integrations

---

## 9. Functional Requirements

## 9.1 Unity SDK

The MetaDyn SDK must:
- install into existing Unity projects
- provide reusable runtime/editor systems
- include deployment tooling
- include dashboard/editor surfaces for status and updates
- validate required dependencies
- support future remote update checks

The SDK must not require full starter-space content to be usable.

## 9.2 SDK Update System

Requirements:
- SDK must know its installed version
- SDK must check a remote manifest/release source
- Unity `MetaDyn Dashboard` must show:
  - installed version
  - latest version
  - update status
  - update action button
- `Update SDK` button must be disabled when current
- update logic must use current working file layout as canonical path target

Current status:
- UI exists in mock form
- real manifest file exists
- remote fetch is not yet implemented

## 9.3 Dependency Management

Requirements:
- Photon Fusion is a required dependency
- supported Fusion version must be explicit
- dashboard must show:
  - supported Fusion version
  - installed Fusion version
- Fusion should be treated as part of supported installation flow

Current supported version:
- `Photon Fusion 2.0.9 Stable`

## 9.4 Deployment Tooling

Requirements:
- deployment tooling is part of the SDK
- deploy from Unity Editor
- support SSH/rsync/scp style deployment paths
- support per-space isolated build deployment
- support runtime-config-driven deployment metadata
- report status to the user inside Unity

Current deployment rule:
- each space is its own build

## 9.5 Hosting Models

Requirements:
- support self-hosting
- support shared hosting
- retain per-space build isolation
- allow some infrastructure/platform values to be dashboard-configurable

## 9.6 Authentication

Requirements:
- web-first auth
- shared-cookie/session continuity
- Unity WebGL auth bootstrap
- profile loading and avatar persistence
- dashboard-linked identity model

## 9.7 Multiplayer and User Management

Requirements:
- player spawning and joining
- room/session handling
- user list and moderation
- admin ownership model
- synchronized names and presence

## 9.8 Voice and Communication

Requirements:
- AI push-to-talk microphone recording
- player-to-player voice
- lip sync
- WebGL-compatible voice path

Important current runtime requirement:
- `Assets/StreamingAssets/microphone-processor.js` is required by the active microphone worklet path

## 9.9 Embodied AI

Requirements:
- environmental perception
- vision-enabled multimodal interaction
- autonomous movement
- gaze/head tracking
- persistent memory
- action-tag-driven behavior

## 9.10 Dashboard / Backend Sync

Requirements:
- selected metadata should sync between Unity and backend/dashboard
- creator auth in editor should not require unsafe service-key handling
- dashboard should eventually influence selected infra/platform settings

---

## 10. UX Requirements

### 10.1 Unity Creator UX

Creators should be able to:
- open Unity and see MetaDyn status
- see SDK version and update status
- see Fusion version status
- configure/deploy spaces from editor tooling
- work with platform systems without rebuilding the platform manually

### 10.2 Space User UX

End users should be able to:
- authenticate smoothly
- enter spaces with persistent identity
- spawn correctly into a deployed world
- use voice and multiplayer features
- interact with AI-enabled experiences

---

## 11. Canonical File Ownership (Current Product Reality)

The current working file layout is the source of truth for SDK/update planning.

Canonical SDK/platform-owned paths currently include:
- `Assets/MetaDyn`
- `Assets/Common`
- `Assets/Plugins/WebGL`
- `Assets/Pavilion/Scripts/GameManager.cs`
- `Assets/Pavilion/Scripts/Player.cs`
- `Assets/Pavilion/Scripts/PlayerInput.cs`
- `Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs`
- `Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs`
- `Assets/Photon`
- `Assets/StreamingAssets/microphone-processor.js`

This is important because:
- update/install logic must target these existing working paths
- the PRD should reflect product reality, not an imaginary future structure

---

## 12. Business / Commercial Requirements

MetaDyn must support a business model that keeps the platform open where it matters while monetizing:
- managed convenience
- hosting
- support
- visibility
- enterprise outcomes

Current monetization planning areas:
- memberships
- sponsorships
- strategic partnerships
- enterprise/platform partnerships

---

## 13. Strategic Partnership Requirement

MetaDyn should actively support strategic studio/platform partnerships that increase:
- delivery capacity
- platform credibility
- enterprise reach
- flagship project quality
- differentiated AI/avatar experiences

Strategic partnerships may influence:
- platform build priorities
- AI roadmap
- avatar/holographic initiatives
- enterprise go-to-market structure

---

## 14. Security / Compliance Expectations

Current expectations:
- HTTPS/SSL by default
- secure auth/session validation
- avoid exposing backend service credentials in client/editor flows
- use developer tokens and controlled auth paths where needed

Areas to keep tightening:
- deployment auth handling
- SSH trust/security tradeoffs
- editor token storage hygiene
- permissioning around deployment ownership

---

## 15. Operational Requirements

MetaDyn must support:
- build and deployment repeatability
- per-space isolation
- admin/ownership clarity
- version visibility
- dependency visibility
- manageable update paths

Eventually it should also support:
- staging/prod distinctions
- rollback/version history
- team/organization permissions

---

## 16. Current Product Gaps

The following are known gaps between current implementation and intended product state:

1. SDK update UI is live, but remote manifest fetch is not yet implemented
2. SDK packaging/distribution flow is not fully productized yet
3. managed/shared hosting flows need deeper definition
4. dashboard-driven infra configuration needs clearer field boundaries
5. deployment governance/permissions need more definition
6. long-term package/install/update mechanics still need to be completed

---

## 17. Success Criteria

MetaDyn is succeeding when:

### Creator Success
- a creator can install the SDK into a project
- configure a space
- deploy a space
- authenticate users
- use voice/multiplayer/AI features

### Platform Success
- spaces deploy reliably
- SDK updates are visible and manageable
- hosting models support both self-host and managed/shared needs
- identity and runtime metadata stay coherent

### Business Success
- platform supports paid memberships/sponsorships/enterprise partnerships
- strategic partners can build and deliver with MetaDyn
- flagship use cases validate the platform as a real alternative in the market

---

## 18. Immediate Next Steps

1. Implement real manifest fetch in `MetaDynDashboard`
2. Finalize GitHub/repo source-of-truth for SDK update flow
3. Continue curating SDK-owned file set based on canonical current layout
4. Define managed/shared hosting workflow in more detail
5. Define dashboard-configurable infra fields
6. Continue packaging/dependency planning around Fusion and SDK distribution

---

## 19. Related Documentation

- `.claude/Quick Reference/QUICK_REFERENCE.md`
- `.claude/Quick reference/SDK_DEVELOPMENT.md`
- `.claude/Quick reference/SDK_TOOLKIT_INVENTORY.md`
- `.claude/Quick reference/SDK_UPDATE_MANIFEST.md`
- `.claude/Quick reference/DEPLOYMENT_ARCHITECTURE.md`
- `.claude/Quick reference/AUTH_SYSTEM.md`
- `.claude/Quick reference/AI_EMBODIMENT.md`
- `.claude/Quick reference/INFRASTRUCTURE.md`
- `.claude/Planning/Sponsorship_And_Membership_Worksheet.md`
