"""Blender operator entry point for Auto Mold generation."""

from __future__ import annotations

import bpy

from ..analysis import analyze_mesh_object, choose_best_pull_direction, score_pull_directions
from ..analysis.types import MoldGenerationSettings
from ..geometry import generate_two_part_mold


def _settings_from_props(props) -> MoldGenerationSettings:
    return MoldGenerationSettings(
        silicone_thickness_mm=props.silicone_thickness_mm,
        wall_thickness_mm=props.wall_thickness_mm,
        flange_margin_mm=props.flange_margin_mm,
        flange_height_mm=props.flange_height_mm,
        register_radius_mm=props.register_radius_mm,
        register_depth_mm=props.register_depth_mm,
        clamp_hole_radius_mm=props.clamp_hole_radius_mm,
        sprue_radius_mm=props.sprue_radius_mm,
        vent_radius_mm=props.vent_radius_mm,
        proxy_voxel_size_mm=props.proxy_voxel_size_mm,
        cleanup_voxel_size_mm=props.cleanup_voxel_size_mm,
        allow_proxy_remesh=props.allow_proxy_remesh,
        output_collection_name=props.output_collection_name,
    )


class AUTO_MOLD_OT_generate(bpy.types.Operator):
    """Generate a conservative two-part mold from the active mesh."""

    bl_idname = "auto_mold.generate"
    bl_label = "Generate Mold"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.auto_mold
        source_obj = context.active_object

        analysis = analyze_mesh_object(source_obj, props.allow_proxy_remesh)
        if not analysis.can_continue:
            props.last_status = analysis.failure_reason or "Validation failed"
            props.last_warning_summary = "-"
            self.report({"ERROR"}, props.last_status)
            return {"CANCELLED"}

        scores = score_pull_directions(source_obj)
        best_direction = choose_best_pull_direction(scores)

        generation = generate_two_part_mold(
            context,
            source_obj,
            analysis,
            best_direction,
            _settings_from_props(props),
        )

        props.last_status = (
            f"Generated {len(generation.generated_objects)} mold halves in {generation.collection_name}"
        )
        props.last_pull_direction = generation.pull_direction
        props.last_warning_summary = generation.warnings[-1] if generation.warnings else "-"

        for warning in generation.warnings:
            self.report({"WARNING"}, warning)
        self.report({"INFO"}, props.last_status)
        return {"FINISHED"}
