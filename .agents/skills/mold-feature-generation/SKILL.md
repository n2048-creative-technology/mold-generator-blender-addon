---
name: mold-feature-generation
description: Generate the concrete mold-system geometry for this project, including cavity blocks, silicone shell offsets, rigid support geometry, flanges, alignment features, clamp features, vents, and sprues. Use when the mold strategy is already known and the task is building or modifying generated parts.
metadata:
  version: 2
  scope: geometry-generation
  phases:
    - phase-1
    - phase-2
    - phase-3
  primary_paths:
    - docs/geometry_algorithm_blueprint.md
    - src/blender_auto_mold/geometry/
    - src/blender_auto_mold/utils/collections.py
    - src/blender_auto_mold/utils/object_ops.py
    - src/blender_auto_mold/utils/units.py
  outputs:
    - generated mold parts
    - geometry helpers
    - collection and naming behavior
  related_skills:
    - parting-analysis
    - bmesh-boolean-debug
    - prusa-3d-printing-mold-output
---

# Mold Feature Generation

Use this skill when the task is creating or revising the actual mold-part geometry.

## Use this skill when

- building the Phase 1 two-part mold blocks
- generating silicone or rigid shell geometry
- adding flanges, keys, clamp features, sprues, or vents
- changing output naming, duplication flow, or collection behavior
- converting analysis results into produced mold parts

Typical requests sound like:

- "build the mold halves"
- "add alignment keys"
- "generate flanges around the seam"
- "route output parts into collections"

## Do not use this skill when

- the main question is still how the object should split
- the task is mostly Blender operator or panel wiring
- the work is printer-fit planning after parts already exist
- the main issue is stabilizing failed boolean operations rather than designing geometry

## Concrete inputs

- the accepted mold strategy and any analysis outputs
- source-object handling rules from `AGENTS.md`
- existing geometry code under `src/blender_auto_mold/geometry/`
- collection, object, and unit helpers under `src/blender_auto_mold/utils/`

## Expected outputs

- generated geometry that respects source-preservation rules
- named output parts in the proper collection
- reusable geometry helpers instead of large operator logic
- docs when mold-part behavior or parameter expectations change materially

## Read first

1. `AGENTS.md`
2. `docs/geometry_algorithm_blueprint.md`
3. `docs/skills_design.md`
4. `src/blender_auto_mold/geometry/*`
5. `src/blender_auto_mold/utils/collections.py`
6. `src/blender_auto_mold/utils/object_ops.py`
7. `src/blender_auto_mold/utils/units.py`

## Workflow

1. Confirm the upstream parting decision and phase boundary before building parts.
2. Preserve the original source object by duplicating before any destructive operation.
3. Keep generation steps explicit and inspectable:
   - create operands
   - apply operations in a controlled order
   - name outputs clearly
   - clean up temporary objects
4. Route generated parts into the output collection instead of leaving them mixed with source content.
5. Keep millimeter parameters explicit and convert units at the boundary.
6. Favor the smallest number of mold parts consistent with safe demolding and assembly.
7. Protect sealing faces, alignment geometry, and demolding paths from incidental edits.
8. Update docs if a new generated feature changes what contributors should expect from the pipeline.

## Failure handling

- If a requested feature depends on Phase 2 or 3 analysis that does not exist yet, stop at a documented boundary.
- If geometry steps become unstable, add explicit intermediate debug objects or hand off to `bmesh-boolean-debug`.
- If a temporary workaround would mutate the source mesh in place, do not use it.

## File update expectations

Typical files for this skill:

- `src/blender_auto_mold/geometry/*.py`
- `src/blender_auto_mold/utils/collections.py`
- `src/blender_auto_mold/utils/object_ops.py`
- `src/blender_auto_mold/utils/units.py`
- `docs/geometry_algorithm_blueprint.md`
- `README.md` when output behavior changes materially

## Boundary with nearby skills

- `parting-analysis` decides how the mold should separate; this skill constructs the resulting parts.
- `bmesh-boolean-debug` begins when geometry exists but mesh operations are unreliable.
- `prusa-3d-printing-mold-output` begins after rigid parts exist or their envelopes are well defined.
