# Architectural Decisions Log

## Format
```
## Decision Title
**Date:** YYYY-MM-DD
**Status:** Accepted | Rejected | Superseded | Deprecated
**Context:** What situation led to this decision
**Options Considered:**
1. Option A - pros/cons
2. Option B - pros/cons
**Decision:** What was chosen
**Rationale:** Why this was the best choice
**Consequences:** Impact on the project
```

---

## Dynamic Avatar Selection with Dual Lists (Not Static Male/Female)

**Date:** 2025-12-21
**Status:** Accepted

**Context:**
Avatar selection was hardcoded to 2 options (MaleAvatarPrefab/FemaleAvatarPrefab on GameManager). As MetaDyn expands avatar offerings across Ready Player Me and Avatar SDK, need scalable system supporting unlimited avatars with visual selection.

**Options Considered:**

1. **Keep Static Fields, Add More (Male/Female/Teen/Child/etc.)**
   - Pros: Simple, no code changes
   - Cons: Doesn't scale, UI would need manual updates for each new avatar, limited to predefined types

2. **Single Avatar List on GameManager**
   - Pros: Scalable, simple data structure
   - Cons: No visual separation between RPM and AvatarSDK, harder to organize

3. **Dual Lists with AvatarEntry Class (RPM + AvatarSDK)**
   - Pros: Scalable to unlimited avatars, visual separation by provider, thumbnail support, dynamic UI generation
   - Cons: Slightly more complex, requires UI layout components

4. **Move Avatar Lists to UIGameMenu**
   - Pros: Data lives where it's used
   - Cons: GameManager needs data for spawning, creates circular dependency

5. **ScriptableObject Avatar Config**
   - Pros: Data separate from logic, reusable
   - Cons: Extra asset management, overkill for current needs

**Decision:** Dual Lists with AvatarEntry Class on GameManager, dynamic UI population in UIGameMenu

**Implementation:**
- `AvatarEntry` class: `NetworkObject prefab` + `Sprite thumbnail`
- GameManager stores: `readyPlayerMeAvatars` and `avatarSDKAvatars` lists
- UIGameMenu waits for GameManager.Instance in Update(), then populates dual scrollviews
- Index-based selection: RPM avatars get indices 0, 1, 2..., AvatarSDK continues from there
- PlayerPrefs stores combined index

**Rationale:**
- **Scalability:** Add unlimited avatars without code changes
- **Visual Organization:** Separate scrollviews for RPM vs AvatarSDK
- **Thumbnails:** Players see what they're selecting
- **Data Location:** GameManager owns data (singleton, spawning logic needs it)
- **WebGL Compatible:** Timing fix ensures UI waits for GameManager to spawn
- **Future-Proof:** Easy to add categories (Premium, Community, etc.) by adding more lists

**Consequences:**
- ✅ Unlimited avatar scalability
- ✅ Visual thumbnail selection
- ✅ Works in Editor and WebGL
- ✅ Clear separation by provider (RPM vs AvatarSDK)
- ⚠️ UI requires HorizontalLayoutGroup + ContentSizeFitter setup
- ⚠️ Must wait for GameManager.Instance before populating (WebGL timing)
- 🔮 Future: Could add categories, filters, search, marketplace integration

---

## Use Photon Fusion Shared Mode (Not Client-Server)

**Date:** Nov 2025 (estimated)
**Status:** Accepted

**Context:**
Choosing network topology for multiplayer metaverse platform.

**Options Considered:**
1. **Photon Fusion Client-Server Mode**
   - Pros: More authoritative, better for competitive games, dedicated server control
   - Cons: More complex, requires server hosting, harder to develop
2. **Photon Fusion Shared Mode**
   - Pros: Simpler P2P model, players have authority over their objects, easier development
   - Cons: Less secure, not ideal for competitive gameplay
3. **Photon PUN 2**
   - Pros: Mature, well-documented
   - Cons: Older framework, less performance than Fusion

**Decision:** Photon Fusion 2.0.4 Shared Mode

**Rationale:**
- Metaverse is social, not competitive (security less critical)
- Faster development iteration
- Players having authority over their own character feels natural
- Host authority for UserListManager provides needed moderation control
- Hybrid approach: Shared Mode for players, host authority for global state

**Consequences:**
- Easier to prototype and develop
- Host migration needed for production
- Permission system must be host-authoritative (implemented in UserListManager)
- Works well for 8-16 player sessions

---

## Render-Based Change Detection (Not IPlayerJoined/IPlayerLeft)

**Date:** 2025-11-29
**Status:** Accepted

**Context:**
User list synchronization had race conditions between player spawn and registration timing. Fusion's IPlayerJoined fires when player joins session, not when they're added to custom user list.

**Options Considered:**
1. **Use Fusion's IPlayerJoined/IPlayerLeft callbacks**
   - Pros: Standard Fusion pattern
   - Cons: Timing issues, fires before custom registration, race conditions
2. **Render-based change detection (frame-by-frame diff)**
   - Pros: Frame-accurate, no race conditions, reacts to actual state changes
   - Cons: Slightly more code, runs every frame
3. **Manual event firing on registration**
   - Pros: Explicit control
   - Cons: Easy to forget, coupling between systems

**Decision:** Render-based change detection with previous state comparison

**Rationale:**
- Eliminates all race conditions between spawn and registration
- Frame-accurate detection of NetworkDictionary changes
- No dependency on Fusion's callback timing
- Handles late-joiners automatically
- Performance impact negligible (dictionary comparison is fast)

**Consequences:**
- More reliable user list synchronization
- Cleaner code (no callback interfaces)
- Pattern can be reused for other NetworkDictionary use cases
- Slight CPU overhead (acceptable for user list size)

---

## RPC Registration Pattern for User List

**Date:** 2025-11-29
**Status:** Accepted

**Context:**
Players need to register with UserListManager, but in Shared Mode they spawn with state authority over their own object while only the host has authority over UserListManager.

**Options Considered:**
1. **Direct registration in Player.Spawned()**
   - Pros: Simple, direct
   - Cons: Doesn't work - players can't modify host's NetworkDictionary
2. **RPC to host for registration**
   - Pros: Works with authority model, decouples systems
   - Cons: Slight network delay (acceptable)
3. **Host detects spawns via callback**
   - Pros: Centralized control
   - Cons: Tight coupling, harder to debug

**Decision:** RPC-based registration (`RPC_RegisterWithUserList`)

**Rationale:**
- Respects authority boundaries (player has authority on self, host on user list)
- Decouples Player from UserListManager
- Works regardless of spawn order
- Single source of truth (host's UserListManager)
- Allows player to send their name with registration

**Consequences:**
- Clean separation of concerns
- Slight network delay for registration (negligible)
- Pattern works well with Shared Mode topology

---

## First-Player Auto-Admin

**Date:** Nov 2025 (estimated)
**Status:** Accepted

**Context:**
Need someone to moderate sessions, but no external auth system yet.

**Options Considered:**
1. **No default admin (manual assignment)**
   - Pros: More control
   - Cons: How do you assign first admin?
2. **First player becomes admin**
   - Pros: Always someone in charge, great for testing
   - Cons: First player has power (could be abused)
3. **Random admin assignment**
   - Pros: Fair
   - Cons: Unpredictable, confusing

**Decision:** First player to join becomes admin (with toggle to disable)

**Rationale:**
- Ensures there's always someone who can moderate
- Great for development and testing
- Solves "cold start" problem
- Can be disabled via inspector for production
- Will be superseded by proper auth system later

**Consequences:**
- Sessions always have a moderator
- Potential for abuse (acceptable for alpha)
- Inspector toggle provides flexibility
- TODO: Replace with Supabase role assignment

---

## Push-to-Talk Default (IsMuted = true)

**Date:** Nov 2025 (estimated)
**Status:** Accepted

**Context:**
Voice recording system ready, need to decide default mic state.

**Options Considered:**
1. **Hot mic (always on)**
   - Pros: Easier conversation flow
   - Cons: Privacy issues, background noise, accidental recording
2. **Push-to-talk (default muted)**
   - Pros: Privacy, bandwidth savings, professional standard
   - Cons: Requires button hold to speak

**Decision:** Default to muted, push-to-talk to speak

**Rationale:**
- Privacy-first approach
- Prevents accidental hot mic situations
- Industry standard for multiplayer (Discord, VRChat, etc.)
- Reduces bandwidth when voice streaming is implemented
- User controls when they speak

**Consequences:**
- Better user experience (no surprise recordings)
- Slightly more friction to speak (acceptable trade-off)
- Reduced bandwidth usage
- Professional user expectation

---

## WebGL-First Platform Strategy

**Date:** Nov 2025 (estimated)
**Status:** Accepted

**Context:**
Choosing primary target platform for metaverse.

**Options Considered:**
1. **Native builds (Windows/Mac/Linux)**
   - Pros: Better performance, full feature access
   - Cons: Download barrier, deployment complexity
2. **WebGL (browser-based)**
   - Pros: No download, instant access, cross-platform
   - Cons: Performance limitations, browser API restrictions
3. **VR-first (Quest/PCVR)**
   - Pros: Immersive
   - Cons: Limited audience, expensive hardware

**Decision:** WebGL as primary target, native as fallback

**Rationale:**
- Instant access (no download) lowers barrier to entry
- Deployment system optimized for web servers
- MetaDyn SDK built around WebGL deployment
- Browser is most accessible platform
- Can still build native for better performance
- Voice recording system has WebGL-specific optimizations

**Consequences:**
- Custom JavaScript plugins for browser features (microphone)
- Performance tuning required (large buffer sizes, disabled processing)
- Build size considerations
- Deployment pipeline focused on web servers
- Native builds available for power users

---

## Object Pooling for UI Elements

**Date:** 2025-11-29
**Status:** Accepted

**Context:**
User list entries created/destroyed as players join/leave, causing GC spikes.

**Options Considered:**
1. **Instantiate/Destroy on demand**
   - Pros: Simple, straightforward
   - Cons: GC allocation spikes, frame drops
2. **Object pooling with reuse**
   - Pros: No GC spikes, smooth performance
   - Cons: More code, memory overhead
3. **Static list with enable/disable**
   - Pros: No allocation
   - Cons: Wastes memory for max capacity

**Decision:** Object pooling with initial size of 10 entries

**Rationale:**
- Prevents GC spikes during gameplay
- Professional optimization for multiplayer
- 10-entry pool covers typical session size (8 players)
- Grows dynamically if needed
- Performance-critical (player join/leave happens frequently)

**Consequences:**
- Smooth performance during player join/leave
- Slightly more complex code (Queue management)
- Memory overhead acceptable (~10 UI objects)
- Reusable pattern for other UI systems

---

## SDK Component Pattern (Inspector-Friendly, Inline Editor Code)

**Date:** 2025-12-19
**Status:** Accepted

**Context:**
MetaDyn SDK needs standardized pattern for world-building components that non-programmers can use. Need clear guidelines for implementing features like seats, teleporters, doors, triggers, etc.

**Options Considered:**
1. **Separate Editor folder structure**
   - Pros: Clean separation, traditional Unity pattern
   - Cons: More files, harder to maintain, split context
2. **Inline editor code with #if UNITY_EDITOR**
   - Pros: Single file, easy to maintain, clear context
   - Cons: Slightly larger runtime builds (negligible after compilation)
3. **No editor visualization (runtime only)**
   - Pros: Simplest code
   - Cons: Poor creator experience, hard to configure

**Decision:** Inline editor code pattern with strict conventions

**Pattern Requirements:**
- All SDK components in `MetaDyn` namespace
- Single file per component in `/Assets/MetaDyn/Core/Runtime/`
- XML documentation on classes (`/// <summary>`)
- `[Header]` and `[Tooltip]` attributes on all public fields
- Public API for external script access
- Inline editor code with `#if UNITY_EDITOR` directives
- Clear gizmos and scene view helpers
- Inspector-friendly configuration (no code required)
- Minimal dependencies or clearly documented

**Rationale:**
- **Single file convenience**: Easier to maintain, copy, share, and understand
- **Context preservation**: Editor visualization next to runtime code
- **Creator-friendly**: Non-programmers can use components via inspector
- **Visual feedback**: Gizmos provide immediate feedback in scene view
- **Consistent API**: All SDK components follow same pattern
- **Professional polish**: Tooltips and headers improve UX
- **Build size negligible**: `#if UNITY_EDITOR` removes editor code from builds

**Reference Implementation:**
SeatHotspot.cs (407 lines) demonstrates pattern:
- Comprehensive tooltips on all public fields
- Inspector sections with [Header] attributes
- Public API (IsOccupied, SitDown(), StandUp())
- Editor gizmos (seat position, orientation arrow, interaction range)
- Inline editor code at end of file with #if UNITY_EDITOR
- Zero external dependencies

**Consequences:**
- Faster SDK component development (no separate editor files)
- Better creator experience (visual feedback in scene view)
- Consistent API across all SDK features
- Clear development guidelines for team
- Reduced learning curve for world creators
- Pattern established for future features (teleporters, doors, spawn points, triggers, zone volumes, etc.)

---

## Template for Future Decisions

```markdown
## Decision Title

**Date:** YYYY-MM-DD
**Status:** Accepted

**Context:**
Why this decision needed to be made.

**Options Considered:**
1. **Option A**
   - Pros: Benefits
   - Cons: Drawbacks
2. **Option B**
   - Pros: Benefits
   - Cons: Drawbacks

**Decision:** What was chosen

**Rationale:**
- Why this was the best choice
- Key factors in the decision

**Consequences:**
- Impact on the project
- Trade-offs accepted
```
