# SDK Update Manifest

First-pass manifest format for the MetaDyn SDK update check system.

**Status:** Planned | **Last Updated:** 2026-03-02

---

## Purpose

This manifest is the remote source the Unity `MetaDyn Dashboard` should check to determine:

- installed SDK version vs latest SDK version
- supported Unity version range
- supported Photon Fusion version
- download/update target
- tracked SDK-owned file roots
- optional components available for later install

The current working SDK file layout is the source of truth. The updater should target those same paths.

---

## Current Status

Confirmed current state:

- `MetaDynVoiceController` has been moved into `Assets/MetaDyn/AI/MetaDynVoiceController.cs`
- `MetaDynDashboard` now shows mock SDK update UI
- `MetaDynDashboard` shows supported + installed Photon Fusion version
- a real SDK manifest file now exists at `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynSDKManifest.json`
- current working file locations are the canonical update/install targets
- `Assets/StreamingAssets/microphone-processor.js` is confirmed required by the active WebGL microphone pipeline

Remaining implementation gap:

- dashboard still uses mock SDK version lookup instead of fetching remote manifest data

---

## Canonical Paths

Until intentionally redesigned, the SDK updater should treat these paths as canonical:

- `Assets/MetaDyn`
- `Assets/Common`
- `Assets/Plugins/WebGL`
- `Assets/Pavilion/Scripts/GameManager.cs`
- `Assets/Pavilion/Scripts/Player.cs`
- `Assets/Pavilion/Scripts/PlayerInput.cs`
- `Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs`
- `Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs`
- `Assets/Photon`
- `Assets/StreamingAssets/microphone-processor.js`

That means the update system should pull files back into these same locations.

---

## Manifest File

File:
- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynSDKManifest.json`

Shape:

```json
{
  "sdkName": "MetaDyn SDK",
  "channel": "stable",
  "latestVersion": "1.0.0",
  "minimumSupportedVersion": "1.0.0",
  "unity": {
    "minimumVersion": "6000.0.62f1",
    "recommendedVersion": "6000.0.67f1"
  },
  "fusion": {
    "required": true,
    "supportedVersion": "2.0.9 Stable",
    "minimumVersion": "2.0.9"
  },
  "releaseNotesUrl": "https://github.com/MetaDyn/MetaDynSDK/releases/tag/v1.0.0",
  "downloadUrl": "https://github.com/MetaDyn/MetaDynSDK/archive/refs/tags/v1.0.0.zip",
  "packageRoot": "Assets",
  "trackedRoots": [
    "Assets/MetaDyn",
    "Assets/Common",
    "Assets/Plugins/WebGL",
    "Assets/Pavilion/Scripts/GameManager.cs",
    "Assets/Pavilion/Scripts/Player.cs",
    "Assets/Pavilion/Scripts/PlayerInput.cs",
    "Assets/Pavilion/Scripts/AvatarSdkPlayerLipSync.cs",
    "Assets/Pavilion/Scripts/Wolf3DPlayerLipSync.cs",
    "Assets/Photon",
    "Assets/StreamingAssets/microphone-processor.js"
  ]
}
```

---

## Field Meanings

- `sdkName`
  - Display name for UI/debug purposes.

- `channel`
  - Update channel such as `stable` or `beta`.

- `latestVersion`
  - The newest available SDK version for this channel.

- `minimumSupportedVersion`
  - Lowest installed version that can be updated directly without special migration handling.

- `unity.minimumVersion`
  - Oldest Unity version supported by this release.

- `unity.recommendedVersion`
  - Preferred Unity editor version for this release.

- `fusion.required`
  - Whether Photon Fusion is mandatory for this SDK release.

- `fusion.supportedVersion`
  - Exact supported Fusion version string shown in the MetaDyn Dashboard.

- `fusion.minimumVersion`
  - Lowest acceptable Fusion version before the dashboard warns/blocks.

- `releaseNotesUrl`
  - Link to release notes shown by the dashboard later.

- `downloadUrl`
  - Archive/package source used by the updater.

- `packageRoot`
  - Root folder used to resolve tracked roots in the downloaded artifact.

- `trackedRoots`
  - Canonical SDK-owned folders/files that the updater manages.

- `optionalComponents`
  - Reserved for future installable extras.

- `notices`
  - Reserved for UI messages, migration notes, and warnings.

---

## Dashboard Use

`MetaDynDashboard` should eventually:

1. Read installed local SDK version.
2. Fetch remote manifest JSON.
3. Compare installed version to `latestVersion`.
4. Show:
   - installed version
   - latest version
   - update status
   - supported Fusion version
   - installed Fusion version
5. Enable `Update SDK` only when update is available and compatible.

---

## Next Implementation Step

Replace the current mock `GetLatestVersion()` logic in:

- `Assets/MetaDyn/Core/Editor/MetaDynSDK/MetaDynDashboard.cs`

with:

- remote manifest fetch
- JSON parse
- version comparison using `latestVersion`

The updater should not invent new file destinations. It should update the canonical paths listed above.
