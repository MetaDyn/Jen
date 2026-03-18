# Unity 6 SDK Productization

This document captures the current MetaDyn SDK boundary, packaging direction, update model, and productization gaps between the working Unity project and the installable platform MetaDyn intends to ship.

## Executive Summary

MetaDyn is not just building a Unity scene collection. It is building a reusable platform layer that should eventually be installable into other Unity projects.

The current documented product shape has three related parts:
- **MetaDyn SDK** — reusable runtime/editor/platform systems
- **MetaDyn Starter Space Template** — a MetaDyn-owned starter project or environment built on top of the SDK
- **MetaDyn Hosted Platform** — the deployment/runtime/backend layer that makes spaces operational on the web

The practical challenge is that the current codebase already contains much of this functionality, but the package boundaries are still transitional.

## Current Product Boundary

### What Counts As SDK Today

The imported inventory docs define the current core SDK/update scope as:
- `Assets/MetaDyn/**`
- `Assets/Plugins/WebGL/**` for MetaDyn browser bridge files
- `Assets/StreamingAssets/microphone-processor.js`
- several baseline platform files that still live outside `Assets/MetaDyn`

### Important Transitional Reality

Some files are still structurally outside the future ideal SDK folder layout, but they are functionally part of the platform.

The most important documented examples are:
- `Assets/Common/UIGameMenu.cs`
- `Assets/Common/UIGameMenu.prefab`
- `Assets/Pavilion/Scripts/GameManager.cs`
- `Assets/Pavilion/Scripts/Player.cs`
- `Assets/Pavilion/Scripts/PlayerInput.cs`
- `Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs`
- `Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs`

These should not be mentally dismissed as project glue just because of where they live today.

## Canonical Current SDK-Owned Paths

The imported manifest and PRD material repeatedly treat the following paths as canonical update/install targets:
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

That is important for two reasons:
1. the updater should not invent a fantasy file layout that the working project does not use
2. product docs should reflect current operational reality, not only future cleanup goals

## Why Productization Matters

Without clear SDK boundaries, MetaDyn risks several problems:
- hard-to-maintain updates
- fuzzy distinction between reusable platform code and one-off world logic
- unsafe overwrite behavior during updates
- weak install story for external creators or partner teams
- confusion about what belongs in the SDK versus the starter template

Productization is what turns “we have a sophisticated project” into “we have a platform.”

## Current SDK Scope Categories

### 1. Runtime Systems
Examples from the imported docs:
- core reusable components such as `SeatHotspot`, `Interactable`, `ProjectionSurface`, `Trigger`, and `EntrancePoint`
- managers such as `InputManager`, `SettingsManager`, and `UIManager`
- auth/runtime bridges
- AI embodiment systems
- user list and social systems
- WebRTC and audio integration

### 2. Editor Tooling
Examples:
- `MetaDynDashboard`
- `MetaDynMenu`
- `MetaDynProjectConfig`
- `MetaDynDeploymentManager`
- `MetaDynServerProfile`

These are crucial because MetaDyn’s platform experience is intentionally Unity-native, not “download some files and fend for yourself.”

### 3. Browser / WebGL Bridge Layer
Examples:
- `AuthBridge.jslib`
- `MicrophonePlugin.jslib`
- `ProjectionSurface.jslib`
- `WebRTCVoice.jslib`
- `microphone-processor.js`

These are part of the SDK story because the primary target is WebGL.

## SDK Experience Goals

The imported docs already point toward a productized creator experience inside Unity.

Expected UX:
- open Unity
- see MetaDyn SDK status in the dashboard
- see installed version and latest version
- see supported Fusion version and installed version
- check for updates
- update safely when appropriate
- eventually browse/install optional components

This matters because MetaDyn is not just shipping runtime scripts. It is shipping a creator workflow.

## Update System Direction

### Current Status
Documented current state includes:
- a real local SDK manifest file exists
- the Unity dashboard already shows mock update UI
- Photon Fusion version visibility is already planned into the dashboard surface
- the real missing piece is remote manifest fetch and a safe update execution path

### Current Manifest Direction
The imported manifest planning includes fields for:
- SDK version
- channel (`stable`, later possibly `beta`)
- Unity version compatibility
- Photon Fusion compatibility
- download/release notes URLs
- tracked roots

That is the correct shape for a practical updater.

### Important Operational Principle
The update system must preserve project-specific content and avoid blindly overwriting user work.

That means update productization needs:
- tracked roots
- local-modification awareness
- compatible-version checks
- migration notes when needed
- a safe user-controlled flow rather than silent mutation

## Photon Fusion As A Product Dependency

The docs are explicit that Photon Fusion is a required dependency of the MetaDyn SDK.

Current supported version:
- `Photon Fusion 2.0.9 Stable`

That should remain visible in the docs because the SDK is not complete without its required networking substrate.

MetaDyn should treat Fusion as:
- a required dependency in install/update planning
- a clearly surfaced compatibility item in the editor dashboard
- part of the supported installation contract

## The MetaDyn Bridge / Service Direction

The imported SDK docs point at an architectural improvement that would make productization stronger: a clearer central bridge/service model rather than direct singleton discovery everywhere.

Suggested future direction includes:
- a central `MetaDynBridge` or equivalent entry point
- explicit subsystem interfaces for auth, users, AI, voice, deployment, and runtime config
- cleaner separation between stable SDK-facing contracts and project-level implementation details

This is not yet the full current implementation, but it is a useful north star for documentation and refactoring decisions.

## Starter Template vs SDK

The documentation should keep this distinction sharp.

### MetaDyn SDK
Reusable systems that should travel across projects.

### MetaDyn Starter Space Template
A MetaDyn-owned starter environment built using the SDK, including baseline world setup and content scaffolding.

### Project-Specific Content
Environment-specific assets, scene polish, and world-specific glue that should not be treated as part of the reusable SDK by default.

This distinction is one of the main things that prevents future update pain.

## Deployment Tooling Belongs In The SDK

One of the most important product decisions in the imported docs is that deployment tooling is not separate ops garnish. It is part of the SDK.

That means:
- creators should be able to reason about deployment from inside Unity
- deployment/version/config surfaces belong in the MetaDyn dashboard/menu story
- the SDK is partly a runtime package and partly a creator operations surface

That is a stronger and more ambitious product stance than a conventional “asset pack.”

## Current Packaging Gaps

The imported docs are already honest about the current gaps.

Most important ones:
1. SDK packaging/distribution is not fully productized yet
2. remote manifest fetch is not yet implemented
3. file boundaries still reflect transitional project history
4. update/install safety mechanisms need more detail
5. optional component/catalog install flow is still planned, not realized
6. the final package/install story for external use is still being formed

## Documentation Guidance

The docs should present the SDK as:
- **real and already substantial**
- **not yet fully packaged or distributed in final form**
- **clearly separated in concept even when some files are still transitional in placement**

That is more accurate than either “it is already a finished package product” or “it is just a Unity project with some helpers.”

## Recommended Structure For The Curated Docs

The normalized docs should keep pointing readers to four distinct concerns:
1. what the SDK is
2. what files currently belong to it
3. how deployment and hosting tie into it
4. what remains to be productized before it is a clean install/update product

## Key Open Questions

1. Which out-of-folder baseline files should be moved into cleaner SDK/package boundaries first?
2. What update behavior is allowed when creators have modified SDK-owned files locally?
3. What is the final distribution mechanism: GitHub releases, package feed, OpenUPM-compatible path, or a hybrid?
4. Which systems are baseline SDK versus optional installable modules?
5. What is the exact division between SDK and starter-space template over time?

## Source Basis

Primary imported sources used in this synthesis:
- `import/unity6-docs/.claude/Quick Reference/SDK_DEVELOPMENT.md`
- `import/unity6-docs/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`
- `import/unity6-docs/.claude/Quick Reference/SDK_UPDATE_MANIFEST.md`
- `import/unity6-docs/.claude/Planning/MetaDyn_Platform_PRD_v1.0.md`
