# Generic Unity / Web App Nginx SSL Proxy Template

Use this as a copy-forward template for a new project that needs:
- name-based host resolution
- HTTP to HTTPS redirect
- Let's Encrypt SSL termination
- static Unity WebGL hosting

Replace these placeholders before use:
- `<APP_HOSTNAME>`
- `<APP_ROOT>`
- `<LETSENCRYPT_CERT_NAME>`

Example substitutions:
- `<APP_HOSTNAME>` -> `pavilion.metadyn.xyz`
- `<APP_ROOT>` -> `/var/www/unity-webgl/pavilion`
- `<LETSENCRYPT_CERT_NAME>` -> `metadyn.xyz`

## Generic Template

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name <APP_HOSTNAME>;

    return 301 https://$host$request_uri;
}

# HTTPS - Static Unity WebGL / app host
server {
    listen 443 ssl http2;
    server_name <APP_HOSTNAME>;

    root <APP_ROOT>;
    index index.html;

    ssl_certificate /etc/letsencrypt/live/<LETSENCRYPT_CERT_NAME>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<LETSENCRYPT_CERT_NAME>/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Brotli compressed WASM files - most specific first
    location ~* \.wasm\.br$ {
        types { }
        default_type application/wasm;
        add_header Content-Encoding br;
    }

    # Brotli compressed data files
    location ~* \.data\.br$ {
        types { }
        default_type application/octet-stream;
        add_header Content-Encoding br;
    }

    # Brotli compressed JS files
    location ~* \.js\.br$ {
        types { }
        default_type application/javascript;
        add_header Content-Encoding br;
    }

    # Regular WASM and data files
    location ~* \.(data|wasm|symbols\.json)$ {
        gzip on;
        gzip_types application/octet-stream application/wasm;
        gzip_vary on;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Main app route
    location / {
        try_files $uri $uri/ /index.html;

        # Useful for Unity WebGL/browser clients
        add_header Access-Control-Allow-Origin '*' always;
        add_header Access-Control-Allow-Methods 'GET, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Content-Type' always;
    }

    client_max_body_size 200M;
}
```

## Notes

- Use this template for static Unity/WebGL style deployments where Nginx serves files directly from disk.
- If the project is a Node app behind Nginx instead of static hosting, replace the `location /` block with a `proxy_pass` block.
- Standard MetaDyn default: use the wildcard/apex certificate lineage `metadyn.xyz` for `*.metadyn.xyz` deployments.
- Only use a hostname-specific certificate lineage if there is a deliberate exception to the wildcard-domain standard.
- For multi-subdomain projects, keep one server block per hostname unless you intentionally move to a wildcard routing pattern.

## Automation Guidance

This template is suitable for future one-click provisioning as long as the deploy system can fill in the placeholder values and write the generated config into the correct Nginx location.

### Required Automation Inputs

- `hostname`
- `app_root`
- `cert_name`
- `site_config_name`
- `nginx_sites_available_path`
- `nginx_sites_enabled_path`

### Expected Automation Flow

1. Copy this template
2. Replace:
   - `<APP_HOSTNAME>`
   - `<APP_ROOT>`
   - `<LETSENCRYPT_CERT_NAME>`
3. Write the result to:
   - `/etc/nginx/sites-available/<site_config_name>`
4. Symlink into:
   - `/etc/nginx/sites-enabled/<site_config_name>`
5. Run:
   - `nginx -t`
6. Reload Nginx only if the config test succeeds

### Intended Provisioning Model

This template is meant to be consumed by the future host deployment API described in `../Planning/Build_Server_Distribution_Plan.md`.

That API should allow the dashboard to request provisioning of:
- a Unity space template, or
- a Hyperfy space template

For Unity/static deployments, this file can be used directly as the generated nginx site config baseline.

### Validation Rules For Automation

- `hostname` must already resolve or be provisioned in DNS
- `app_root` must exist before enabling the site
- `cert_name` must point to an existing certificate lineage under `/etc/letsencrypt/live/`
- generated config names should be deterministic and safe for filesystem use

### Variants

- **Static Unity/WebGL app**
  - keep the template as written

- **Node/Hyperfy app**
  - replace the `location /` block with a reverse proxy block
  - keep the same hostname + SSL structure

- **Wildcard/shared-host routing**
  - use this as the per-host baseline
  - move to wildcard `server_name` only when the runtime/router is intentionally designed for it
