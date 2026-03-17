"""Axis-based pull scoring for conservative phase-1 mold selection."""

from __future__ import annotations

from mathutils import Vector

from .types import PullDirectionScore

_CANDIDATES = (
    ("+X", Vector((1.0, 0.0, 0.0))),
    ("-X", Vector((-1.0, 0.0, 0.0))),
    ("+Y", Vector((0.0, 1.0, 0.0))),
    ("-Y", Vector((0.0, -1.0, 0.0))),
    ("+Z", Vector((0.0, 0.0, 1.0))),
    ("-Z", Vector((0.0, 0.0, -1.0))),
)


def score_pull_directions(obj) -> list[PullDirectionScore]:
    """Score world-axis pull directions from face-normal distribution."""
    scores: list[PullDirectionScore] = []
    mesh = obj.data
    normal_matrix = obj.matrix_world.to_3x3()
    total_area = sum(poly.area for poly in mesh.polygons) or 1.0

    for axis_name, vector in _CANDIDATES:
        positive_area = 0.0
        negative_area = 0.0
        neutral_area = 0.0
        weighted_alignment = 0.0

        for poly in mesh.polygons:
            world_normal = normal_matrix @ poly.normal
            if world_normal.length == 0.0:
                continue
            world_normal.normalize()
            dot = world_normal.dot(vector)
            weighted_alignment += abs(dot) * poly.area

            if dot > 0.2:
                positive_area += poly.area
            elif dot < -0.2:
                negative_area += poly.area
            else:
                neutral_area += poly.area

        balance = min(positive_area, negative_area) / (max(positive_area, negative_area) + 1e-6)
        alignment = weighted_alignment / total_area
        neutral_ratio = neutral_area / total_area
        score = (balance * 0.55) + (alignment * 0.35) - (neutral_ratio * 0.20)

        notes: list[str] = []
        if neutral_ratio > 0.45:
            notes.append("large neutral band around the seam")
        if balance < 0.25:
            notes.append("heavily one-sided surface distribution")

        scores.append(
            PullDirectionScore(
                axis_name=axis_name,
                vector=vector,
                score=score,
                positive_area=positive_area,
                negative_area=negative_area,
                neutral_area=neutral_area,
                notes=notes,
            )
        )

    return sorted(scores, key=lambda item: item.score, reverse=True)


def choose_best_pull_direction(scores: list[PullDirectionScore]) -> PullDirectionScore:
    """Return the highest-ranked pull direction."""
    if not scores:
        raise ValueError("No pull-direction candidates were produced.")
    return scores[0]
