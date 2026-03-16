# Platform Overview

## Summary

MetaDyn is a creator-first metaverse platform centered around a Unity 6 runtime, a reusable SDK/platform layer, and a deployment model for immersive multi-user spaces.

The current imported documentation shows a platform that already combines:
- multi-user WebGL spaces
- persistent identity and profile systems
- voice and avatar systems
- moderation and user management
- deployment tooling inside the Unity workflow
- a path toward shared-hosted and self-hosted deployments

## Product Layers

The imported PRD describes MetaDyn as three connected product layers.

### 1. MetaDyn SDK
A reusable Unity platform layer that provides runtime systems, editor tooling, deployment tooling, auth integration, and platform services.

### 2. MetaDyn Starter Space Template
A MetaDyn-owned Unity starter project/template containing the SDK plus a ready-to-build starter world.

### 3. MetaDyn Hosted Platform
The runtime and hosting layer for deployed spaces, including WebGL hosting, auth/session continuity, backend integration, and support for managed/shared hosting as well as self-hosting.

## Platform Goals

The Unity platform is designed to:
- let creators build and deploy multi-user WebGL spaces with low friction
- keep deployment as a first-class part of the SDK workflow
- support identity continuity across spaces and subdomains
- provide strong social and voice foundations
- support embodied AI as a native differentiator
- support both managed/shared hosting and self-hosted deployment models

## Core Pillars

### Unity SDK Platform Layer
The SDK is the reusable core. It should be installable into Unity projects and carry platform logic, runtime services, editor features, and deployment tooling.

### Space Deployment
Each space is its own build. Deployment is per-space, with runtime configuration and isolated hosting paths.

### Identity and Access
The platform uses web-first auth, persistent profiles, avatar persistence, owner/admin identification, and cross-space session continuity.

### Social / Multiplayer
The platform includes multiplayer sessions, moderation, synchronized presence, user lists, and voice communication.

### Embodied Experience Foundation
Even though broader AI docs will be organized separately later, the platform already expects space experiences to support avatars, voice, embodied presence, and persistent context.

## Current Positioning

The imported docs consistently position MetaDyn as:
- WebGL-first
- creator-first
- SDK-driven
- deployment-aware
- able to support both internal spaces and client/partner spaces

This makes the Unity 6 platform the main delivery layer for the broader MetaDyn metaverse vision.
