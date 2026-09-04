# Pavilion

## Project snapshot

**Project:** Pavilion  
**Type:** Core platform / immersive space runtime  
**Status:** Active

## Why it matters

Pavilion is one of the most important active MetaDyn project surfaces and appears to be the real runtime context for near-term implementation work.

## Current known context

- Pavilion is the real environment that should receive avatar-related implementation work rather than a fake isolated sandbox.
- Current avatar direction is no longer "stay prefab-based forever."
- The practical platform direction is:
  - validated user-uploaded `VRM`
  - validated user-uploaded `GLB`
  - normalization against a MetaDyn-controlled avatar spec
  - binding accepted avatars onto a MetaDyn-owned player runtime
- Uploaded avatar visuals should not replace the main player/network prefab/runtime.
- Prefab avatar families are the current / legacy reality, but not the desired long-term architecture.

## Active threads

- Avatar uploader prototype
- Runtime binder / canonical player runtime ownership
- Validation limits and acceptance rules for uploaded avatars
- Integration sequence inside the real Pavilion runtime
- Identity / profile continuity implications for avatar persistence later

## Key decisions

- Build and test the uploader path against the actual repo/runtime that will receive the merge.
- Prefer branch-based implementation in the real system rather than proving things only in an isolated starter clone.
- Keep the canonical player runtime owned by MetaDyn; attach avatar visuals after validation.

## Open questions

- What is the smallest proof milestone for Pavilion avatar uploads?
- Which exact runtime hooks need to be touched first?
- What should the first validator enforce versus defer?
- What should persistence look like after local binding works?

## Next actions

- Turn the avatar strategy into an implementation checklist.
- Define the smallest real uploader + local bind milestone.
- Capture exact runtime integration points once code work begins.

## Related docs

- `../../planning/metadyn-avatar-strategy-2026-04-06.md`
- `../../planning/metadyn-vrm-and-glb-upload-implementation-guide-2026-04-06.md`
- `../../planning/metadyn-byoa-architecture-plan-2026-04-06.md`
