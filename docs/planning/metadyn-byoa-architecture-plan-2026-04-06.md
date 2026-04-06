# MetaDyn BYOA Architecture Plan

## Purpose

Define the platform architecture for bring-your-own-avatar support in MetaDyn Pavilion and future MetaDyn spaces.

BYOA here means:

- users can bring avatars from supported providers
- users can upload avatars that conform to MetaDyn rules
- MetaDyn owns the runtime contract rather than any one avatar vendor

## Strategic Goal

Make avatars portable into MetaDyn without making MetaDyn dependent on:

- one avatar SaaS
- one creator pipeline
- one rigging vendor

## Architecture Overview

MetaDyn BYOA should be built around four layers:

1. source layer
2. validation and normalization layer
3. runtime avatar layer
4. profile and networking layer

## Layer 1: Source Layer

Supported avatar sources:

- provider-created avatars
 - Avaturn
 - Avatar SDK
 - Genies
 - future providers
- direct uploads
 - VRM
 - GLB
 - later FBX

This layer only handles acquisition.

It should not define runtime behavior.

## Layer 2: Validation and Normalization Layer

This is the core of the system.

Responsibilities:

- inspect incoming avatar assets
- validate against MetaDyn Avatar Spec
- auto-fix safe issues
- reject irrecoverable problems
- output a normalized runtime package

This layer makes BYOA feasible without chaos.

## Layer 3: Runtime Avatar Layer

The runtime layer should expose one platform-owned player contract regardless of avatar source.

Required output contract:

- avatar root
- humanoid animator mapping
- movement-compatible skeleton
- head and hand anchors
- face support tier
- voice/lip-sync adapter binding
- camera framing metadata

The player controller should never need to know whether an avatar came from:

- Avaturn
- Avatar SDK
- Genies
- direct upload

## Layer 4: Profile and Networking Layer

Profile data should store:

- active avatar ID
- source type
- source metadata
- normalized package reference
- preview image
- feature flags such as facial support tier

Networking data should transmit enough information for remote reconstruction:

- avatar descriptor ID
- runtime package reference
- source/provider type if needed for analytics/debugging

Remote peers should not depend on raw third-party login state to render another user.

## Recommended Runtime Model For Pavilion

Pavilion should migrate toward:

- one canonical MetaDyn network player prefab
- runtime-loaded avatar visuals

Instead of:

- many avatar-family-specific player prefabs

Reason:

- cheaper to maintain
- easier to support BYOA
- easier to support future providers
- simpler voice/lip-sync abstraction

## Proposed Systems

## Avatar Descriptor

Represents the normalized identity of an avatar.

Fields should include:

- `avatarId`
- `ownerUserId`
- `sourceType`
- `sourceFormat`
- `runtimeAssetRef`
- `thumbnailRef`
- `faceSupportTier`
- `humanoidStatus`
- `warnings`

## Avatar Source Adapter

One adapter per source family.

Examples:

- `AvaturnSourceAdapter`
- `AvatarSdkSourceAdapter`
- `GeniesSourceAdapter`
- `DirectUploadSourceAdapter`

Responsibilities:

- import/acquire source asset
- produce raw intake payload for the normalization pipeline

## Avatar Normalizer

Responsibilities:

- apply upload spec
- run normalization stages
- publish normalized runtime package

## Runtime Avatar Binder

Responsibilities:

- load normalized avatar package
- attach to player root
- bind animator
- provide anchors
- connect lip sync adapter

## Face Adapter

Responsibilities:

- hide source-specific blendshape differences
- expose a unified interface for:
 - blink
 - mouth open
 - viseme playback
 - speaking start/stop

## Provider Independence Rule

MetaDyn should enforce this rule:

- source systems may create or supply avatars
- only normalized MetaDyn runtime packages may be used in production runtime

This prevents vendor logic from bleeding into core gameplay.

## Upload and Publish Flow

Recommended flow:

1. user chooses source:
 - provider
 - upload
2. source adapter ingests avatar
3. validation runs
4. user receives report
5. accepted avatar enters normalization job
6. normalized runtime package is created
7. avatar is published to user profile
8. profile marks avatar as selectable/active
9. Pavilion loads normalized avatar at spawn

## Feature Tiers

## Tier 1: Provider + Normalized Runtime

Fastest path.

Supports:

- existing providers
- provider-created humanoid avatars
- lowest normalization complexity

## Tier 2: Open Upload

Supports:

- VRM and GLB uploads
- strict validation and normalization

## Tier 3: Advanced Creator Pipeline

Supports:

- creator diagnostics
- richer repair tools
- better facial feature remapping
- optional premium/manual pipeline

## Pavilion Migration Implications

Current Pavilion assumptions that should change:

- avatar choice should stop being only a prefab index
- lip sync should stop being hard-coded to current avatar families
- player prefab should stop being tightly coupled to avatar source

Target Pavilion direction:

- one player controller runtime
- one networking model
- many avatar sources
- one normalized avatar contract

## Best Initial Format Policy

Recommended initial policy:

- preferred: `VRM`
- accepted: `GLB`
- later or restricted: `FBX`

Reason:

- `VRM` is the cleanest BYOA format for humanoid avatars
- `GLB` is broadly useful and web-friendly
- `FBX` is common but high-maintenance

## Economic Advantage

This architecture matters because it reduces long-term costs.

Instead of paying a recurring premium provider fee forever, MetaDyn can:

- support provider avatars when useful
- allow direct user-controlled uploads
- keep platform ownership of runtime behavior

That is a better fit for a small open platform.

## Recommended Rollout

### Phase 1

- define and publish MetaDyn Avatar Spec
- build validation reports
- support provider avatars plus normalized runtime contract

### Phase 2

- support `VRM` and `GLB` uploads
- load normalized avatars in Pavilion

### Phase 3

- replace current multi-prefab avatar logic with runtime avatar binding
- fully abstract lip sync and face animation

### Phase 4

- improve creator UX
- moderation tools
- attachment/wearable extensions

## Recommended Immediate Next Step

Build the architecture around normalization first.

Do not start with:

- arbitrary upload UI
- provider-specific hacks
- custom one-off fixes for each avatar family

The spec and normalization layer are the foundation that make everything else maintainable.
