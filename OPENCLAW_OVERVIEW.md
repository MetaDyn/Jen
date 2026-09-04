# OpenClaw Overview

Last updated: 2026-03-16

This is a working notes document for the local OpenClaw install on this host. It mixes official documentation with a few practical notes from the current setup so there is one place to start from.

## What OpenClaw Is

OpenClaw is a gateway-centered orchestration layer for AI agents. The model is only one part of the system. OpenClaw provides the long-lived gateway, browser control UI, channel integrations, node/device pairing, routing, plugin loading, and local state/config management around the model.

Official references:

- Docs home: https://docs.openclaw.ai/
- Gateway architecture: https://docs.openclaw.ai/concepts/architecture
- CLI reference: https://docs.openclaw.ai/cli

## Core Mental Model

- One host runs one Gateway process.
- The Gateway owns messaging surfaces and the main WebSocket API.
- Browser operators, CLI tools, automations, and paired nodes all connect to that Gateway.
- Channels route messages into the Gateway; the configured model/provider does reasoning; OpenClaw handles delivery, tools, sessions, and policy.

From the official docs, current high-level components are:

- Gateway / WebSocket server
- Control UI / dashboard
- Channel connectors such as WhatsApp, Telegram, Discord, Slack, Signal, and iMessage support depending on platform/setup
- Nodes for macOS, iOS, Android, and headless companions
- Plugins and skills
- Multi-agent routing with isolated workspaces and sessions

## Capability Snapshot

Based on the official docs and the installed CLI, this OpenClaw build supports:

- Browser Control UI served from the gateway port
- Agent chat and session management
- Channel integrations and deterministic reply routing
- Device pairing for new browsers and nodes
- Nodes with commands such as canvas, camera, notifications, system actions, and other device-specific features
- Plugins that can add RPC methods, HTTP handlers, agent tools, CLI commands, background services, and skills
- Health checks, logs, security audits, and configuration helpers

References:

- Features: https://docs.openclaw.ai/concepts/features
- Control UI: https://docs.openclaw.ai/web/control-ui
- Nodes: https://docs.openclaw.ai/nodes
- Plugins: https://docs.openclaw.ai/tools/plugin
- Channels and routing: https://docs.openclaw.ai/channels/channel-routing

## Local Install Notes

Current local config file:

- `~/.openclaw/openclaw.json`

Current local install details observed on this machine:

- Installed CLI version: `2026.3.13`
- Gateway port: `18789`
- Primary runtime model (confirmed 2026-09-04): `openai-codex/gpt-6-astra`
- Workspace path: `~/.openclaw/workspace`

## Local Access Notes

OpenClaw’s dashboard is the Control UI served from the same host/port as the gateway:

- Local default: `http://127.0.0.1:18789/`
- CLI helper: `openclaw dashboard`
- Gateway start: `openclaw gateway`

The official docs currently note:

- `openclaw gateway` is the standard run command
- `openclaw gateway run` is a foreground alias
- `openclaw dashboard --no-open` prints the current dashboard URL
- For SecretRef-managed tokens, `dashboard` may intentionally print a non-tokenized URL to avoid leaking secrets

References:

- Gateway CLI: https://docs.openclaw.ai/cli/gateway
- Dashboard CLI: https://docs.openclaw.ai/cli/dashboard
- Dashboard docs: https://docs.openclaw.ai/web/dashboard

## Remote Access Notes

Official guidance strongly prefers:

- `localhost`
- Tailscale Serve / tailnet access
- SSH tunneling

Why: the Control UI is an admin surface, and remote plain HTTP has security and browser secure-context limitations.

Important current behavior from the docs:

- Non-loopback Control UI deployments must explicitly set `gateway.controlUi.allowedOrigins`
- Remote dev or remote UI access may require `gatewayUrl` and explicit auth
- `dangerouslyDisableDeviceAuth` bypasses Control UI device identity checks, but the docs describe it as a severe security downgrade
- Plain `http://<lan-ip>` runs in a non-secure browser context, which blocks WebCrypto and causes the Control UI device-identity problem unless you use HTTPS, localhost, or the break-glass flag

References:

- Web surfaces: https://docs.openclaw.ai/web
- Control UI remote access details: https://docs.openclaw.ai/web/control-ui

## Current Host-Specific State

This host was adjusted to allow LAN access during setup troubleshooting:

- Gateway bind changed from `loopback` to `lan`
- Allowed origin added for `http://192.168.0.201:18789`
- `gateway.controlUi.dangerouslyDisableDeviceAuth=true` enabled temporarily so the dashboard can load over plain HTTP on LAN

That last setting is convenient for testing, but it is not the recommended steady-state setup. The safer next step is:

1. Put the Control UI behind HTTPS, Tailscale Serve, or an SSH tunnel
2. Remove `dangerouslyDisableDeviceAuth`
3. Rotate the gateway token after testing

## Good Commands To Know

```bash
openclaw gateway
openclaw dashboard
openclaw dashboard --no-open
openclaw status
openclaw health
openclaw config file
openclaw config get gateway.auth.token
openclaw plugins list
openclaw channels login --channel whatsapp
openclaw security audit
```

## Likely Documentation Next Steps

- Add a host-specific runbook for this machine: start, stop, restart, logs, token rotation
- Add a safer remote-access guide: SSH tunnel or Tailscale Serve
- Add a channel-specific guide if you plan to use WhatsApp, Telegram, or Discord
- Add a plugin evaluation page listing which extensions are worth enabling for this environment

## Sources Used

- https://docs.openclaw.ai/
- https://docs.openclaw.ai/concepts/architecture
- https://docs.openclaw.ai/cli
- https://docs.openclaw.ai/cli/gateway
- https://docs.openclaw.ai/cli/dashboard
- https://docs.openclaw.ai/web
- https://docs.openclaw.ai/web/control-ui
- https://docs.openclaw.ai/web/dashboard
- https://docs.openclaw.ai/nodes
- https://docs.openclaw.ai/tools/plugin
- https://docs.openclaw.ai/channels/channel-routing
- https://docs.openclaw.ai/concepts/features
