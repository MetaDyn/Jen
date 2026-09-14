# MetaDyn Digital Twin — Enterprise Planning

**Created:** 2026-09-14  
**Status:** Initial strategic planning draft; not a production-readiness or security certification statement.

## Direction

Josh has clarified that MetaDyn will focus much more on **immersive spaces and AI interaction within the enterprise**, with self-hosting a key reason the platform fits this direction.

MetaDyn Digital Twin applies that focus to environments where people need to understand, interact with, and collaborate around representations of real-world places, equipment, systems, and processes.

Working positioning:

> MetaDyn brings people, AI, and spatial context together in immersive enterprise environments, with deployment options designed to give organizations control over their experiences and operational continuity.

This is a focused enterprise entry point into the broader MetaDyn vision, not a declaration that community, openness, or cross-platform continuity are being abandoned.

## Product Boundary: An Immersive Space Is Not Automatically a Digital Twin

An immersive representation can be valuable for training, explanation, and collaboration without being a live digital twin.

For this planning effort, distinguish:

- **Immersive representation:** a navigable model of a place, asset, or process.
- **Connected digital twin:** a representation linked to identified real-world assets and relevant operational data, with explicit update frequency, provenance, and state semantics.
- **Simulation:** modeled behavior or hypothetical scenarios, clearly distinguished from observed real-world state.
- **Operational control:** commands that affect real systems; a separate, higher-risk capability that must not be implied by visualization or AI interaction.

Live telemetry, enterprise connectors, validated simulation, and real-world control are not established as shipped capabilities by this document. Their requirements and implementation status must be assessed separately.

## Existing Platform Foundations

The platform documentation provides a basis for this direction through:

- Unity 6 immersive runtime and browser-delivered WebGL experiences.
- Multiplayer presence and shared spatial experiences.
- AI voice interaction, avatar embodiment, and documented environmental/perception context foundations.
- Web-first identity and persisted profile continuity.
- Reusable SDK systems and deployment workflows.
- The open SDK and independent/self-hosted operating model described in the hosting strategy.

These foundations support investigation of enterprise digital-twin experiences. They do not, by themselves, establish enterprise security readiness, arbitrary-scale operation, or complete private deployment.

Older platform documents retain historical Photon/WebRTC descriptions. The later UGS/NGO and Vivox direction takes precedence for the migrated baseline. Verify the actual deployment and branch before making technical promises.

## Relationship to Spatial.io and Other Alternatives

Spatial.io remains a useful experience reference and part of MetaDyn's historical motivation for building an alternative with more control, flexibility, and continuity.

However, the enterprise proposition should not depend on being a feature-for-feature replacement:

> Lead with the enterprise workflow and outcome; explain immersive interaction, AI, and deployment control as the means of delivering it.

MetaDyn's experience with third-party platform constraints informs the emphasis on ownership and continuity. Current competitor capabilities must be independently verified before publishing comparative claims. This document does not claim that Spatial.io or other competitors lack specific features.

## Initial Use-Case Hypotheses

These are proposed opportunities to validate, not an approved delivery roadmap.

### 1. AI-Assisted Training and Onboarding

Employees explore an equipment or facility representation, ask an in-context AI guide questions, and practice a defined procedure. Human instructors can participate in the shared environment.

Potential measures: time to proficiency, task accuracy, instructor time, and knowledge retention.

### 2. Collaborative Asset and Facility Understanding

Distributed teams inspect a shared representation, discuss a component or location, and consult approved documentation through contextual AI assistance.

Potential measures: time to locate relevant information, issue comprehension, and reduced coordination effort.

### 3. Security and Incident Preparedness

Explore immersive rehearsal of enterprise security scenarios, procedures, and coordinated responses. The scope could include physical, cyber, and operational concerns, but the specific threat model and buyer problem remain to be defined with Josh.

Potential measures: response accuracy, procedural adherence, coordination quality, and time to identify or escalate a problem.

Immersion is a potential interface for understanding and rehearsing security work; it is not itself a security control or proof of risk reduction.

## Deployment Control and Continuity

Self-hosting is a central differentiator, but its scope must be explicit.

Hosting a WebGL build on customer infrastructure does not automatically place identity, multiplayer, voice, AI inference, logs, or connected data within that same boundary.

For each proposed deployment, document:

- Which components run within customer-controlled infrastructure.
- Which services remain external, including relevant UGS/Vivox and AI-provider dependencies.
- What data crosses each boundary and under which retention and access policies.
- What remains functional when disconnected from MetaDyn or third-party services.
- Who owns updates, monitoring, backups, recovery, and support.

The open SDK strategy describes an independent operating path, including disabling MetaDyn-connected authentication. That is a continuity mechanism, not a substitute for enterprise authentication or authorization. An enterprise standalone deployment still needs an appropriate access-control design.

Do not equate self-hosted assets with air-gapped operation, full data sovereignty, or compliance certification.

## Enterprise Security — Next Discussion

Josh intends to expand this planning work with details on how MetaDyn can help address major enterprise and digital-twin security concerns through immersive technology.

Keep two related but distinct questions visible:

1. **How can MetaDyn help customers understand, rehearse, and respond to security problems?**
2. **How is the MetaDyn deployment itself secured, including its AI and digital-twin integrations?**

Topics to develop with Josh:

- Target enterprise users, buyers, threat models, and highest-priority security problems.
- Sensitive facility models, asset information, operational data, and data classification.
- Identity, organization/role boundaries, least privilege, and authoritative permission checks.
- AI access to approved knowledge, prompt-injection defenses, tool permissions, and sensitive-data handling.
- Digital-twin data integrity, provenance, freshness, and clear separation of simulated and observed state.
- Separation of visualization from operational commands, with approval and audit requirements if control is ever introduced.
- Deployment trust boundaries, external dependencies, private inference options, and disconnected behavior.
- Auditability, incident response, secure updates, recovery, and customer operational responsibility.
- Evidence required to demonstrate effectiveness and support any security or compliance claims.

Existing security review documents identify authorization-hardening concerns. They are inputs to verification, not proof that those findings remain unresolved in the current build. Current remediation status must be checked before asserting readiness or active vulnerabilities.

No security architecture, new service, control integration, or production change is authorized by this planning document.

## Commercial Approach

Recommended initial approach: validate one bounded, repeatable enterprise workflow before presenting an all-purpose digital-twin platform.

A candidate pilot should identify:

- A specific customer problem and accountable business owner.
- The environment or assets represented.
- Why spatial interaction improves the task compared with a conventional interface.
- The AI assistant's permitted knowledge and actions.
- Data sources, hosting requirements, and security boundaries.
- A measurable outcome and acceptance criteria.
- Which parts can be reused across customers rather than becoming bespoke development.

AI-assisted training is an initial recommendation from the discussion, not a final market selection. Josh's forthcoming security-focused detail may establish a different first use case.

## Open Decisions

1. Which enterprise/security problem should anchor the first Digital Twin offering?
2. Is the first experience an immersive representation, a connected twin, or a simulation?
3. Which existing capabilities are demonstrable today, and which require implementation or hardening?
4. What deployment boundary must the initial customer require?
5. What should AI explain, recommend, or do—and what must remain prohibited?
6. What evidence would justify a paid pilot and subsequent rollout?

## References

- Strategy discussion with Josh, 2026-09-14: enterprise immersive spaces and AI interaction; self-hosting emphasis; Spatial.io alternative framing; request for Digital Twin planning and a subsequent security-focused discussion.
- [Open SDK and hosting model](../platforms/unity6/open-sdk-and-hosting-model-2026-05-25.md)
- [Platform deep dive](../platforms/unity6/platform-deep-dive.md) — includes historical architecture; use later baseline decisions where they differ.
- [Realtime voice and AI interaction](../platforms/unity6/realtime-voice.md) — includes both current-direction notes and historical implementation detail.
- [Auth and identity](../platforms/unity6/auth-identity.md)
- [Security priority fixes](../platforms/unity6/security-priority-fixes.md) — review findings; verify current remediation status.
- [UGS SDK production punch-list](MetaDyn_UGS_SDK_Production_PunchList.md)
- [Deployment and hosting](../platforms/unity6/deployment-hosting.md)
