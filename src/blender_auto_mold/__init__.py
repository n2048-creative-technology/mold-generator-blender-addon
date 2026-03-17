"""Blender Auto Mold add-on package."""

bl_info = {
    "name": "Auto Mold Generator",
    "author": "OpenAI Codex",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Auto Mold",
    "description": "Generate conservative two-part mold halves from a mesh object",
    "category": "Object",
}

import bpy

from .operators.generate_mold import AUTO_MOLD_OT_generate
from .panels.auto_mold_panel import VIEW3D_PT_auto_mold
from .properties import AutoMoldProperties

CLASSES = (
    AutoMoldProperties,
    AUTO_MOLD_OT_generate,
    VIEW3D_PT_auto_mold,
)


def register():
    """Register Blender classes and scene properties."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.auto_mold = bpy.props.PointerProperty(type=AutoMoldProperties)


def unregister():
    """Unregister Blender classes and scene properties."""
    del bpy.types.Scene.auto_mold
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
