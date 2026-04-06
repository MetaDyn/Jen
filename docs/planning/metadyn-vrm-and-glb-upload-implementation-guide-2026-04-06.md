# MetaDyn VRM and GLB Upload Implementation Guide

## Purpose

Explain how MetaDyn can support user avatar uploads with:

- `VRM`
- `GLB`

and turn accepted uploads into avatars that work with the Pavilion player runtime.

This document is intentionally practical. It includes:

- architecture
- setup steps
- validation rules
- runtime flow
- starter C# scripts

These scripts are a starting scaffold, not a complete production drop-in.

## Recommended First Scope

Version 1 should support:

- `VRM` uploads
- `GLB` uploads with an existing humanoid rig
- strict validation
- runtime binding to the existing MetaDyn player object

Version 1 should not try to:

- auto-rig unrigged meshes
- fully repair broken skeletons
- support every arbitrary `FBX`

## Why VRM and GLB First

### VRM

Best first BYOA format because:

- avatar-oriented format
- humanoid-friendly
- good fit for user-provided characters
- typically easier to validate consistently

### GLB

Good secondary format because:

- web-friendly
- already broadly used
- current repo already includes `com.unity.cloud.gltfast`

### FBX

Not recommended for first public upload version because:

- more fragile
- worse pipeline consistency
- often requires more importer-specific cleanup

## Repo Fit

Current repo facts that matter:

- Pavilion is Unity 6 + URP
- `Packages/manifest.json` already includes `com.unity.cloud.gltfast`
- current player runtime is built around:
 - `Assets/Pavilion/Scripts/Player.cs`
 - `Assets/Pavilion/Scripts/PlayerInput.cs`
 - `Assets/Pavilion/Scripts/GameManager.cs`
- current avatar flow is prefab-based

That means the first implementation should:

- keep the existing network player object
- attach uploaded avatar visuals to that player object
- not replace movement/networking with imported avatar prefabs

## Recommended Package Setup

## GLB Support

Already present:

- `com.unity.cloud.gltfast`

Use that for:

- loading `GLB`
- extracting instantiated runtime hierarchy

## VRM Support

Recommended production choice:

- use `UniVRM v0.131.0`
- install it through `UPM` with pinned git URLs
- do not use a floating `latest`
- do not rely on manually imported `unitypackage` files for the production repo

Reason:

- official release page says UniVRM supports `Unity 2022.3 LTS or later`
- Unity 6 is within that supported baseline
- `v0.131.0` is the current latest official release
- pinning an exact version is the safest production posture
- this repo already uses package-based dependency management, so UPM is the correct fit

Recommended package set for MetaDyn:

- `com.vrmc.vrm`
 - VRM 1.0 support
- `com.vrmc.univrm`
 - VRM 0.x compatibility path
- `com.vrmc.gltf`
 - UniVRM's underlying glTF package

Why install both VRM packages:

- many existing creator avatars are still `VRM 0.x`
- production upload support should not silently exclude older creator files
- MetaDyn should support:
 - `VRM 1.0`
 - legacy `VRM 0.x`

Important official install note:

- from `v0.131.0`, the package paths moved from `Assets/...` to `Packages/...`
- use the new `Packages/...` git URLs

Recommended `Packages/manifest.json` additions:

```json
{
 "dependencies": {
 "com.vrmc.gltf": "https://github.com/vrm-c/UniVRM.git?path=/Packages/UniGLTF#v0.131.0",
 "com.vrmc.univrm": "https://github.com/vrm-c/UniVRM.git?path=/Packages/VRM#v0.131.0",
 "com.vrmc.vrm": "https://github.com/vrm-c/UniVRM.git?path=/Packages/VRM10#v0.131.0"
 }
}
```

Recommended install policy:

1. create a branch just for package integration
2. add the pinned manifest entries
3. let Unity reimport
4. import the official VRM samples from Package Manager only if needed for reference
5. do not merge until runtime VRM loading is verified in Pavilion

MetaDyn should treat VRM support as a package dependency, not custom parser work.

## High-Level Flow

The upload flow should work like this:

1. user picks file in upload UI
2. backend or local intake stores file
3. format is identified:
 - `vrm`
 - `glb`
4. validator inspects:
 - skeleton
 - humanoid compatibility
 - size/budget
 - materials
 - face support
5. if accepted:
 - normalize scale/orientation/materials
 - create runtime descriptor
6. player runtime loads the normalized avatar
7. runtime binder attaches avatar to the MetaDyn player object
8. face/lip-sync adapter is chosen based on avatar capabilities

## Runtime Strategy

Do not spawn uploaded avatars as the main network prefab.

Instead:

- keep a canonical MetaDyn player prefab
- add a visual root under that player
- load the accepted avatar into the visual root
- bind animator/avatar metadata to the player runtime

This preserves:

- networking
- movement
- name tags
- voice logic
- camera behavior

## Minimal Scene Setup

Recommended components:

### 1. Upload Manager

Scene object:

- `AvatarUploadManager`

Responsibilities:

- receive selected file
- classify file type
- run validation
- persist descriptor

### 2. Avatar Runtime Binder

Attach to player root or visual root:

- `PlayerAvatarRuntimeBinder`

Responsibilities:

- destroy previous visual avatar
- instantiate accepted avatar
- bind animator
- derive anchors
- attach lip-sync adapter

### 3. Validation Service

Can start as a local utility:

- `AvatarValidationService`

Responsibilities:

- inspect imported avatar
- return pass/fail + warnings

## Suggested Folder Layout

If implemented in code, use something like:

```text
Assets/MetaDyn/Avatars/Runtime/
Assets/MetaDyn/Avatars/Upload/
Assets/MetaDyn/Avatars/Validation/
Assets/MetaDyn/Avatars/Importers/
Assets/MetaDyn/Avatars/LipSync/
```

## Data Model

Basic upload descriptor:

```csharp
using System;

namespace MetaDyn.Avatars
{
 public enum AvatarSourceFormat
 {
 Unknown = 0,
 VRM = 1,
 GLB = 2
 }

 public enum AvatarFaceSupportTier
 {
 None = 0,
 Basic = 1,
 Full = 2
 }

 [Serializable]
 public class AvatarUploadDescriptor
 {
 public string AvatarId;
 public string OwnerUserId;
 public AvatarSourceFormat SourceFormat;
 public string OriginalFileName;
 public string OriginalFilePath;
 public string RuntimeAssetPath;
 public AvatarFaceSupportTier FaceSupportTier;
 public bool IsHumanoid;
 public float HeightMeters;
 public int TriangleCount;
 public int MaterialCount;
 }
}
```

## Validation Result Model

```csharp
using System.Collections.Generic;

namespace MetaDyn.Avatars
{
 public sealed class AvatarValidationResult
 {
 public bool IsValid;
 public bool CanAutoFix;
 public AvatarFaceSupportTier FaceSupportTier;
 public readonly List<string> Errors = new();
 public readonly List<string> Warnings = new();
 }
}
```

## Upload Manager Starter Script

This is the high-level intake service.

```csharp
using System;
using System.IO;
using UnityEngine;

namespace MetaDyn.Avatars
{
 public sealed class AvatarUploadManager : MonoBehaviour
 {
 [SerializeField] private AvatarValidationService validationService;

 public AvatarUploadDescriptor CreateDescriptor(string userId, string filePath)
 {
 var format = DetectFormat(filePath);

 return new AvatarUploadDescriptor
 {
 AvatarId = Guid.NewGuid().ToString("N"),
 OwnerUserId = userId,
 SourceFormat = format,
 OriginalFileName = Path.GetFileName(filePath),
 OriginalFilePath = filePath
 };
 }

 public AvatarSourceFormat DetectFormat(string filePath)
 {
 var ext = Path.GetExtension(filePath).ToLowerInvariant();

 return ext switch
 {
 ".vrm" => AvatarSourceFormat.VRM,
 ".glb" => AvatarSourceFormat.GLB,
 _ => AvatarSourceFormat.Unknown
 };
 }

 public AvatarValidationResult ValidateAvatar(AvatarUploadDescriptor descriptor, GameObject importedRoot)
 {
 if (validationService == null)
 {
 return new AvatarValidationResult
 {
 IsValid = false,
 CanAutoFix = false
 };
 }

 return validationService.Validate(importedRoot, descriptor.SourceFormat);
 }
 }
}
```

## Validation Service Starter Script

This validates the imported hierarchy after the format importer loads it.

```csharp
using System.Linq;
using UnityEngine;

namespace MetaDyn.Avatars
{
 public sealed class AvatarValidationService : MonoBehaviour
 {
 [Header("Geometry Limits")]
 [SerializeField] private int maxTriangles = 100000;
 [SerializeField] private int maxMaterials = 8;

 public AvatarValidationResult Validate(GameObject avatarRoot, AvatarSourceFormat format)
 {
 var result = new AvatarValidationResult();

 if (avatarRoot == null)
 {
 result.Errors.Add("Avatar root is null.");
 return result;
 }

 var animator = avatarRoot.GetComponentInChildren<Animator>(true);
 if (animator == null)
 {
 result.Errors.Add("No Animator found.");
 return result;
 }

 if (animator.avatar == null || !animator.avatar.isHuman || !animator.avatar.isValid)
 {
 result.Errors.Add("Avatar is not a valid humanoid.");
 return result;
 }

 var renderers = avatarRoot.GetComponentsInChildren<SkinnedMeshRenderer>(true);
 if (renderers.Length == 0)
 {
 result.Errors.Add("No skinned mesh renderers found.");
 return result;
 }

 int triangleCount = 0;
 int materialCount = 0;

 foreach (var renderer in renderers)
 {
 if (renderer.sharedMesh != null)
 {
 triangleCount += renderer.sharedMesh.triangles.Length / 3;
 }

 materialCount += renderer.sharedMaterials.Count(m => m != null);
 }

 if (triangleCount > maxTriangles)
 {
 result.Errors.Add($"Triangle count too high: {triangleCount} > {maxTriangles}");
 }

 if (materialCount > maxMaterials)
 {
 result.Warnings.Add($"Material count high: {materialCount} > {maxMaterials}");
 }

 result.FaceSupportTier = DetectFaceSupport(renderers);
 result.CanAutoFix = true;
 result.IsValid = result.Errors.Count == 0;
 return result;
 }

 private AvatarFaceSupportTier DetectFaceSupport(SkinnedMeshRenderer[] renderers)
 {
 bool hasBasic = false;
 bool hasFull = false;

 foreach (var renderer in renderers)
 {
 var mesh = renderer.sharedMesh;
 if (mesh == null)
 continue;

 for (int i = 0; i < mesh.blendShapeCount; i++)
 {
 string shape = mesh.GetBlendShapeName(i).ToLowerInvariant();

 if (shape.Contains("mouth") || shape.Contains("jaw"))
 {
 hasBasic = true;
 }

 if (shape.Contains("viseme") || shape == "aa" || shape == "ih" || shape == "ou")
 {
 hasFull = true;
 }
 }
 }

 if (hasFull) return AvatarFaceSupportTier.Full;
 if (hasBasic) return AvatarFaceSupportTier.Basic;
 return AvatarFaceSupportTier.None;
 }
 }
}
```

## Runtime Binder Starter Script

This attaches the validated avatar visual to the existing player runtime.

```csharp
using UnityEngine;

namespace MetaDyn.Avatars
{
 public sealed class PlayerAvatarRuntimeBinder : MonoBehaviour
 {
 [SerializeField] private Transform visualRoot;
 [SerializeField] private RuntimeAnimatorController locomotionController;

 private GameObject _currentAvatar;
 private Animator _currentAnimator;

 public void BindAvatar(GameObject importedAvatar, AvatarUploadDescriptor descriptor)
 {
 if (visualRoot == null)
 {
 visualRoot = transform;
 }

 ClearCurrentAvatar();

 _currentAvatar = importedAvatar;
 _currentAvatar.transform.SetParent(visualRoot, false);
 _currentAvatar.transform.localPosition = Vector3.zero;
 _currentAvatar.transform.localRotation = Quaternion.identity;
 _currentAvatar.transform.localScale = Vector3.one;

 NormalizeTransform(_currentAvatar.transform);

 _currentAnimator = _currentAvatar.GetComponentInChildren<Animator>(true);
 if (_currentAnimator != null && locomotionController != null)
 {
 _currentAnimator.runtimeAnimatorController = locomotionController;
 }
 }

 private void NormalizeTransform(Transform avatarTransform)
 {
 avatarTransform.localScale = Vector3.one;
 avatarTransform.localRotation = Quaternion.identity;
 }

 private void ClearCurrentAvatar()
 {
 if (_currentAvatar != null)
 {
 Destroy(_currentAvatar);
 _currentAvatar = null;
 _currentAnimator = null;
 }
 }
 }
}
```

## GLB Importer Example

This is the shape of the GLB runtime import path using `glTFast`.

```csharp
using System.Threading.Tasks;
using GLTFast;
using UnityEngine;

namespace MetaDyn.Avatars
{
 public sealed class GlbAvatarImporter
 {
 public async Task<GameObject> ImportAsync(string filePath)
 {
 var gltf = new GltfImport();
 bool success = await gltf.Load(filePath);
 if (!success)
 {
 return null;
 }

 var root = new GameObject("ImportedGLBAvatar");
 await gltf.InstantiateMainSceneAsync(root.transform);
 return root;
 }
 }
}
```

## VRM Importer Example

With the recommended pinned package set above, the importer should use UniVRM's runtime loading API instead of a placeholder.

```csharp
using System.Threading.Tasks;
using UnityEngine;
using UniGLTF;
using UniVRM10;

namespace MetaDyn.Avatars
{
 public sealed class VrmAvatarImporter
 {
 public async Task<GameObject> ImportAsync(string filePath)
 {
 var vrmInstance = await Vrm10.LoadPathAsync(
 filePath,
 canLoadVrm0X: true,
 showMeshes: false,
 awaitCaller: new RuntimeOnlyAwaitCaller());

 if (vrmInstance == null)
 {
 return null;
 }

 var runtimeInstance = vrmInstance.GetComponent<RuntimeGltfInstance>();
 if (runtimeInstance != null)
 {
 runtimeInstance.ShowMeshes();
 runtimeInstance.EnableUpdateWhenOffscreen();
 }

 vrmInstance.name = "ImportedVRMAvatar";
 return vrmInstance.gameObject;
 }
 }
}
```

Why this is the correct production direction:

- it uses the official runtime import API
- it allows `VRM 1.0`
- it also allows older `VRM 0.x` files through `canLoadVrm0X: true`
- it produces a real runtime object with the UniVRM components attached

Recommended production handling after import:

- inspect `Vrm10Instance`
- derive the `Animator`
- classify face support from blendshapes/expressions
- disable or tune spring-bone behavior if performance requires it
- normalize transform before binding to the player runtime

## Auto-Fix Pass

After import and before binding, the first auto-fix pass should do only safe changes:

- normalize root rotation
- normalize scale
- assign approved URP materials if required
- compress or swap oversized textures if running an offline processing step
- record face support tier

Do not attempt in version 1:

- full mesh repair
- full auto-rigging
- generating missing visemes from nothing

## Lip Sync Strategy

Version 1 face behavior should be tiered:

- `Full`
 - use viseme-capable adapter
- `Basic`
 - use jaw-open / mouth-open fallback
- `None`
 - no lip sync or reject depending on product decision

That means imported avatars can still be usable even when they do not match Avatar SDK quality exactly.

## Upload UI Setup

Basic user flow:

1. user opens profile/avatar panel
2. clicks `Upload Avatar`
3. picks `.vrm` or `.glb`
4. system displays:
 - validation result
 - warnings
 - preview if accepted
5. user confirms `Use Avatar`
6. descriptor is stored on profile
7. runtime loads normalized avatar on spawn

UI should clearly report:

- accepted
- accepted with limitations
- rejected

## First Production Rules

Start strict.

Recommended first public rules:

- `VRM` and `GLB` only
- humanoid required
- no unrigged avatars
- poly/material limits enforced
- unsupported shaders downgraded or rejected
- no guarantee of full facial animation

This is how you keep the system maintainable.

## What “Works Like Avatar SDK” Means

A compliant uploaded avatar can work like current Avatar SDK avatars in these ways:

- humanoid locomotion
- player controller compatibility
- camera compatibility
- voice speaking fallback
- networked runtime visual

It does not mean every upload will have:

- identical facial fidelity
- identical viseme set
- identical material quality

That should be framed as capability tiers, not universal parity.

## Recommended Next Implementation Steps

1. add pinned `UniVRM v0.131.0` packages through `UPM`
2. create the Avatar upload/runtime folders under `Assets/MetaDyn/Avatars/`
3. implement local runtime import tests for:
 - one VRM
 - one GLB humanoid avatar
4. validate against the `MetaDyn_Avatar_Upload_Spec`
5. bind imported avatar to a single local test player
6. only after that:
 - connect profile persistence
 - connect multiplayer reconstruction
 - connect lip-sync abstraction

## UniVRM Recommendation Summary

For this repo, the recommended production answer is:

- install `UniVRM v0.131.0`
- use `UPM`, not loose unitypackages
- pin the exact git URLs in `Packages/manifest.json`
- support both:
 - `VRM 1.0`
 - `VRM 0.x`
- use `Vrm10.LoadPathAsync(... canLoadVrm0X: true ...)` as the primary runtime import path

That is the cleanest path to solid production-quality VRM uploads in Pavilion.

## Sources

- UniVRM official install docs:
 - https://vrm.dev/en/univrm/install/univrm_install/
- UniVRM official release page:
 - https://github.com/vrm-c/UniVRM/releases
- UniVRM runtime import docs:
 - https://vrm.dev/en/api/runtime-import/VRM_VrmUtility/
- UniVRM runtime load example:
 - https://vrm.dev/en/api/humanoid/runtime_vrma/
