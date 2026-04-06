# MetaDyn Avatar Upload Spec

## Purpose

Define the upload contract for bring-your-own-avatar support in MetaDyn so user-submitted avatars can be:

- validated
- normalized
- safely used in Pavilion
- kept compatible with movement, emotes, voice, and networking

This is the canonical spec for BYOA acceptance rules.

## Goals

- keep MetaDyn open to user-provided avatars
- avoid permanent lock-in to an expensive avatar SaaS
- preserve a consistent in-world runtime contract
- reject broken or dangerous uploads early
- auto-fix only what is safe and deterministic

## Non-Goals

- accept every arbitrary 3D character file
- fully auto-rig raw meshes with no usable skeleton
- guarantee facial animation for every upload
- support unlimited asset complexity

## Recommended Supported Input Formats

### Tier 1

- `VRM`
- `GLB` / `glTF 2.0`

Reason:

- best fit for web delivery
- cleaner runtime import story
- more consistent avatar-oriented metadata
- easier to validate than general FBX pipelines

### Tier 2

- `FBX`

Reason:

- common creator format
- useful for advanced users and migration cases

Constraint:

- should initially be limited or admin-gated until the normalization pipeline is mature

## Upload Modes

### Mode A: Provider Avatar

Source:

- Avaturn
- Avatar SDK
- Genies
- future providers

Behavior:

- provider-specific import path
- provider metadata attached
- still normalized to MetaDyn runtime contract

### Mode B: BYOA File Upload

Source:

- direct user upload of `VRM`, `GLB`, or eventually `FBX`

Behavior:

- validate against MetaDyn Avatar Spec
- auto-fix safe issues
- reject irrecoverable issues

## Acceptance Rules

An uploaded avatar must pass these categories to be considered acceptable.

## 1. File Integrity

Required:

- readable file
- supported file extension
- valid parse with no fatal importer error
- no missing required mesh or skeleton data

Reject if:

- parse fails
- file is corrupt
- embedded data is malformed beyond repair

## 2. Humanoid Compatibility

Required:

- humanoid or clearly humanoid-compatible skeleton
- valid root
- recognizable head, spine, arm, and leg chain

Preferred:

- Unity Humanoid Avatar can be generated

Accept if:

- exact bone names differ but skeleton can be mapped deterministically

Reject if:

- creature/non-humanoid topology
- no workable armature
- extreme skeleton ambiguity

## 3. Transform and Orientation

Required normalized outcome:

- forward-facing orientation
- upright avatar
- stable root transform
- predictable world scale

Auto-fix allowed:

- rotation
- scale normalization
- root offset correction

## 4. Geometry Budgets

Initial recommended budgets for WebGL:

- triangles:
 - target: under `70k`
 - soft limit: `100k`
- skinned meshes:
 - target: `1-6`
- materials:
 - target: under `8`
- texture resolution:
 - target max: `2048`
 - preferred: `1024`

Reject or warn if:

- excessive triangle count
- too many materials/draw calls
- oversized textures

## 5. Materials and Shaders

Allowed runtime target:

- MetaDyn-approved URP-compatible shaders only

Auto-fix allowed:

- remap unsupported shaders to approved URP shader set
- compress textures
- convert transparent settings where deterministic

Reject if:

- material graph relies on unsupported custom shader logic that cannot be normalized

## 6. Skinning Quality

Required:

- mesh must be skinned to a usable skeleton
- weights must not be catastrophically broken

Reject if:

- mesh is unrigged
- weights explode under validation
- skeleton and skinned mesh bindings are invalid

Important:

- MetaDyn should not promise universal full auto-rigging for arbitrary uploads in the first BYOA version

## 7. Face / Lip Sync Capability

Support tiers:

### Tier A: Full Face Compatible

Has:

- visemes or known mouth blendshapes
- eye blink support
- usable face mesh references

### Tier B: Basic Mouth Animation Compatible

Has:

- at least one open-mouth or jaw-open compatible channel

### Tier C: No Facial Support

Has:

- no usable face animation channels

Policy:

- Tier A and Tier B may be accepted
- Tier C may still be accepted if MetaDyn allows “no lip sync” fallback avatars

Reject only if:

- product policy requires speaking avatars for all users

## 8. Animation Compatibility

Required:

- compatible with MetaDyn locomotion and idle animation set after humanoid retargeting

Preferred:

- clean humanoid retargeting in Unity

Reject if:

- retargeting fails completely
- avatar proportions or armature break core locomotion

## 9. Safety / Content Validation

Required:

- file size limits
- extension whitelist
- content scan hooks if upload reaches backend storage
- metadata scrub as needed

Recommended:

- NSFW moderation pipeline
- blocked content categories
- manual moderation override tools

## Spec Tiers

## Tier 1: Fully Supported Avatar

Passes:

- humanoid
- budget
- materials
- locomotion
- basic or full face animation

Outcome:

- accepted
- full Pavilion compatibility target

## Tier 2: Supported With Reduced Features

Passes:

- humanoid
- budgets close enough
- movement compatible

But:

- limited face animation
- material downgraded
- minor compromises

Outcome:

- accepted with fallback flags

## Tier 3: Rejected

Fails:

- humanoid mapping
- file integrity
- rig validity
- performance budget by large margin
- unsafe unsupported material complexity

Outcome:

- rejected with a clear validation report

## Auto-Fix Policy

## Safe Auto-Fixes

MetaDyn may automatically:

- normalize scale
- normalize facing direction
- remap materials to supported URP shaders
- resize/compress textures
- merge obvious duplicate materials
- map common blendshape aliases
- generate/import a Unity humanoid avatar mapping if deterministic

## Unsafe Auto-Fixes

MetaDyn should not promise to automatically:

- rig a completely unrigged character
- repair bad topology
- reconstruct missing facial blendshapes
- fix severely broken skin weights
- make a non-humanoid character work as a humanoid avatar

## Metadata Produced After Acceptance

Accepted avatars should produce a normalized descriptor containing:

- avatar ID
- source type
- original upload format
- normalized runtime asset location
- humanoid status
- face support tier
- performance metrics
- attachment point metadata
- import warnings

## Recommended Product Rule

User-facing messaging should say:

- “Upload avatars that meet the MetaDyn Avatar Spec”
- not “upload any model”

That keeps the platform open while still enforceable.

## Recommended Initial Rollout

### Version 1

- `VRM` and `GLB` only
- humanoid only
- strict budgets
- accept basic facial fallbacks

### Version 2

- selected `FBX` support
- better blendshape remapping
- improved material conversion

### Version 3

- optional assisted repair tooling
- richer moderation/reporting
- creator diagnostics before final upload
