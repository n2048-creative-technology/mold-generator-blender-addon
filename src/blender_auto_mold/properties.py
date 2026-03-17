"""Scene properties exposed in the Auto Mold panel."""

from __future__ import annotations

import bpy


class AutoMoldProperties(bpy.types.PropertyGroup):
    """User-configurable Phase 1 mold settings."""

    silicone_thickness_mm: bpy.props.FloatProperty(
        name="Silicone Thickness",
        description="Clearance shell generated around the source for the rigid support mold",
        default=6.0,
        min=0.5,
        soft_max=25.0,
        subtype="DISTANCE",
    )
    wall_thickness_mm: bpy.props.FloatProperty(
        name="Wall Thickness",
        description="Rigid mold wall thickness outside the cavity",
        default=8.0,
        min=2.0,
        soft_max=40.0,
        subtype="DISTANCE",
    )
    flange_margin_mm: bpy.props.FloatProperty(
        name="Flange Margin",
        description="Extra width around the seam for flanges and hardware",
        default=12.0,
        min=2.0,
        soft_max=40.0,
        subtype="DISTANCE",
    )
    flange_height_mm: bpy.props.FloatProperty(
        name="Flange Height",
        description="Overlap around the parting plane",
        default=6.0,
        min=1.0,
        soft_max=20.0,
        subtype="DISTANCE",
    )
    register_radius_mm: bpy.props.FloatProperty(
        name="Register Radius",
        description="Alignment register radius",
        default=3.0,
        min=1.0,
        soft_max=12.0,
        subtype="DISTANCE",
    )
    register_depth_mm: bpy.props.FloatProperty(
        name="Register Depth",
        description="Alignment register embed depth",
        default=3.0,
        min=1.0,
        soft_max=12.0,
        subtype="DISTANCE",
    )
    clamp_hole_radius_mm: bpy.props.FloatProperty(
        name="Clamp Radius",
        description="Radius for clamp-through holes on the flange",
        default=2.2,
        min=0.5,
        soft_max=10.0,
        subtype="DISTANCE",
    )
    sprue_radius_mm: bpy.props.FloatProperty(
        name="Sprue Radius",
        description="Central fill channel radius",
        default=3.0,
        min=0.5,
        soft_max=12.0,
        subtype="DISTANCE",
    )
    vent_radius_mm: bpy.props.FloatProperty(
        name="Vent Radius",
        description="Vent channel radius",
        default=1.5,
        min=0.3,
        soft_max=8.0,
        subtype="DISTANCE",
    )
    proxy_voxel_size_mm: bpy.props.FloatProperty(
        name="Proxy Voxel Size",
        description="Voxel size for the temporary non-manifold recovery proxy",
        default=1.5,
        min=0.2,
        soft_max=10.0,
        subtype="DISTANCE",
    )
    cleanup_voxel_size_mm: bpy.props.FloatProperty(
        name="Cleanup Voxel Size",
        description="Optional voxel cleanup applied to generated halves if booleans leave them non-manifold",
        default=0.8,
        min=0.0,
        soft_max=6.0,
        subtype="DISTANCE",
    )
    allow_proxy_remesh: bpy.props.BoolProperty(
        name="Allow Proxy For Non-Manifold",
        description="Use a temporary voxel remesh proxy when the source is not watertight",
        default=True,
    )
    output_collection_name: bpy.props.StringProperty(
        name="Output Collection",
        description="Collection receiving generated mold parts",
        default="Mold_Output",
    )
    last_status: bpy.props.StringProperty(
        name="Status",
        description="Last operator result",
        default="Idle",
    )
    last_pull_direction: bpy.props.StringProperty(
        name="Pull Direction",
        description="Last chosen pull direction",
        default="-",
    )
    last_warning_summary: bpy.props.StringProperty(
        name="Warnings",
        description="Summary of the last generation warnings",
        default="-",
    )
