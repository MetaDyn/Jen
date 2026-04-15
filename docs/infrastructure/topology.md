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
