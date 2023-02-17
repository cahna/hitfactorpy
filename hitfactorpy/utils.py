import decimal

from .decimal_ import D4
from .enums import PowerFactor, Scoring


def calculate_hit_factor(
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
    hit_factor: float | decimal.Decimal | str = 0.0,  # If stage is chrono, this is required
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
