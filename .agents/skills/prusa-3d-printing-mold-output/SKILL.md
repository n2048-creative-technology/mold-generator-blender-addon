---
name: prusa-3d-printing-mold-output
description: Plan generated rigid mold parts for practical printing on Prusa-class printers, including printer-fit checks, split planning, orientation, support reduction, and assembly-aware clearances. Use when rigid mold parts must be manufacturable after their geometry is defined.
metadata:
  version: 2
  scope: printability-and-manufacture
  phases:
    - phase-1
    - phase-2
    - phase-3
  primary_paths:
    - README.md
    - docs/skills_design.md
    - docs/geometry_algorithm_blueprint.md
    - src/blender_auto_mold/geometry/
  outputs:
    - printer-fit rules
    - print-driven split decisions
    - manufacturability notes
  related_skills:
    - mold-feature-generation
    - test-scene-validation
---

# Prusa 3D Printing Mold Output

Use this skill when the task is about whether generated rigid parts can actually be printed and assembled.

## Use this skill when

- checking whether rigid support-shell parts fit a target printer profile
- planning the fewest extra splits needed for oversized rigid parts
- choosing orientations that protect sealing and mating faces
- documenting printer assumptions that affect geometry decisions

Typical requests sound like:

- "will this mold fit a Prusa"
- "split this shell for printing"
- "choose a safer print orientation"
- "add printer-profile assumptions"

## Do not use this skill when

- the task is still generating the mold geometry itself
- the main issue is a broken boolean or invalid mesh
- the work is still deciding the parting strategy rather than printability
- the part has no rigid printed output requirement yet

## Concrete inputs

- generated rigid mold parts or their expected bounding boxes
- target printer profile if known
- sealing, alignment, and clamp features that must be protected
- current project phase and piece-count constraints

## Expected outputs

- a printer-fit assessment
- the minimum additional split strategy, if needed
- practical orientation or support recommendations
- updated docs or config when printer assumptions become durable repo knowledge

## Default printer profiles

Prefer configurable profiles instead of one hard-coded machine.

- `PRUSA_MK4S`: 250 x 210 x 220 mm
- `PRUSA_CORE_ONE`: 250 x 220 x 270 mm
- `PRUSA_CORE_ONE_L`: 300 x 300 x 330 mm

## Read first

1. `AGENTS.md`
2. `README.md`
3. `docs/skills_design.md`
4. relevant rigid-output geometry files under `src/blender_auto_mold/geometry/`

## Workflow

1. Confirm which outputs are intended to be rigid printed parts.
2. Compare each part envelope against the active printer profile.
3. If a part does not fit, prefer the fewest extra splits that preserve:
   - sealing quality
   - alignment accuracy
   - clamp usability
4. Choose orientations that reduce support damage on cavity-facing and mating surfaces.
5. Keep printability changes aligned with the repo goal of minimal part count.
6. Document printer assumptions that future sessions should reuse.

## Failure handling

- If no safe split exists, report that clearly rather than forcing a damaging split.
- If printability conflicts with sealing or alignment quality, document the tradeoff explicitly.
- If the printer profile is unknown, use a documented default and say which one was assumed.

## File update expectations

Typical files for this skill:

- `README.md`
- `src/blender_auto_mold/geometry/*.py`
- printer-profile configuration if later added
- docs covering manufacturability assumptions or printer-driven limits

## Boundary with nearby skills

- `mold-feature-generation` creates the rigid parts first.
- `test-scene-validation` checks whether printability assumptions hold across representative cases.
- This skill should not absorb general geometry-generation or boolean-debug work.
