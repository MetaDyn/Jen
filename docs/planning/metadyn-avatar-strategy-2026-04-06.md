# MetaDyn Avatar Strategy 2026-04-06

## Current Strategic Position

MetaDyn currently has prefab-based avatar paths in Pavilion, but those paths should be treated as legacy or transitional rather than the long-term platform strategy.

The current prefab model does not cleanly fit MetaDyn's actual product direction because it creates unnecessary coupling between:

- avatar source
- player runtime
- multiplayer representation
- lip sync behavior
- long-term platform portability

## Canonical Direction

The practical avatar strategy for MetaDyn is:

- support user-uploaded `VRM`
- support user-uploaded `GLB`
- validate uploads against a MetaDyn-controlled avatar spec
- normalize accepted avatars into a MetaDyn-owned runtime contract
- bind normalized avatars onto a canonical MetaDyn player runtime

This is the strategy that best fits the Pavilion system and MetaDyn's broader platform goals.

## What This Means

### 1. Prefabs Are Not The Long-Term Architecture

Prefab avatars may remain useful for:

- current continuity
- testing
- fallback content
- short-term operational stability

But prefab families should not define the future avatar architecture for MetaDyn.

### 2. MetaDyn Should Own The Runtime Contract

MetaDyn should not let any one avatar vendor define how avatars behave in production.

Instead, MetaDyn should own:

- validation rules
- normalization rules
- player runtime expectations
- networking representation
- lip sync capability tiers
- avatar compatibility policy

### 3. Portable Formats Fit Better Than Vendor Lock-In

The most realistic near-term portable formats are:

- `VRM`
- `GLB`

These formats fit MetaDyn's needs better than rebuilding the system around another single avatar SaaS.

### 4. The Player Runtime Should Stay MetaDyn-Owned

Uploaded avatars should not replace the main player/network prefab.

Instead, MetaDyn should keep:

- one canonical player runtime
- one networking model
- one movement stack
- one camera and voice ownership model

Avatar visuals should attach to that runtime after validation and normalization.

## Strategic Rationale

This direction is stronger because it:

- works better with the existing system shape than trying to force a new prefab family
- reduces vendor dependency
- preserves WebGL-friendly flexibility
- supports future profile continuity
- creates a cleaner path to BYOA
- avoids turning current avatar stopgaps into permanent architecture

## Recommended Working Rule

For current planning and implementation decisions, use this rule:

- **legacy/current state:** prefab-based avatars exist
- **real platform direction:** validated `VRM` and `GLB` uploads bound to a MetaDyn-owned runtime

## Immediate Implication For Pavilion

When discussing avatar work in Pavilion, the default assumption should be:

- do not design around adding more prefab families unless there is a specific short-term reason
- do design toward upload validation, normalization, runtime binding, and provider-independent avatar support

## Related Docs

This strategy should be read together with:

- `docs/planning/metadyn-avatar-upload-spec-2026-04-06.md`
- `docs/planning/metadyn-avatar-normalization-pipeline-2026-04-06.md`
- `docs/planning/metadyn-byoa-architecture-plan-2026-04-06.md`
- `docs/planning/metadyn-vrm-and-glb-upload-implementation-guide-2026-04-06.md`
- `docs/planning/avatar-provider-replacement-options-2026-04-06.md`
- `docs/planning/genies-avatar-sdk-integration-plan-2026-04-06.md`
