# Morgan Stanley — Unity Immersive Art Gallery

**Status:** Initial discovery / prototype brief; not an approved production specification  
**Updated:** 2026-09-21  
**Audience:** Unity implementation subagent, Josh, and project collaborators  
**Project direction:** Explore a high-quality, accurately scaled, content-manageable immersive gallery built on MetaDyn's Unity platform.

## 1. Mission and immediate assignment

Establish a practical starting point for Morgan Stanley's immersive art gallery experience. Translate the recorded discussion into a small, reviewable Unity prototype and an implementation plan without treating unresolved business or technical choices as approved requirements.

Start by inspecting the assigned Unity repository and reporting the existing scene, SDK, content, navigation, build, and authentication paths. This brief does not identify or authorize changes to a specific Unity repository or production environment: obtain that target from Josh before implementation.

The initial focus is the artwork and visitor experience, not avatar customization or a new backend. Reuse the existing MetaDyn platform and project conventions. Do not create new agents, services, dashboards, or infrastructure to satisfy this brief without approval.

## 2. Source and evidence boundaries

Primary source: Twenty CRM opportunity **Morgan Stanley** (`9ed35780-8759-4286-bde8-e6a951a1dc9e`).

Saved note: **Morgan Stanley — Art gallery discussion and next steps**, created 2026-09-12; note ID `1b60f676-919d-4a4f-9bdf-fdb48560270e`. This contains a Morgan Stanley discussion summary shared by Josh. It records interests and discussion points, not a signed scope or verified implementation.

On 2026-09-21, Josh requested this initial Unity subagent brief so work can get started despite limited information. All proposed implementation details below are working recommendations, not additional client commitments.

No finalized budget, delivery date, gallery layout, integration contract, collection size, or concurrency target is recorded in the source note.

## 3. Recorded discussion points

- **Internal and external uses:** Internal art collection management and external public consumption are both under consideration. They may require different access and deployment models.
- **Bespoke experiences:** MetaDyn was discussed as offering more dynamic, customizable experiences than the previous Spatial setup, especially for large collections and virtual tours.
- **Curation and scale:** Reassess the assets selected for the gallery and ensure accurate representation of artwork dimensions.
- **Gallery design:** Potentially introduce modern gallery layouts that make better use of MetaDyn's capabilities. No layout has been selected.
- **Content flexibility:** Support easier digital-asset management and explore automatic updates from internal storage rather than the constraints of the previous workflow.
- **Analytics:** An analytics backend is important; metrics and provider are not yet specified.
- **Platform demonstration:** Unity 6, improved visual quality, and AI integration were demonstrated. AI functionality is not a committed gallery requirement.
- **Hosting:** On-premise hosting, deployment ease, and compatibility were discussed. A deployment target has not been chosen.
- **Authentication:** Options ranging from no login to SSO were discussed. Neither a specific identity provider nor a client-approved authentication flow is established.
- **Audience scale and avatars:** Follow-up should explore large audiences without requiring avatars. This does not establish a multiplayer requirement or prove large-scale concurrency support.
- **Public backend scope:** Public experiences may require additional backend work for user management and substantial concurrent traffic.

### Recorded follow-up ownership

- **Mackenzie Constantinou:** Schedule a follow-up to explore needs, especially large-audience experiences without required avatars.
- **Michael Potts:** Distribute access to MetaDyn demo areas.

Completion of these actions has not been verified in this brief. Josh is the internal clarification point for the implementation subagent; no dedicated implementation owner or client approver is established here.

## 4. Proposed first prototype

The following is a recommended narrow slice for review, not a production commitment.

### A. One representative gallery space

- Build or adapt one small gallery using existing project conventions.
- Use approved sample artworks if available; otherwise use clearly labeled placeholders with synthetic metadata and known dimensions.
- Prioritize artwork legibility, proportion, comfortable spacing, and restrained visual design.
- Separate artwork dimensions from frame dimensions where those differ.
- Preserve image aspect ratio; avoid stretching art to fit arbitrary wall slots.
- Use explicit units and validate world scale. Proposed convention: one Unity unit equals one meter, subject to the target project's existing setup.
- Label placeholder architecture and sample content as unapproved.

### B. Visitor flow without mandatory avatar selection

- Demonstrate entering, moving around, inspecting an artwork, reading its details, and returning to browsing.
- Prefer existing project camera/navigation controls; avoid creating another movement framework.
- Make artwork interaction clear and controls discoverable, with a reset/recovery path if the visitor gets stuck.
- Prototype a path with no mandatory avatar-selection step. Whether this uses an unseen player representation, a standalone camera, or existing platform behavior must follow repository inspection.
- Do not equate avatar-free navigation with anonymous access, disabled authentication, or absence of networking.
- Avoid introducing multiplayer, voice, or AI solely for the prototype.

### C. Data-driven artwork presentation

- Reuse an existing content model if present. Otherwise propose the smallest project-local representation for review.
- Candidate fields: stable artwork ID, title, artist, optional year/medium/description, image reference, physical width/height with units, optional frame information, and gallery placement.
- Keep private collection-management fields out of public display data.
- Keep display data separate from scene-specific rendering where practical, so content can change without hand-editing each artwork component.
- Demonstrate a sample content change through the chosen local workflow. Do not describe a local fixture as a working internal-storage integration.
- Flag missing dimensions or invalid content clearly rather than silently presenting guessed physical scale as accurate.
- Document the potential integration boundary for future storage updates; do not implement client-system access without approved access and a defined contract.

### D. Visual quality and runtime practicality

- Inspect the existing Unity, render pipeline, and build configuration before selecting techniques or dependencies.
- Optimize the representative scene for the agreed initial target, with WebGL a working candidate rather than a confirmed client requirement.
- Pay attention to image resolution, texture memory, loading behavior, lighting, and draw calls.
- Record build size, loading observations, and frame/memory measurements where tooling supports them, including test device and browser.
- Do not invent performance thresholds or claim cross-device support from a single test.

### E. Analytics planning only unless already available

- Identify existing platform analytics hooks before proposing additions.
- Candidate events: gallery entry, artwork details opened, tour started/completed, and content-load errors.
- Define event meanings and distinguish measurement from interpretation; for example, elapsed time does not prove engagement.
- Avoid personal identifiers, artwork-sensitive metadata, and new tracking vendors without approval.
- If no integration exists, propose a minimal event contract rather than deploying an analytics backend.

## 5. Working approach and checkpoints

### Checkpoint 1 — Inspect and report

Before editing the Unity project, return:

1. Repository, branch, Unity version, render pipeline, and relevant scene paths.
2. Actual SDK/runtime and navigation/authentication paths in use.
3. Existing artwork/content-loading and analytics capabilities, if any.
4. Proposed smallest prototype change set and files likely to change.
5. Missing inputs, blockers, and any choices requiring Josh's approval.

Read exact handler/state/render and content-loading paths before modifying behavior. Do not patch by guessing. Do not replace working platform architecture merely because older documentation describes another stack.

### Checkpoint 2 — Build the agreed narrow slice

Once the target and approach are confirmed, implement the representative gallery using approved or placeholder content. Keep project-specific work isolated according to existing repository conventions. Do not change shared authentication, networking, deployment, or backend behavior without explicit scope approval.

### Checkpoint 3 — Demonstrate and hand back

Provide:

- Scene/build locations and reproducible run/build instructions.
- Changed files and a concise explanation of the implementation.
- Screenshots or a short walkthrough when the environment permits.
- Verification results and exact testing limitations.
- The local content-editing workflow.
- A short list of decisions needed for the next increment.

Do not report the gallery complete simply because code compiles. Verify the actual visitor and artwork flows in the relevant runtime, or state explicitly which checks could not be performed.

## 6. Proposed prototype acceptance checks

These checks are for internal review, not client acceptance of production delivery.

- A visitor can enter the test gallery without a mandatory avatar-selection step in the approved test configuration.
- Navigation, artwork inspection, and return-to-browsing behavior work without trapping the visitor.
- At least one sample artwork has known dimensions verified against the scene scale.
- Artwork images retain their aspect ratios; framing and artwork dimensions are not conflated.
- Displayed title/artist information matches the selected sample content.
- One sample content update can be demonstrated without manually rebuilding each display component.
- Missing or failed image loads produce a usable fallback or clear error state rather than a broken interaction.
- The agreed target build runs, with measured observations and known limitations documented.
- No production authentication, client storage, or infrastructure has been changed as an incidental part of prototyping.

## 7. Explicitly unresolved / out of initial scope

Do not imply these capabilities are delivered or approved:

- Production collection-management backend or authoring dashboard.
- Automatic synchronization with Morgan Stanley's internal storage.
- Enterprise SSO, client identity-provider configuration, or security certification.
- On-premise deployment or enterprise network integration.
- Public high-concurrency infrastructure, load-test targets, or scaling guarantees.
- Multiplayer, visible avatars, voice, or shared guided tours.
- AI curator, AI guide, or conversational artwork assistance.
- Full collection ingestion, rights clearance, or public publication of client artwork.
- Accessibility conformance certification, mobile/VR support, or a production service-level agreement.

Internal versus public use must be resolved before exposing real collection data. Authentication choices, analytics privacy, artwork rights, and client approvals remain release gates, even if placeholders allow prototype work to proceed.

## 8. Questions for Josh / client follow-up

### Needed to begin implementation

1. Which Unity repository, branch, and starter scene should the subagent use?
2. Is there an existing gallery to adapt, or should the prototype use a neutral placeholder layout?
3. Are approved sample artworks, physical dimensions, and display metadata available?
4. What is the initial review target: desktop browser, another runtime, or multiple targets?

### Needed before broader implementation

5. Which first release matters most: internal collection access, public viewing, or separate experiences?
6. What does "without avatars" mean to the stakeholders: no selection screen, no visible bodies, non-social browsing, or something else?
7. Should the initial visitor experience be free exploration, a guided route, or both?
8. What system holds the artwork and metadata, and how would approved updates be exposed?
9. Which fields and artworks are permitted for public display?
10. What are expected collection size, concurrent audience size, and device/browser coverage?
11. What authentication, hosting, security review, and analytics requirements apply?
12. Who approves visual design and content, and what milestone/date should guide delivery?

## 9. Platform references and source precedence

Use these for context, then verify them against the assigned implementation repository:

- [Unity platform documentation](../../platforms/unity6/README.md)
- [System architecture](../../platforms/unity6/system-architecture.md)
- [UGS/NGO production punch list](../../planning/MetaDyn_UGS_SDK_Production_PunchList.md)
- [Authentication and identity](../../platforms/unity6/auth-identity.md)
- [Security priority fixes](../../platforms/unity6/security-priority-fixes.md)
- [Deployment and hosting](../../platforms/unity6/deployment-hosting.md)
- [Open SDK and hosting model](../../platforms/unity6/open-sdk-and-hosting-model-2026-05-25.md)

Some historical platform summaries reference Photon; newer platform guidance identifies UGS/NGO as the active Starter baseline. Neither is authorization to migrate this project. Report the actual installed/runtime stack before planning changes.

**Decision discipline:** Josh's explicit project instructions and approved client requirements set scope. The target repository establishes what is implemented. CRM establishes the recorded discussion. Recommendations in this brief remain proposals until agreed.
