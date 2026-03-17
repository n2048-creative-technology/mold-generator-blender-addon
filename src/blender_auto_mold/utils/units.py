"""Unit conversion helpers."""

from __future__ import annotations


def mm_to_scene(mm_value: float, scene) -> float:
    """Convert millimeters to current scene units."""
    scale_length = scene.unit_settings.scale_length or 1.0
    meters = mm_value / 1000.0
    return meters / scale_length


def scene_to_mm(scene_value: float, scene) -> float:
    """Convert current scene units to millimeters."""
    scale_length = scene.unit_settings.scale_length or 1.0
    meters = scene_value * scale_length
    return meters * 1000.0
