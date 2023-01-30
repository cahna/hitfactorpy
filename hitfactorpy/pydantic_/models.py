from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConstrainedDecimal, Field, NonNegativeInt

from ..enums import PowerFactor, Scoring
from ..utils import calculate_uspsa_hit_factor


class TimeDecimal(ConstrainedDecimal):
    ge = 0
    max_digits = 8
    decimal_places = 2


class HitFactorDecimal(ConstrainedDecimal):
    ge = 0
    max_digits = 8
    decimal_places = 4


class UspsaStageScore(BaseModel):
    """
    Minimum attributes for a stage score report to be able to calculate hit_factor
    """

    dq: bool = False
    dnf: bool = False
    scoring_type: Scoring = Scoring.COMSTOCK
    power_factor: PowerFactor = PowerFactor.MINOR
    a: NonNegativeInt = 0
    c: NonNegativeInt = 0
    d: NonNegativeInt = 0
    m: NonNegativeInt = 0
    ns: NonNegativeInt = 0
    procedural: NonNegativeInt = 0
    other_penalty: NonNegativeInt = 0
    late_shot: NonNegativeInt = 0
    extra_shot: NonNegativeInt = 0
    extra_hit: NonNegativeInt = 0
    time: Annotated[TimeDecimal, Field(default_factory=Decimal)]
    hit_factor: Annotated[HitFactorDecimal, Field(default_factory=Decimal)]

    @staticmethod
    def calculate_hit_factor(stage_score: "UspsaStageScore"):
        pass
