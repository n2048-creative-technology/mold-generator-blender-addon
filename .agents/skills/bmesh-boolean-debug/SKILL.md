---
name: bmesh-boolean-debug
description: Diagnose and stabilize Blender mesh, BMesh, and boolean failures in mold-generation workflows. Use when geometry operations already exist but produce invalid meshes, missing faces, non-manifold output, inverted normals, or unreliable boolean results.
metadata:
  version: 2
  scope: geometry-debugging
  phases:
    - phase-1
    - phase-2
    - phase-3
  primary_paths:
    - src/blender_auto_mold/geometry/
    - src/blender_auto_mold/utils/object_ops.py
    - src/blender_auto_mold/analysis/mesh_validation.py
    - docs/phase1_validation_matrix.md
  outputs:
    - reproducible failure reports
    - safer boolean workflow
    - debug instrumentation
  related_skills:
    - mold-feature-generation
    - parting-analysis
    - test-scene-validation
---

# BMesh Boolean Debug

Use this skill when geometry generation exists but the mesh operations are unstable.

## Use this skill when

- boolean modifiers fail or produce empty results
- generated parts become non-manifold or self-intersecting
- normals flip unexpectedly during mold generation
- temporary operands or cleanup steps corrupt the output
- a reproducible geometry failure needs explicit debug instrumentation

Typical requests sound like:

- "the boolean exploded"
- "generated halves are invalid"
- "this mesh turns non-manifold"
- "help debug the BMesh pipeline"

## Do not use this skill when

- the main issue is choosing the correct mold strategy
- the task is only Blender UI wiring
- no concrete geometry failure exists yet
- the task is general moldmaking research without a broken mesh path

## Concrete inputs

- the failing mesh class or scene case
- current geometry code path and the exact failing step
- any validation or error messages already available
- representative case expectations from `docs/phase1_validation_matrix.md`

## Expected outputs

- a reproducible failure description
- narrowed root cause in operands, topology, or operation order
- safer geometry steps, extra validation, or debug outputs
- updated validation notes if the failure represents a new unsupported case

## Read first

1. `AGENTS.md`
2. relevant files under `src/blender_auto_mold/geometry/`
3. `src/blender_auto_mold/utils/object_ops.py`
4. `src/blender_auto_mold/analysis/mesh_validation.py`
5. `docs/phase1_validation_matrix.md`

## Workflow

1. Reproduce the failure on the smallest representative case available.
2. Separate the problem into one of these buckets:
   - bad input mesh
   - wrong parting decision
   - unstable operand construction
   - unsafe boolean order or cleanup
3. Inspect intermediate geometry explicitly instead of guessing.
4. Prefer deterministic debug signals:
   - named temporary objects
   - extra validation checks
   - counts of missing or invalid faces
   - clear error messages
5. Stabilize the pipeline at the root cause, not by hiding the failure.
6. If the root problem is actually unsupported geometry for the current phase, reject it clearly and document the boundary.
7. Add or update validation notes so the failure class is tested again later.

## Failure handling

- If the problem is caused by unsupported input geometry, do not contort the pipeline into pretending support exists.
- If the failure is intermittent, add deterministic debug outputs before making broad structural changes.
- If the boolean path is fundamentally unsafe for Phase 1, prefer explicit graceful failure over brittle heuristics.

## File update expectations

Typical files for this skill:

- `src/blender_auto_mold/geometry/*.py`
- `src/blender_auto_mold/utils/object_ops.py`
- `src/blender_auto_mold/analysis/mesh_validation.py`
- `docs/phase1_validation_matrix.md`
- debug notes in `docs/` when a failure class becomes recurrent

## Boundary with nearby skills

- `mold-feature-generation` owns the intended geometry; this skill hardens it when execution breaks.
- `parting-analysis` should be revisited only if the failure reveals a wrong separation decision.
- `test-scene-validation` captures the fixed failure as a representative regression case afterward.
