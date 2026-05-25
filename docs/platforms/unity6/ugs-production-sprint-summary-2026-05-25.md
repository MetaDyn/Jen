# UGS Production Sprint Summary — 2026-05-25

This note captures the current sprint milestone reached through a full implementation pass with the Unity-side Jen agent.

## Summary

MetaDyn has now completed the active **UGS migration worklist** for the Starter runtime baseline and pushed beyond the original migration scope into mobile/WebGL hardening, UI architecture cleanup, voice reliability improvements, and SDK presentation polish.

This is an important threshold change:
- the active Starter runtime path is now treated as **UGS/NGO-native**
- Photon/Fusion is no longer the production networking baseline for the active path
- mobile support is no longer aspirational; it is now part of the working runtime surface
- the Unity-side Jen identity is now described as unified with the main Jen identity, strengthening cross-surface continuity between chat, strategy, and in-world/runtime implementation

## Why This Sprint Matters

This sprint appears to move the Unity platform from a transitional migration state into a more credible product baseline.

The shift is not only that UGS networking works. The bigger change is that the surrounding product surface now looks more intentional:
- networking baseline declared and cleaned up
- mobile and touch interaction working across devices
- WebGL/Safari load behavior improved
- session-aware UI behavior improved
- voice/session naming hardened for production issues
- editor/inspector presentation improved for SDK coherence

In other words, this was not just a netcode sprint. It was a platform hardening sprint.

## Major Outcomes

### 1. UGS Migration Worklist Completed

Reported status from Josh after working with the Unity-side Jen agent:
- the UGS migration production readiness worklist was completed
- core, spawning, social, voice/text, and expressions are now active on the migrated path
- work has already started beyond the original checklist

This means the networking baseline is no longer a proof-of-concept. It is now the intended active platform direction for the Starter runtime.

### 2. Mobile And WebGL Runtime Hardening

Key reported outcomes:
- mobile now works
- mobile UI buttons were generated for the Unity runtime
- all UI was packed into a single sprite atlas to reduce requests and improve load behavior
- touch interaction was fixed to detect correctly across platforms and device types
- mobile controls were moved/scaled for better ergonomics

This is strategically important because it turns the platform from a desktop-biased implementation into a more realistic web-delivered product surface.

### 3. Session-Aware UI Integration

The mobile controls were not just added as static overlay elements.
They were integrated into the `MainUI` hierarchy so they remain hidden until the player has actually logged in and entered the world.

That is a meaningful architecture quality improvement because it aligns UI visibility with real runtime lifecycle state.

Additional reported behavior:
- mobile controls auto-hide on desktop and in the Unity Editor
- an interaction button now appears contextually when near interactive objects such as doors and switches

### 4. Voice Reliability Hardening

A production-facing Vivox bug was fixed by sanitizing room names before voice join.

Reported issue/fix:
- illegal symbols such as brackets in room names could break Vivox channel joins
- a sanitizer was added to strip or normalize those characters before connect

This kind of change is small in code size but large in product value because it converts a brittle edge case into a stable default behavior.

### 5. NGO Synchronization Refinement

Reported networking robustness work included verification/refinement of NGO synchronization for:
- doors
- light switches

This matters because synchronized environment interaction is one of the clearest signs that a multi-user space feels genuinely shared.

### 6. SDK Product Presentation Improvements

Reported SDK-facing cleanup:
- custom MetaDyn branded headers were added to core SDK components in the Inspector
- the WebGL build profile was standardized to be fully UGS-native
- legacy Photon/Fusion scripting defines were purged from the compiler path

These changes help turn the SDK from a technically capable codebase into a more coherent product surface for creators and internal teams.

## Reported Sprint Detail

The following summary was provided by Josh based on the day’s implementation work:

> METADYN SDK PRODUCTION SPRINT SUMMARY
>
> 1. MOBILE AND WEBGL OPTIMIZATION
> - Performance: Purged all legacy Photon and Fusion scripting defines to clean up the compiler.
> - Safari Fix: Implemented a Master Sprite Atlas to bundle UI icons, reducing web requests and improving iPhone load times.
> - Touch Input: Updated Interactable.cs and InputManager.cs to use IPointer events, making the world fully responsive to touch and taps.
> - Virtual Controls: Created a modern Virtual Joystick and Jump Button with custom branding for mobile movement.
> - Ergonomics: Refined the mobile UI layout by moving controls to the corners and scaling them for better visibility.
>
> 2. UI ARCHITECTURE AND LOGIC
> - Session Sync: Integrated mobile controls into the MainUI hierarchy so they stay hidden until the player actually logs in and enters the world.
> - Platform Toggle: Added logic to automatically hide mobile controls when playing on Desktop or in the Unity Editor.
> - Contextual HUD: Created an automated interaction button that only appears when a player is near a door, switch, or object.
>
> 3. NETWORKING AND ROBUSTNESS
> - Vivox Fix: Added a character sanitizer to strip illegal symbols (like brackets) from room names, preventing voice chat join failures.
> - NGO Sync: Verified and refined Netcode for GameObjects synchronization for doors and light switches.
>
> 4. BRANDING AND HYGIENE
> - Professional Look: Added custom MetaDyn branded headers to all core SDK components in the Inspector.
> - Compiler Cleanup: Standardized the WebGL build profile to be 100 percent UGS-native.

## Product Interpretation

The most important interpretation is that MetaDyn is no longer merely “migrating away from Fusion” in the active Starter path.

The platform has started to behave like:
- a UGS-native SDK baseline
- a WebGL/mobile-capable social runtime
- a creator-facing product with stronger internal coherence

This is a better state than simply saying “UGS works.”

## What This Unlocks Next

With the active migration work completed, the next highest-leverage work likely shifts toward:
- editor validation and readiness checks for UGS project setup
- runtime/deployment config hardening so spaces join the intended sessions consistently
- clearer SDK manifest/dashboard reporting for installed UGS package versions and services readiness
- creator-facing documentation of the new baseline and prefab/runtime requirements
- further mobile browser smoke tests and load/performance verification on real devices
- larger room/load testing as confidence grows

## Documentation Impact

This sprint changes several assumptions that older Unity docs may still state incorrectly.

Docs should now treat the following as the live direction unless a project explicitly says otherwise:
- active networking baseline: **UGS/NGO**
- active production voice/text direction for the UGS path: **Vivox**
- primary delivery target remains **WebGL**
- mobile browser support is now part of the practical runtime surface, not a distant future concern
- Photon/Fusion should be discussed as legacy/reference context for the migrated branch, not as the declared active baseline

## Strategic Meaning

This sprint is notable not just for implementation volume but because it tightens the bridge between:
- Jen as orchestration/strategy layer
- Jen as Unity-side implementation collaborator
- MetaDyn as a coherent cross-surface product platform

That kind of identity/runtime continuity matters for the broader MetaDyn vision, because the assistant is not only advising about the platform from outside it, but increasingly participating inside the same product surface.
