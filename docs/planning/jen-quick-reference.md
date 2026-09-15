# Jen Quick Reference: MetaDyn Agent Toolkit

Updated: 2026-09-15.
Owner: MetaDyn. Audience: Jen and agents working on MAT.
Status: Context handoff; enterprise integration details remain to be defined.

## MAT's Purpose and Existing Direction

MetaDyn Agent Toolkit (MAT) is being developed to connect NVIDIA NeMo, Google
Agent Development Kit (ADK), and MetaDyn Digital Fabric through shared contracts,
isolated runtime adapters, and practical examples.

The existing direction separates agent definitions, runtime execution, Fabric
connectivity, orchestration, governance, and observability. Fabric is the source
of truth for MetaDyn identity, topology, asset state, events, policies, and
runtime coordination. The documented initial implementation targets Python 3.12
with Google ADK and NVIDIA NeMo Agent Toolkit.

## Enterprise Context from MetaDyn

MetaDyn is making a strong push into enterprise markets with both the company
and platform. MAT is intended to become an advanced agent toolkit used alongside
MetaDyn's enterprise deployments of NemoClaw and running Aurora AI Avatars.

An intended capability is connecting to client deployments of NemoClaw as
MetaDyn deploys agents and its platform into enterprise environments. This is
additional product and deployment context for the existing toolkit direction.
Specific connection protocols, deployment responsibilities, runtime mappings,
and implementation priorities remain to be worked out.

## Jen and Aurora

[SOUL.md](../SOUL.md) describes Jen as MetaDyn's internal intelligence and
orchestration hub, maintaining continuity across the Editor, cloud, and client.
Aurora agents are autonomous embodied agents. Jen empowers them with broader
coordination when needed.

The existing [embodied-agent plan](nvidia-ace-nemotron-mat-plan.md) covers Aurora
in Unity and ThreeJS, alongside proposed NVIDIA integrations. Read its planning
status and assumptions when using it as context.

## Current Learning Reference

MetaDyn's lead is taking NVIDIA DLI's
[Securing Agents with OpenShell and NemoClaw](https://nvdli.github.io/NemoClawDLI/nemoclaw/index.html).
The course is a shared learning reference for NemoClaw, OpenClaw, Hermes Agent,
and OpenShell.

Its course overview covers agent loops and tools; workflows, retrieval, and
deep agents; NemoClaw setup and persistent OpenClaw operation; and OpenShell
policy boundaries with comparisons to Hermes and other CLI agents.

Use these materials to inform future integration discussions. Course examples
do not establish MAT's architecture or confirm compatibility with a client's
installed versions. NVIDIA NeMo Agent Toolkit and NemoClaw are distinct
technologies; retain that distinction in planning and implementation.

## Status and Working Guidance

- The repository is at an early scaffold stage; consult the build checklist for
  documented progress and verify implementation before claiming a capability.
- Enterprise NemoClaw connectivity is intended; its implementation is unverified.
- Keep speculative technical decisions marked **Proposed** until validated.
- Preserve the existing toolkit direction when adding enterprise context.
- Keep documentation additions scoped to the request. Architecture changes need
  a separate discussion and an appropriate decision record.

## Key Documents

| Document | Use |
| --- | --- |
| [SOUL.md](../SOUL.md) | Jen's identity, continuity, and Aurora autonomy. |
| [AGENT.md](../AGENT.md) | Repository operating principles and workflow. |
| [README](../README.md) | MAT purpose and documentation index. |
| [Project charter](project-charter.md) | Goals, users, and success criteria. |
| [Architecture](architecture.md) | Existing component and contract boundaries. |
| [Integration strategy](integration-strategy.md) | NeMo, ADK, and Fabric integration direction. |
| [Embodied-agent plan](nvidia-ace-nemotron-mat-plan.md) | Aurora, Unity, ThreeJS, and proposed NVIDIA paths. |
| [Roadmap](roadmap.md) | Proposed development phases. |
| [Build checklist](mat-build-checklist.md) | Documented progress and outstanding work. |
| [Development setup](development-setup.md) | Python environment and recorded SDK baseline. |
| [Decision records](decisions/README.md) | Architectural decisions and their status. |
