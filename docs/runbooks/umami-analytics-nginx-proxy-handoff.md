# Umami Analytics nginx Proxy Handoff

Last updated: 2026-04-07

## Purpose

This runbook captures the current Umami analytics deployment pattern for the MetaDyn Hetzner nginx SSL host.

This is a sanitized operational handoff. Do not add database URLs, app secrets, passwords, tokens, private keys, or other secrets to this document.

## Host Role

The host is a MetaDyn nginx SSL proxy for `*.metadyn.xyz`.

Additional apps include:

- GitLab CE at `https://gitlab.metadyn.xyz`
- Umami analytics at `https://analytics.metadyn.xyz`

## Current Deployment Model

Umami is not running in Docker on this host.

Current pattern:

- Umami source install
- local PostgreSQL
- systemd service
- app listens only on `127.0.0.1:3000`
- host nginx terminates TLS and proxies to loopback
- public browser traffic stays on host nginx `:80` and `:443`

Known app version at setup time:

```text
v3.0.3
```

## Public Endpoints

Canonical analytics endpoints:

```text
https://analytics.metadyn.xyz
https://analytics.metadyn.xyz/script.js
https://analytics.metadyn.xyz/api/send
```

Do not use path-based historical examples such as `/analytics/script.js` as the current standard for this host.

## TLS

Use the existing shared wildcard certificate:

```text
/etc/letsencrypt/live/metadyn.xyz/fullchain.pem
/etc/letsencrypt/live/metadyn.xyz/privkey.pem
```

## Storage Layout

Umami was intentionally installed on the root disk rather than the extra Hetzner app volume.

Application layout:

```text
/opt/umami
/opt/umami/app
```

Config layout:

```text
/etc/umami/umami.env
```

The extra Hetzner volume already backs GitLab state and had shown read-only mount behavior during earlier work. Do not migrate Umami to the volume without a deliberate storage plan.

## Database

Umami uses local PostgreSQL 16 from apt.

Expected values:

```text
cluster: 16/main
database: umami
user: umami
listener: 127.0.0.1:5432
```

The database connection string is stored in:

```text
/etc/umami/umami.env
```

Do not commit that file or its values.

## Application Runtime

Dedicated service account:

```text
user: umami
home: /opt/umami
shell: /usr/sbin/nologin
```

Primary systemd unit:

```text
/etc/systemd/system/umami.service
```

Expected service behavior:

```text
User=umami
Group=umami
WorkingDirectory=/opt/umami/app/.next/standalone
EnvironmentFile=/etc/umami/umami.env
ExecStart=/usr/bin/node server.js
Restart=always
```

Important runtime note:

- Upstream Umami `scripts/start-env.js` failed under this host's Node 18 ESM resolution because it imports `next-start` without a `.js` suffix.
- A direct `pnpm start` invocation also misparsed CLI arguments in this environment.
- The stable host solution uses the standalone Next.js server output directly via systemd.

## nginx Configuration

Host nginx vhost:

```text
/etc/nginx/sites-available/analytics.metadyn.xyz
/etc/nginx/sites-enabled/analytics.metadyn.xyz
```

Expected behavior:

- `80` redirects to HTTPS
- `443` terminates TLS with the shared wildcard cert
- requests proxy to `http://127.0.0.1:3000`
- no additional public port is opened for Umami

Validate before reload:

```bash
sudo nginx -t
```

Only reload nginx after syntax validation passes and the change is explicitly approved:

```bash
sudo systemctl reload nginx
```

## Validation

Loopback heartbeat:

```bash
curl -I -H 'Host: analytics.metadyn.xyz' http://127.0.0.1:3000/api/heartbeat
```

Expected:

```text
HTTP/1.1 200 OK
```

nginx HTTPS path:

```bash
curl -Ik --resolve analytics.metadyn.xyz:443:127.0.0.1 https://analytics.metadyn.xyz/api/heartbeat
```

Expected:

```text
HTTP/2 200
```

HTTP redirect:

```bash
curl -I --resolve analytics.metadyn.xyz:80:127.0.0.1 http://analytics.metadyn.xyz/
```

Expected:

```text
HTTP/1.1 301 Moved Permanently
```

Service check:

```bash
sudo systemctl status umami --no-pager
```

## Tracking Context

Umami is intended to serve:

- standalone analytics UI at `analytics.metadyn.xyz`
- analytics backend for custom reporting inside `dashboard.metadyn.xyz`
- Unity WebGL and Hyperfy tracking workflows

Known example tracked Unity site at setup time:

```text
pavilion.metadyn.xyz
```

Known website ID at setup time:

```text
7c866698-3cf8-4e03-a451-1e1c48ae6d86
```

## Credential Handling

Upstream Umami's default initial login is:

```text
username: admin
password: umami
```

This default password should be changed immediately after first login.

Do not commit runtime secrets from `/etc/umami/umami.env`.

## Operational Caveats

- The host remains a production MetaDyn nginx SSL host.
- Future Umami changes should stay minimal and avoid broad nginx refactors.
- The shared wildcard cert is intentionally reused.
- Umami is currently on the root disk, not the extra Hetzner app volume.
- If the volume is repaired and remounted read-write later, migrate Umami only through a deliberate migration plan.
- Treat Umami as both a standalone analytics UI and a future backend data source for `dashboard.metadyn.xyz`.
