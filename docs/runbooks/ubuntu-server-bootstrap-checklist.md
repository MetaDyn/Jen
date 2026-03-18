# Ubuntu Server Bootstrap Checklist

Last updated: 2026-03-18

## Purpose

This is a basic first-pass checklist for preparing a fresh Ubuntu server to host MetaDyn-origin workloads behind the documented Cloudflare + nginx SSL proxy pattern.

This is intentionally practical and conservative. It is not a full production hardening guide, but it gives a solid initial baseline.

## Assumptions

- Ubuntu Server host
- SSH access already available
- you intend to run nginx as the public origin on the host
- Cloudflare manages the public DNS zone
- the host may serve either static Unity/WebGL content or reverse-proxy local apps such as Hyperfy/Node services

## 1. Update the host

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

After reconnecting:

```bash
sudo apt update
```

## 2. Create or confirm an admin user

If needed:

```bash
sudo adduser metadyn
sudo usermod -aG sudo metadyn
```

If you already have the right user, skip this.

## 3. Lock down SSH basics

Copy your SSH key if needed:

```bash
ssh-copy-id metadyn@your-server-ip
```

Check SSH daemon config:

```bash
sudo nano /etc/ssh/sshd_config
```

Recommended first-pass settings:

- `PermitRootLogin no`
- `PasswordAuthentication no` once key auth is confirmed
- `PubkeyAuthentication yes`

Validate and restart:

```bash
sudo sshd -t
sudo systemctl restart ssh
```

## 4. Install core packages

```bash
sudo apt install -y \
  nginx \
  certbot \
  python3-certbot-nginx \
  python3-pip \
  ufw \
  fail2ban \
  curl \
  wget \
  git \
  unzip \
  jq \
  rsync \
  htop
```

If using Cloudflare DNS validation with Certbot, also install the plugin if available for your Ubuntu release:

```bash
sudo apt install -y python3-certbot-dns-cloudflare
```

## 5. Enable the firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status verbose
```

## 6. Prepare app/content directories

For static Unity/WebGL hosting:

```bash
sudo mkdir -p /var/www/unity-webgl
sudo chown -R $USER:$USER /var/www/unity-webgl
```

For app-backed services, create a place for service repos/runtime files:

```bash
sudo mkdir -p /opt/metadyn
sudo chown -R $USER:$USER /opt/metadyn
```

## 7. Confirm nginx is installed and enabled

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx --no-pager
```

Test config:

```bash
sudo nginx -t
```

## 8. Create an nginx site config using the full MetaDyn pattern

### Static Unity/WebGL example

Create a site file:

```bash
sudo nano /etc/nginx/sites-available/example-space.metadyn.xyz
```

Use the full static-host pattern:

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name example-space.metadyn.xyz;

    return 301 https://$host$request_uri;
}

# HTTPS - Static Unity WebGL / app host
server {
    listen 443 ssl http2;
    server_name example-space.metadyn.xyz;

    root /var/www/unity-webgl/example-space;
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

### Reverse proxy example

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name hyperfy.metadyn.xyz;

    return 301 https://$host$request_uri;
}

# HTTPS - Reverse proxy to Hyperfy / Node app
server {
    listen 443 ssl http2;
    server_name hyperfy.metadyn.xyz;

    ssl_certificate /etc/letsencrypt/live/metadyn.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/metadyn.xyz/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://127.0.0.1:3001;
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

These are intentionally the full examples matching the current MetaDyn config patterns, not slimmed-down placeholders.

Enable the site and validate:

```bash
sudo ln -s /etc/nginx/sites-available/example-space.metadyn.xyz /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 9. Set up DNS in Cloudflare

For each hostname:

- create an `A` record pointing to the server IP
- or use the preferred DNS shape you already manage
- enable Cloudflare proxying if this host is meant to sit behind Cloudflare

Verify DNS:

```bash
dig +short example-space.metadyn.xyz
```

## 10. Obtain or install SSL certificates

### Option A: Certbot with nginx

If issuing directly for a hostname:

```bash
sudo certbot --nginx -d example-space.metadyn.xyz
```

### Option B: Cloudflare DNS validation

If using the Cloudflare DNS plugin and a credentials file:

```bash
sudo certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /root/.secrets/certbot/cloudflare.ini \
  -d metadyn.xyz \
  -d '*.metadyn.xyz'
```

Check installed certs:

```bash
sudo certbot certificates
```

Test renewals:

```bash
sudo certbot renew --dry-run
```

## 11. Deploy the application or static files

### Static content

```bash
mkdir -p /var/www/unity-webgl/example-space
# copy WebGL build output into that directory
```

### Node/Hyperfy-style app

Example:

```bash
cd /opt/metadyn
git clone <your-app-repo-url> app-name
cd app-name
npm install
```

If using a process manager:

```bash
sudo npm install -g pm2
pm2 start npm --name app-name -- start
pm2 save
pm2 startup
```

## 12. Verify end-to-end behavior

Check local nginx response:

```bash
curl -I http://localhost
curl -Ik https://localhost
```

Check the public hostname:

```bash
curl -I https://example-space.metadyn.xyz
```

If proxying an app, test upstream locally too:

```bash
curl -I http://127.0.0.1:3001
```

Check nginx logs:

```bash
sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log
```

## 13. Enable basic service persistence and monitoring

Useful checks:

```bash
systemctl list-units --type=service --state=running
pm2 status
sudo systemctl status nginx --no-pager
```

Optional but recommended next steps:

- configure log rotation where needed
- add monitoring/uptime checks
- add backup strategy for deployed assets/config
- document each hostname and origin mapping

## 14. Basic hardening follow-up

Good next steps after first bootstrap:

- install unattended security updates
- review open ports with `ss -tulpn`
- tighten SSH further if appropriate
- configure Fail2ban jails
- document which subdomains point to which services
- keep app services bound to localhost unless they truly need public exposure

Helpful commands:

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
ss -tulpn
sudo fail2ban-client status
```

## 15. Safe nginx change workflow

Use this every time you change nginx config:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Never reload first and hope.

## Quick Command Checklist

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y nginx certbot python3-certbot-nginx python3-pip ufw fail2ban curl wget git unzip jq rsync htop
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo systemctl enable nginx
sudo systemctl start nginx
sudo nginx -t
sudo certbot certificates
sudo certbot renew --dry-run
ss -tulpn
```

## Notes

This checklist is a baseline for initial setup only.

For MetaDyn specifically, the documented public ingress pattern assumes:

- Cloudflare in front
- nginx on the origin
- valid SSL on nginx
- per-hostname routing
- static or reverse-proxy origin mode depending on the workload

Related docs:
- `docs/infrastructure/nginx-ssl-proxy.md`
- `docs/infrastructure/topology.md`
- `docs/runbooks/cloudflare-jen-tunnel.md`
