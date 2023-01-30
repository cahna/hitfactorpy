import decimal
from typing import Protocol

from .enums import PowerFactor, PowerFactorLiteral, Scoring, ScoringLiteral


class IUspsaStageScore(Protocol):
    scoring_type: Scoring | ScoringLiteral | None
    power_factor: PowerFactor | PowerFactorLiteral | None
    dq: bool | None
    dnf: bool | None
    a: int | None
    c: int | None
    d: int | None
    m: int | None
    ns: int | None
    procedural: int | None
    other_penalty: int | None
    late_shot: int | None
    extra_shot: int | None
    extra_hit: int | None
    time: float | decimal.Decimal | None
    hit_factor: float | decimal.Decimal | str | None  # If stage is chrono, this is required


def calculate_uspsa_hit_factor(stage_score: IUspsaStageScore) -> decimal.Decimal:
    return decimal.Decimal(
        getattr(stage_score, "hit_factor", 0)
        if getattr(stage_score, "scoring_type", Scoring.COMSTOCK) == Scoring.CHRONO
        else max(
            0.0,
            0.0
            if getattr(stage_score, "dq", False) or getattr(stage_score, "dnf", False)
            else (
                getattr(stage_score, "a", 0) * 5
                + (
                    getattr(stage_score, "c", 0)
                    * (4 if getattr(stage_score, "power_factor", PowerFactor.MINOR) == PowerFactor.MAJOR else 3)
                )
                + (
                    getattr(stage_score, "d", 0)
                    * (2 if getattr(stage_score, "power_factor", PowerFactor.MINOR) == PowerFactor.MAJOR else 1)
                )
                + (getattr(stage_score, "m", 0) * -10)
                + (getattr(stage_score, "ns", 0) * -10)
                + (getattr(stage_score, "procedural", 0) * -10)
                + (getattr(stage_score, "other_penalty", 0) * -1)
                + (getattr(stage_score, "late_shot", 0) * -5)
                + (getattr(stage_score, "extra_shot", 0) * -10)
                + (getattr(stage_score, "extra_hit", 0) * -10)
            )
            / (getattr(stage_score, "time", None) or 1),
        )
    ).quantize(decimal.Decimal(".0001"))
