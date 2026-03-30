# Cloudflare Tunnel For Jen

## Purpose

This runbook captures the recommended path for putting `jen.metadyn.xyz` in front of the local OpenClaw control surface with HTTPS.

The preferred architecture is:

- `jen.metadyn.xyz`
- Cloudflare Tunnel
- Cloudflare Access
- local OpenClaw gateway bound to `127.0.0.1:18789`

This avoids directly exposing the OpenClaw admin surface to the public internet.

## Why Tunnel Instead Of Direct Public Proxy

OpenClaw is an operator/admin surface, not a generic public website.

The safer pattern is:

- keep OpenClaw local-only on the host
- terminate public access through Cloudflare
- require Cloudflare Access authentication before the dashboard is reachable

This is preferable to:

- exposing the host IP directly
- opening inbound firewall ports to the dashboard
- depending on `dangerouslyDisableDeviceAuth` for normal operation

## Target Result

After setup, the intended flow is:

- user visits `https://jen.metadyn.xyz`
- Cloudflare Access prompts for identity/auth
- Cloudflare Tunnel forwards traffic to `http://127.0.0.1:18789`
- OpenClaw remains loopback-only on the host

## What Is Needed

For a headless server, the recommended inputs are:

- Cloudflare account that owns `metadyn.xyz`
- `account_id`
- either:
  - a scoped Cloudflare API token
  - or a tunnel token created from the Cloudflare dashboard on another machine

Avoid relying on:

- legacy `cloudflare.ini`
- broad global API keys

## Recommended Cloudflare Permissions

If using an API token, keep it narrowly scoped.

Typical minimum needs:

- Account: Cloudflare Tunnel write/edit permissions
- Zone: DNS edit permissions for `metadyn.xyz`

If Cloudflare Access is also being provisioned by API, additional Access-related permissions may be needed.

## Local OpenClaw Changes Expected

When `jen.metadyn.xyz` is ready, the local OpenClaw config should move back toward a safer posture:

- bind gateway to `127.0.0.1`
- remove or disable LAN-only unsafe overrides where possible
- remove `dangerouslyDisableDeviceAuth=true`
- treat Cloudflare Access as the outer trust boundary

## High-Level Steps

1. Install `cloudflared` on the host.
2. Create or receive a Cloudflare Tunnel token.
3. Create a tunnel that forwards to `http://127.0.0.1:18789`.
4. Route `jen.metadyn.xyz` to that tunnel in Cloudflare DNS.
5. Configure Cloudflare Access for the hostname.
6. Run `cloudflared` as a persistent service.
7. Re-lock OpenClaw to loopback-only operation.
8. Verify:
   - HTTPS page load
   - dashboard auth flow
   - WebSocket connection through Cloudflare

## Notes For This Host

Current local context:

- OpenClaw currently runs on port `18789`
- host LAN IP has been `192.168.0.201`
- this server is headless
- prior LAN testing used temporary insecure settings to make the dashboard reachable over HTTP

Those settings were useful for internal testing, but they should not be treated as the final public ingress model.

## Headless Workflow Preference

Because the host is headless, the easiest operational path is usually one of:

- create the tunnel in Cloudflare dashboard on another machine, then copy the tunnel token here
- or use a scoped API token and create the tunnel from CLI/API on the host

The browser-driven `cloudflared tunnel login` flow is not the preferred primary path for this machine.
