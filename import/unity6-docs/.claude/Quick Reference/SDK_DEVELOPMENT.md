# SDK Development & Documentation Guide

Standards and workflow for building, documenting, and shipping MetaDyn SDK features/components.

**Status:** Active Reference | **Last Updated:** 2026-02-23

---

## Purpose

Use this document when adding or updating MetaDyn SDK systems so implementation, editor UX, runtime behavior, and documentation stay consistent.

Goals:
- Keep SDK components predictable for scene builders and developers.
- Ship features with documentation and examples at the same time.
- Preserve WebGL-first performance and multiplayer/networking constraints.

---

## Scope (What Counts as SDK)

MetaDyn SDK includes reusable runtime components, managers, editor tooling, deployment utilities, and integration bridges used across spaces/projects.

Examples:
- Runtime components (`SeatHotspot`, `Interactable`, `ProjectionSurface`)
- Managers (`InputManager`, `SettingsManager`, `UIManager`)
- Dashboard/auth integration (`SupabaseAuthManager`, `WebAuthBridge`)
- AI embodiment systems (`AIPerceptionManager`, `AIMemoryManager`)
- Editor tools (`MetaDynProjectConfig`, deployment tooling)

---

## Core Principles

1. Reusable first: Build features as configurable components, not scene-specific scripts.
2. WebGL-aware by default: Avoid allocations/spikes and browser-incompatible APIs unless guarded.
3. Multiplayer-safe: Be explicit about authority, RPC ownership, and synchronization.
4. Document as you build: API, inspector fields, setup, and limitations ship together.
5. Backward-friendly changes: Prefer additive changes; call out migrations when breaking changes are necessary.

---

## Spatial Toolkit Reference Notes (Planning Input)

Based on review of Spatial Toolkit docs/reference and the Spatial Unity SDK repo (used here only as a design benchmark for MetaDyn SDK planning):

### What Was Observed (Unity-side)

- Spatial exposes platform features through a central bridge/facade (`SpatialBridge`) with service-style accessors.
- Their scripting/network model is normalized around SDK base types and synced variables (for example `SpatialNetworkBehaviour`, `NetworkVariable<T>` style usage).
- Platform actions are wrapped in coroutine-friendly async operations (`SpatialAsyncOperation` pattern).
- Repo/package organization is disciplined (`Runtime`, `Editor`, simulation/testing layers, examples, docs/reference).
- Documentation is split between task guides and API reference, which lowers adoption friction.

### What MetaDyn Should Borrow

- A single SDK entry point (`MetaDynBridge` or equivalent) instead of direct singleton discovery everywhere.
- Service interfaces for major subsystems (auth, users, voice, AI, UI, deployment/runtime config).
- A simplified SDK-facing networking abstraction over Fusion for common operations (ownership, spawn, sync, callbacks).
- Coroutine-friendly async wrappers for auth/memory/API operations.
- Better packaging boundaries (`Runtime` vs `Editor`, examples/samples, templates).
- Task docs + API docs + examples shipped together.

### What MetaDyn Should NOT Copy Blindly

- Spatial-specific platform constraints/sandbox assumptions.
- API shapes that depend on Spatial runtime semantics rather than our Fusion/WebGL/self-hosted stack.

### Immediate MetaDyn Planning Implication

Before broad SDK expansion, define:

1. SDK boundary (what is core package, what is baseline platform/starter content, and what is truly project-specific)
2. Service map (bridge + interfaces)
3. Extraction plan for core SDK/platform scripts currently outside `Assets/MetaDyn`

This is now tracked in the SDK inventory docs and future architecture planning.

---

## Recommended Folder Placement

Use the existing SDK structure unless there is a strong reason to introduce a new category.

```text
/Assets/MetaDyn/Core/Runtime/Components/     Reusable scene components
/Assets/MetaDyn/Managers/                    Cross-cutting managers/singletons
/Assets/MetaDyn/[FeatureArea]/               Feature systems (AI, Audio, Dashboard, UserList)
/Assets/MetaDyn/Core/Editor/MetaDynSDK/      Editor windows, deployment tools, inspectors
/Assets/Plugins/WebGL/                       jslib browser bridges
```

Rules:
- Runtime code must not depend on UnityEditor APIs.
- WebGL browser interop belongs in `.jslib` + a C# bridge wrapper.
- Truly world-specific orchestration stays outside the SDK when possible.
- Baseline launcher/player/session/bootstrap files required by every MetaDyn space are part of the unified SDK system, even if they are temporarily located outside `Assets/MetaDyn`.

---

## Unity-Integrated SDK Product Requirements (Planned)

The MetaDyn SDK is intended to be a **fully integrated Unity toolkit experience**, not just a static set of files copied manually.

### Creator Experience Goals

- SDK functionality is surfaced directly inside Unity via the **MetaDyn menu/dashboard**.
- Creators can see:
  - current installed SDK version
  - latest available SDK version
  - update availability/status
  - release notes / breaking change warnings
  - optional/new components available to install and test
- Common actions should be one-click from Unity:
  - `Check for Updates`
  - `Update SDK`
  - `Install Optional Component`
  - `View Changelog / Docs`

### Distribution / Storage Model (Planned)

- SDK source and release assets can be hosted on **GitHub** (similar to Spatial's public SDK distribution model).
- Unity editor tooling should query a remote manifest/release endpoint (GitHub release metadata or a MetaDyn-maintained manifest JSON).
- First-pass manifest structure is documented in `SDK_UPDATE_MANIFEST.md`.
- SDK updater should determine:
  - installed version
  - latest compatible version
  - optional package/component availability
  - migration notes (if any)

### Unity Startup Update Check (Planned)

When a creator opens Unity with a project using MetaDyn SDK:

1. MetaDyn editor bootstrap runs on editor load.
2. It checks installed SDK version (local metadata).
3. It checks remote manifest/release info.
4. If newer compatible version exists:
   - show non-blocking notification in Unity
   - surface update action in MetaDyn Dashboard/Menu
5. Creator chooses whether to update immediately or later.

Important:
- Default behavior should be **non-destructive** and creator-controlled.
- Auto-update should not silently overwrite project-specific modifications.

### Update Mechanism Requirements (Planned)

- Pull/update SDK files into the project in a controlled way (GitHub-backed source).
- Preserve project-specific content (environments, avatars, scenes, custom scripts).
- Detect/flag local modifications to SDK files before overwrite.
- Provide clear success/failure status and rollback guidance.
- Support version pinning or channels later (`stable`, `beta`) if needed.

### Optional Components / Marketplace-Like Behavior (Planned)

MetaDyn menu/dashboard should support discovering and installing additional SDK modules/components, for example:

- new runtime components
- editor tools
- integrations (AI, auth, analytics, moderation)
- sample prefabs/templates

This should be driven by a manifest/catalog so creators can browse what is available without manually importing packages.

### Planning Implications

This means the SDK roadmap includes not only runtime components, but also:

- Editor update service / manifest client
- Version management and compatibility checks
- Install/update UX in `MetaDynDashboard` / `MetaDynMenu`
- Component catalog/install flow
- Safe file replacement / migration strategy

These are product requirements for the SDK experience and should be treated as first-class SDK work.

### MetaDyn Dashboard Update UX Requirement (Current Editor Integration Target)

The existing Unity editor window `MetaDynDashboard` is the correct place to surface SDK update state and update actions.

Current implementation reference:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDashboard.cs`
- Current status label location includes `Status: Ready`

Planned behavior:
- The dashboard should check the installed SDK version against the latest available SDK version.
- In the dashboard status area, near the current `Status: Ready` UI, show update state clearly.
- On the right-hand side of that status row/panel, add an `Update SDK` button.

Button state rules:
- **Up to date:** button is visible but disabled
- **Update available:** button is enabled
- **Checking:** optional temporary disabled/loading state
- **Error checking:** disabled or retry-capable, with status text explaining failure

Minimum dashboard information to show:
- installed version
- latest version
- status (`Up to date`, `Update available`, `Checking`, `Check failed`)
- actionable update button

This should be treated as the first concrete UI target for the SDK self-update system.

---

## Packaging & Distribution Requirements (Planned)

MetaDyn planning must distinguish between:

- **Unity Starter Package**: Unity-provided baseline package/files used by a Unity starter setup
- **MetaDyn SDK**: MetaDyn-provided reusable platform/runtime/editor systems
- **MetaDyn Starter Space Template**: MetaDyn-provided Unity project/template containing the SDK plus a starter environment

### Deliverable Definitions

#### Unity Starter Package

This is **not** provided by MetaDyn.

It refers to the Unity-side starter/bootstrap package content that a Unity starter setup may already include. MetaDyn should not treat this as a MetaDyn-owned deliverable.

#### MetaDyn SDK

This is the MetaDyn-owned reusable installable platform layer.

It includes:
- platform SDK runtime systems
- editor tooling and dashboards
- deployment/runtime configuration path
- dependency management/version checks
- MetaDyn-owned integrations and components

The SDK should be installable into existing Unity projects.

#### MetaDyn Starter Space Template

This is a separate MetaDyn-owned starter Unity environment/template.

It includes:
- MetaDyn SDK
- a starter/home environment
- any project/template setup needed for creators to begin building a space

### Space Portability Requirement

Each MetaDyn space / instance / activation should carry the same MetaDyn platform layer with it through the SDK and any required integration files.

Practical implication:
- the same core platform systems should travel with each project/space
- creators should not need to reconstruct core startup/auth/platform plumbing manually
- SDK updates should target a known, structured package layout

### Unity Package Requirement

The repository should be structured so the MetaDyn SDK can be distributed as a Unity package/importable toolkit, not only as a manually copied project folder.

Planning target:
- package-friendly folder boundaries
- minimal scene/environment assumptions inside SDK contents
- stable editor/runtime separation
- clear separation between SDK contents and starter space template contents

### Project Settings Rule

`ProjectSettings` are not part of the MetaDyn SDK by default.

Reason:
- the SDK must be installable into existing Unity projects
- project-level Unity configuration should not be treated as reusable SDK content

`ProjectSettings` may belong to a MetaDyn Starter Space Template if needed for that template to open and run correctly.

### OpenUPM / Package Manager Planning

MetaDyn should plan for a package distribution model compatible with Unity package workflows, including future support for something like OpenUPM.

This implies:
- package metadata and versioning discipline
- semantic versioning expectations
- dependency clarity
- no hidden reliance on arbitrary project-local files
- a clean install/update story for package consumers

### Photon Fusion Dependency Requirement

Photon Fusion is a required dependency of the MetaDyn SDK and should be treated as part of the supported installation flow.

Current supported version in this project:
- **Photon Fusion 2.0.9 Stable**

Planning requirement:
- the supported Fusion version must install as a dependency when MetaDyn SDK is installed
- creators should not have to manually reconstruct the correct Fusion setup for a normal SDK install
- MetaDyn editor tooling should still verify that the correct Fusion version is present after install/update

Known platform/business note:
- Fusion is legally distributable with the package flow used for MetaDyn
- default/freemium usage is currently understood as having a `20 user` limit unless the license is upgraded

Implications for package/update planning:
- MetaDyn package manifest/dependency flow should target the correct Fusion version
- MetaDyn Dashboard should eventually show Fusion dependency status alongside SDK status
- installer/updater should detect incompatible Fusion versions and prompt corrective action
- docs should clearly state the supported Fusion version and any license/usage caveat

### MetaDyn Dashboard Fusion Info Requirement

The Unity `MetaDyn Dashboard` should include a separate informational section for Photon Fusion.

Required dashboard behavior:
- show the supported Fusion version used by the SDK
- show the currently installed Fusion version detected in the local project
- present Fusion as a required platform dependency
- keep this informational only unless/until a future Fusion validation flow is added

Important:
- this dashboard section is **not** for updating Fusion directly right now
- it is for clearly exposing the expected Fusion version to creators inside Unity

### Architectural Consequence

When evaluating whether a file belongs in the SDK, ask:

1. Is this MetaDyn-owned reusable platform functionality?
2. Does this belong in the MetaDyn SDK, in a MetaDyn starter space template, or outside MetaDyn-owned deliverables?
3. Can this be updated safely through SDK/package updates later?

This framing should guide all extraction and packaging decisions going forward.

---

## Component Design Standard (Runtime)

Follow the existing MetaDyn SDK component pattern:

```csharp
namespace MetaDyn
{
    public class ComponentName : MonoBehaviour
    {
        [Header("Configuration")]
        [Tooltip("What this field controls")]
        public float someSetting = 1f;

        public bool IsReady => _isReady;

        public bool TryDoThing(GameObject target)
        {
            // Return success/failure; avoid silent no-op APIs.
            return false;
        }

        #if UNITY_EDITOR
        private void OnDrawGizmos() { }
        #endif
    }
}
```

Guidelines:
- Prefer explicit inspector fields with `[Header]` and `[Tooltip]`.
- Expose read-only state via properties.
- Prefer `Try*` methods or clear return values for interaction APIs.
- Add editor gizmos for spatial components (ranges, hotspots, paths).
- Keep responsibilities narrow; use managers/orchestrators for cross-system behavior.

---

## Multiplayer / Fusion Checklist

For any networked SDK feature, define and document:

- Authority model: `StateAuthority`, `InputAuthority`, or local-only.
- Sync method: `Networked` properties, `NetworkDictionary`, RPCs, or local state.
- Join-in-progress behavior: What state late joiners receive.
- Host-only actions: Validation paths for kick/ban/admin/moderation actions.
- Failure handling: What happens if authority is missing.

Common pattern:

```csharp
if (!Object.HasStateAuthority) return;
```

Document the exact reason for authority checks so future changes do not break host/client behavior.

---

## WebGL Compatibility Checklist

Before calling a feature "SDK ready", verify:

- `UNITY_WEBGL && !UNITY_EDITOR` guards around browser-specific code.
- Fallback behavior in Editor/native builds.
- No unsupported threading/background assumptions.
- Reasonable memory usage and reduced allocations.
- Input/browser permission flows (mic/camera) are user-triggered where required.
- `jslib` bridge functions fail safely and log actionable errors.

If a feature is WebGL-limited, document it clearly in the component section and quick reference.

---

## Documentation Requirements (Per Feature)

Every new SDK feature/system should include documentation updates in the same change set.

Minimum documentation:
- What it does (1-2 sentences)
- File path(s)
- Public API (methods, events, key properties)
- Inspector configuration (important serialized fields)
- Setup steps (scene/prefab dependencies)
- Runtime behavior notes (authority, events, lifecycle)
- Known limits/performance considerations
- Example usage (short code or scene setup)

Where to document:
- `QUICK_REFERENCE.md`: Add file path and one-line purpose if broadly useful
- Feature docs in `.claude/Quick reference/`: For larger systems (AI/auth/infra-level complexity)
- `CHANGELOG.md`: User-visible changes
- `DECISIONS.md`: Architectural decisions/tradeoffs (when applicable)

---

## Build-Out Workflow (Recommended)

1. Define the component/system contract
   - Purpose, scope, non-goals
   - Inspector fields and defaults
   - Public API and events
   - Networking/authority behavior (if applicable)
2. Implement the runtime/editor code
   - Keep runtime/editor separation clean
   - Add guards/logging for invalid setup
   - Add gizmos/debug tooling for complex spatial systems
3. Integrate in one scene/prefab
   - Validate real usage, not just isolated code
   - Test WebGL path if browser interop/audio/video/network is involved
4. Document immediately
   - Update quick reference entry
   - Add or extend feature doc
   - Record caveats and setup requirements
5. Ship with verification notes
   - What was tested (Editor, WebGL, multiplayer, number of clients)
   - What remains unverified

---

## Definition of Done (SDK Feature)

A feature is considered SDK-complete when:

- Implementation works in intended scenes
- Public API is stable and documented
- Inspector settings are clear and self-describing
- WebGL behavior is tested or limitations documented
- Multiplayer authority/sync paths are tested or documented
- Error cases fail safely (no hard null crashes in common misconfigurations)
- `QUICK_REFERENCE.md` and relevant docs are updated

---

## Documentation Template (Copy/Paste)

Use this section structure for new SDK docs in `.claude/Quick reference/`.

```md
# Feature/System Name

Short description of what the system does and why it exists.

**Status:** Prototype / In Progress / Production Ready | **Last Updated:** YYYY-MM-DD

---

## Overview

## Key Files

## Features

## Public API

## Inspector Configuration

## Setup / Integration

## Runtime Behavior

## Performance Considerations

## Troubleshooting

## Related Documentation
```

---

## Suggested Build Priorities for SDK Expansion

When building out the SDK further, prioritize reusable systems over project-specific polish:

1. Core reusable components (interaction, triggers, seating, projection)
2. Multiplayer moderation/admin tooling
3. Editor productivity tools (validation, setup wizards, deploy UX)
4. Auth/profile integrations shared across Unity + web surfaces
5. AI embodiment modules with clear toggles/fallbacks
6. Analytics/telemetry and diagnostics tooling

This order improves adoption and reduces maintenance cost.

---

## Common Pitfalls

- Building feature logic directly into Pavilion scene scripts instead of SDK components.
- Mixing editor APIs into runtime assemblies/scripts.
- Shipping undocumented inspector fields with unclear defaults.
- Assuming host authority on all clients.
- Marking features production-ready without WebGL validation.
- Forgetting to update quick reference paths after file moves/renames.

---

## Related Documentation

- [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- [INFRASTRUCTURE.md](INFRASTRUCTURE.md)
- [AUTH_SYSTEM.md](AUTH_SYSTEM.md)
- [AI_EMBODIMENT.md](AI_EMBODIMENT.md)
