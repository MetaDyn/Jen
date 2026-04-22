# MetaDyn Daily Agenda

**Date:** 2026-04-22
**Timezone:** America/Chicago

- **Top priorities today:**
  - Move one founder-visible proof point on cross-surface identity/profile continuity so MetaDyn’s core product story feels real, not abstract.
  - Turn survey and beta interest into concrete follow-through: decide who gets direct outreach first, what they should see, and what feedback MetaDyn wants back.
  - Keep Discord visibly tied to the actual build with a midweek builder-style update instead of generic hype.
  - Align Josh, Marzio, and MetaMike on the few outcomes that should be true before the week ends across build progress, outreach, and positioning.

- **Recent carry-forward context:**
  - Daily agendas were explicitly reworked to include real carry-forward context from recent work instead of stale recurring filler.
  - The implemented auth bridge is now clearly framed: users log in on `dashboard.metadyn.xyz`, Unity spaces read the shared `.metadyn.xyz` token, and persisted profile fields like avatar selection carry through.
  - Recent infra mapping clarified the current environment split: Netlify for site/dashboard, AWS for stage and several experience origins, Hetzner for prod/service apps, and the on-prem edge for Hyperfy/Pavilion/dev surfaces.
  - Wiki migration and infrastructure consolidation are actively underway, which means MetaDyn now has real internal operating material to refine rather than starting from scattered notes.

- **Platform / product build:**
  - Pick one concrete continuity milestone to move today: validate dashboard-to-space identity flow, tighten persisted profile handoff, or document the next profile-continuity implementation step clearly enough to ship.
  - Review the highest-priority trust gap in the current auth/runtime path so client-supplied identity does not quietly become the source of truth inside live experiences.
  - End the day with one founder-visible artifact — a screenshot, build note, validation result, or implementation decision — that can be reused in both team coordination and community updates.

- **Community / Discord:**
  - Today’s Discord focus: **builder signal**.
  - Primary post: share one real build update — screenshot, GIF, or short note — tied to identity continuity, profile persistence, or another concrete platform thread in motion.
  - Engagement prompt: ask, **“What should MetaDyn feel like in one word?”**
  - Quiet ops task: keep `#build-log` / `#beta-updates` disciplined and consistent so visible progress does not disappear into scattered chat.

- **Beta / user outreach:**
  - Segment current beta interest into highest-value design partners, strong early testers, and broader community-interest users.
  - Prepare or send a short follow-up that thanks them, reflects what they asked for, and sets a realistic expectation for onboarding timing.
  - Decide which outreach should come directly from Josh for leverage and which can move as standard MetaDyn follow-through.

- **Business / strategy / coordination:**
  - Keep this week’s founder coordination anchored in one clear narrative: MetaDyn is building continuity, control, and ownership across immersive surfaces — not just isolated spaces.
  - Use today to lock the small set of outcomes that matter by Friday: one visible build proof point, one real community momentum beat, and one concrete beta/onboarding move.
  - Fold the latest infra/wiki consolidation work into founder planning so product, deployment, and messaging stay grounded in the same operating picture.

- **If there’s extra time:**
  - Pull 3 strong survey or beta-request themes into one reusable note for product and messaging.
  - Draft tomorrow’s beta-onboarding-style community update now so momentum carries into Thursday.
  - Tighten the beta tracker so contact status, use case, and priority are easy to scan.
