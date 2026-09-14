# MetaDyn — Enterprise Differentiation and Security Commitments

**Status:** Discussion draft for enterprise evaluation; not a security certification or contractual guarantee.  
**Date:** 2026-09-14  
**Audience:** Enterprise business, technology, and security stakeholders, including prospective financial-services evaluators such as Morgan Stanley. No relationship, endorsement, or approval is implied.

## What Makes MetaDyn Different

MetaDyn is focusing on immersive enterprise spaces where people and AI can interact around shared spatial context: facilities, equipment, products, and procedures.

Our intended distinction is not simply a virtual meeting room or a chatbot placed inside a 3D scene. It is the combination of:

- **Spatial interaction:** Unity-based environments that let people explore and discuss places, objects, and processes together.
- **Contextual AI interaction:** voice and embodied AI foundations that can support explanations and guidance within an environment, with knowledge and actions scoped to the use case.
- **Deployment choice:** a self-hostable experience layer and an open SDK direction, rather than making every experience inseparable from a single hosted destination.
- **Continuity and customization:** a strategy that lets organizations retain useful experiences and adapt them to their needs without depending exclusively on MetaDyn-connected services.

These are platform foundations and product principles, not proof that every enterprise integration or fully private deployment is available today. Their value must be demonstrated against a specific customer workflow.

## Our Security Position

**Immersive technology does not remove enterprise security obligations. It introduces another interface that must respect them.**

MetaDyn can potentially help people understand complex environments, rehearse procedures, and coordinate responses. Those benefits are separate from the controls needed to secure the application, its AI, and its connected data.

Our proposed approach is to make security boundaries explicit, keep initial deployments narrowly scoped, and give enterprise evaluators evidence they can inspect rather than broad assurances.

## Concrete Commitments Enterprises Can Hold Us To

The following are proposed evaluation and pilot commitments. They must be accepted by MetaDyn and reflected in the agreed scope before becoming contractual obligations. They are not a claim that all listed evidence already exists.

| Proposed commitment | What the customer should be able to inspect |
| --- | --- |
| **We will distinguish what is available from what is planned.** | A capability list showing demonstrated features, external dependencies, limitations, and work required for the proposed deployment. |
| **We will explain where customer data goes.** | A scoped component/data-flow inventory covering hosting, identity, multiplayer, voice, AI providers, storage, and relevant logs, including data leaving the customer's boundary. |
| **We will not call a deployment fully private merely because its 3D build is self-hosted.** | A clear statement of customer-hosted and external components, required network connections, and disconnected behavior. |
| **We will agree what data is permitted before a pilot begins.** | A written data scope, starting with synthetic or non-sensitive material unless more sensitive use has been explicitly reviewed and approved. |
| **We will define and test access boundaries before sensitive use.** | Documented roles and permission checks, including tests that unauthorized users cannot access protected content or invoke privileged actions. |
| **We will keep AI authority explicit and limited.** | An inventory of permitted knowledge sources and tools. Read-only guidance is the proposed starting point; any consequential action requires separately agreed authorization and approval controls. |
| **We will clearly distinguish representation, simulation, and live state.** | Labels and source/freshness information appropriate to the use case, so users do not mistake a training scenario or stale model for verified current conditions. |
| **We will document operational responsibility and known gaps.** | Named owners for support, patching, incident reporting, retention/deletion, and recovery, plus limitations and unresolved risks shared with the evaluator. |
| **We will make security claims only as far as evidence supports them.** | Relevant test results and deployment documentation; certifications or independent assessments referenced only if actually obtained and applicable. |

## Self-Hosting: What We Will Be Precise About

Self-hosting can give customers control over delivery of an immersive experience, but the full trust boundary depends on the selected architecture.

Identity, multiplayer, voice, AI inference, telemetry, and storage may still involve external services. The documented platform includes UGS/Vivox and AI-provider dependencies that must be assessed for the specific deployment.

A deployment review should answer:

1. What runs on customer infrastructure?
2. What connects externally, and what information is transmitted?
3. Who can access the information, and how long is it retained?
4. Which dependencies can be configured, replaced, or disconnected today?
5. What stops working during an outage or disconnection?

Disabling MetaDyn-connected authentication may support independent operation, but it is not an enterprise access-control solution. Any private enterprise deployment still needs an appropriate identity and authorization design.

## How Immersive Experiences Could Help Address Security Concerns

Initial opportunities to validate include:

- **Security training and rehearsal:** practice escalation, access procedures, and incident coordination in a representation of the relevant environment.
- **Shared situational understanding:** help teams discuss assets, locations, dependencies, and incident scenarios using a common spatial reference.
- **Contextual procedural guidance:** let users consult approved instructions through an AI interface associated with the equipment or process being discussed.

These are use-case hypotheses. We should measure whether they improve understanding, procedural accuracy, or response coordination compared with existing methods. We should not claim that immersion alone prevents breaches or that an AI explanation is an authoritative operational instruction.

Connecting sensitive enterprise systems or enabling physical/operational control is outside a basic demonstration and requires a separate security review and scope approval.

## A Credible First Enterprise Evaluation

For an organization such as Morgan Stanley, the initial offer should be a bounded evaluation—not a request to trust an unreviewed platform with sensitive production data.

Proposed starting conditions:

- One clearly defined workflow and accountable business sponsor.
- Synthetic or non-sensitive content.
- No connection to production systems and no operational commands.
- An agreed participant/access model and documented service dependencies.
- AI limited to approved demonstration content, with its limitations made clear.
- Success criteria covering business usefulness, access boundaries, and data handling.
- A review checkpoint before expanding data sensitivity, integrations, or user scope.

This lets the enterprise assess both the experience and our engineering discipline without assuming readiness for regulated production workloads.

## What We Are Not Claiming

This document does not establish:

- SOC 2, ISO 27001, financial-services regulatory compliance, or customer security approval.
- Fully air-gapped operation, complete data sovereignty, or private deployment of every dependency.
- Completed enterprise SSO, tenant isolation, comprehensive audit logging, or independently validated security testing.
- A production-connected digital twin, validated simulation, or safe autonomous control of real-world systems.
- A guarantee against breaches, AI errors, or third-party outages.

Each applicable requirement must be verified for the proposed deployment. Known security findings and remediation status must be reviewed against the current build rather than inferred from historical documentation.

## Suggested Introductory Language

> MetaDyn is developing immersive enterprise environments that bring people, AI, and spatial context together. Our approach emphasizes deployment choice, continuity, and clear security boundaries. We propose starting with a narrowly scoped evaluation using non-sensitive content, with explicit documentation of data flows, external services, access requirements, and AI permissions. We distinguish demonstrated capabilities from planned work and would work with your technology and security teams to establish the requirements for any broader deployment.

## Next Decisions Before External Use

- Select the specific buyer problem and demonstration scenario.
- Confirm which proposed commitments MetaDyn is prepared to adopt and who owns each one.
- Verify the deployment architecture and current control implementation.
- Prepare the scoped capability list and data-flow inventory.
- Agree the pilot's entry criteria, acceptance tests, and stop/expansion conditions.
- Review external wording so it matches the actual offering and evidence.

## Related Planning

- [MetaDyn Digital Twin — Enterprise Planning](metadyn-digital-twin.md)
- [Open SDK and hosting model](../platforms/unity6/open-sdk-and-hosting-model-2026-05-25.md)
- [Auth and identity](../platforms/unity6/auth-identity.md)
- [Security priority fixes — historical review input; verify current status](../platforms/unity6/security-priority-fixes.md)

**Discussion basis:** Josh's 2026-09-14 direction toward enterprise immersive spaces and AI, the Digital Twin planning discussion, and the request for a basic, accountable security positioning document for prospective enterprise conversations.
