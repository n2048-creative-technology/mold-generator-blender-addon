"""Validation helpers for deciding whether phase-1 generation can proceed."""

from __future__ import annotations

import bmesh
from mathutils import Vector

from .types import MeshAnalysisResult


def _empty_analysis(reason: str) -> MeshAnalysisResult:
    zero = Vector((0.0, 0.0, 0.0))
    return MeshAnalysisResult(
        is_mesh=False,
        has_faces=False,
        is_manifold=False,
        has_consistent_normals=False,
        has_self_intersections=False,
        bbox_min=zero.copy(),
        bbox_max=zero.copy(),
        bbox_size=zero.copy(),
        volume_estimate=0.0,
        face_count=0,
        vertex_count=0,
        can_continue=False,
        failure_reason=reason,
    )


def _world_bbox(obj) -> tuple[Vector, Vector, Vector]:
    corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    bbox_min = Vector(
        (
            min(corner.x for corner in corners),
            min(corner.y for corner in corners),
            min(corner.z for corner in corners),
        )
    )
    bbox_max = Vector(
        (
            max(corner.x for corner in corners),
            max(corner.y for corner in corners),
            max(corner.z for corner in corners),
        )
    )
    return bbox_min, bbox_max, bbox_max - bbox_min


def analyze_mesh_object(obj, allow_proxy_remesh: bool) -> MeshAnalysisResult:
    """Validate the selected mesh for conservative phase-1 generation."""
    if obj is None:
        return _empty_analysis("Select a mesh object before running Auto Mold.")
    if obj.type != "MESH":
        return _empty_analysis("The active object must be a mesh.")

    mesh = obj.data
    if len(mesh.polygons) == 0:
        return _empty_analysis("The selected mesh has no faces.")

    bm = bmesh.new()
    warnings: list[str] = []
    try:
        bm.from_mesh(mesh)
        bm.normal_update()

        is_manifold = all(edge.is_manifold for edge in bm.edges)
        has_consistent_normals = all(face.normal.length > 0.0 for face in bm.faces)
        try:
            volume_estimate = bm.calc_volume(signed=False) if is_manifold else 0.0
        except ValueError:
            volume_estimate = 0.0

        bbox_min, bbox_max, bbox_size = _world_bbox(obj)
        needs_proxy = not is_manifold and allow_proxy_remesh
        can_continue = True
        failure_reason = None

        if not is_manifold:
            if allow_proxy_remesh:
                warnings.append(
                    "Mesh is non-manifold; generation will use a temporary voxel-remeshed proxy."
                )
            else:
                can_continue = False
                failure_reason = (
                    "Mesh is non-manifold and proxy recovery is disabled."
                )

        return MeshAnalysisResult(
            is_mesh=True,
            has_faces=True,
            is_manifold=is_manifold,
            has_consistent_normals=has_consistent_normals,
            has_self_intersections=False,
            bbox_min=bbox_min,
            bbox_max=bbox_max,
            bbox_size=bbox_size,
            volume_estimate=volume_estimate,
            face_count=len(mesh.polygons),
            vertex_count=len(mesh.vertices),
            can_continue=can_continue,
            needs_proxy=needs_proxy,
            failure_reason=failure_reason,
            warnings=warnings,
        )
    finally:
        bm.free()
