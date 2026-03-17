"""Sidebar UI for the Auto Mold operator."""

from __future__ import annotations

import bpy


class VIEW3D_PT_auto_mold(bpy.types.Panel):
    """Auto Mold controls."""

    bl_label = "Auto Mold"
    bl_idname = "VIEW3D_PT_auto_mold"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Auto Mold"

    def draw(self, context):
        layout = self.layout
        props = context.scene.auto_mold

        layout.label(text="Phase 1 Conservative Two-Part Mold")

        sizing = layout.box()
        sizing.label(text="Sizing")
        sizing.prop(props, "silicone_thickness_mm")
        sizing.prop(props, "wall_thickness_mm")
        sizing.prop(props, "flange_margin_mm")
        sizing.prop(props, "flange_height_mm")

        features = layout.box()
        features.label(text="Features")
        features.prop(props, "register_radius_mm")
        features.prop(props, "register_depth_mm")
        features.prop(props, "clamp_hole_radius_mm")
        features.prop(props, "sprue_radius_mm")
        features.prop(props, "vent_radius_mm")

        recovery = layout.box()
        recovery.label(text="Recovery")
        recovery.prop(props, "allow_proxy_remesh")
        recovery.prop(props, "proxy_voxel_size_mm")
        recovery.prop(props, "cleanup_voxel_size_mm")
        recovery.prop(props, "output_collection_name")

        layout.operator("auto_mold.generate", icon="MOD_BOOLEAN")

        status = layout.box()
        status.label(text="Last Run")
        status.label(text=f"Status: {props.last_status}")
        status.label(text=f"Pull: {props.last_pull_direction}")
        status.label(text=f"Note: {props.last_warning_summary}")
