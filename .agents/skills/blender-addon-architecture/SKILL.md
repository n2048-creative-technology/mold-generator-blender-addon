---
name: blender-addon-architecture
description: Define or refactor the Blender add-on structure so analysis, geometry, operators, panels, and utilities stay separated and maintainable. Use when the task is mainly about module boundaries, dependency direction, or keeping Blender-facing code thin.
metadata:
  version: 2
  scope: architecture-and-refactor
  phases:
    - phase-1
    - phase-2
    - phase-3
  primary_paths:
    - AGENTS.md
    - docs/skills_design.md
    - src/blender_auto_mold/
  outputs:
    - module-boundary decisions
    - structural refactors
    - dependency rules
  related_skills:
    - blender-5-addon-creation
    - mold-feature-generation
    - parting-analysis
---

# Blender Add-on Architecture

Use this skill when the main problem is structural rather than feature-specific.

## Use this skill when

- deciding where new logic should live
- splitting a growing module into smaller pieces
- checking whether an operator is doing too much work
- defining dependency direction between analysis, geometry, and UI
- making package layout decisions before a large implementation pass

Typical requests sound like:

- "where should this logic live"
- "split this operator"
- "clean up the package structure"
- "keep the add-on maintainable as features grow"

## Do not use this skill when

- the structure is already clear and the task is writing one feature
- the task is mainly Blender registration, panel, or property wiring
- the main issue is pull-direction logic or mesh-generation details
- the task is debugging a geometry failure instead of module ownership

## Concrete inputs

- the feature or refactor being considered
- current files under `src/blender_auto_mold/`
- existing phase scope and repo rules from `AGENTS.md`
- any pain points such as duplicated logic or oversized operators

## Expected outputs

- a clear ownership decision for each responsibility
- smaller, more stable module boundaries
- reduced coupling between Blender API code and reusable logic
- doc updates when architecture rules become important for future sessions

## Read first

1. `AGENTS.md`
2. `README.md`
3. `docs/skills_design.md`
4. relevant files under `src/blender_auto_mold/`

## Workflow

1. Inspect the current package layout before proposing new folders.
2. Identify the responsibility being added or moved.
3. Place it according to repo ownership rules:
   - `analysis/` for scoring, validation, seam, and undercut logic
   - `geometry/` for generated meshes and mold-part construction
   - `operators/` for orchestration of user actions
   - `panels/` and `properties.py` for UI exposure
   - `utils/` for narrow reusable helpers that are not mold-domain logic
4. Keep dependency direction simple:
   - UI and operators may depend on analysis, geometry, and utils
   - geometry may depend on analysis outputs and utils
   - analysis should not depend on panels or operators
5. Prefer extracting reusable functions before adding new classes.
6. Keep phase-limited features isolated so later-phase work does not destabilize Phase 1.
7. Update docs when the new structure changes how contributors should extend the repo.

## Failure handling

- If multiple layouts could work, choose the one that keeps operators thinnest and future geometry reusable.
- If a refactor would touch unrelated code for little gain, keep the smaller patch and document the boundary instead.
- If the repo lacks a needed module, add the minimum structure required rather than speculative abstraction.

## File update expectations

Typical files for this skill:

- `src/blender_auto_mold/__init__.py`
- `src/blender_auto_mold/analysis/*`
- `src/blender_auto_mold/geometry/*`
- `src/blender_auto_mold/operators/*`
- `src/blender_auto_mold/panels/*`
- `src/blender_auto_mold/utils/*`
- `docs/skills_design.md`

## Boundary with nearby skills

- `blender-addon-architecture` decides the structure; `blender-5-addon-creation` writes Blender-facing code inside that structure.
- `parting-analysis` and `mold-feature-generation` own the domain logic that architecture work is organizing.
- Use this skill before a large feature when file placement is unclear; skip it when the implementation slot is already obvious.
