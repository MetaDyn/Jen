# Avatar Provider Replacement Options 2026

## Purpose

Document the practical replacement paths for MetaDyn Pavilion after the Ready Player Me shutdown, with specific attention to:

- current Pavilion architecture
- WebGL-first deployment needs
- implementation cost
- vendor risk
- licensing and pricing pressure

## Current Situation

As of `April 5, 2026`:

- Ready Player Me public services were discontinued on `January 31, 2026`
- MetaDyn Pavilion still contains existing RPM-integrated prefabs and scripts, but the external service is no longer a reliable forward path
- current Pavilion avatar support is split across:
 - legacy Ready Player Me paths
 - current Avatar SDK paths

This creates an immediate platform decision: keep the currently working non-RPM path alive, or replace it with a more durable provider.

## External Vendor Snapshot

## 1. Ready Player Me

Current status:

- discontinued for public use after the Netflix acquisition

Implication for MetaDyn:

- not a viable long-term provider
- existing local prefab assets may still be usable as frozen content
- no new platform strategy should depend on RPM services

## 2. Avatar SDK

Current official signals reviewed:

- Avatar SDK is actively courting Ready Player Me migrations
- Avatar SDK has a specific migration page promising:
 - temporary migration discounts
 - migration support
 - web, Unity, and Unreal workflows
- public pricing currently shows:
 - `Pro: $800/month`
 - not `$800/year`

Implication for MetaDyn:

- technically the safest short-term path because the project already uses it
- commercially it may still be too expensive depending on actual expected usage and budget
- because they are actively pitching RPM replacements, MetaDyn should negotiate before treating list price as final

## 3. Genies

Current official signals reviewed:

- Genies Avatar SDK is free for commercial use according to the current FAQ
- Genies requires Genies developer and user account flows
- official docs currently list supported build targets as:
 - iOS
 - Android
 - Windows Standalone
- official docs do not currently list WebGL as a supported Avatar SDK target

Implication for MetaDyn:

- promising on price
- attractive on long-term avatar/editor/UGC direction
- risky for Pavilion if WebGL support is a hard requirement today
- still worth tracking if you have a partner/beta WebGL path or if native is part of the roadmap

## 4. Avaturn

Current official signals reviewed:

- official Unity integration docs say Avaturn supports:
 - WebGL
 - Android
 - iOS
 - Windows/Mac by request
- Unity integration docs say:
 - "You can use Avaturn in your Unity project for free"
- public pricing page shows:
 - free basic tier
 - pro tier for branded/customized SDK-style usage

Implication for MetaDyn:

- strongest currently visible WebGL-friendly replacement candidate
- likely a better fit for Pavilion than Genies if WebGL is non-negotiable
- worth immediate technical evaluation

## Recommendation

## Best Practical Path

MetaDyn should not choose a single answer immediately.

The practical strategy is:

1. keep Avatar SDK as the short-term continuity path because it already works in the repo
2. immediately open a pricing/migration conversation with Avatar SDK
3. run a fast technical evaluation of Avaturn for WebGL compatibility and integration fit
4. keep Genies as a secondary track only if:
 - you have non-public WebGL access
 - or you are willing to treat it as native-first for now

## Why This Is The Best Tradeoff

### Avatar SDK

Pros:

- already integrated
- lowest migration engineering risk
- vendor is actively supporting RPM refugees

Cons:

- expensive at current public Pro pricing
- continued vendor dependency

### Avaturn

Pros:

- WebGL support is explicitly documented
- free path exists
- strong candidate for replacing the RPM-style web/avatar flow

Cons:

- still requires integration work
- unknown fit against current lip sync / animation assumptions
- branded/custom UX likely pushes you toward paid tiers later

### Genies

Pros:

- free
- modern avatar editor and identity model
- potentially strong long-term ecosystem

Cons:

- official Avatar SDK docs still do not make WebGL a safe default assumption
- requires Genies account model
- bigger architecture change versus current Pavilion setup

## Decision Tree

If the priority is:

### Keep shipping quickly with minimum code churn

Choose:

- Avatar SDK short-term

Action:

- negotiate pricing immediately
- ask for RPM migration discount and usage-based structure

### Preserve WebGL-first strategy while reducing SaaS risk

Choose:

- evaluate Avaturn first

Action:

- build a Unity WebGL proof of concept
- test runtime avatar replacement into current player flow

### Build toward a richer long-term avatar ecosystem and can tolerate more uncertainty

Choose:

- Genies exploration track

Action:

- confirm your actual WebGL access/support path with Genies
- do not make Pavilion production depend on undocumented support

## Recommended Next 7 Days

1. Keep current Avatar SDK path alive so Pavilion remains operational.
2. Contact Avatar SDK and ask for:
 - RPM migration discount
 - lower-volume plan options
 - exact WebGL licensing terms for your expected usage
3. Build a technical spike for Avaturn in a branch.
4. Compare these exact integration areas:
 - WebGL build success
 - login/account flow
 - runtime avatar loading
 - player controller compatibility
 - animator compatibility
 - lip sync feasibility
 - remote player reconstruction
5. Keep Genies in the planning set, but require a confirmed WebGL answer from Genies before platform commitment.

## Recommended Platform Position

For Pavilion specifically, the strongest current stance is:

- short-term runtime continuity: Avatar SDK
- medium-term WebGL replacement candidate: Avaturn
- longer-term strategic track: Genies if WebGL support becomes real and documented for your use case

That is the least risky and most cost-aware path.

## Sources

- Ready Player Me shutdown notice:
 - https://readyplayer.me/
- Ready Player Me acquisition coverage:
 - https://techcrunch.com/2025/12/19/netflix-acquires-gaming-avatar-maker-ready-player-me/
- Avatar SDK migration page:
 - https://avatarsdk.com/blog/2026/01/15/switch-from-ready-player-me-to-avatar-sdk-fast-familiar-production-ready/
- Avatar SDK pricing:
 - https://avatarsdk.com/pricing-cloud/
- Avaturn Unity integration docs:
 - https://docs.avaturn.me/docs/integration/unity/
- Avaturn pricing:
 - https://avaturn.dev/pricing/
- Genies FAQ:
 - https://docs.genies.com/docs/sdk-avatar/tools/faq/
- Genies prerequisites:
 - https://docs.genies.com/docs/sdk-avatar/getting-started/prerequisites/
