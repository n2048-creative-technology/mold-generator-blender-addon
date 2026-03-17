---
name: mold-research
description: Translate physical moldmaking constraints into concrete repo rules, defaults, and phase boundaries. Use when the task is deciding what the add-on should do before writing or revising geometry code.
metadata:
  version: 2
  scope: research-and-planning
  phases:
    - phase-1
    - phase-2
    - phase-3
  primary_paths:
    - AGENTS.md
    - README.md
    - docs/geometry_algorithm_blueprint.md
    - docs/skills_design.md
  outputs:
    - design constraints
    - parameter defaults
    - phase-scoped decisions
  related_skills:
    - parting-analysis
    - mold-feature-generation
    - test-scene-validation
---

# Mold Research

Use this skill when the main task is deciding rules, defaults, tradeoffs, or scope before implementation.

## Use this skill when

- deciding what Phase 1 should support or reject
- turning moldmaking practice into explicit repo constraints
- setting parameter defaults with physical rationale
- documenting tradeoffs such as demolding safety versus piece count
- clarifying whether a requested capability belongs in Phase 1, 2, or 3

Typical requests sound like:

- "what should the default silicone thickness be"
- "is this a Phase 1 feature or later"
- "should we support this mold strategy"
- "what constraints should the algorithm enforce"

## Do not use this skill when

- the main work is implementing Blender UI or registration
- the task is already a concrete pull-direction or seam algorithm
- the task is debugging a broken boolean or invalid mesh
- the user only wants a code patch inside an already accepted design

## Concrete inputs

- the user question or design decision to resolve
- current project phase and any phase constraints
- relevant repo docs, especially `docs/geometry_algorithm_blueprint.md`
- any existing code or defaults that the decision would affect

## Expected outputs

- a clear design decision with rationale
- explicit supported versus unsupported behavior
- proposed defaults, thresholds, or invariants when needed
- doc updates that future sessions can reuse

## Read first

1. `AGENTS.md`
2. `README.md`
3. `docs/geometry_algorithm_blueprint.md`
4. `docs/skills_design.md`

Read source files only if the decision depends on current implementation details.

## Workflow

1. Restate the design question in operational terms, not abstract theory.
2. Identify the current phase and refuse to smuggle in later-phase behavior.
3. Pull the relevant physical concerns into a short decision frame:
   - demolding reliability
   - piece count
   - silicone usage
   - sealing quality
   - printability of rigid parts
4. Compare the requested behavior against current repo scope and architecture.
5. Produce a concrete decision:
   - support now
   - reject for now
   - defer to a later phase
6. Encode the result in durable docs when the decision will matter again.
7. Hand implementation work off to the next skill explicitly:
   - `parting-analysis` for pull or seam decisions
   - `mold-feature-generation` for geometry steps
   - `blender-addon-architecture` or `blender-5-addon-creation` for add-on integration

## Failure handling

- If the repo has no evidence for a strong conclusion, document the uncertainty instead of inventing certainty.
- If a requested feature spans multiple phases, split the recommendation by phase.
- If physical best practice conflicts with current implementation reality, document the tradeoff and keep Phase 1 conservative.

## File update expectations

Typical files for this skill:

- `README.md`
- `AGENTS.md` only for truly repo-wide durable rules
- `docs/geometry_algorithm_blueprint.md`
- `docs/skills_design.md`
- new docs under `docs/` when a reusable design decision needs a home

Avoid implementing Blender code here unless a tiny constant or stub is necessary to keep docs truthful.

## Boundary with nearby skills

- `mold-research` decides the rule; `parting-analysis` turns that rule into mesh-level analysis.
- `mold-research` may recommend a feature family; `mold-feature-generation` builds the geometry.
- `test-scene-validation` uses the resulting support rules to define expected pass or fail cases.
