# Generic Hyperfy / Node App Nginx SSL Proxy Template

Use this as a copy-forward template for a new project that needs:
- name-based host resolution
- HTTP to HTTPS redirect
- Let's Encrypt SSL termination
- reverse proxying to a Hyperfy or other Node-based app
- websocket upgrade support

Replace these placeholders before use:
- `<APP_HOSTNAME>`
- `<UPSTREAM_URL>`
- `<LETSENCRYPT_CERT_NAME>`

Example substitutions:
- `<APP_HOSTNAME>` -> `hyperfy.metadyn.xyz`
- `<UPSTREAM_URL>` -> `http://127.0.0.1:3001`
- `<LETSENCRYPT_CERT_NAME>` -> `metadyn.xyz`

## Generic Template

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name <APP_HOSTNAME>;

    return 301 https://$host$request_uri;
}

# HTTPS - Reverse proxy to Hyperfy / Node app
server {
    listen 443 ssl http2;
    server_name <APP_HOSTNAME>;

    ssl_certificate /etc/letsencrypt/live/<LETSENCRYPT_CERT_NAME>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<LETSENCRYPT_CERT_NAME>/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass <UPSTREAM_URL>;
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

## Notes

- Use `127.0.0.1` instead of `0.0.0.0` for the upstream target unless you have a specific reason not to.
- This template is appropriate for Hyperfy and similar Node apps that serve both HTTP and websocket traffic from one upstream.
- Standard MetaDyn default: use the wildcard/apex certificate lineage `metadyn.xyz` for `*.metadyn.xyz` deployments.
- Only use a hostname-specific certificate lineage if there is a deliberate exception to the wildcard-domain standard.
- Keep one server block per hostname unless you intentionally move to a wildcard/shared-router design.

## Automation Guidance

This template is suitable for future one-click provisioning as long as the deploy system can fill in the placeholder values and write the generated config into the correct Nginx location.

### Required Automation Inputs

- `hostname`
- `upstream_url`
- `cert_name`
- `site_config_name`
- `nginx_sites_available_path`
- `nginx_sites_enabled_path`

### Expected Automation Flow

1. Copy this template
2. Replace:
   - `<APP_HOSTNAME>`
   - `<UPSTREAM_URL>`
   - `<LETSENCRYPT_CERT_NAME>`
3. Write the result to:
   - `/etc/nginx/sites-available/<site_config_name>`
4. Symlink into:
   - `/etc/nginx/sites-enabled/<site_config_name>`
5. Run:
   - `nginx -t`
6. Reload Nginx only if the config test succeeds

### Validation Rules For Automation

- `hostname` must already resolve or be provisioned in DNS
- `upstream_url` must point to a running or soon-to-be-started local app instance
- `cert_name` must point to an existing certificate lineage under `/etc/letsencrypt/live/`
- generated config names should be deterministic and safe for filesystem use

### Intended Provisioning Model

This template is meant to be consumed by the future host deployment API described in `../Planning/Build_Server_Distribution_Plan.md`.

That API should allow the dashboard to request provisioning of:
- a Unity space template, or
- a Hyperfy space template

For Hyperfy/Node deployments, this file can be used directly as the generated nginx site config baseline.
