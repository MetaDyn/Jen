# MetaDyn UGS SDK Production Punch-List
**Status:** Post-Migration / Pre-Production  
**Target:** Master SDK v1.2.0 (UGS/NGO Baseline)

---

## 🛡️ Pillar 1: Declaration (Establishing the Baseline)
*Goal: Officially transition the SDK identity to UGS-native and clearly categorize legacy assets.*

- [ ] **SDK Manifest Update**: Modify `MetaDynSDKManifest.json` to set UGS/NGO as the `stable` networking provider and deprecate Photon Fusion.
- [ ] **UPM Restructuring**: Prepare `Assets/MetaDyn` for distribution by adding a formal `package.json` and associated `.asmdef` files.
- [ ] **Editor Tool Rebranding**: Update headers in `MetaDynProjectConfig` and `MetaDynSDKSyncCheckWindow` to display the UGS-Master status.
- [ ] **Documentation Refresh**: Update internal `.md` guides to replace Photon-specific setup steps with the Unity Cloud / UGS workflow.

## 🔍 Pillar 2: Validation (The Creator Guardrails)
*Goal: Catch configuration errors in the Editor before they break WebGL builds.*

- [x] **`MetaDynSDKValidator` Implementation**: Create a one-click validation suite that checks:
    - [x] **Service Connectivity**: Is the Project ID linked and are UGS services active?
    - [x] **Package Integrity**: Are required NGO, Relay, and Vivox packages installed?
    - [x] **Scene Configuration**: Does the `NetworkManager` have a valid Player Prefab and use WebSockets for WebGL?
    - [x] **Runtime Config**: Does the `MetaDynRuntimeConfig` asset have a valid `spaceId` and `roomName`?
- [x] **Entrance Point Check**: Ensure the scene has at least one unique `EntrancePoint` to prevent spawning at the origin.
- [ ] **Pre-Build Validation Hook**: Stop WebGL builds automatically if "Blocking" errors (like missing Space IDs) are detected.

## 🏗️ Pillar 3: Hardening & Diagnostics (Production Reliability)
*Goal: Provide enterprise-grade stability and clear feedback for field failures.*

- [ ] **Structured Log Diagnostics**: Categorize runtime logs into `[UGS]`, `[AUTH]`, `[VOICE]`, and `[SPAWN]` for faster troubleshooting in the browser console.
- [ ] **Multi-Tenant Safety**: Update `MetaDynDeploymentManager` to ensure "Dev" builds cannot accidentally join "Production" UGS sessions via environment-matching logic.
- [x] **Session Lifecycle Hardening**: 
    - [x] Implement "Space ID as Session Key" for 100% deterministic and secure joins.
    - [x] Added robust "Join or Create" race-condition handling in `MetaDynUGSSessionService`.
    - [x] Finalize a clean "Back to Menu" disconnect flow that clears local NGO state.
    - [x] Forced NGO shutdown before new joins to resolve `NetworkManagerStartFailed` errors.
- [ ] **UGS Host Migration & Authority Recovery**:
    - [ ] Enable UGS Sessions host migration when creating Relay sessions. The current `SessionOptions` chain uses `WithRelayNetwork()` but does not call `WithHostMigration(...)`, so host migration is disabled.
    - [ ] Implement an NGO-compatible `IMigrationDataHandler` that snapshots/restores the minimum authoritative state required to rebuild the session after host loss. Do not use the package's default migration handler blindly; it is provided for Entities Netcode rather than this NGO player stack.
    - [ ] Handle `SessionHostChanged`, `SessionMigrated`, and migration-failure events in `MetaDynUGSSessionService`, including a visible reconnecting/migrating UI state and bounded timeout.
    - [ ] Allow UGS Sessions to elect a remaining session member as the new host, create a replacement Relay allocation, restart NGO as host on that client, and reconnect the other clients.
    - [ ] Rebuild player objects using stable UGS/Supabase identity rather than old NGO client IDs, then restore display name, selected prefab shell, `active_avatar_model_id`, permissions, and other required player state.
    - [ ] Define which world state must survive migration and which state may safely reset. Persist important shared state outside the departing host or include it in the migration snapshot.
    - [ ] If migration cannot complete, shut down the stale NGO client cleanly and return users to a recoverable rejoin/menu flow instead of leaving the world visually frozen.
    - [ ] Test graceful host leave and abrupt host loss with at least three clients in Editor/native and WebGL/Relay, including movement, avatar GLB restoration, Vivox rejoin, late join after migration, and repeated host changes.
- [ ] **Networked Animation Sync**: 
    - [x] Programmatically added `NetworkAnimator` to all player prefabs.
    - [x] Implemented networked speed and jump state synchronization for remote proxies.
    - [x] Replaced the server-authoritative NGO `NetworkAnimator` on every avatar-registry and default player shell with the owner-authoritative `OwnerNetworkAnimator`, bound to the same root `Animator` used by `MetaDynUGSPlayerController`.
    - [x] Ensured custom-avatar profile restore lands on an owner-authoritative network shell even when it falls back to `AvatarChoice = 0` (`Player 2`).
    - [x] Preserve the last synchronized locomotion parameters, layer state, normalized time, and layer weights across each runtime GLB `Animator.Rebind()` on owners and remote proxies.
    - [x] Built and multiplayer-tested the stored user-bucket GLB path; uploaded-avatar animation appeared normal to all participating players (verified 2026-08-05).
    - [x] Documented the symptom, root cause, owner-authority contract, implementation, affected files, verification boundary, and regression rules in `Runtime_Avatar_Upload_And_Rigging_Plan.md` section 6.8.
    - [ ] Verify with a host and at least two clients that a client-owned stored GLB avatar correctly shows idle, walk/run, stop, jump, landing, reload restore, and late-join animation without ice skating.
    - [ ] Validate a replacement Humanoid Avatar before removing the current visible avatar, so an invalid GLB cannot leave the player without a rendered model.
    - [ ] Add a per-player/model load generation guard so a stale asynchronous GLB request cannot overwrite a newer avatar selection.
    - [ ] Route emote and seat-driven Animator controller/rebind operations through the state-preserving avatar-swap path; verify controller parameter/layer compatibility.
    - **Regression rule:** Do not replace `OwnerNetworkAnimator` with stock server-authoritative `NetworkAnimator` while owner-only locomotion writes remain in `MetaDynUGSPlayerController`.
    - **Scope boundary:** This fix preserves avatar animation during runtime GLB loading; it does not provide UGS host migration or authority recovery after the host leaves.
- [ ] **Resource Management**: Explicitly document and validate microphone-sharing constraints between Vivox (Voice) and the AI Perception (Speech Capture).
- [ ] **Automated AWS Deployment (Pull-Trigger Model)**:
    - [ ] Add `webhookUrl` and `webhookSecret` fields to `MetaDynServerProfile` for UCB integration.
    - [ ] Develop the **EC2 Deployment Gateway** blueprint (UCB Webhook -> API -> AWS Download/Unzip).
    - [ ] Integrate **AWS SES** for automated "Your Space is Live" email notifications.
    - [ ] Implement automated "Live" status synchronization with the Supabase dashboard.

---

## 🫂 Pillar 4: Social Identity & Persistence
*Goal: Bridge UGS real-time presence with existing Supabase account/profile data.*

- [ ] **Unity Friends & Presence Integration**:
    - [ ] Link UGS Player IDs to Supabase User IDs for consistent identity.
    - [ ] Implement presence updates: "In Space: [SpaceName]" or "In Main Menu".
    - [ ] Add "Join Friend" logic that pulls session data from a friend's UGS presence.
- [ ] **Cross-Space Global Chat**:
    - [ ] Configure a "Global" Vivox text/voice channel that ignores spatial positioning.
    - [ ] Add a "Global/Local" toggle logic to the current `ChatUI`.
- [ ] **Persistent Messaging (DMs)**:
    - [ ] Implement Vivox Directed Text for 1-to-1 messaging between online users.
    - [ ] Add an "Incoming Message" HUD notification system (visual/UI hook).
- [ ] **Relationship Sync (Supabase Bridge)**:
    - [ ] Implement a background sync that pulls the "Friends List" from Supabase into the UGS social cache.
    - [ ] Ensure blocking/muting in the Unity client persists back to the Supabase user profile.
- [ ] **Social Service Validation**:
    - [ ] Add "Friends Service Enabled" and "Presence Service Enabled" checks to the `MetaDynSDKValidator`.

---

## 💰 Pillar 5: Economy & Digital Assets
*Goal: Bridge existing Web Dashboard commerce with in-engine utility.*

- [ ] **Unity-Web Economy Bridge**:
    - [ ] Implement a sync service to pull currency/wallet data from the Web Dashboard (Supabase).
    - [ ] Integrate **UGS Economy** for real-time transaction handling and "Space-Specific" currencies.
- [x] **Inventory System**: 
    - [x] Create a persistent inventory manager that tracks owned items (emotes, wearables, tools) across all spaces. (Cloud Registry Verified)
- [ ] Implement a "Virtual Storefront" component for in-world item purchases.

## 🌎 Pillar 6: Persistent World State (The "Living World")
*Goal: Ensure player actions and environment settings have a lasting impact.*

- [ ] **World Persistence (UGS Cloud Save)**:
    - [ ] Implement logic to save/load interactable object states (e.g., furniture positions, light toggles).
    - [ ] Save player-specific data like "Last Spawn Point" and "World Interaction History."
- [ ] **Remote Environment Control**:
    - [ ] Link **UGS Remote Config** to `WeatherManager` and `DayNightCycle`.
    - [ ] Enable global atmospheric overrides from the Web Dashboard.

## 🤖 Pillar 7: Embodied AI (Aurora 2.0)
*Goal: Deepen AI spatial awareness and tighten memory persistence.*

- [ ] **AI Spatial Perception**:
    - [ ] Update Aurora to use the **NGO User List** to identify and greet players by their Supabase Display Name.
    - [ ] Implement "Gaze Tracking" toward the active speaker in the NGO session.
- [ ] **Tightened Memory Integration**:
    - [ ] Bridge Aurora's existing Cloudflare persistence with UGS/Supabase for cross-platform memory consistency.
    - [ ] Implement "Session Memory" where Aurora remembers specific events from the current multiplayer session.
- [ ] **AI Event Hosting**:
    - [ ] Allow Aurora to trigger NGO-synced events (starting tours, changing music, controlling lights).

## 📈 Pillar 8: Analytics, Safety & Moderation
*Goal: Data-driven growth and enterprise-grade community governance.*

- [ ] **Hybrid Analytics**:
    - [ ] Combine existing **Umami** web analytics with deep in-engine **UGS Analytics** (Heatmaps, Social Graphs).
    - [ ] Track "Session Duration" and "Interaction Depth" per space.
- [ ] **Community Governance**:
    - [ ] Implement a "Global Ban/Mute" system synced with the Web Dashboard.
    - [ ] Create a "Report User" UI that captures session context for moderators.

---

## 🌀 Pillar 9: Interoperability & Portals (The "Open Metaverse" Layer)
*Goal: Enable seamless travel and asset portability between self-hosted "spoke" spaces.*

- [ ] **Cyberpunk Portal System**:
    - [ ] **Visual Design**: Create a "Stargate-like" cyberpunk portal prefab (VFX-heavy, neon-lit).
    - [ ] **Portal Logic**: Implement `MetaDynPortal` component that triggers the `ConnectToSpace(targetSpaceId)` handshake.
    - [ ] **Transition HUD**: A "Warping" UI that covers the transition between NGO session disconnect and the new space join.
- [ ] **Portable Inventory (Universal Asset Bridge)**:
    - [ ] **Asset Portability Strategy**: Develop a system for loading licensed assets (Avatars, Cars, Auras) via **Addressables/CDN**.
    - [ ] **License Verification**: Implement a real-time check against the Web Dashboard/Supabase to verify asset ownership before spawning in a spoke.
    - [ ] **Space Permission System**: Define a "Rules Metadata" set for spaces (e.g., "No Cars Allowed," "Avatar Restrictions") that the SDK enforces upon arrival.
- [ ] **Cross-Space Identity Handshake (The Transit Token)**:
    - [ ] Develop a "Transit Token" system (URL parameters/LocalStorage) for passing identity between different WebGL domains.
    - [ ] Ensure the player's "Inventory Manifest" and "Aurora Memory State" are passed securely and validated against Supabase upon arrival.

---

## 🛠️ Pillar 10: Creator Empowerment & UGC (The Construction Kit)
*Goal: Provide the "No-Code" toolkit for rapid, high-fidelity world building.*

- [x] **MetaDyn Interaction Kit**:
    - [x] Develop a library of "Ready-to-Use" NGO-synced components: `MetaDynSeat`, `MetaDynDoor`, `MetaDynLightSwitch`, and `MetaDynTrigger`.
    - [x] Ensure all interactions are automatically networked with zero scripting required by the creator.
- [x] **Branded Inspector Suite**:
    - [x] Implement a standardized, logo-branded header for all core MetaDyn components (`SeatHotspot`, `Interactable`, `Trigger`, etc.).
- [ ] **The "Spoke" Template Scene**: 
- [ ] Build a "Plug-and-Play" template scene with `NetworkManager`, `AuthManager`, `Aurora`, and `EntrancePoints` pre-configured.
- [ ] **Asset Optimization Auditor**:
    - [ ] Implement an editor tool to validate custom 3D models (poly count, draw calls, texture size) for WebGL performance.
- [ ] **In-World Editing (UGC Lite)**:
    - [ ] Implement a restricted "Builder Mode" where space owners can manipulate objects while live, saving state back to **UGS Cloud Save**.

---

## 📱 Pillar 11: Multi-Device & WebGL Optimization
*Goal: Optimize for Safari load-times and "fat-finger" mobile interaction.*

- [x] **Define Purge**: Strip legacy `FUSION` and `PHOTON` scripting defines to clean up the compiler.
- [x] **Sprite Atlas Implementation**: Bundle all UI icons into a single atlas to reduce WebGL draw calls and fetch requests.
- [x] **Touch Interaction Update**: 
    - [x] Transition `Interactable.cs` to use `IPointerDownHandler` for mobile touch support.
    - [x] Add a "Mobile Interaction HUD" (a simple virtual button that appears when near an object).
    - [x] Implement modern Virtual Joystick (Left) and Jump Button (Right) for mobile movement.
    - [x] **Fixed Mobile UI Scaling**: Joystick (300x300) and Jump (250x250) anchored properly to screen corners.
    - [x] **UI-Aware Camera**: Camera look logic now ignores touches over UI elements to prevent spinning.
    - [x] **Browser Security Fix**: Disabled automatic cursor locking on WebGL/Mobile to stop security banners and "Cursor Fight".

---

## 🚀 Immediate "Post-Build" Sprint
1. **Implement `MetaDynSDKValidator`** (High Value).
2. **Wire Validator into the Deployment Center UI**.
3. **Restructure `Assets/MetaDyn` as a formal UPM package** (See [Implementation Plan: UPM Transition](../../.claude/Quick Reference/UPM_MIGRATION_PLAN.md)).
