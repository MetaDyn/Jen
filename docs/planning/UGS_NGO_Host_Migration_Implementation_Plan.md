# UGS/NGO Host Migration Implementation Plan

**Created:** 2026-08-06  
**Status:** Read-only audit complete; implementation proposed, not started  
**Target:** Unity 6000.0.67f1, UGS Multiplayer 2.2.3, NGO 2.7.0, Relay, WebGL primary  
**Primary goal:** Preserve the current working multiplayer path while adding recoverable host transfer that approaches the continuity users experienced in Photon builds.

---

## 1. Executive Summary

The current MetaDyn UGS session is a Relay-backed NGO client/server session. The first player who creates the session becomes both UGS session host and NGO server. When that player leaves, the remaining clients lose the NGO server and can appear frozen because host migration is not enabled and MetaDyn has no migration lifecycle.

UGS Multiplayer 2.2.3 already provides the transport/session portion of host migration when `WithHostMigration(IMigrationDataHandler)` is configured on every participant:

1. UGS Lobby elects a remaining session member as host.
2. The selected client becomes the new UGS host.
3. The package stops the old NGO/Relay network locally.
4. The new host receives the last uploaded migration payload.
5. The new host creates a replacement Relay allocation and starts NGO as host.
6. UGS updates the session network metadata.
7. Remaining clients join the replacement Relay allocation and restart NGO as clients.
8. `ISession.SessionMigrated` is raised after the local network restart completes.

UGS does **not** provide a default NGO world snapshot. The package's parameterless/default migration handler is compiled for Netcode for Entities, not this NGO project. MetaDyn must supply a small NGO-compatible `IMigrationDataHandler` and restore player/SDK state after NGO has restarted.

The safest implementation is additive: retain `MetaDynUGSSessionService`, its public join/leave API, deterministic Space ID lookup, Relay/WSS configuration, manual avatar spawning, existing player prefabs, Supabase avatar restore, and Vivox channel. Add a migration coordinator and versioned snapshot around those systems rather than replacing them.

---

## 2. Read-Only Audit Findings

### 2.1 Current session lifecycle

`MetaDynUGSSessionService` currently:

- initializes Unity Services and signs into UGS Authentication;
- queries by deterministic session name and `space_id`;
- joins an existing UGS Session or creates one with `WithRelayNetwork()`;
- lets the UGS Multiplayer package start NGO automatically;
- enables NGO connection approval and manually spawns the chosen player prefab;
- joins a deterministic Vivox channel after connection;
- leaves the UGS Session and shuts NGO down when the user explicitly disconnects.

Host migration is currently disabled because neither `SessionOptions` nor `JoinSessionOptions` calls `WithHostMigration(...)`.

### 2.2 Installed package capability

Local package source confirms:

- `com.unity.services.multiplayer` is version `2.2.3`;
- `WithHostMigration(IMigrationDataHandler)` is available for both create and join option types through `BaseSessionOptions`;
- the default upload interval is five seconds and the default data handling timeout is three seconds;
- the minimum supported upload interval is one second;
- migration payload size is bounded by a server-provided limit and must remain compact;
- the host periodically calls `IMigrationDataHandler.Generate()` and uploads the resulting bytes;
- a newly elected host calls `IMigrationDataHandler.Apply(byte[])` after the old network is stopped and before the replacement network is started;
- Relay migration creates a replacement allocation and may preserve the previous Relay region;
- clients detect new network metadata and reconnect automatically;
- `ISession.SessionHostChanged`, `ISession.SessionMigrated`, `ISession.Network.StateChanged`, and `ISession.Network.MigrationFailed` are available.

### 2.3 MetaDyn integration gaps

The following gaps must be addressed before merely enabling the UGS option:

1. **Only the original creator is configured as a manual-spawn server.** `ConfigureManualPlayerSpawning()` is called only on the create-host branch. A client elected as replacement host may have connection approval enabled without the callback needed to approve and manually spawn reconnecting players.
2. **NGO client IDs are temporary.** They will be reassigned after NGO restarts and cannot identify players across migration.
3. **The connection payload contains only an avatar index.** It does not carry a version or stable UGS/Supabase identity for reconnect reconciliation.
4. **Avatar choices are cached by old NGO client ID.** `_clientAvatarChoices` cannot safely survive a restart.
5. **Player state lives in destroyed NetworkObjects.** Display name, custom avatar model ID, transform, and Animator state are recreated when player objects respawn.
6. **Remote Supabase identity is not actually transmitted.** `MetaDynUGSPlayerController.GetSupabaseUserId()` reads the local process's Supabase session, so it cannot reliably identify a remote player. Host migration must not use this method as the cross-client identity source.
7. **Permissions can change accidentally.** `firstPlayerIsAdmin` depends on registration order. After restart, an empty user list could grant admin to whichever player registers first instead of preserving the pre-migration permission.
8. **World state is server-owned.** `MetaDynDoor` and `MetaDynLightSwitch` use server-write `NetworkVariable<bool>` values that return to scene defaults when NGO restarts unless captured.
9. **RPC history is transient.** `MetaDynNetworkEventRelay` events are not durable state and cannot be replayed automatically.
10. **The UI has only joined/left behavior.** It has no migrating, restoring, timed-out, or recoverable-failure state.
11. **Vivox is independent of the Relay allocation.** The deterministic voice channel should remain joined during migration; logging out/rejoining unnecessarily would increase disruption. Its positional reference must rebind to the replacement local player.
12. **Existing callbacks need restart-safe behavior.** Player spawn, local-player-ready, user-list, camera, custom-avatar restore, and voice-position code must tolerate a second NGO lifecycle without duplicating subscriptions or retaining old client IDs.

---

## 3. Preservation and Compatibility Rules

These rules keep the implementation as additive as possible:

1. Do not replace `MetaDynUGSSessionService` or change its existing `JoinConfiguredWorldAsync(...)` and `LeaveSessionAsync()` public contracts during the first implementation.
2. Keep the deterministic Space ID query/create behavior and existing race-condition retry.
3. Keep UGS-managed Relay/NGO startup. Do not introduce parallel manual Relay allocation code.
4. Keep WebGL Relay protocol as WSS and native protocol as UDP.
5. Keep manual player spawning and the existing avatar registry/default-prefab fallback.
6. Keep owner-authoritative movement, `NetworkTransform`, and `OwnerNetworkAnimator` behavior.
7. Keep Supabase Storage as the source of GLB bytes; migrate only `active_avatar_model_id`, never model bytes.
8. Keep the existing Vivox channel during successful migration.
9. Do not modify package-cache source. Integrate only through public UGS APIs.
10. Put migration behind a serialized/runtime feature flag until the complete three-client matrix passes. With the flag disabled, behavior must remain identical to the current join/create flow.
11. Use versioned payloads and ignore unknown optional fields so future SDK state providers remain backward-compatible.
12. Treat explicit user disconnect separately from involuntary host migration; explicit leave must retain the current clean menu/scene reload behavior.

---

## 4. Target Lifecycle

```text
Connected
   |
   | UGS SessionHostChanged / network state Migrating
   v
MigrationDetected
   |- freeze local gameplay input
   |- keep menu scene and persistent services alive
   |- keep Vivox channel joined
   v
UGS package stops NGO and old Relay
   |
   +-- elected client: Apply snapshot -> create Relay -> StartHost
   |
   +-- other clients: wait for new metadata -> join Relay -> StartClient
   v
NGO Connected
   |- replacement host re-enables approval/manual spawning
   |- all players reconnect with versioned stable identity payload
   |- host spawns player objects
   v
RestorePending
   |- match new NGO client IDs to stable UGS player IDs
   |- restore player and durable SDK state
   |- rebind local camera, avatar, user list, and voice position
   v
SessionMigrated
   |- verify local player exists
   |- unfreeze input
   |- clear migration UI
   v
Connected

Any bounded-time failure
   -> shutdown stale NGO state
   -> retain enough context for one controlled session reconnect
   -> otherwise return to menu with a clear error and retry action
```

Recommended service states:

```text
Idle
Joining
Connected
MigrationDetected
RestartingNetwork
RestoringState
MigrationFailed
Leaving
```

Only one join, leave, reconnect, or migration transition may run at a time.

---

## 5. Stable Identity Contract

### 5.1 Canonical migration key

Use the UGS Authentication Player ID as the canonical in-session migration key because UGS Sessions already use it for membership and host election. NGO client IDs are transport-instance identifiers only.

Keep the Supabase user ID as application identity for profiles, ownership, permissions, and avatar Storage. Associate it with the UGS player for the current session through a validated connection/session-player record.

### 5.2 Versioned connection payload

Replace the raw four-byte avatar index with a compact, versioned DTO while retaining legacy parsing for four-byte payloads during rollout.

Required fields:

- schema version;
- UGS Player ID;
- selected prefab/avatar index;
- optional Supabase user ID;
- optional active avatar model ID.

Validation rules:

- reject malformed or oversized payloads;
- confirm the supplied UGS Player ID is a current `ISession.Players` member before using it as a restore key;
- clamp avatar index through `MetaDynUGSAvatarRegistry`;
- never trust client-supplied permission level;
- restore permission from the migration snapshot or authoritative `ownerId` comparison;
- keep legacy four-byte payload support until all deployed builds use the versioned schema.

The server maintains both mappings for the current NGO generation:

```text
UGS Player ID -> NGO client ID
NGO client ID -> UGS Player ID
```

Both maps are cleared and rebuilt on every NGO restart.

---

## 6. Migration Snapshot Contract

### 6.1 Format

Use a versioned, compact DTO serialized to UTF-8 JSON initially for auditability and WebGL debugging. Include a schema version, session/space ID, capture timestamp, and monotonically increasing snapshot sequence. If payload size becomes material at the 50-user target, retain the DTO and replace only the serializer with a compact binary format.

`IMigrationDataHandler.Generate()` must be synchronous, fast, and side-effect free. It should copy from an in-memory state registry rather than search the whole scene or perform network/storage operations every five seconds.

`Apply(byte[])` runs before the new NGO host starts. It must validate/deserialise and store a pending snapshot in a persistent coordinator. It must not attempt to spawn NGO objects at that point.

### 6.2 Required player state

Key each player record by UGS Player ID and include:

- Supabase user ID when authenticated;
- display name;
- prefab/avatar registry index;
- active avatar model ID;
- position and rotation;
- permission level;
- local mute preference only if it is currently intended to persist inside a session;
- snapshot timestamp/sequence.

Do not snapshot:

- raw GLB bytes or signed Storage URLs;
- NGO client ID or NetworkObject ID as durable identity;
- current Relay join code/allocation data;
- camera references;
- transient animation triggers, footstep events, or active RPC calls.

After respawn, movement and owner-authoritative Animator state resume from the owner. A currently playing emote may reset to idle for the first production increment unless emote persistence is separately approved.

### 6.3 Durable SDK world state

Introduce an opt-in state-provider contract instead of hard-coding every component into the session service:

```text
IMetaDynMigrationStateProvider
  StableStateId
  CaptureState()
  RestoreState(payload)
```

Initial providers:

- `MetaDynDoor`: open/closed;
- `MetaDynLightSwitch`: on/off.

Each provider needs a stable scene-authored ID validated for uniqueness. Missing or unknown provider IDs are logged and skipped without failing the entire migration.

Transient `MetaDynNetworkEventRelay` messages do not replay. If a future event changes durable world state, the receiving system must expose that state through a provider.

### 6.4 Restore ordering

1. `Apply(...)` stores the validated pending snapshot.
2. UGS starts the replacement Relay/NGO network.
3. Replacement host registers connection approval and spawn callbacks before clients complete reconnection.
4. Reconnecting players identify themselves with the versioned payload.
5. Host spawns the existing selected prefab for each new NGO client ID.
6. Player controller restores name, model ID, transform, and permission mapping by UGS Player ID.
7. Each client downloads the GLB from Supabase through the existing loader path.
8. Host restores registered durable scene providers after scene NetworkObjects are spawned.
9. Local camera/input/user-list/Vivox positional bindings are refreshed.
10. Migration completes only after a local player exists and required state restoration has either succeeded or explicitly fallen back.

The snapshot may contain the departed host. Restore only records whose UGS Player IDs remain members/reconnect within the bounded restore window.

---

## 7. Additive Code Structure

### New files

```text
Assets/MetaDyn/Runtime/Networking/HostMigration/MetaDynUGSHostMigrationDataHandler.cs
Assets/MetaDyn/Runtime/Networking/HostMigration/MetaDynUGSMigrationCoordinator.cs
Assets/MetaDyn/Runtime/Networking/HostMigration/MetaDynUGSMigrationSnapshot.cs
Assets/MetaDyn/Runtime/Networking/HostMigration/MetaDynUGSConnectionPayload.cs
Assets/MetaDyn/Runtime/Networking/HostMigration/IMetaDynMigrationStateProvider.cs
```

Responsibilities:

- **Data handler:** bridge UGS `Generate/Apply` calls to the persistent coordinator.
- **Coordinator:** own pending/latest snapshots, stable identity maps, migration generation, restore readiness, timeout, and state-provider registry.
- **Snapshot DTO:** versioned player and world-state records with strict validation.
- **Connection payload:** backward-compatible serialization/parsing and size validation.
- **State-provider interface:** allow SDK components to opt into durable restoration without coupling them to UGS package types.

### Existing files to modify during implementation

```text
Assets/MetaDyn/Runtime/Networking/MetaDynUGSSessionService.cs
Assets/MetaDyn/Runtime/Networking/MetaDynUGSPlayerController.cs
Assets/MetaDyn/Runtime/UserList/MetaDynUGSUserListManager.cs
Assets/MetaDyn/Runtime/Core/Starter/UIGameMenu.cs
Assets/MetaDyn/Runtime/Core/Components/MetaDynDoor.cs
Assets/MetaDyn/Runtime/Core/Components/MetaDynLightSwitch.cs
```

Optional follow-up integration may be needed in the component that updates Vivox positional audio if it retains the old local player reference.

No existing player prefab or `OwnerNetworkAnimator` authority mode should change for host migration.

---

## 8. Implementation Phases and Gates

### Phase 0 — Instrumentation and feature flag

- Add migration state/events and structured `[UGS MIGRATION]` logging.
- Add a disabled-by-default `enableHostMigration` setting without changing current behavior.
- Centralize bind/unbind for all `ISession` and `ISession.Network` events.
- Distinguish explicit leave from unexpected network loss/migration.

**Gate:** With the flag disabled, the current create, join, avatar spawn, Vivox join, and disconnect flows behave identically.

### Phase 1 — Restart-safe session lifecycle

- Configure manual player spawning and connection approval on every participant before join/create, not only the original creator.
- Add the custom handler via `WithHostMigration(...)` to both create and join options when the flag is enabled.
- Preserve Relay protocol behavior and consider `preserveRegion` only after latency testing.
- Handle `SessionHostChanged`, network `StateChanged`, `SessionMigrated`, and `MigrationFailed`.
- Freeze local gameplay input during migration and apply a bounded timeout.
- Re-register/verify NGO callbacks after restart without duplicate subscriptions.

**Gate:** Three clients can migrate to a replacement Relay/NGO host and all obtain new NGO connections, even if player state initially resets.

### Phase 2 — Stable player identity and respawn

- Introduce the versioned connection payload with legacy parsing.
- Rebuild UGS-player/NGO-client maps each network generation.
- Stop using old NGO IDs as migration keys.
- Ensure every reconnected session member receives exactly one player object.
- Fix remote identity propagation so the user list never reads another process's Supabase identity.

**Gate:** The same logical users reappear once, with the correct display names and selected prefab shells, regardless of reconnect order.

### Phase 3 — Player state restoration

- Capture/restore transform, custom avatar model ID, and permission level.
- Reuse the current Storage download/GLB loader and owner-authoritative Animator flow.
- Rebind local camera and input after the replacement player object spawns.
- Preserve first-person visibility and reset transient seat/emote state safely.
- Rebuild the user list from stable identity; never grant admin based solely on post-migration registration order.

**Gate:** All remaining users continue with correct positions, names, permissions, preset/uploaded avatars, movement, and network animation.

### Phase 4 — Durable SDK world state

- Add the opt-in provider registry.
- Migrate door and light state first.
- Define default/reset behavior for components without providers.
- Log skipped incompatible provider payloads without failing migration.

**Gate:** Door/light state survives graceful and abrupt host replacement; transient events reset by documented design.

### Phase 5 — UX, voice, and recovery

- Add non-blocking "Connection interrupted — restoring session..." UI.
- Keep Vivox logged in and in the existing deterministic channel.
- Rebind positional voice to the new local player.
- On timeout/failure, shut down stale NGO state and attempt one controlled `ISession.ReconnectAsync()`/session rejoin path.
- If recovery still fails, show a clear message and return to the existing menu/rejoin flow.

**Gate:** No participant remains indefinitely frozen or receives an unusable hidden UI state.

### Phase 6 — Production validation and rollout

- Keep the feature flag disabled by default until all required tests pass.
- Enable first in a development UGS environment/space.
- Add telemetry for migration start, elected-host status, duration, restore counts, failure reason, and fallback result.
- Enable production only after WebGL/Relay repetition and mixed-platform validation.

---

## 9. Timeout and Failure Policy

Recommended starting budgets, subject to measured WebGL behavior:

- UGS migration data upload interval: five seconds (package default).
- Migration data handling timeout: three seconds (package default initially).
- Overall replacement-network and local-player restore timeout: 20 seconds.
- One controlled recovery/rejoin attempt after migration failure.

Rules:

- A stale snapshot is preferable to a frozen session, but show/log its age.
- Snapshot parse/version failure must fall back to reconnecting with default scene/player state rather than preventing the replacement network from starting.
- Migration failure must never call normal explicit-leave UI callbacks as though the user chose to disconnect.
- Explicit Back to Menu must cancel migration/recovery work and use the current leave flow.
- Do not recursively retry without a hard attempt limit.

---

## 10. Test Matrix

All multiplayer tests require at least three participants so a host can leave while two users remain.

### Required scenarios

1. Graceful original-host Back to Menu.
2. Original-host browser tab close.
3. Original-host browser process/network loss.
4. Elected replacement host is using an uploaded stored GLB.
5. Non-host client is using an uploaded stored GLB.
6. All remaining users move/jump during and immediately after recovery.
7. Host leaves while a door is open and a light is off.
8. Host leaves while a client is seated or emoting; transient state resets safely.
9. Late join after one completed migration.
10. Second host migration in the same session.
11. Migration payload absent, stale, corrupt, or unsupported version.
12. Replacement host fails Relay allocation or NGO startup.
13. One client fails to reconnect while the others succeed.
14. User clicks Back to Menu while migration is in progress.
15. Migration with guest/no-Supabase user and authenticated users together.

### Platforms

- Editor/native host plus native clients for rapid diagnostics.
- WebGL host plus two WebGL clients over Relay/WSS.
- Mixed WebGL/native participants.
- Browser background-tab throttling and temporary network interruption.

### Acceptance criteria

- UGS session ID/space membership remains usable after host loss.
- Exactly one replacement host starts.
- Remaining clients reconnect to the new Relay allocation without manual room selection.
- Each remaining user gets exactly one player object and a new valid NGO client ID.
- Stable identity, display name, prefab choice, uploaded avatar model, transform, permissions, and required world state restore.
- Owner-authoritative movement and animation remain correct after restart.
- Vivox remains usable and positional audio follows the replacement local player.
- Late join works after migration.
- Repeated migration works.
- Any unrecoverable failure exits to a clear, actionable rejoin state; no indefinite freeze.
- With migration disabled, existing multiplayer behavior is unchanged.

---

## 11. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Enabling migration before every client has a handler | Add the handler to both create and join options behind a build/runtime compatibility flag. |
| New host lacks approval/spawn callback | Configure restart-safe server callbacks on every participant before the initial join. |
| Old client IDs restore the wrong player | Key snapshots by UGS Player ID and rebuild mappings each NGO generation. |
| Wrong Supabase identity/permissions | Transmit/validate identity explicitly and restore permission from authoritative state, not registration order. |
| `Apply()` runs before NGO objects exist | Store a pending snapshot and consume it only after replacement NGO objects spawn. |
| Payload exceeds UGS limit | Snapshot only durable IDs/state; no asset bytes; measure serialized size and skip optional providers if required. |
| Snapshot up to five seconds old | Record sequence/time; accept bounded positional rollback for MVP; tune interval only after bandwidth/rate testing. |
| Duplicate callbacks after NGO restart | Centralize idempotent bind/unbind and track network generation. |
| Voice disruption | Keep Vivox channel joined; only rebind positional player reference. |
| Feature destabilizes current sessions | Disabled-by-default flag, phased gates, and unchanged legacy flow when off. |

---

## 12. Recommended First Implementation Increment

Implement Phases 0 and 1 only after plan review:

1. migration feature flag;
2. restart-safe session/network event binding;
3. manual-spawn configuration on every participant;
4. no-op/versioned `IMigrationDataHandler` scaffold that safely stores an empty snapshot;
5. `WithHostMigration(...)` on both create and join options when enabled;
6. migration state, logs, timeout, and clean failure path;
7. three-client proof that UGS reallocates Relay and restarts NGO.

This increment deliberately proves the UGS lifecycle before adding identity or world-state restoration. It is small, reversible, and leaves the existing feature-disabled path untouched.

Do not call this production-ready until Phases 2 through 6 and the full acceptance matrix are complete.

---

## 13. Audit Sources

Project runtime:

```text
Assets/MetaDyn/Runtime/Networking/MetaDynUGSSessionService.cs
Assets/MetaDyn/Runtime/Networking/MetaDynUGSPlayerController.cs
Assets/MetaDyn/Runtime/UserList/MetaDynUGSUserListManager.cs
Assets/MetaDyn/Runtime/Networking/MetaDynVivoxService.cs
Assets/MetaDyn/Runtime/Core/Starter/UIGameMenu.cs
Assets/MetaDyn/Runtime/Core/Components/MetaDynDoor.cs
Assets/MetaDyn/Runtime/Core/Components/MetaDynLightSwitch.cs
Assets/MetaDyn/Runtime/Networking/MetaDynNetworkEventRelay.cs
```

Installed package source:

```text
Packages/manifest.json
Packages/packages-lock.json
Library/PackageCache/com.unity.services.multiplayer@1c7846287c66/Runtime/Multiplayer/Session/Migration/HostMigrationOption.cs
Library/PackageCache/com.unity.services.multiplayer@1c7846287c66/Runtime/Multiplayer/Session/Migration/HostMigrationHandler.cs
Library/PackageCache/com.unity.services.multiplayer@1c7846287c66/Runtime/Multiplayer/Session/Models/Migration/IMigrationDataHandler.cs
Library/PackageCache/com.unity.services.multiplayer@1c7846287c66/Runtime/Multiplayer/Modules/Network/NetworkModule.cs
Library/PackageCache/com.unity.services.multiplayer@1c7846287c66/Runtime/Multiplayer/Modules/Network/Handlers/NetworkHandler/GameObjectsNetcodeNetworkHandler.cs
```

No runtime code, package source, prefab, scene, compile, or build was changed during this audit.
