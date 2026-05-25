# Open SDK and Hosting Model — 2026-05-25

This note captures an important product and business decision for the MetaDyn Unity platform after completion of the active UGS migration sprint.

## Core Decision

MetaDyn intends to release the advanced Unity SDK itself as an **open-source SDK** while layering additional value on top through the broader MetaDyn ecosystem.

The key product stance is:
- the SDK remains open and useful on its own
- creators can self-host and run their own build independently
- creators can also host with MetaDyn or connect their space/runtime to the wider MetaDyn ecosystem
- connection to the greater MetaDyn ecosystem can carry membership-gated or service-gated value
- the open SDK should never trap creators in a way that makes their space die if MetaDyn disappears or stops serving that integration path

This is strategically important because it aligns the platform with MetaDyn’s stated values around ownership, continuity, and anti-enshittification.

## The Protection / Exit Principle

A non-negotiable platform trust principle emerged from this discussion:

**If something happens to MetaDyn, creators should still be able to keep their space alive indefinitely.**

The current practical mechanism described by Josh is:
- in Unity, a creator can simply turn off MetaDyn authentication
- this disconnects the build from the MetaDyn dashboard/login flow
- the creator can then continue running that build forever on their own infrastructure

This is a very strong strategic message because it means MetaDyn is not building a hostage platform.

### Why This Matters

Most platforms create leverage by making exit painful.
MetaDyn can create leverage by making adoption safe.

That reinforces the broader MetaDyn narrative of:
- true ownership
- platform continuity
- portable runtime value
- an ecosystem that creators join because it helps them, not because they are trapped

## Product Layers In This Model

### 1. Open SDK Layer

This remains available even if a creator does not want global MetaDyn connectivity.

Expected characteristics:
- advanced Unity runtime systems remain available
- creators can ship their own build
- creators can self-host on infrastructure they control
- creators can disable MetaDyn auth dependencies when they want a standalone mode
- creators retain long-term operational continuity over the delivered experience

### 2. MetaDyn-Connected Ecosystem Layer

This is the value-added path for creators who want to participate in the broader MetaDyn fabric.

Possible connected value includes:
- dashboard-connected authentication and profile continuity
- ecosystem-wide identity/presence continuity
- managed hosting or easier deployment workflows
- membership-gated features or services
- broader platform/network effects
- future control-plane benefits, discovery, analytics, federation, or service integrations

This means MetaDyn can ethically stack value on top of the open layer instead of closing the core product.

### 3. Hosting Choice Layer

Creators should have a clear, legible set of choices:
- **self-host** — run independently, optionally with MetaDyn connectivity turned off
- **host with MetaDyn** — use MetaDyn-managed/shared hosting and connected platform services
- **hybrid path** — keep the SDK/project open and portable while selectively using MetaDyn-connected services where valuable

## Business / Product Framing

This creates a strong positioning pattern:

- **The SDK is open.**
- **The ecosystem is valuable.**
- **Participation is chosen, not coerced.**

That is a much stronger long-term trust posture than trying to maximize short-term lock-in.

It also maps cleanly onto MetaDyn’s broader goal of building a connective digital fabric rather than an extractive gatekeeper platform.

## Technical Implication For Auth

The web-first MetaDyn auth model remains an important value-add and a core part of the connected ecosystem path.

But this decision clarifies that auth must also be understood as:
- a configurable layer
- valuable when enabled
- removable when a creator wants a fully standalone deployment

This means docs and product language should clearly distinguish between:
- **SDK capability**
- **MetaDyn-connected capability**
- **MetaDyn-required capability**

The more precise MetaDyn is here, the more trust it will build.

## Documentation And Packaging Implications

The open-source release docs should clearly explain:

### Standalone / Independent Mode
- how to build and self-host
- how to disable MetaDyn-connected auth if desired
- what platform capabilities remain available without MetaDyn connectivity
- what features become unavailable when not connected to the MetaDyn ecosystem

### MetaDyn-Connected Mode
- what extra value the creator gets by connecting to MetaDyn
- what membership or service requirements apply
- what continuity/auth/profile/network effects are enabled by connecting
- what remains portable if they later disconnect

### Trust Guarantee
- creators are not locked out of their own delivered spaces
- the SDK is designed so that disconnection from MetaDyn does not destroy their build viability

## Suggested Product Language Direction

A useful plain-language version of the model is:

> The MetaDyn SDK is open and self-hostable. You can run it independently forever. If you choose to connect to the broader MetaDyn ecosystem, you gain access to additional connected features, services, and continuity benefits — but the core platform remains yours.

That message is powerful because it combines:
- openness
- safety
- optionality
- ecosystem upside

## Website / Information Architecture Direction

Josh also reported a planned website/content structure direction:
- remove Photon as the active platform story from the website
- make the platform navigation more explicit
- use a structure such as `platform.metadyn.xyz`
- provide onboarding/docs-style routes such as `platform.metadyn.xyz/getting-started`

This is a good move because it:
- separates the broader MetaDyn brand/site from the platform product surface
- gives the SDK/platform story its own durable home
- creates a clearer entry point for creators and technical evaluators
- supports future expansion into docs, hosting options, release notes, onboarding, and ecosystem/membership explanations

## Recommended Top-Level Site Structure

A likely strong direction for the platform site is:
- `platform.metadyn.xyz/` — platform overview / why MetaDyn platform
- `platform.metadyn.xyz/getting-started` — first-run onboarding and install path
- `platform.metadyn.xyz/sdk` — SDK overview and capability map
- `platform.metadyn.xyz/hosting` — self-host vs host-with-MetaDyn comparison
- `platform.metadyn.xyz/open-source` — licensing/open-core/open-SDK explanation
- `platform.metadyn.xyz/membership` — ecosystem-connected value and eligibility
- `platform.metadyn.xyz/docs` — technical docs and implementation references

The exact route list can evolve, but the strategic point is that the platform deserves its own product-information surface.

## Positioning Value

This model lets MetaDyn say something unusually strong and credible:

- creators own their path
- creators can leave without losing everything
- MetaDyn still creates premium value through connection, convenience, continuity, and ecosystem benefits

That is aligned with the company’s stated direction toward reverse enshittification and long-term trust.

## Related Documentation Areas To Keep In Sync

This decision should remain synchronized with:
- `docs/platforms/unity6/auth-identity.md`
- `docs/platforms/unity6/deployment-hosting.md`
- `docs/platforms/unity6/sdk-productization.md`
- `docs/company/positioning.md`
- future platform-site copy and onboarding docs
