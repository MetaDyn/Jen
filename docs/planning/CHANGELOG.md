# MetaDyn Project Changelog

## Format
```
## YYYY-MM-DD - Feature/Area Name
**Changed:** What was modified
**Added:** What was created
**Fixed:** What was corrected
**Files:** Affected files
**Reason:** Why the change was made
```

---

## 2026-08-06 - UGS/NGO Host Migration Read-Only Audit and Plan

**Added:**
- Added a dedicated implementation plan for additive UGS Sessions host migration with Relay and NGO.
- Documented the current lifecycle, installed Multiplayer 2.2.3 behavior, MetaDyn integration gaps, stable identity and snapshot contracts, migration state machine, phased rollout gates, failure policy, risks, and three-client test matrix.

**Changed:**
- Expanded the production punch list with the audited prerequisites: handler configuration for both creators and joiners, restart-safe manual spawning, versioned stable identity, correct remote Supabase identity, opt-in SDK world-state providers, and compatibility rules.
- Added the host-migration plan to the quick-reference documentation map.

**Files:**
- `/.claude/Planning/UGS_NGO_Host_Migration_Implementation_Plan.md`
- `/.claude/Planning/SDK_Private_Documentation/Documentation~/MetaDyn_UGS_SDK_Production_PunchList.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/CHANGELOG.md`

**Verification:**
- Cross-checked the plan against the current MetaDyn session/player/user-list/avatar/voice/world-state code and the installed UGS Multiplayer 2.2.3 migration/network-handler source.
- Documentation-only planning work; no runtime code, package source, prefab, scene, compile, or build was changed.

**Reason:**
- Host migration restarts the Relay/NGO network and changes all NGO client/object identities. A phased state-restoration design is required to approach Photon-like continuity without destabilizing the existing working multiplayer path.

---

## 2026-08-06 - Network Animator Fix Documentation

**Changed:**
- Reconciled the runtime avatar plan with the implemented and multiplayer-verified owner-authoritative network animator fix.
- Added a durable technical record of the ice-skating symptom, mismatched-authority root cause, required prefab/component contract, state-preserving GLB rebind sequence, affected files, verification boundary, and regression rules.
- Separated the verified defect fix from remaining host-plus-two-client regression coverage and follow-up hardening for invalid/stale GLB swaps and emote/seat rebinds.
- Explicitly documented that network animator synchronization and UGS host migration are separate concerns.

**Files:**
- `/.claude/Planning/Runtime_Avatar_Upload_And_Rigging_Plan.md`
- `/.claude/Planning/SDK_Private_Documentation/Documentation~/MetaDyn_UGS_SDK_Production_PunchList.md`
- `/.claude/CHANGELOG.md`

**Verification:**
- Cross-checked the documentation against `OwnerNetworkAnimator`, `MetaDynUGSPlayerController`, `GLBAvatarLoader`, and the active player prefab changes.
- Documentation-only update; no compile or build was run.

**Reason:**
- Preserve the verified fix and its authority assumptions so future prefab or avatar-loading changes do not reintroduce remote position-only ice skating.

---

## 2026-08-04 - Owner-Authoritative GLB Network Animation Fix

**Changed:**
- Replaced the server-authoritative NGO `NetworkAnimator` with `OwnerNetworkAnimator` on the active `Player 2`, `Player 3`, and default `Player UGS` network shells.
- Added runtime validation that every spawned `MetaDynUGSPlayerController` has an `OwnerNetworkAnimator` bound to the same root `Animator`.
- Updated runtime GLB avatar swapping to capture animator parameters and layer state before the old skeleton is removed, then restore that state after assigning the new humanoid avatar and calling `Animator.Rebind()`.
- Kept the owner as the locomotion source of truth while preserving the last received state on remote proxies during asynchronous storage download and GLB application.

**Files:**
- `/Assets/MetaDyn/Runtime/Networking/MetaDynUGSPlayerController.cs`
- `/Assets/MetaDyn/Runtime/Avatar/GLBAvatarLoader.cs`
- `/Assets/Starter/PlayerPrefab/Player 2.prefab`
- `/Assets/Starter/PlayerPrefab/Player 3.prefab`
- `/Assets/Starter/PlayerPrefab/Player UGS.prefab`
- `/.claude/Planning/SDK_Private_Documentation/Documentation~/MetaDyn_UGS_SDK_Production_PunchList.md`

**Verification:**
- Reviewed active registry/default prefab script references and confirmed they all use `OwnerNetworkAnimator` with the root Animator assigned.
- Built and multiplayer-tested by the project owner on 2026-08-05; animation for an uploaded GLB restored from the user's Storage bucket appeared normal to all participating players.
- Exhaustive host-plus-two-client, reload, and late-join coverage remains open on the production punch list.
- No compile or build was run by the agent; build execution remained with the project owner.

**Reason:**
- Client-owned avatars could synchronize position while remote users saw idle/T-pose locomotion or ice skating because several active shells used server-authoritative animation and runtime GLB rebinding reset proxy animator state.

---

## 2026-07-17 - Individual Membership Tier Naming Finalized

**Changed:**
- Renamed the `$20/month` self-service tier from Community Member to Individual.
- Updated the dashboard card copy, annual-plan label, Stripe product/price placeholders, entitlement key, onboarding flow, Discord role, conversion target, and launch copy.
- Preserved Individual and Organization as the only dashboard self-service membership plans.
- Recorded the created Stripe product IDs and all four monthly/annual recurring price IDs for Individual and Organization.

**Files:**
- `/.claude/Planning/Sponsorship_And_Membership_Worksheet.md`
- `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/.claude/STRIPE_MEMBERSHIP_IMPLEMENTATION_PLAN.md`
- `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/.claude/README.md`

**Reason:** Make the two self-service tiers immediately understandable as individual-versus-organization offerings and align the documentation with the Stripe products being created.

---

## 2026-07-15 - Dashboard Self-Service Membership Tiers Finalized

**Changed:**
- Finalized Community Member and Organization as the only self-service subscription tiers.
- Clarified that only Community and Organization appear as subscription cards in the MetaDyn Dashboard.
- Corrected the onboarding flow so Silver, Gold, and Platinum are consistently treated as sponsorship/assisted offerings outside dashboard self-service.
- Marked the Community tier explicitly as a dashboard subscription card alongside Organization.
- Added the canonical React dashboard repository path and separated dashboard billing responsibilities from Unity SDK entitlement enforcement.

**Files:**
- `/.claude/Planning/Sponsorship_And_Membership_Worksheet.md`

**Reason:** Remove conflicting tier language and establish the final dashboard billing boundary before Stripe implementation.

---

## 2026-07-15 - SDK Entitlement Scope Correction

**Changed:**
- Corrected the membership entitlement model: active entitlement gates protected SDK capabilities, including deployment, rather than paid/private world access or Unity launch/join.
- Renamed the associated token in the worksheet to the MetaDyn SDK access token and aligned grace-period enforcement with protected SDK operations.

**Files:**
- `/.claude/Planning/Sponsorship_And_Membership_Worksheet.md`

**Reason:** Ensure the Stripe membership implementation enforces the actual product boundary for MetaDyn SDK access.

---

## 2026-07-15 - Organization Membership Tier Naming

**Changed:**
- Renamed the `$60/month` self-serve `Business` subscription tier to `Organization`.
- Updated the Stripe product/price placeholders, entitlement tier key, Discord role, dashboard card copy, annual-plan label, and public announcement copy to use `Organization`.

**Files:**
- `/.claude/Planning/Sponsorship_And_Membership_Worksheet.md`

**Reason:** Align the paid-tier name with the intended audience of teams, studios, and other managed-platform organizations.

---

## 2026-06-24 - Subscription Entitlement Expiry Planning

**Added:**
- Added token/access invalidation guidance to the Stripe membership worksheet.
- Clarified that MetaDyn paid/private platform access token validity is gated by current entitlement state.
- Added grace-period expiry fields, token-versioning guidance, and access-check behavior for dashboard, backend, and Unity launch/join flows.

**Files:**
- `/.claude/Planning/Sponsorship_And_Membership_Worksheet.md`

**Reason:** Ensure expired subscriptions can be downgraded or locked after grace period without relying on stale client tokens or cached plan state.

---

## 2026-06-24 - Membership Pricing and Dashboard Card Plan Update

**Changed:**
- Updated Community Member subscription pricing from `$10/month` to `$20/month`.
- Added a Business subscription tier at `$60/month`.
- Clarified that dashboard self-serve subscription cards should be Community and Business only.
- Kept Silver, Gold, and Platinum sponsorships in the plan, but marked them as separate from dashboard subscription cards.
- Added Business Stripe product/price placeholders and metadata tier key.

**Files:**
- `/.claude/Planning/Sponsorship_And_Membership_Worksheet.md`

**Reason:** Align the dashboard billing plan with the intended self-serve subscription cards while preserving sponsorship offerings outside the dashboard card flow.

---

## 2026-06-24 - Stripe Dashboard Billing Plan Update

**Changed:**
- Updated the membership/sponsorship worksheet with a dashboard-first Stripe integration direction.
- Added embedded Stripe Checkout for first subscription signup/upgrade.
- Added Stripe Customer Portal redirect for billing management.
- Clarified that Supabase entitlement state must be webhook-driven, not success-redirect-driven.
- Added future Stripe Connect compatibility notes and separated subscriber/customer identity from creator/seller connected-account identity.

**Files:**
- `/.claude/Planning/Sponsorship_And_Membership_Worksheet.md`

**Reason:** Preserve a dashboard-native billing experience while keeping the architecture compatible with future marketplace payouts through Stripe Connect.

---

## 2026-06-24 - Enterprise Security Advantages Planning Note

**Added:**
- Created `Enterprise_Security_Advantages.md` documenting MetaDyn's enterprise security positioning, current security advantages, safe claims, claims requiring more work, and a hardening roadmap.

**Files:**
- `/.claude/Planning/Enterprise_Security_Advantages.md`

**Reason:** Capture the platform's enterprise-ready security advantages for planning, partner discussions, and roadmap alignment.

---

## 2026-06-24 - Custom GLB Animator Refresh Fix

**Fixed:**
- Added `MetaDynUGSPlayerController.RefreshAnimatorAfterAvatarSwap` to reapply locomotion animator state after a runtime GLB avatar bind.
- Forced player animators to `AlwaysAnimate` so hidden/render-swapped model renderers do not leave the Animator culled or visually frozen.
- Called the refresh path immediately after `GLBAvatarLoader` assigns the runtime humanoid avatar and calls `Rebind`.

**Files:**
- `/Assets/MetaDyn/Runtime/Networking/MetaDynUGSPlayerController.cs`
- `/Assets/MetaDyn/Runtime/Avatar/GLBAvatarLoader.cs`

**Reason:** Uploaded custom avatars restored and appeared on remote clients, but the swapped GLB model could remain visually frozen/ice-skating because animator state was reset during runtime avatar rebinding.

---

## 2026-06-24 - LoginUI Custom Avatar Restore Preparation

**Fixed:**
- Updated `UIGameMenu.ApplyAuthenticatedProfile` to prepare uploaded custom avatar restore as soon as authenticated profile data is applied.
- Added a visible status message when `active_avatar_model_id` is found: `Custom avatar found. Press Start to join.`

**Files:**
- `/Assets/MetaDyn/Runtime/Core/Starter/UIGameMenu.cs`

**Reason:** In WebGL scenes where `LoginUI` handles authentication, the web-auth-specific `UIGameMenu.OnProfileFetched` path does not run. Custom avatar restore must be prepared from the shared profile application path used by both LoginUI and web auth.

---

## 2026-06-24 - Uploaded Avatar Restore Order Fix

**Fixed:**
- Moved custom avatar restore in `UIGameMenu.HandleLocalPlayerReady` before the menu panel is hidden, so uploaded avatar restoration is not blocked if the GLB loader is attached to or under the UI hierarchy.

**Files:**
- `/Assets/MetaDyn/Runtime/Core/Starter/UIGameMenu.cs`

**Reason:** On refresh, the existing prefab avatar is expected to spawn first as the network shell, but the saved uploaded GLB should immediately restore and replace the visible avatar model.

---

## 2026-06-24 - Unity Cloud Build AI Desktop Dependency Fix

**Fixed:**
- Removed the direct `com.unity.ai.desktop` local file dependency from `Packages/manifest.json`.
- Removed the matching local package lock entry from `Packages/packages-lock.json`.

**Files:**
- `/Packages/manifest.json`
- `/Packages/packages-lock.json`

**Reason:** Unity Cloud Build cannot resolve user-profile Unity Hub bundled package paths such as `C:\Users\joshg\AppData\Roaming\UnityHub\cocreate-bundled-packages\...`. Keeping the registry `com.unity.ai.assistant` dependency preserves the editor package while avoiding the cloud-only package resolution failure.

---

## 2026-06-23 - Runtime Avatar Storage MVP Integration

**Added:**
- Created `MetaDynAvatarStorageService` for authenticated Supabase avatar model upload, metadata registration, active-profile selection, metadata fetch, and Storage download.
- Added runtime support for `profiles.active_avatar_model_id` in `SupabaseProfile`.
- Added NGO custom avatar model id sync on `MetaDynUGSPlayerController` so remote clients and late joiners can resolve uploaded avatars by model id.

**Changed:**
- Updated `GLBAvatarLoader` to upload authenticated GLB selections to Supabase before applying, while preserving local-only GLB application for unauthenticated use.
- Updated `UIGameMenu` profile restore logic so uploaded custom avatars count as an existing avatar choice without changing local prefab `avatar_index` behavior.
- Updated `Runtime_Avatar_Upload_And_Rigging_Plan.md` checklist to reflect completed Supabase setup and Unity-side MVP integration steps.

**Files:**
- `/Assets/MetaDyn/Runtime/Avatar/MetaDynAvatarStorageService.cs`
- `/Assets/MetaDyn/Runtime/Avatar/GLBAvatarLoader.cs`
- `/Assets/MetaDyn/Runtime/Dashboard/SupabaseAuthManager.cs`
- `/Assets/MetaDyn/Runtime/Core/Starter/UIGameMenu.cs`
- `/Assets/MetaDyn/Runtime/Networking/MetaDynUGSPlayerController.cs`
- `/.claude/Planning/Runtime_Avatar_Upload_And_Rigging_Plan.md`

**Reason:** Establish the first runtime-persistent uploaded GLB avatar path while keeping existing prefab avatar selection additive and unchanged.

---

## 2026-06-05 - Netlify Deployment Compression Fix

**Changed:**
- Enhanced `MetaDynNetlifyService.cs` to generate both `_headers` and `netlify.toml` for maximum compatibility with Netlify's deployment engines.
- Updated header rules to use broader splat patterns (`/Build/*.br` and `/Build/*.gz`) to ensure Unity 6 builds with long or space-containing filenames are correctly served with `Content-Encoding`.
- Explicitly set `Content-Type` for `.js.br`, `.wasm.br`, `.data.br`, and `.framework.js.br` to match Unity's required MIME types.
- Forced UTF-8 (No BOM) encoding for configuration files to prevent parsing issues on Netlify's backend.

**Fixed:**
- Resolved "Failed to parse binary data" error in WebGL builds where Brotli-compressed assets were served without the proper encoding headers.

**Files:**
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynNetlifyService.cs`

**Reason:** Ensure production WebGL builds deployed via the Netlify API load correctly in all browsers by properly signaling file compression.

---

## 2026-06-05 - Unity MCP Bridge Configuration for Codex

**Added:**
- Documented Unity MCP bridge restart/verification steps in `STARTUP_SUMMARY.md`.

**Changed:**
- Installed Unity AI Assistant's relay binaries and configured Codex to use the Windows relay at `/mnt/c/Users/joshg/.unity/relay/relay_win.exe`.
- Added `[mcp_servers.unity_mcp]` to `~/.codex/config.toml` with `--mcp` and a Windows-format project-specific `--project-path` targeting this Unity project.

**Verified:**
- Relay starts and reports `Unity AI Relay` version `1.0.12-build.96`.
- Standalone MCP probe connected to Unity's named pipe for `MetaDynStarter-UGS`.
- `tools/list` returned `_server_info` plus 29 Unity tools, including scene, console, resource, script, GameObject, and command execution tools.
- The Linux relay was not suitable for this WSL-to-Windows Unity setup because Unity publishes Windows named-pipe bridge files under `C:\Users\joshg\.unity\mcp\connections\`.

**Operational Note:**
- Do not run more standalone `relay_win.exe --mcp` probes after restart. Each probe can register as a separate Unity MCP client and trigger another approval request. Use only the MCP connection Codex loads from `~/.codex/config.toml`.

**Files:**
- `/.claude/Quick Reference/STARTUP_SUMMARY.md`
- `~/.codex/config.toml`
- `/mnt/c/Users/joshg/.unity/relay/relay_win.exe`

**Reason:** Enable Codex to connect to the running Unity Editor through Unity's MCP bridge after the next Codex restart.

---

## 2026-05-30 - SDK Onboarding and Configuration Hardening

**Added:**
- Created `MetaDynWelcomePanel.cs` providing a branded, automatic-startup onboarding window for new SDK users.
- Implemented "Active Config" validation in `MetaDynProjectConfig` to ensure the selected world settings match the build's source-of-truth.
- Added a "Make Active" utility to automatically rename and relocate `MetaDynRuntimeConfig` assets into the required `Assets/Resources/` path.

**Changed:**
- Updated `MetaDynProjectConfig` with robust fallback logic to automatically reconnect to available config assets.
- Enhanced `MetaDynSDKValidator` with actionable fix-links for missing or inactive runtime configurations.
- Integrated `MetaDynWelcomePanel` into the top-level `MetaDyn` menu for easy re-access.

**Files:**
- `/Assets/MetaDyn/Core/Editor/MetaDynWelcomePanel.cs`
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynSDKValidator.cs`
- `/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`

**Reason:** Improving the "Pillar 2: Validation" creator experience by providing clear onboarding and hardening the link between Editor configuration and the production build's runtime settings.

---

## 2026-05-31 - Runtime Avatar Upload Planning

**Added:**
- Created `Runtime_Avatar_Upload_And_Rigging_Plan.md` establishing the blueprint for runtime user-model uploads (GLB/VRM), auto-rigging, and UGS/NGO network synchronization.

**Reason:** Initiating the "Dynamic Embodiment" feature to allow users to bring their own identity into the MetaDyn platform at runtime without build-time prefabs.

---

## 2025-05-29 - GitHub Deployment & Social UI Update

**Added:**
- Created `GITHUB_DEPLOYMENT_PLAN.md` blueprint for decentralized hosting.
- Implemented `SocialSortBar` in `SocialHubPanel.prefab` with Multi-Mode Sorting.
- Added `SocialHub_BaseIcon.png` and modular branding overlay system.

**Changed:**
- Updated `SocialHubUI.cs` with sorting logic (Alpha, Newest, Oldest, Favorite).
- Updated `SocialHubEntry.cs` with Favorite star toggle support.
- Corrected logo placement to top-left SideMenu per user indication.

**Files:**
- `/.claude/GITHUB_DEPLOYMENT_PLAN.md`
- `/.claude/CHANGELOG.md`
- `/Assets/MetaDyn/Social/SocialHubUI.cs`
- `/Assets/MetaDyn/Social/SocialHubEntry.cs`
- `/Assets/MetaDyn/Social/SocialHubPanel.prefab`

**Reason:** Establishing the Pillar 9 decentralized hosting strategy while finalizing the production-ready Social Hub UI for brand-swappable deployments.

---

## 2026-05-29 - Social Hub Implementation (Phase 1)

**Added:**
- Created `MetaDynSocialManager.cs` for Supabase social data orchestration (friends, communities).
- Created `SocialHubUI.cs` and `SocialHubEntry.cs` to manage the social hub interface.
- Established `Assets/MetaDyn/Social/` directory for social system assets.
- Implemented friend list fetching with Supabase join queries for profiles.

**Changed:**
- Exposed `SupabaseConfig` in `SupabaseAuthManager` for SDK-wide access.
- Updated `SOCIAL_HUB_ROADMAP.md` with communities and inventory integration details.

**Files:**
- `/Assets/MetaDyn/Managers/MetaDynSocialManager.cs`
- `/Assets/MetaDyn/Social/SocialHubUI.cs`
- `/Assets/MetaDyn/Social/SocialHubEntry.cs`
- `/Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs`
- `/.claude/Planning/SOCIAL_HUB_ROADMAP.md`

**Reason:** Bridging the Dashboard's social systems with the Unity runtime to enable player connectivity, community building, and inventory visualization.

---

## 2026-05-29 - Inventory System Branding and Menu Integration

**Added:**
- Created `MetaDynItemMetadataEditor.cs` providing a branded, utility-focused custom inspector for item metadata.
- Organized inventory scripts into `Assets/MetaDyn/Inventory/` with standard `Runtime` and `Editor` subdirectories.

**Changed:**
- Updated `MetaDynItemMetadata.cs` with `AddComponentMenu` for easier component discovery.
- Updated `MetaDynItemBundler.cs` menu path to `Tools > MetaDyn > Product Bundler`.
- Integrated `MetaDynEditorHeader` and `MetaDynStyle` into both the `MetaDynItemBundler` window and `MetaDynItemMetadata` inspector.

**Files:**
- `/Assets/MetaDyn/Inventory/Runtime/MetaDynItemMetadata.cs`
- `/Assets/MetaDyn/Inventory/Editor/MetaDynItemBundler.cs`
- `/Assets/MetaDyn/Inventory/Editor/MetaDynItemMetadataEditor.cs`
- `/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`
- `/.claude/CHANGELOG.md`

**Reason:** Ensure the new Inventory and Item management system aligns with the MetaDyn SDK's branding, UX patterns, and directory structure. Moving tools to `Tools > MetaDyn` and adding `AddComponentMenu` improves platform discoverability for creators.

---

## 2026-05-22 - SDK Sync Tool Scrollbar Fix

**Fixed:**
- Resolved an issue where the results scrollbar in the `SDK Sync Tool` was stuck or not functioning.
- Removed a nested `BeginScrollView` in `DrawResults` that was competing with the main window scrollview using the same `Vector2` state.

**Files:**
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynSDKSyncCheckWindow.cs`

**Reason:** Nested scrollviews using the same state variable in IMGUI cause "scroll fighting" and often result in a non-functional or jittery scrollbar. Consolidation into a single top-level scrollview ensures smooth navigation of comparison results.

## 2026-05-22 - UGS Zombie Session and UI Hardening

**Fixed:**
- Implemented automatic "Zombie Session" recovery in `MetaDynUGSSessionService`. If joining a discovered session fails (e.g., dead Relay allocation), the SDK now bypasses it and attempts to host a new session.
- Hardened `UIGameMenu` with `try-catch-finally` to ensure the "Joining..." state is always reset, allowing users to retry connections after failures.
- Fixed `DontDestroyOnLoad` console warnings by unparenting managers before marking them persistent.
- Resolved ambiguous `Random` reference and missing `System` using in `UIGameMenu`.

**Files:**
- `/Assets/MetaDyn/Networking/MetaDynUGSSessionService.cs`
- `/Assets/Common/UIGameMenu.cs`
- `/Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs`
- `/Assets/MetaDyn/Managers/UIManager.cs`
- `/.claude/CHANGELOG.md`

## 2026-05-22 - Spawning Flow Optimization

**Improved:**
- Decoupled player spawning from the internal networking handshake in `MetaDynUGSSessionService`.
- Modified `UIGameMenu` to trigger `EnsurePlayerObjectsSpawned` only *after* the login panel is deactivated. This prevents "flicker" and ensures the user only sees their avatar once the transition is complete.
- Exposed `EnsurePlayerObjectsSpawned` as a public method for UI-controlled spawn timing.

**Files:**
- `/Assets/MetaDyn/Networking/MetaDynUGSSessionService.cs`
- `/Assets/Common/UIGameMenu.cs`
- `/.claude/CHANGELOG.md`

## 2026-05-22 - SDK Performance and Stability Hardening

**Improved:**
- Moved `MetaDynPlatformDetector` execution from `Start` to `Awake`. This ensures platform-specific UI (like mobile joysticks or desktop-only panels) are toggled before the first frame, preventing UI flicker.
- Hardened `MetaDynUGSSessionService` with initialization locks and strict 15s operation timeouts for production WebGL reliability.
- Optimized `UIGameMenu` hide logic to trigger immediately upon successful NGO handshake.

**Files:**
- `/Assets/MetaDyn/Core/Runtime/Components/MetaDynPlatformDetector.cs`
- `/Assets/MetaDyn/Networking/MetaDynUGSSessionService.cs`
- `/.claude/CHANGELOG.md`

## 2026-05-22 - Platform Detection SDK Component Added

**Added:**
- Created `MetaDynPlatformDetector.cs` as an inspector-friendly SDK component for environment-specific branching.
- Added UnityEvents for WebGL, Mobile, XR, and Desktop detection.
- Implemented a branded Editor inspector for the component in `MetaDynComponentEditors.cs`.
- Updated `SDK_TOOLKIT_INVENTORY.md` to include the new component.

**Files:**
- `/Assets/MetaDyn/Core/Runtime/Components/MetaDynPlatformDetector.cs`
- `/Assets/MetaDyn/Core/Editor/MetaDynComponentEditors.cs`
- `/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`

**Reason:** Provide creators with a robust, branded way to handle platform-specific logic (e.g., enabling mobile HUDs, triggering VR-specific onboarding, or adjusting WebGL quality) directly from the Unity Inspector without writing code.

## 2026-05-22 - SOUL.md Integration and Startup Update

**Changed:**
- Updated `STARTUP_SUMMARY.md` to include `SOUL.md` in the "Read By Default" section.
- Added `SOUL.md` to the Documentation Map in `QUICK_REFERENCE.md`.

**Files:**
- `/.claude/Quick Reference/STARTUP_SUMMARY.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`

**Reason:** Ensure the "Ironman Jarvis" identity (Jen) and platform vision are always loaded as part of the core agent context.

## 2026-05-22 - WebGL Production Test Successful

**Added:**
- Verified full UGS/NGO/Vivox stack in a live WebGL production environment.
- Confirmed stability of the new NGO player controller and camera system.
- Validated Mobile Interaction HUD (Joystick/Jump) in browser.
- Successfully performed multi-user testing (4+ users) with spatial audio and lip-sync.

**Changed:**
- Updated maturity rating to 98% in `FDS.md` and `QUICK_REFERENCE.md`.
- Marked Phase 9: Production Test Gates as [COMPLETED] in the SDK Checklist.

**Files:**
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/Planning/FDS.md`
- `/.claude/UGSMigration/UGS_SDK_Production_Readiness_Checklist.md`
- `/.claude/UGSMigration/UGS_Networking_Plan.md`

**Reason:** Core networking and social systems are now verified in the primary target environment (WebGL), proving the success of the UGS migration.

## 2026-05-20 - Networked Emotes Restored for NGO


**Added:**
- Ported `EmoteManager.cs` to the NGO stack, enabling networked full-body emotes.
- Implemented `PlayEmoteServerRpc` and `PlayEmoteClientRpc` in `MetaDynUGSPlayerController` for global animation syncing.
- Restored hotkey support ("1" for Dance, "C" for Clap) for local players.
- Added movement-locking logic during emotes (configurable in the scene's `EmoteManager`).

**Changed:**
- Updated `EmoteManager` to be a Singleton for easier access by player instances.
- Replaced legacy Fusion player-finding logic with NGO `LocalClient` references.

**Files:**
- `Assets/MetaDyn/Core/Runtime/Components/Emote.cs`
- `Assets/MetaDyn/Networking/MetaDynUGSPlayerController.cs`

**Reason:** Ensure social expressions are networked and functional after the transition from Fusion to UGS/NGO.

**Added:**
- Created `MetaDynVivoxService.cs` for unified voice and text chat management using UGS Vivox.
- Implemented automatic Vivox login and channel join (positional voice + global text) in `MetaDynUGSSessionService`.
- Added mute/unmute synchronization between `MetaDynUGSUserListManager` and Vivox.

**Changed:**
- Refactored `ChatUI.cs` to use Vivox instead of the legacy Photon Chat system.
- Updated `FDS.md` and `Stage_1_UGS_Backend_Replacement.md` to reflect Vivox as the primary social layer.

**Files:**
- `Assets/MetaDyn/Networking/MetaDynVivoxService.cs`
- `Assets/MetaDyn/Networking/MetaDynUGSSessionService.cs`
- `Assets/MetaDyn/Chat/ChatUI.cs`
- `Assets/MetaDyn/UserList/MetaDynUGSUserListManager.cs`

**Reason:** Consolidate the social stack into UGS, removing external dependencies on Photon Chat and simplifying the Master SDK for production use.

**Added:**
- Restored networked Lip-Sync signaling by porting `WebRTCManager` to the NGO stack.
- Implemented WebRTC SDP/ICE signaling using NGO `CustomMessagingManager`.
- Added automatic peer discovery and connection initiation for WebRTC streams in UGS sessions.

**Changed:**
- Updated `WebRTCManager` to use `Unity.Netcode.NetworkBehaviour` and `NetworkVariable`.
- Refactored `WebRTCManager` to find lip-sync components on NGO-spawned player objects.

**Files:**
- `Assets/MetaDyn/Managers/WebRTCManager.cs`
- `.claude/UGSMigration/Stage_1_UGS_Backend_Replacement.md`
- `.claude/Planning/FDS.md`

**Reason:** Restore a critical social presence feature (lip-sync) that was broken during the transition from Fusion to UGS/NGO.

**Added:**
- Created `MetaDynUGSAvatarRegistry.cs` and asset for centralized avatar management.
- Implemented `ConnectionData` payload support in `MetaDynUGSSessionService` for passing avatar choices.
- Implemented Server-side manual spawning logic based on client choice index.
- Added `FindThumbnailImage` and `PopulateAvatarContainerFromRegistry` to `UIGameMenu.cs`.

**Changed:**
- Converted 8 legacy Fusion prefabs to NGO-ready UGS prefabs (PlayerAvatarSDK 0-4, Player 2, Player 3).
- Updated `UIGameMenu` to populate the avatar picker from the new `MetaDynUGSAvatarRegistry`.
- Updated `NetworkManager` in the main scene to include all NGO player prefabs.
- Fixed UI issue where avatar thumbnails appeared white due to missing sprite links.

**Files:**
- `Assets/MetaDyn/Networking/MetaDynUGSAvatarRegistry.cs`
- `Assets/Resources/MetaDynUGSAvatarRegistry.asset`
- `Assets/MetaDyn/Networking/MetaDynUGSSessionService.cs`
- `Assets/Common/UIGameMenu.cs`
- `Assets/Starter/PlayerPrefab/` (Updated 8 prefabs)
- `Assets/Starter/MetaDynStarter.unity`

**Reason:** Complete the core spawning loop for the UGS migration, enabling multi-avatar support and removing the final major dependency on the legacy Fusion GameManager for joining.

**Added:**
- Created `FDS.md` as the high-level Functional Design Specification and pseudo-PRD.
- Defined the project as the **Master SDK Template** for the entire MetaDyn platform.

**Changed:**
- Updated `STARTUP_SUMMARY.md` to load `FDS.md` with high priority.
- Updated `QUICK_REFERENCE.md` to reflect the Master SDK role and current UGS networking status.
- Marked Photon Fusion as Superseded in `DECISIONS.md` and added UGS baseline and Master SDK template decisions.

**Files:**
- `/.claude/Planning/FDS.md`
- `/.claude/Quick Reference/STARTUP_SUMMARY.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/DECISIONS.md`
- `/.claude/CHANGELOG.md`

**Reason:** Align project documentation with its new role as the canonical starter package and reflect the successful Phase 1 migration to Unity Gaming Services.

**Added:**
- Documented that Unity projects in this workspace use Unity Version Control and Unity Cloud connectivity, not Git
- Documented that Git should not be used for Unity project status, diff, or change tracking unless explicitly requested
- Documented that Unity `.meta` files should not be created, edited, deleted, or otherwise managed by automation

**Files:**
- `/.claude/Quick Reference/STARTUP_SUMMARY.md`
- `/.claude/README.md`
- `/.claude/WORKFLOW.md`
- `/.claude/CHANGELOG.md`

**Reason:** Make the Unity project workflow rule explicit so future work does not use Git assumptions or manually manage Unity `.meta` files.

## 2026-05-19 - SDK Console Logger Component Added

**Added:**
- Added `MetaDynConsoleLogger` as an inspector-friendly SDK component for logging UnityEvent output to the console
- Added methods for logging default messages, strings, warnings, errors, ints, floats, bools, and network relay message triples

**Changed:**
- Updated the SDK toolkit inventory to include the new logger component and refreshed file counts

**Files:**
- `/Assets/MetaDyn/Core/Runtime/Components/MetaDynConsoleLogger.cs`
- `/Assets/MetaDyn/Core/Runtime/Components/MetaDynConsoleLogger.cs.meta`
- `/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`
- `/.claude/CHANGELOG.md`

**Reason:** Provide a simple reusable logging utility that can be wired directly from UnityEvents while testing SDK components such as the UGS network event relay.

## 2026-05-19 - UGS Network Event Relay SDK Component Added

**Added:**
- Added `MetaDynNetworkEventRelay` as an inspector-friendly NGO/UGS SDK component for sending lightweight network events from UnityEvents
- Added self, others, and everyone audience choices
- Added byte-sized channel routing plus optional event name and string payload support
- Added received UnityEvents for generic receive, channel receive, payload-only receive, event-name-only receive, and channel/event/payload receive
- Added stable last-received properties for channel, event name, payload, and sender client ID

**Changed:**
- Updated the SDK toolkit inventory to list the new Networking SDK section and UGS event relay component
- Updated current SDK file counts in the inventory
- Added UGS user-list files to the inventory's User List section

**Files:**
- `/Assets/MetaDyn/Networking/MetaDynNetworkEventRelay.cs`
- `/Assets/MetaDyn/Networking/MetaDynNetworkEventRelay.cs.meta`
- `/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`
- `/.claude/CHANGELOG.md`

**Reason:** Provide a reusable creator-facing SDK component for small UGS/NGO event messages that can be wired directly through UnityEvents.

## 2026-05-18 - UGS SDK Production Readiness Checklist Added

**Added:**
- Created a focused UGS SDK production-readiness checklist for turning the current Starter UGS migration into the default MetaDyn SDK/platform baseline
- Added phased checklist coverage for SDK manifest/dashboard updates, UGS session hardening, player prefab stabilization, user list production behavior, voice/text direction, editor validation, deployment/runtime config wiring, Fusion cleanup, and production test gates
- Linked the new checklist from the UGS migration README

**Files:**
- `/.claude/UGSMigration/UGS_SDK_Production_Readiness_Checklist.md`
- `/.claude/UGSMigration/README.md`
- `/.claude/CHANGELOG.md`

**Reason:** Capture the agreed next steps in one actionable checklist so UGS production-readiness work can proceed without re-deriving priorities from multiple planning docs.

## 2026-05-16 - UGS Runtime Status And No-Fusion-Fallback Rule Documented

**Added:**
- Documented that the active Starter migration path is UGS/NGO-only, not a Fusion compatibility layer
- Documented current UGS player, user list, and AI spatial-awareness status in the Stage 1 UGS migration notes
- Documented that Photon/Fusion code may be used as behavior reference only while active runtime systems are ported away from it
- Added a cross-project UGS update file inventory that separates newly added files, existing files to merge, and Unity scene/project setup

**Changed:**
- Updated UGS migration docs to state that touched runtime systems should remove or port Fusion dependencies instead of adding fallbacks
- Updated current progress notes for manual NGO player spawning, camera binding ownership, UGS user list registration, player landing state, and AI player detection
- Updated the AI migration status to note that `AIPerceptionManager`, `MetaDynVoiceController`, and `FacePlayer` now use the UGS-spawned player path for detection/identity/facing
- Updated the Stage 1 docs so downstream projects can see exactly which UGS files should be copied and which existing project files need careful merging

**Current Status:**
- UGS session creation/join works
- Menu hides and main UI opens after join
- NGO player prefab spawns from the active `NetworkManager` player prefab
- Camera binds through the local `MetaDynUGSPlayerController`
- Basic movement and jumping work
- Landing state now returns the player animator to grounded after jumping
- UGS user list registration is active through `MetaDynUGSUserListManager`
- AI spatial awareness sees the UGS-spawned player again
- Avatar selection is still not fully wired into NGO spawning
- WebRTC remains required, but its Fusion reliable-data signaling path still needs a UGS/NGO replacement

**Files:**
- `/.claude/UGSMigration/Stage_1_UGS_Backend_Replacement.md`
- `/.claude/UGSMigration/README.md`
- `/.claude/CHANGELOG.md`

**Reason:** Capture the current handoff point accurately and prevent future work from reintroducing Fusion fallback behavior into the UGS migration path.

## 2026-05-16 - UGS NGO Player Spawn And Controller Progress

**Added:**
- Added `MetaDynUGSPlayerController` as the first NGO replacement for the old Fusion `Player` + `SimpleKCC` controller
- Added manual NGO player object spawning to the UGS session service after successful session join
- Added UGS/NGO spawn and camera-binding logs for player prefab setup, session role, client IDs, selected `EntrancePoint`, local player object discovery, and camera assignment
- Added current progress and known-issue notes to the Stage 1 UGS migration docs

**Changed:**
- Updated `MetaDynUGSSessionService` to match sessions by both `space_id` and configured session name
- Updated `MetaDynUGSSessionService` to configure NGO connection approval so player objects are spawned manually instead of relying on automatic `NetworkManager` player creation
- Updated the UGS player path so the local camera binds to the spawned NGO player object
- Updated the first-pass NGO player controller to use existing `PlayerInput`, `CameraFollow`, Animator parameters, first-person renderer hiding, and networked player name sync
- Updated movement iteration so basic movement and jumping work in play mode, with transform sync narrowed to the intended NGO `NetworkTransform` path

**Current Status:**
- UGS session connection works
- Menu hides and main UI opens after join
- NGO player prefab spawns
- Camera moves to the spawned player
- Basic movement and jumping work
- Movement remains somewhat jerky compared with the old Fusion `SimpleKCC` controller and needs further tuning
- Avatar selection is not yet fully wired into NGO spawning
- WebRTC remains required, but the current `WebRTCManager` must be ported from Fusion signaling to NGO/UGS signaling before it can return to the player prefab

**Files:**
- `/Assets/MetaDyn/Networking/MetaDynUGSSessionService.cs`
- `/Assets/MetaDyn/Networking/MetaDynUGSPlayerController.cs`
- `/.claude/UGSMigration/README.md`
- `/.claude/UGSMigration/Stage_1_UGS_Backend_Replacement.md`
- `/.claude/CHANGELOG.md`

**Reason:** Record the current handoff point for the UGS migration: room connectivity is proven, manual NGO player spawn works, and the first player controller port is functional but still needs smoothing and broader SDK feature migration.

## 2026-05-16 - Stage 1 UGS Session Connector Added

**Added:**
- Added `MetaDynUGSSessionService` as the first Starter-side Unity Gaming Services session connector
- Added UGS package dependencies for Netcode for GameObjects, Unity Authentication, Unity Multiplayer Services, and Vivox
- Added `Stage_1_UGS_Backend_Replacement.md` as the reusable migration process document for applying this backend replacement to other MetaDyn projects

**Changed:**
- Updated `UIGameMenu.StartGame()` so the existing menu/auth/avatar flow joins a deterministic UGS session from `MetaDynRuntimeConfig.Instance` instead of starting a Fusion `NetworkRunner`
- Updated `UIGameMenu.Disconnect()` and menu state checks so the current UGS session can be disconnected through the existing UI flow
- Updated the Stage 1 UGS service from Distributed Authority sessions to standard Relay-backed sessions with explicit WSS protocol for WebGL-first compatibility
- Documented the concrete Stage 1 implementation files in the UGS migration notes
- Documented the required Unity scene setup for an explicit NGO `NetworkManager` + `UnityTransport` object instead of runtime-creating one in code

**Files:**
- `/.claude/UGSMigration/Stage_1_UGS_Backend_Replacement.md`
- `/Packages/manifest.json`
- `/Assets/MetaDyn/Networking/MetaDynUGSSessionService.cs`
- `/Assets/Common/UIGameMenu.cs`
- `/.claude/UGSMigration/README.md`
- `/.claude/CHANGELOG.md`

**Reason:** Implement the first production-oriented UGS connectivity pass while preserving the existing `UIGameMenu`, profile/auth flow, avatar picker, and runtime config contract.

## 2026-05-16 - MetaDyn VR UGS Reference Notes Added

**Added:**
- Documented MetaDyn VR as the first UGS/Relay/Vivox reference project for the Starter UGS migration track
- Captured the VR project's Stage 1 config-driven auto-join bridge pattern, Unity-native auth gate, deterministic room grouping approach, and Vivox microphone-sharing caution
- Added concrete notes from the VR code path for `MetaDynRuntimeConfig`, `MetaDynRuntimeManager`, `SDKMultiplayerBridge`, `XRINetworkGameManager.JoinDeterministicRoom`, and `SessionManager.CreateSession`
- Documented that the reusable pattern for Starter is the config-to-session bridge, not the VR UI shell
- Recorded the Stage 1 Starter implementation shape: preserve `UIGameMenu`, auth/profile flow, avatar picker, and existing runtime config while replacing only the Fusion join backend with a UGS session join
- Noted that any future backend swap consideration should be UGS to custom WebSockets plus Cloudflare Durable Objects, not a Stage 1 Photon/UGS switcher

**Files:**
- `/.claude/UGSMigration/README.md`
- `/.claude/CHANGELOG.md`

**Reason:** Preserve the user's note that the VR project's `.claude` docs should inform this Starter UGS migration, especially around basic UGS connectivity and Vivox voice, while keeping the copied networking plan as reference material only.

## 2026-05-16 - UGS Migration Documentation Folder Added

**Added:**
- Created `.claude/UGSMigration/README.md` to mark this project as the Unity Gaming Services migration track for the current Photon-based MetaDyn project and SDK
- Copied the Pavilion `UGS_Networking_Plan.md` into `.claude/UGSMigration/` as the initial migration reference material

**Files:**
- `/.claude/UGSMigration/README.md`
- `/.claude/UGSMigration/UGS_Networking_Plan.md`
- `/.claude/CHANGELOG.md`

**Reason:** Establish a dedicated documentation area for the UGS migration effort and preserve the Pavilion networking plan as the starting reference for porting the project and SDK from Photon to Unity Gaming Services.

## 2026-04-11 - SDK Sync Check Dynamic Script Root Resolution

**Changed:**
- Updated `SDK Sync Check` so baseline platform script entries are resolved by file identity when the project-specific folder under `Assets/*/Scripts/` is not literally `Pavilion`
- Kept the canonical SDK comparison keys for those files while mapping them to the actual on-disk script location in each project
- Reduced false `Missing in current` results for shared baseline files like `GameManager.cs`, `Player.cs`, `PlayerInput.cs`, and the lip-sync bridge scripts when downstream projects rename the top-level scripts folder
- Simplified the dynamic script-root resolver so those baseline entries are matched by filename under `Assets/*/Scripts/`, without depending on project-name similarity

**Files:**
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynSDKSyncCheckWindow.cs`
- `/.claude/CHANGELOG.md`

**Reason:** The sync checker was treating canonical `Assets/Pavilion/Scripts/...` paths as literal requirements even though downstream MetaDyn projects often store the same baseline platform scripts under a project-specific folder such as `Assets/Starter/Scripts/...`.

## 2026-04-11 - SDK Sync Check File Classification Tags

**Changed:**
- Added a classification legend to `SDK Sync Check` so result rows can be read as shared SDK, shared baseline, cross-project shared, manual-merge hotspot, or project-specific drift
- Tagged each result path inline so cross-project comparison work can more quickly separate common MetaDyn files from build-specific differences
- Marked known cross-project/manual-merge hotspots like `LoginUI`, `UIGameMenu`, and `MetaDynVoiceController` directly in the UI instead of relying on memory or external notes

**Files:**
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynSDKSyncCheckWindow.cs`
- `/.claude/CHANGELOG.md`

**Reason:** The sync checker already showed file differences, but it did not visually distinguish portable shared SDK files from project-specific drift or known manual-merge hotspots when comparing Starter against downstream projects like VITL Medical.

## 2026-04-11 - SDK Sync Check Window Accordion Cleanup

**Changed:**
- Made the `Projects` and `Scope` sections in `SDK Sync Check` collapsible using foldout-header/accordion-style UI
- Set the top `Projects` section open by default and the `Scope` section collapsed by default to reduce visual density in the editor window

**Files:**
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynSDKSyncCheckWindow.cs`
- `/.claude/CHANGELOG.md`

**Reason:** The SDK sync checker editor window was getting crowded as more controls were added. Matching the top configuration sections to the collapsible lower sections keeps the UI easier to scan without removing functionality.

## 2026-04-11 - SDK Sync Check GitHub Source Extension

**Changed:**
- Updated the starter project's `SDK Sync Check` editor window to match the latest Pavilion implementation
- Added comparison source modes for:
  - another local Unity project
  - the canonical MetaDyn SDK/Starter GitHub archive configured by `MetaDynSDKManifest.json`
- Expanded comparison results to show:
  - same files
  - missing files in current project
  - extra files in current project
  - different-content files
- Added manifest tracked-root support in scope building
- Added a planned action model and UI section so future recommended actions and one-click fixes can be layered onto the current read-only comparison flow without restructuring the tool
- Updated the starter SDK inventory to include `MetaDynSDKSyncCheckWindow.cs`

**Files:**
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynSDKSyncCheckWindow.cs`
- `/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`
- `/.claude/CHANGELOG.md`

**Reason:** Make the starter project the current baseline for SDK sync work, with the same GitHub-aware read-only sync checker and matching SDK inventory documentation.

## 2026-04-11 - Cross-Project SDK Sync Notes Added

**Added:**
- Created a dedicated cross-project SDK sync notes document covering the starter baseline, VITL Medical, and NetflixHouse

**Changed:**
- Documented which shared auth and voice-controller files are direct-sync candidates versus manual-merge candidates
- Captured the current downstream gaps for VITL and NetflixHouse relative to recent starter auth-routing and voice-controller detection changes
- Linked the new cross-project sync doc from the quick reference map

**Files:**
- `/.claude/Planning/SDK_Cross_Project_Sync_Notes.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/CHANGELOG.md`

**Reason:** Shared MetaDyn SDK behavior now needs to stay aligned across multiple downstream projects. A lightweight sync document was needed so future sessions can quickly see which files diverged, what changed in the starter baseline, and where manual merges are required.

## 2026-04-11 - Auth And AI Detection Documentation Refresh

**Changed:**
- Updated auth reference docs to document the current WebGL behavior where active `LoginUI` takes precedence over dashboard token auth in that scene and keeps the cursor unlocked while login is visible
- Updated AI embodiment docs to document the new voice-controller user-detection events, session greeting tracking, one-shot internal-event response path, and UnityEvent inspector wiring pattern
- Added quick-reference notes pointing future sessions to the new auth override and detection-hook behavior

**Files:**
- `/.claude/Quick Reference/AUTH_SYSTEM.md`
- `/.claude/Quick Reference/AI_EMBODIMENT.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/CHANGELOG.md`

**Reason:** Recent code changes introduced important runtime behavior around WebGL auth routing and AI perception-driven greeting hooks. The quick-reference docs needed to reflect the actual current contracts so future sessions do not have to rediscover them from code.

## 2026-04-10 - Voice Controller User Detection Greeting Hooks

**Added:**
- Added a voice-controller-level user detection event that fires when perception detects a new active user
- Added a no-argument companion detection event for easier Unity inspector wiring
- Added session greeting state tracking helpers so greeting systems can check whether a detected user has already been greeted in the current runtime session
- Added a one-shot internal-event response trigger so non-user events can prompt the model without being stored as fake user chat
- Added an inspector-friendly `TriggerGreetingForCurrentDetectedUser()` entry point for wiring greeting behavior from detection events
- Added configurable per-event instruction support so internal event responses can be customized for greetings, warnings, prompts, or other AI reactions
- Added `TriggerDetectedUserResponseFromInspector(string instruction)` so UnityEvents that only expose a single string parameter can still trigger configurable detected-user responses

**Changed:**
- Added inspector options to evaluate per-session greeted state and optionally auto-mark detected users as greeted when the detection event fires
- Moved user identity resolution into reusable voice-controller helpers so detection events and session greeting checks work even without the memory manager assigned

**Files:**
- `/Assets/MetaDyn/AI/MetaDynVoiceController.cs`
- `/.claude/CHANGELOG.md`

**Reason:** Perception already detected users internally, but there was no clean voice-controller event or configurable session-level greeted-state tracking for hooking automatic greeting behavior without duplicating detection logic elsewhere.

## 2026-04-10 - WebGL LoginUI Auth Mode Override Fix

**Changed:**
- Made `LoginUI` explicitly claim authentication handling for scenes that include it, including WebGL builds
- Prevented `UIGameMenu` from starting dashboard web-auth token checks when `LoginUI` is present and active in the scene
- Prevented WebGL builds using `LoginUI` from hiding the login panel and redirecting to the dashboard unintentionally
- Kept the cursor unlocked while the `LoginUI` panel is visible so WebGL input fields remain focusable without pressing Escape first

**Files:**
- `/Assets/MetaDyn/Dashboard/LoginUI.cs`
- `/Assets/Common/UIGameMenu.cs`
- `/.claude/CHANGELOG.md`

**Reason:** WebGL builds with `LoginUI` were still falling into the dashboard web-auth path, which hid the Unity login flow, redirected unauthenticated users to the dashboard, and bypassed the intended manual login/spawn path that already worked in Play Mode.

## 2026-04-09 - LoginUI Auth Gate and Spawn Flow Fix

**Changed:**
- Made `LoginUI` explicitly hide the gameplay/start UI until authentication completes in manual login flows
- Ensured successful manual login reveals the gameplay UI, hides the login panel, and continues into the existing spawn/avatar flow instead of stalling on the login screen
- Added a fallback path so authenticated users can still proceed if profile loading fails after login
- Unified manual login profile handoff with the same shared `UIGameMenu` profile UI path used by web auth, including profile image/name updates

**Fixed:**
- Prevented gameplay UI from remaining available behind the login form during failed login attempts
- Prevented manual login success from getting stuck waiting on the login panel when auth succeeded but downstream profile flow was brittle
- Fixed manual login not updating the shared user profile image/name UI even though web auth already did

**Files:**
- `/Assets/MetaDyn/Dashboard/LoginUI.cs`
- `/Assets/Common/UIGameMenu.cs`
- `/.claude/CHANGELOG.md`

**Reason:** The in-scene Unity login flow could leave the start/game UI active during failed authentication and could stall after valid login instead of hiding the login panel and continuing into the expected world join flow.

## 2026-04-10 - Auth Mode And SDK Portability Documentation Update

**Changed:**
- Documented the current three-mode auth model: guest/no-auth, dashboard web auth, and Unity `LoginUI`
- Added a cross-project integration checklist for copying the shared auth/menu SDK scripts into other MetaDyn SDK-based projects
- Updated SDK docs to explicitly treat `LoginUI.cs` and `UIGameMenu.cs` as part of the same portable auth/join contract

**Files:**
- `/.claude/Quick Reference/AUTH_SYSTEM.md`
- `/.claude/Quick Reference/SDK_DEVELOPMENT.md`
- `/.claude/Quick Reference/SDK_TOOLKIT_INVENTORY.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/CHANGELOG.md`

**Reason:** The shared auth and join behavior now spans guest access, dashboard web auth, and Unity login across multiple SDK-based projects, so the portability rules and integration expectations needed to be made explicit in the docs.

## 2026-04-10 - SDK Updater And Build Server Architecture Plan Added

**Added:**
- Created a dedicated architecture/planning document for the SDK updater, deployment API, remote build support, managed hosting, self-host deployment, and deployment-session token model

**Changed:**
- Linked the new architecture plan from the quick reference, SDK docs, update-manifest doc, deployment doc, and infrastructure doc

**Files:**
- `/.claude/Planning/SDK_Update_And_Build_Server_Architecture.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/Quick Reference/SDK_DEVELOPMENT.md`
- `/.claude/Quick Reference/SDK_UPDATE_MANIFEST.md`
- `/.claude/Quick Reference/DEPLOYMENT_ARCHITECTURE.md`
- `/.claude/Quick Reference/INFRASTRUCTURE.md`
- `/.claude/CHANGELOG.md`

**Reason:** The updater and deployment roadmap now spans local builds, remote builds, managed deployment, self-host deployment, and secure deployment-session tokens, so the architecture needed its own canonical planning document and discoverable references from the existing SDK and deployment docs.

## 2026-04-10 - SDK Updater And Build Server Implementation Plan Added

**Added:**
- Created a concrete phased implementation plan for the updater, deployment mode abstraction, managed deploy flow, remote build flow, and managed self-host support

**Changed:**
- Linked the implementation plan from the parent architecture doc and from the quick-reference / SDK / deployment docs

**Files:**
- `/.claude/Planning/SDK_Updater_And_Build_Server_Implementation_Plan.md`
- `/.claude/Planning/SDK_Update_And_Build_Server_Architecture.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/Quick Reference/SDK_DEVELOPMENT.md`
- `/.claude/Quick Reference/DEPLOYMENT_ARCHITECTURE.md`
- `/.claude/CHANGELOG.md`

**Reason:** The architecture plan was useful as a target state, but implementation work also needed a concrete, phased breakdown tied to the current Unity editor files so the work can be executed in sequence without code guesswork.

## 2026-03-12 - VITL Starter Template Checklist

**Added:**
- Created a planning/checklist document for turning the Pavilion + MetaDyn SDK codebase into a client starter template for VITL

**Changed:**
- Documented the recommended rollout order for VITL, including using a MetaDyn-hosted subdomain first and treating `vitl.world` as a later custom-domain step unless auth handoff is built
- Captured the concrete setup areas for runtime config, auth wiring, deployment profiles, scene conversion, and launch readiness

**Files:**
- `/.claude/Planning/VITL_Starter_Template_Checklist.md`
- `/.claude/CHANGELOG.md`

**Reason:** Provide a practical migration checklist for onboarding the VITL client onto the current Pavilion + MetaDyn SDK platform without assuming unsupported custom-domain auth behavior on day one.

## 2026-03-12 - Startup Summary Added

**Added:**
- Created a machine-oriented startup summary file in `.claude/Quick Reference/STARTUP_SUMMARY.md`

**Changed:**
- Updated startup workflow docs to point at `STARTUP_SUMMARY.md` first instead of implicitly loading the broader quick-reference set
- Added the new summary file to the quick-reference documentation map

**Files:**
- `/.claude/Quick Reference/STARTUP_SUMMARY.md`
- `/.claude/README.md`
- `/.claude/WORKFLOW.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/CHANGELOG.md`

**Reason:** Reduce startup context usage by making the default preload a compact routing document and reserving deeper quick-reference docs for on-demand loading by task area.

## 2026-03-12 - Dev vs Prod Deployment Pattern Documented

**Changed:**
- Added a concrete dev-vs-prod deployment pattern to the deployment architecture reference
- Documented the recommended branch, server-profile, runtime-config, and nginx-host split for `pavilion.metadyn.xyz` vs `dev.pavilion.metadyn.xyz`
- Called out the current code behavior that appends `/{roomName}-{spaceId}/` to deployed URLs and paths

**Files:**
- `/.claude/Quick Reference/DEPLOYMENT_ARCHITECTURE.md`
- `/.claude/CHANGELOG.md`

**Reason:** Capture a practical environment-separation strategy for the current Unity deployment tooling so dev and production hosting can be planned without assuming unsupported bare-root deployment behavior.

## 2026-03-12 - Quick Reference Path Cleanup

**Changed:**
- Updated active documentation and skill references to use the current quick-reference path under `.claude/Quick Reference/`
- Corrected the top-level `.claude` folder structure example to show the `Quick Reference/` directory

**Files:**
- `/.claude/README.md`
- `/.claude/WORKFLOW.md`
- `/.claude/skills/README.md`
- `/.claude/skills/community-manager/SKILL.md`
- `/.claude/skills/devops-specialist/SKILL.md`
- `/.claude/skills/marketing-strategist/SKILL.md`
- `/.claude/skills/metaverse-cto/SKILL.md`
- `/.claude/skills/unity-architect/SKILL.md`
- `/.claude/skills/ux-architect/SKILL.md`
- `/.claude/Planning/MetaDyn_Platform_PRD_v1.0.md`
- `/.claude/CHANGELOG.md`

**Reason:** The quick reference was moved into `.claude/Quick Reference/`, but several active docs still pointed at the old `.claude/QUICK_REFERENCE.md` path, which would misdirect future startup and skill workflows.

## 2026-03-07 - Deployment Directory Verification Hardening

**Changed:**
- Hardened Unity deployment preflight to fail fast if the remote deployment directory cannot be created and verified over SSH
- Added explicit remote directory verification before `rsync`/`scp` transfer begins
- Added blocking editor dialog with server/path/error details when directory setup fails

**Files:**
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `/.claude/Quick Reference/DEPLOYMENT_ARCHITECTURE.md`
- `/.claude/Quick Reference/INFRASTRUCTURE.md`
- `/.claude/CHANGELOG.md`

**Reason:** Prevent deployments from continuing into `rsync`/`scp` when the target path was not actually created, reducing ambiguous failures and making preflight errors visible immediately in the Unity Editor.

## 2026-03-04 - Documentation Scope Compliance Update

**Changed:**
- Added explicit instruction-compliance rules to `.claude/README.md`
- Added explicit scope-control and startup compliance rules to `.claude/WORKFLOW.md`
- Added bold non-negotiable instruction-following rules to `.claude/Quick Reference/QUICK_REFERENCE.md`

**Files:**
- `/.claude/README.md`
- `/.claude/WORKFLOW.md`
- `/.claude/Quick Reference/QUICK_REFERENCE.md`
- `/.claude/CHANGELOG.md`

**Reason:** Make strict compliance with user instructions explicit in the project docs: read the requested docs, follow them, and do not perform unrequested side work.

## 2025-01-03 - Stage 1: Login Dashboard & User Management Complete

**Completed full Supabase authentication integration with web-first auth flow**

**Added:**
- `SupabaseAuthManager.cs` - Singleton for login, signup, session management, token validation
- `SupabaseConfig.cs` - ScriptableObject for Supabase URL and anon key credentials
- `WebAuthBridge.cs` - C# bridge with inspector settings (RequireAuth, EnableWebAuth, DashboardUrl)
- `LoginUI.cs` - Fallback login UI for Editor testing with UIGameMenu integration
- `AuthBridge.jslib` - JavaScript bridge for cookie/localStorage token handling and redirects

**Features:**
- Web-first authentication (Spatial.io style) - login on dashboard, token via cookie
- Three auth modes: Guest (no login), Web-first (cookie SSO), Manual (LoginUI fallback)
- Cross-subdomain SSO via `metadyn_token` cookie (domain=.metadyn.xyz)
- Profile fetching with name, avatar_url, avatar_index
- Avatar choice persistence to Supabase (avatar_index column)
- Auto-spawn for returning users with saved avatar
- ?redirect= param handling for seamless Unity ↔ Dashboard flow

**Documentation Refactor:**
- Split QUICK_REFERENCE.md into 4 files (was exceeding token limits)
- Created `.claude/Quick Reference/` folder
- New files: QUICK_REFERENCE.md, AI_EMBODIMENT.md, INFRASTRUCTURE.md, AUTH_SYSTEM.md
- Updated all cross-references with proper relative links

**Files:**
- `/Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs` (NEW)
- `/Assets/MetaDyn/Dashboard/SupabaseConfig.cs` (NEW)
- `/Assets/MetaDyn/Dashboard/WebAuthBridge.cs` (NEW)
- `/Assets/MetaDyn/Dashboard/LoginUI.cs` (NEW)
- `/Assets/Plugins/WebGL/AuthBridge.jslib` (NEW)
- `/.claude/Quick Reference/` folder (NEW - 4 files)

**Database:**
- Added `avatar_index` column to Supabase profiles table (INTEGER DEFAULT -1)
- -1 = no avatar selected (show picker), 0+ = valid avatar index

**Verified:**
- ✅ Login/signup via Supabase REST API
- ✅ Token validation with /auth/v1/user endpoint
- ✅ Profile fetching and avatar_index sync
- ✅ Cookie-based SSO across subdomains
- ✅ LoginUI fallback in Editor
- ✅ Three auth modes working

**Reason:** Moved authentication from clunky Unity UI to web dashboard for better UX, password manager support, OAuth readiness, and faster Unity load times. Stage 1 of dashboard integration complete.

---

## 2025-12-21 - Dynamic Avatar Selection System

**Created scalable avatar selection UI with dual scrollviews**

**Added:**
- `AvatarEntry` serializable class in GameManager (NetworkObject prefab + Sprite thumbnail)
- Two avatar lists on GameManager: `readyPlayerMeAvatars` and `avatarSDKAvatars`
- Dynamic UI population in UIGameMenu with horizontal scrollviews
- Index-based selection system (combined index across both lists)
- Separate containers for RPM and AvatarSDK avatars
- Thumbnail display with proper Image component detection
- WebGL timing fix: waits for GameManager.Instance before populating UI

**Changed:**
- Removed static `MaleAvatarPrefab` and `FemaleAvatarPrefab` fields from GameManager
- Replaced hardcoded 0/1 avatar choice with unlimited index-based system
- UIGameMenu now populates avatar UI in Update() instead of OnEnable()
- Avatar selection now scales to unlimited avatars without code changes

**Fixed:**
- WebGL thumbnail display issue (timing: UIGameMenu tried to access GameManager before it spawned)
- Image component detection now searches for "Thumbnail" child GameObject
- Added `preserveAspect = true` for proper thumbnail rendering

**Files:**
- `/Assets/Pavilion/Scripts/GameManager.cs` - Added AvatarEntry class, dual avatar lists, GetAllAvatars() method
- `/Assets/Common/UIGameMenu.cs` - Dynamic UI generation, separate RPM/AvatarSDK containers, WebGL timing fix

**UI Setup:**
- Two horizontal ScrollViews (RPM + AvatarSDK)
- Each with HorizontalLayoutGroup + ContentSizeFitter on Content object
- AvatarEntryPrefab: Button (root) + Image child (thumbnail) with LayoutElement

**How It Works:**
1. GameManager stores avatar lists (prefab + thumbnail per entry)
2. UIGameMenu waits for GameManager.Instance to exist
3. Populates two separate scrollview containers dynamically
4. Each avatar gets index (RPM: 0, 1, 2..., AvatarSDK: 3, 4, 5...)
5. Saves selected index to PlayerPrefs
6. GameManager reads index and spawns correct prefab

**Verified:**
- ✅ Works in Unity Editor play mode
- ✅ Works in WebGL builds (thumbnails display correctly)
- ✅ Scalable to unlimited avatars
- ✅ Selection persists between sessions

**Reason:** Previous static male/female system was limited to 2 avatars. New system supports unlimited avatars across two categories (Ready Player Me + Avatar SDK), with visual thumbnails for easy selection. Essential for avatar marketplace and user choice.

---

## 2025-12-20 - Expert Agent Skills System (Updated: 6 Skills)

**Created 6 specialized AI agent skills for MetaDyn development**

**Added:**
- Metaverse CTO skill (platform strategy, economics, scaling, monetization)
- Unity Technical Architect skill (implementation, networking, performance)
- UX Architect skill (player-facing systems, onboarding, social features)
- DevOps Specialist skill (infrastructure, CI/CD, monitoring, costs)
- **Marketing Strategist skill** (user acquisition, brand positioning, growth, partnerships) **NEW**
- **Community Manager skill** (community building, moderation, Discord, events) **NEW**

**How It Works:**
- Skills automatically activate when Claude detects relevant topics
- Each skill has domain expertise and understands MetaDyn's context
- Skills can work independently or collaboratively
- Full workflow: CTO (strategy) → Marketing (go-to-market) → UX (design) → Unity (implement) → DevOps (deploy) → Community (engage)

**Files:**
- `.claude/skills/metaverse-cto/SKILL.md` (NEW)
- `.claude/skills/unity-architect/SKILL.md` (NEW)
- `.claude/skills/ux-architect/SKILL.md` (NEW)
- `.claude/skills/devops-specialist/SKILL.md` (NEW)
- `.claude/skills/marketing-strategist/SKILL.md` (NEW)
- `.claude/skills/community-manager/SKILL.md` (NEW)
- `.claude/skills/README.md` (NEW - usage guide, updated to v2.0)

**Example Usage:**
```
"Should MetaDyn support land ownership?" → CTO analyzes economics
"Implement a door system" → Unity Architect provides code
"Design friend request flow" → UX Architect creates user flows
"Set up monitoring" → DevOps configures analytics
"Plan our beta launch" → Marketing Strategist creates campaign
"Create Code of Conduct" → Community Manager designs policies
```

**Benefits:**
- Strategic thinking before coding
- Consistent with MetaDyn patterns
- Domain-specific expertise (technical + business + community)
- Cost and scale awareness
- Go-to-market planning
- Community engagement from day one
- Team knowledge sharing (skills committed to git)

**Reason:** As MetaDyn reaches 80-85% technical completion, next phase requires strategic platform decisions (economy, scaling, monetization) PLUS successful launch and community building. Specialized agents ensure decisions are informed by industry expertise across all domains.

---

## 2025-12-20 - WebRTC Lip Sync Integration

**Fixed WebRTC-triggered lip sync for networked players**

**Problem:**
- Spatial audio was working perfectly
- WebRTC was detecting speech and calling `StartSpeaking()` on AvatarSdkPlayerLipSync
- But lip sync animations weren't playing for remote players
- Root cause: `Update()` method was monitoring `audioSource` field and immediately cancelling WebRTC-triggered lip sync because audioSource wasn't playing

**Fixed:**
- Added `webRTCControlled` boolean flag to AvatarSdkPlayerLipSync
- When WebRTC calls `StartSpeaking()`, it sets flag to prevent Update() interference
- When WebRTC calls `StopSpeaking()`, it clears flag
- Update() now only monitors audioSource when NOT under WebRTC control

**Files:**
- `/Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs` (MODIFIED)

**Result:**
- ✅ Spatial audio verified working
- ✅ Lip sync verified working with WebRTC voice
- ✅ AudioSource testing still works (no regression)
- Both triggering mechanisms (WebRTC + AudioSource) now coexist without conflict

**Reason:** Essential for realistic multiplayer communication - players can now see lip movement synchronized with voice over WebRTC P2P voice chat.

---

## 2025-12-18 - Supabase Authentication Integration

**Implemented Supabase authentication system for Unity-Dashboard integration**

**Added:**
- SupabaseAuthManager singleton for login/signup/logout
- SupabaseConfig ScriptableObject for storing Supabase URL and API keys
- LoginUI component that integrates with UIGameMenu
- Profile fetching from Supabase profiles table
- Auto-spawn on successful login with profile name

**Files:**
- `/Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs` (NEW)
- `/Assets/MetaDyn/Dashboard/SupabaseConfig.cs` (NEW)
- `/Assets/MetaDyn/Dashboard/LoginUI.cs` (NEW)

**How It Works:**
1. User enters email/password in LoginUI
2. SupabaseAuthManager authenticates with Supabase (same instance as React dashboard)
3. Fetches user profile (id, name, avatar_url) from profiles table
4. Sets UIGameMenu nickname to profile.name
5. Auto-spawns player into world

**Data Structure:**
- `SupabaseUser` (from auth.users): id, email, role
- `SupabaseProfile` (from profiles table): id, name, avatar_url
- Email comes from auth response, NOT profiles table

**Integration Status:**
- ✅ Authentication working with dashboard's Supabase instance
- ✅ Profile data fetched correctly
- ✅ Auto-spawn integrated with UIGameMenu
- 🚧 Remaining: Space data API, launch flow, asset management

**Reason:** First step in Unity-Dashboard integration. Users can now login to Unity with their dashboard credentials and spawn with their profile name.

---

## 2025-12-19 - SDK Component Pattern Established

**Established standardized pattern for MetaDyn SDK components**

**Added:**
- SeatHotspot.cs as first example of SDK component pattern
- SDK Component Pattern documentation in QUICK_REFERENCE.md
- Component pattern checklist for future SDK features

**Files:**
- `/Assets/MetaDyn/Core/Runtime/SeatHotspot.cs` (NEW - user created)
- `/.claude/QUICK_REFERENCE.md` (updated with SDK Component Pattern section)

**Pattern Requirements:**
- MetaDyn namespace for all SDK components
- XML documentation on classes
- [Header] and [Tooltip] attributes on all public fields
- Public API for external script access
- Inline editor visualization with #if UNITY_EDITOR
- Clear gizmos and scene view helpers
- Inspector-friendly configuration
- Minimal or documented dependencies

**SeatHotspot Features:**
- Interactive sit/stand system with custom animations
- Forced avatar orientation (optional)
- Priority-based auto-assignment
- Runtime sprite indicators (billboard to camera)
- Interaction range and customizable key binding
- Position offset control
- Editor gizmos (seat position, orientation arrow, interaction range)
- Integration with SimpleKCC and PlayerInput
- Fusion networking compatible

**Public API:**
```csharp
bool IsOccupied              // Check if seat is taken
GameObject OccupyingAvatar   // Get current occupant
bool SitDown(GameObject avatar)  // Make avatar sit
void StandUp()               // Stand up current occupant
void ForceStandUp()          // Admin override
```

**Reason:** Establish clear pattern for SDK components that world creators will use. All future SDK features (teleporters, doors, triggers, etc.) will follow this pattern for consistency and ease of use.

**Impact:**
- Clear development guidelines for future SDK components
- Inspector-friendly components for non-programmers
- Consistent API design across MetaDyn SDK
- Reduced learning curve for world creators
- SeatHotspot provides reference implementation

---

## 2025-12-11 - Photon Voice Integration Plan

**Created comprehensive implementation plan for real-time voice chat**

**Added:**
- Detailed Photon Voice integration guide (4-phase plan)
- Production-ready implementation strategy (~4 hours)
- Code examples for push-to-talk, mute controls, spatial audio
- Testing checklist (local, WebGL, production)
- Troubleshooting guide for common issues

**Files:**
- `/Assets/Docs/Photon_Voice_Integration_Plan.md` (complete guide)

**Plan Includes:**
- Phase 1: Package setup and Fusion weaver configuration
- Phase 2: Scene setup (FusionVoiceClient, Recorder, Speaker)
- Phase 3: Player prefab integration (VoiceNetworkObject)
- Phase 4: Production features (PTT, mute, admin controls, indicators)

**Key Features Planned:**
- Real-time voice chat (< 200ms latency)
- Spatial 3D audio (proximity-based)
- Push-to-talk with InputManager integration
- Admin/moderator force-mute capabilities
- Speaking indicators on nametags
- WebGL compatible

**Architecture Decision:**
- Keep both voice systems:
  - Photon Voice = Player-to-player real-time chat
  - OpenAI Voice = AI agent conversations (existing MetaDynVoiceController)

**Timeline:** 3.5-4.5 hours total (package → testing → production-ready)

---

## 2025-12-11 - Ready Player Me Stage 1 Implementation

**Status:** Stage 1 Complete - Basic RPM Integration

**Added:**
- Ready Player Me Core SDK 7.4.0 (via GitHub package)
- Basic RPM avatar integration for AI Agent (AI_Agent.fbx)
- Wolf3D lip sync system for avatar facial animations
- MetaDynVoiceController with OpenAI integration (Whisper, Assistants API, TTS)
- RPM avatar animations (idle variations, talking variations)
- Multiple player prefab variants for testing

**Files:**
- `/Assets/Pavilion/AI_Agent/RPMVers/AI_Agent.fbx` (RPM avatar)
- `/Assets/Pavilion/AI_Agent/Scripts/Wolf3DLipSync.cs` (lip sync system)
- `/Assets/Pavilion/AI_Agent/Scripts/Wolf3DLipSyncTimestamped.cs`
- `/Assets/Pavilion/Scripts/MetaDynVoiceController.cs` (complete voice AI system)
- `/Assets/Pavilion/Player.prefab`, `Player_New.prefab`, `Player 1.prefab`
- RPM animations in `/Assets/Pavilion/AI_Agent/RPMVers/animations/`

**Implementation Details:**
- **RPM SDK**: Installed via Packages manifest (com.readyplayerme.core from GitHub)
- **Avatar Integration**: AI_Agent with full rigging and textures
- **Lip Sync**: Wolf3D blend shapes for mouth movements (visemes)
- **Voice System**: Push-to-talk → Whisper transcription → OpenAI Assistant → TTS playback
- **Animation Support**: Idle and talking animation variations from RPM
- **Player Controller**: Maintained SimpleKCC third-person controller integration

**Current Capabilities:**
- RPM avatar loads and displays correctly
- Facial animations work via lip sync system
- Voice AI fully functional with avatar integration
- Animation state machine (idle/talking) working

**Next Steps (Stage 2):**
- Implement simple UI for male/female avatar selection
- Create default male and female RPM avatars
- Avatar selection at spawn/character creation
- Later: Full RPM Creator integration with Supabase user profiles

**Technical Notes:**
- Project structure migrated from `/Assets/Lunara/` to `/Assets/Pavilion/`
- RPM avatars compatible with existing network architecture
- Wolf3D (Ready Player Me's former name) blend shapes supported
- Voice controller includes input locking for UI interactions

---

## 2025-12-04 - RPM Integration Plan Major Revision

**Discovered:**
- Official Photon Fusion 2 Industries Addon with Ready Player Me integration
- Production-ready RPMAvatarLoader component (no custom build required)
- UserInfo component for automatic avatar URL synchronization
- Built-in caching, error handling, and optional features

**Updated:**
- RPM Integration Plan completely revised (Version 2.0)
- Timeline reduced from 4-5 days to 1.5-2 days (~2.5 days saved)
- Risk level reduced from High to Low (official addon vs custom code)
- Implementation phases simplified (7 phases, but much shorter)
- Dependencies updated (Industries Addon v2.0.6+ required)

**Files:**
- `/Assets/Docs/RPM_Integration_Plan.md` (revised, 831 lines)

**Reason:**
- Discovered official Photon solution eliminates need for custom networking code
- Official addon is production-tested, maintained, and supported
- Significantly faster implementation with lower risk
- Better long-term support and update compatibility

**Impact:**
- 60% time savings (2 days vs 5 days)
- Official support from Photon team
- Pre-built components reduce development burden
- More time available for voice chat integration
- Lower technical debt

**Key Changes:**
- Section 1: Updated architecture to use addon components
- Section 2: New section documenting addon features
- Section 3: Revised component structure (RPMAvatarLoader from addon)
- Section 4: Completely new implementation phases (addon-based)
- Section 7: Updated dependencies (Industries Addon + RPM Core 3.3)
- Section 12: Timeline reduced from 4-5 days to 1.5-2 days
- Section 15: New section on advantages of official addon
- Section 17: Revised next steps with hourly breakdown

---

## 2025-12-03 - InputManager System for UI Input Locking

**Added:**
- Centralized InputManager system with singleton pattern
- Stack-based input locking mechanism (supports multiple UI systems)
- Debug logging and inspector visualization
- Emergency unlock methods and debug utilities
- Comprehensive rollback documentation

**Changed:**
- PlayerInput.cs now checks InputManager.IsInputLocked before processing movement
- ChatUI.cs tracks input field focus and locks/unlocks player movement
- Movement (WASD, Jump, Sprint) disabled while typing in chat
- Camera rotation and zoom intentionally NOT locked (still functional while typing)

**Files:**
- `/Assets/MetaDyn/Core/Runtime/InputManager.cs` (created, 212 lines)
- `/Assets/MetaDyn/PlayerInput.cs` (modified, added InputManager check)
- `/Assets/MetaDyn/Chat/ChatUI.cs` (modified, focus tracking and locking)
- `/Assets/Docs/InputManager_Rollback.md` (created, rollback guide)

**Reason:**
- Prevent player movement while typing in chat (UX issue)
- Create reusable system for future UI elements (pause menu, settings, inventory)
- Maintain separation of concerns (no coupling between PlayerInput and ChatUI)
- Enable selective input locking (movement vs camera controls)

**Impact:**
- Improved user experience when interacting with chat
- Scalable architecture ready for additional UI systems
- Stack-based locking prevents conflicts between multiple UI elements
- Inspector visualization aids debugging
- Full rollback capability if issues arise

**Testing:**
- ✅ Normal movement works (chat closed)
- ✅ Movement locks when typing in chat
- ✅ Camera controls still work while typing (intentional)
- ✅ Focus transitions properly lock/unlock input
- ✅ OnDestroy cleanup prevents stuck locks

---

## 2025-12-03 - Comprehensive Platform Evaluation

**Added:**
- Comprehensive metaverse platform evaluation (1,200+ lines)
- Full codebase exploration and analysis
- Feature maturity breakdown (90-100%, 50-89%, 0-49%)
- Innovation highlights and unique aspects
- Recommended roadmap (Phase 1-3)
- Technical debt assessment
- Critical issues and risk analysis

**Updated:**
- Project stats: Unity 6000.0.62f1, 107 C# files (up from 77)
- AI Avatar size: 183MB (previously 158MB)
- Claude context system documents with latest findings
- QUICK_REFERENCE.md with accurate statistics

**Evaluated:**
- Core Systems: Networking (90%), User Management (85%), Voice (60%), Chat (80%), Deployment (85%)
- Code Quality: Architecture (A), Documentation (A+), Performance (B+), Security (B), Test Coverage (C)
- Overall Grade: A- (92/100), Production Alpha (65-70% complete)
- Timeline Estimates: Beta in 3-4 weeks, MVP in 8-10 weeks

**Files:**
- `/.claude/QUICK_REFERENCE.md` (updated)
- `/.claude/CHANGELOG.md` (this file)
- Evaluation document (conversation-based)

**Reason:**
- Establish baseline assessment after 2 weeks of development
- Document current maturity level and completion percentages
- Identify critical gaps: automated tests, voice streaming, authentication
- Create actionable roadmap for Production Beta and MVP
- Update context system with accurate project statistics

**Impact:**
- Clear visibility into project status and health
- Prioritized roadmap for next development phases
- Identified 5 high-priority issues and 5 medium-priority issues
- Confirmed strong architectural foundation (A- grade)
- Validated WebGL-first strategy and MetaDyn SDK approach

---

## 2025-11-29 - User List Synchronization System

**Added:**
- Render-based change detection system in UserListManager
- Frame-by-frame NetworkDictionary monitoring
- Event system (OnUserJoined, OnUserLeft, OnUserDataChanged)
- Object pooling for UserListUI entries

**Changed:**
- Player.cs registration flow to use RPC pattern
- User list now updates via change detection instead of IPlayerJoined/IPlayerLeft callbacks

**Files:**
- `/Assets/MetaDyn/UserList/UserListManager.cs` (modified 12:03)
- `/Assets/MetaDyn/Player.cs` (modified 14:04)
- `/Assets/MetaDyn/UserList/UserListUI.cs` (modified 12:01)

**Reason:**
- Eliminates race conditions between player spawn and user list registration
- More reliable synchronization regardless of callback timing
- Frame-accurate detection of changes
- Handles late-joiners seamlessly

**Impact:**
- Improved reliability of user list synchronization
- Cleaner code (no callback interface dependencies)
- Better debugging capability

---

## 2025-11-29 - Project Evaluation Documentation

**Added:**
- Comprehensive project evaluation document
- `/Assets/Docs/Project_Evaluation.md` (1,200+ lines)
- Claude context system in `.claude/` folder

**Files:**
- `/Assets/Docs/Project_Evaluation.md`
- `/.claude/README.md`
- `/.claude/CHANGELOG.md`
- `/.claude/DECISIONS.md`
- `/.claude/QUICK_REFERENCE.md`

**Reason:**
- Document current state of project
- Establish context system for future Claude conversations
- Create reference for architectural decisions

---

## Previous Work (Nov 15-29, 2025)

**Note:** This section documents work completed with Claude web over 2 weeks prior to this evaluation.

### MetaDyn SDK - Deployment System
**Added:**
- One-click deployment to web servers via SSH/SCP
- Server profile management (ScriptableObject)
- Unity Editor integration (MetaDynProjectConfig window)
- Runtime world configuration system
- Build automation with version tracking

**Files:**
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDeploymentManager.cs`
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynProjectConfig.cs`
- `/Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynServerProfile.cs`
- `/Assets/MetaDyn/Core/Runtime/MetaDynRuntimeConfig.cs`

### User Management System
**Added:**
- Permission-based user system (User/Moderator/Admin)
- NetworkDictionary for user tracking
- Block/Kick/Ban functionality
- First-player auto-admin feature
- Push-to-talk default (IsMuted = true)

**Files:**
- `/Assets/MetaDyn/UserList/UserListManager.cs`
- `/Assets/MetaDyn/UserList/UserData.cs`
- `/Assets/MetaDyn/UserList/UserListUI.cs`
- `/Assets/MetaDyn/UserList/UserListEntry.cs`

### WebGL Voice Recording
**Added:**
- Push-to-talk microphone recording
- WebGL JavaScript plugin for browser mic access
- Performance-optimized audio settings
- WAV encoding for API integration
- Visual feedback system

**Files:**
- `/Assets/MetaDyn/Audio/MicrophoneRecorder.cs`
- `/Assets/MetaDyn/Audio/AudioUtils.cs`
- `/Assets/MetaDyn/Audio/MicrophonePlugin.jslib`

### Player & Core Systems
**Added:**
- Third-person player controller with SimpleKCC
- Billboard NameTag system
- Camera zoom and rotation controls
- Performance stats display (FPS, ping, memory)
- GameManager with spawn point system

**Files:**
- `/Assets/MetaDyn/Player.cs`
- `/Assets/MetaDyn/GameManager.cs`
- `/Assets/MetaDyn/PlayerInput.cs`
- `/Assets/MetaDyn/Core/Runtime/NameTag.cs`
- `/Assets/MetaDyn/Core/Runtime/StatsDisplay.cs`

---

## Template for Future Entries

```markdown
## YYYY-MM-DD - Feature Name

**Added:**
- New feature or file

**Changed:**
- Modified behavior or refactored code

**Fixed:**
- Bug fix or correction

**Removed:**
- Deprecated or deleted code

**Files:**
- `/path/to/file1.cs`
- `/path/to/file2.cs`

**Reason:**
- Why this change was made

**Impact:**
- How this affects the project
```
