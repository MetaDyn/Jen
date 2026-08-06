# Planning: Runtime Avatar Upload & Auto-Rigging
**Status:** MVP Storage Plan Updated (v1.1)  
**Orchestrator:** Jen (MetaDyn AI)  
**Primary Target:** WebGL (Production-Ready)

## 1. Vision: "The Dynamic Embodiment"
To fulfill the Ironman Jarvis vision, users must not be limited to pre-baked SDK prefabs. This system enables a "Zero-Install" workflow where a user can bring their own identity into a live session, with the MetaDyn SDK handling the complex task of storage, rigging, networking, and synchronization on the fly.

**MVP Scope:** Start with one active uploaded **GLB** avatar per authenticated user, persisted through Supabase Storage and profile metadata. Design the storage and runtime APIs so **VRM** can be added through the same pipeline later without changing the user-facing persistence model.

## 2. Core Technical Challenges
*   **WebGL File Access:** Standard C# file I/O is restricted. Requires a JavaScript Bridge.
*   **Runtime Humanoid Rigging:** Unity's Humanoid Avatar system is typically Editor-only. We must implement a runtime "Bone Mapping Heuristic" to bind external meshes to our `MetaDynUGSPlayerController`.
*   **Network Persistence:** Custom models are not part of the build. All clients must download and rig the model independently based on a stable networked model identifier or storage object path.
*   **Large User Assets:** MVP allows avatar uploads up to **100 MB**. Dynamic LOD, mesh optimization, texture compression, and avatar validation can be layered on after the persistence path is proven.
*   **Future Format Expansion:** GLB is the first supported runtime format. VRM should use the same bucket, metadata table, and active-avatar profile pointer when added.

## 3. Implementation Phases

### Phase 1: The Upload & Storage Bridge
*   **Objective:** Get a 3D avatar file from the user's hard drive into authenticated Supabase Storage and persist the selected model for future sessions.
*   **Workflow:**
    1.  **JS Bridge:** Use the existing WebGL file picker bridge to trigger the browser's file explorer and return selected bytes to Unity.
    2.  **Runtime Storage Service:** Create `MetaDynAvatarStorageService` under `Assets/MetaDyn/Runtime/Avatar/` to validate, upload, register, and select avatar models.
    3.  **Supabase Storage:** Create an `avatar-models` bucket in Supabase.
    4.  **Object Path Convention:** Store files at `users/{user_id}/{avatar_model_id}/avatar.{ext}`.
    5.  **Upload Logic:** Upload with the authenticated Supabase JWT using `Content-Type: model/gltf-binary` for GLB and `x-upsert: true` for replacing the user's active model.
    6.  **Metadata:** Store file metadata in an `avatar_models` table. Store only the active model reference in `profiles`, not raw bytes and not an expiring signed URL.
    7.  **MVP Selection:** Support one active uploaded avatar per user. Multiple saved avatar slots are a later feature, but the table shape should support them.

### Phase 1A: Supabase Schema & Policies
*   **Storage Bucket:** `avatar-models`
*   **MVP File Limit:** 100 MB
*   **Initial Formats:** `.glb` only
*   **Planned Formats:** `.vrm` through the same bucket/table/profile pointer
*   **Recommended Table:**

```sql
create table public.avatar_models (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  object_path text not null,
  display_name text,
  format text not null default 'glb',
  mime_type text not null default 'model/gltf-binary',
  file_size_bytes bigint,
  status text not null default 'active',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.profiles
add column active_avatar_model_id uuid references public.avatar_models(id);
```

*   **Policy Direction:**
    1.  Users can upload/update/delete only under their own `users/{auth.uid()}/...` prefix.
    2.  Authenticated users can read avatar model objects so multiplayer clients can render other players.
    3.  Users can insert/update/delete only their own `avatar_models` rows.
    4.  Authenticated users can read active avatar model metadata needed for in-world rendering.
    5.  Moderation can later set `status = 'blocked'` or hide unsafe/oversized assets without deleting user data.

### Phase 2: Runtime Model Acquisition
*   **Objective:** Download and instantiate the model using `GLTFast`.
*   **Workflow:**
    1.  Fetch the selected `avatar_models` record from Supabase by `active_avatar_model_id` or by a networked model id.
    2.  Download the object bytes from Supabase Storage with `apikey` and `Authorization` headers.
    3.  Load GLB bytes through the existing `GLBAvatarLoader`/glTFast byte-loading path.
    4.  Keep model loading format-aware so VRM can route to a future UniVRM runtime loader while sharing the same storage and persistence service.
    5.  Use the proven GLTFast Resources material conversion pattern documented below. Do **not** fall back to generic URP/Lit conversion as the primary WebGL fix.

### Phase 3: The Auto-Rigging Utility (`MetaDynRuntimeRigBuilder`)
*   **Objective:** Connect the downloaded mesh to the Animator.
*   **Workflow:**
    1.  **Bone Discovery:** Scan the hierarchy for standard bone names (Hips, Spine, Head, etc.).
    2.  **Avatar Creation:** Research runtime Avatar creation (e.g., via VRM loader or manual Bone-to-Bone retargeting).
    3.  **Animator Hot-Swap:** Assign the new Avatar to the existing `Animator` component and call `Rebind()`.
    4.  **Root Alignment:** Adjust the model height and scale to match the `CharacterController` bounds.

### Phase 4: Network Synchronization
*   **Objective:** Ensure all players see the custom model.
*   **Workflow:**
    1.  **NetworkVariable:** Add a networked model id or storage object path to `MetaDynUGSPlayerController`.
    2.  **Do Not Sync Bytes:** Never sync the raw GLB/VRM bytes through NGO RPCs or NetworkVariables.
    3.  **Avoid Expiring URLs:** Prefer syncing `avatar_model_id` or `object_path`, not signed URLs. Each client can resolve/download using its authenticated Supabase session.
    4.  **OnValueChanged:** When the id/path changes, clients download and apply the model locally. Late joiners receive the current id/path through NGO state and run the same load path.
    5.  **Security:** Check format, declared file size, max file size, owner, and `avatar_models.status` before loading. Add moderator override/blocking later.
    6.  **Persistence Restore:** On login/profile fetch, if `profiles.active_avatar_model_id` exists, cache it and apply it after the local player spawns.

### Phase 5: Later Optimization & Avatar Library
*   **Objective:** Improve runtime cost and user choice after the one-active-avatar MVP works.
*   **Deferred Work:**
    1.  Multiple saved avatars per user using the existing `avatar_models` table.
    2.  Dashboard avatar library management: rename, preview, select, delete.
    3.  Runtime or server-side optimization: texture limits, mesh simplification, generated LODs, thumbnail generation, and validation reports.
    4.  VRM support using the same upload/persist/select/download flow with a format-specific runtime loader.

## 4. Format Support Matrix
| Format | Support Level | Rationale |
| :--- | :--- | :--- |
| **GLB** | **MVP Primary** | Web-native, single file, supported by `GLTFast`, already proven in this project. |
| **VRM** | **Planned Secondary** | Standard for humanoid/avatar identity workflows; should share the same bucket/table/profile pointer and use a format-specific loader later. |
| **GLTF** | **Deferred** | Multi-file structure complicates browser upload and Storage persistence. Prefer GLB first. |
| **FBX** | **Not MVP** | Too heavy and unsuitable for WebGL runtime import without proprietary/heavy loaders. |

## 5. Next Steps
1.  [x] **Supabase Bucket Setup:** Create `avatar-models` with a 100 MB upload limit and authenticated read policies.
2.  [x] **Supabase Metadata Setup:** Add `avatar_models` and `profiles.active_avatar_model_id`.
3.  [x] **Runtime Storage Service:** Implement `MetaDynAvatarStorageService` for validate/upload/register/select/download.
4.  [x] **GLB Loader Refactor:** Keep `GLBAvatarLoader` byte loading, but add paths for upload persistence and download-by-object-path.
5.  [x] **Profile Restore:** Extend `SupabaseProfile` and login/menu flow to restore `active_avatar_model_id`.
6.  [x] **Network Sync:** Add model id/path sync to `MetaDynUGSPlayerController` for remote clients and late joiners.
7.  [x] **Network Animator GLB-Swap Fix:** Use `OwnerNetworkAnimator` on every registry/default network shell, prevent custom-avatar restore from falling back to a server-authoritative shell, and preserve synchronized locomotion state across `Animator.Rebind()`. Built and multiplayer-verified with a stored user-bucket GLB on 2026-08-05.
8.  [ ] **Network Animator Regression Coverage:** Complete host-plus-two-client coverage for reload restore, late join, repeated avatar replacement, and the full idle/walk/run/stop/jump/land sequence.
9.  [ ] **Animator Swap Hardening:** Validate a replacement humanoid before removing the visible avatar, discard stale asynchronous load completions, and route any emote/seat controller rebinds through the same state-preserving swap path.
10. [ ] **Bone Mapping Script:** Continue hardening Mixamo/RPM bone mapping and runtime humanoid binding.

## 6. MVP Architecture Details

### 6.1 Unity Runtime Responsibilities

**`MetaDynAvatarStorageService` (new)**

Location:

```text
Assets/MetaDyn/Runtime/Avatar/MetaDynAvatarStorageService.cs
```

Responsibilities:

1. Validate selected avatar file before upload.
2. Create or reuse the user's active `avatar_models` row.
3. Upload bytes to Supabase Storage.
4. Patch `profiles.active_avatar_model_id`.
5. Fetch avatar metadata by id for restore/network loading.
6. Download avatar bytes by `object_path`.
7. Keep format routing centralized so GLB and future VRM use the same persistence contract.

**`GLBAvatarLoader` (modify)**

Current role: byte-based GLB load, runtime humanoid binding, material conversion, and local player application.

Planned role:

1. Keep the proven `LoadAndApply(byte[] bytes)` path.
2. Add an authenticated upload entry path that sends selected GLB bytes to `MetaDynAvatarStorageService`.
3. Add a download/apply path that accepts an `AvatarModelRecord` or `object_path`.
4. Report load/upload errors to the existing menu/status UI.
5. Avoid owning Supabase REST details directly; storage/persistence belongs to `MetaDynAvatarStorageService`.

**`SupabaseAuthManager` / `SupabaseProfile` (modify)**

Planned additions:

```text
SupabaseProfile.active_avatar_model_id
```

Profile fetch should cache the active avatar model id so the menu/player spawn flow can restore the user's uploaded avatar without forcing another picker interaction.

**`UIGameMenu` / login flow (modify)**

Planned behavior:

1. Fetch authenticated profile as today.
2. If `avatar_index >= 0`, preserve existing prefab-avatar behavior.
3. If `active_avatar_model_id` exists, prepare custom avatar restore.
4. On join/spawn, apply the uploaded avatar after `MetaDynUGSPlayerController.OnLocalPlayerReady`.
5. Keep guest/no-auth behavior unchanged.

**`MetaDynUGSPlayerController` (modify)**

Planned additions:

1. Owner-writable networked avatar model id or object path.
2. On local player spawn, publish the active custom avatar reference if available.
3. On remote value change, resolve metadata/download bytes and apply locally.
4. Late joiners rely on current NGO state instead of a one-time RPC.

### 6.2 Runtime API Shape

Use small data records so GLB and VRM share one contract:

```csharp
public enum MetaDynAvatarModelFormat
{
    Glb,
    Vrm
}

public sealed class MetaDynAvatarModelRecord
{
    public string id;
    public string user_id;
    public string object_path;
    public string display_name;
    public string format;
    public string mime_type;
    public long file_size_bytes;
    public string status;
}
```

Recommended service methods:

```csharp
ValidateAvatarFile(byte[] bytes, string filename, out string error)
UploadAndSelectAvatar(byte[] bytes, string filename, Action<MetaDynAvatarModelRecord> onSuccess, Action<string> onError)
FetchAvatarModel(string avatarModelId, Action<MetaDynAvatarModelRecord> onSuccess, Action<string> onError)
DownloadAvatarBytes(MetaDynAvatarModelRecord model, Action<byte[]> onSuccess, Action<string> onError)
```

The loader should branch by `model.format`:

```text
glb -> GLBAvatarLoader / glTFast
vrm -> future VRM runtime loader
```

### 6.3 Supabase REST Flow

**Upload/select flow:**

1. User selects `.glb`.
2. Unity validates:
   - authenticated user exists
   - extension is `.glb`
   - bytes are non-empty
   - bytes are <= 100 MB
3. Unity creates an `avatar_models` row or reuses the current one for the one-active-avatar MVP.
4. Unity uploads bytes to:

```text
/storage/v1/object/avatar-models/users/{user_id}/{avatar_model_id}/avatar.glb
```

5. Unity patches the `avatar_models.object_path`, `format`, `mime_type`, and `file_size_bytes`.
6. Unity patches:

```text
profiles.active_avatar_model_id = avatar_model_id
```

7. Unity applies the bytes locally immediately.
8. Local player publishes the model id/path over NGO so other clients load it.

**Restore flow:**

1. Auth/profile fetch returns `active_avatar_model_id`.
2. Unity stores it in memory until the local player exists.
3. On local player ready, Unity fetches the `avatar_models` row.
4. Unity downloads bytes from Storage.
5. Unity applies the model locally.
6. Local player publishes the active model id/path to NGO.

**Remote player flow:**

1. Remote `MetaDynUGSPlayerController` receives model id/path through networked state.
2. Client fetches metadata if needed.
3. Client checks `status`, format, and file size.
4. Client downloads bytes from Storage with authenticated headers.
5. Client applies the model to the remote player's avatar root.

### 6.4 Validation Rules

MVP upload checks:

| Rule | MVP Behavior |
| :--- | :--- |
| Authentication | Upload requires authenticated Supabase session. |
| Format | `.glb` only. `.vrm` rejected with a future-support message. |
| Size | Reject above 100 MB. |
| Empty file | Reject zero-byte files. |
| Storage path | Must start with `users/{current_user_id}/`. |
| Metadata owner | `avatar_models.user_id` must equal current auth user. |
| Status | Only `active` models load automatically. |

Runtime safety checks before applying:

1. Refuse unknown format values.
2. Refuse `status = 'blocked'`.
3. Refuse files above the configured client max even if metadata says they exist.
4. Show a fallback prefab avatar if download, import, rigging, or material setup fails.
5. Log enough detail to distinguish auth failure, Storage policy failure, invalid GLB, rigging failure, and shader/material failure.

### 6.5 MVP UX Behavior

Initial UI can remain minimal:

1. Add or reuse an "Upload GLB" action in the avatar selection/menu flow.
2. Show upload progress if available from `UnityWebRequest.uploadProgress`.
3. Show clear states:
   - Selecting file
   - Uploading avatar
   - Saving avatar
   - Loading avatar
   - Avatar ready
   - Upload failed / load failed
4. After upload succeeds, the user should not need to select the file again on the next session.
5. If the uploaded avatar fails to load, fall back to the existing avatar picker/prefab avatar path.

### 6.6 MVP Acceptance Criteria

The MVP is complete when:

1. An authenticated WebGL user can choose a `.glb` up to 100 MB.
2. The GLB uploads to `avatar-models/users/{user_id}/{avatar_model_id}/avatar.glb`.
3. `avatar_models` contains the uploaded model metadata.
4. `profiles.active_avatar_model_id` points to the model.
5. The uploaded avatar applies to the local player in the current session.
6. Reloading the app restores the same uploaded avatar after login/spawn.
7. Other connected users see the uploaded avatar through NGO model id/path synchronization with correct idle, locomotion, jump, and landing animation rather than position-only ice skating.
8. Late joiners see the uploaded avatar with its current networked animator state after the runtime GLB `Animator.Rebind()`.
9. Invalid, oversized, or blocked models fall back cleanly without preventing session join.
10. Existing preset avatar selection still works for users who do not upload a custom model.

### 6.7 Open Decisions

These can remain undecided until implementation:

1. **Model id vs object path in NGO:** Model id is cleaner and lets clients fetch metadata/status; object path is fewer REST calls. Prefer model id unless latency becomes a problem.
2. **One-active row strategy:** Either reuse one row per user in MVP or create a new row per upload and mark the latest active. Prefer new row per upload because it naturally supports the later multi-avatar library.
3. **Private vs public bucket:** Prefer private bucket with authenticated read. Public bucket is simpler, but harder to moderate and less aligned with user-owned assets.
4. **Dashboard preview timing:** Dashboard avatar library can wait until the Unity MVP proves upload/restore/network sync.
5. **LOD/optimization location:** Runtime optimization is fastest to iterate, but server-side optimization will eventually be better for repeated loads and mobile WebGL performance.

### 6.8 Owner-Authoritative Network Animator Fix

**Implemented:** 2026-08-04  
**Multiplayer verification:** 2026-08-05  
**Status:** The reported stored-GLB ice-skating defect is fixed. Broader regression coverage remains on the production punch list.

#### Reported symptom

Remote users received correct network position changes and could sometimes see a jump transition, but the uploaded GLB did not consistently play locomotion animation. The avatar therefore appeared to slide or "ice skate" between synchronized positions.

#### Root cause

`MetaDynUGSPlayerController` calculates and writes locomotion Animator parameters only for the owning player. Several active player shells still used NGO's server-authoritative `NetworkAnimator`, so the component authority did not match the code that produced the animation state. In addition, applying a downloaded GLB assigns a runtime Humanoid `Avatar` and calls `Animator.Rebind()`, which resets Animator parameters and state on both the owner and remote proxies unless that state is explicitly preserved.

#### Authority contract

1. The owning client is the source of truth for its locomotion Animator parameters.
2. Every network shell used by the avatar registry or default/custom-avatar fallback must use `MetaDyn.Networking.OwnerNetworkAnimator`.
3. `OwnerNetworkAnimator.Animator` and `MetaDynUGSPlayerController` must reference the same root `Animator`.
4. Raw animation state is synchronized through NGO; GLB bytes are not. Each client downloads and binds the model locally from the networked model id.
5. Runtime avatar replacement must preserve already-received proxy state across `Animator.Rebind()`.

#### Implemented changes

- Replaced the stock server-authoritative `NetworkAnimator` component on `Player 2`, `Player 3`, and default `Player UGS` with `OwnerNetworkAnimator`. This also covers the custom-avatar `AvatarChoice = 0` fallback through `Player 2`.
- Added spawn-time diagnostics in `MetaDynUGSPlayerController.OnNetworkSpawn()` for a missing `OwnerNetworkAnimator` or a mismatched root `Animator` reference.
- Added `PrepareAnimatorForAvatarSwap()` to capture non-trigger parameters plus each Animator layer's current state hash, normalized time, and weight before the existing skeleton is removed.
- Added `ApplyRuntimeAvatar()` to assign the validated runtime Humanoid Avatar, call `Animator.Rebind()`, restore captured parameter/layer state, and immediately reapply the owner's current locomotion truth without damping.
- Updated `GLBAvatarLoader.ApplyToPlayer()` to use that state-preserving prepare/apply sequence instead of directly rebinding the Animator.
- Kept `AnimatorCullingMode.AlwaysAnimate` after the swap so remote animation evaluation is not lost when renderer visibility changes.

Triggers are intentionally not reconstructed during a rebind because they are transient events rather than durable Animator state. Durable locomotion booleans/floats and layer state are restored.

#### Files involved

```text
Assets/MetaDyn/Runtime/Networking/OwnerNetworkAnimator.cs
Assets/MetaDyn/Runtime/Networking/MetaDynUGSPlayerController.cs
Assets/MetaDyn/Runtime/Avatar/GLBAvatarLoader.cs
Assets/Starter/PlayerPrefab/Player 2.prefab
Assets/Starter/PlayerPrefab/Player 3.prefab
Assets/Starter/PlayerPrefab/Player UGS.prefab
```

#### Verification and remaining coverage

The project owner built and multiplayer-tested the stored user-bucket GLB flow on 2026-08-05. Uploaded-avatar animation appeared normal to all participating players. The agent did not compile or build the project.

Still required before closing the production punch-list item:

1. Host plus at least two clients.
2. Idle, walk/run, stop, jump, free-fall, and landing viewed from every peer.
3. Profile restore after a full reload.
4. A late join while the uploaded avatar is already active and moving.
5. Repeated avatar replacement and failure fallback.

This animation fix does not implement UGS host migration. Host departure/authority recovery is a separate production punch-list item.

## 7. WebGL GLB Material Fix - Proven Working
**Date verified:** 2026-06-09  
**Status:** Working in WebGL test build

### Symptom
Custom GLB avatar upload could load correctly at first spawn, then reset to Unity magenta/pink after the avatar was applied to the UGS player. A previous fallback conversion to generic URP materials prevented magenta but flattened the avatar to white because it did not preserve the glTF material/shader semantics.

### Root Cause
Runtime GLB materials created by glTFast need glTFast shadergraph shaders available in the WebGL player. Because the materials are created at runtime, Unity can strip the relevant shaders/variants unless the project has build-time references. The correct fix is to anchor glTFast-compatible shader materials in `Resources`, then convert runtime imported materials onto clones of those Resources-backed materials.

### Working Assets
Generate these project Resources materials:

```text
Assets/Resources/GLTFastShaders/gltfast_metallic.mat
Assets/Resources/GLTFastShaders/gltfast_specular.mat
Assets/Resources/GLTFastShaders/gltfast_unlit.mat
```

Use the editor helper:

```text
Tools > MetaDyn > Create GLTFast Shader Materials (WebGL Fix)
```

Implementation helper:

```text
Assets/MetaDyn/Editor/GLTFastShaderMaterialsCreator.cs
```

### Runtime Loader Pattern
The GLB avatar loader must:

1. Let glTFast load and instantiate the GLB normally.
2. Snapshot/log imported material state when diagnosing.
3. Load the three Resources materials with:

```csharp
Resources.Load<Material>("GLTFastShaders/gltfast_metallic");
Resources.Load<Material>("GLTFastShaders/gltfast_specular");
Resources.Load<Material>("GLTFastShaders/gltfast_unlit");
```

4. For each imported renderer material, select the matching glTFast template by shader/material name (`unlit`, `specular`, otherwise `metallic`).
5. Clone the template material, copy imported material properties, restore the template shader, preserve keywords and render queue, then assign the clone back to `renderer.sharedMaterials`.
6. Run the conversion immediately after glTFast instantiate and again after `Animator.Rebind()`/renderer refresh. In the verified build, this stopped the avatar from resetting to pink.

### Do Not Repeat
Do not convert runtime GLB avatar materials to generic `Universal Render Pipeline/Lit`, `Simple Lit`, or `Standard` fallback materials as the primary WebGL fix. That loses glTFast shader behavior and can produce white avatars even when textures exist.

### Useful Logs
If this regresses, capture browser console lines with:

```text
[GLBAvatarLoader] Material after glTFast instantiate:
[GLBAvatarLoader] GLB material Resources conversion at after glTFast instantiate: changed=
[GLBAvatarLoader] Material after Resources material conversion:
[GLBAvatarLoader] GLB material Resources conversion at after animator rebind: changed=
[GLBAvatarLoader] Material after animator rebind conversion:
```

Important fields are `shader=`, `supported=`, and `tex=`.
