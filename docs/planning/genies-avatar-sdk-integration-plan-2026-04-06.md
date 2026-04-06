# Genies Avatar SDK Integration Plan

## Purpose

Define a practical integration plan for bringing the Genies Avatar SDK into MetaDyn Pavilion without breaking the current Ready Player Me and Avatar SDK avatar flows, input flow, multiplayer spawn flow, or WebGL-first platform assumptions.

This document is intentionally grounded in:

- the current MetaDyn Pavilion codebase
- the current Genies Avatar SDK documentation
- current known product constraints around WebGL, Fusion multiplayer, and existing avatar selection flows

## Executive Summary

Genies can be integrated into the MetaDyn platform, but it should not be treated as a drop-in third avatar prefab family.

The current MetaDyn architecture assumes:

- avatar choice is prefab-driven
- local player control uses the old Unity Input Manager APIs
- WebGL is the primary production target
- voice lip sync is avatar-family-specific and manually wired

The current Genies documentation indicates:

- URP is required
- the Bootstrap Wizard expects Active Input Handling to be switched to `New`
- developer registration requires a Genies app with client ID and client secret
- the Avatar SDK currently supports builds for:
 - iOS
 - Android
 - Windows Standalone
- WebGL is not currently supported and is only listed as a planned future platform

Because MetaDyn Pavilion is WebGL-first, the correct product strategy is:

1. treat Genies as a phased avatar-provider integration, not an immediate global replacement
2. isolate Genies behind a MetaDyn avatar-provider abstraction
3. keep current Ready Player Me and Avatar SDK flows alive during the transition
4. run the first Genies implementation as a native-only integration track or gated prototype track until official WebGL support exists or a validated workaround is proven

## Primary Source Findings

### Genies SDK Requirements and Constraints

From the current Genies docs:

- Installation is done through the Unity Asset Store package import plus the Genies Bootstrap Wizard
- The SDK must be used in a URP project
- The Bootstrap Wizard configures project prerequisites and asks the project to switch Active Input Handling to `New`
- Project registration requires:
 - a Genies Developer Portal account
 - a Genies app
 - client ID
 - client secret
- The SDK supports Unity 2022.3.62f2 or later, including Unity 6
- Current documented supported build targets are:
 - iOS
 - Android
 - Windows Standalone
- WebGL is currently listed under planned future build support, not current support

### Genies Runtime Model

The docs show that Genies is not just a static imported mesh workflow.

The SDK centers around:

- `Genies.Sdk.AvatarSdk`
- login flows
- loading global avatars from Genies-backed definitions
- loading local/default avatars from local definitions
- a `ManagedAvatar` object that exposes the runtime avatar root and animator
- an Avatar Editor framework for user customization

That means the correct integration model is runtime avatar loading plus MetaDyn-side controller binding, not manually authoring a large library of prebuilt Genies player prefabs.

## Current MetaDyn Pavilion State

## Current Input Model

Current local player control is handled by:

- `Assets/Pavilion/Scripts/PlayerInput.cs`

This script currently uses the legacy Unity input APIs:

- `Input.GetMouseButton`
- `Input.GetAxisRaw`
- `Input.GetAxis`
- `Input.GetButtonDown`
- `Input.GetButton`

The current project setting is:

- `ProjectSettings/ProjectSettings.asset`
- `activeInputHandler: 0`

This means the project is still configured for the old input manager, while the Genies install flow explicitly expects the new Input System.

This is the first concrete integration conflict.

## Current Player / Avatar Runtime Model

The current player stack is centered on:

- `Assets/Pavilion/Scripts/Player.cs`
- `Assets/Pavilion/Scripts/PlayerInput.cs`
- `Assets/Pavilion/Scripts/GameManager.cs`

Current behavior:

- `GameManager` selects a player avatar by prefab index
- avatar options are split into two lists:
 - Ready Player Me avatars
 - current Avatar SDK avatars
- local selection is stored in `PlayerPrefs`
- the selected prefab is spawned directly through Fusion

This architecture works for fixed prefab variants, but it is not yet designed for a runtime-loaded avatar identity provider such as Genies.

## Current Avatar Families

The project currently has two avatar families exposed in the main flow:

- Ready Player Me
- Avatar SDK avatars

The UI for avatar selection also assumes these two buckets:

- `Assets/Common/UIGameMenu.cs`

This means Genies integration affects:

- UI grouping
- player spawn logic
- avatar persistence
- potentially auth and profile data

## Current Lip Sync / Voice Coupling

Current avatar-family-specific lip sync scripts:

- `Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs`
- `Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs`

Current WebRTC voice code explicitly looks for these specific script types:

- `Assets/MetaDyn/Managers/WebRTCManager.cs`
- `Assets/MetaDyn/Managers/WebRTCAudioReceiver.cs`

This means Genies is not just an avatar loading task. It also requires a third avatar-family adapter for:

- lip sync
- head/face binding
- remote speaking state

## Current Multiplayer / Identity Coupling

The current multiplayer spawn model assumes:

- one spawned network prefab per player
- local player identity comes from current auth/name state
- avatar identity is selected by prefab index before spawn

Genies introduces a new kind of identity data:

- Genies login state
- Genies user ID
- Genies avatar definition or avatar profile reference

That data is not currently represented in the networked player payload or user data structures.

## Core Integration Risks

## Risk 1: WebGL Product Mismatch

This is the biggest issue.

MetaDyn Pavilion is WebGL-first, but the current Genies Avatar SDK documentation only lists:

- iOS
- Android
- Windows Standalone

as supported build targets.

WebGL is only mentioned in the planned features page, which means:

- a production Pavilion WebGL rollout should not depend on Genies in the near term
- any Genies integration should be behind platform gating until proven safe
- this should be treated as an R&D or secondary-platform track first

## Risk 2: Input System Migration Cost

The current Pavilion control path still depends on the old Input Manager.

Genies installation explicitly expects switching Active Input Handling to `New`.

That creates a repo-wide risk because several platform systems currently rely on old input assumptions, including:

- `PlayerInput`
- `SeatHotspot`
- camera drag behavior
- movement and sprint/jump actions

The safest assumption is that MetaDyn should migrate toward the new Input System in a controlled pass before or alongside Genies integration, rather than trying to bolt Genies onto the legacy input layer indefinitely.

## Risk 3: Avatar Runtime Architecture Mismatch

Current spawn logic is prefab-first.

Genies is runtime-avatar-first.

If MetaDyn tries to represent Genies as a pile of static prefabs, the integration will fight the SDK and lose most of the Genies value:

- persistent user avatar
- global avatar loading
- runtime editor flow
- account-based identity

## Risk 4: Authentication Model Split

MetaDyn currently uses Supabase-centered auth and profile flow.

Genies has its own:

- developer app credentials
- user login flow
- user account identity
- cached login state

That means MetaDyn must decide whether Genies is:

- a separate optional linked avatar identity
- a fully separate login flow
- or a provider attached after MetaDyn login

The recommended approach is linked-provider, not replacement auth.

## Risk 5: Lip Sync / Rigging Differences

Current lip sync scripts are hard-coded around known mesh names and blend shape conventions for the existing avatar families.

Genies avatars will likely need:

- a new lip sync adapter
- a face blend shape mapping layer
- a validation checklist for remote voice and local AI voice

## Recommended Product Direction

## Recommended High-Level Strategy

MetaDyn should integrate Genies as a third avatar provider through a normalized MetaDyn avatar-provider layer.

Do not:

- replace the player controller first
- replace Supabase auth with Genies auth
- wire Genies directly into the current prefab-only avatar selection design without an abstraction layer

Do:

1. keep MetaDyn auth as the platform root
2. add Genies as an optional linked avatar provider
3. create a runtime avatar-provider abstraction
4. add native-only support first
5. defer WebGL production rollout until official support exists or a controlled proof says otherwise

## Proposed Target Architecture

### Layer 1: MetaDyn Player Runtime

Keep one MetaDyn-owned network player object that always represents the player in Fusion.

That network object remains responsible for:

- movement
- networking
- name tags
- voice state
- moderation hooks
- camera ownership
- local interaction hooks

### Layer 2: Avatar Provider Adapter

Create an abstraction that attaches a visual avatar implementation to the MetaDyn player root.

Proposed provider types:

- Ready Player Me
- Avatar SDK
- Genies

Recommended concepts:

- `IAvatarProvider`
- `IAvatarVisualAdapter`
- `IAvatarLipSyncAdapter`
- `AvatarProviderType`

This allows MetaDyn to keep gameplay/networking stable while changing how avatar visuals are loaded and bound.

### Layer 3: Provider-Specific Identity

Separate:

- MetaDyn account identity
- avatar provider identity

For Genies, this likely means storing linked provider data such as:

- provider type
- Genies user ID
- avatar definition reference or local definition handle
- local cache status

### Layer 4: Provider-Specific UI

Do not cram Genies into the current two-list picker as a quick hack.

Instead, evolve avatar selection into a provider-aware UI:

- Ready Player Me
- Avatar SDK
- Genies

And eventually:

- provider linking state
- login state
- avatar edit action
- fallback / unsupported-platform messaging

## Phased Plan

## Phase 0: Feasibility and Guardrails

Goal:

- prove the Genies SDK can coexist in the repo without forcing an unsafe production change

Tasks:

1. Import Genies Avatar SDK in a working branch and run the Bootstrap Wizard in a controlled environment.
2. Capture all project-level changes the Bootstrap Wizard wants to make:
 - input handling
 - graphics API
 - packages
 - scripting/backend settings
 - TMP resources
3. Verify whether Genies can coexist with:
 - Fusion
 - current WebRTC scripts
 - current URP configuration
4. Build a native-only smoke-test scene:
 - Windows Standalone first
5. Explicitly do not merge WebGL-dependent production behavior in this phase.

Exit criteria:

- SDK imports cleanly
- native sample avatar loads
- project compiles
- exact repo-level config diffs are documented

## Phase 1: Input System Migration Decision

Goal:

- decide whether Pavilion migrates fully to the new Input System or uses dual-mode input during transition

Recommended direction:

- move toward `Both` first if possible during migration
- then refactor gameplay input to the new Input System

Reason:

- current codebase still uses legacy input heavily
- a hard switch to `New` too early is likely to break core controls

Tasks:

1. Audit all legacy `UnityEngine.Input` usage across runtime-critical scripts.
2. Identify systems that must be migrated before switching the project setting:
 - `Assets/Pavilion/Scripts/PlayerInput.cs`
 - `Assets/MetaDyn/Core/Runtime/Components/SeatHotspot.cs`
 - any camera or interaction scripts using direct `Input.*`
3. Decide whether MetaDyn wants:
 - a centralized input action asset
 - a compatibility wrapper that exposes the existing `GameplayInput` struct
4. Refactor `PlayerInput` to read from the new Input System while preserving current movement semantics.
5. Validate camera drag, zoom, jump, sprint, and UI input locking.

Exit criteria:

- player movement works under the new Input System path
- seated interaction still works
- chat/menu locking still works
- no regressions in local control flow

## Phase 2: Avatar Provider Abstraction

Goal:

- remove hard dependency on prefab-family-specific player spawn logic

Tasks:

1. Refactor `GameManager` avatar selection away from pure prefab-index logic.
2. Introduce provider-aware player appearance metadata.
3. Keep one canonical network player prefab and attach avatar visuals at runtime where practical.
4. Define the provider contract:
 - load avatar
 - unload avatar
 - provide animator
 - provide root transform
 - provide face/lip sync targets
5. Preserve old prefab paths during the first pass if runtime reattachment is too risky.

Recommended first implementation:

- keep existing prefab flows working
- add a parallel provider architecture
- migrate old families into adapters after Genies is proven

Exit criteria:

- MetaDyn can represent avatar choice as provider + avatar payload
- Genies is no longer blocked on static prefab authoring

## Phase 3: Genies Authentication and Account Linking

Goal:

- integrate Genies identity without replacing MetaDyn platform auth

Recommended model:

- user logs into MetaDyn as usual
- user optionally links or signs into Genies within the avatar/profile flow
- Genies account state is stored as provider-specific linked identity

Tasks:

1. Decide where Genies login lives:
 - pre-world profile UI
 - dashboard-linked profile flow
 - in-world avatar management panel
2. Add a Genies provider state model:
 - linked / unlinked
 - logged in / not logged in
 - anonymous / account user if supported in chosen flow
3. Persist enough provider data for session restoration.
4. Keep Supabase as the main platform account authority.
5. Do not use Genies credentials as the MetaDyn root identity.

Exit criteria:

- MetaDyn auth and Genies auth can coexist
- provider state is explicit and recoverable

## Phase 4: Runtime Genies Avatar Loading

Goal:

- load and bind a Genies avatar onto the MetaDyn player runtime

Tasks:

1. Create a `GeniesAvatarProvider` service or component.
2. Use Genies login state to:
 - instant-login where available
 - or trigger OTP / anonymous login flow as product requires
3. Load a Genies avatar via the Genies SDK into a known player visual root.
4. Bind the returned `ManagedAvatar` animator to MetaDyn movement/animation expectations.
5. Validate root placement, scale, rotation, and camera framing.
6. Define fallback behavior when avatar load fails.

Important note:

- Genies docs describe loading global avatars, local avatars, and default avatars
- multiplayer should likely use a serialized avatar definition or provider-owned user identity rather than assuming all remote peers can be represented by prefab choice only

Exit criteria:

- local player can spawn with a Genies visual
- animation controller binding works
- camera and movement still feel correct

## Phase 5: Multiplayer Representation

Goal:

- replicate enough provider identity so remote peers can reconstruct Genies avatars safely

Tasks:

1. Extend player identity payload/network state with:
 - avatar provider type
 - provider-specific avatar descriptor
2. Decide what remote peers receive:
 - Genies user ID
 - avatar definition snapshot
 - local cached avatar reference
3. Ensure remote players can reconstruct the correct avatar deterministically.
4. Add fallback rendering if a remote Genies avatar fails to load.

Recommended direction:

- prefer explicit avatar definition or controlled provider payload over relying only on user ID lookups

Reason:

- remote reconstruction needs determinism
- login state on remote clients should not be required to see another user's avatar

Exit criteria:

- remote Genies players render correctly
- late joiners reconstruct the same avatar state

## Phase 6: Lip Sync, Voice, and Facial Adapter

Goal:

- support WebRTC speaking indicators and local voice-driven facial movement for Genies avatars

Tasks:

1. Inspect Genies rig/blend shape naming and facial animation options.
2. Implement `GeniesPlayerLipSync` or a generalized `IAvatarLipSyncAdapter`.
3. Refactor `WebRTCManager` so it does not hard-code only:
 - `AvatarSdkPlayerLipSync`
 - `Wolf3DPlayerLipSync`
4. Route speaking start/stop through an adapter interface instead of `SendMessage` alone.
5. Validate:
 - remote WebRTC speaking
 - AI voice playback
 - silence reset
 - mouth close on despawn

Exit criteria:

- Genies avatars can react to speaking state
- WebRTC code is provider-agnostic

## Phase 7: UI / UX Integration

Goal:

- expose Genies in a way that fits the MetaDyn platform model

Tasks:

1. Update avatar selection UI to add a Genies provider section.
2. Add provider status messaging:
 - linked
 - not linked
 - unsupported on this platform
3. Add actions such as:
 - Sign in to Genies
 - Load My Genies Avatar
 - Edit Genies Avatar
4. Decide whether the current `UIGameMenu` is still the right place or whether avatar provider management should move into a more profile-centric panel.

Recommended UX rule:

- if running in WebGL, do not present Genies as a standard supported path unless a validated WebGL implementation exists
- instead present:
 - disabled state
 - native-only badge
 - waitlist / coming soon wording if desired

## Phase 8: Production Rollout Policy

Goal:

- avoid shipping unsupported behavior into the WebGL-first platform

Recommended rollout:

1. Internal native prototype
2. Native-only hidden feature flag
3. Platform/provider abstraction merged
4. Public provider UI only on supported targets
5. WebGL public rollout only after official support or validated engineering proof

## Recommended Code Changes

## Near-Term Refactor Targets

These are the highest-value code areas to prepare before real Genies implementation:

- `Assets/Pavilion/Scripts/PlayerInput.cs`
 - migrate off legacy-only input path

- `Assets/Pavilion/Scripts/GameManager.cs`
 - stop treating avatar selection as only prefab index

- `Assets/Common/UIGameMenu.cs`
 - evolve from two hard-coded avatar families to provider-aware UI

- `Assets/MetaDyn/Managers/WebRTCManager.cs`
 - remove lip-sync-type hard-coding

- `Assets/MetaDyn/Managers/WebRTCAudioReceiver.cs`
 - route into provider-agnostic lip sync adapter

- `Assets/MetaDyn/UserList/UserData.cs`
 - eventually expand provider identity if player/provider state should surface in-world

## Suggested New Systems

Recommended new MetaDyn-owned folders and concepts:

- `Assets/MetaDyn/Avatars/Providers/`
 - `AvatarProviderType.cs`
 - `IAvatarProvider.cs`
 - `IAvatarVisualAdapter.cs`
 - `IAvatarLipSyncAdapter.cs`
 - `ReadyPlayerMeAvatarProvider.cs`
 - `AvatarSdkAvatarProvider.cs`
 - `GeniesAvatarProvider.cs`

- `Assets/MetaDyn/Avatars/Runtime/`
 - `PlayerAvatarRuntime.cs`
 - `PlayerAvatarDescriptor.cs`
 - `PlayerAvatarLoader.cs`

- `Assets/MetaDyn/Avatars/LipSync/`
 - retain current scripts
 - add `GeniesPlayerLipSync.cs`
 - or replace family-specific scripts with adapters

## Open Questions

These should be answered before implementation begins:

1. Is Genies intended for:
 - native clients only at first
 - or is there an expectation of immediate Pavilion WebGL availability?

2. Should MetaDyn users be required to create a Genies account, or should Genies remain optional?

3. Does MetaDyn want:
 - a linked-provider model
 - an anonymous Genies fallback
 - or a custom local-avatar-definition flow for some use cases?

4. Should Genies avatars be:
 - player-only
 - player + NPC
 - or a full platform-wide avatar provider option?

5. Is avatar editing meant to happen:
 - inside Unity runtime
 - in dashboard/profile UI
 - or both?

6. Do we want to preserve the current multi-prefab avatar setup long-term, or migrate all avatar families to one runtime-loaded player visual model?

## Recommended Immediate Next Steps

1. Treat WebGL support as blocked for production until Genies officially supports it or we validate a working path ourselves.
2. Run a controlled import of the Genies SDK in a branch and document all Bootstrap Wizard changes.
3. Audit all legacy input usage and define the migration path to the new Input System.
4. Design the MetaDyn avatar-provider abstraction before adding Genies-specific gameplay code.
5. Build a native-only proof of concept that:
 - logs in
 - loads a Genies avatar
 - binds it to the MetaDyn player runtime
 - confirms animator compatibility
6. Refactor lip sync and avatar selection code so Genies is added as a provider, not a one-off exception path.

## Sources

Primary external sources used for this plan:

- Genies installation docs:
 - https://docs.genies.com/docs/sdk-avatar/getting-started/installation/
- Genies prerequisites:
 - https://docs.genies.com/docs/sdk-avatar/getting-started/prerequisites/
- Genies registration:
 - https://docs.genies.com/docs/sdk-avatar/getting-started/registration/
- Genies user login:
 - https://docs.genies.com/docs/sdk-avatar/frameworks/user-login/
- Genies avatar loading:
 - https://docs.genies.com/docs/sdk-avatar/frameworks/load-avatar/
- Genies avatar editor:
 - https://docs.genies.com/docs/sdk-avatar/frameworks/avatar-editor/
- Genies FAQ:
 - https://docs.genies.com/docs/sdk-avatar/tools/faq/
- Genies planned features:
 - https://docs.genies.com/docs/sdk-avatar/tools/planned-features/

Primary local files inspected for this plan:

- `Assets/Pavilion/Scripts/PlayerInput.cs`
- `Assets/Pavilion/Scripts/Player.cs`
- `Assets/Pavilion/Scripts/GameManager.cs`
- `Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs`
- `Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs`
- `Assets/Common/UIGameMenu.cs`
- `Assets/MetaDyn/Managers/WebRTCManager.cs`
- `Assets/MetaDyn/Managers/WebRTCAudioReceiver.cs`
- `Assets/MetaDyn/UserList/UserData.cs`
- `Assets/MetaDyn/Core/Runtime/Components/SeatHotspot.cs`
- `ProjectSettings/ProjectSettings.asset`
- `Packages/manifest.json`
