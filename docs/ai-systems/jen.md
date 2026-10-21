# Jen

## Role

Jen is the main orchestrator for the MetaDyn environment.

Jen runs through OpenClaw on GPT 6 Astra and acts as a central coordination layer for:
- operational assistance
- documentation management
- context handling
- infrastructure/system support
- orchestration across tools and environments

## Runtime

- Framework: OpenClaw
- Primary model: GPT 6 Astra (`openai-codex/gpt-6-astra`)
- Upgrade confirmed: 2026-09-04. Josh confirmed that refreshing the Control UI updated its stale GPT 5.4 dropdown display to the new model.
- Operating mode: main orchestrator

## Working Model

Jen should help unify context across platforms, infrastructure, AI systems, and immersive deployments.

The server itself is also managed with Codex in the CLI, and that path should be used where useful for implementation and operational work.

For the more detailed control-plane model and proposed remote subagent API contract, see:
- `agent-orchestration-and-remote-subagents.md`

## Related Agent Projects (2026-10-21)

- [MetaDyn Agent Toolkit](https://github.com/MetaDyn/MetaDynAgentToolkit) (MAT) is its own repository, separate from Jen and the deployable remote subagent. It is the proposed shared contract and adapter layer for NVIDIA NeMo Agent Toolkit, Google ADK, and the MetaDyn Digital Fabric. The Python SDK environment and basic CLI/import checks are documented; core contracts, runtime adapters, and live Fabric integration are not yet implemented.
- [MetaDyn Remote Subagent](https://github.com/MetaDyn/MetaDynRemoteSubagent) is a separate host-side service for delegated tasks. On `main` through `cd9dcfc`, it has one shared Node handler with Node and Netlify entry points, bearer-authenticated `connectivity` and read-only `workspace_review` tasks, Codex SDK modes for API key, persistent ChatGPT login, and local OpenAI-compatible models, plus structured telemetry. Its test suite passed 17 tests. A live MetaDyn-network Ollama model answered a basic question through the model adapter; the exact-`OK` task returned HTTP 502 when the model replied `OK.`. Netlify deployment, a Jen-origin request, and live Codex workspace review are unverified.
- Jen should choose and frame delegation, then synthesize returned results. The planned next step for the subagent is capability discovery and routing across host-local text, audio, and video services, with asynchronous status and artifacts for long media tasks. These features are not implemented yet.

## System Responsibilities

Potential long-term responsibilities include:
- maintaining environment documentation
- assisting with infrastructure operations
- coordinating system context
- supporting AI avatar architecture
- managing persistent knowledge artifacts
- helping standardize operational runbooks

## Memory Direction

A major MetaDyn objective is persistent, unified memory across platforms and AI/avatar systems.

This repository should document:
- what memory layers exist
- what data belongs in each layer
- how memory is synchronized
- what should and should not be persisted
- privacy and security boundaries for memory systems
