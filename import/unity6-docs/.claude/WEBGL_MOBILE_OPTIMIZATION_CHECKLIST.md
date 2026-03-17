# WebGL Mobile Optimization Checklist

## Purpose

This checklist is for shipping the current Unity WebGL space to mobile browsers and PWA installs without breaking the existing desktop-first experience.

It is based on current project decisions and runtime patterns:
- WebGL is the primary platform, native is fallback.
- Browser-native integrations are preferred when WebGL has platform limits.
- Current UI is largely standard Unity `Button`/`TMP_InputField` driven, with a few custom mouse-driven interaction paths in gameplay/UI scripts.

## Current Project Findings

### What already aligns well

- Standard Unity UI buttons should translate to touch through the scene `EventSystem` and `StandaloneInputModule`.
- WebGL-specific browser bridges already exist under `Assets/Plugins/WebGL`.
- The project already treats WebGL as the main deployment target in `.claude/DECISIONS.md`.

### Current mobile risk areas

- Gameplay camera/look code was written around mouse semantics and needs touch-aware pointer handling.
- UI-adjacent scripts had mouse-only checks for "click outside" and input refocus behavior.
- There is no evidence yet of a complete mobile locomotion/control scheme for in-world play.
- Mobile WebGL still has stricter CPU, GPU, memory, thermal, and browser autoplay/input constraints than desktop WebGL.

## Release Checklist

### 1. Define the mobile support target first

- Decide whether "mobile support" means:
  - Full in-world traversal and social features on phones/tablets.
  - UI/login/chat/voice access on mobile, with reduced world interaction.
  - Spectator/lightweight mode only.
- Set a minimum device/browser matrix before optimizing:
  - iPhone Safari
  - Android Chrome
  - iPad Safari
- Set a fallback rule for unsupported devices:
  - Show a lightweight landing page or "best on desktop" notice instead of loading the full scene blindly.

### 2. Put hard budgets in place

- Build size:
  - Keep the initial mobile payload as small as possible.
  - Avoid shipping unused demo assets, sample scenes, and redundant avatar content.
- Runtime memory:
  - Budget for lower RAM ceilings than desktop browsers.
  - Test for repeated scene reloads and reconnects to catch leaks.
- Frame time:
  - Target stable frame pacing, not peak FPS.
  - Treat sustained thermal throttling as a failure even if startup FPS looks acceptable.

### 3. Reduce GPU pressure for mobile browsers

- Use the lowest-cost URP path that still preserves the space identity.
- Minimize:
  - real-time lights
  - shadowed lights
  - transparent overdraw
  - expensive post-processing
  - high-frequency Shader Graph effects
- Prefer:
  - baked lighting where possible
  - simple lit/unlit materials
  - compressed textures sized for mobile screens
  - lower reflection/probe update cost
- Audit avatars for mobile:
  - fewer materials
  - fewer skinned meshes
  - lower blend shape update frequency where acceptable

### 4. Reduce CPU and GC pressure

- Remove avoidable per-frame allocations in gameplay/UI code paths.
- Avoid unnecessary `Update()` polling in UI systems where events are enough.
- Pool frequently created UI items and runtime objects.
- Keep string formatting/log spam out of hot paths in release builds.
- Re-test join/leave flows, avatar selection, chat, and voice together because browser GC spikes stack badly on mobile.

### 5. Make input explicitly touch-aware

- Treat any custom pointer logic as suspect until tested on touch.
- For any script using:
  - `Input.GetMouseButton*`
  - `Input.mousePosition`
  - `EventSystem.current.IsPointerOverGameObject()`
  use touch-aware handling instead of mouse-only assumptions.
- When checking if a touch is over UI, pass the touch `fingerId`.
- Verify these flows on real devices:
  - tap button
  - tap outside to dismiss
  - scroll lists
  - focus chat/message input
  - avatar selection
  - hold-to-talk buttons
  - camera drag vs UI drag conflict

### 6. Separate gameplay controls from UI taps

- Do not let a touch on UI also drive camera/world rotation.
- Add explicit safe zones if the mobile camera uses drag-anywhere controls.
- Consider a dedicated mobile control layer:
  - left thumb movement
  - right thumb camera
  - larger touch targets
  - no hover-dependent affordances
- If full mobile traversal is required, keyboard/mouse-only movement bindings are not enough.

### 7. Optimize UI for touch

- Increase touch target sizes for all critical actions.
- Add spacing so neighboring buttons do not produce accidental taps.
- Avoid tiny icon-only controls unless they have generous hit areas.
- Re-check canvas scaling on portrait and landscape phone widths.
- Test the on-screen keyboard with:
  - chat
  - nickname entry
  - login/profile fields
- Ensure keyboard open/close does not hide critical buttons.

### 8. Degrade features intentionally on mobile

- Add a mobile quality profile instead of hoping desktop defaults scale down.
- Candidates for mobile downgrades:
  - render scale
  - shadow distance
  - avatar count/detail
  - AI perception frequency
  - expensive ambient animation
  - background visual flourishes
- If voice, AI, and multiplayer all run together, define which system loses quality first under load.

### 9. Respect browser-specific WebGL rules

- Keep all mic/audio start flows tied to user gesture.
- Confirm PWA/mobile HTTPS permissions for mic access.
- Test resume behavior after:
  - app switch
  - screen lock
  - Safari/Chrome tab backgrounding
- Validate reconnect and audio recovery after browser interruption.

### 10. Test with a real-device matrix

- Desktop emulation is not enough.
- Minimum manual test pass:
  - iPhone Safari
  - Android Chrome
  - iPad Safari
- For each device test:
  - cold load time
  - peak memory symptoms
  - touch/UI correctness
  - chat keyboard behavior
  - voice permission flow
  - reconnect after background/resume
  - thermal degradation after several minutes

## Input Bugs Reviewed In Current Code

### Fixed in code

- `Assets/Pavilion/Scripts/PlayerInput.cs`
  - UI hit-testing for drag-to-look now uses touch-aware pointer checks instead of mouse-only checks.
- `Assets/Pavilion/Scripts/CameraFollow.cs`
  - Camera drag now respects touch-aware UI hit-testing and touch delta input.
- `Assets/MetaDyn/UserList/UserListEntry.cs`
  - Closing the context menu by tapping outside now works with touch, not just mouse clicks.
- `Assets/MetaDyn/Chat/ChatUI.cs`
  - Re-focusing the chat input now responds to touch taps as well as mouse clicks.

### Still needs product decision / further work

- World movement is still desktop-oriented unless a mobile locomotion scheme is added.
- Push-to-talk and long-press flows should be validated on real devices for pointer-cancel edge cases.
- Any UI prefabs with very small buttons may still be technically correct but poor to use on phones.

## Recommended Execution Order

1. Fix touch/input correctness first.
2. Define a mobile control scheme.
3. Add a mobile quality profile with aggressive rendering defaults.
4. Run device profiling and trim the largest asset/render costs.
5. Re-test voice, chat, avatar UI, and reconnect flows together on phones/tablets.
