# Nvidia GB10 Enterprise Inference Plan — 2026-07-07

## Purpose

Working plan for standing up enterprise-grade inference infrastructure around Nvidia-aligned software, Dell Pro Max GB10 hardware, and a sellable dedicated-node offer that can generate real revenue for MetaDyn.

This is an active planning document, not a final proposal.

## Current Direction

MetaDyn is considering:

- upgrading Jen / OpenClaw infrastructure toward a more professional Nvidia-centered stack
- using Nvidia-oriented components described in current discussion as NemoClaw, Hermes, and OpenShell
- purchasing **2 x Dell Pro Max GB10** systems with networking
- starting with just the first **2 units** as the initial production footprint
- moving toward running Jen more directly on dedicated production infrastructure
- using the current system here as a migration source, example deployment, and potentially a reusable enterprise baseline/system image
- eventually running **Nemotron** models custom-trained for MetaDyn
- using this infrastructure not just internally, but as the basis for a revenue-generating **enterprise inference** offer
- potentially hosting Unity WebGL workloads directly on a GB10 as part of the same enterprise-grade platform story

## Initial Commercial Thesis

The near-term business case is:

1. secure capital quickly
2. purchase and deploy the first 2 GB10 units
3. stand them up as credible production infrastructure
4. package dedicated enterprise inference offers
5. close initial customers fast
6. use early revenue to justify expansion

This matters because it shifts the conversation from speculative platform R&D into a tangible infrastructure business with near-term cashflow potential.

## Hardware Assumptions

Current discussed assumptions:

- **GB10 unit price:** about **$5,689** each
- **Initial purchase:** **2 units**
- **Prior pricing basis including cables/networking:** about **$11,676** total
- **Depreciation assumption:** 3-year useful life, 10% salvage
- **Derived monthly depreciation from earlier working model:** about **$291.90/month total**

These assumptions should be validated against current vendor quotes before committing to any external model.

## Initial Pricing Models Discussed

### 1) Dedicated Private Node

- **$499/month per node**
- **$4,990/year per node**

This is the clearest enterprise offer and the easiest to explain.

### 2) Sliced Multi-Tenant Instances

- 4 slices per box
- **$149/month per slice**
- **$1,490/year per slice**

This likely improves utilization flexibility, but adds packaging and noisy-neighbor risk.

### 3) Hybrid Base + Usage

- **$199/month base**
- **$1,990/year base**
- plus metered overage

This may become the strongest long-term model once usage data is real.

## Recommended Initial Go-To-Market

For phase 1, the recommended default offer is:

- lead with **dedicated private nodes**
- keep pricing simple and enterprise-readable
- use the sliced/hybrid models later if demand requires them

Why:

- easiest to sell
- easiest to position as premium
- easiest to support operationally
- avoids overcomplicating the first motion

## Expansion Scenario Discussed

Josh asked about a 3-year scenario based on:

- purchasing **2 units every 2 months**
- selling them as **dedicated nodes**
- using **$499/month per node** as the working revenue assumption

### Working 3-Year Projection

Assumptions:

- 2 nodes purchased every 2 months
- full occupancy once deployed
- no financing cost modeled
- excludes taxes, support labor, and extra networking unless added separately

Projected after 3 years:

- **units purchased:** 36
- **hardware cost:** **$204,804**
- **total revenue:** **$341,316**
- **gross hardware spread:** **$136,512**

Using the earlier fixed operating estimate:

- **fixed ops estimate:** $306/month
- **36 months ops:** **$11,016**
- **net after hardware + fixed ops:** **$125,496**

End-of-year-3 run rate:

- **active dedicated nodes:** 36
- **monthly revenue:** **$17,964/month**
- **annualized revenue run rate:** **$215,568/year**

## Important Caveat

This model is useful as a directional planning tool, but it is still optimistic because it assumes:

- full occupancy
- no lag between purchase and sale
- no downtime
- no customer acquisition drag
- no support burden growth
- no financing friction

Before this is used in any investor or buyer-facing material, it needs a more realistic scenario model with:

- ramp time
- occupancy assumptions
- deployment lag
- replacement reserve
- support burden
- true networking / rack / power / backup / monitoring costs

## Strategic Upside

If this works, the upside is bigger than just infra resale.

It could become:

- the production substrate for Jen
- a MetaDyn internal AI platform layer
- a proving ground for Nemotron tuning/customization
- a sellable B2B inference product
- a bridge from scarce capital to self-funded technical expansion

## Risks

Primary risks right now:

- raising capital fast enough
- buying hardware before demand is validated
- underestimating production-readiness work
- overestimating occupancy speed
- unclear enterprise packaging / SLA definition
- security/compliance gaps for enterprise customers
- support expectations outrunning current team capacity

## Immediate Punch List

### A. Commercial Model

- [ ] Confirm current live pricing/availability for Dell Pro Max GB10 units
- [ ] Confirm networking/cable/accessory BOM for the first 2-node deployment
- [ ] Build a more realistic revenue model with occupancy ramps
- [ ] Build a downside case, base case, and aggressive case
- [ ] Decide whether dedicated-node is the official phase-1 offer
- [ ] Define minimum viable contract term: monthly vs annual vs setup fee
- [ ] Define whether onboarding/setup fees should be charged
- [ ] Define what “enterprise inference” includes in plain English

### B. Offer Design

- [ ] Write the dedicated-node offer as a 1-page commercial brief
- [ ] Define who the first ideal buyers are
- [ ] Define whether the offer is private inference, hosted model serving, agent hosting, or all three
- [ ] Define expected workloads and supported model families
- [ ] Define what is and is not included in support
- [ ] Define uptime target and service expectations

### C. Technical Architecture

- [ ] Validate the actual Nvidia software stack to be used in production
- [ ] Clarify what NemoClaw, Hermes, and OpenShell map to concretely in the deployment architecture
- [ ] Decide node roles for the first 2-box deployment
- [ ] Define orchestration, inference, storage, monitoring, and backup layers
- [ ] Define network topology and secure remote access pattern
- [ ] Define tenancy boundaries for customer isolation
- [ ] Decide whether phase 1 is single-tenant only

### D. Production Readiness

- [ ] Create a deployment runbook for the first two systems
- [ ] Define monitoring, alerting, and logging requirements
- [ ] Define backup and recovery expectations
- [ ] Define patching/update policy
- [ ] Define secrets management approach
- [ ] Define incident response basics
- [ ] Define customer provisioning workflow

### E. Finance / Funding

- [ ] Define exact near-term capital requirement for first deployment
- [ ] Separate capex from recurring opex clearly
- [ ] Identify fastest credible funding sources
- [ ] Prepare a lightweight ROI summary for investor conversations
- [ ] Decide whether expansion cadence should really be every 2 months or demand-triggered

### F. Sales Motion

- [ ] Make a target list of early enterprise buyers/partners
- [ ] Write a short offer deck or one-pager
- [ ] Write outreach language for the first conversations
- [ ] Define proof points needed to close the first customer
- [ ] Decide whether early customers get discounted anchor pricing

## Suggested Next Deliverables

The next documents to create from this plan should probably be:

1. **financial model worksheet**
2. **1-page dedicated-node commercial brief**
3. **technical deployment architecture draft**
4. **first-deployment runbook**
5. **sales/outreach punch list**

## Recommended Next Decision

The next key decision should be:

**Is phase 1 officially a dedicated private node offer, or do we want to position a broader enterprise inference service from day one?**

That answer determines pricing, packaging, architecture, and sales language.
