# MetaDyn Avatar Normalization Pipeline

## Purpose

Define how MetaDyn should transform uploaded or provider-sourced avatars into one consistent runtime shape for Pavilion.

This is the processing pipeline that sits between:

- avatar source
- validation
- final in-world runtime usage

## Core Principle

MetaDyn should not let raw avatar files directly become runtime player avatars.

Everything should pass through a normalization pipeline so the output conforms to a single runtime contract.

## Input Sources

The normalization pipeline must support:

- provider avatars
 - Avaturn
 - Avatar SDK
 - Genies
- direct BYOA uploads
 - VRM
 - GLB
 - later FBX

## Pipeline Stages

## Stage 0: Intake

Input:

- uploaded file or provider payload

Output:

- intake record with source metadata

Tasks:

- assign upload/import job ID
- record source type
- record user ID / provider ID
- store original file safely

## Stage 1: Parse and Inspect

Tasks:

- parse avatar file
- inspect skeleton
- inspect meshes
- inspect materials
- inspect textures
- inspect blendshapes
- inspect animation compatibility signals

Output:

- raw inspection report

## Stage 2: Validate Against MetaDyn Avatar Spec

Tasks:

- apply upload spec rules
- compute budget metrics
- determine humanoid compatibility
- determine face support tier
- detect shader/material issues

Output:

- validation result:
 - pass
 - pass with warnings
 - reject

If reject:

- stop pipeline
- return clear user-facing reasons

## Stage 3: Skeleton Normalization

Goal:

- convert accepted avatars into a standard humanoid runtime contract

Tasks:

- resolve root transform
- normalize orientation
- normalize scale
- generate or map humanoid avatar definition
- map required bones to MetaDyn expected semantics

Target contract:

- root
- hips
- spine
- chest
- neck
- head
- upper/lower arms
- hands
- upper/lower legs
- feet

Output:

- normalized skeleton contract

## Stage 4: Mesh and Material Normalization

Tasks:

- merge or split meshes only when needed
- reduce excessive material count
- remap unsupported shaders
- compress textures
- enforce alpha/material policies
- generate approved material instances

Goals:

- predictable URP rendering
- acceptable WebGL performance
- avoid custom unsupported shader breakage

Output:

- normalized mesh and material bundle

## Stage 5: Face and Lip Sync Classification

Tasks:

- identify blink channels
- identify mouth/jaw channels
- detect visemes if present
- remap known blendshape aliases to MetaDyn face map

Face capability outputs:

- `full`
- `basic`
- `none`

Fallback rules:

- `full`: use advanced lip sync adapter
- `basic`: use mouth-open or jaw-open fallback
- `none`: allow no facial animation or reject based on policy

## Stage 6: Attachment Point Derivation

Tasks:

- derive stable anchor points for:
 - head
 - left hand
 - right hand
 - chest
 - root

Reason:

- needed for camera behavior
- needed for interaction systems
- needed for future wearables and props

## Stage 7: Runtime Packaging

Tasks:

- write normalized asset bundle or equivalent runtime-ready output
- write descriptor metadata
- associate with user profile
- cache preview thumbnail if needed

Output:

- normalized avatar package
- runtime descriptor

## Stage 8: Runtime Binding in Pavilion

Tasks:

- attach normalized avatar to MetaDyn player runtime
- bind animator
- bind camera offset logic
- bind voice/lip-sync adapter
- bind name tag anchor rules

Outcome:

- all accepted avatars look different, but behave consistently in the platform

## Runtime Contract Output

Every normalized avatar should expose the same minimum contract:

- avatar root transform
- humanoid Animator / Avatar mapping
- movement-compatible skeleton
- face support tier
- head anchor
- hand anchors
- bounds / height metrics
- metadata flags

## Auto-Fix Boundaries

## Good Candidates For Automation

- scale correction
- orientation correction
- root offset normalization
- material conversion
- texture compression
- blendshape alias mapping
- humanoid remapping when deterministic

## Poor Candidates For Automation

- complete auto-rigging of raw mesh
- manual-quality skin weight repair
- creation of missing visemes from nothing
- repair of severely malformed skeletons

Those should become:

- rejection reasons
- or later premium/manual pipeline steps

## Processing Modes

## Mode A: Synchronous Validation

Use for:

- quick file acceptance checks

Tasks:

- parse
- validate
- generate immediate user report

## Mode B: Asynchronous Normalization Job

Use for:

- accepted avatars that need pipeline work

Tasks:

- full normalization
- packaging
- final publishing to profile

This is the better default architecture.

## Failure Modes

The pipeline should report failures by category:

- invalid file
- unsupported format
- non-humanoid
- rig failure
- budget exceeded
- material unsupported
- facial support missing
- runtime packaging error

User feedback should be specific, not generic.

## Recommended First Version

For the first shippable MetaDyn BYOA pipeline:

- accept `VRM` and `GLB`
- support humanoid only
- produce:
 - standard player locomotion
 - camera compatibility
 - basic name tag support
 - basic or full lip sync depending on face support
- reject heavy or malformed assets early

## Why This Pipeline Matters

Without normalization:

- every avatar source becomes a special case
- player controller compatibility becomes fragile
- networking and remote reconstruction become inconsistent
- voice/lip sync integration becomes vendor-specific

With normalization:

- MetaDyn owns the runtime rules
- providers become inputs, not dependencies
- BYOA remains open but controlled
