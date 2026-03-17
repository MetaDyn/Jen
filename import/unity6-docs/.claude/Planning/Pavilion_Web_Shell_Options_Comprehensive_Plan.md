# Pavilion Web Shell Options Comprehensive Plan

## Purpose

This document compares the two realistic shell options around MetaDyn Pavilion:

1. Use the existing dashboard as the authenticated shell
2. Use `MetaDyn/Dev/website-v2` as the shell

The goal is to outline what is already present in code, what is missing, and which path is the smaller and safer implementation.

## Current Code Reality

### Dashboard already behaves like an app shell

The dashboard codebase already has:

- session-aware auth state via Supabase in `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/contexts/AuthContext.tsx`
- redirect handling for Unity/world launch via `redirect` query param in `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/App.tsx`
- login/signup pages that already honor redirect flow in:
  - `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/pages/LoginPage.tsx`
  - `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/pages/SignUpPage.tsx`
- a persistent authenticated frame in:
  - `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/components/layout/DashboardLayout.tsx`
  - `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/components/layout/Header.tsx`
  - `/mnt/c/Metaverse/MetaDyn/Dev/dashboard-scaffolding/components/layout/Sidebar.tsx`

This means the dashboard is already structurally an application wrapper.

### Website-v2 is still a marketing site, not an application shell

`website-v2` currently has:

- a single marketing-site root layout in `/mnt/c/Metaverse/MetaDyn/Dev/website-v2/app/layout.tsx`
- a long landing page in `/mnt/c/Metaverse/MetaDyn/Dev/website-v2/app/page.tsx`
- documentation that mentions shared auth as a future/related integration in `/mnt/c/Metaverse/MetaDyn/Dev/website-v2/claude.md`

What it does not visibly have in its active `app/` code:

- live Supabase auth provider
- protected routes
- session-aware user shell
- a dashboard/app frame
- Unity launcher or embed route

So `website-v2` is currently better described as the public-facing MetaDyn site, not the logged-in product shell.

## Recommendation

Use the dashboard as the first Pavilion shell.

Reason:

- it already owns the live auth/session layer
- it already knows how to redirect back to a world URL
- it already has authenticated application chrome
- it is less work and less risk than turning `website-v2` into a product shell first

Use `website-v2` later as:

- the public funnel
- the marketing/brand entry point
- a launcher into dashboard/world routes

## Option A: Dashboard as the Pavilion Shell

### What already exists

- Supabase auth state and token cookie management in `AuthContext.tsx`
- auth-gated app root in `App.tsx`
- login and signup flows already aligned with redirect-based world launch
- persistent application layout in `DashboardLayout.tsx`

### What would need to be added

#### 1. A dedicated Pavilion route/screen inside the dashboard

Needed deliverable:

- a new nav item or dedicated route such as `world`, `spaces/:id/launch`, or `pavilion`

Possible implementation shapes:

- full-window Unity page inside dashboard app routing
- embedded Unity `iframe` inside dashboard content area
- minimal “launch page” that removes most chrome and focuses on the world

#### 2. A Unity container component

Needed deliverable:

- a React component responsible for rendering the Unity WebGL entry

Likely responsibilities:

- world URL selection
- loading state and error state
- mobile/incompatible browser messaging
- optional pass-through launch parameters

#### 3. Decide app chrome behavior while in-world

Three realistic modes:

1. Full dashboard chrome
   - sidebar/header remain visible
   - easiest to implement
   - worst for available viewport

2. Reduced chrome mode
   - minimal top bar only
   - better for WebGL use

3. World-first full-window mode
   - Unity takes the full viewport
   - dashboard acts mostly as auth/session launcher
   - best UX for real use

The third mode is likely the right end state.

#### 4. Launch contract between shell and Pavilion

Need to standardize:

- which world/space ID is being launched
- whether auth is handled by cookie only or by explicit token handoff
- whether wrapper passes metadata in query params
- whether Unity is embedded or opened as a separate origin/page

#### 5. Session/failure UX

Need explicit behavior for:

- expired session
- failed auth handoff
- mobile/iOS unsupported state
- reload/rejoin after app crash

### Dashboard-shell advantages

- smallest implementation delta
- uses code that already exists
- easiest place to centralize auth fixes
- clean place for user/profile/space/favorites launch flows

### Dashboard-shell risks

- dashboard layout may feel too “admin/product” for immersive world entry
- if Unity stays inside the full dashboard chrome, available viewport will be poor
- dashboard currently uses internal state navigation, not a more formal route system

## Option B: Website-v2 as the Pavilion Shell

### What already exists

- public-facing MetaDyn brand/site shell
- strong visual presentation
- good top-of-funnel environment for showcasing Pavilion

### What is missing

To make `website-v2` the real Pavilion shell, it would first need:

#### 1. Authentication layer

Missing pieces:

- Supabase client integration in active site runtime
- auth provider/context
- session bootstrap
- login/signup UI or redirect flow
- protected app routes

#### 2. Product shell

Missing pieces:

- account-aware layout
- user menu/profile/session handling
- authenticated navigation separate from the marketing page

#### 3. Dedicated world route

Missing pieces:

- page such as `/platform`, `/app`, `/world`, or `/spaces/[slug]`
- Unity container
- launch/fallback/error UX

#### 4. Shared auth behavior with dashboard

If website and dashboard both become auth entry points, they must stay aligned on:

- session ownership
- cookie/token behavior
- logout semantics
- user profile updates

That increases complexity.

### Website-shell advantages

- stronger branded experience
- cleaner public-to-product journey
- good if the requirement is “Pavilion lives inside the main MetaDyn site”

### Website-shell risks

- materially more implementation work
- duplicates auth shell work already present in dashboard
- higher chance of auth drift between website and dashboard
- would delay getting a stable Pavilion wrapper online

## Suggested Delivery Sequence

### Phase 1: Use dashboard as the working shell

Build:

- a dedicated Pavilion launch page inside dashboard
- minimal or full-window world mode
- stable auth/session behavior

Outcome:

- working authenticated wrapper around Pavilion with the least new architecture

### Phase 2: Define relationship with website-v2

Choose one:

1. `website-v2` remains public marketing only and links into dashboard/world
2. `website-v2` gets a lightweight launcher page but still delegates auth/app state to dashboard
3. `website-v2` becomes the full shell later, after auth/product shell work is deliberately implemented

### Phase 3: Consolidate product architecture

If long-term product direction is a single branded experience:

- unify routing strategy
- unify auth/session bootstrap
- define whether dashboard remains separate or becomes a section of the main site

## Minimal Technical Architecture Recommendation

Short version:

- keep dashboard as authenticated application shell
- add a dedicated world route/page there
- let `website-v2` link users into that flow
- do not rebuild auth in `website-v2` until there is a clear product reason

## Concrete Work Breakdown

### Dashboard path

Implementation items:

1. Add a new dashboard navigation item or launch entry point
2. Create a Pavilion container component/page
3. Decide full-window vs embedded mode
4. Define launch params and return behavior
5. Add session-expired and unsupported-device states

### Website-v2 path

Implementation items:

1. Add Supabase auth to website runtime
2. Add protected route structure
3. Add authenticated layout separate from marketing home page
4. Add Pavilion world page/container
5. Reconcile auth ownership with dashboard

## Final Recommendation

If the goal is speed, stability, and minimal architecture churn:

- build Pavilion into the dashboard first

If the goal is a polished branded journey later:

- let `website-v2` become the public entry and launcher
- only promote it to full shell after the dashboard-based wrapper is stable
