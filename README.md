# mold-generator-blender-addon

Blender add-on project for generating casting mold systems from mesh objects.

## Objective

The project is being developed in phases:

- Phase 1: two-part mold generator for clean manifold meshes
- Phase 2: undercut detection and removable inserts
- Phase 3: multi-part mold decomposition

The geometry pipeline and current design intent are described in `docs/geometry_algorithm_blueprint.md`.

## Codex Customization

This repo includes checked-in Codex guidance so repeated development sessions stay consistent.

- Repo-wide rules live in `AGENTS.md`.
- Repo skills live under `.agents/skills/`.
- Cross-skill routing and phase usage live in `docs/skills_design.md`.

Codex customization in this repo follows current Codex patterns:

- keep `AGENTS.md` small and durable
- make skill `name` and `description` explicit enough for discovery
- keep detailed workflows in `SKILL.md`
- load deeper references only when the matching skill needs them

## Extending The Skill Layer

When adding or revising Codex guidance in this repo:

1. Put stable repo rules in `AGENTS.md` only if they should apply to every task.
2. Put repeatable specialized workflows in a narrowly scoped skill under `.agents/skills/`.
3. Keep `SKILL.md` front matter explicit enough that Codex can choose the correct skill from the description alone.
4. Update `docs/skills_design.md` when a new skill changes routing, ownership, or overlap.
5. Add supporting docs under `docs/` when a skill needs reusable project context.

## Printer Profiles And Mold Output

Rigid mold parts should be planned against configurable printer profiles rather than a single hard-coded machine.

Default design guidance currently assumes these profiles:

- `PRUSA_MK4S`: 250 x 210 x 220 mm
- `PRUSA_CORE_ONE`: 250 x 220 x 270 mm
- `PRUSA_CORE_ONE_L`: 300 x 300 x 330 mm

These profiles affect:

- whether rigid support-shell parts fit without splitting
- how many printed parts are required to stay within build volume
- where print-driven splits should be placed to protect sealing faces and alignment features
- which orientation and support tradeoffs are acceptable for generated parts

## Current State

This repository currently contains:

- the first Phase 1 add-on scaffold in `src/blender_auto_mold/`
- repo-specific Codex guidance for repeated development sessions
- planning docs for geometry, validation, and skill routing

Current Phase 1 add-on behavior:

- installs as the `blender_auto_mold` package
- adds an `Auto Mold` panel in the 3D View sidebar
- validates the active mesh object
- scores world-axis pull directions
- creates two conservative rigid mold halves in `Mold_Output`
- adds seam flanges, alignment registers, clamp holes, and basic sprue and vent channels
- can accept non-manifold meshes by generating a temporary voxel-remeshed proxy for analysis and booleans

Current limitations:

- non-manifold support is conservative and proxy-based, so output follows a watertight approximation rather than the raw open mesh exactly
- pull-direction scoring still uses the original object, while boolean cutting and bounds use the proxy when required
- the rigid mold shape is still based on a conservative block-style outer envelope rather than an optimized shell mold
- sprue, vent, clamp, and register placement are simple defaults rather than feature-aware placement
- generated parts now use exact booleans first and a conservative voxel cleanup pass if needed, which improves watertight output but can slightly soften sharp detail
- this path is intended to make common meshes such as Suzanne usable without claiming robust support for every open mesh failure mode

To install it in Blender, package the contents of `src/` so the add-on archive contains the `blender_auto_mold/` folder at the archive root.

## Usage

1. Enable the add-on in Blender.
2. Select a mesh object.
3. Open `View3D > Sidebar > Auto Mold`.
4. Adjust the phase-1 sizing and recovery settings.
5. Run `Generate Mold`.

Generated halves are written to `Mold_Output`. The source object is preserved. When proxy recovery is needed, the operator reports that the booleans used a temporary voxel-remeshed proxy.

## Contributor Notes

- Start with `AGENTS.md` for repo rules.
- Use `docs/skills_design.md` to understand which skill should handle a task.
- Keep new guidance specific, phase-aware, and tied to actual repo files.
- Do not broaden Phase 1 scope silently when documenting or implementing new workflows.
