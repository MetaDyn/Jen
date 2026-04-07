# Grafana Supabase Monitoring Runbook

Last updated: 2026-04-07

## Purpose

This runbook documents the conservative deployment pattern for using Grafana to monitor/query MetaDyn Supabase data from a MetaDyn nginx SSL proxy host.

The current example hostname is:

- `monitor.metadyn.xyz`

## Host Pattern

Follow the same pattern used for other MetaDyn internal apps:

- host nginx terminates public TLS on `:80` and `:443`
- the app listens only on loopback
- nginx proxies public HTTPS traffic to the loopback app port
- the shared MetaDyn wildcard certificate is reused
- credentials and secrets stay out of repository docs

For the current Hetzner host, Grafana is expected to run on:

```text
127.0.0.1:3001
```

This avoids colliding with Umami, which uses:

```text
127.0.0.1:3000
```

## Grafana Package Install

Use Grafana OSS from Grafana's official APT repository.

High-level package flow:

```bash
sudo apt-get install -y apt-transport-https wget gnupg
sudo install -d -m 755 /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/grafana.asc https://apt.grafana.com/gpg-full.key
sudo chmod 644 /etc/apt/keyrings/grafana.asc
printf '%s\n' 'deb [signed-by=/etc/apt/keyrings/grafana.asc] https://apt.grafana.com stable main' | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install -y grafana
```

After install, configure Grafana before exposing it publicly.

## Grafana Server Config

Edit:

```text
/etc/grafana/grafana.ini
```

Recommended settings for `monitor.metadyn.xyz`:

```ini
http_addr = 127.0.0.1
http_port = 3001
domain = monitor.metadyn.xyz
root_url = https://monitor.metadyn.xyz/
serve_from_sub_path = false
admin_user = admin
admin_password = REPLACE_WITH_LONG_RANDOM_PASSWORD
```

Do not commit the generated admin password.

Then enable and start Grafana:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now grafana-server
sudo systemctl status grafana-server --no-pager
```

Local health check:

```bash
curl -I http://127.0.0.1:3001/login
```

Expected:

```text
HTTP/1.1 200 OK
```

## nginx Reverse Proxy

Create:

```text
/etc/nginx/sites-available/monitor.metadyn.xyz
```

Use the host's shared wildcard certificate:

```nginx
server {
    if ($host = monitor.metadyn.xyz) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    listen [::]:80;
    server_name monitor.metadyn.xyz;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name monitor.metadyn.xyz;

    ssl_certificate /etc/letsencrypt/live/metadyn.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/metadyn.xyz/privkey.pem;

    client_max_body_size 20M;
    proxy_read_timeout 3600;
    proxy_send_timeout 3600;
    proxy_connect_timeout 300;

    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_http_version 1.1;

        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Ssl on;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
    }
}
```

Enable and validate:

```bash
sudo ln -sfn /etc/nginx/sites-available/monitor.metadyn.xyz /etc/nginx/sites-enabled/monitor.metadyn.xyz
sudo nginx -t
```

Only reload nginx after syntax validation passes:

```bash
sudo systemctl reload nginx
```

Local HTTPS verification:

```bash
curl -Ik --resolve monitor.metadyn.xyz:443:127.0.0.1 https://monitor.metadyn.xyz/login
```

Expected:

```text
HTTP/2 200
```

HTTP redirect verification:

```bash
curl -I --resolve monitor.metadyn.xyz:80:127.0.0.1 http://monitor.metadyn.xyz/
```

Expected:

```text
HTTP/1.1 301 Moved Permanently
Location: https://monitor.metadyn.xyz/
```

## DNS

Ensure DNS points to the MetaDyn host before expecting external access:

```text
monitor.metadyn.xyz -> MetaDyn nginx SSL host public IP
```

If local DNS does not resolve yet, use `curl --resolve` for on-host validation.

## Supabase Data Source Approach

Grafana should use a direct PostgreSQL datasource connection to Supabase.

Do not use the Supabase CLI as Grafana's live query path. The CLI is for development/admin workflows, not dashboard query serving.

Recommended Grafana datasource settings:

- Type: PostgreSQL
- Host: Supabase database host
- Database: usually `postgres`
- User: dedicated read-only user, for example `grafana_reader`
- Password: generated long random password
- SSL mode: `require`

## Production Database Safety

Using Grafana against production Supabase is acceptable only if access is narrow and read-only.

Main risks:

- accidentally granting write access
- exposing sensitive schemas or tables
- running expensive dashboard queries against production tables
- leaking datasource credentials
- allowing too many Grafana users to edit datasources or arbitrary SQL panels

Safer defaults:

- create a dedicated `grafana_reader` login
- grant only `CONNECT`, `USAGE`, and `SELECT`
- start with the `public` schema only
- avoid `auth` and `storage` unless explicitly required
- prefer reporting views or summary tables over raw large-table queries
- restrict datasource editing to trusted admins

## Minimal Supabase SQL

Use this first unless Grafana needs more than the `public` schema.

```sql
create role grafana_reader
with
  login
  password 'REPLACE_WITH_A_LONG_RANDOM_PASSWORD'
  nosuperuser
  nocreatedb
  nocreaterole
  noinherit;

grant connect on database postgres to grafana_reader;
grant usage on schema public to grafana_reader;
grant select on all tables in schema public to grafana_reader;
grant select on all sequences in schema public to grafana_reader;

alter default privileges in schema public
grant select on tables to grafana_reader;

alter default privileges in schema public
grant select on sequences to grafana_reader;
```

## Broader Supabase SQL

Only use this if Grafana genuinely needs additional Supabase-managed schemas.

```sql
create role grafana_reader
with
  login
  password 'REPLACE_WITH_A_LONG_RANDOM_PASSWORD'
  nosuperuser
  nocreatedb
  nocreaterole
  noinherit;

grant connect on database postgres to grafana_reader;

grant usage on schema public to grafana_reader;
grant usage on schema auth to grafana_reader;
grant usage on schema storage to grafana_reader;

grant select on all tables in schema public to grafana_reader;
grant select on all tables in schema auth to grafana_reader;
grant select on all tables in schema storage to grafana_reader;

grant select on all sequences in schema public to grafana_reader;
grant select on all sequences in schema auth to grafana_reader;
grant select on all sequences in schema storage to grafana_reader;

alter default privileges in schema public
grant select on tables to grafana_reader;

alter default privileges in schema auth
grant select on tables to grafana_reader;

alter default privileges in schema storage
grant select on tables to grafana_reader;

alter default privileges in schema public
grant select on sequences to grafana_reader;

alter default privileges in schema auth
grant select on sequences to grafana_reader;

alter default privileges in schema storage
grant select on sequences to grafana_reader;
```

## Notes

- The Supabase database name is usually `postgres` unless changed.
- `alter default privileges` only affects future objects created by the role that runs the statement.
- The safest long-term production setup is to expose only specific reporting views to Grafana.
- Never commit Grafana admin credentials, Supabase passwords, service-role keys, JWT secrets, or database URLs.
