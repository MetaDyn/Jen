# Authentication System

Complete documentation for MetaDyn's web-first authentication, Supabase integration, and dashboard connectivity.

**Status:** Stage 1 Complete (Stage 3 Planned: Unity + Hyperfy Unified SSO) | **Last Updated:** 2026-02-21

---

## Overview

Authentication moved from Unity UI to web dashboard, matching how Spatial.io and other production WebGL platforms handle auth. Login happens on dashboard.metadyn.xyz, Unity reads the session token via cookie-based JavaScript bridge.

**Benefits:** Better UX, OAuth-ready, faster Unity load, cross-subdomain SSO

---

## Domain Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         metadyn.xyz Ecosystem                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  dashboard.metadyn.xyz (React Dashboard)                                 │
│  ├── /login - Email/password + future OAuth (Google, Discord)           │
│  ├── /signup - New user registration                                     │
│  ├── /profile - Edit name, avatar, settings                             │
│  ├── /spaces - Create and manage virtual spaces                         │
│  └── Supabase auth → token stored in localStorage                       │
│                          ↓                                               │
│                    On "Launch" click                                     │
│                          ↓                                               │
│  metadyn.xyz/platform OR pavilion.metadyn.xyz                           │
│  ├── Check for auth token (via URL param or shared cookie)              │
│  ├── No token → redirect to dashboard.metadyn.xyz/login                 │
│  ├── Has token → load Unity WebGL                                       │
│  └── Unity reads token via jslib bridge                                 │
│                          ↓                                               │
│  Unity WebGL                                                             │
│  ├── Validate token with Supabase                                       │
│  ├── Fetch profile (name, avatar_index)                                 │
│  ├── avatar_index >= 0 → spawn immediately                              │
│  └── avatar_index = -1 → show avatar picker, save, spawn                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Key Files

### Unity Files
```
/Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs  # Singleton auth manager
/Assets/MetaDyn/Dashboard/SupabaseConfig.cs       # ScriptableObject for credentials
/Assets/MetaDyn/Dashboard/WebAuthBridge.cs        # Browser↔Unity JS bridge
/Assets/MetaDyn/Dashboard/LoginUI.cs              # Fallback login UI (Editor)
/Assets/Plugins/WebGL/AuthBridge.jslib            # JavaScript cookie bridge
```

### Dashboard Files
```
/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/
├── contexts/AuthContext.tsx     # Cookie management + auth state
├── pages/LoginPage.tsx          # Login with ?redirect= support
├── pages/SignUpPage.tsx         # Signup with ?redirect= support
├── services/authService.ts      # Supabase auth wrapper
└── types.ts                     # TypeScript interfaces
```

---

## Cross-Subdomain Token Handling

**Using: Shared Cookie (Most Seamless)**

Dashboard sets cookie on login/signup that's readable by all subdomains:

```javascript
// In dashboard AuthContext.tsx after successful auth
const isProduction = window.location.hostname.endsWith('.metadyn.xyz');
const domain = isProduction ? '; domain=.metadyn.xyz' : '';
document.cookie = `metadyn_token=${token}${domain}; path=/; samesite=lax; secure; max-age=3600`;
```

Unity reads via jslib:

```javascript
// AuthBridge.jslib
AuthBridge_GetTokenFromCookie: function() {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith('metadyn_token=')) {
            return cookie.substring('metadyn_token='.length);
        }
    }
    return null;
}
```

---

## JavaScript Bridge

**File:** `/Assets/Plugins/WebGL/AuthBridge.jslib`

```javascript
mergeInto(LibraryManager.library, {

    // Get token from cookie (primary method - shared across subdomains)
    AuthBridge_GetTokenFromCookie: function() {
        try {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.startsWith('metadyn_token=')) {
                    var token = cookie.substring('metadyn_token='.length);
                    if (token && token.length > 0) {
                        var bufferSize = lengthBytesUTF8(token) + 1;
                        var buffer = _malloc(bufferSize);
                        stringToUTF8(token, buffer, bufferSize);
                        return buffer;
                    }
                }
            }
        } catch (e) {
            console.error('[AuthBridge] Error getting token from cookie:', e);
        }
        return null;
    },

    // Get token from localStorage (fallback for same-origin)
    AuthBridge_GetTokenFromLocalStorage: function() {
        try {
            var token = localStorage.getItem('metadyn_token');
            if (token && token.length > 0) {
                var bufferSize = lengthBytesUTF8(token) + 1;
                var buffer = _malloc(bufferSize);
                stringToUTF8(token, buffer, bufferSize);
                return buffer;
            }
        } catch (e) {
            console.error('[AuthBridge] Error getting token from localStorage:', e);
        }
        return null;
    },

    // Redirect to dashboard login page with return URL
    AuthBridge_RedirectToLogin: function(dashboardUrlPtr) {
        try {
            var dashboardUrl = UTF8ToString(dashboardUrlPtr);
            var returnUrl = encodeURIComponent(window.location.href);
            var loginUrl = dashboardUrl + '/login?redirect=' + returnUrl;
            window.location.href = loginUrl;
        } catch (e) {
            console.error('[AuthBridge] Error redirecting to login:', e);
        }
    },

    // Clear token cookie (on logout)
    AuthBridge_ClearTokenCookie: function() {
        try {
            document.cookie = 'metadyn_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            document.cookie = 'metadyn_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.metadyn.xyz;';
            localStorage.removeItem('metadyn_token');
        } catch (e) {
            console.error('[AuthBridge] Error clearing token:', e);
        }
    }
});
```

---

## Unity C# Integration

### WebAuthBridge.cs

**File:** `/Assets/MetaDyn/Dashboard/WebAuthBridge.cs`

```csharp
using System.Runtime.InteropServices;
using UnityEngine;

namespace MetaDyn.Dashboard
{
    public class WebAuthBridge : MonoBehaviour
    {
        public static WebAuthBridge Instance { get; private set; }

        [Header("Web Auth Settings")]
        [SerializeField] private bool requireAuthentication = true;
        [SerializeField] private bool enableWebAuth = true;
        [SerializeField] private string dashboardUrl = "https://dashboard.metadyn.xyz";

#if UNITY_WEBGL && !UNITY_EDITOR
        [DllImport("__Internal")] private static extern string AuthBridge_GetTokenFromCookie();
        [DllImport("__Internal")] private static extern string AuthBridge_GetTokenFromLocalStorage();
        [DllImport("__Internal")] private static extern void AuthBridge_RedirectToLogin(string dashboardUrl);
        [DllImport("__Internal")] private static extern void AuthBridge_ClearTokenCookie();
#endif

        public bool RequireAuthentication => requireAuthentication;
        public bool EnableWebAuth => enableWebAuth;
        public string DashboardUrl => dashboardUrl;

        public string GetToken()
        {
#if UNITY_WEBGL && !UNITY_EDITOR
            // Try cookie first, then localStorage
            string token = AuthBridge_GetTokenFromCookie();
            if (string.IsNullOrEmpty(token))
                token = AuthBridge_GetTokenFromLocalStorage();
            return token;
#else
            return null; // Editor uses LoginUI fallback
#endif
        }

        public void RedirectToLogin()
        {
#if UNITY_WEBGL && !UNITY_EDITOR
            AuthBridge_RedirectToLogin(dashboardUrl);
#endif
        }

        public void ClearToken()
        {
#if UNITY_WEBGL && !UNITY_EDITOR
            AuthBridge_ClearTokenCookie();
#endif
        }
    }
}
```

### SupabaseAuthManager.cs

**File:** `/Assets/MetaDyn/Dashboard/SupabaseAuthManager.cs`

Key methods:

```csharp
// Initialize from web token (web-first flow)
public void InitializeFromWebToken(Action<SupabaseUser> onSuccess, Action<string> onError)
{
    if (WebAuthBridge.Instance == null || !WebAuthBridge.Instance.EnableWebAuth)
    {
        onError?.Invoke("Web auth disabled");
        return;
    }

    string token = WebAuthBridge.Instance.GetToken();
    if (string.IsNullOrEmpty(token))
    {
        WebAuthBridge.Instance.RedirectToLogin();
        return;
    }

    ValidateToken(token, onSuccess, onError);
}

// Validate token with Supabase /auth/v1/user
public void ValidateToken(string token, Action<SupabaseUser> onSuccess, Action<string> onError)
{
    StartCoroutine(ValidateTokenCoroutine(token, onSuccess, onError));
}

// Fetch profile with avatar_index
public void FetchProfile(string userId, Action<SupabaseProfile> onSuccess, Action<string> onError)
{
    StartCoroutine(FetchProfileCoroutine(userId, onSuccess, onError));
}

// Update avatar_index in profiles table
public void UpdateAvatarIndex(int avatarIndex, Action onSuccess, Action<string> onError)
{
    StartCoroutine(UpdateAvatarIndexCoroutine(userId, avatarIndex, onSuccess, onError));
}
```

---

## Data Structures

### SupabaseUser
```csharp
[Serializable]
public class SupabaseUser
{
    public string id;
    public string email;
    public string email_confirmed_at;
    public string created_at;
    public SupabaseProfile profile;  // Fetched separately
}
```

### SupabaseProfile
```csharp
[Serializable]
public class SupabaseProfile
{
    public string id;           // User's UUID (matches auth.users.id)
    public string name;         // Display name
    public string avatar_url;   // Profile picture URL
    public int avatar_index;    // -1 = not set, 0+ = avatar choice

    public bool NeedsAvatarSelection => avatar_index < 0;
}
```

### SupabaseSession
```csharp
[Serializable]
public class SupabaseSession
{
    public string accessToken;
    public string refreshToken;
    public int expiresIn;
    public SupabaseUser user;
}
```

---

## Database Schema

```sql
-- profiles table (created by Supabase trigger on signup)
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    name TEXT,
    avatar_url TEXT,
    avatar_index INTEGER DEFAULT -1
);

-- avatar_index values:
-- -1 = no avatar selected (show picker)
-- 0+ = valid avatar index (spawn immediately)
```

---

## Auth Modes

| Require Auth | Enable Web Auth | Behavior |
|--------------|-----------------|----------|
| OFF | - | Guest mode - no login, just play |
| ON | ON | Web-first - cookie token, redirect to dashboard |
| ON | OFF | Manual login via LoginUI (Editor/fallback) |

### WebAuthBridge Inspector Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `Require Authentication` | ON | If OFF, guest mode (no login required) |
| `Enable Web Auth` | ON | If OFF, uses LoginUI for manual login |
| `Dashboard Url` | `https://dashboard.metadyn.xyz` | Redirect target for login |

---

## Login Flow

### First Visit (New User)
```
1. User visits Unity WebGL space
2. WebAuthBridge checks for cookie token → None found
3. Redirect to dashboard.metadyn.xyz/login?redirect={unity_url}
4. User creates account on dashboard
5. Dashboard sets metadyn_token cookie (domain=.metadyn.xyz)
6. Dashboard redirects back to Unity with ?redirect= param
7. Unity reads cookie → validates with Supabase
8. Fetch profile → avatar_index = -1 → Show avatar picker
9. User selects avatar → Save to Supabase
10. User clicks "Start" → Spawn into world
```

### Return Visit (Existing User)
```
1. User visits Unity WebGL space
2. WebAuthBridge checks for cookie token → Found!
3. Validate token with Supabase → Success
4. Fetch profile → avatar_index = 2
5. Set PlayerPrefs.SetInt("AvatarChoice", 2)
6. User clicks "Start" → Spawn with saved avatar
```

### Logout Flow
```
1. User clicks logout (in dashboard or Unity)
2. SupabaseAuthManager.Logout() called
3. WebAuthBridge.ClearToken() → Cookie expired
4. onAuthStateChange fires in dashboard
5. clearAuthCookie() called
6. User redirected to login (if in Unity)
```

---

## Dashboard Integration

**Location:** `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding`
**URL:** dashboard.metadyn.xyz (Netlify)
**Tech Stack:** React 19 + TypeScript + Vite + Supabase

### Cookie Flow

```
Login/Signup on dashboard
    → onAuthStateChange fires
    → setAuthCookie(session.access_token)
    → Cookie: metadyn_token={token}; domain=.metadyn.xyz
    → If ?redirect= param exists, redirect back to Unity space
    → Unity reads cookie → validates → spawns

Logout on dashboard
    → onAuthStateChange fires with SIGNED_OUT
    → clearAuthCookie()
    → Cookie expired on all subdomains
```

### Files Modified for Auth Integration
- `contexts/AuthContext.tsx` - Added `setAuthCookie()` and `clearAuthCookie()` helpers
- `pages/LoginPage.tsx` - Added `?redirect=` param handling for Unity return flow
- `pages/SignUpPage.tsx` - Added `?redirect=` param handling for Unity return flow

---

## Unified Unity + Hyperfy SSO (Stage 3 Planned)

Goal: Use the same dashboard/Supabase login session for both Unity WebGL spaces and Hyperfy spaces, with one user identity (`auth.users.id`) across the platform.

### Design Decision

Use **dashboard-first redirect + token exchange**:
- Keep Dashboard/Supabase as identity provider.
- Keep Hyperfy's existing internal world JWT for WebSocket sessions.
- Do **not** pass raw Supabase access tokens directly through Hyperfy WebSocket query params.

### Why This Approach

- Reuses existing working Unity auth flow and user expectations.
- Preserves Hyperfy's current network/session architecture with minimal disruption.
- Keeps one canonical user ID across dashboard, Unity, and Hyperfy.
- Reduces risk by exchanging Supabase token server-side and issuing short-lived world token.

### Cross-Platform Login Flow (Target)

```
1. User opens Unity or Hyperfy space URL
2. Client checks shared cookie: metadyn_token (domain=.metadyn.xyz)
3. If missing/invalid:
   → redirect to dashboard.metadyn.xyz/login?redirect={space_url}
4. Dashboard login/signup succeeds:
   → sets metadyn_token cookie
   → redirects back to original space URL
5. Space backend validates Supabase token
6. Space backend maps identity to auth.users.id (UUID)
7. Space enters world/session with that canonical user identity
```

### Hyperfy-Specific Integration Pattern

Current Hyperfy behavior uses its own JWT (`authToken`) in WebSocket URL and creates anonymous users when token decode fails.

Planned bridge:
1. Hyperfy client reads `metadyn_token` cookie.
2. Hyperfy client calls `POST /api/auth/exchange` with Supabase token.
3. Hyperfy server validates Supabase token and extracts `sub` (user UUID).
4. Hyperfy server upserts local `users` row using that UUID as `id`.
5. Hyperfy server returns short-lived internal `authToken` (existing Hyperfy JWT format).
6. Hyperfy client connects WebSocket using returned internal token.

### Domain Requirement

For seamless SSO, Unity and Hyperfy spaces should be hosted under `*.metadyn.xyz` so the shared cookie (`domain=.metadyn.xyz`) is readable by both.

If Hyperfy runs on a different root domain, add a dashboard-mediated launch handoff flow instead of relying on cross-domain cookies.

### Planned File Touchpoints

Dashboard:
- `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/contexts/AuthContext.tsx` (shared cookie remains source)
- `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/pages/LoginPage.tsx` (`?redirect=` return flow)
- `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/pages/SignUpPage.tsx` (`?redirect=` return flow)

Hyperfy:
- `/mnt/c/Metaverse/MetaDyn/Dev/HyperfyDev/hyperfy/src/server/index.js` (add `/api/auth/exchange`)
- `/mnt/c/Metaverse/MetaDyn/Dev/HyperfyDev/hyperfy/src/core/systems/ServerNetwork.js` (use canonical user ID path, avoid anonymous fallback when authenticated)
- `/mnt/c/Metaverse/MetaDyn/Dev/HyperfyDev/hyperfy/src/core/utils-server.js` (token validation/mint helpers, or split into dedicated auth module)
- `/mnt/c/Metaverse/MetaDyn/Dev/HyperfyDev/hyperfy/src/client/world-client.js` or `/mnt/c/Metaverse/MetaDyn/Dev/HyperfyDev/hyperfy/src/client/index.js` (pre-connect token exchange bootstrap)

Unity:
- Existing web-first flow remains in place (`WebAuthBridge` + `AuthBridge.jslib` + `SupabaseAuthManager`).

### Hyperfy Follow-Up Checklist

- [x] Read shared auth state for Hyperfy login continuity.
- [x] Validate/auth-exchange to preserve canonical Supabase user identity.
- [x] Support unified login flow across dashboard and Hyperfy.
- [ ] Carry stored username/display name cleanly into Hyperfy.
- [ ] Carry avatar selection / avatar identity cleanly into Hyperfy.
- [ ] Carry additional persisted profile fields where appropriate.
- [ ] Ensure logout/session clearing remains coherent across dashboard, Unity, and Hyperfy.
- [ ] Validate end-to-end identity continuity: Dashboard -> Unity -> Hyperfy -> Unity.

---

## LoginUI (Fallback)

**File:** `/Assets/MetaDyn/Dashboard/LoginUI.cs`

Simple login/signup UI for Editor testing and fallback scenarios.

### Features
- Email/password input fields
- Login and Signup buttons
- Status and error text display
- Auto-hides when web auth is enabled in WebGL
- Integrates with UIGameMenu for auto-spawn on successful login
- Profile fetching with display name

### When It's Used
- Unity Editor (always, for testing)
- WebGL when `enableWebAuth = false`
- As fallback if cookie auth fails

### Integration with UIGameMenu
```csharp
// On successful login + profile fetch
if (autoSpawnOnLogin && uiGameMenu != null)
{
    uiGameMenu.NicknameText.text = profile.name;
    bool hasAvatar = uiGameMenu.LoadAvatarFromProfile(profile);

    if (hasAvatar)
    {
        StartCoroutine(DelayedStartGame());
    }
}
```

---

## Comparison: In-Unity vs Web-First Auth

| Aspect | In-Unity (Old) | Web-First (New) |
|--------|----------------|-----------------|
| Login UX | Clunky Unity UI | Native web forms |
| Password managers | Don't work | Work perfectly |
| OAuth (Google, Discord) | Complex | Native support |
| Unity load time | Waits for login | Already authenticated |
| Profile management | Limited | Full dashboard |
| Session handling | Manual | Browser-native |
| Future 2FA | Very hard | Easy |

---

## Stage 1 Completion Checklist

- [x] SupabaseAuthManager singleton (login/signup/session)
- [x] SupabaseConfig ScriptableObject
- [x] WebAuthBridge with inspector settings
- [x] AuthBridge.jslib for cookie handling
- [x] LoginUI fallback for Editor
- [x] Profile fetching (name, avatar_index)
- [x] avatar_index persistence to Supabase
- [x] Dashboard cookie integration
- [x] ?redirect= param handling
- [x] Three auth modes (Guest/Web-first/Manual)

## Stage 2 (Planned)

- [x] Store permission levels in Supabase (Implemented via Owner ID check in `MetaDynRuntimeConfig`)
- [ ] User stats persistence (play time, achievements)
- [ ] Space ownership and settings
- [ ] OAuth providers (Google, Discord)
- [ ] Custom subdomains for spaces

---

## Troubleshooting

### Token not found in WebGL
1. Check browser DevTools → Application → Cookies
2. Look for `metadyn_token` cookie
3. Verify domain is `.metadyn.xyz` (with leading dot)
4. Check if cookie is expired (max-age: 3600)

### Redirect loop
1. Check `requireAuthentication` setting
2. Verify dashboard login actually sets cookie
3. Check for typos in dashboardUrl

### Profile not loading
1. Check Supabase profiles table exists
2. Verify RLS policies allow read access
3. Check user ID matches auth.users.id

### Avatar not persisting
1. Check `avatar_index` column exists in profiles
2. Verify RLS allows update access
3. Check UpdateAvatarIndex is called after selection

---

## Related Documentation

- **Main Quick Reference:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **AI System:** [AI_EMBODIMENT.md](AI_EMBODIMENT.md)
- **Infrastructure:** [INFRASTRUCTURE.md](INFRASTRUCTURE.md)
- **Dashboard Context:** `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/.claude/`

---

**Last Updated:** 2026-02-21
**Status:** Stage 1 Complete | Stage 3 Planned (Unified Unity + Hyperfy SSO)
rd-scaffolding/.claude/`

---

**Last Updated:** 2026-02-21
**Status:** Stage 1 Complete | Stage 3 Planned (Unified Unity + Hyperfy SSO)
