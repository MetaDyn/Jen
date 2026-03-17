# SDK Toolkit Inventory (Current State)

Categorized file inventory of what currently constitutes the MetaDyn toolkit/platform layer in this project, including files that should be tracked for SDK updates.

**Status:** Working Inventory | **Last Updated:** 2026-03-02

---

## Purpose

This document answers:

- What files are currently the MetaDyn toolkit/SDK?
- What files should be transferred to another project for the full MetaDyn platform/toolkit experience (excluding environment and avatar GameObjects)?
- What files are likely touched by SDK updates?

This is a current-state boundary map, not a final packaging layout.

The long-term target is a clear separation between:

- MetaDyn SDK/runtime/editor systems
- MetaDyn starter space template content
- portable platform flow shared by each space/instance/activation

So this inventory should be used not only to decide "what is SDK", but also:

- what belongs in the MetaDyn SDK
- what belongs in a MetaDyn starter space template
- what should remain project-specific glue

---

## Boundary Definition (Current)

### Future Packaging Lens

As packaging work progresses, files should be evaluated through three eventual buckets:

- **MetaDyn SDK**: reusable SDK/editor/runtime files intended to ship via Unity package distribution
- **MetaDyn Starter Space Template**: MetaDyn-owned starter environment/template content
- **Project Glue**: game/world-specific integration that should stay outside the reusable deliverable

The current Tier A / Tier B / Tier C model is a temporary transition map toward that structure.

### Tier A: Core SDK / Toolkit Package (Definite SDK Update Scope)

These files are the primary toolkit and should be treated as the core update set:

- `Assets/MetaDyn/**` (runtime, editor tools, UI prefabs, managers, auth, AI, etc.)
- `Assets/Plugins/WebGL/*.jslib` and related browser bridge JS files used by MetaDyn systems

### Tier B: Core Baseline Platform Files (Currently Outside `Assets/MetaDyn`)

These files are **core SDK/platform functionality**, even though they are still located outside `Assets/MetaDyn` today.

They are not optional glue. They are part of the baseline MetaDyn platform experience that every space depends on.

- `Assets/Common/UIGameMenu.cs`
- `Assets/Common/UIGameMenu.prefab`
- `Assets/Pavilion/Scripts/GameManager.cs`
- `Assets/Pavilion/Scripts/Player.cs`
- `Assets/Pavilion/Scripts/PlayerInput.cs`

### Tier B2: SDK-Adjacent Integration Files (Currently Outside `Assets/MetaDyn`)

These are still important to the transferable platform experience, but are secondary to the baseline platform bootstrap above:

- `Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs`
- `Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs`

### Tier C: Excluded from Toolkit Transfer (By Request / Not SDK)

Not considered toolkit for transfer/update inventory:

- Environment scene content and scene-specific world GameObjects
- Avatar GameObjects/prefabs/models (RPM/Avatar SDK avatar assets themselves)
- Scene-only visual polish scripts (for example `AzureLensFlare`, `CameraFollow`) unless intentionally productized later

---

## Inventory Summary (Current Counts)

- `Assets/MetaDyn` non-`.meta` files: `67`
- `Assets/Plugins/WebGL` MetaDyn-relevant bridge files: `5`
- `Assets/StreamingAssets` MetaDyn-relevant runtime files: `1`
- **Definite core toolkit total (Tier A): `72` files**
- Additional core/update-scope files currently outside `Assets/MetaDyn`: `7` files

---

## Tier A: Core SDK / Toolkit Package (`Assets/MetaDyn`)

### AI (`8`)

- `Assets/MetaDyn/AI/--AIAgent--.prefab`
- `Assets/MetaDyn/AI/AI.prefab`
- `Assets/MetaDyn/AI/AIEye.cs`
- `Assets/MetaDyn/AI/AIMemoryManager.cs`
- `Assets/MetaDyn/AI/AIMovementController.cs`
- `Assets/MetaDyn/AI/AIPerceptionManager.cs`
- `Assets/MetaDyn/AI/HeadLookController.cs`
- `Assets/MetaDyn/AI/MetaDynVoiceController.cs`

### Animations (`4`)

- `Assets/MetaDyn/Animations/Clap.anim`
- `Assets/MetaDyn/Animations/M_Dances_003.anim`
- `Assets/MetaDyn/Animations/Sitting Idle.fbx`
- `Assets/MetaDyn/Animations/SittingIdle.anim`

### Audio (`3`)

- `Assets/MetaDyn/Audio/AudioUtils.cs`
- `Assets/MetaDyn/Audio/MicrophoneRecorder.cs`
- `Assets/MetaDyn/Audio/MicrophoneVisualizer.cs`

### Chat (`4`)

- `Assets/MetaDyn/Chat/ChatIntegration.cs`
- `Assets/MetaDyn/Chat/ChatManager.cs`
- `Assets/MetaDyn/Chat/ChatMessageEntry.cs`
- `Assets/MetaDyn/Chat/ChatUI.cs`

### Core (`19`)

#### Core Assets / Config

- `Assets/MetaDyn/Core/MetaDynDashboard.asset`
- `Assets/MetaDyn/Core/MetaDyn_Hyp01_Dev.asset`

#### Core Runtime

- `Assets/MetaDyn/Core/Runtime/MetaDynRuntimeConfig.cs`
- `Assets/MetaDyn/Core/Runtime/NameTag.cs`
- `Assets/MetaDyn/Core/Runtime/SettingsUI.cs`
- `Assets/MetaDyn/Core/Runtime/StatsDisplay.cs`

#### Core Runtime Components

- `Assets/MetaDyn/Core/Runtime/Components/Emote.cs`
- `Assets/MetaDyn/Core/Runtime/Components/EntrancePoint.cs`
- `Assets/MetaDyn/Core/Runtime/Components/Interactable.cs`
- `Assets/MetaDyn/Core/Runtime/Components/ProjectionSurface.cs`
- `Assets/MetaDyn/Core/Runtime/Components/SeatHotspot.cs`
- `Assets/MetaDyn/Core/Runtime/Components/Trigger.cs`

#### Core Runtime Component Prefabs

- `Assets/MetaDyn/Core/Runtime/Components/Prefabs/ProjectionSurface.prefab`

#### Core Editor / MetaDyn SDK Tooling

- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDashboard.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynMenu.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynSDK.cs`
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynServerProfile.cs`

### Dashboard / Auth (`4`)

- `Assets/MetaDyn/Dashboard/LoginUI.cs`
- `Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs`
- `Assets/MetaDyn/Dashboard/SupabaseConfig.cs`
- `Assets/MetaDyn/Dashboard/WebAuthBridge.cs`

### Managers (`10`)

- `Assets/MetaDyn/Managers/ChatManager.prefab`
- `Assets/MetaDyn/Managers/GameManager.prefab`
- `Assets/MetaDyn/Managers/InputManager.cs`
- `Assets/MetaDyn/Managers/SettingsManager.cs`
- `Assets/MetaDyn/Managers/UIManager.cs`
- `Assets/MetaDyn/Managers/WeatherManager.cs`
- `Assets/MetaDyn/Managers/WebRTC-Voice-System.md`
- `Assets/MetaDyn/Managers/WebRTCAudioReceiver.cs`
- `Assets/MetaDyn/Managers/WebRTCJSMessageForwarder.cs`
- `Assets/MetaDyn/Managers/WebRTCManager.cs`

### Sounds (`4`)

- `Assets/MetaDyn/Sounds/clapping-90104.mp3`
- `Assets/MetaDyn/Sounds/ui-exit-menu-243462.mp3`
- `Assets/MetaDyn/Sounds/ui-menu-sounds-effects-button-2-203594.mp3`
- `Assets/MetaDyn/Sounds/ui-pop-up-243471.mp3`

### UI (`6`)

- `Assets/MetaDyn/UI/MainUI.prefab`
- `Assets/MetaDyn/UI/MessageEntry.prefab`
- `Assets/MetaDyn/UI/SpeechPanel (1).prefab`
- `Assets/MetaDyn/UI/SpeechPanel.prefab`
- `Assets/MetaDyn/UI/UserListEntry.prefab`
- `Assets/MetaDyn/UI/UserListPanel.prefab`

### User List (`4`)

- `Assets/MetaDyn/UserList/UserData.cs`
- `Assets/MetaDyn/UserList/UserListEntry.cs`
- `Assets/MetaDyn/UserList/UserListManager.cs`
- `Assets/MetaDyn/UserList/UserListUI.cs`

### Voice Chat (`1`)

- `Assets/MetaDyn/VoiceChat/VoiceSpeaker.prefab`

---

## Tier A (Required Companion): WebGL Browser Bridge Files (`Assets/Plugins/WebGL`)

These are part of the toolkit runtime experience for WebGL and should be versioned alongside SDK updates.

- `Assets/Plugins/WebGL/AuthBridge.jslib` (dashboard auth cookie/localStorage bridge)
- `Assets/Plugins/WebGL/MicrophonePlugin.jslib` (AI push-to-talk mic capture)
- `Assets/Plugins/WebGL/ProjectionSurface.jslib` (projection surface browser integration)
- `Assets/Plugins/WebGL/WebRTCVoice.jslib` (player-to-player voice chat browser/WebRTC layer)
- `Assets/Plugins/WebGL/microphone-processor.js` (mic/audio worklet/processor helper)

## Tier A (Required Companion): Streaming Assets Runtime Files (`Assets/StreamingAssets`)

These files are required by current runtime paths and should be treated as SDK-owned if referenced by active WebGL/browser code.

- `Assets/StreamingAssets/microphone-processor.js` (active AudioWorklet file loaded by `Assets/Plugins/WebGL/MicrophonePlugin.jslib`)

---

## Tier B: Core Baseline Platform Files (Outside `Assets/MetaDyn`)

These files are part of the core MetaDyn platform baseline and should travel with every space/instance/activation.

They are currently outside `Assets/MetaDyn`, but they should be treated as first-class SDK update scope.

### Starter / Launcher Integration (Core SDK Baseline)

- `Assets/Common/UIGameMenu.cs`
- `Assets/Common/UIGameMenu.prefab`

Notes:
- Handles world join flow, runtime config usage, and Supabase web-first auth/profile/avatar integration.
- High coupling to `MetaDynRuntimeConfig` and `SupabaseAuthManager`.
- This is core baseline platform functionality, not optional template glue.

### Core Player/Session Integration (Core SDK Baseline)

- `Assets/Pavilion/Scripts/GameManager.cs`
- `Assets/Pavilion/Scripts/Player.cs`
- `Assets/Pavilion/Scripts/PlayerInput.cs`

Notes:
- These drive spawning, avatar selection lists, input locking integration, name tags, and user registration hooks.
- These are required parts of the baseline MetaDyn platform/player bootstrap.
- They should be planned as unified SDK/platform files, even if refactoring is needed before final package placement.

## Tier B2: SDK-Adjacent Integration Files (Outside `Assets/MetaDyn`)

These files are still part of the transferable platform experience, but they are not as foundational as the launcher/player/session bootstrap files above.

### AI Voice Orchestration

- `Assets/MetaDyn/AI/MetaDynVoiceController.cs`

Notes:
- Successfully moved into the SDK AI folder and validated by compile + Play Mode spawn test.
- Now considered part of Tier A SDK update scope, not Tier B.

### Avatar Voice/Lip Sync Integration (SDK-Adjacent)

- `Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs`
- `Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs`

Notes:
- These are avatar-attached scripts, but they are part of the platform voice experience and may change with WebRTC/audio SDK updates.
- Exclude avatar GameObjects themselves from transfer if desired, but keep these scripts on the review list.

---

## Likely Non-SDK / Excluded Pavilion Files (Current)

These are present in `Assets/Pavilion/Scripts` but are currently better treated as scene/game-specific:

- `Assets/Pavilion/Scripts/AzureLensFlare.cs`
- `Assets/Pavilion/Scripts/CameraFollow.cs` (could become reusable later, but currently scene/player camera behavior)

---

## What to Transfer to Another Project (Practical Starting Set)

If the goal is "full MetaDyn toolkit/platform experience" without environment/avatar GameObjects:

1. Transfer all Tier A files (`Assets/MetaDyn/**` non-meta + WebGL bridge files).
2. Transfer Tier B and Tier B2 files (or replace them with future SDK equivalents when extracted).
3. Recreate/assign scene objects and avatar prefabs in the target project.
4. Re-wire prefab references (UI, player prefab, AI agent prefab, audio sources, runtime config assets).

This is the minimum realistic current-state transfer boundary.

---

## SDK Update Review Checklist (Current Repo)

When preparing an SDK update, review changes in:

1. `Assets/MetaDyn/**`
2. `Assets/Plugins/WebGL/AuthBridge.jslib`
3. `Assets/Plugins/WebGL/MicrophonePlugin.jslib`
4. `Assets/Plugins/WebGL/ProjectionSurface.jslib`
5. `Assets/Plugins/WebGL/WebRTCVoice.jslib`
6. `Assets/Plugins/WebGL/microphone-processor.js`
7. `Assets/Common/UIGameMenu.cs`
8. `Assets/Common/UIGameMenu.prefab`
9. `Assets/Pavilion/Scripts/GameManager.cs`
10. `Assets/Pavilion/Scripts/Player.cs`
11. `Assets/Pavilion/Scripts/PlayerInput.cs`
12. `Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs`
13. `Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs`

---

## Follow-Up (Recommended)

Create an extraction plan to unify the remaining out-of-folder core SDK files into the package/baseline platform structure:

- `MetaDynVoiceController.cs` (completed move to `Assets/MetaDyn/AI/`)
- `UIGameMenu.cs` / `UIGameMenu.prefab` (core baseline SDK)
- `GameManager.cs`, `Player.cs`, `PlayerInput.cs` (core baseline SDK)
- Avatar lip sync integrations (as adapters/components)

---

## Related Documentation

- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- [SDK_DEVELOPMENT.md](SDK_DEVELOPMENT.md)
- [AI_EMBODIMENT.md](AI_EMBODIMENT.md)
- [AUTH_SYSTEM.md](AUTH_SYSTEM.md)
- [INFRASTRUCTURE.md](INFRASTRUCTURE.md)
