# Unity 6 Auth & Identity

This document captures the current MetaDyn identity model for Unity 6 spaces, including the implemented web-first auth bridge, current persistence behavior, and the next integration steps toward broader platform continuity.

## Executive Summary

The current MetaDyn Unity auth model is **web-first, dashboard-led, and Supabase-backed**.

Today the canonical flow is:
- user authenticates on `dashboard.metadyn.xyz`
- dashboard writes a shared `metadyn_token` cookie on `.metadyn.xyz`
- Unity WebGL space reads that cookie through a browser bridge
- Unity validates the token with Supabase
- Unity fetches the user profile and persisted fields such as `avatar_index`
- the player enters the space with persistent identity context

This is not merely a convenience feature. It is the current bridge that makes MetaDyn feel like a platform rather than a disconnected set of scenes.

## Why This Model Matters

Moving auth out of in-Unity UI and into the dashboard creates several platform advantages:
- browser-native login UX
- compatibility with password managers
- easier future OAuth support
- faster world-entry flow for returning users
- cleaner session continuity across MetaDyn-owned subdomains
- a clearer path toward identity continuity across Unity and non-Unity surfaces

In other words, login is not a scene concern. It is a platform concern.

## Current Implemented Model

### Primary Components

Current documented Unity-side auth files:
- `Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs`
- `Assets/MetaDyn/Dashboard/SupabaseConfig.cs`
- `Assets/MetaDyn/Dashboard/WebAuthBridge.cs`
- `Assets/MetaDyn/Dashboard/LoginUI.cs`
- `Assets/Plugins/WebGL/AuthBridge.jslib`

### Current Browser / Dashboard Flow

The dashboard is the current login surface. After successful auth, it writes a cookie roughly like this:

```javascript
document.cookie = `metadyn_token=${token}; domain=.metadyn.xyz; path=/; samesite=lax; secure; max-age=3600`;
```

That makes the session token readable by MetaDyn subdomains such as dashboard and Unity space hosts under `*.metadyn.xyz`.

### Current Unity WebGL Flow

At runtime, Unity uses `WebAuthBridge` and `AuthBridge.jslib` to:
- read the shared cookie
- optionally fall back to local storage in same-origin cases
- redirect to dashboard login if no valid token exists
- clear the token on logout

The bridge is intentionally lightweight. Browser-specific auth handling stays in `.jslib`, while Unity consumes it through a narrow C# wrapper.

## Canonical Login Flows

### First-Time User

1. User opens a Unity WebGL space.
2. No valid `metadyn_token` is found.
3. The space redirects to `dashboard.metadyn.xyz/login?redirect={space_url}`.
4. User signs up or logs in.
5. Dashboard writes the shared cookie.
6. Dashboard redirects back to the Unity space.
7. Unity validates the token with Supabase.
8. Unity fetches the profile.
9. If `avatar_index` is unset, the user selects an avatar.
10. The profile is updated and the user enters the world.

### Returning User

1. User opens a Unity WebGL space.
2. Unity finds the shared cookie.
3. Unity validates the token with Supabase.
4. Unity fetches the profile.
5. Persisted identity fields such as avatar selection are restored.
6. User enters the space without repeating login or setup.

## Identity Data Model

### Current Canonical Identity Backend

Supabase is the current source of truth for:
- authentication
- canonical user ID
- profile persistence
- avatar selection persistence
- dashboard-linked identity continuity

### Current Profile Shape

Documented important fields include:
- `id` — canonical user UUID
- `name` — display name
- `avatar_url` — profile image or linked avatar metadata
- `avatar_index` — stored avatar choice for Unity spawning

The currently important practical field for Unity continuity is `avatar_index`.

### Current Unity Use Of Profile Data

Unity currently uses the fetched profile to restore:
- display identity
- avatar choice / avatar continuity
- spawn-time user context

That means current auth is already more than access control. It is the start of persistent presence.

## Auth Modes

The imported platform docs describe three modes:

### 1. Guest Mode
- authentication not required
- user can enter without dashboard login
- useful for testing or deliberately open spaces

### 2. Web-First Mode
- primary production path
- token read from browser cookie
- redirects to dashboard when needed
- most aligned with MetaDyn platform direction

### 3. Manual Login Mode
- fallback path for editor use or non-web-first scenarios
- `LoginUI.cs` provides direct email/password login
- useful for testing when the full browser-cookie flow is unavailable

## Domain Architecture

The current model assumes MetaDyn-controlled surfaces under the same root domain.

Typical shape:
- `dashboard.metadyn.xyz` — login, profile, spaces, account surfaces
- Unity space hosts under `*.metadyn.xyz`
- shared cookie on `.metadyn.xyz`

This same-root-domain model is what makes the current cookie-based SSO workable without a more complex brokered handoff.

## Current Strengths

### Web-Native UX
Login happens where browsers are strongest: forms, redirects, cookies, and future OAuth.

### Reduced Friction For Returning Users
Returning users should not need to repeatedly authenticate or re-select avatars when moving between MetaDyn-controlled spaces.

### Canonical User ID
The Supabase user UUID provides a real platform identity anchor rather than scene-local naming or ad hoc guest state.

### Platform Fit
This model supports MetaDyn’s broader positioning as a connected digital fabric rather than a collection of isolated WebGL builds.

## Important Current Constraints

### Subdomain Assumption
The shared-cookie model works naturally for `*.metadyn.xyz`. It does not automatically generalize to unrelated root domains.

### Token Lifetime / Session Semantics
The imported docs describe a `max-age=3600` cookie pattern. Session refresh and long-lived continuity details need to remain aligned between dashboard and Unity behavior.

### Unity Is Not Yet The Whole Platform Story
Unity auth continuity is comparatively coherent today, but broader identity continuity across every runtime is still an ongoing platform integration effort.

## Hyperfy Continuity Direction

Older planning docs treated unified login across dashboard, Unity, and Hyperfy as a future stage. Current reality is ahead of that in one important way: per long-term memory, Hyperfy unified login is already working.

The next integration step should therefore be understood as:
- preserving the same user identity across surfaces
- carrying persisted profile fields more completely
- ensuring username, avatar, and related user data remain coherent across dashboard, Unity, and Hyperfy

That is the more accurate current framing than “auth is not yet unified.”

## Custom Domain Implication

The current cookie model depends on `.metadyn.xyz`. If a space is served from a customer-owned domain, that space cannot read the MetaDyn root-domain cookie directly.

That creates a future requirement for a more explicit auth handoff, likely dashboard-mediated, when custom domains become a standard product feature.

## Security And Operational Notes

### What Is Good About The Current Model
- avoids exposing service-role credentials to the Unity client
- keeps login on the dashboard instead of in a game-style UI flow
- uses the browser’s native session and redirect mechanisms

### What Still Needs Discipline
- token storage and refresh semantics must remain consistent between dashboard and Unity
- logout must clear session state cleanly across surfaces
- editor-side developer auth must remain distinct from runtime end-user auth

## Recommended Documentation Position

The Unity auth story should be documented as:
- **implemented and real** for dashboard-to-Unity continuity
- **platform-critical**, not a side subsystem
- **not yet the end-state** for every domain and runtime edge case

That balance matters. The docs should not undersell what is working, and they should not overstate what is fully generalized.

## Key Open Questions

1. Which profile fields beyond `avatar_index` should be treated as required cross-surface continuity data?
2. What is the canonical handoff for custom domains that cannot read `.metadyn.xyz` cookies?
3. How should session refresh and expiry be handled across dashboard, Unity, and other runtimes?
4. Which identity fields are owned by dashboard/backend versus authored or overridden locally in Unity?
5. What is the explicit logout/session-clearing contract across all MetaDyn surfaces?

## Recommended Next Documentation Moves

1. Keep this document as the Unity identity source of truth.
2. Cross-link it from deployment docs whenever subdomain or custom-domain hosting is discussed.
3. Cross-link it from multiplayer/social docs because profile identity and presence are tightly coupled.
4. Add a future dedicated cross-runtime identity document once Unity and Hyperfy profile continuity is fully specified.

## Source Basis

Primary imported sources used in this synthesis:
- `import/unity6-docs/.claude/Quick Reference/AUTH_SYSTEM.md`
- `import/unity6-docs/.claude/Planning/Dashboard_Unity_Hyperfy_Flows.md`
- `import/unity6-docs/.claude/Planning/MetaDyn_Platform_PRD_v1.0.md`
- workspace `MEMORY.md` for current platform reality around Unity ↔ Hyperfy continuity
