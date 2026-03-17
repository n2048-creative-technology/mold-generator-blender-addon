---
name: blender-5-addon-creation
description: Create or refactor Blender-facing add-on code for this project, including registration, operators, panels, properties, and collection output wiring. Use when the task is primarily about Blender API integration or exposing existing mold logic inside the add-on.
metadata:
  version: 2
  scope: blender-api-integration
  phases:
    - phase-1
    - phase-2
    - phase-3
  primary_paths:
    - src/blender_auto_mold/__init__.py
    - src/blender_auto_mold/operators/
    - src/blender_auto_mold/panels/
    - src/blender_auto_mold/properties.py
    - src/blender_auto_mold/utils/collections.py
  outputs:
    - Blender operators
    - panels and properties
    - registration flow
  related_skills:
    - blender-addon-architecture
    - parting-analysis
    - mold-feature-generation
---

# Blender 5 Add-on Creation

Use this skill when the main task is writing or revising Blender-facing code.

## Use this skill when

- adding or refactoring operators
- exposing an analysis or geometry workflow in the UI
- adding panels, scene properties, or registration wiring
- managing generated-object collections and active-object flow
- making the add-on installable and predictable inside Blender

Typical requests sound like:

- "add a Blender operator"
- "wire this into the Auto Mold panel"
- "expose this setting in the UI"
- "clean up add-on registration"

## Do not use this skill when

- the main task is choosing pull directions or seam logic
- the task is creating mold geometry independent of Blender UI glue
- the work is stabilizing broken booleans or invalid meshes
- the main issue is long-term module ownership rather than Blender code itself

## Concrete inputs

- the user-facing workflow to expose
- existing reusable analysis or geometry functions
- current add-on files under `src/blender_auto_mold/`
- any new parameters that need Blender properties

## Expected outputs

- thin operators that orchestrate reusable logic
- honest UI controls for supported phase behavior
- predictable registration and unregistration flow
- generated outputs routed into named collections
- README updates when installation or usage changes materially

## Read first

1. `AGENTS.md`
2. `README.md`
3. `docs/skills_design.md`
4. current Blender-facing files under `src/blender_auto_mold/`

## Workflow

1. Confirm the relevant logic already exists or define a small, explicit integration boundary for it.
2. Keep Blender state handling at the edges:
   - selection changes
   - active object changes
   - mode switching
   - scene property access
3. Use scene properties with millimeter-based names such as `silicone_thickness_mm`.
4. Keep operators small:
   - validate context
   - gather settings
   - call reusable analysis or geometry code
   - report success or failure clearly
5. Route generated objects to a named output collection instead of mutating the source object.
6. Preserve the original source object and return Blender to a sensible state after execution.
7. If a feature is partial, expose the current limitation honestly rather than implying support that does not exist.
8. Update README notes if installation, panel behavior, or user workflow changed.

## Failure handling

- If the needed geometry or analysis logic does not exist yet, define the integration seam clearly rather than embedding large placeholder logic in the operator.
- If Blender API behavior is uncertain, prefer the simplest pattern already used in the repo.
- If a UI control would advertise unsupported behavior, leave it out and document the limitation instead.

## File update expectations

Typical files for this skill:

- `src/blender_auto_mold/__init__.py`
- `src/blender_auto_mold/operators/*.py`
- `src/blender_auto_mold/panels/*.py`
- `src/blender_auto_mold/properties.py`
- `src/blender_auto_mold/utils/collections.py`
- `src/blender_auto_mold/utils/object_ops.py`
- `README.md`

## Boundary with nearby skills

- `blender-addon-architecture` decides structure before large refactors.
- `parting-analysis` supplies pull or seam logic for operators to call.
- `mold-feature-generation` owns geometry creation; this skill only exposes it in Blender.
