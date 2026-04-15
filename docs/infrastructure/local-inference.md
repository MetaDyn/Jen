# Local Inference

## Summary

MetaDyn currently has a working local inference path for OpenClaw/Jen using LM Studio on the Windows host and OpenClaw in the Ubuntu VM.

This is a host-backed local model path, not GPU passthrough inside the VM.

## Current Shape

- Windows host runs LM Studio with local Gemma models.
- Ubuntu VM runs OpenClaw and calls LM Studio over the private network.
- OpenClaw local provider endpoint is:
  - `http://192.168.0.187:1234/v1`
- Configured local models in `~/.openclaw/openclaw.json`:
  - `lmstudio/gemma-4-e2b-it`
  - `lmstudio/gemma-4-e4b-it`
- OpenClaw primary default model remains:
  - `openai-codex/gpt-5.4`

## What Was Configured

- Added an `lmstudio` provider in OpenClaw config.
- Pointed that provider at the Windows host LM Studio server on the private LAN.
- Added Gemma 4 local model entries to the available OpenClaw model list.
- Kept Codex as the default primary model while allowing local Gemma session overrides.
- Verified the Ubuntu VM can reach the host LM Studio endpoint.
- Confirmed this path uses host-side GPU inference through LM Studio, not VM GPU passthrough.

## LM Studio And OpenClaw Notes

- The working OpenClaw path for local Gemma is intentionally slimmed down.
- Local Gemma currently uses:
  - text input
  - image input
- Local Gemma does not use the full coding-agent tool payload on this path.
- The local Gemma prompt keeps a compact MetaDyn/OpenClaw identity plus memory/docs grounding.

## Prompt/Behavior Notes

The local Gemma path was tuned to keep latency low while preserving identity.

Current prompt intent is:
- identity: OpenClaw for MetaDyn
- default scope: MetaDyn unless user changes scope
- grounding priority:
  - `docs/README.md`
  - `OPENCLAW_OVERVIEW.md`
  - `AGENTS.md`
  - `MEMORY.md`
  - `memory/*.md`

## Known Limits

- `gemma-4-e4b-it` has worked in the local OpenClaw path after prompt slimming, but earlier direct public endpoint testing showed load instability on some runs.
- `gemma-4-e2b-it` responded reliably in prior public endpoint testing.
- Image understanding on the local Gemma path is functional but has produced generic/weak outputs in observed tests.
- The fast local Gemma path is optimized for lightweight contextual chat, not the full heavy coding-agent/tool contract.

## Public Endpoint Note

Prior testing also exists for the public MetaDyn endpoint:
- `https://aurora-02.metadyn.xyz/api/v1/chat`

Observed prior test notes:
- expects `model` + `input`
- `gemma-4-e2b-it` responded successfully
- `gemma-4-e4b-it` failed to load in at least one earlier test
- image input was accepted for `gemma-4-e2b-it`
- Josh later provided the current public test curl, which also confirms support for `system_prompt`

Current reference curl:
```bash
curl https://aurora-02.metadyn.xyz/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "gemma-4-e2b-it", "system_prompt": "Answer in a more direct, technical manner", "input": "What is the Metaverse?"}'
```

Current practical interpretation:
- this is the public MetaDyn chat/inference surface on `aurora-02`
- it currently provides Gemma 4 e2b processing
- it is expected to evolve into the backing endpoint for Aurora, Jen's embodied Metaverse presence

## Where To Check

- OpenClaw config:
  - `~/.openclaw/openclaw.json`
- Workspace memory:
  - `memory/2026-04-09.md`
  - `memory/2026-04-10.md`
