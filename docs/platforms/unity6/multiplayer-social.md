# Unity 6 Multiplayer, Presence, And Social Systems

This document captures the current social-runtime model of the MetaDyn Unity 6 platform: player networking, identity-in-session, moderation, spawning, and realtime voice presence.

## Executive Summary

MetaDyn’s Unity runtime is built around a clear product goal: users should enter a shared world with persistent identity, realtime voice, and enough moderation/control primitives to make the experience feel like a platform instead of a demo.

As of the 2026-05-25 UGS production sprint milestone, the active Starter runtime path should be understood as **UGS/NGO-first** rather than Fusion-first. Older Fusion language in this document remains useful as implementation history/reference context, but should not be mistaken for the declared active production baseline on the migrated branch.

The current documented foundation is:
- Photon Fusion multiplayer
- Shared Mode networking
- per-player authority over player objects
- host/state-authority control over shared moderation state
- synchronized user list and presence
- integrated WebRTC player voice
- persistent identity context supplied by Supabase-backed profile data

## Current Technical Baseline

Documented stack:
- Unity 6 (`6000.0.62f1`)
- URP 17.0.4
- Photon Fusion 2.0.9 Stable
- Shared Mode networking
- WebGL-first deployment target
- WebRTC for player-to-player voice chat

## Core Social Runtime Principles

### 1. Identity Should Carry Into Session
Players should not enter as arbitrary anonymous scene entities if the platform already knows who they are.

### 2. Moderation Must Exist At The Runtime Layer
Even early-stage spaces need ownership, admin context, and tools like kick/ban/block.

### 3. Voice Is A Core Social Primitive
Voice is not an optional novelty feature. It is central to the feeling of presence.

### 4. The Runtime Must Stay WebGL-Realistic
Everything needs to respect browser constraints, multiplayer synchronization realities, and future scale limits.

## Player And Session Model

### Player Objects
The documented current authority pattern is:
- each player object owns its own player behavior/state path where appropriate
- each player has authority over their own player object
- host/state authority manages shared systems that require centralized control

This allows player-local movement and interaction while keeping moderation and canonical shared lists on the authoritative side.

### Spawning
Current spawning behavior includes:
- room/session join flow driven by runtime config
- spawn point selection through `EntrancePoint` markers
- auto-join behavior based on the configured room name
- avatar selection continuity driven by persisted profile data

### Name And Presence
Presence is intended to be legible in-world and in UI.

The imported references describe support for:
- synchronized names
- name tags
- user list UI
- profile-linked display context

## Key Files

Important currently documented files include:
- `Assets/Pavilion/Scripts/Player.cs`
- `Assets/Pavilion/Scripts/GameManager.cs`
- `Assets/Pavilion/Scripts/PlayerInput.cs`
- `Assets/Common/UIGameMenu.cs`
- `Assets/MetaDyn/Core/Runtime/Components/EntrancePoint.cs`
- `Assets/MetaDyn/UserList/UserListManager.cs`
- `Assets/MetaDyn/UserList/UserData.cs`
- `Assets/MetaDyn/UserList/UserListUI.cs`
- `Assets/MetaDyn/UserList/UserListEntry.cs`
- `Assets/MetaDyn/Managers/WebRTCManager.cs`

## User List System

The user list is one of the clearest indicators that MetaDyn is treating multi-user presence as a first-class system.

### What It Tracks
The documented system tracks at least:
- who is in the space
- player names
- moderation-relevant permission context
- join/leave changes

### Current Synchronization Pattern
The imported docs describe the user list as being built around a `NetworkDictionary` and authority-controlled registration flow.

Typical pattern:
- player joins
- player registers with the authoritative user list system through RPC
- authoritative list updates
- other clients receive synchronized list state

### Why This Matters
A synchronized user list is not just admin tooling. It is also:
- social proof that the space is alive
- a simple presence layer
- a launch point for moderation and future social features

## Permission And Moderation Model

### Current Permission Levels
Documented permission levels:
- `0` = User
- `1` = Moderator
- `2` = Admin

### Current Moderation Actions
The imported docs reference support for:
- block
- kick
- ban

### Current Admin Resolution
There are two important documented patterns:

#### Fallback Pattern
If no stronger ownership model is supplied, the first player can become admin automatically.

#### Preferred Current Ownership Pattern
More recent infra docs describe a database-driven admin check where the player’s authenticated Supabase user ID is compared against the configured `ownerId` stored in `MetaDynRuntimeConfig`.

This is the better platform direction because it ties authority to real identity instead of session join order.

## Multiplayer Architecture Pattern

### Shared State vs Local State
The current model uses a mixture of:
- networked properties for replicated player/session state
- `NetworkDictionary` for shared user list state
- RPCs for actions that need authority validation
- local-only state for client UI/input behavior

### Join-In-Progress
The current architecture is intended to support late joiners seeing the current shared player/user state rather than requiring a fresh session.

That matters for platform behavior, events, and persistent-style spaces.

## Social UX Layer

The imported docs make clear that MetaDyn is not only trying to synchronize transforms.
It is trying to deliver a usable social space.

Current pieces include:
- tab-toggleable user list UI
- context-menu-driven user controls
- name tags
- avatar continuity
- input locking so chat/UI use does not break movement handling
- settings and menu surfaces that support real use, not just testing

## Voice As Presence

### Current Voice Model
Player-to-player voice currently uses browser-native WebRTC.

This provides:
- realtime player voice
- spatial audio behavior
- avatar lip sync integration
- browser-compatible voice transport for WebGL spaces

### Why It Is Important
Without voice, multiplayer can still function technically, but the social layer feels much thinner.
For MetaDyn’s target use cases, voice is part of the baseline experience.

### Current Limitation
The current voice topology is mesh-based P2P WebRTC. That works for the current target range, but it has an obvious scale ceiling. Future migration to an SFU such as LiveKit or a Cloudflare-based realtime stack is already documented as the next path once larger rooms justify it.

## Current Scale Assumption

The imported docs consistently describe a current target around:
- up to 50 users per session

Important caveat:
- networking and especially voice bandwidth remain topology-dependent
- the current ceiling is practical, not theoretical
- large-room voice will eventually require a different media architecture

## Relationship To Identity

The multiplayer system should not be documented in isolation from auth.

It depends on:
- authenticated user identity
- persisted profile data
- owner/admin identity resolution
- coherent cross-space naming/avatar continuity

That means the actual social runtime is the combination of:
- auth and profile
- multiplayer transport
- moderation systems
- voice systems
- in-world UI and player bootstrap

## What Is Already Strong

### Real Moderation Direction
MetaDyn already has an actual permission model instead of punting moderation to future planning.

### Real Presence Layer
User list, name tags, and profile-linked spawning together create a meaningful presence baseline.

### Voice Is Not Hand-Waved
The docs do not treat voice as a vague future aspiration. It is implemented enough to shape the platform architecture and scale planning.

### Platform-Oriented Player Bootstrap
The player/session layer already reflects platform requirements rather than a one-off game scene.

## What Still Needs Sharper Productization

1. clearer documentation of exact authority boundaries for each major social subsystem
2. a more explicit distinction between current verified scale and aspirational scale
3. tighter docs around moderation persistence and ban/block semantics
4. future cross-runtime social continuity planning, especially if Unity and Hyperfy share user identity and account-level social surfaces
5. documentation for team/org roles once the platform grows beyond single-owner admin assumptions

## Recommended Product Framing

The docs should describe the current Unity social stack as:
- a real production-leaning alpha foundation
- already beyond prototype status in core social architecture
- still needing future scale and product-surface hardening

That framing is more accurate than either extreme of underselling or overselling it.

## Cross-References That Should Stay Tight

This document should stay linked to:
- auth/identity docs for canonical user identity and owner resolution
- deployment docs for session/public-hosting context
- voice/realtime docs for media-layer details
- SDK/productization docs for which runtime files are truly part of the platform package

## Source Basis

Primary imported sources used in this synthesis:
- `import/unity6-docs/.claude/Quick Reference/QUICK_REFERENCE.md`
- `import/unity6-docs/.claude/Quick Reference/INFRASTRUCTURE.md`
- `import/unity6-docs/.claude/Planning/MetaDyn_Platform_PRD_v1.0.md`
- `import/unity6-docs/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`
