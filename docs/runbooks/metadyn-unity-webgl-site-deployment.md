# MetaDyn Unity WebGL Site Deployment Runbook

Last updated: 2026-04-07

## Purpose

This runbook documents the standard pattern for creating a new nginx-served Unity WebGL site under `*.metadyn.xyz` on a MetaDyn SSL proxy host.

## Current Host Pattern

The current Hetzner host is used as a MetaDyn nginx SSL proxy and deployment target.

Expected conventions:

- web root parent: `/var/www/unity-webgl`
- site root: `/var/www/unity-webgl/<site-slug>`
- nginx site file: `/etc/nginx/sites-available/<full-domain>`
- enabled symlink: `/etc/nginx/sites-enabled/<full-domain>`
- shared certificate: `/etc/letsencrypt/live/metadyn.xyz/fullchain.pem`
- shared private key: `/etc/letsencrypt/live/metadyn.xyz/privkey.pem`

Do not reload or restart nginx unless explicitly requested.

Do not reference `/etc/letsencrypt/options-ssl-nginx.conf` or `/etc/letsencrypt/ssl-dhparams.pem` unless those files are confirmed present on the host.

## Required Input

Confirm the exact full domain before writing config.

Example:

```text
example.metadyn.xyz
```

Derive:

- `site_slug`: `example`
- `web_root`: `/var/www/unity-webgl/example`
- `nginx_file`: `/etc/nginx/sites-available/example.metadyn.xyz`

If the hostname is ambiguous or misspelled, stop and confirm it.

## Standard nginx Config

Replace `<full-domain>` and `<site-slug>`.

```nginx
server {
    if ($host = <full-domain>) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    listen [::]:80;
    server_name <full-domain>;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name <full-domain>;

    root /var/www/unity-webgl/<site-slug>;
    index index.html;

    ssl_certificate /etc/letsencrypt/live/metadyn.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/metadyn.xyz/privkey.pem;

    location ~* \.wasm\.br$ {
        types { }
        default_type application/wasm;
        add_header Content-Encoding br;
    }

    location ~* \.data\.br$ {
        types { }
        default_type application/octet-stream;
        add_header Content-Encoding br;
    }

    location ~* \.js\.br$ {
        types { }
        default_type application/javascript;
        add_header Content-Encoding br;
    }

    location ~* \.(data|wasm|symbols\.json)$ {
        gzip on;
        gzip_types application/octet-stream application/wasm;
        gzip_vary on;
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        try_files $uri $uri/ /index.html;

        add_header Access-Control-Allow-Origin '*' always;
        add_header Access-Control-Allow-Methods 'GET, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Content-Type' always;
    }

    client_max_body_size 200M;
}
```

## Procedure

1. Confirm the exact domain.
2. Derive the site slug from the subdomain.
3. Create the site root.

```bash
sudo install -d -m 755 /var/www/unity-webgl/<site-slug>
```

4. Add a placeholder `index.html` until the real Unity build is deployed.
5. Write the nginx config to `/etc/nginx/sites-available/<full-domain>`.
6. Enable the site.

```bash
sudo ln -sfn /etc/nginx/sites-available/<full-domain> /etc/nginx/sites-enabled/<full-domain>
```

7. Validate nginx syntax.

```bash
sudo nginx -t
```

8. Report whether nginx was reloaded. Do not reload unless explicitly requested.

## Build Deployment

Deploy Unity WebGL build contents into:

```text
/var/www/unity-webgl/<site-slug>/
```

Typical build contents:

- `index.html`
- `Build/`
- `StreamingAssets/`
- `TemplateData/`

Deployment layout can vary by site. Do not assume the local export layout matches the remote layout.

Dry run pattern:

```bash
rsync -avz --delete --dry-run --progress -e "ssh -i ~/.ssh/<keyfile>" /path/to/local/export/ root@<host-ip>:/var/www/unity-webgl/<site-slug>/
```

Live pattern:

```bash
rsync -avz --delete --progress -e "ssh -i ~/.ssh/<keyfile>" /path/to/local/export/ root@<host-ip>:/var/www/unity-webgl/<site-slug>/
```

Keep the trailing slash on the source if the intended behavior is to copy the contents of the local export into the remote site root.

## Verification Checklist

- Domain matches exactly.
- `server_name` matches exactly.
- `root` points to `/var/www/unity-webgl/<site-slug>`.
- Shared `metadyn.xyz` cert paths are used.
- Site file exists in `sites-available`.
- Symlink exists in `sites-enabled`.
- Web root exists.
- Placeholder or build `index.html` exists.
- `sudo nginx -t` passes.
- No reload or restart was performed unless explicitly requested.
- `rsync --dry-run` output was reviewed before first live deployment when practical.

## Operational Notes

- Keep changes minimal and reversible.
- Do not modify certificate paths unless explicitly requested.
- Do not change existing live sites while adding a new one.
- Confirm whether the remote should receive a full WebGL export or only the contents of a local `Build/` directory.
