# MetaDyn nginx SSL Proxy Setup

Last updated: 2026-03-18

## Purpose

This document captures the currently documented MetaDyn nginx SSL proxy pattern based on the local normalized docs and imported infrastructure/deployment notes.

It describes the common architecture, certificate pattern, nginx role, Cloudflare role, and the two main origin-serving modes currently documented for MetaDyn-hosted experiences.

## High-Level Request Path

The documented public request path is:

```text
User -> Cloudflare -> nginx origin -> app or static space
```

In this model:

- Cloudflare is the public edge layer
- nginx is the origin router/server
- the origin either serves static Unity/WebGL content directly or reverse-proxies to a local app runtime such as Hyperfy

## Cloudflare Role

Cloudflare is documented as the public edge layer for:

- DNS
- proxying
- SSL/TLS
- CDN/caching
- WebSocket pass-through/support

The intended architecture is therefore not a direct public nginx-only exposure. Cloudflare sits in front of the origin and handles the internet-facing edge responsibilities.

Sources:
- `docs/platforms/unity6/deployment-hosting.md`
- `docs/platforms/unity6/system-architecture.md`
- `import/unity6-docs/.claude/Quick Reference/INFRASTRUCTURE.md`

## SSL/TLS Model

The documented SSL model is end-to-end encryption:

```text
browser <-> Cloudflare <-> nginx
```

That means:

- the browser uses HTTPS to Cloudflare
- Cloudflare uses HTTPS to the nginx origin
- nginx is expected to present a valid certificate for the requested hostname

The imported infra notes indicate the expected Cloudflare SSL mode is:

- `Full`
- or preferably `Full (Strict)`

This implies nginx is not expected to be plain HTTP behind Cloudflare for public routes.

Source:
- `import/unity6-docs/.claude/Quick Reference/INFRASTRUCTURE.md`

## Certificate Pattern

The strongest repeated certificate pattern in the docs is a shared Let's Encrypt lineage for `metadyn.xyz`.

Documented certificate paths:

```text
/etc/letsencrypt/live/metadyn.xyz/fullchain.pem
/etc/letsencrypt/live/metadyn.xyz/privkey.pem
```

The imported Hyperfy planning notes additionally describe the chosen approach as:

- Ubuntu + nginx
- public Let's Encrypt wildcard certificate
- issued/managed with Certbot
- Cloudflare DNS validation used during issuance

In practice, the documented standard is:

- use Certbot
- validate via Cloudflare DNS when needed
- reference the shared live certificate lineage from nginx server blocks

Sources:
- `import/unity6-docs/.claude/config/unity-proxy-config.md`
- `import/unity6-docs/.claude/config/hyperfy-proxy-config.md`
- `import/unity6-docs/.claude/config/netflixhouse-proxy-config.md`
- `import/unity6-docs/.claude/Planning/Hyperfy_User_System_Integration.md`

## nginx Virtual Host Pattern

The documented nginx layout is classic hostname-based virtual hosting.

Typical shape:

1. a port 80 server block
2. redirect all HTTP traffic to HTTPS
3. a port 443 server block
4. bind `server_name` to the target hostname/subdomain
5. load the SSL certificate and private key
6. either serve static files or reverse-proxy to a local upstream

This means routing is primarily driven by hostname/subdomain.

Sources:
- `import/unity6-docs/.claude/config/unity-proxy-config.md`
- `import/unity6-docs/.claude/config/hyperfy-proxy-config.md`
- `import/unity6-docs/.claude/config/netflixhouse-proxy-config.md`

## Two Main Origin Modes

### 1. Static Unity/WebGL hosting

For Unity/WebGL spaces, nginx is documented as serving files directly from disk.

Common documented elements include:

- `root <APP_ROOT>`
- `index index.html`
- `try_files $uri $uri/ /index.html`
- handling for Unity compressed asset types such as:
  - `.wasm.br`
  - `.data.br`
  - `.js.br`
- cache headers for static assets
- headers appropriate for browser/WebGL delivery
- SPA-style fallback to `index.html`

This is the documented pattern for deployed Unity spaces and similar static immersive experiences.

Sources:
- `import/unity6-docs/.claude/config/unity-proxy-config.md`
- `import/unity6-docs/.claude/config/netflixhouse-proxy-config.md`

### 2. Reverse proxy for Hyperfy / Node app runtimes

For Hyperfy-style or Node-backed services, nginx is documented as terminating TLS and then proxying to a local upstream service.

Typical documented pattern:

```text
proxy_pass http://127.0.0.1:3001
```

or:

```text
proxy_pass http://localhost:3001
```

Typical forwarded headers include:

- `Host`
- `X-Real-IP`
- `X-Forwarded-For`
- `X-Forwarded-Proto`

Typical WebSocket support includes:

- `proxy_http_version 1.1`
- `proxy_set_header Upgrade $http_upgrade`
- `proxy_set_header Connection 'upgrade'`
- `proxy_cache_bypass $http_upgrade`

This is the documented pattern for Hyperfy and similar app-driven origin services.

Sources:
- `import/unity6-docs/.claude/config/hyperfy-proxy-config.md`
- `import/unity6-docs/.claude/Planning/Hyperfy_User_System_Integration.md`

## WebSocket Support

WebSocket support is explicitly part of the documented stack.

At the Cloudflare layer, the docs expect WebSocket pass-through/support for realtime traffic.

At the nginx layer, the reverse-proxy templates explicitly include the `Upgrade` and `Connection` headers needed for upgraded connections.

That means the documented stack expects nginx + Cloudflare to support live upgraded connections for relevant services.

Sources:
- `import/unity6-docs/.claude/Quick Reference/INFRASTRUCTURE.md`
- `import/unity6-docs/.claude/config/hyperfy-proxy-config.md`

## Routing and Space Isolation

The docs are explicit that each space is its own build.

That means:

- multiple spaces may share one host
- nginx routes subdomains/hostnames to the correct deployment
- Unity deployments are commonly isolated by directory
- app-backed experiences are isolated by instance/upstream

A documented per-space deployment path example is:

```text
{remotePath}/{roomName}-{spaceId}/
```

This supports cleaner isolation, rollback discipline, and per-space routing.

Sources:
- `docs/platforms/unity6/deployment-hosting.md`
- `import/unity6-docs/.claude/Quick Reference/INFRASTRUCTURE.md`

## Concrete Documented Examples

### Hyperfy

The clearest reverse-proxy example in the docs is `hyperfy.metadyn.xyz`.

Documented pattern:

- Cloudflare in front
- nginx on Ubuntu origin
- Let's Encrypt cert lineage for `metadyn.xyz`
- port 80 redirects to HTTPS
- port 443 terminates TLS
- nginx proxies to `http://localhost:3001`
- websocket upgrade headers are enabled

Source:
- `import/unity6-docs/.claude/Planning/Hyperfy_User_System_Integration.md`

### NetflixHouse Unity host

The clearest static-host example is `netflixhouse.metadyn.xyz`.

Documented pattern:

- static Unity content served from `/var/www/unity-webgl/netflixhouse`
- shared `metadyn.xyz` certificate lineage
- Unity/WebGL compression-aware asset handling
- SPA fallback for client-side navigation

Source:
- `import/unity6-docs/.claude/config/netflixhouse-proxy-config.md`

### Pavilion environment split

The docs also sketch an environment split for:

- `pavilion.metadyn.xyz`
- `dev.pavilion.metadyn.xyz`

Both are described as following the same general Cloudflare + nginx + per-hostname routing model.

Source:
- `import/unity6-docs/.claude/Quick Reference/DEPLOYMENT_ARCHITECTURE.md`

## Operational Activation Flow

The documented operational pattern for nginx config changes is:

1. create or update the nginx config
2. link or enable it under `sites-enabled`
3. run `nginx -t`
4. only reload nginx if the config test succeeds

This is described as the expected safe deployment workflow.

Sources:
- `import/unity6-docs/.claude/config/unity-proxy-config.md`
- `import/unity6-docs/.claude/config/hyperfy-proxy-config.md`
- `import/unity6-docs/.claude/Planning/Deployment_Production_Readiness_Plan.md`

## What Is Explicit vs Inferred

### Explicitly documented

- Cloudflare is the public edge layer
- nginx is the origin router/server
- public routes are expected to use HTTPS end-to-end
- `metadyn.xyz` Let's Encrypt cert lineage is the standard cert path shown in docs
- nginx uses hostname-based virtual hosts
- HTTP redirects to HTTPS
- Unity spaces are generally served statically from disk
- Hyperfy/Node services are reverse-proxied to localhost upstreams
- websocket support is part of the expected config
- safe nginx activation is `nginx -t` followed by reload

### Inferred / still incomplete

- the full live inventory of current hostnames and origins is not yet documented in one place
- MetaDyn likely has some environment-specific variation because the normalized topology doc describes a hybrid footprint across AWS, on-prem, and additional VPS/providers
- not every active production hostname is enumerated in the normalized docs

Source:
- `docs/infrastructure/topology.md`

## Bottom Line

The documented MetaDyn nginx SSL proxy setup is:

- Cloudflare at the edge
- nginx behind it as the origin server/router
- Let's Encrypt certificates on nginx using the `metadyn.xyz` lineage
- Cloudflare `Full` or `Full (Strict)` SSL mode
- HTTP to HTTPS redirect at nginx
- per-hostname/per-subdomain routing
- then either:
  - static Unity/WebGL serving from per-space directories
  - or reverse proxying to local app runtimes such as Hyperfy
- websocket upgrade support where required

This is the clearest documented baseline for how MetaDyn-hosted public surfaces are expected to be exposed.
