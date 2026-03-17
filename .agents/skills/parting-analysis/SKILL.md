---
name: parting-analysis
description: Analyze pull direction, undercuts, seam candidates, and mold split strategy for a mesh. Use when the task is deciding how the object should demold or whether a conservative two-part mold is viable before geometry generation.
metadata:
  version: 2
  scope: geometry-analysis
  phases:
    - phase-1
    - phase-2
    - phase-3
  primary_paths:
    - docs/geometry_algorithm_blueprint.md
    - src/blender_auto_mold/analysis/mesh_validation.py
    - src/blender_auto_mold/analysis/pull_direction.py
    - src/blender_auto_mold/analysis/types.py
  outputs:
    - validation rules
    - pull-direction scoring
    - seam or undercut decisions
  related_skills:
    - mold-research
    - mold-feature-generation
    - bmesh-boolean-debug
---

# Parting Analysis

Use this skill when the main question is how a mesh should separate, demold, or be rejected.

## Use this skill when

- deciding the best pull direction
- defining conservative Phase 1 acceptance rules for meshes
- identifying undercuts or seam candidates
- deciding whether a two-part mold is sufficient
- adding debug visibility for analysis decisions

Typical requests sound like:

- "how should this object split"
- "score pull directions"
- "detect undercuts"
- "when should Phase 1 reject a mesh"

## Do not use this skill when

- the parting strategy is already chosen and the task is geometry construction
- the task is Blender UI wiring
- the main issue is a boolean or BMesh failure after geometry already exists
- the user only needs physical rationale with no mesh-level implementation

## Concrete inputs

- the mesh class or selected object behavior to analyze
- current project phase and acceptance rules
- existing analysis structures under `src/blender_auto_mold/analysis/`
- any current debug or failure-reporting expectations

## Expected outputs

- mesh validation or pull-direction logic
- explicit supported versus unsupported analysis outcomes
- structured outputs that geometry generation can consume
- clear debug or user-facing reporting for analysis results

## Read first

1. `AGENTS.md`
2. `docs/geometry_algorithm_blueprint.md`
3. `docs/skills_design.md`
4. `src/blender_auto_mold/analysis/mesh_validation.py`
5. `src/blender_auto_mold/analysis/pull_direction.py`
6. `src/blender_auto_mold/analysis/types.py`

## Workflow

1. Confirm the current phase boundary before broadening acceptance logic.
2. Start with explicit validation rules before any scoring heuristics.
3. Produce structured analysis outputs rather than burying decisions inside operators.
4. Keep Phase 1 conservative:
   - prefer simple, inspectable pull candidates
   - reject unsupported undercuts clearly
   - avoid silently inventing inserts or multipart solutions
5. Make scoring and rejection logic inspectable through named results, counts, or future debug helpers.
6. Hand off cleanly to geometry generation with outputs that answer:
   - can this object proceed
   - which direction is preferred
   - what seam or split constraints apply
7. Update docs if the acceptance boundary for a geometry class changes.

## Failure handling

- If the right split strategy is ambiguous, prefer explicit rejection over fake certainty.
- If a requested geometry class belongs to Phase 2 or 3, document that and keep Phase 1 behavior conservative.
- If analysis and geometry failures are mixed together, isolate the analysis decision first before changing booleans.

## File update expectations

Typical files for this skill:

- `src/blender_auto_mold/analysis/mesh_validation.py`
- `src/blender_auto_mold/analysis/pull_direction.py`
- `src/blender_auto_mold/analysis/types.py`
- `docs/geometry_algorithm_blueprint.md`
- `docs/phase1_validation_matrix.md`

## Boundary with nearby skills

- `mold-research` explains why a rule should exist; `parting-analysis` implements that rule on meshes.
- `parting-analysis` decides whether and how the object should separate; `mold-feature-generation` builds geometry from that decision.
- `bmesh-boolean-debug` starts after geometry operations become unstable, not while the split strategy is still undecided.
