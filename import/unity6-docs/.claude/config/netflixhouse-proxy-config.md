# NetflixHouse Nginx SSL Proxy Config

This config is based on the generic Unity / Web App Nginx SSL Proxy Template and is ready to use for the NetflixHouse Unity project.

Project values:
- Hostname: `netflixhouse.metadyn.xyz`
- App root: `/var/www/unity-webgl/netflixhouse`
- Certificate lineage: `metadyn.xyz`
- Standard MetaDyn wildcard cert paths:
  - `/etc/letsencrypt/live/metadyn.xyz/fullchain.pem`
  - `/etc/letsencrypt/live/metadyn.xyz/privkey.pem`

## Nginx Config

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name netflixhouse.metadyn.xyz;

    return 301 https://$host$request_uri;
}

# HTTPS - Static Unity WebGL / app host
server {
    listen 443 ssl http2;
    server_name netflixhouse.metadyn.xyz;

    root /var/www/unity-webgl/netflixhouse;
    index index.html;

    ssl_certificate /etc/letsencrypt/live/metadyn.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/metadyn.xyz/privkey.pem;
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

        add_header Access-Control-Allow-Origin '*' always;
        add_header Access-Control-Allow-Methods 'GET, OPTIONS' always;
        add_header Access-Control-Allow-Headers 'Content-Type' always;
    }

    client_max_body_size 200M;
}
```

## Notes

- Root path assumed: `/var/www/unity-webgl/netflixhouse`
- Certificate lineage assumed: wildcard/apex `metadyn.xyz`
- This project is using the standard MetaDyn wildcard certificate lineage, not a hostname-specific certificate
- If the deployment root changes, update the `root` line before use
- Generic template source: `.claude/config/unity-proxy-config.md`
