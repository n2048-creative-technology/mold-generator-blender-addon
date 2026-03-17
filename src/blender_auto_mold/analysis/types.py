"""Structured analysis and generation datatypes."""

from __future__ import annotations

from dataclasses import dataclass, field

from mathutils import Vector


@dataclass(slots=True)
class MeshAnalysisResult:
    """Summary of the mesh validation pass."""

    is_mesh: bool
    has_faces: bool
    is_manifold: bool
    has_consistent_normals: bool
    has_self_intersections: bool
    bbox_min: Vector
    bbox_max: Vector
    bbox_size: Vector
    volume_estimate: float
    face_count: int
    vertex_count: int
    can_continue: bool
    needs_proxy: bool = False
    failure_reason: str | None = None
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PullDirectionScore:
    """Scored candidate pull direction."""

    axis_name: str
    vector: Vector
    score: float
    positive_area: float
    negative_area: float
    neutral_area: float
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MoldGenerationSettings:
    """Settings consumed by geometry generation."""

    silicone_thickness_mm: float
    wall_thickness_mm: float
    flange_margin_mm: float
    flange_height_mm: float
    register_radius_mm: float
    register_depth_mm: float
    clamp_hole_radius_mm: float
    sprue_radius_mm: float
    vent_radius_mm: float
    proxy_voxel_size_mm: float
    cleanup_voxel_size_mm: float
    allow_proxy_remesh: bool
    output_collection_name: str


@dataclass(slots=True)
class MoldGenerationResult:
    """Summary of a successful generation run."""

    collection_name: str
    generated_objects: list[str]
    pull_direction: str
    used_proxy: bool
    warnings: list[str] = field(default_factory=list)
