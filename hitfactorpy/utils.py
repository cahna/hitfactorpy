import decimal
from typing import Protocol

from .enums import PowerFactor, PowerFactorLiteral, Scoring, ScoringLiteral


class StageScore(Protocol):
    class _Competitor(Protocol):
        power_factor: PowerFactor | PowerFactorLiteral
        dq: bool | None

    class _Stage(Protocol):
        scoring_type: Scoring | ScoringLiteral

    stage: _Stage
    competitor: _Competitor
    dq: bool | None
    dnf: bool | None
    a: int
    c: int
    d: int
    m: int
    ns: int
    procedural: int
    other_penalty: int
    late_shot: int
    extra_shot: int
    extra_hit: int
    time: float | decimal.Decimal
    hit_factor: float | decimal.Decimal | str  # If stage is chrono, this is required


class StageScoreWithStagePowerFactor(StageScore):
    stage_power_factor: PowerFactor | PowerFactorLiteral | None


def calculate_uspsa_hit_factor(stage_score: StageScore | StageScoreWithStagePowerFactor) -> decimal.Decimal:
    return decimal.Decimal(
        stage_score.hit_factor
        if stage_score.stage.scoring_type == Scoring.CHRONO
        else max(
            0.0,
            0.0
            if getattr(stage_score, "dq", False)
            or getattr(stage_score, "dnf", False)
            or getattr(stage_score.competitor, "dq", False)
            else (
                stage_score.a * 5
                + (
                    stage_score.c
                    * (
                        4
                        if getattr(stage_score, "stage_power_factor", stage_score.competitor.power_factor)
                        == PowerFactor.MAJOR
                        else 3
                    )
                )
                + (
                    stage_score.d
                    * (
                        2
                        if getattr(stage_score, "stage_power_factor", stage_score.competitor.power_factor)
                        == PowerFactor.MAJOR
                        else 1
                    )
                )
                + (stage_score.m * -10)
                + (stage_score.ns * -10)
                + (getattr(stage_score, "procedural", 0) * -10)
                + (getattr(stage_score, "other_penalty", 0) * -1)
                + (getattr(stage_score, "late_shot", 0) * -5)
                + (getattr(stage_score, "extra_shot", 0) * -10)
                + (getattr(stage_score, "extra_hit", 0) * -10)
            )
            / (getattr(stage_score, "time", None) or 1),
        )
    ).quantize(decimal.Decimal(".0001"))
