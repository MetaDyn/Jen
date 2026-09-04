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
