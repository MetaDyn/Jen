# MetaDyn Browser Companion - Planning Draft

**Status:** Planning
**Date:** 2026-03-16
**Purpose:** Define a lightweight browser extension that can support MetaDyn authentication continuity, browser-to-platform context bridging, and future agent/presence capabilities.

---

## 1. Summary

MetaDyn should explore a very lightweight browser companion, initially targeting Chrome-compatible browsers, that can:

1. help bridge authentication/session continuity
2. act as a lightweight browser-side agent companion
3. eventually report useful metaverse context back into the broader MetaDyn/OpenClaw system
4. support user-controlled sharing of current location/context within the metaverse

This is best framed as a **MetaDyn Browser Companion**, not merely an auth plugin.

---

## 2. Why This Makes Sense

The current MetaDyn auth model is already browser-centric:

- login starts in `dashboard.metadyn.xyz`
- Supabase is the identity backend
- continuity between dashboard and immersive spaces is handled via the shared `metadyn_token` cookie on `.metadyn.xyz`
- Unity WebGL spaces consume that browser session rather than owning login directly

A browser companion sits in a natural position to:

- observe MetaDyn dashboard and space contexts
- help maintain coherent session behavior
- detect which MetaDyn surface the user is currently in
- eventually act as a bridge between browser context, immersive space state, and agent systems

---

## 3. Product Framing

### Recommended framing

**MetaDyn Browser Companion**

Not just:
- Chrome auth plugin
- cookie helper
- simple extension launcher

The broader framing leaves room for:
- auth/session assistance
- launch assistance
- presence publishing
- user-controlled location sharing
- lightweight agent behaviors
- dashboard ↔ immersive runtime ↔ orchestration bridging

---

## 4. Proposed Role in the Architecture

### Browser Companion
Acts as:
- browser-side observer
- session helper
- optional presence publisher
- user-consented sharing/control point

### Dashboard / Backend
Acts as:
- identity source
- permissions source
- preferences store
- presence/share broker

### Immersive Spaces
Act as:
- runtime source of truth for in-world context
- source of richer location metadata

### Jen / OpenClaw / Agent Layer
Acts as:
- orchestrator
- consumer of presence and context
- messaging/sharing assistant
- coordination layer across users, spaces, and systems

---

## 5. Phased Capability Model

## Phase 1 - Auth Helper

Keep this extremely lightweight.

Responsibilities:
- detect MetaDyn dashboard/session state
- assist launch flows into immersive spaces
- support redirect/login/session continuity
- optionally surface quick actions such as launching the dashboard or opening a MetaDyn space

Goals:
- no new identity silo
- no separate authentication stack
- no overreach into deeper presence logic yet

---

## Phase 2 - Presence Companion

Once basic auth/session continuity is solid, the extension can:

- detect when the user is inside a MetaDyn immersive space
- identify current surface and session context
- publish that presence to a trusted MetaDyn backend endpoint

Examples of data:
- user identity
- current space ID
- current domain/subdomain
- room/session ID
- public join URL
- optional location label

At this stage, the extension becomes a lightweight presence bridge.

---

## Phase 3 - Metaverse-Aware Agent Companion

Longer term, the browser companion can evolve into a metaverse-aware agent bridge that can:

- report where the user is in the metaverse
- expose what space/page/context they are currently in
- support user-controlled sharing with others
- provide "join me" or "meet me here" style flows
- relay browser/space context back into Jen/OpenClaw systems

This turns the extension into a meaningful platform differentiator rather than a narrow auth utility.

---

## 6. Authentication Strategy

### Core principle

The browser companion should **not** create a second auth system.

It should reuse the existing MetaDyn model:
- dashboard login remains canonical
- Supabase remains the identity backend
- browser session remains the continuity layer
- extension operates as a companion to that model

### Current MetaDyn auth model (canonical understanding)

1. User logs in on `dashboard.metadyn.xyz`
2. Dashboard authenticates against Supabase
3. Dashboard sets shared cookie:
   - `metadyn_token`
   - scoped to `.metadyn.xyz`
4. User launches a Unity WebGL immersive space
5. Space reads the token through the WebGL JS bridge
6. Unity validates token with Supabase
7. Unity fetches the user profile
8. Profile fields such as `avatar_index` are used for continuity
9. If token is missing, user is redirected to dashboard login with `?redirect=` return flow

### Implication for the extension

The extension should piggyback on this system rather than replace it.

Possible approach:
- dashboard login remains source of truth
- extension detects authenticated MetaDyn browser state
- if extension needs privileged backend communication, backend can issue a scoped extension/session token

---

## 7. Presence / Location Model

"Location in the metaverse" should be modeled in layers.

### Level 1 - Coarse presence
- on dashboard
- in Unity space
- in Hyperfy space
- offline

### Level 2 - Space presence
- space ID
- domain/subdomain
- room/session ID
- join URL

### Level 3 - In-world location
- coordinates
- zone/area name
- landmark
- timestamp

### Level 4 - Shareable social presence
- "In MetaDyn Pavilion"
- "In Main Hall"
- "Available to join"
- "Share exact location with team only"

### Recommendation

Human-readable location should be primary.

Examples:
- in Pavilion
- in Main Hall
- in Beta Test Space A
- available to join

Raw coordinates should be optional/internal rather than the primary sharing unit.

---

## 8. Privacy and Consent Principles

This system should be explicitly designed around user consent.

Recommended controls:
- share nothing
- share online/offline only
- share current space only
- share current area/room
- share exact position
- share only with selected audiences (team, friends, invited users)
- invisible mode / pause reporting

The system should feel empowering, not invasive.

---

## 9. Recommended Technical Shape for a Lightweight V1

### 1. Browser extension background/service worker
Responsibilities:
- auth/session awareness
- communication to backend
- tab/domain detection

### 2. Content scripts
Injected only on MetaDyn surfaces such as:
- `dashboard.metadyn.xyz`
- `*.metadyn.xyz` immersive spaces

Responsibilities:
- read safe page context
- observe stable MetaDyn browser events/contracts
- report context upward to the extension runtime

### 3. Popup UI
Used for:
- signed-in status
- current MetaDyn context
- simple share toggle/status
- launch/open dashboard
- copy join link or similar quick actions

### 4. Backend endpoint(s)
Used for:
- registering extension session
- presence updates
- retrieving preferences
- issuing scoped extension/session tokens if needed

---

## 10. How the Extension Should Learn Metaverse Context

There are two main patterns.

### Option A - Read existing browser/page state
Examples:
- URL/subdomain
- DOM markers
- JS globals
- local/session storage
- app-emitted events if already present

**Pros**
- fast to prototype
- minimal initial platform work

**Cons**
- brittle
- tied to frontend internals
- weak long-term contract

### Option B - Formal MetaDyn Presence Bridge
Immersive spaces explicitly publish a stable browser-facing contract with data such as:
- current space ID
- room ID
- location label
- coordinates
- joinability
- sharing flags

Possible implementation forms:
- `window.postMessage(...)`
- custom DOM events
- small JS bridge object

**Pros**
- clean
- durable
- versionable
- consistent across Unity and Hyperfy if standardized

**Cons**
- requires deliberate implementation

### Recommendation

Use Option B as the real architecture.

The extension should consume a formal, versioned MetaDyn presence contract instead of relying on scraping.

---

## 11. Relationship to Hyperfy / Unified SSO

Current production understanding:
- Unity + dashboard auth continuity is implemented today
- Hyperfy unified SSO is still planned rather than the current production path

Planned future direction:
- same dashboard/Supabase identity source
- same shared `.metadyn.xyz` cookie
- server-side exchange to mint a short-lived Hyperfy/world token
- preserve canonical Supabase user UUID across dashboard, Unity, and Hyperfy

This means the browser companion should be designed to work with that future model, but it should not assume Hyperfy parity already exists.

---

## 12. Strong Initial V1 Scope Recommendation

Keep the first version intentionally narrow.

### Suggested V1
- Chrome-compatible extension for MetaDyn domains
- detect signed-in MetaDyn state
- show current dashboard/space context
- consume a minimal stable "current space" payload if available
- optionally send presence heartbeat to MetaDyn backend
- support simple share states:
  - not sharing
  - share current space
  - share join link

### What V1 should avoid
- heavy browser automation
- deep in-world control logic
- full coordinate sharing by default
- separate auth model
- scraping-heavy architecture as the long-term solution

---

## 13. Strategic Upside

If done well, this becomes more than a utility extension.

It could eventually support:
- user presence awareness across MetaDyn surfaces
- easy invite and coordination flows
- contextual agent assistance
- continuity between dashboard, immersive runtime, and orchestration systems
- differentiated social and operational tooling around place, presence, and identity

This aligns strongly with MetaDyn's broader platform vision.

---

## 14. Recommended Next Steps

1. Write a lightweight product/architecture spec for the MetaDyn Browser Companion
2. Define the first version of the MetaDyn Presence Bridge contract
3. Decide the minimum V1 scope and privacy defaults
4. Define how Jen/OpenClaw should consume presence data from the system
5. Only then begin implementation

---

## 15. Practical Working Recommendation

Short version:
- yes, explore this
- frame it as a browser companion, not a narrow auth plugin
- keep dashboard/Supabase as canonical auth
- use a formal browser-facing presence contract from immersive spaces
- make privacy and share controls explicit from the beginning
- start with a narrow V1 and grow carefully
