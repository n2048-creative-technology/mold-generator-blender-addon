# Skills Design

This document explains how the repo-level Codex customization is structured and how the skills fit together across project phases.

The design follows current Codex customization patterns:

- `AGENTS.md` stays compact and holds durable repo-wide rules.
- skills stay narrowly scoped and reusable.
- skill `name` and `description` carry most of the routing burden.
- `SKILL.md` contains the detailed workflow only after the skill is selected.
- deeper docs should be loaded progressively, not copied into every prompt.

Only `name` and `description` are relied on for Codex discovery. Extra front-matter metadata in this repo is for maintainers and contributors.

## Repo Customization Layers

Use the layers in this order:

1. `AGENTS.md`
   Applies to every task in the repository.
2. `.agents/skills/*/SKILL.md`
   Applies only when the task matches a specialized workflow.
3. `docs/*.md`
   Supplies project details that the chosen skill may read as needed.

## Current Skill Inventory

### `mold-research`

Purpose:
Translate physical moldmaking constraints into explicit repo rules, defaults, tradeoffs, and phase boundaries.

Route here when:

- the task is still deciding what the add-on should do
- a default, limitation, or constraint needs physical rationale
- Phase 1, 2, and 3 ownership is unclear

Do not route here when:

- the main work is coding Blender integration
- the task is debugging a concrete mesh or boolean failure

Primary outputs:

- design decisions in `docs/`
- clarified parameter defaults or constraints
- phase-scoped acceptance and rejection rules

### `blender-addon-architecture`

Purpose:
Keep the add-on modular by enforcing clean boundaries between `analysis/`, `geometry/`, `operators/`, `panels/`, and `utils/`.

Route here when:

- file placement or dependency direction is unclear
- a refactor is needed to keep operators thin
- the add-on package is growing in the wrong shape

Do not route here when:

- the structure is already settled and the task is implementing one feature inside it

Primary outputs:

- module-boundary decisions
- refactor plans or focused structural patches
- docs explaining ownership and dependency direction

### `blender-5-addon-creation`

Purpose:
Implement Blender-facing registration, operators, panels, properties, and collection wiring around existing logic.

Route here when:

- the task is Blender API integration
- a working analysis or geometry path must be exposed in the UI
- registration or property wiring needs to change

Do not route here when:

- the main problem is algorithm design, seam choice, or boolean stability

Primary outputs:

- Blender-facing code in `src/blender_auto_mold/`
- updated UI or operator behavior
- README notes when user workflow changes

### `parting-analysis`

Purpose:
Choose pull direction, identify undercuts, define seam strategy, and decide whether a two-part mold is viable before geometry generation.

Route here when:

- the task is deciding how a mesh should demold
- the work concerns pull scoring, seam candidates, or undercut detection
- Phase 1 support versus graceful rejection needs to be defined for a mesh class

Do not route here when:

- the split strategy is already decided and the job is building the mold parts

Primary outputs:

- analysis structures and scoring logic
- debug visibility for parting decisions
- clear success or graceful-failure rules by phase

### `mold-feature-generation`

Purpose:
Build the actual mold-system geometry once the split strategy and analysis outputs are known.

Route here when:

- the task is silicone shell, rigid shell, flange, key, clamp, vent, or sprue geometry
- object duplication, output collection behavior, or generated part naming needs to change

Do not route here when:

- pull direction or seam choice is still unresolved

Primary outputs:

- geometry code under `src/blender_auto_mold/geometry/`
- supporting helpers in `src/blender_auto_mold/utils/`
- docs when generated-part behavior changes materially

### `bmesh-boolean-debug`

Purpose:
Diagnose and stabilize invalid meshes, BMesh issues, and failing boolean operations in the mold pipeline.

Route here when:

- geometry generation exists but produces broken or unreliable meshes
- booleans fail, invert, explode topology, or create non-manifold results
- the team needs reproducible debug outputs for geometry failures

Do not route here when:

- the work is still deciding the algorithm, not stabilizing it

Primary outputs:

- reproducible failure notes
- narrower geometry preconditions or safer mesh steps
- explicit debug instrumentation and failure reporting

### `prusa-3d-printing-mold-output`

Purpose:
Make generated rigid mold parts manufacturable on Prusa-class printers without losing sealing, alignment, or assembly quality.

Route here when:

- printer fit, orientation, split planning, or assembly-aware printability is the task
- generated rigid parts already exist or their dimensions are known

Do not route here when:

- the job is still core geometry creation or mesh debugging

Primary outputs:

- printer-fit rules or configuration
- print-driven split planning
- docs on printer assumptions and tradeoffs

### `test-scene-validation`

Purpose:
Validate workflow behavior across representative object classes instead of a single hand-picked example.

Route here when:

- the task is building a validation matrix
- a change needs representative pass or fail expectations
- a phase boundary should be captured as a repeatable validation case

Do not route here when:

- the task is still implementing the algorithm itself

Primary outputs:

- validation docs and scene coverage
- expected pass or fail behavior by phase
- regression notes tied to representative object classes

## Boundary Rules

Some overlap is intentional. Use these boundaries to keep routing consistent:

- `mold-research` decides policy and rationale; `parting-analysis` operationalizes that policy on meshes.
- `blender-addon-architecture` decides where logic belongs; `blender-5-addon-creation` writes Blender-facing code inside those boundaries.
- `parting-analysis` decides separation strategy; `mold-feature-generation` builds geometry from that strategy.
- `mold-feature-generation` creates geometry; `bmesh-boolean-debug` stabilizes it when mesh operations fail.
- `prusa-3d-printing-mold-output` begins only after rigid parts exist or their dimensions are concretely specified.
- `test-scene-validation` evaluates behavior after design or implementation decisions exist; it does not replace those decisions.

## Phase Mapping

### Phase 1

Focus:

- conservative two-part mold generation
- watertight manifold meshes only
- explicit failure reporting
- inspectable pull-direction selection
- stable generated-output collection behavior

Primary skills:

- `mold-research`
- `blender-addon-architecture`
- `parting-analysis`
- `mold-feature-generation`
- `blender-5-addon-creation`
- `test-scene-validation`

Support skills:

- `bmesh-boolean-debug`
- `prusa-3d-printing-mold-output` only when printed support-shell constraints materially affect Phase 1 output

### Phase 2

Focus:

- undercut detection
- removable inserts
- broader geometry acceptance beyond simple conservative cases

Primary skills:

- `mold-research`
- `parting-analysis`
- `mold-feature-generation`
- `bmesh-boolean-debug`
- `test-scene-validation`

Secondary skills:

- `blender-addon-architecture`
- `blender-5-addon-creation`
- `prusa-3d-printing-mold-output`

### Phase 3

Focus:

- multi-part mold decomposition
- assembly-aware split strategy across more parts
- manufacturable rigid output planning across complex molds

Primary skills:

- `mold-research`
- `parting-analysis`
- `mold-feature-generation`
- `prusa-3d-printing-mold-output`
- `test-scene-validation`

Secondary skills:

- `bmesh-boolean-debug`
- `blender-addon-architecture`
- `blender-5-addon-creation`

## Recommended Multi-Step Flows

### New algorithm or feature

1. `mold-research` if defaults, constraints, or phase ownership are still unclear.
2. `blender-addon-architecture` if new modules or dependencies are needed.
3. `parting-analysis` to define pull, seam, and rejection rules.
4. `mold-feature-generation` to build or revise geometry.
5. `blender-5-addon-creation` to expose it in Blender.
6. `test-scene-validation` to confirm representative success and failure behavior.
7. `bmesh-boolean-debug` only if geometry operations prove unstable.

### Mesh failure or broken booleans

1. `bmesh-boolean-debug` to reproduce and isolate the failure.
2. `parting-analysis` if the failure reveals a wrong split decision.
3. `mold-feature-generation` if the failure is caused by geometry construction.
4. `test-scene-validation` to prevent regressions on representative cases.

### Printable rigid output review

1. `mold-feature-generation` to confirm the rigid parts being produced.
2. `prusa-3d-printing-mold-output` to check fit, splits, and orientation.
3. `test-scene-validation` to capture printer-driven pass or fail expectations.

## Supporting Docs

- `docs/geometry_algorithm_blueprint.md` describes the intended analysis and generation pipeline.
- `docs/phase1_validation_matrix.md` records the baseline representative cases for Phase 1 validation.

## Maintenance Rules

Update `AGENTS.md` when:

- a rule should apply to every task in the repo
- a repeated mistake crosses multiple skills

Update a skill when:

- the workflow is repeated often enough to deserve its own procedure
- routing is unclear in real use
- inputs, outputs, or failure modes are still vague

Update this document when:

- a skill is added, renamed, or retired
- phase ownership changes
- two skills overlap in practice and need a documented handoff
