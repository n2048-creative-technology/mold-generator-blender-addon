"""Helpers for routing generated objects into predictable collections."""

from __future__ import annotations

import bpy


def ensure_collection(name: str, parent: bpy.types.Collection) -> bpy.types.Collection:
    """Return a collection with the requested name under the given parent."""
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
    if collection not in parent.children[:]:
        parent.children.link(collection)
    return collection


def move_object_to_collection(obj: bpy.types.Object, collection: bpy.types.Collection) -> None:
    """Move an object into the target collection and unlink prior users."""
    for user_collection in list(obj.users_collection):
        user_collection.objects.unlink(obj)
    if obj not in collection.objects[:]:
        collection.objects.link(obj)
