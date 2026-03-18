# System Architecture

## Technical Baseline

Documented platform baseline from the imported material:
- Unity 6 (`6000.0.62f1`)
- URP 17.0.4
- Photon Fusion 2.0.9 Stable
- Shared Mode networking
- WebGL as primary target
- Native builds as secondary target
- Supabase for authentication/profile systems
- Cloudflare for DNS, SSL, proxying, and edge delivery
- WebRTC for player-to-player voice

## Architectural Model

The platform is built as a layered architecture.

### Experience Layer
Unity scenes, player interactions, social spaces, avatars, UI, and immersive world logic.

### Platform Layer
MetaDyn-owned runtime/editor/deployment systems that provide the reusable platform capabilities inside projects.

### Identity Layer
Supabase-backed authentication, profile loading, avatar persistence, cookie/session continuity, and Unity-side authorization boundaries.

A newly documented security priority is that authorization decisions inside Unity must not trust client-supplied identity fields as proof of identity. Owner/admin behavior should ultimately come from validated session state or signed backend claims rather than raw UUID comparison.

### Realtime Social Layer
Photon Fusion sessions, spawning, user list synchronization, permissions/moderation, and presence handling.

### Voice Layer
Two distinct communication paths are documented:
- AI push-to-talk voice flow
- player-to-player WebRTC voice flow

For the platform section, the most important part is that real-time player communication is a first-class system and WebGL-compatible.

### Hosting Layer
Cloudflare + origin hosting + per-space isolated deployment directories, with a trajectory toward shared-hosted and self-hosted delivery.

## Networking Model

### Photon Fusion Shared Mode
The platform intentionally uses Photon Fusion Shared Mode rather than a dedicated client-server authority model.

Reasons documented in imported decisions:
- social/metaverse use case over competitive gameplay
- easier iteration and development speed
- natural player authority over their own objects
- host authority retained for selected global systems such as moderation/user management

### Hybrid Authority Pattern
The platform uses a hybrid authority design:
- players control their own player objects
- host/state authority controls central systems like the user list and moderation actions
- registration into host-controlled systems occurs via RPC patterns

## Space Deployment Model

A central architectural rule appears repeatedly in the imported docs:

**Each space is its own build.**

That rule remains true whether the space is:
- self-hosted
- MetaDyn shared-hosted
- deployed under a subdomain or routed hostname

## Platform Direction

The Unity platform is not described as a one-off app. It is a reusable metaverse platform architecture that supports:
- branded or client spaces
- MetaDyn-owned spaces
- reusable SDK systems
- future dashboard/backend integration
- eventual broader cross-platform identity and presence workflows

## Important Architectural Reality

A key conclusion from the deeper import review is that MetaDyn is already thinking like a **multi-space platform**, but the implementation boundary between project code and platform code is still transitional.

In practice, the current platform spans both:
- `Assets/MetaDyn/**`
- several still-essential files outside that root, such as shared/common and Pavilion runtime files

That means the platform architecture is real, but the packaging boundary is not fully clean yet.

## Productization Gaps Visible From Architecture

The imported docs also make it clear that some platform-level architecture is more mature in concept than in final productized form.

Examples include:
- SDK extraction and packaging boundaries
- dashboard-versus-Unity source-of-truth rules
- rollback/versioned deployment model
- shared-hosting provisioning automation
- unified cross-runtime identity flows beyond current Unity-first implementation
