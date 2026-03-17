"""Conservative phase-1 rigid mold generation."""

from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Vector

from ..analysis.types import MeshAnalysisResult, MoldGenerationResult, MoldGenerationSettings, PullDirectionScore
from ..utils.collections import ensure_collection, move_object_to_collection
from ..utils.object_ops import apply_modifier, delete_objects, duplicate_object, ensure_object_mode, set_active_object
from ..utils.units import mm_to_scene


def _axis_index(direction: Vector) -> int:
    absolute = [abs(component) for component in direction]
    return absolute.index(max(absolute))


def _axis_rotation(axis_index: int) -> tuple[float, float, float]:
    if axis_index == 0:
        return (0.0, math.pi / 2.0, 0.0)
    if axis_index == 1:
        return (math.pi / 2.0, 0.0, 0.0)
    return (0.0, 0.0, 0.0)


def _create_box(context, name: str, bbox_min: Vector, bbox_max: Vector, collection):
    center = (bbox_min + bbox_max) * 0.5
    size = bbox_max - bbox_min
    bpy.ops.mesh.primitive_cube_add(location=center)
    obj = context.active_object
    obj.name = name
    obj.scale = size * 0.5
    move_object_to_collection(obj, collection)
    return obj


def _create_uv_sphere(context, name: str, location: Vector, radius: float, collection):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    obj = context.active_object
    obj.name = name
    move_object_to_collection(obj, collection)
    return obj


def _create_cylinder(
    context,
    name: str,
    location: Vector,
    radius: float,
    depth: float,
    axis_index: int,
    collection,
):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=depth,
        location=location,
        rotation=_axis_rotation(axis_index),
    )
    obj = context.active_object
    obj.name = name
    move_object_to_collection(obj, collection)
    return obj


def _apply_boolean(context, target, operand, operation: str, suffix: str) -> None:
    modifier = target.modifiers.new(name=f"AutoMold{suffix}", type="BOOLEAN")
    modifier.object = operand
    modifier.operation = operation
    modifier.solver = "EXACT"
    apply_modifier(context, target, modifier.name)


def _ensure_manifold_or_cleanup(context, obj, cleanup_voxel_size: float) -> bool:
    bm = bmesh.new()
    try:
        bm.from_mesh(obj.data)
        bm.normal_update()
        is_manifold = all(edge.is_manifold for edge in bm.edges)
    finally:
        bm.free()

    if is_manifold or cleanup_voxel_size <= 0.0:
        return is_manifold

    modifier = obj.modifiers.new(name="AutoMoldCleanup", type="REMESH")
    modifier.mode = "VOXEL"
    modifier.voxel_size = cleanup_voxel_size
    modifier.adaptivity = 0.0
    apply_modifier(context, obj, modifier.name)
    return True


def _build_proxy_object(context, source_obj, settings: MoldGenerationSettings, collection):
    proxy = duplicate_object(context, source_obj, f"{source_obj.name}_proxy_tmp", collection=collection)
    modifier = proxy.modifiers.new(name="AutoMoldProxyRemesh", type="REMESH")
    modifier.mode = "VOXEL"
    modifier.voxel_size = mm_to_scene(settings.proxy_voxel_size_mm, context.scene)
    modifier.adaptivity = 0.0
    apply_modifier(context, proxy, modifier.name)
    return proxy


def _build_cavity_object(context, working_obj, settings: MoldGenerationSettings, collection):
    cavity = duplicate_object(context, working_obj, f"{working_obj.name}_cavity_tmp", collection=collection)
    thickness = mm_to_scene(settings.silicone_thickness_mm, context.scene)
    if thickness > 0.0:
        modifier = cavity.modifiers.new(name="AutoMoldSiliconeOffset", type="SOLIDIFY")
        modifier.thickness = thickness
        modifier.offset = 1.0
        modifier.use_even_offset = True
        modifier.use_quality_normals = True
        apply_modifier(context, cavity, modifier.name)
    return cavity


def _half_bounds(
    analysis: MeshAnalysisResult,
    axis_index: int,
    scene,
    settings: MoldGenerationSettings,
) -> tuple[tuple[Vector, Vector], tuple[Vector, Vector]]:
    bbox_min = analysis.bbox_min.copy()
    bbox_max = analysis.bbox_max.copy()
    center = (bbox_min + bbox_max) * 0.5
    outer_side = mm_to_scene(settings.wall_thickness_mm + settings.flange_margin_mm, scene)
    outer_axis = mm_to_scene(settings.wall_thickness_mm, scene)
    seam_overlap = mm_to_scene(settings.flange_height_mm, scene)

    positive_min = bbox_min.copy()
    positive_max = bbox_max.copy()
    negative_min = bbox_min.copy()
    negative_max = bbox_max.copy()

    for index in range(3):
        if index == axis_index:
            positive_min[index] = center[index] - (seam_overlap * 0.5)
            positive_max[index] = bbox_max[index] + outer_axis
            negative_min[index] = bbox_min[index] - outer_axis
            negative_max[index] = center[index] + (seam_overlap * 0.5)
        else:
            positive_min[index] = bbox_min[index] - outer_side
            positive_max[index] = bbox_max[index] + outer_side
            negative_min[index] = bbox_min[index] - outer_side
            negative_max[index] = bbox_max[index] + outer_side

    return (positive_min, positive_max), (negative_min, negative_max)


def _register_positions(
    analysis: MeshAnalysisResult,
    axis_index: int,
    scene,
    settings: MoldGenerationSettings,
) -> list[Vector]:
    center = (analysis.bbox_min + analysis.bbox_max) * 0.5
    extents = analysis.bbox_size * 0.5
    margin = mm_to_scene(settings.flange_margin_mm * 0.6, scene)

    other_indices = [index for index in range(3) if index != axis_index]
    offsets = []
    for sign_a in (-1.0, 1.0):
        for sign_b in (-1.0, 1.0):
            location = center.copy()
            location[other_indices[0]] += sign_a * (extents[other_indices[0]] + margin)
            location[other_indices[1]] += sign_b * (extents[other_indices[1]] + margin)
            offsets.append(location)
    return offsets


def _seam_window_bounds(
    analysis: MeshAnalysisResult,
    axis_index: int,
    scene,
    settings: MoldGenerationSettings,
) -> tuple[Vector, Vector]:
    center = (analysis.bbox_min + analysis.bbox_max) * 0.5
    bbox_min = analysis.bbox_min.copy()
    bbox_max = analysis.bbox_max.copy()
    silicone_margin = mm_to_scene(settings.silicone_thickness_mm * 1.1, scene)
    opening_depth = mm_to_scene(
        max(settings.flange_height_mm * 1.5, settings.wall_thickness_mm),
        scene,
    )

    cutter_min = bbox_min.copy()
    cutter_max = bbox_max.copy()

    for index in range(3):
        if index == axis_index:
            cutter_min[index] = center[index] - opening_depth
            cutter_max[index] = center[index] + opening_depth
        else:
            cutter_min[index] = bbox_min[index] - silicone_margin
            cutter_max[index] = bbox_max[index] + silicone_margin

    return cutter_min, cutter_max


def _open_parting_window(context, halves, analysis, axis_index, settings, collection, warnings):
    cutter_min, cutter_max = _seam_window_bounds(analysis, axis_index, context.scene, settings)
    cutter = _create_box(
        context,
        "seam_window_tmp",
        cutter_min,
        cutter_max,
        collection,
    )
    try:
        for half in halves:
            _apply_boolean(context, half, cutter, "DIFFERENCE", "SeamWindow")
    finally:
        delete_objects(context, [cutter])

    warnings.append("Opened the parting window so the cavity is exposed at the seam.")


def _add_registers(context, top_half, bottom_half, analysis, axis_index, settings, collection, warnings):
    radius = mm_to_scene(settings.register_radius_mm, context.scene)
    depth = mm_to_scene(settings.register_depth_mm, context.scene)
    offset = Vector((0.0, 0.0, 0.0))
    offset[axis_index] = depth * 0.35
    temp_objects = []

    for index, position in enumerate(_register_positions(analysis, axis_index, context.scene, settings)):
        peg = _create_uv_sphere(context, f"register_peg_tmp_{index}", position + offset, radius, collection)
        socket = _create_uv_sphere(context, f"register_socket_tmp_{index}", position + offset, radius * 1.03, collection)
        temp_objects.extend([peg, socket])
        _apply_boolean(context, top_half, peg, "UNION", f"RegisterPeg{index}")
        _apply_boolean(context, bottom_half, socket, "DIFFERENCE", f"RegisterSocket{index}")

    delete_objects(context, temp_objects)
    warnings.append("Added four seam alignment registers.")


def _add_clamp_holes(context, halves, analysis, axis_index, settings, collection, warnings):
    radius = mm_to_scene(settings.clamp_hole_radius_mm, context.scene)
    positions = _register_positions(analysis, axis_index, context.scene, settings)
    depth = max(analysis.bbox_size) + (mm_to_scene(settings.wall_thickness_mm, context.scene) * 4.0)
    temp_objects = []

    for index, position in enumerate(positions):
        cutter = _create_cylinder(
            context,
            f"clamp_hole_tmp_{index}",
            position,
            radius,
            depth,
            axis_index,
            collection,
        )
        temp_objects.append(cutter)
        for half in halves:
            _apply_boolean(context, half, cutter, "DIFFERENCE", f"ClampHole{index}")

    delete_objects(context, temp_objects)
    warnings.append("Added clamp-through holes on the flange corners.")


def _add_sprue_and_vents(context, top_half, analysis, axis_index, settings, collection, warnings):
    center = (analysis.bbox_min + analysis.bbox_max) * 0.5
    depth = max(analysis.bbox_size) + (mm_to_scene(settings.wall_thickness_mm, context.scene) * 3.0)
    temp_objects = []

    sprue = _create_cylinder(
        context,
        "sprue_tmp",
        center,
        mm_to_scene(settings.sprue_radius_mm, context.scene),
        depth,
        axis_index,
        collection,
    )
    temp_objects.append(sprue)
    _apply_boolean(context, top_half, sprue, "DIFFERENCE", "Sprue")

    vent_positions = _register_positions(analysis, axis_index, context.scene, settings)[:2]
    for index, position in enumerate(vent_positions):
        vent = _create_cylinder(
            context,
            f"vent_tmp_{index}",
            position,
            mm_to_scene(settings.vent_radius_mm, context.scene),
            depth,
            axis_index,
            collection,
        )
        temp_objects.append(vent)
        _apply_boolean(context, top_half, vent, "DIFFERENCE", f"Vent{index}")

    delete_objects(context, temp_objects)
    warnings.append("Cut one central sprue and two simple vent channels in the positive half.")


def generate_two_part_mold(
    context,
    source_obj,
    analysis: MeshAnalysisResult,
    pull_direction: PullDirectionScore,
    settings: MoldGenerationSettings,
) -> MoldGenerationResult:
    """Generate a conservative two-part rigid mold from the selected mesh."""
    ensure_object_mode(context)
    output_collection = ensure_collection(settings.output_collection_name, context.scene.collection)
    temp_collection = ensure_collection(f"{settings.output_collection_name}_TMP", output_collection)

    warnings = list(analysis.warnings)
    temp_objects = []
    working_source = None

    if analysis.needs_proxy:
        working_source = _build_proxy_object(context, source_obj, settings, temp_collection)
        warnings.append("Used a temporary voxel remesh proxy for booleans and cavity bounds.")
    else:
        working_source = duplicate_object(
            context,
            source_obj,
            f"{source_obj.name}_working_tmp",
            collection=temp_collection,
        )
    temp_objects.append(working_source)

    cavity = _build_cavity_object(context, working_source, settings, temp_collection)
    temp_objects.append(cavity)

    axis_index = _axis_index(pull_direction.vector)
    positive_bounds, negative_bounds = _half_bounds(analysis, axis_index, context.scene, settings)

    top_half = _create_box(
        context,
        f"{source_obj.name}_mold_positive",
        positive_bounds[0],
        positive_bounds[1],
        output_collection,
    )
    bottom_half = _create_box(
        context,
        f"{source_obj.name}_mold_negative",
        negative_bounds[0],
        negative_bounds[1],
        output_collection,
    )

    _apply_boolean(context, top_half, cavity, "DIFFERENCE", "TopCavity")
    _apply_boolean(context, bottom_half, cavity, "DIFFERENCE", "BottomCavity")
    _open_parting_window(
        context,
        (top_half, bottom_half),
        analysis,
        axis_index,
        settings,
        temp_collection,
        warnings,
    )

    _add_registers(context, top_half, bottom_half, analysis, axis_index, settings, temp_collection, warnings)
    _add_clamp_holes(context, (top_half, bottom_half), analysis, axis_index, settings, temp_collection, warnings)
    _add_sprue_and_vents(context, top_half, analysis, axis_index, settings, temp_collection, warnings)

    cleanup_voxel = mm_to_scene(settings.cleanup_voxel_size_mm, context.scene)
    if not _ensure_manifold_or_cleanup(context, top_half, cleanup_voxel):
        warnings.append("Positive half remained non-manifold after booleans.")
    if not _ensure_manifold_or_cleanup(context, bottom_half, cleanup_voxel):
        warnings.append("Negative half remained non-manifold after booleans.")

    delete_objects(context, temp_objects)
    set_active_object(context, top_half)

    return MoldGenerationResult(
        collection_name=output_collection.name,
        generated_objects=[top_half.name, bottom_half.name],
        pull_direction=pull_direction.axis_name,
        used_proxy=analysis.needs_proxy,
        warnings=warnings,
    )
