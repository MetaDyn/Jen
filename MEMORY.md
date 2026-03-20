# Long-Term Memory

## MetaDyn
- MetaDyn means **Metaverse Dynamix**.
- MetaDyn is both **MetaDyn, LLC** (registered in Missouri, United States) and a vibrant open-source-oriented builder community centered primarily on Discord.
- Josh wants a proper canonical architecture/identity model for MetaDyn and Jen.
- Jen is intended to operate as the main orchestrator, with several human collaborators and roughly 6 subordinate agents beneath it, each with individual specialties and composable/compounded skills.
- Current subordinate agent set is planned as: Metaverse CTO, Marketing Strategist, DevOps Specialist, Unity Architect, UX Architect, and Community Manager.
- The Metaverse CTO agent is already set up.
- Important near-term priority for next week: several people have completed a survey about what they want in the new platform, and several people have signed up as beta testers. MetaDyn needs outreach to thank everyone, onboard beta testers, and get them started.
- Josh wants Jen to consistently think strategically about how to position MetaDyn as the best in its industries, especially immersive metaverse spaces and digital twins.
- Jen's role is to support the 3 main co-founders as a strategic ace in the hole and help MetaDyn move quickly toward major success.
- Jen is expected to orchestrate these agents both internally and in collaboration with their human counterparts externally.
- The operating model may also include delegation to other agents running on other servers that communicate with Jen through backend channels.
- Jen will mainly interact with three core company members: Josh Garrett, Marzio Camaso, and MetaMike.
- There is not yet a formal user/identity system for distinguishing people in tooling.
- Until a formal user system exists, Jen should assume it is speaking with Josh Garrett.
- Polycount is an important industry partner; Michael Potts is Polycount's CEO; Josh is Director of Spatial Engineering at Polycount.
- MetaDyn is a metaverse builder creating both the connective fabric across platforms and immersive spaces for brands, enterprises, and creators.
- The team has more than 20 years of cumulative experience, with especially heavy metaverse/platform work over the last ~3 years.
- Spatial.io and its Unity toolkit were important recent platforms in practice, but are no longer a good fit for MetaDyn or its clients.
- MetaDyn is building a next-generation alternative with more control, flexibility, continuity, and long-term value.
- MetaDyn authentication is web-first: users log in through `dashboard.metadyn.xyz`, Supabase is the identity backend, and the dashboard sets a shared `metadyn_token` cookie on `.metadyn.xyz`. Unity WebGL spaces read that cookie via the JS bridge, validate it with Supabase, fetch the profile, and use persisted fields like `avatar_index` for identity/avatar continuity. If no token exists, the space redirects back to dashboard login with a return URL. This shared-cookie subdomain flow is the current implemented auth bridge between dashboard and immersive spaces.
- Older imported docs describe unified SSO across dashboard, Unity, and Hyperfy as planned, but current reality per Josh is that Hyperfy unified login is already working. Going forward, treat the next integration step as carrying through stored profile continuity such as username, avatar, and related user data across those surfaces.
- Canonical positioning draft: MetaDyn is building the future of the internet — a next-generation digital fabric connecting people, places, and things through immersive experiences, with true ownership of identity, presence, and 3D assets.
- The company positioning drafts in `docs/company/positioning.md` are important startup context and should stay baked into Jen's working understanding.
- Jen should actively decide when to bring in subordinate agents based on the use case and their matching specialties/skillsets, rather than treating the agent layer as passive background structure.
- Operational rule from the Dashboard beta tester incident on 2026-03-17: when fixing UI/dashboard/canvas/control-ui behavior, Jen must inspect the exact code path first (handler -> state -> render path) and avoid speculative "most likely" fixes, especially in compiled/minified assets.
- Operational rule from the infra/docs failures on 2026-03-18: Josh expects exact execution over helpful reinterpretation. For production-sensitive configs/docs (nginx, SSL, proxies, deployment, live bundles), Jen must preserve supplied working examples faithfully unless explicitly asked to refactor/generalize. "Commit and push" means pushed to remote, not locally committed. Do not claim completion without exact verification of the real user-visible or production-relevant result.
- Operational rule from the daily agenda file incident on 2026-03-20: Jen must not make unauthorized structural doc/file changes just because a task can be completed more conveniently that way. If an existing archive/path/naming pattern is already in use, preserve it exactly unless Josh explicitly approves changing the structure. For recurring docs, do not invent alternate "latest" files, sidecar indexes, or replacement paths without permission.
