# MetaDyn Daily Agenda

**Date:** 2026-04-21
**Timezone:** America/Chicago

- **Top priorities today:**
  - Lock today’s founder-visible push around platform continuity: dashboard login -> shared identity -> in-space profile continuity.
  - Turn beta demand into active follow-through: thank the strongest signups, segment who should get personal founder outreach first, and set expectations for onboarding.
  - Keep Discord visibly alive with a gratitude-and-momentum update tied to real platform direction, not generic hype.
  - Align Josh, Marzio, and MetaMike on this week’s concrete outcomes across build progress, outreach, and positioning.

- **Recent carry-forward context:**
  - The core MetaDyn story is now firmly about portable identity, portable assets, and cross-platform continuity, and Josh wants those live updates carried forward into daily agendas.
  - The current implemented auth bridge is web-first: users log in on `dashboard.metadyn.xyz`, Unity spaces read the shared `.metadyn.xyz` token, and persisted profile fields like avatar selection carry through.
  - Hyperfy unified login is already working, so the next meaningful continuity step is carrying profile data cleanly across surfaces rather than treating each experience as isolated.
  - Recent infrastructure mapping clarified the active surface split: Netlify for site/dashboard, AWS for stage and several immersive origins, Hetzner for prod/service apps, and the on-prem edge for Hyperfy/Pavilion/dev experiments.

- **Platform / product build:**
  - Pick one visible continuity milestone to move today: validate the dashboard-to-space identity flow, tighten profile persistence behavior, or document the next cross-surface profile handoff clearly enough to implement.
  - Review the highest-priority auth trust gap before it compounds: do not let client-supplied identity values stand in for verified identity inside Unity runtime paths.
  - Capture one founder-visible artifact by end of day — a decision, implementation note, screenshot, or validation result — so platform progress is legible this week.

- **Deployment / infrastructure / orchestration:**
  - Verify which current thread belongs on which surface before work fans out: Netlify for dashboard/site changes, AWS for stage/app origins, Hetzner for service surfaces, and on-prem edge for Pavilion/Hyperfy experimentation.
  - If any live build or UI path is touched, verify the actual served surface after the change instead of trusting source-only edits.
  - Keep orchestration/docs aligned with the real current topology so founder planning, ops, and technical decisions stay grounded in the actual environment map.

- **Community / Discord:**
  - Today’s Discord focus: **gratitude + momentum**.
  - Primary post: thank survey respondents and beta signups, then share 2-3 concrete things the community is steering — especially around continuity, ownership, and what people want to see first in beta.
  - Engagement prompt: run a quick poll on what MetaDyn should show first in the beta.
  - Quiet ops task: tag or DM the strongest beta signups with a short thank-you and a note that onboarding details are coming this week.

- **Beta / user outreach:**
  - Sort beta signups into three buckets: highest-value design partners, strong early testers, and broader community-interest users.
  - Prepare or send a short follow-up that thanks them, reflects what they asked for, and sets a realistic next-step timeline.
  - Decide which outreach should come directly from Josh for leverage and which can be handled as broader MetaDyn follow-through.

- **Business / strategy / coordination:**
  - Keep this week’s founder coordination anchored in one clear narrative: MetaDyn is not just building spaces, but the connective fabric across immersive surfaces with stronger ownership and continuity.
  - Align Josh, Marzio, and MetaMike on the few outcomes that should be true by Friday: one visible build proof point, one real community momentum beat, and one concrete beta/onboarding move.
  - Use today’s outreach and community signal to sharpen both positioning language and near-term product priority, not as separate tracks.

- **If there’s extra time:**
  - Pull 3 strong survey or beta-request themes into one reusable internal note for product and messaging.
  - Draft tomorrow’s builder-style update now so midweek community momentum is easier to sustain.
  - Tighten the beta tracker so contact status, use case, and priority are easy to scan.
