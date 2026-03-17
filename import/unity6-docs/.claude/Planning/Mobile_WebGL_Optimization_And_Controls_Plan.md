# Mobile WebGL Optimization And Controls Plan

**Project:** MetaDyn Pavilion
**Date:** 2026-03-03
**Status:** Planning
**Primary Target:** Mobile WebGL in phone/tablet browsers and PWA installs

---

## Goal

Ship a usable mobile WebGL experience for MetaDyn Pavilion without regressing the current desktop-first flow.

This work has two equally important tracks:

1. **Mobile runtime optimization**
2. **Mobile gameplay and UI controls**

The mobile experience should support:

- Login/auth flow
- Avatar selection and spawn flow
- Basic locomotion
- Camera control
- Chat and core UI access
- Voice permission and core voice usage
- Stable multiplayer session behavior on supported devices

---

## Current Baseline

### Already true in the project

- WebGL is the primary deployment target.
- Touch-awareness work has already started in some UI/input paths.
- `PlayerInput` and `CameraFollow` remain fundamentally desktop-oriented.
- Voice is WebRTC-based and already aligned with browser-native behavior.
- Authentication is already web-first, which is a good fit for mobile browsers and PWA installs.

### Current gaps

- No dedicated mobile locomotion UI exists yet.
- No virtual joystick / right-stick camera layer exists yet.
- No mobile-specific quality profile appears to be wired into runtime behavior.
- Existing player movement still depends on desktop input axes.
- Existing camera control still assumes drag + mouse semantics.
- Mobile browser lifecycle cases need explicit validation: keyboard, resume, mic permission, backgrounding.

---

## Product Definition

### Phase 1 mobile support target

Phase 1 should aim for **playable mobile participation**, not full parity with desktop.

Supported:

- Join a space
- Move around with virtual controls
- Rotate/look with touch controls
- Open core UI panels
- Use chat
- Use voice where browser permissions allow

Reduced or constrained on mobile if needed:

- Visual fidelity
- Maximum simultaneous avatar density
- Aggressive AI update frequency
- Optional visual polish effects

Not required for Phase 1:

- Perfect desktop feature parity
- High-end graphics on older phones
- Unlimited player counts on thermally constrained devices

---

## Core Principles

1. Preserve the existing desktop control path.
2. Add mobile behavior as an explicit mode, not a pile of conditionals scattered across gameplay code.
3. Separate touch UI interaction from gameplay camera and movement input.
4. Degrade quality intentionally on mobile rather than relying on desktop defaults.
5. Validate on real devices early, not only in browser emulation.

---

## Proposed Architecture

### 1. Introduce a mobile input adapter layer

Create a small mobile control system that feeds the same gameplay input model already used by the player.

Recommended approach:

- Keep `GameplayInput` as the common payload.
- Extend `PlayerInput` so it can merge input from:
  - desktop axes/mouse
  - mobile UI controls
  - touch camera gestures
- Avoid duplicating player movement logic in `Player.cs`.

Likely new components:

- `MobileInputManager`
- `VirtualJoystick`
- `MobileActionButton`
- `MobileHUDController`
- `MobileDeviceProfile` or `MobileRuntimeSettings`

### 2. Separate movement touch from camera touch

Recommended mobile control scheme:

- **Left thumb:** virtual joystick for locomotion
- **Right thumb:** drag area for camera yaw/pitch
- **Action buttons:** jump, sprint/run, chat, voice, menu

This is preferable to drag-anywhere controls because:

- it avoids UI conflicts
- it is easier to teach
- it scales better with chat/menu overlays

### 3. Add a mobile runtime quality profile

At startup, detect mobile WebGL and apply a constrained runtime profile.

Recommended profile controls:

- reduced render scale
- lower shadow distance or disabled real-time shadows
- lower avatar quality budget where possible
- lower AI polling/perception frequency where acceptable
- reduced post-processing and transparency-heavy effects
- optional cap on visible remote detail

### 4. Add explicit mobile-safe UI behavior

Mobile mode should also govern:

- larger hit targets
- safe-area layout handling
- keyboard-aware layout behavior
- control visibility when chat/menu overlays are open
- touch-aware pointer ownership so gameplay input never leaks through UI

---

## Implementation Plan

## Phase 0: Scope And Baseline Validation

Purpose: lock scope before code changes.

Tasks:

- Define supported device/browser matrix:
  - iPhone Safari
  - Android Chrome
  - iPad Safari
- Define minimum acceptable gameplay target:
  - can join
  - can move
  - can rotate camera
  - can chat
  - can use voice permission flow
- Capture current mobile pain points from existing build on at least one iPhone and one Android device.

Deliverable:

- Baseline notes with concrete failures and performance observations.

## Phase 1: Mobile Input Foundation

Purpose: make player input source-agnostic.

Tasks:

- Refactor `PlayerInput` to support injected mobile input state alongside existing desktop polling.
- Keep `GameplayInput` as the canonical network-facing input structure.
- Add a clean API for:
  - movement vector
  - look delta
  - jump pressed
  - sprint held
  - optional interact/voice/menu triggers
- Ensure `InputManager` locks still suppress gameplay movement from both desktop and mobile paths.

Likely files:

- `Assets/Pavilion/Scripts/PlayerInput.cs`
- `Assets/MetaDyn/Managers/InputManager.cs`
- new mobile input scripts under `Assets/MetaDyn` or `Assets/Pavilion`

Exit criteria:

- Desktop controls still behave the same.
- Mobile controls can feed the player without modifying `Player.cs` movement logic.

## Phase 2: Mobile HUD And Virtual Controls

Purpose: provide an actual playable control surface.

Tasks:

- Build a mobile HUD canvas/prefab.
- Add a left virtual joystick for movement.
- Add a right-side camera touch zone or virtual look stick.
- Add large touch buttons for:
  - jump
  - sprint
  - chat toggle
  - menu
  - push-to-talk if feasible
- Hide or minimize controls that are not useful on phones.
- Respect notches/safe areas.

Design constraints:

- Controls must not overlap critical game UI.
- Buttons must remain reachable with thumbs on common phone sizes.
- Chat open state should hide or disable conflicting gameplay controls.

Likely files:

- new mobile HUD prefab(s)
- new mobile UI scripts
- scene/prefab wiring where the local player or UI bootstrap occurs

Exit criteria:

- A mobile player can move, look, jump, and open core UI without accidental conflicts.

## Phase 3: Camera And Touch Conflict Resolution

Purpose: make camera behavior feel intentional on touch devices.

Tasks:

- Replace mouse-only assumptions in camera rotation with explicit mobile look input.
- Prevent right-side look drag from being stolen by UI panels.
- Ensure taps on UI never rotate the camera.
- Decide whether pinch-to-zoom is supported in Phase 1.

Recommendation:

- Do **not** add pinch zoom in the first implementation unless it is low-risk.
- Preserve the current zoom model for desktop and set a fixed or simplified zoom behavior for mobile initially.

Likely files:

- `Assets/Pavilion/Scripts/CameraFollow.cs`
- `Assets/Pavilion/Scripts/PlayerInput.cs`
- `Assets/MetaDyn/UI/PointerInputUtility.cs`

Exit criteria:

- Camera look is stable and predictable on phones/tablets.
- UI interactions do not leak into camera or movement behavior.

## Phase 4: Mobile Runtime Optimization

Purpose: improve performance and thermal stability.

Tasks:

- Add a mobile runtime detection path.
- Apply mobile quality defaults at startup.
- Audit and reduce:
  - overdraw
  - real-time shadow cost
  - post-processing cost
  - avatar rendering cost
  - frequent allocations in hot paths
- Reduce noisy logs in release-sensitive code paths if they affect mobile performance.
- Revisit AI update cadence for mobile sessions if needed.

Optimization areas to inspect:

- URP asset settings
- Quality settings
- avatar materials and skinned mesh counts
- expensive scene lights
- transparency-heavy UI and VFX
- update-driven scripts in Pavilion and MetaDyn runtime systems

Exit criteria:

- The mobile build is stable over several minutes of session time on target devices.
- Quality degradation is explicit and acceptable.

## Phase 5: Browser And Mobile Lifecycle Hardening

Purpose: handle real mobile browser behavior.

Tasks:

- Validate mic/audio start only from user gestures.
- Test app switching, tab backgrounding, and device lock/unlock.
- Confirm reconnect behavior after resume.
- Test on-screen keyboard interactions with:
  - login/profile
  - avatar naming
  - chat
- Ensure mobile HUD hides or reflows when keyboard is open.

Systems to validate together:

- Web auth bridge
- chat UI
- voice permission flow
- WebRTC audio recovery
- Fusion reconnect/session state

Exit criteria:

- Common interruption cases recover cleanly or fail in a controlled way.

## Phase 6: Device Testing And Acceptance

Purpose: define ship-readiness.

Required manual test matrix:

- iPhone Safari
- Android Chrome
- iPad Safari

For each device, test:

- cold load
- join world
- avatar spawn/select flow
- movement
- camera look
- chat open/type/send
- voice permission and speaking
- background/resume
- thermal degradation after several minutes
- PWA-installed behavior if applicable

Ship criteria:

- core loop is usable
- no blocking UI/input bugs
- no repeated disconnect or unrecoverable audio failures
- acceptable frame pacing for the selected support tier

---

## File And System Impact

### Highest-probability gameplay files

- `Assets/Pavilion/Scripts/PlayerInput.cs`
- `Assets/Pavilion/Scripts/CameraFollow.cs`
- `Assets/Pavilion/Scripts/Player.cs`
- `Assets/MetaDyn/Managers/InputManager.cs`
- `Assets/MetaDyn/UI/PointerInputUtility.cs`
- `Assets/Common/UIGameMenu.cs`
- `Assets/MetaDyn/Chat/ChatUI.cs`

### Likely new assets/scripts

- mobile HUD prefab/canvas
- virtual joystick component
- mobile action button component
- mobile runtime settings/profile component
- mobile bootstrap/controller script

### Likely project settings to review

- Quality settings
- URP asset settings
- WebGL player settings
- canvas scaler settings for mobile layouts

---

## Key Technical Decisions To Make Early

1. **Control scheme**
   - Recommended: left joystick + right drag/look zone + action buttons

2. **Zoom behavior on mobile**
   - Recommended: fixed default zoom at first, revisit advanced zoom later

3. **Push-to-talk UX**
   - Recommended: large hold-to-talk button only after movement/camera are stable

4. **Mobile quality switching**
   - Recommended: automatic runtime mobile profile, not manual user setup only

5. **Feature degradation order under load**
   - Recommended order:
     1. visual quality
     2. AI update frequency
     3. nonessential ambient effects
     4. optional UI animation polish

---

## Risks

### Input regression risk

`PlayerInput` is central. Refactoring it carelessly could break desktop controls or network input consistency.

Mitigation:

- preserve `GameplayInput` shape
- add mobile input as an additive path
- verify desktop behavior after each step

### UI conflict risk

Chat, menus, and gameplay touches can easily fight each other on mobile.

Mitigation:

- assign explicit touch regions
- route all mobile gameplay controls through a single mobile controller
- rely on pointer ownership rules instead of ad hoc checks

### Performance risk

A control layer alone will not make the experience viable if the runtime remains desktop-heavy.

Mitigation:

- pair controls work with a mobile quality profile early
- test on real devices before polishing the control UI

### Voice/browser lifecycle risk

Mobile browser audio and mic permissions are fragile, especially across background/resume.

Mitigation:

- test lifecycle behavior in the middle of implementation, not only at the end

---

## Recommended Delivery Order

1. Refactor input foundation.
2. Add mobile HUD and virtual controls.
3. Resolve camera and UI touch conflicts.
4. Add mobile quality/runtime profile.
5. Validate browser lifecycle and voice behavior.
6. Run device acceptance pass and tune.

---

## Definition Of Done

The first mobile milestone is complete when:

- a user can join on a supported phone/tablet browser
- movement and camera control are reliable with touch UI
- chat and key menus remain usable
- the build applies a mobile-appropriate quality profile
- voice permission flow works where supported
- the session remains playable for several minutes without major thermal or input failure

---

## Immediate Next Step

Before implementation starts, convert this plan into a concrete task checklist with:

- exact scripts/prefabs to create
- ownership of each phase
- acceptance checks per phase
- at least one real iPhone and one real Android device reserved for repeated testing
