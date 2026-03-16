# Deployment and Hosting

## Delivery Model

The imported platform docs are explicit that deployment is part of the product, not a disconnected ops concern.

The Unity platform is designed so that creators can:
- configure deployment from the Unity editor
- build WebGL output
- deploy to remote infrastructure using SSH/rsync/scp-style workflows
- embed runtime metadata into the deployed build

## Canonical Deployment Rule

**Each space is its own build.**

This rule is central to the imported deployment architecture and applies across both hosting models.

## Hosting Models

### Shared Hosting
MetaDyn intends to support a shared-hosting model where:
- multiple spaces can live on the same physical or virtual host
- each space still has isolated deployment files or runtime instance boundaries
- routing/proxy rules map each hostname/subdomain to the correct space deployment

### Self-Hosting
MetaDyn also intends to support self-hosted deployments where:
- customers, partners, or studios deploy to infrastructure they control
- the same core deployment model still applies
- runtime config, deployment metadata, and routing remain important

## Cloudflare Role

Imported infrastructure docs describe Cloudflare as the edge layer for:
- DNS
- proxying
- SSL/TLS
- CDN behavior
- cached Unity WebGL asset delivery
- WebSocket support for realtime systems

This supports the WebGL-first platform strategy by reducing latency and improving global delivery.

## Unity WebGL Hosting Pattern

The documented per-space deployment pattern uses isolated remote directories such as:

```text
{remotePath}/{roomName}-{spaceId}/
```

This supports:
- per-space isolation
- cleaner routing management
- better rollback/version discipline
- managed hosting for multiple spaces on one server

## Deployment Tooling

Imported docs point to editor-integrated tooling for:
- server profile management
- deployment configuration
- remote upload via SSH/rsync/scp
- runtime config embedding
- deployment preflight checks

Documented hardening already includes:
- remote directory creation/verification before transfer
- explicit failure handling when remote paths cannot be confirmed
- more actionable deployment feedback inside Unity

## Operational Direction

The imported docs point toward a more mature hosting/control model over time, including:
- deployment metadata per space
- routing/proxy automation
- version tracking and rollback
- shared-hosting vs self-hosting distinction
- dashboard/backend visibility into deployment state

## Why This Matters

This is one of the clearest platform differentiators in the imported material:

MetaDyn is not just offering a Unity world. It is building a **deployable platform workflow** where creation, packaging, and hosting are part of one continuous product experience.
