# Hyperfy User System Integration (MetaDyn Auth)

## Goal
Use MetaDyn’s Supabase auth/profile system in Hyperfy so users do not spawn as "Anonymous" and instead carry their real name/avatar.

## Current Hyperfy Flow (Summary)
- Client uses `authToken` from local storage and appends it to the WS URL.
- Server verifies `authToken` using a local JWT secret; if invalid/missing, creates a local user with name "Anonymous".
- User is stored in Hyperfy’s local `users` table and used for player spawn.

## Integration Overview
### 1) Client: Provide MetaDyn Token
- Read MetaDyn token (cookie or URL param) and store it as Hyperfy `authToken`.
- Hyperfy client will then pass it automatically in the WS URL.

### 2) Server: Validate Supabase Token
- Replace/extend JWT verification to validate Supabase JWTs.
- Options:
  - **Local verification:** use Supabase JWT secret.
  - **API verification:** call Supabase `/auth/v1/user` with bearer token.

### 3) User Mapping
- Use Supabase `user.id` as Hyperfy user ID.
- Fetch Supabase profile (name + avatar_url) and upsert into Hyperfy `users` table.
- Spawn player with profile name/avatar instead of "Anonymous".

### 4) Optional Sync Back
- When Hyperfy updates player name/avatar, push back to Supabase.
- Otherwise, keep Hyperfy as read-only consumer of Supabase profile data.

## Hyperfy Touchpoints
- Client token usage: `src/core/systems/ClientNetwork.js`
- Server auth + fallback user creation: `src/core/systems/ServerNetwork.js`
- JWT helper: `src/core/utils-server.js`

## Working Repository Note
- The Hyperfy repository for this integration work is not inside this project folder.
- Active repo path:
  - `/mnt/c/Metaverse/MetaDyn/Dev/HyperfyDev/hyperfy`
- Integration work against the Hyperfy client/server auth flow should be performed in that repository.
- This is the canonical source repository that is pushed to GitHub and pulled onto the server for deployment.
- The MetaDyn dashboard codebase is also outside this project folder.
- Active dashboard repo path:
  - `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding`
- Dashboard-side auth, deploy UI, and API integration work should be performed in that repository.

## Data Flow (Simplified)
1. Dashboard login → `metadyn_token` cookie
2. Hyperfy client reads token → stores as `authToken`
3. Hyperfy server validates token with Supabase
4. Fetch profile → set player name/avatar
5. Player spawns with real identity

## Decisions Needed
- JWT validation: local secret vs Supabase API call
- Sync policy: one-way (Supabase → Hyperfy) or two-way
- Avatar source: Supabase avatar_url or Hyperfy default

## Progress Update (2026-03-05)

### Infrastructure Decision Reached
- Hyperfy is being moved under the shared MetaDyn domain model so auth can rely on a shared cookie instead of cross-domain localStorage.
- Active hostname: `hyperfy.metadyn.xyz`
- This aligns Hyperfy with the existing MetaDyn auth plan using `metadyn_token` with `Domain=.metadyn.xyz`.

### SSL / Proxy Approach Chosen
- Chosen approach: public Let's Encrypt wildcard certificate on Ubuntu/Nginx
- Certificate covers:
  - `metadyn.xyz`
  - `*.metadyn.xyz`
- Issued successfully with Certbot using Cloudflare DNS validation
- Active certificate paths:
  - `/etc/letsencrypt/live/metadyn.xyz/fullchain.pem`
  - `/etc/letsencrypt/live/metadyn.xyz/privkey.pem`

### Nginx Status
- Nginx proxy for `hyperfy.metadyn.xyz` is working
- HTTP port 80 redirects to HTTPS
- HTTPS terminates on Nginx and proxies Hyperfy to `http://localhost:3001`
- Reference template: see `.claude/config/unity-proxy-config.md` for the canonical nginx SSL proxy pattern with name-based resolution
- Working pattern:

```nginx
server {
    listen 80;
    server_name hyperfy.metadyn.xyz;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name hyperfy.metadyn.xyz;

    ssl_certificate /etc/letsencrypt/live/metadyn.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/metadyn.xyz/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### Practical Implication For Auth Integration
- Shared-cookie SSO is now viable once the dashboard sets `metadyn_token` for `.metadyn.xyz`
- Hyperfy no longer needs to rely on a different-domain storage model
- Next implementation work should focus on:
  1. reading the shared MetaDyn token on the Hyperfy client
  2. validating the Supabase token on the Hyperfy server
  3. mapping Supabase profile data into Hyperfy user spawn data

### Current Auth Status
- Unified login is now working in Hyperfy under the shared MetaDyn domain model.
- Current verified behavior:
  1. visiting Hyperfy without `metadyn_token` redirects to dashboard login
  2. logging in on the dashboard returns the user to Hyperfy
  3. Hyperfy receives the dashboard auth token and allows entry through the unified login path
- Legacy local Hyperfy auth fallback has been disabled/commented out in favor of requiring the MetaDyn token during this rollout.

### Current Known Issue
- The user name displayed in Hyperfy UI is not yet updating correctly from the synced login identity.
- Auth gate and login redirect behavior are working, but UI/display-name propagation still needs follow-up.
- Avatar URL sync from token is intentionally disabled for now.

### Deployment Topology Constraint
- The Next.js dashboard is hosted on a different server than the Hyperfy/Nginx origin.
- Because of that, dashboard deployment cannot directly write files, create Nginx configs, or reload services on the Hyperfy host.
- The dashboard must call a trusted remote deployment mechanism that runs on, or has secure access to, the Hyperfy server.

## One-Click Deployment Target

### Product Goal
The long-term operator flow should be:
1. choose a subdomain
2. click deploy
3. MetaDyn provisions the Hyperfy space automatically

### Manual Flow Now Confirmed
The current manual deployment steps are now validated:
1. create or select the Hyperfy space/app directory
2. generate the name-based space config
3. create the Cloudflare DNS subdomain
4. create the Nginx site config with the correct `server_name`
5. enable the site config
6. reload Nginx
7. verify public HTTPS access

### Automation Pipeline To Build
The one-click deployment workflow should automate these exact steps:

1. **Validate subdomain**
   - ensure format is valid
   - reject reserved system names
   - ensure uniqueness

2. **Provision deployment target**
   - create/copy the Hyperfy app or space directory
   - attach the selected space identifier

3. **Generate space config**
   - write name-based config values for the new space
   - include hostname/subdomain metadata
   - include any auth/domain settings needed for shared MetaDyn login

4. **Create DNS record**
   - create the subdomain in Cloudflare
   - point it to the shared host/origin
   - keep proxy enabled

5. **Generate Nginx site config**
   - create a config file for the new hostname
   - set `server_name` to the selected subdomain
   - point traffic at the correct Hyperfy upstream or space deployment
   - include HTTP→HTTPS redirect behavior
   - use the existing wildcard-capable MetaDyn certificate paths

6. **Enable and reload**
   - link the site into `sites-enabled`
   - run `nginx -t`
   - reload Nginx only if config test passes

7. **Post-deploy verification**
   - confirm DNS resolves
   - confirm HTTPS loads
   - confirm websocket proxying works
   - confirm the space is reachable at its public URL

### Required Inputs For One-Click Deploy
- `subdomain`
- `spaceId` or equivalent Hyperfy world identifier
- target deployment directory or template source
- upstream port/process info if spaces are isolated by runtime

### Notes
- In this deployment model, creating and enabling the Nginx site config is the host-routing step.
- DNS alone is not the deploy action; the Nginx site config is what binds the hostname to the correct Hyperfy space runtime or directory.
- This deployment pipeline is now concrete enough to be implemented as dashboard-driven provisioning.
- The nginx SSL/name-based routing template for this pattern is documented in `.claude/config/unity-proxy-config.md`.

### Example: Next.js Dashboard Flow
Below is a simple example of what the operator-facing flow could look like in the MetaDyn dashboard.

#### Important Architecture Note
Because the dashboard runs on a different server, the Next.js app should not be treated as the machine that performs deployment locally.

Instead:
- the dashboard gathers operator input
- the dashboard API validates the request and authorization
- the dashboard API calls a remote deploy service or job runner on the Hyperfy host
- that remote service performs filesystem, Nginx, and process changes
- the dashboard receives status/progress back from that service

#### UI Flow
1. User opens `dashboard.metadyn.xyz/spaces/new`
2. User enters:
   - space name
   - desired subdomain
   - template or source space
3. User clicks `Deploy Space`
4. Dashboard calls a protected deploy API
5. API runs the provisioning pipeline and returns the public URL

#### Example Form Component
```tsx
'use client'

import { useState } from 'react'

export default function NewHyperfySpacePage() {
  const [spaceName, setSpaceName] = useState('')
  const [subdomain, setSubdomain] = useState('')
  const [template, setTemplate] = useState('default')
  const [status, setStatus] = useState<string | null>(null)
  const [deploying, setDeploying] = useState(false)

  async function handleDeploy(e: React.FormEvent) {
    e.preventDefault()
    setDeploying(true)
    setStatus('Deploying...')

    const res = await fetch('/api/spaces/deploy', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        spaceName,
        subdomain,
        template,
        platform: 'hyperfy',
      }),
    })

    const data = await res.json()

    if (!res.ok) {
      setStatus(data.error || 'Deployment failed')
      setDeploying(false)
      return
    }

    setStatus(`Deployed: ${data.url}`)
    setDeploying(false)
  }

  return (
    <form onSubmit={handleDeploy}>
      <input
        value={spaceName}
        onChange={e => setSpaceName(e.target.value)}
        placeholder="Space name"
      />
      <input
        value={subdomain}
        onChange={e => setSubdomain(e.target.value)}
        placeholder="Subdomain"
      />
      <select value={template} onChange={e => setTemplate(e.target.value)}>
        <option value="default">Default</option>
        <option value="gallery">Gallery</option>
        <option value="event">Event</option>
      </select>
      <button type="submit" disabled={deploying}>
        {deploying ? 'Deploying...' : 'Deploy Space'}
      </button>
      {status && <p>{status}</p>}
    </form>
  )
}
```

#### Example API Route
```ts
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  const body = await req.json()
  const { spaceName, subdomain, template, platform } = body

  if (!spaceName || !subdomain) {
    return NextResponse.json(
      { error: 'spaceName and subdomain are required' },
      { status: 400 }
    )
  }

  const deployResponse = await fetch(process.env.DEPLOY_SERVICE_URL + '/hyperfy/deploy', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${process.env.DEPLOY_SERVICE_TOKEN}`,
    },
    body: JSON.stringify({
      spaceName,
      subdomain,
      template,
      platform,
    }),
  })

  const deployResult = await deployResponse.json()

  if (!deployResponse.ok) {
    return NextResponse.json(
      { error: deployResult.error || 'Deployment failed' },
      { status: deployResponse.status }
    )
  }

  return NextResponse.json({
    success: true,
    url: `https://${subdomain}.metadyn.xyz`,
    deploymentId: deployResult.deploymentId,
  })
}
```

#### Example Deploy Service Responsibilities
The deploy service behind the dashboard API would be responsible for:
- validating the subdomain
- creating the Cloudflare DNS record
- copying or provisioning the Hyperfy space
- generating the space config
- generating and enabling the Nginx site config
- testing and reloading Nginx
- returning deployment status and final public URL

#### Recommended Production Shape
For this topology, the clean deployment architecture is:

1. **Dashboard server**
   - hosts the Next.js UI and authenticated API route
   - stores operator/user context
   - submits deployment requests

2. **Deploy service on Hyperfy host**
   - runs on the same server as Hyperfy/Nginx, or has direct privileged access to it
   - performs:
     - file copy/provisioning
     - config generation
     - Nginx site creation
     - `sites-enabled` linking
     - `nginx -t` and reload

3. **Cloudflare API integration**
   - can live either in the deploy service or in a central backend
   - creates the required DNS records before final verification

#### Secure Implementation Options
Reasonable ways to execute the remote deployment step:

- **Preferred:** a small authenticated deploy API running on the Hyperfy server
  - dashboard calls it over HTTPS
  - deploy API performs the privileged local operations

- **Alternative:** dashboard triggers an SSH-based deployment script on the Hyperfy host
  - workable for early-stage internal tooling
  - less clean than a dedicated deploy service

- **Later-stage:** queue/job runner model
  - dashboard submits a job
  - deploy worker on the Hyperfy host pulls and executes it
  - best for retries, audit logs, and scaling

#### Planning Impact
This means the one-click deploy feature is not just a dashboard form.
It requires:
- a remote execution layer
- authentication between dashboard and deploy service
- deployment status reporting
- failure handling and rollback rules if DNS or Nginx steps fail

## Custom Domain Mapping

### Platform Rule
- Every space should always have a canonical MetaDyn hostname, for example:
  - `myspace.metadyn.xyz`
- Custom domains should be treated as optional aliases, not the primary system of record.

### Why This Matters
- Users authenticate through the MetaDyn dashboard.
- Shared-cookie SSO works naturally across `*.metadyn.xyz` using `metadyn_token` with `Domain=.metadyn.xyz`.
- A customer-owned domain such as `world.clientbrand.com` will not share that cookie automatically.

### Recommended Domain Model
1. Deploy canonical space URL first
   - `myspace.metadyn.xyz`

2. Allow optional custom-domain attachment later
   - `world.clientbrand.com`

3. Keep MetaDyn hostname as fallback and auth anchor
   - internal routing, moderation, and login flows should always be able to fall back to the canonical MetaDyn URL

### Recommended Auth Behavior For Custom Domains
For custom domains, auth should still be anchored on the MetaDyn dashboard domain family.

Practical flow:
1. User visits `world.clientbrand.com`
2. Space checks whether the MetaDyn session token is available
3. If not authenticated, redirect user to:
   - `https://dashboard.metadyn.xyz/login?redirect=https://world.clientbrand.com`
4. After login, dashboard completes auth and returns the user to the custom domain
5. Space receives a valid auth handoff and signs the user into the Hyperfy experience

### Important Constraint
- Cookie-based SSO alone is not sufficient on customer-owned domains.
- Custom domains require an auth handoff flow, because `.metadyn.xyz` cookies are not readable on non-MetaDyn domains.

### Implementation Options For Custom-Domain Auth
1. **Redirect + token handoff**
   - dashboard login completes
   - dashboard redirects back with a short-lived signed token or exchange code
   - custom-domain space exchanges that for session/auth state

2. **Redirect to canonical MetaDyn URL for login**
   - user lands on custom domain
   - unauthenticated users are sent through the canonical MetaDyn-hosted flow
   - after login, user returns to the custom domain

3. **MetaDyn-only auth domain policy**
   - custom domains are public aliases
   - privileged account flows still resolve through the canonical `*.metadyn.xyz` hostname

### Recommended Rollout Order
1. First ship shared-cookie auth across `*.metadyn.xyz`
2. Then ship MetaDyn-managed subdomain deployment
3. Then add custom subdomain mapping via CNAME
4. After that, build custom-domain auth handoff

## Future Auth UX (Phase 2)

### Planned Direction
- Phase 1 should prioritize unified login using the shared MetaDyn dashboard auth flow.
- Phase 2 can add direct in-app auth entry points inside both Hyperfy and Unity.

### What Phase 2 Likely Includes
- Hyperfy UI for:
  - log in
  - sign up
  - account/session awareness
- Unity UI for:
  - log in
  - sign up
  - account/session awareness

### Product Intent
- Even when login/signup is initiated inside Hyperfy or Unity, MetaDyn auth should still remain the shared system of record.
- This should feel like a native in-experience auth flow, while still using the same dashboard/Supabase-backed account system underneath.

### Planning Note
- Phase 2 should be treated as a UX/accessibility layer on top of the unified auth system, not a separate auth stack.
- Phase 1 remains:
  - dashboard-driven login
  - shared MetaDyn session token
  - Hyperfy/Unity consuming the same authenticated user identity

### Dashboard Product Flow For Custom Domains
1. User deploys `myspace.metadyn.xyz`
2. User opens domain settings in dashboard
3. User enters `world.clientbrand.com`
4. Dashboard shows DNS instructions
   - usually CNAME to the canonical MetaDyn space hostname
5. Platform verifies ownership/routing
6. Platform adds the hostname to origin routing/Nginx
7. Dashboard marks the custom domain as active

### Operational Note
- Canonical MetaDyn subdomains should remain mandatory even when a custom domain is attached.
- This keeps auth, support, moderation, and recovery flows under MetaDyn control.
