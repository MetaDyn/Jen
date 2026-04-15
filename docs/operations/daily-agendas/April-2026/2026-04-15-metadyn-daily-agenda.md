# MetaDyn Daily Agenda

**Date:** 2026-04-15
**Timezone:** America/Chicago

- **Top priorities today:**
  - Lock the most founder-visible build thread for the rest of the week and make sure product, messaging, and coordination all point at the same thing.
  - Turn the new infrastructure/domain mapping work into practical next-step clarity instead of letting it remain a scattered reference dump.
  - Keep beta interest moving by choosing who should get first-contact follow-up and what the onboarding path actually looks like.
  - Show visible builder momentum in Discord today with a real build update, not just a generic status post.

- **Recent carry-forward context:**
  - The MetaDyn infra picture is materially clearer now: stage is on AWS, prod/core service surfaces are on Hetzner, Netlify handles the root/dashboard class of sites, and the `136.34.121.206` environment is effectively a broader on-prem/dev edge with active Hyperfy and Pavilion routes.
  - Josh wants more of that operational knowledge captured in docs, not left buried only in memory or chat.
  - Cloudflare is now the right mental model for ingress across the estate, with wildcard-domain coverage and nginx reverse proxy as the default pattern for non-Netlify surfaces.
  - The control UI now has a native `Network Map` route, which makes infra visibility a live internal surface rather than just a note-taking exercise.

- **Platform / product build:**
  - Decide what today’s visible build artifact is: a cleaner network map pass, a product milestone update, a continuity/auth thread, or another concrete in-flight feature that the team can rally around.
  - Turn that into something inspectable today: a screenshot, GIF, short internal demo target, implementation checkpoint, or a yes/no architecture decision.
  - Keep quality tight on anything user-visible: if a route, panel, or dashboard view needs work, patch the exact live path and corresponding source path rather than treating one without the other as done.

- **Deployment / infrastructure / orchestration:**
  - Consolidate the current domain/host map into a founder-usable operating picture: what runs on AWS, what runs on Hetzner, what lives behind the on-prem/dev edge, and which surfaces are still legacy or transitional.
  - Verify whether any near-term work depends on that map today: deployment planning, reverse-proxy cleanup, environment naming, or clearer internal docs for who touches what.
  - If the network-map/control-UI view still looks rough, refine presentation quality so it reads like an intentional operator tool instead of a placeholder.

- **Community / Discord:**
  - Today’s rhythm is Wednesday builder signal: post one real build update tied to current momentum.
  - Primary post: share a screenshot, GIF, or short note showing visible progress on a live MetaDyn surface or system.
  - Engagement prompt: ask, “What should MetaDyn feel like in one word?” to keep replies lightweight but signal-rich.
  - Quiet ops task: keep `#build-log` / `#beta-updates` usage consistent and reply to any high-signal comments so the momentum feels founder-led, not abandoned.

- **Beta / user outreach:**
  - Choose the first beta contacts who matter most this week: strongest fit, strongest strategic upside, or easiest fast-start testers.
  - Send or prepare a concise founder-friendly follow-up that thanks them, sets expectations, and tells them what happens next.
  - Keep the beta tracker lightweight but real: name/handle, use case, contact status, onboarding status, and owner.

- **Business / strategy / coordination:**
  - Use today to align Josh, Marzio, MetaMike, and any relevant support around one shared story: MetaDyn is building continuity across immersive surfaces, not another disconnected destination.
  - Turn the clearer infra picture into strategic leverage by identifying which surfaces are stable enough to reference externally and which still need internal cleanup before being showcased.
  - Capture any decisions made today in docs while they are fresh so architecture, positioning, and operator context stop drifting apart.

- **If there’s extra time:**
  - Tighten the network map and related docs into a cleaner canonical reference the team can reuse.
  - Draft Thursday’s beta-onboarding Discord post today so tomorrow’s message is concrete, not improvised.
  - Pull 2–3 clean talking points that connect current build progress with outreach and partner conversations.
