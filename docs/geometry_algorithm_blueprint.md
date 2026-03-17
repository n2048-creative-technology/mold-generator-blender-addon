# Geometry Algorithm Blueprint
## Auto Mold Generator for Blender

## Purpose

This document defines the geometry and analysis pipeline for the Auto Mold Generator Blender add-on.

The goal is to generate physically usable mold systems around a selected object while optimizing for:

- minimum number of mold parts
- easy demolding
- minimal silicone use
- printable rigid support shells
- alignment and clamping
- vents and filling sprues
- predictable and inspectable geometry generation

This blueprint is intentionally conservative.

Version 1 should focus on:
- watertight manifold meshes
- two-part shell molds
- robust geometry generation
- explicit failure reporting
- debug visualization

More advanced multipart and insert-based decomposition should be built on top of this foundation.

---

## 1. Design Overview

The add-on should generate a mold system in layers:

1. **Source Object**
2. **Silicone Negative Shell**
3. **Rigid Outer Support Shell**
4. **Parting Geometry**
5. **Alignment Features**
6. **Clamp Features**
7. **Sprue and Vent Geometry**

The core problem is not just "wrap the object in a shell".

The real problem is:

- determine whether the object can demold in two directions
- find the best pull direction
- find a practical parting line
- minimize mold-piece count
- generate mold geometry that is printable and assemblable

---

## 2. Core Pipeline

The full pipeline is:

1. Mesh Validation
2. Surface Analysis
3. Candidate Pull Direction Generation
4. Pull Direction Scoring
5. Undercut Detection
6. Parting Region Extraction
7. Seam / Parting Line Construction
8. Mold Strategy Decision
9. Silicone Shell Generation
10. Rigid Shell Generation
11. Flange Generation
12. Alignment Feature Generation
13. Clamp Feature Generation
14. Sprue and Vent Generation
15. Part Splitting and Collection Output
16. Validation of Generated Parts

---

## 3. Data Structures

Use small structured data containers.

### 3.1 MeshAnalysisResult

```python
@dataclass
class MeshAnalysisResult:
    is_manifold: bool
    has_consistent_normals: bool
    has_self_intersections: bool
    bbox_min: Vector
    bbox_max: Vector
    bbox_size: Vector
    volume_estimate: float
    face_count: int
    vertex_count: int
    warnings: list[str]