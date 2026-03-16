# Core Systems

## Multiplayer Foundation

### Player and Session Model
The imported documentation describes a multiplayer platform based on Photon Fusion, including:
- player spawning and joining
- room/session handling
- synchronized names and presence
- spawn point handling
- session-scale targets up to roughly 50 users depending on voice topology and bandwidth

### User Management and Moderation
Documented platform systems include:
- user list synchronization
- permission levels (`User`, `Moderator`, `Admin`)
- kick / ban / block moderation paths
- host-authoritative moderation checks
- first-player auto-admin fallback when a proper owner/admin identity is not yet available

### Synchronization Patterns
Imported decisions highlight several implementation patterns:
- render-based change detection for reliable user-list sync
- RPC-based registration into host-controlled systems
- object pooling for UI entries
- singleton-style managers for core runtime services

## Identity and Authentication

The platform docs describe a web-first auth model built around Supabase.

Capabilities documented in the imported material include:
- login / signup / session management
- token validation
- profile fetching
- avatar selection persistence
- cookie-based SSO across subdomains
- browser ↔ Unity bridging through WebGL JavaScript integration

This establishes identity continuity as a platform capability rather than a one-off space feature.

## Avatar System

Imported docs show the avatar system evolving from static avatar selection toward a scalable provider-based model.

Documented characteristics include:
- Ready Player Me support
- Avatar SDK support
- dynamic avatar lists
- thumbnail-based avatar selection UI
- persistent avatar choice
- WebGL timing considerations for UI initialization

The recorded architectural decision favors dual categorized avatar lists over fixed male/female fields, enabling scalability and better provider separation.

## Voice and Communication

### Player Voice
The Unity platform includes WebRTC-based player-to-player voice with:
- spatial audio
- WebGL-compatible browser implementation
- lip sync integration
- mesh-topology voice scaling assumptions up to current target ranges

### AI Voice
The imported docs also show a push-to-talk AI voice path, but broader AI documentation will be organized separately later.

For platform purposes, the main takeaway is that MetaDyn treats voice as a native experience layer, not an external add-on.

## SDK and Editor Systems

The platform includes a MetaDyn SDK layer that provides:
- reusable runtime components
- editor tooling
- deployment configuration surfaces
- runtime config handling
- component conventions for inspector-friendly world-building features

Imported docs describe a consistent SDK component pattern with:
- clear namespaces
- XML documentation
- inspector headers/tooltips
- public APIs
- inline editor visualization via `#if UNITY_EDITOR`

Example component areas documented in the imported reference include:
- entrance/spawn points
- seats
- emotes
- interactables
- triggers
- projection surfaces

## Documentation Discipline

One of the strongest aspects of the imported Unity platform material is that it was already highly documented while the platform was being built.

The imported `.claude` structure includes:
- startup summaries
- quick references
- changelog history
- architectural decisions
- planning docs
- specialized project skills

That documentation practice is important because it captures not only what the platform does, but why key decisions were made.
