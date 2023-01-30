import decimal
from typing import Protocol

from .decimal_ import D4
from .enums import PowerFactor, Scoring


def get_hf(
    scoring_type: Scoring = Scoring.COMSTOCK,
    power_factor: PowerFactor = PowerFactor.MINOR,
    dq: bool = False,
    dnf: bool = False,
    a: int = 0,
    c: int = 0,
    d: int = 0,
    m: int = 0,
    ns: int = 0,
    procedural: int = 0,
    other_penalty: int = 0,
    late_shot: int = 0,
    extra_shot: int = 0,
    extra_hit: int = 0,
    time: float | decimal.Decimal = 0.0,
    hit_factor: float | decimal.Decimal | str = 0.0,
) -> decimal.Decimal:
    return D4(
        hit_factor
        if scoring_type in [Scoring.CHRONO, Scoring.CHRONO.value]
        else max(
            (
                0.0,
                0.0
                if dq or dnf
                else (
                    (
                        (a * 5)
                        + (c * (4 if power_factor in [PowerFactor.MAJOR, PowerFactor.MAJOR.value] else 3))
                        + (d * (2 if power_factor in [PowerFactor.MAJOR, PowerFactor.MAJOR.value] else 1))
                        + (m * -10)
                        + (ns * -10)
                        + (procedural * -10)
                        + (other_penalty * -1)
                        + (late_shot * -5)
                        + (extra_shot * -10)
                        + (extra_hit * -10)
                    )
                    / (time or 1)
                ),
            )
        )
    )


class IUspsaStageScore(Protocol):
    scoring_type: Scoring = Scoring.COMSTOCK
    power_factor: PowerFactor = PowerFactor.MINOR
    dq: bool = False
    dnf: bool = False
    a: int = 0
    c: int = 0
    d: int = 0
    m: int = 0
    ns: int = 0
    procedural: int = 0
    other_penalty: int = 0
    late_shot: int = 0
    extra_shot: int = 0
    extra_hit: int = 0
    time: float | decimal.Decimal = 0.0
    hit_factor: float | decimal.Decimal | str = 0.0  # If stage is chrono, this is required


def calculate_uspsa_hit_factor(stage_score: IUspsaStageScore) -> decimal.Decimal:
    return D4(
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
    )
