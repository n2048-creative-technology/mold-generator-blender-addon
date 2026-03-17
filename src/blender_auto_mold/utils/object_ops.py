"""Thin wrappers around common Blender object operations."""

from __future__ import annotations

import bpy

from .collections import move_object_to_collection


def ensure_object_mode(context) -> None:
    """Ensure Blender is in object mode before editing objects or modifiers."""
    if context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")


def set_active_object(context, obj) -> None:
    """Make an object active and selected."""
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    context.view_layer.objects.active = obj


def duplicate_object(context, source_obj, name: str, collection=None, linked: bool = False):
    """Duplicate an object and optionally move it to a target collection."""
    duplicate = source_obj.copy()
    duplicate.data = source_obj.data if linked else source_obj.data.copy()
    duplicate.name = name
    context.scene.collection.objects.link(duplicate)
    if collection is not None:
        move_object_to_collection(duplicate, collection)
    return duplicate


def apply_modifier(context, obj, modifier_name: str) -> None:
    """Apply a modifier on an object while preserving selection sanity."""
    ensure_object_mode(context)
    set_active_object(context, obj)
    bpy.ops.object.modifier_apply(modifier=modifier_name)


def delete_objects(context, objects) -> None:
    """Delete objects that were used as temporary operands."""
    existing = [obj for obj in objects if obj is not None and bpy.data.objects.get(obj.name) is not None]
    if not existing:
        return
    ensure_object_mode(context)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in existing:
        obj.select_set(True)
    context.view_layer.objects.active = existing[0]
    bpy.ops.object.delete()
