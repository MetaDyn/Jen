# Unity 6 Security Priority Fixes

This document captures the current highest-priority Unity auth and identity trust issues discovered during review, the most plausible exploit path, and the recommended remediation sequence.

## Executive Summary

The most serious current issue is **not necessarily full Supabase account compromise**.

The more immediate and plausible weakness is that parts of the Unity runtime currently treat **client-supplied identity values as if they were proof of identity**.

That creates a dangerous gap between:
- authenticated identity
- public user identifiers
- display metadata

Those concepts are not consistently separated today.

## Current Risk Assessment

### Most Likely Result Of The Current Weakness

If the currently documented code paths behave as reviewed:
- a tester may be able to appear as another user inside Unity
- a tester may be able to trigger owner/admin behavior if they know the owner UUID
- this may happen **without actually logging into the dashboard as that user**

### Less Certain From Unity Code Alone

The Unity-side findings do **not by themselves** establish:
- full dashboard account takeover
- full Supabase account compromise
- token theft as the primary exploit path in this specific issue

Those more serious outcomes would more likely require:
- token theft
- browser compromise
- XSS or another trusted-subdomain compromise

## Highest-Priority Confirmed Weak Point

## 1. Client-Supplied UUID Is Trusted For Permissions

### Current Reviewed Flow

- `Assets/Pavilion/Scripts/Player.cs`
  - `RPC_RegisterWithUserList(string playerName, string userId)` forwards `userId` from the client path
- `Assets/MetaDyn/UserList/UserListManager.cs`
  - `RegisterPlayer(PlayerRef playerRef, string playerName, string userId)` compares `userId` to `MetaDynRuntimeConfig.ownerId`
  - if they match, the user is granted admin

### Why This Is Critical

A raw UUID is being treated as if it proves identity.

That is the core trust failure.
If an attacker can provide the owner UUID, they may be able to gain owner/admin rights inside the Unity space even without authenticating as that real owner.

### Impact

- plausible in-world impersonation
- plausible owner/admin escalation
- authorization decisions made from unverified client data

This is the **top-priority remediation item**.

## Additional Confirmed Weak Points

## 2. Profile Fetch API Shape Allows Arbitrary `userId` Lookup

### Current Reviewed Flow

- `Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs`
  - `FetchProfile(string userId, ...)`
  - performs `GET /rest/v1/profiles?id=eq.{userId}&select=*`

### Why This Is Weak

Even if current calling code uses it correctly today, the API surface itself is wrong for bootstrap identity.
It models identity bootstrap as:
- “fetch the profile for UUID X”

instead of:
- “fetch the profile for the currently authenticated session user”

### Risk

If Supabase RLS is permissive, this shape may enable:
- profile disclosure
- misuse by future code paths
- profile impersonation behavior

Even with correct RLS, it is still the wrong trust model for session bootstrap.

## 3. Display Identity Is Still PlayerPrefs-Driven

### Current Reviewed Flow

- `Assets/Common/UIGameMenu.cs`
  - copies profile name into `PlayerPrefs("PlayerName")`
- `Assets/Pavilion/Scripts/Player.cs`
  - uses `PlayerPrefs("PlayerName")` as the networked display name

### Why This Matters

Display identity is currently too loosely bound to verified auth state.
That makes impersonation in-world easier, even if no authorization is granted from it.

### Risk

- user impersonation in presentation/UI
- confusion between cosmetic identity and authoritative identity
- future accidental reuse of local mutable state as an auth signal

## 4. Shared Browser Token Is JavaScript-Readable

### Current Reviewed Flow

- `Assets/Plugins/WebGL/AuthBridge.jslib`
  - reads `metadyn_token` from cookie or localStorage

### Why This Matters

This may be necessary in the current WebGL/browser architecture, but it means any XSS on a trusted MetaDyn subdomain can potentially become token theft.

### Important Distinction

This is a real risk, but it is **separate from** the UUID trust problem.
The UUID trust issue is the more immediate authorization flaw inside Unity itself.

## Root Cause

The current system mixes three concepts that must be separated:

- **authenticated identity** — who the validated session actually is
- **public identifier** — a UUID or other external identifier used for lookup/reference
- **display metadata** — user-facing name, avatar, and profile presentation

Right now, those boundaries are blurry enough that:
- UUID can influence authorization
- profile lookup is parameterized by UUID
- display name is carried through mutable local state

The correct model is:
- auth token proves identity
- UUID is only an identifier
- display name and avatar are non-authoritative profile fields

## Immediate Fix Strategy

These are the shortest-path changes that remove the most dangerous trust failures.

## Fix 1. Remove Owner/Admin Assignment Based On Raw `userId`

### Required Change

Stop granting admin because:
- `userId == ownerId`

### Principle

Unity must not accept a client-provided UUID as proof of ownership.

### Temporary Safe Fallback Options

Until a stronger role/claim model exists:
- disable owner-by-UUID elevation entirely
- if absolutely needed, use a controlled host-side admin assignment path
- disable `firstPlayerIsAdmin` in production unless there is a strict operational reason to keep it

### Priority

**Critical**

## Fix 2. Bind Profile Fetch To The Authenticated Session User

### Required Change

Replace:
- `FetchProfile(string userId, ...)`

With something like:
- `FetchMyProfile(...)`

### Principle

Unity bootstrap should never ask:
- “give me the profile for UUID X”

for the current-user bootstrap path.
It should instead read only:
- the authenticated session user
- that user’s own profile

### Priority

**High**

## Fix 3. Treat Display Name As Cosmetic Only

### Required Change

- keep `PlayerPrefs("PlayerName")` only as cached display state if needed
- do not use it as any permission, role, ownership, or identity-proof signal

### Priority

**High**

## Structural Fix Strategy

## Fix 4. Introduce Signed Unity Join Tokens

### Recommended Future Architecture

1. user authenticates on dashboard with Supabase
2. dashboard/backend requests a short-lived Unity join token
3. token contains claims such as:
   - `sub`
   - `space_id`
   - `role`
   - `exp`
   - `nonce`
4. Unity presents that token when joining
5. host or backend verifies signature and claims
6. owner/admin privileges come from signed claims, not raw UUID comparison

### Why This Is The Durable Fix

This model:
- removes trust in client-supplied identity fields
- allows explicit per-space authorization
- supports cleaner future Unity/Hyperfy identity alignment
- separates bootstrap identity from cosmetic profile data

### Priority

**High**

## Fix 5. Separate Public Profile Reads From Authoritative Identity

### Required Change

- public profile data should be a limited safe projection
- authoritative identity and role checks should come only from validated session or signed backend claims

### Priority

**Medium**

## Supabase Review Items

These must be reviewed outside the Unity repo itself.

## `profiles` RLS Audit

Confirm whether authenticated users can:
- read only their own profile
- read all profiles
- update only their own profile
- update fields beyond intended self-service fields

### Desired Outcome

- self-profile read/update only for bootstrap and avatar settings
- any public profile access should be explicitly scoped and non-sensitive

## Session / Token Handling Review

Confirm:
- whether the dashboard intentionally stores the access token in a JavaScript-readable cookie
- whether any `.metadyn.xyz` app can read it
- whether CSP and XSS defenses are strong enough for that architecture

### Desired Outcome

- minimize token exposure
- tighten CSP and XSS defenses on dashboard and related subdomains

## Recommended Implementation Order

1. remove raw UUID-based owner/admin elevation in Unity
2. replace arbitrary `FetchProfile(userId)` with authenticated `FetchMyProfile()`
3. disable `firstPlayerIsAdmin` in production unless explicitly required
4. review Supabase RLS on `profiles`
5. introduce signed short-lived Unity join tokens
6. refactor identity flow so display metadata is separate from authorization

## Minimal Patch Scope

If implementing the smallest safe first pass, change these areas first:

- `Assets/MetaDyn/UserList/UserListManager.cs`
  - remove `ownerId == userId` as an authorization decision
- `Assets/Pavilion/Scripts/Player.cs`
  - stop sending auth-significant identity claims via RPC
- `Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs`
  - replace arbitrary profile-by-id bootstrap path with current-session-only profile lookup
- `Assets/Common/UIGameMenu.cs`
  - use authenticated self-profile fetch only

## Recommended Documentation Position

The docs should now describe the current Unity auth situation as:
- web-first auth is real and working for bootstrap continuity
- current identity trust boundaries still need hardening
- client-supplied UUID values must not be treated as proof of identity
- signed server-issued claims are the durable direction for Unity authorization

That is the accurate balance: the platform has a real auth bridge, but parts of authorization remain under-hardened.

## Final Summary

The exposed UUID is not the secret.

The actual problem is that the Unity side currently treats that UUID as if it were proof of identity in at least one important authorization path. That makes in-world impersonation and possible owner/admin escalation plausible even without full dashboard account compromise.

The immediate fix is to remove all authorization decisions that trust client-supplied UUID values.
The durable fix is to move Unity entry and role assignment to a signed, short-lived, server-issued join token model.
