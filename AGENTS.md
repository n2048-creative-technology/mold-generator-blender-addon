# AGENTS.md

This repository defines Codex guidance for the Blender Auto Mold Generator project.

Keep this file compact. Put durable repo rules here. Put specialized workflows in `.agents/skills/`. Put cross-skill routing in `docs/skills_design.md`.

## Project Goal

Generate mold systems from mesh objects with:

- minimal mold-piece count
- reliable demolding
- reduced silicone use
- robust alignment features
- printable rigid parts

## Read First

- Treat repository files as the source of truth.
- Read `README.md` before changing repo workflow or contributor guidance.
- Read `docs/skills_design.md` before adding, merging, or renaming skills.
- Read `docs/geometry_algorithm_blueprint.md` before changing mold-analysis or geometry workflows.

## Working Style

- Keep modules small and composable under `analysis/`, `geometry/`, `operators/`, `panels/`, and `utils/`.
- Treat operators as orchestration layers; keep reusable logic out of Blender UI code.
- Prefer explicit geometry steps over compact cleverness.
- Add docstrings to modules and clear names to public functions.
- Update nearby docs when a workflow, boundary, or limitation materially changes.

## Current Architecture

- `src/blender_auto_mold/analysis/` owns mesh validation, pull-direction scoring, and future seam or undercut analysis.
- `src/blender_auto_mold/geometry/` owns generated mold geometry and part construction.
- `src/blender_auto_mold/operators/` owns Blender operator entry points only.
- `src/blender_auto_mold/panels/` and `src/blender_auto_mold/properties.py` own Blender UI exposure.
- `src/blender_auto_mold/utils/` owns collection, object, and unit helpers.

## Geometry Invariants

- Never modify the original source mesh in place.
- Always follow `duplicate -> operate -> output`.
- Place generated objects in a named collection.
- Use millimeters for mold parameters and encode units in names such as `silicone_thickness_mm`.
- Protect sealing surfaces, alignment features, and demolding paths from incidental geometry changes.

## Phase Discipline

- Phase 1: two-part mold generation for watertight manifold meshes.
- Phase 2: undercut detection and removable inserts.
- Phase 3: multi-part mold decomposition.
- Do not let Phase 2 or Phase 3 ideas destabilize Phase 1 behavior unless the user explicitly asks for that tradeoff.
- Prefer explicit graceful failure over silently widening scope.

## Error And Debug Expectations

- Invalid meshes must not crash the add-on.
- Report the reason for failure when practical and abort cleanly when geometry is unsafe.
- Prefer explicit debug outputs over silent heuristics when geometry decisions are hard to inspect.
- Visualization helpers are expected for pull direction, undercuts, seam candidates, and vent locations as those systems mature.

## Codex Customization

- Use skills for repeatable repo-specific workflows; keep `AGENTS.md` durable and small.
- Keep skill scopes narrow enough that `name` and `description` alone make routing reliable.
- When overlap is unavoidable, document the boundary in both `SKILL.md` files and `docs/skills_design.md`.
- If repeated confusion appears during development, update the closest applicable guidance file so the correction persists.
