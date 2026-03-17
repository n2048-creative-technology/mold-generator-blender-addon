---
name: test-scene-validation
description: Validate mold-generation behavior on representative object classes and scene cases. Use when the task is checking whether analysis, geometry generation, or printability rules hold across repeatable cases instead of a single example mesh.
metadata:
  version: 2
  scope: validation-and-regression
  phases:
    - phase-1
    - phase-2
    - phase-3
  primary_paths:
    - docs/phase1_validation_matrix.md
    - docs/skills_design.md
    - docs/geometry_algorithm_blueprint.md
    - src/blender_auto_mold/
  outputs:
    - validation matrix
    - representative cases
    - expected pass/fail notes
  related_skills:
    - parting-analysis
    - mold-feature-generation
    - bmesh-boolean-debug
    - prusa-3d-printing-mold-output
---

# Test Scene Validation

Use this skill when the repo needs repeatable evidence, not a one-off anecdote.

## Use this skill when

- creating or maintaining representative validation cases
- checking whether a new workflow holds beyond one mesh
- documenting expected success, rejection, or graceful failure by phase
- building a regression matrix after a geometry or analysis change

Typical requests sound like:

- "validate this across representative objects"
- "what cases should Phase 1 pass"
- "create a validation matrix"
- "turn this bug into a repeatable regression case"

## Do not use this skill when

- the task is still core implementation of the algorithm
- the issue is purely add-on architecture or Blender registration
- there is no behavior yet to validate
- the task is only physical moldmaking research with no repo workflow impact

## Concrete inputs

- the workflow or feature to validate
- current project phase and acceptance rules
- known weak points such as undercuts, holes, thin walls, or oversized parts
- any existing failures that should become regression cases

## Expected outputs

- a representative set of validation cases
- expected pass, fail, or deferred status for each case
- regression notes tied to real failure classes
- updated docs so future sessions reuse the same coverage

## Read first

1. `AGENTS.md`
2. `docs/phase1_validation_matrix.md`
3. `docs/skills_design.md`
4. `docs/geometry_algorithm_blueprint.md`
5. the source files changed by the feature under review

## Workflow

1. Define success for the current phase before picking cases.
2. Choose a small set of representative objects that stress different failure modes.
3. Record for each case whether it should:
   - succeed now
   - fail gracefully now
   - be deferred to a later phase
4. Validate the relevant layers explicitly:
   - mesh validation
   - parting analysis
   - generated geometry
   - printed-output assumptions when relevant
5. Capture regressions and unsupported geometry classes in docs so later sessions can reproduce them.
6. Keep the validation set small and representative rather than exhaustive noise.

## Failure handling

- If there are no reusable scene assets yet, document the validation matrix first.
- If a new case reveals unsupported scope, record the boundary instead of silently broadening support.
- If a failure belongs to one specific subsystem, hand off clearly to the owning skill instead of mixing fixes and validation.

## File update expectations

Typical files for this skill:

- `docs/phase1_validation_matrix.md`
- other validation docs under `docs/`
- future scene or fixture assets if the repo adds them
- notes on expected pass or fail behavior by phase

## Boundary with nearby skills

- `parting-analysis`, `mold-feature-generation`, and `prusa-3d-printing-mold-output` define behavior.
- `bmesh-boolean-debug` stabilizes broken cases before they become regressions.
- This skill evaluates behavior; it does not own the implementation itself.
