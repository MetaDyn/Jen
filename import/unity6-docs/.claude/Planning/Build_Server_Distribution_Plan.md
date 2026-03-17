# Build Server Distribution Plan

## Goal
Offer SDK users a managed build pipeline so they can deploy without building locally, similar to Spatial.io. The Project Deployment component should allow switching between local build and a dedicated build server.

## Target Flow (High Level)
1. User selects "Build on Server" in the Deployment component.
2. Client packages source + config, then uploads to build server.
3. Build server produces WebGL build and bundles artifacts.
4. Artifacts are pushed to the target VM (or stored for later pull).
5. User receives a status report and deployment URL.

## Host Deployment API Direction

The planned production architecture is that the MetaDyn dashboard will call a new API running on the host server.

That host API will be responsible for provisioning and deploying either:
- a **Unity space template**, or
- a **Hyperfy space template**

This means the dashboard is the control plane, while the host server is the execution plane.

### Intended Request Flow
1. User chooses a space type in dashboard
   - Unity
   - Hyperfy
2. User selects subdomain / deployment options
3. Dashboard calls the host deployment API
4. Host API provisions the selected template
5. Host API generates config, routing, and deployment metadata
6. Host API activates the space and returns status to dashboard

### Host API Responsibilities
- authenticate and authorize dashboard deployment requests
- decide which template to provision
  - Unity template
  - Hyperfy template
- create deployment directory or instance
- generate runtime config
- generate/update nginx site config
- validate nginx config and reload safely
- return deployment status, logs, and public URL

### Why This Matters
- the dashboard does not need direct filesystem or nginx access
- deployment logic stays close to the host machine that actually serves the spaces
- the same API can later support:
  - one-click deploy
  - redeploy
  - stop/start
  - rollback
  - status checks

## Packaging Strategy
### Option A: Compressed Project Snapshot (Recommended)
- Create a filtered archive (zip/tar.gz) that excludes:
  - `/Library/`, `/Temp/`, `/Logs/`, `/.git/`
- Include:
  - `/Assets/`, `/Packages/`, `/ProjectSettings/`, build config
- Reason: fastest + smallest payload, deterministic build.

### Option B: Exported Unity Package
- Use Unity package export for assets + config.
- Not ideal for full build because scene/build settings can be incomplete.

## Build Server Pipeline
1. **Upload:** Receive archive + build config (target, quality, dev/prod, scene list).
2. **Extract:** Expand into a clean workspace.
3. **Build:** Invoke Unity batchmode build for WebGL.
4. **Bundle:** Produce build output + metadata (version, commit hash, build time).
5. **Deploy:** Push to VM via SSH/SCP or rsync (existing pattern).

## Build Artifact Bundling
- Output: `/Build` directory (Unity WebGL output)
- Wrap in:
  - `build.zip` (for transport) + `manifest.json`
- Manifest fields: buildId, timestamp, version, unityVersion, gitCommit, targetUrl

## Deployment Options
### Option 1: Server Push to VM (Most seamless)
- Build server uses SSH keys to push to VM.
- Mirrors current Project Deployment rsync/scp workflow.

### Option 2: Client Pull from Build Server
- Build server stores artifacts; client triggers download to VM.
- Useful when VM credentials are not shared with build server.

## Security Model
- Upload requires auth token tied to org/project.
- Build server runs in isolated containers per build.
- Secrets stored in secure vault; short-lived SSH keys for deploy.
- Logs accessible to user; private by default.

## UI/SDK Changes (Deployment Component)
- Add build mode toggle: **Local Build** / **Build Server**
- Add build server URL + API token field
- Add progress/status panel (queue, building, deploying)

## Incremental Rollout
1. **Phase 1:** Build server produces artifacts only; user downloads or manual deploy.
2. **Phase 2:** Build server deploys to VM with SSH integration.
3. **Phase 3:** Full automation + dashboard build history + rollback.

## Template-Based Space Provisioning

For the current MetaDyn direction, deployment is no longer only "build artifacts to VM".
It also includes template provisioning on the host.

Two initial deployment modes should be supported:

### Unity Space Template
- provision a static Unity WebGL deployment target
- copy or sync the built Unity files into the correct host directory
- apply nginx static-host config using the project proxy template

### Hyperfy Space Template
- provision a Hyperfy instance or space directory
- write runtime/environment config for that space
- apply nginx reverse-proxy config for the assigned hostname

### Shared Pattern
Both deployment modes should go through the same host deployment API so the dashboard can offer one operator workflow while branching internally by template type.

## Open Questions
- Should build server be multi-tenant or per-org?
- Do we support custom Unity versions or fixed versions only?
- How are build caches handled for speed?


## Dashboard Integration (UI/UX)
- **Build Queue View:** Status cards (Queued, Building, Deploying, Failed, Complete).
- **Build History:** Versioned list with timestamps, commit hash, Unity version.
- **Rollback:** One-click restore to prior build on the VM/CDN.
- **Logs:** Streaming build logs + deploy logs with download/export.
- **Artifacts:** Download build.zip + manifest.json for manual deployment.

## Security & Ops
- **Auth:** API tokens scoped per org/project.
- **Isolation:** Per-build container/workspace; auto-clean after build.
- **Secrets:** Store SSH keys and tokens in vault; issue short-lived deploy creds.
- **Auditing:** Record who triggered builds, target VM, and artifact checksum.
- **Rate Limits:** Prevent abuse and control costs.

## Observability
- **Metrics:** Build duration, queue time, artifact size, deploy time.
- **Alerts:** Build failures, deploy failures, and VM connectivity issues.
- **Health:** Build server status endpoint for SDK to surface.
