# MetaDyn Membership + Sponsorship Worksheet

**Date:** 2026-02-17  
**Owner:** MetaDyn Team  
**Purpose:** Implement a sustainable open-source-friendly revenue model with Stripe-backed subscriptions.

---

## 1) Packaging Strategy

### Positioning
- Keep the **core platform and SDK open**.
- Charge for **managed convenience, visibility, support, and enterprise outcomes**.
- Make each paid tier answer: "What business result do I get for this price?"

### Tier Structure (Current + Recommended Framing)
- **Community Member** - `$10/month`  
  Audience: individual creators and early adopters.
- **Silver Sponsor** - `$50/month`  
  Audience: indie studios, freelancers, small communities.
- **Gold Sponsor** - `$100/month`  
  Audience: agencies, growing projects, serious builders.
- **Platinum Sponsor** - `$1,000/month`  
  Audience: enterprise, corporate innovation, branded experiences.

---

## 2) Tier Matrix (Implementable)

## Community Member - $10/mo
- Discord role: `Community Member`
- Access: member channels, monthly roadmap call, early feature previews
- Product perks: 1 hosted space profile, basic analytics snapshot
- Support: community support only
- Recognition: name listed on supporters page (opt-in)

## Silver Sponsor - $50/mo
- Discord role: `Silver Sponsor`
- Everything in Community, plus:
- Recognition: logo/name in sponsor section (site + Discord)
- Product perks: 3 hosted spaces, priority feature voting
- Activation: one community shoutout/month
- Support: best-effort async support (target 72h first response)

## Gold Sponsor - $100/mo
- Discord role: `Gold Sponsor`
- Everything in Silver, plus:
- Product perks: 10 hosted spaces, advanced analytics dashboard access
- Activation: quarterly spotlight/demo slot
- Collaboration: input into quarterly planning roundtable
- Support: priority async support (target 24-48h first response)

## Platinum Sponsor - $1,000/mo
- Discord role: `Platinum Partner`
- Everything in Gold, plus:
- Business package: private onboarding session + implementation plan
- Product perks: private branded world option, SSO/auth advisory, admin controls package
- Operations: named success contact + monthly strategy check-in
- Support: SLA-style support window (define exact terms in MSA)
- Co-marketing: joint case study or event option

---

## 3) Annual Plans (Cash Flow + Retention)

Create annual prices with ~2 months free:
- Community: `$100/year`
- Silver: `$500/year`
- Gold: `$1,000/year`
- Platinum: `$10,000/year`

Recommendation:
- Default Stripe checkout toggle to monthly, but visibly show annual savings.
- Offer annual upgrade prompts after 30 days of active usage.

---

## 4) Stripe Product Setup (Worksheet)

If products/prices already exist in Stripe, **do not recreate them**.  
Use existing IDs and map them to entitlements.

## Existing Stripe Setup Path (Recommended for Current State)
- Export/copy all existing recurring `price_id` values.
- Map each `price_id` to:
  - `tier` (`community|silver|gold|platinum`)
  - `billing_cycle` (`monthly|annual`)
  - entitlement profile key (limits + support level)
- Validate each existing price:
  - `active = true`
  - `type = recurring`
  - expected amount/currency
  - correct interval (`month` or `year`)
- Keep this mapping in one config table used by webhook handlers.

Create one product per tier, two recurring prices per product only if you are starting from scratch.

## Product/Price Definitions
- Product: `MetaDyn Community`
  - Price: `community_monthly_usd_10`
  - Price: `community_annual_usd_100`
- Product: `MetaDyn Silver Sponsor`
  - Price: `silver_monthly_usd_50`
  - Price: `silver_annual_usd_500`
- Product: `MetaDyn Gold Sponsor`
  - Price: `gold_monthly_usd_100`
  - Price: `gold_annual_usd_1000`
- Product: `MetaDyn Platinum Partner`
  - Price: `platinum_monthly_usd_1000`
  - Price: `platinum_annual_usd_10000`

## Stripe Metadata (Add to products/prices)
- `tier`: `community|silver|gold|platinum`
- `billing_cycle`: `monthly|annual`
- `discord_role`: role key for automation
- `spaces_limit`: numeric
- `support_sla`: string label
- `entitlements_version`: e.g. `v1`

## Webhook Events to Handle
- `checkout.session.completed`
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_failed`
- `invoice.paid`

## Internal Entitlement States
- `active`
- `grace_period`
- `past_due`
- `canceled`

---

## 5) Entitlements + Access Control

Map Stripe tier to app permissions in one source of truth.

## Suggested Entitlements Table
- `max_spaces`
- `priority_support`
- `analytics_level`
- `branding_options`
- `event_spotlight_eligibility`
- `roadmap_influence_weight`
- `discord_role`

## Enforcement Rules
- On subscription downgrade: preserve data, block new over-limit creation.
- On cancellation: move to grace period, then to free/default access.
- On payment failure: notify at day 0, day 3, day 7, then lock premium features.

---

## 6) Onboarding Flows by Tier

## Community/Silver/Gold (Self-Serve)
1. Stripe checkout success.
2. Redirect to welcome page with next steps.
3. Auto-assign Discord role (via bot + account linking).
4. Show entitlement dashboard and "how to get value in 10 minutes."

## Platinum (Assisted)
1. Stripe checkout or sales-assisted invoice.
2. Trigger internal task for success/onboarding owner.
3. Send kickoff scheduler link + intake form.
4. Deliver implementation plan in first 5 business days.

---

## 7) KPI Dashboard (First 90 Days)

Track weekly:
- New subscriptions by tier
- Trial-to-paid or visit-to-paid conversion
- MRR and ARR by tier
- Churn by tier (logo + revenue churn)
- Average support response time by tier
- Sponsor benefit utilization (spotlights, calls, analytics usage)
- Payback period on any paid acquisition

Targets to define now:
- Community conversion target
- Silver+ attachment rate target
- Platinum pipeline target per month

---

## 8) Launch Plan (Practical Sequence)

## Phase 1: Foundation (Week 1)
- Finalize tier matrix and entitlement schema.
- Create Stripe products/prices and webhook processing.
- Build "Billing + Plan" section in dashboard.

## Phase 2: Activation (Week 2)
- Ship Discord role automation.
- Publish sponsorship page with benefit matrix and FAQ.
- Announce to community with founding sponsor framing.

## Phase 3: Optimization (Weeks 3-6)
- A/B test checkout copy and annual plan placement.
- Tighten benefits that are underused.
- Start monthly sponsor report format.

---

## 9) Risk Checklist

- **Vague benefits:** Each tier must have measurable deliverables.
- **Support overload:** Gate SLA promises to Gold/Platinum and capacity-plan.
- **Enterprise ambiguity:** Platinum must include clear business outcomes and onboarding.
- **Open-source trust risk:** Clearly communicate what remains open vs paid managed layers.

---

## 9.5) Partnerships Pipeline

Use this section to track strategic studio/platform/brand partnerships separately from recurring sponsorship tiers.

### Partnership Evaluation Criteria
- Strategic fit with MetaDyn’s XR / spatial computing / immersive web direction
- Capability overlap vs complementarity
- Credibility signals: team, clients, shipped work, contactability
- Distribution leverage: enterprise access, creator network, brand relationships
- Technical leverage: Unity/XR/3D pipeline strength, interoperability mindset
- Partnership model clarity: referral, co-sell, delivery partner, content partner, channel partner
- Risk profile: dependency risk, reputation risk, delivery mismatch, exclusivity constraints

### Target Partnership Types
- **Studio / Delivery Partners**
  - Teams that can design/build spaces, activations, digital twins, or branded worlds on MetaDyn
- **Technology Partners**
  - AI, voice, analytics, identity, infra, or interoperability providers
- **Channel / Brand Partners**
  - Communities, agencies, associations, and brands that can drive pilots and usage

---

## 9.6) Initial Due Diligence: Polycount.io / M2 Studio

### Current Assessment
- **Status:** Active discussions underway
- **Relationship Status:** Executive-level strategic relationship in formation
- **Key Contact:** Michael Potts
- **Internal Relationship Context:** Josh Garrett is Director of Spatial Engineering at Polycount
- **Partnership Type:** Strategic corporate / studio / platform partner
- **Priority:** Highest

### Strategic Significance
- This is a major strategic development, not a standard partner prospect.
- The relationship has potential implications across:
  - platform build
  - AI roadmap/execution
  - holographic avatar development
  - enterprise delivery and business development
  - long-term company alignment
- A reciprocal ownership structure is being discussed in principle:
  - MetaDyn owning `10%` of Polycount
  - Polycount owning `10%` of MetaDyn
- Final structure and exact terms are still being worked out and should be treated as pending, not final.

### Known Relationship Context
- MetaDyn is already in discussions with Polycount.
- MetaDyn has an existing direct relationship with Polycount CEO Michael Potts.
- Josh Garrett is part of the relationship from the inside, not as an external observer, through his role as Director of Spatial Engineering at Polycount.
- Platform build, some AI work, and holographic avatar work are considered strategic partnership areas with Polycount.
- This is tied to an executive-level role context, not just exploratory vendor outreach.

### What We Verified
- Polycount presents itself as a creative design agency focused on immersive games, digital twins, XR experiences, and AI-enabled XR applications.
- Polycount lists a current team, contact info, and service lines on its website.
- Polycount publicly highlights capabilities in:
  - immersive experiences
  - digital twins
  - AI + XR custom apps
  - Roblox / interactive gaming
  - visualization / 3D content production
- Polycount appears to have named leadership and delivery roles, including:
  - Michael Potts
  - Dayana Guerrero
  - Josh Garrett
  - Alex Antuna
  - Zach Taylor
- Public contact details are available:
  - `info@polycount.io`
  - `214-752-7279`
  - `2211 North Lamar Street #302, Dallas, TX 75202`

### Relationship to "M2 Studio"
- Public reporting indicates M2 Studio later became known as Polycount.
- ARPost reported in November 2022 that Spatial had known “a design studio called M2 Studio (now known as Polycount)” and that Polycount had prior enterprise/metaverse work with Spatial-related clients.
- This suggests Polycount/M2 Studio is not just a cold lead; there is relevant category history.

### Why This Is A Strong Fit For MetaDyn
- They are directly in the immersive environment / spatial activation business.
- Their positioning overlaps with the kind of:
  - branded spaces
  - digital twins
  - XR applications
  - custom enterprise experiences
  that MetaDyn wants to enable.
- They are already relevant beyond generic outreach because there is active strategic overlap in:
  - executive relationships
  - platform build
  - AI-related work
  - holographic avatar-related work
- They can potentially serve as:
  - strategic corporate partner
  - strategic build partner
  - enterprise delivery partner
  - showcase/case-study partner
  - referral/channel partner

### Updated Evaluation
- This should no longer be tracked as ordinary partnership pipeline only.
- It should be treated as a strategic relationship workstream with both:
  - operational partnership value
  - potential ownership/corporate structure significance
- If the reciprocal ownership discussion progresses, Polycount becomes one of the most important external relationships in MetaDyn’s current operating landscape.

### Company Evaluation: MetaDyn
- **Core Strength**
  - Platform/IP leverage: MetaDyn appears strongest where it owns platform runtime, SDK, deployment flow, AI embodiment, authentication, and reusable infrastructure.
- **Strategic Value To Polycount**
  - Gives Polycount a controllable platform layer instead of depending entirely on third-party platform constraints.
  - Creates a path to productized delivery rather than one-off bespoke builds only.
  - Enables Polycount to pitch not just design/build services, but a repeatable immersive platform stack.
- **Current Weakness / Risk**
  - Platform maturity still needs continued packaging, update flow, and productization work.
  - MetaDyn likely benefits from stronger enterprise-facing design/delivery validation than it can generate alone.

### Company Evaluation: Polycount
- **Core Strength**
  - Strong design/build credibility in immersive experiences, branded activations, digital twins, XR, and enterprise-facing experiential work.
- **Strategic Value To MetaDyn**
  - Polycount can bring high-value client relationships, design quality, enterprise credibility, and premium execution capacity.
  - Polycount has visible overlap with the exact category MetaDyn wants to serve: immersive branded spaces, enterprise XR, AI/XR applications, and avatar-forward experiences.
- **Current Weakness / Risk**
  - If Polycount remains too services-led without platform standardization, scale and repeatability are constrained.
  - If MetaDyn is not embedded as a real platform layer, the relationship could collapse into project-by-project custom work instead of durable platform advantage.

### Maximum Mutual Benefit Focus

To maximize value for both organizations, the strategic partnership should focus on areas where:
- Polycount brings client access, design/build execution, and enterprise trust
- MetaDyn brings platform IP, repeatable infrastructure, deployment/runtime control, and product leverage

Highest-value focus areas:

1. **Platformized Enterprise Delivery**
   - Polycount sells and delivers premium immersive experiences.
   - MetaDyn provides the reusable platform/runtime/SDK layer underneath.
   - Benefit:
     - Polycount improves delivery repeatability and differentiation.
     - MetaDyn gets real enterprise deployment validation and revenue-linked platform usage.

2. **Flagship Showcase Projects**
   - Build one or more public-facing spaces/demos together that prove:
     - premium environment quality
     - embodied AI
     - holographic/advanced avatar presence
     - deployable branded world infrastructure
   - Benefit:
     - Polycount gets a stronger platform-backed showcase.
     - MetaDyn gets category-defining proof, not just internal prototypes.

3. **AI + Avatar Productization**
   - Use Polycount’s experiential design strengths and MetaDyn’s AI embodiment stack to create differentiated offerings around:
     - AI concierges/guides
     - enterprise training/simulation assistants
     - holographic avatar presence
     - premium interactive brand characters
   - Benefit:
     - Polycount gets new premium service/product lines.
     - MetaDyn turns AI embodiment into a market-facing competitive wedge.

4. **Digital Twin / Enterprise XR Infrastructure**
   - Position MetaDyn as the deployable platform layer for selected Polycount digital twin and XR applications.
   - Benefit:
     - Polycount gets an owned/flexible runtime path.
     - MetaDyn gets credibility in practical enterprise use cases beyond “metaverse” branding.

5. **Joint GTM and Strategic Positioning**
   - Position the relationship as:
     - Polycount = premium immersive design/build execution
     - MetaDyn = platform, infrastructure, AI, and deployable runtime layer
   - Benefit:
     - Clear market narrative
     - Reduced overlap/confusion
     - Better enterprise sales story

### What To Avoid
- Letting the relationship become vague “we should collaborate” positioning without a defined operating model.
- Using MetaDyn only as internal tooling instead of a visible platform advantage.
- Letting Polycount become only a services channel without creating reusable MetaDyn platform proof.
- Entering reciprocal ownership discussions without parallel clarity on:
  - governance
  - execution ownership
  - commercial rights
  - product/IP boundaries

### Recommended Strategic Focus Order
1. Secure one flagship joint win
2. Define the platform-vs-services operating model
3. Productize AI/avatar and enterprise XR offerings together
4. Then formalize deeper structural alignment if the operating relationship proves durable

### Active / Likely Partnership Angles
- **Platform Build Partner**
  - Polycount contributes to or collaborates around platform-facing build opportunities
- **AI Partner**
  - Collaboration on selected AI-enabled immersive experiences/workflows
- **Holographic Avatar Partner**
  - Collaboration around avatar embodiment / holographic presence use cases
- **Enterprise Delivery Partner**
  - Polycount designs/builds client-facing environments using MetaDyn platform infrastructure
- **Showcase / Case Study Partner**
  - Joint flagship environment, demo, or launch partner story

### Strength Signals
- Clear current website with named service areas
- Named team page
- Public contact info
- Public claims of substantial 3D/XR experience
- Public materials showing focus on enterprise/brand immersive work
- Public third-party article tying them to Spatial-era immersive design work

### Risks / Open Questions
- Need to validate how active/recent their real delivery pipeline is today
- Need to verify whether they are primarily:
  - agency/design
  - full technical build partner
  - or a mix
- Need to define the exact structure of the strategic relationship:
  - services partnership
  - platform partnership
  - commercial channel partnership
  - equity/cap-table relationship
  - or a combined structure
- Need to confirm governance boundaries if reciprocal ownership proceeds
- Need to verify commercial compatibility:
  - project size
  - pricing expectations
  - exclusivity or preferred platform relationships
  - conflict-of-interest or role-boundary considerations
- Need to ensure all strategic assumptions are documented separately from any unsigned legal reality

### Recommended Next Steps
1. Convert current discussions into a defined strategic partnership track
2. Clarify scope buckets:
   - platform build
   - AI collaboration
   - holographic avatar collaboration
   - corporate/equity structure
3. Define whether Polycount is:
   - strategic corporate partner
   - strategic build partner
   - referral/channel partner
   - flagship showcase partner
   - some combination of the above
4. Identify first concrete joint win:
   - pilot
   - demo environment
   - client-facing activation
   - co-marketing/showcase story

### Source Notes
- Polycount home/about/contact/team pages
- ARPost article on Spatial / Exclusible / Polycount relationship (November 16, 2022)
- Internal relationship context provided by Josh Garrett

---

## 10) Discord Launch Copy (Ready to Post)

## Option A (Short, punchy)
`@everyone`  
MetaDyn memberships and sponsorships are now live.  
If you want to help us build an open, creator-first alternative in the metaverse, you can join at:
- Community Member - $10/mo
- Silver Sponsor - $50/mo
- Gold Sponsor - $100/mo
- Platinum Partner - $1,000/mo (enterprise/corporate)

Your support funds hosting, AI features, and open-source development.  
Reply here if you want the signup link + founder perks details.

## Option B (Story-driven)
We’re building MetaDyn to be open where it matters and sustainable where it counts.  
Today we launched memberships + sponsorship tiers through Stripe:
- Community ($10)
- Silver ($50)
- Gold ($100)
- Platinum ($1,000, enterprise)

If you believe in a Spatial-style platform with open-source DNA, this is the best way to back it and shape what we ship next.  
Founding sponsors will get early recognition and direct input on roadmap priorities.

Drop a `+1` and we’ll send you the signup link.

## Option C (Enterprise-focused)
MetaDyn Sponsor Program is open.  
For teams and brands exploring immersive collaboration, events, and AI-powered virtual spaces:
- Gold Sponsor ($100/mo)
- Platinum Partner ($1,000/mo)

Includes priority support, brand visibility, and structured onboarding options.  
DM us to discuss fit, rollout timeline, and pilot scope.

---

## 11) FAQ Snippets for Community

- **Is MetaDyn still open-source?**  
Yes. Core components stay open; paid plans fund managed infrastructure, support, and advanced enterprise services.

- **Can I upgrade/downgrade any time?**  
Yes, through Stripe customer portal and your dashboard billing page.

- **Why sponsorship tiers?**  
To fund reliable hosting, ongoing development, and dedicated support while keeping the platform accessible.

---

## 12) Implementation Checklist

- [ ] Finalize public pricing page copy
- [ ] Map existing Stripe `price_id` values to tier entitlements
- [ ] Validate existing recurring price intervals/amounts/status
- [ ] Implement webhook entitlement sync
- [ ] Build billing portal link in dashboard
- [ ] Add Discord role automation
- [ ] Publish sponsor recognition section on website
- [ ] Write onboarding emails per tier
- [ ] Set up KPI dashboard and weekly review cadence
