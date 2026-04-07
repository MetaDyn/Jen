# GitLab CE nginx Proxy Handoff

Last updated: 2026-04-07

## Purpose

This runbook captures the current GitLab CE deployment pattern for the MetaDyn Hetzner nginx SSL host.

This is a sanitized operational handoff. Do not add GitLab initial passwords, tokens, private keys, database URLs, or other secrets to this document.

## Host Role

The host is a MetaDyn nginx SSL proxy for `*.metadyn.xyz`.

Additional app:

- GitLab CE at `https://gitlab.metadyn.xyz`

## Current Deployment Model

- Package: `gitlab-ce`
- Known installed version at setup time: `18.10.1-ce.0`
- HTTPS terminates at host nginx using the existing MetaDyn wildcard certificate.
- GitLab's bundled nginx remains enabled only as an internal loopback listener.
- Public traffic should not connect directly to GitLab's internal listener.

## TLS

Use the existing shared wildcard certificate:

```text
/etc/letsencrypt/live/metadyn.xyz/fullchain.pem
/etc/letsencrypt/live/metadyn.xyz/privkey.pem
```

GitLab's own Let's Encrypt automation is intentionally disabled because host nginx terminates TLS.

## Storage Layout

GitLab mutable data is intended to live on the Hetzner volume:

```text
/mnt/HC_Volume_105018844/apps/gitlab
```

Expected subpaths:

```text
/mnt/HC_Volume_105018844/apps/gitlab/var-opt
/mnt/HC_Volume_105018844/apps/gitlab/var-log
/mnt/HC_Volume_105018844/apps/gitlab/backups
```

Bind mounts:

```text
/var/opt/gitlab -> /mnt/HC_Volume_105018844/apps/gitlab/var-opt
/var/log/gitlab -> /mnt/HC_Volume_105018844/apps/gitlab/var-log
```

Persistent mount configuration lives in:

```text
/etc/fstab
```

If GitLab storage problems occur, check:

```bash
mount
findmnt
grep gitlab /etc/fstab
test -w /mnt/HC_Volume_105018844/apps/gitlab && echo writable
```

## GitLab Configuration

Primary config:

```text
/etc/gitlab/gitlab.rb
```

Key intended settings:

```ruby
external_url 'https://gitlab.metadyn.xyz'
letsencrypt['enable'] = false
nginx['listen_addresses'] = ['127.0.0.1']
nginx['listen_port'] = 8060
nginx['listen_https'] = false
gitlab_rails['trusted_proxies'] = ['127.0.0.1']
gitlab_rails['gitlab_shell_ssh_port'] = 22
gitlab_rails['backup_path'] = '/mnt/HC_Volume_105018844/apps/gitlab/backups'
gitlab_rails['manage_backup_path'] = false
registry['enable'] = false
registry_nginx['enable'] = false
```

Alertmanager loopback settings may be required on this host:

```ruby
alertmanager['flags']['web.listen-address'] = '127.0.0.1:9093'
alertmanager['flags']['cluster.listen-address'] = '127.0.0.1:9094'
alertmanager['flags']['cluster.advertise-address'] = '127.0.0.1:9094'
```

## nginx Configuration

Host nginx vhost:

```text
/etc/nginx/sites-available/gitlab.metadyn.xyz
/etc/nginx/sites-enabled/gitlab.metadyn.xyz
```

Expected behavior:

- `80` redirects to HTTPS
- `443` terminates TLS with the shared wildcard cert
- requests proxy to `http://127.0.0.1:8060`

Validate before reload:

```bash
sudo nginx -t
```

Only reload nginx after syntax validation passes and the change is explicitly approved:

```bash
sudo systemctl reload nginx
```

## Validation

GitLab backend check:

```bash
curl -I -H 'Host: gitlab.metadyn.xyz' http://127.0.0.1:8060/users/sign_in
```

nginx HTTPS path check:

```bash
curl -I --resolve gitlab.metadyn.xyz:443:127.0.0.1 https://gitlab.metadyn.xyz/users/sign_in
```

Expected:

```text
HTTP/2 200
```

Service check:

```bash
sudo gitlab-ctl status
```

Expected major services include:

- `alertmanager`
- `gitaly`
- `gitlab-exporter`
- `gitlab-kas`
- `gitlab-workhorse`
- `logrotate`
- `nginx`
- `node-exporter`
- `postgres-exporter`
- `postgresql`
- `prometheus`
- `puma`
- `redis`
- `redis-exporter`
- `sidekiq`

## Credential Handling

Default admin username:

```text
root
```

The initial password file path may exist temporarily:

```text
/etc/gitlab/initial_root_password
```

Do not commit the initial password value. Change the GitLab root password immediately after first login.

## Operational Caveats

- The host remains a production MetaDyn nginx SSL host.
- Avoid broad nginx refactors.
- Keep GitLab behind the host nginx proxy.
- Do not re-enable GitLab's internal Let's Encrypt unless the TLS strategy changes.
- GitLab data is on the extra volume, but `/etc/gitlab` remains on the root disk.
- Container registry is disabled unless intentionally enabled later with storage planning.
- SSH for Git operations remains on the host's normal port `22`.
