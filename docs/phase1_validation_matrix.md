# Phase 1 Validation Matrix

This document defines the minimum representative validation set for Phase 1 development.

Phase 1 is intentionally conservative. The goal is not to accept every mesh. The goal is to succeed reliably on supported meshes and fail clearly on unsupported ones.

## Phase 1 Acceptance Rules

Expected supported input characteristics:

- active object is a mesh
- mesh contains faces
- mesh is watertight and manifold, or can be converted through the temporary closed-proxy workflow
- object can be handled by a conservative two-part mold workflow
- world-axis pull scoring yields a usable practical direction

Expected Phase 1 behavior:

- generate output in `Mold_Output`
- preserve the original source object
- use explicit user-facing failure messages when validation fails
- warn when a temporary remeshed proxy is used for non-manifold input
- produce rigid printable halves instead of placeholder non-solid planning geometry
- avoid silently broadening into insert or multipart strategies

## Baseline Validation Cases

### Case 1: Rounded simple solid

Example shape:

- sphere
- capsule
- rounded decorative pebble

Expected result:

- should pass mesh validation
- should choose a stable axis-based pull direction
- should generate two rigid mold halves successfully
- halves should include flange and registration features suitable for printing and reassembly

Why this case exists:

- establishes the easiest supported baseline

### Case 2: Boxy asymmetric solid

Example shape:

- figurine torso without undercuts
- asymmetric product housing
- offset block with mixed face orientations

Expected result:

- should pass mesh validation
- pull-direction scoring should remain inspectable and deterministic
- generated halves should still be produced without mutating the source mesh

Why this case exists:

- checks that Phase 1 is not limited to perfectly symmetric objects

### Case 3: Non-manifold but proxy-recoverable mesh

Example shape:

- Blender Suzanne with non-manifold details
- decorative mesh with open seams that voxel remesh can close conservatively

Expected result:

- should warn that a temporary watertight proxy is being used
- should preserve the original source object
- should generate mold halves from the proxy rather than hard-failing immediately

Why this case exists:

- captures the explicit project requirement that common non-manifold meshes still get a usable conservative path

### Case 4: Through-hole object

Example shape:

- torus-like part
- handle with a closed loop
- part with a full pass-through channel

Expected Phase 1 result:

- may fail gracefully if the current two-part strategy is unsafe
- must not crash or produce silent garbage geometry

Why this case exists:

- captures an important boundary between simple solids and more complex demolding cases

### Case 5: Clear undercut

Example shape:

- hook
- mushroom-like cap shape
- reverse lip that traps a two-part pull direction

Expected Phase 1 result:

- should be rejected or clearly marked unsupported until Phase 2 work exists

Why this case exists:

- prevents accidental scope creep into insert handling

### Case 6: Thin or fragile features

Example shape:

- tall thin fin
- narrow protrusion near the parting region
- sharp decorative spikes

Expected Phase 1 result:

- should either produce conservative output or fail explicitly if the geometry is unsafe for current booleans

Why this case exists:

- catches geometry-generation fragility and boolean instability early

## What To Record During Validation

For each representative object, record:

- object class and why it was chosen
- expected phase classification: supported, unsupported, or deferred
- actual validation outcome
- chosen pull direction if generation proceeds
- whether output collection, naming, and source preservation behaved correctly
- any crash, boolean instability, or misleading error message

## When To Update This Matrix

Update this document when:

- Phase 1 support expands or narrows
- a new recurring failure class appears
- representative validation cases become part of repeated development work
- Phase 2 or Phase 3 introduces new expected outcomes for an existing case
