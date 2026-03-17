# Pavilion Web Shell Options Simple Plan

## Best First Path

Use the dashboard as the Pavilion shell first.

Why:

- it already has working Supabase auth in `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/contexts/AuthContext.tsx`
- it already handles Unity/world redirect flow in `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/App.tsx`
- it already has an authenticated app frame in `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/components/layout/DashboardLayout.tsx`

`website-v2` is still mostly a marketing site, not an authenticated product shell.

## Simple Recommendation

### Phase 1

Put Pavilion behind the dashboard.

Build:

- one new dashboard page for Pavilion/world launch
- one Unity container component
- one clean launch mode:
  - preferably full-window
  - second-best is reduced chrome

### Phase 2

Let `website-v2` link into the dashboard/world experience.

Examples:

- `Launch Platform`
- `Open Pavilion`
- `Go to Dashboard`

### Phase 3

Only later decide whether `website-v2` should become the true shell.

Do that only if you want:

- the public website and product to feel like one application
- auth and product UX to live in the main site

## What Each Option Really Costs

### Dashboard shell

Smaller job.

Needs:

- Pavilion page
- Unity embed/full-window route
- launch/failure/loading states

### Website-v2 shell

Bigger job.

Needs:

- Supabase auth layer
- protected routes
- user shell/layout
- Pavilion route
- coordination with dashboard auth/session behavior

## Decision

If the goal is fastest practical result:

- dashboard first

If the goal is highest brand cohesion later:

- website-v2 can become the front door, but not the first implementation shell
