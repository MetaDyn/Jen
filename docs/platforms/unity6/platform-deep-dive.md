# Platform Deep Dive

## Executive Read

After a deeper pass across the imported Quick Reference, Planning, changelog, and decision materials, MetaDyn is best understood as a **WebGL-first multi-space metaverse platform** built around Unity 6.

At its core, the platform combines:
- Unity 6 as the runtime delivery layer
- Photon Fusion Shared Mode for multiplayer/presence
- Supabase for identity, profile, and platform data
- Cloudflare + nginx for edge delivery and routing
- WebRTC for player voice
- a reusable MetaDyn SDK/platform layer
- a dashboard-first control-plane direction

The imported docs make clear that MetaDyn is no longer just a single world or app. It is evolving into infrastructure for many spaces, with deployment, identity, hosting, and platform services treated as core product concerns.

## Full Platform Model

A coherent picture emerges from the imported material:

### 1. SDK Layer
A reusable Unity platform layer containing runtime systems, editor tooling, deployment surfaces, WebGL bridges, auth integration, and major platform capabilities.

### 2. Space Layer
Each space/world is its own build, but carries shared platform systems.

### 3. Hosted Platform Layer
A managed or self-hosted deployment/runtime layer providing routing, identity continuity, delivery, and future platform operations.

### 4. Dashboard / Control Plane Direction
The dashboard is increasingly intended to become the control plane for:
- login/auth bootstrap
- profile/space metadata
- deployment initiation
- future infra/config ownership
- future deployment history/version visibility

## Strongest Mature Areas

From the imported docs, the areas that appear most mature or concretely implemented are:
- core Unity runtime systems
- multiplayer/social presence foundations
- web-first Supabase auth flow for Unity WebGL
- AI embodiment foundations
- current editor-driven deployment workflow
- Cloudflare-backed WebGL hosting path
- avatar selection and voice/lip-sync integration

## Biggest Platform Gaps

The most important unresolved platform/product gaps visible in the imported docs are:

### SDK Packaging Boundary
The SDK is conceptually real, but still physically spans code both inside and outside `Assets/MetaDyn`.

### Shared Hosting Productization
The hosting vision is strong, but platform-scale provisioning automation is still evolving.

### Dashboard vs Unity Authority
The final source-of-truth split between Unity-authored settings and dashboard/backend-owned settings is not yet fully defined.

### Release / Rollback Model
Versioned deployment releases, rollback, manifest discipline, and deployment history are clearly intended, but not yet fully realized.

### Cross-Runtime Identity Completion
Unity auth is comparatively coherent today, while broader unified identity across additional runtimes like Hyperfy is still more architectural direction than completed system.

### Unity Authorization Hardening
A newly elevated gap is not just cross-runtime identity completion, but Unity-side trust-boundary hardening. The current review indicates that client-supplied UUID values may still influence authorization-sensitive behavior in ways that are too trusting. That shifts identity hardening from a future cleanup concern into an active priority fix track.

### Realistic Scale Boundaries
Some maturity claims are more optimistic than the underlying topology fully guarantees, especially around WebRTC mesh scaling and platform-wide production readiness.

## Core Strategic Takeaways

### MetaDyn Is a Platform, Not Just a Project
The docs repeatedly describe MetaDyn as a deployable platform with reusable systems, not just a single branded Unity world.

### Deployment Is a Product Feature
Deployment is not treated as an afterthought. It is intended to be part of the creator experience.

### Identity Is Central
Supabase-backed web-first auth, avatar persistence, and shared-domain continuity are treated as platform primitives.

### Embodied Presence Is Differentiating
Even though AI docs will be organized separately later, the imported corpus makes clear that avatars, embodiment, voice, and persistent presence are central to MetaDyn's strategic identity.

### Multi-Runtime Future Is Implied
The planning set points beyond Unity-only delivery toward a broader metaverse platform where Unity and Hyperfy can eventually operate under one identity/deployment/control model.

## Recommended Documentation Direction

Based on the deeper read, the next best documentation refinements are:
- split identity/auth into a dedicated Unity-platform document
- split multiplayer/social/moderation into its own document
- split SDK/tooling/update boundaries into its own document
- split voice/realtime communications into its own document
- capture known productization gaps explicitly so docs do not overstate maturity
