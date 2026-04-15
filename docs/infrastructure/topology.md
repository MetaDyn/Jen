# Infrastructure Topology

## Summary

MetaDyn operates a hybrid infrastructure footprint spanning:
- on-premise systems
- cloud infrastructure
- multiple VPS/providers
- AWS as the primary hosting platform for immersive/web experiences
- Hetzner for current production-adjacent nginx SSL proxy and app/service hosting
- Netlify for the public website and dashboard hosting surfaces

## Current Environment Inventory

### Stage / AWS
- Hostname: `ec2-16-58-195-11.us-east-2.compute.amazonaws.com`
- IPv4: `16.58.195.11`
- Public URL: `https://stage.metadyn.xyz/`
- Notes: current documented staging environment / AWS-hosted surface

### Prod / Hetzner
- Hostname: `ubuntu-8gb-ash-1`
- IPv4: `87.99.130.86`
- IPv6 block: `2a01:4ff:f4:3cc7::/64`
- Public URLs:
  - `https://prod.metadyn.xyz/`
  - `https://crm.metadyn.xyz/`
  - `https://gitlab.metadyn.xyz/`
  - `https://analytics.metadyn.xyz/`
- Notes: current production infrastructure / Hetzner-hosted service cluster

### Netlify
- Public URLs:
  - `https://metadyn.xyz/`
  - `https://dashboard.metadyn.xyz/`
- Notes: current static/frontend hosting surface for the main site and dashboard

## Current DNS / Routing Inventory

### Authoritative DNS Notes
- The active zone export is from Cloudflare for `metadyn.xyz`.
- Active Cloudflare nameservers in the export:
  - `amit.ns.cloudflare.com`
  - `elisabeth.ns.cloudflare.com`
- The export also contains legacy/extra NS records pointing at GoDaddy (`ns39.domaincontrol.com`, `ns40.domaincontrol.com`). Treat these as historical or transitional until explicitly confirmed as active authority.

### AWS EC2 Stage / App Routing (`16.58.195.11`)
- `stage.metadyn.xyz` -> `16.58.195.11` (DNS only)
- `assets.metadyn.xyz` -> `16.58.195.11` (DNS only)
- `starter.metadyn.xyz` -> `16.58.195.11` (DNS only)
- `vitl-medical.metadyn.xyz` -> `16.58.195.11` (DNS only)
- `netflixhouse.metadyn.xyz` -> `16.58.195.11` (Cloudflare proxied)
- `seaworld-sd.metadyn.xyz` -> `16.58.195.11` (Cloudflare proxied)

### Hetzner Prod / Service Routing (`87.99.130.86`)
- `prod.metadyn.xyz` -> `87.99.130.86` (Cloudflare proxied)
- `crm.metadyn.xyz` -> `87.99.130.86` (DNS only)
- `gitlab.metadyn.xyz` -> `87.99.130.86` (DNS only)
- `analytics.metadyn.xyz` -> `87.99.130.86` (DNS only)
- `monitor.metadyn.xyz` -> `87.99.130.86` (DNS only, TTL 60)
- `aurora-01.metadyn.xyz` -> `87.99.130.86` (DNS only)

### Additional Host / Experience Routing (`136.34.121.206`)
- `aurora-02.metadyn.xyz` -> `136.34.121.206` (DNS only)
- `hyperfy.metadyn.xyz` -> `136.34.121.206` (Cloudflare proxied)
- `lunara.metadyn.xyz` -> `136.34.121.206` (Cloudflare proxied)
- `pavilion.metadyn.xyz` -> `136.34.121.206` (DNS only)

### Netlify-routed Surfaces
- `metadyn.xyz` -> `apex-loadbalancer.netlify.com` (CNAME, DNS only in export)
- `www.metadyn.xyz` -> `rad-tiramisu-2b8e8a.netlify.app` (CNAME, DNS only)
- `dashboard.metadyn.xyz` -> `peaceful-pasca-817e56.netlify.app` (CNAME, Cloudflare proxied)
- `devdashboard.metadyn.xyz` -> `sensational-halva-828f32.netlify.app` (CNAME, Cloudflare proxied)
- `dev.metadyn.xyz` -> `animated-muffin-f86f1e.netlify.app` (CNAME, Cloudflare proxied)
- `agentai-react1.metadyn.xyz` -> `darling-sunflower-088962.netlify.app` (CNAME, Cloudflare proxied)
- `webxrtest1.metadyn.xyz` -> `delightful-halva-506e46.netlify.app` (CNAME, Cloudflare proxied)

### Mail / Legacy GoDaddy-hosted Surfaces (`72.167.59.135`)
- `admin.metadyn.xyz` -> `72.167.59.135`
- `autoconfig.admin.metadyn.xyz` -> `72.167.59.135`
- `autoconfig.metadyn.xyz` -> `72.167.59.135`
- `autodiscover.admin.metadyn.xyz` -> `72.167.59.135`
- `autodiscover.metadyn.xyz` -> `72.167.59.135`
- `cpanel.metadyn.xyz` -> `72.167.59.135`
- `mail.metadyn.xyz` -> `72.167.59.135`
- `webdisk.admin.metadyn.xyz` -> `72.167.59.135`
- `webdisk.metadyn.xyz` -> `72.167.59.135`
- `webmail.metadyn.xyz` -> `72.167.59.135`
- `whm.metadyn.xyz` -> `72.167.59.135`
- `www.admin.metadyn.xyz` -> `72.167.59.135`
- Related mail flow records:
  - root MX -> `mail.metadyn.xyz`
  - `send.metadyn.xyz` MX -> `feedback-smtp.us-east-1.amazonses.com`
  - `email.metadyn.xyz` -> `email.josh-garrett33.workers.dev`

### Early Mapping Inferences
- AWS EC2 (`16.58.195.11`) is currently the primary stage/staging-app origin and also fronts several project/experience-specific subdomains.
- Hetzner (`87.99.130.86`) is currently the main production service host for prod, CRM, GitLab, analytics, and monitoring-related surfaces.
- Netlify is the main frontend/static hosting layer for the public site, dashboard, and some dev/test app surfaces.
- `72.167.59.135` appears to be a legacy/GoDaddy hosting/mail/cPanel surface and should be treated as a separate service cluster from AWS/Hetzner/Netlify.
- `136.34.121.206` is an additional host serving Hyperfy/Lunara/Pavilion-related surfaces and should be documented as its own infrastructure node until ownership/purpose is clarified.

## Primary Hosting Surfaces

### AWS
Primary cloud platform for hosted immersive spaces and web-delivered metaverse infrastructure.

Expected areas to document later:
- accounts/environments
- regions
- networking
- storage
- compute/runtime layers
- CDN/origin patterns
- deployment paths

### On-Premise
Local/private infrastructure supporting development, orchestration, services, or persistent internal systems.

Expected areas to document later:
- roles and responsibilities
- local services
- connectivity to cloud/VPS resources
- security boundaries

### VPS / Additional Providers
Supplementary infrastructure used where appropriate for hosting, services, routing, experiments, or platform-specific workloads.

## Hosted Experience Types

- Unity WebGL
- ThreeJS experiences
- Hyperfy immersive spaces

## Documentation Gaps To Fill

- environment inventory
- DNS and domains
- ingress/proxy layout
- deployment targets
- backup strategy
- monitoring and alerting
- security controls
- cost ownership and provider roles

## Current Ingress Direction

For the Jen / OpenClaw control surface, the preferred ingress direction is:

- Cloudflare Tunnel
- Cloudflare Access
- local loopback-bound OpenClaw gateway

See:
- `docs/runbooks/cloudflare-jen-tunnel.md`
