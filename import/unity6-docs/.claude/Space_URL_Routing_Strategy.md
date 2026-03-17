# MetaDyn Space URL Routing Strategy

**Date:** 2025-12-30
**Status:** Planning
**Purpose:** Define URL structure for user-created spaces with custom subdomains

---

## Executive Summary

This document outlines strategies for allowing users to create custom-named spaces with their own URLs, comparing approaches and recommending an implementation path.

**Goal:** `myspace.metadyn.xyz` instead of `spatial.io/s/My-Space-839485`

---

## Part 1: Comparison with Competitors

### Spatial.io Approach

**URL Format:** `spatial.io/s/Space-Name-839485`

```
https://spatial.io/s/My-Cool-Space-839485
                    │  │              │
                    │  │              └── GUID suffix (uniqueness)
                    │  └── Human-readable name (not unique)
                    └── /s/ route prefix
```

**How it works:**
- Space name is slugified but NOT unique
- GUID suffix guarantees uniqueness
- Single domain, path-based routing
- No DNS complexity

**Pros:**
- Simple infrastructure (no DNS management)
- Guaranteed unique URLs
- Easy to implement
- SEO: all content on main domain

**Cons:**
- Ugly URLs with random numbers
- Not brandable/memorable
- Can't share clean URL verbally
- Looks auto-generated/cheap

### VRChat Approach

**URL Format:** `vrchat.com/home/world/wrld_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

```
https://vrchat.com/home/world/wrld_a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6
```

**Pros:**
- Very simple (just UUIDs)
- No collision possible

**Cons:**
- Completely unreadable
- Impossible to remember or share verbally

### Roblox Approach

**URL Format:** `roblox.com/games/123456789/Game-Name`

```
https://www.roblox.com/games/123456789/Adopt-Me
                            │          │
                            │          └── SEO-friendly slug (optional, ignored)
                            └── Numeric ID (the real identifier)
```

**Pros:**
- Numeric IDs are short
- Slug is just for SEO, can change

**Cons:**
- Still has arbitrary numbers
- Not brandable

### MetaDyn Proposed Approach

**URL Format:** `myspace.metadyn.xyz`

```
https://myspace.metadyn.xyz
        │       │
        │       └── Platform domain
        └── User-chosen unique subdomain
```

**Pros:**
- Clean, brandable URLs
- Easy to share verbally ("visit myspace dot metadyn dot xyz")
- Professional appearance
- Each space feels like its own site
- Memorable

**Cons:**
- More complex infrastructure
- Subdomain squatting concerns
- DNS/routing complexity

---

## Part 2: URL Strategy Options

### Option A: Subdomain Wildcard (Recommended)

**Pattern:** `*.spaces.metadyn.xyz`

```
myspace.spaces.metadyn.xyz
coolworld.spaces.metadyn.xyz
corporate-hq.spaces.metadyn.xyz
```

**DNS Setup:**
```
Type    Name        Content                     Proxy
CNAME   *.spaces    space-router.workers.dev    Proxied (orange)
```

**Routing:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare DNS                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  metadyn.xyz           → Main website (explicit A/CNAME)    │
│  dashboard.metadyn.xyz → Dashboard (explicit CNAME)         │
│  api.metadyn.xyz       → API (explicit CNAME)               │
│  pavilion.metadyn.xyz  → Unity CDN (explicit CNAME)         │
│                                                              │
│  *.spaces.metadyn.xyz  → Space Router Worker (wildcard)     │
│      └── Worker checks DB, routes to Unity with space ID    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Pros:**
- Clean separation: user spaces isolated from system infrastructure
- No risk of conflicts with future system subdomains
- Easy to understand and maintain
- Worker only handles space traffic

**Cons:**
- Slightly longer URLs than root subdomain
- `spaces.` prefix adds visual noise

**URL Examples:**
- `myspace.spaces.metadyn.xyz`
- `acme-corp.spaces.metadyn.xyz`

---

### Option B: Root Subdomain Wildcard

**Pattern:** `*.metadyn.xyz` (with explicit records taking priority)

```
myspace.metadyn.xyz
coolworld.metadyn.xyz
corporate-hq.metadyn.xyz
```

**DNS Setup:**
```
Type    Name        Content                     Proxy
A       @           <main-site-ip>              Proxied
CNAME   dashboard   <dashboard-host>            Proxied
CNAME   api         <api-host>                  Proxied
CNAME   pavilion    <unity-cdn>                 Proxied
CNAME   *           space-router.workers.dev    Proxied (wildcard, lowest priority)
```

**How Priority Works:**
In Cloudflare, explicit records ALWAYS take priority over wildcards:
1. `dashboard.metadyn.xyz` → matches explicit CNAME → Dashboard
2. `random.metadyn.xyz` → no explicit match → falls to wildcard → Worker

**Pros:**
- Cleanest URLs (`myspace.metadyn.xyz`)
- Most brandable
- Easiest to share verbally

**Cons:**
- Must maintain explicit records for ALL system subdomains
- Risk: forgetting to add explicit record for new system subdomain → routes to Worker
- Requires reserved subdomain list in Worker as safety net

**URL Examples:**
- `myspace.metadyn.xyz`
- `acme-corp.metadyn.xyz`

---

### Option C: Worker Routes (No Wildcard DNS)

**Pattern:** Explicit DNS + Worker route patterns

```
myspace.metadyn.xyz
coolworld.metadyn.xyz
```

**DNS Setup:**
```
Type    Name        Content                     Proxy
A       @           <main-site-ip>              Proxied
CNAME   dashboard   <dashboard-host>            Proxied
CNAME   *           <default-server>            Proxied
```

**Worker Route Configuration:**
```toml
# wrangler.toml
routes = [
  { pattern = "*.metadyn.xyz/*", zone_name = "metadyn.xyz", custom_domain = true }
]

# Worker then checks if subdomain is a space or system subdomain
```

**Pros:**
- Fine-grained control over what Worker handles
- Can exclude specific patterns

**Cons:**
- More complex configuration
- Worker still processes all subdomain traffic to check

---

### Option D: Path-Based with Slugs (Spatial Style)

**Pattern:** `metadyn.xyz/s/space-name` or `metadyn.xyz/s/space-name-uuid`

```
metadyn.xyz/s/my-cool-space
metadyn.xyz/s/my-cool-space-a1b2c3d4
```

**Implementation:**
- No DNS complexity
- Single Worker or server handles routing
- Slug uniqueness enforced in database

**Variant D1: Unique Slugs (First-Come-First-Serve)**
```
metadyn.xyz/s/my-space     → Unique, claimed by first user
```

**Variant D2: Slug + Short ID (Spatial Style)**
```
metadyn.xyz/s/my-space-839485   → Slug for readability, ID for uniqueness
```

**Pros:**
- Simplest infrastructure
- No DNS management
- All content on main domain (SEO)

**Cons:**
- Less brandable than subdomains
- `/s/` path looks less professional
- Can't verbally share as easily

---

### Option E: Separate Domain

**Pattern:** Dedicated domain for user spaces

```
myspace.metadyn.world
myspace.on.metadyn.xyz
myspace.metaverse.space
```

**Pros:**
- Complete isolation from main infrastructure
- Can use cheap/creative TLD for spaces
- Clear separation of concerns

**Cons:**
- Additional domain to manage
- Users might be confused by different domain
- SSL certificate management

---

## Part 3: Recommendation

### Primary Recommendation: Option B (Root Subdomain)

**URL Format:** `myspace.metadyn.xyz`

**Rationale:**
1. Cleanest, most professional URLs
2. Highly brandable and memorable
3. Easy to share verbally
4. Cloudflare's explicit-record-priority makes it safe
5. Differentiates from Spatial's ugly GUIDs

**Safety Measures:**
1. Maintain comprehensive reserved subdomain list
2. Worker double-checks against reserved list
3. Regular audit of system subdomains

### Fallback: Option A (Subdomain Wildcard)

**URL Format:** `myspace.spaces.metadyn.xyz`

**Use if:**
- Team prefers extra safety margin
- Concerned about subdomain conflicts
- Want clearer separation

---

## Part 4: Implementation Details

### Reserved Subdomains List

```typescript
const RESERVED_SUBDOMAINS = [
  // Core infrastructure
  'www', 'api', 'cdn', 'static', 'assets', 'media',

  // Applications
  'dashboard', 'admin', 'app', 'platform', 'pavilion',
  'play', 'game', 'world', 'worlds', 'space', 'spaces',

  // Auth & accounts
  'auth', 'login', 'logout', 'signup', 'register',
  'account', 'accounts', 'profile', 'profiles', 'user', 'users',
  'settings', 'preferences',

  // Communication
  'mail', 'email', 'smtp', 'imap', 'pop',
  'chat', 'voice', 'video', 'call',

  // Support
  'help', 'support', 'docs', 'documentation', 'faq',
  'blog', 'news', 'updates', 'changelog',
  'status', 'health', 'ping',

  // Legal & business
  'about', 'contact', 'careers', 'jobs', 'press',
  'legal', 'terms', 'privacy', 'dmca', 'copyright',

  // Development
  'dev', 'development', 'staging', 'stage', 'test', 'testing',
  'demo', 'sandbox', 'preview', 'beta', 'alpha',
  'local', 'localhost',

  // Security
  'admin', 'administrator', 'root', 'system', 'sys',
  'security', 'secure', 'ssl', 'tls',

  // Brand protection
  'metadyn', 'meta', 'official', 'verified', 'real',

  // Common exploits
  'null', 'undefined', 'nan', 'true', 'false',
  'admin', 'administrator', 'moderator', 'mod',

  // Social/vanity
  'me', 'my', 'home', 'main', 'default',
];
```

### Subdomain Validation Rules

```typescript
interface ValidationResult {
  valid: boolean;
  reason?: string;
}

function validateSubdomain(subdomain: string): ValidationResult {
  // 1. Length check (3-63 characters for DNS compliance)
  if (subdomain.length < 3) {
    return { valid: false, reason: 'Must be at least 3 characters' };
  }
  if (subdomain.length > 63) {
    return { valid: false, reason: 'Must be 63 characters or less' };
  }

  // 2. Character check (lowercase alphanumeric + hyphens)
  if (!/^[a-z0-9][a-z0-9-]*[a-z0-9]$/.test(subdomain)) {
    return {
      valid: false,
      reason: 'Must start and end with letter/number, only lowercase letters, numbers, and hyphens allowed'
    };
  }

  // 3. No consecutive hyphens (DNS restriction)
  if (/--/.test(subdomain)) {
    return { valid: false, reason: 'Cannot contain consecutive hyphens' };
  }

  // 4. Reserved check
  if (RESERVED_SUBDOMAINS.includes(subdomain)) {
    return { valid: false, reason: 'This name is reserved' };
  }

  // 5. Profanity check (use library like 'bad-words')
  if (containsProfanity(subdomain)) {
    return { valid: false, reason: 'This name is not allowed' };
  }

  // 6. Trademark/brand check (optional, manual review queue)
  if (looksLikeTrademark(subdomain)) {
    return { valid: false, reason: 'This name may be trademarked. Contact support if you own this brand.' };
  }

  return { valid: true };
}
```

### Database Schema

```sql
-- Supabase migration

-- Add subdomain to spaces table
ALTER TABLE spaces ADD COLUMN subdomain TEXT UNIQUE;

-- Create index for fast lookups
CREATE INDEX idx_spaces_subdomain ON spaces(subdomain) WHERE subdomain IS NOT NULL;

-- Add constraint for valid format
ALTER TABLE spaces ADD CONSTRAINT valid_subdomain_format
  CHECK (subdomain ~ '^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$');

-- Add status for space lifecycle
ALTER TABLE spaces ADD COLUMN status TEXT DEFAULT 'active'
  CHECK (status IN ('active', 'inactive', 'suspended', 'deleted'));

-- Subdomain history (for audit/reuse policy)
CREATE TABLE subdomain_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subdomain TEXT NOT NULL,
  space_id UUID REFERENCES spaces(id),
  claimed_at TIMESTAMPTZ DEFAULT NOW(),
  released_at TIMESTAMPTZ,
  owner_id UUID REFERENCES auth.users(id)
);

-- Prevent subdomain reuse for 30 days after release
CREATE OR REPLACE FUNCTION check_subdomain_cooldown()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM subdomain_history
    WHERE subdomain = NEW.subdomain
    AND released_at > NOW() - INTERVAL '30 days'
    AND owner_id != NEW.owner_id
  ) THEN
    RAISE EXCEPTION 'Subdomain recently released, not available for 30 days';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_subdomain_cooldown
  BEFORE INSERT ON spaces
  FOR EACH ROW
  EXECUTE FUNCTION check_subdomain_cooldown();
```

### Cloudflare Worker: Space Router

```typescript
// workers/space-router/src/index.ts

export interface Env {
  SUPABASE_URL: string;
  SUPABASE_ANON_KEY: string;
  UNITY_ORIGIN: string;  // https://pavilion.metadyn.xyz
}

const RESERVED_SUBDOMAINS = [/* ... full list ... */];

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const hostname = url.hostname;

    // Parse subdomain
    // myspace.metadyn.xyz → myspace
    // myspace.spaces.metadyn.xyz → myspace (if using Option A)
    const subdomain = extractSubdomain(hostname);

    if (!subdomain) {
      // No subdomain - shouldn't hit this Worker, but handle gracefully
      return Response.redirect('https://metadyn.xyz', 302);
    }

    // Safety check: reserved subdomains
    if (RESERVED_SUBDOMAINS.includes(subdomain.toLowerCase())) {
      // This shouldn't happen if DNS is configured correctly
      // But as safety net, redirect to main site
      console.warn(`Reserved subdomain hit Worker: ${subdomain}`);
      return Response.redirect(`https://${subdomain}.metadyn.xyz`, 302);
    }

    // Look up space in database
    const space = await lookupSpace(subdomain, env);

    if (!space) {
      // Space not found - show friendly 404 or redirect to create
      return new Response(
        generateNotFoundHTML(subdomain),
        {
          status: 404,
          headers: { 'Content-Type': 'text/html' }
        }
      );
    }

    if (space.status !== 'active') {
      // Space exists but not active
      return new Response(
        generateInactiveHTML(space),
        {
          status: 403,
          headers: { 'Content-Type': 'text/html' }
        }
      );
    }

    // Space found and active - proxy to Unity
    const unityUrl = new URL(env.UNITY_ORIGIN);
    unityUrl.pathname = url.pathname;
    unityUrl.searchParams.set('space', space.id);

    // Preserve auth token if present
    const token = url.searchParams.get('token');
    if (token) {
      unityUrl.searchParams.set('token', token);
    }

    // Fetch and return Unity content
    const response = await fetch(unityUrl.toString(), {
      method: request.method,
      headers: request.headers,
    });

    // Add space context headers
    const newHeaders = new Headers(response.headers);
    newHeaders.set('X-Space-Id', space.id);
    newHeaders.set('X-Space-Name', space.name);
    newHeaders.set('X-Space-Subdomain', subdomain);

    return new Response(response.body, {
      status: response.status,
      headers: newHeaders
    });
  }
};

function extractSubdomain(hostname: string): string | null {
  // Option A: *.spaces.metadyn.xyz
  // const match = hostname.match(/^([^.]+)\.spaces\.metadyn\.xyz$/);

  // Option B: *.metadyn.xyz
  const match = hostname.match(/^([^.]+)\.metadyn\.xyz$/);

  return match ? match[1].toLowerCase() : null;
}

async function lookupSpace(subdomain: string, env: Env): Promise<Space | null> {
  const response = await fetch(
    `${env.SUPABASE_URL}/rest/v1/spaces?subdomain=eq.${subdomain}&select=id,name,subdomain,status,owner_id`,
    {
      headers: {
        'apikey': env.SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${env.SUPABASE_ANON_KEY}`
      }
    }
  );

  if (!response.ok) {
    console.error('Supabase lookup failed:', await response.text());
    return null;
  }

  const spaces = await response.json();
  return spaces.length > 0 ? spaces[0] : null;
}

function generateNotFoundHTML(subdomain: string): string {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Space Not Found - MetaDyn</title>
      <style>
        body { font-family: system-ui; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #0a0a0a; color: white; }
        .container { text-align: center; }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        p { color: #888; margin-bottom: 2rem; }
        a { color: #00d4ff; text-decoration: none; }
        .btn { display: inline-block; padding: 12px 24px; background: #00d4ff; color: black; border-radius: 8px; font-weight: bold; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Space Not Found</h1>
        <p>"${subdomain}" doesn't exist yet.</p>
        <a href="https://dashboard.metadyn.xyz/spaces/new?name=${subdomain}" class="btn">
          Create This Space
        </a>
      </div>
    </body>
    </html>
  `;
}

function generateInactiveHTML(space: Space): string {
  return `
    <!DOCTYPE html>
    <html>
    <head><title>Space Unavailable - MetaDyn</title></head>
    <body>
      <h1>Space Unavailable</h1>
      <p>This space is currently ${space.status}.</p>
      <a href="https://metadyn.xyz">Return to MetaDyn</a>
    </body>
    </html>
  `;
}

interface Space {
  id: string;
  name: string;
  subdomain: string;
  status: 'active' | 'inactive' | 'suspended' | 'deleted';
  owner_id: string;
}
```

### Availability Check API

```typescript
// In Worker or Dashboard API

app.post('/api/spaces/check-subdomain', async (c) => {
  const { subdomain } = await c.req.json();

  // Validate format
  const validation = validateSubdomain(subdomain);
  if (!validation.valid) {
    return c.json({
      available: false,
      reason: validation.reason
    });
  }

  // Check database
  const existing = await lookupSpace(subdomain, c.env);
  if (existing) {
    return c.json({
      available: false,
      reason: 'This name is already taken'
    });
  }

  // Check cooldown (recently released)
  const recentlyReleased = await checkCooldown(subdomain, c.env);
  if (recentlyReleased) {
    return c.json({
      available: false,
      reason: 'This name was recently released and is not yet available'
    });
  }

  return c.json({
    available: true,
    preview: `${subdomain}.metadyn.xyz`
  });
});
```

### Dashboard: Space Creation UI

```typescript
// components/CreateSpaceForm.tsx

import { useState, useEffect } from 'react';
import { useDebounce } from '@/hooks/useDebounce';

export function CreateSpaceForm() {
  const [name, setName] = useState('');
  const [subdomain, setSubdomain] = useState('');
  const [autoSubdomain, setAutoSubdomain] = useState(true);
  const [availability, setAvailability] = useState<{
    status: 'idle' | 'checking' | 'available' | 'unavailable';
    reason?: string;
  }>({ status: 'idle' });

  const debouncedSubdomain = useDebounce(subdomain, 500);

  // Auto-generate subdomain from name
  useEffect(() => {
    if (autoSubdomain && name) {
      const generated = name
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .substring(0, 63);
      setSubdomain(generated);
    }
  }, [name, autoSubdomain]);

  // Check availability
  useEffect(() => {
    if (debouncedSubdomain.length < 3) {
      setAvailability({ status: 'idle' });
      return;
    }

    setAvailability({ status: 'checking' });

    fetch('/api/spaces/check-subdomain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ subdomain: debouncedSubdomain })
    })
      .then(res => res.json())
      .then(data => {
        setAvailability({
          status: data.available ? 'available' : 'unavailable',
          reason: data.reason
        });
      })
      .catch(() => {
        setAvailability({ status: 'idle' });
      });
  }, [debouncedSubdomain]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (availability.status !== 'available') return;

    // Create space...
  };

  return (
    <form onSubmit={handleSubmit} className="space-form">
      <div className="field">
        <label>Space Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="My Awesome Space"
        />
      </div>

      <div className="field">
        <label>
          URL
          <button
            type="button"
            className="toggle-auto"
            onClick={() => setAutoSubdomain(!autoSubdomain)}
          >
            {autoSubdomain ? 'Customize' : 'Auto-generate'}
          </button>
        </label>

        <div className="subdomain-input">
          <input
            type="text"
            value={subdomain}
            onChange={(e) => {
              setAutoSubdomain(false);
              setSubdomain(e.target.value.toLowerCase());
            }}
            disabled={autoSubdomain}
          />
          <span className="domain-suffix">.metadyn.xyz</span>
        </div>

        <div className={`availability ${availability.status}`}>
          {availability.status === 'checking' && (
            <span>Checking availability...</span>
          )}
          {availability.status === 'available' && (
            <span className="success">✓ Available</span>
          )}
          {availability.status === 'unavailable' && (
            <span className="error">✗ {availability.reason}</span>
          )}
        </div>
      </div>

      <button
        type="submit"
        disabled={availability.status !== 'available'}
        className="create-btn"
      >
        Create Space
      </button>
    </form>
  );
}
```

### Unity: Read Space Context

**Update AuthBridge.jslib:**

```javascript
mergeInto(LibraryManager.library, {

  // ... existing auth methods ...

  GetSpaceId: function() {
    // Try URL param first (from Worker redirect)
    var params = new URLSearchParams(window.location.search);
    var spaceId = params.get('space');

    if (spaceId) {
      var bufferSize = lengthBytesUTF8(spaceId) + 1;
      var buffer = _malloc(bufferSize);
      stringToUTF8(spaceId, buffer, bufferSize);
      return buffer;
    }
    return null;
  },

  GetSpaceSubdomain: function() {
    var hostname = window.location.hostname;
    var match = hostname.match(/^([^.]+)\.(?:spaces\.)?metadyn\.xyz$/);

    if (match) {
      var subdomain = match[1];
      var bufferSize = lengthBytesUTF8(subdomain) + 1;
      var buffer = _malloc(bufferSize);
      stringToUTF8(subdomain, buffer, bufferSize);
      return buffer;
    }
    return null;
  },

  // Get space metadata from response headers (set by Worker)
  GetSpaceMetadata: function() {
    // Note: Headers aren't directly accessible after page load
    // Use URL params or fetch /api/space/current instead
    return null;
  }

});
```

---

## Part 5: Comparison Summary

| Aspect | Spatial.io (Path + GUID) | MetaDyn (Subdomain) |
|--------|--------------------------|---------------------|
| **URL Example** | `spatial.io/s/My-Space-839485` | `myspace.metadyn.xyz` |
| **Memorability** | Low (random numbers) | High (user-chosen) |
| **Verbal Sharing** | Difficult | Easy |
| **Brandability** | Low | High |
| **Infrastructure** | Simple (path routing) | Complex (DNS/Worker) |
| **Uniqueness** | GUID guarantees | First-come-first-serve |
| **Squatting Risk** | None | Moderate (mitigated by rules) |
| **SEO** | All on main domain | Distributed across subdomains |

---

## Part 6: Implementation Checklist

### Phase 1: Infrastructure (Day 1)
- [ ] Add wildcard DNS record (`*.metadyn.xyz` or `*.spaces.metadyn.xyz`)
- [ ] Deploy space-router Worker
- [ ] Configure Worker routes
- [ ] Test with manual database entries

### Phase 2: Database (Day 1)
- [ ] Add `subdomain` column to spaces table
- [ ] Add unique constraint and index
- [ ] Add validation constraint
- [ ] Create subdomain_history table
- [ ] Add cooldown trigger

### Phase 3: API (Day 2)
- [ ] Implement `/api/spaces/check-subdomain` endpoint
- [ ] Update space creation to include subdomain
- [ ] Add subdomain validation middleware
- [ ] Implement reserved subdomain check

### Phase 4: Dashboard UI (Days 3-4)
- [ ] Add subdomain input to space creation form
- [ ] Implement real-time availability checking
- [ ] Add auto-generation from space name
- [ ] Add URL preview

### Phase 5: Unity Integration (Day 5)
- [ ] Update AuthBridge.jslib with space methods
- [ ] Update WebAuthBridge.cs
- [ ] Handle space loading from subdomain/params
- [ ] Test full flow

### Phase 6: Polish (Week 2)
- [ ] Add profanity filter
- [ ] Implement trademark review queue
- [ ] Create subdomain transfer feature
- [ ] Add subdomain change (with cooldown)
- [ ] Create admin tools for subdomain management

---

## Part 7: Future Considerations

### Custom Domains (Premium Feature)
Allow users to point their own domain to their space:
```
mycompany.com → mycompany.spaces.metadyn.xyz
```

Requires:
- Cloudflare for SaaS (or custom SSL)
- Domain verification flow
- CNAME setup instructions

### Subdomain Marketplace
Allow selling/transferring subdomains:
- Auction system for premium names
- Transfer fees
- Verification of ownership

### Analytics per Subdomain
Track visits, engagement per space URL:
- Cloudflare Analytics
- Custom Worker logging
- Dashboard integration

---

**Document Status:** Ready for implementation
**Recommended Approach:** Option B (Root Subdomain Wildcard)
**Estimated Implementation:** 1-2 weeks
