from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConstrainedDecimal, Field, NonNegativeInt, validator

from ..decimal_ import D2, D4
from ..enums import PowerFactor, Scoring
from ..utils import get_hf


class UspsaStageScore(BaseModel):
    """
    Minimum attributes for a stage score report to be able to calculate hit_factor
    """

    class Config:
        orm_mode = True

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
    time: Decimal = Field(ge=0, max_digits=8, decimal_places=2, default_factory=lambda: D2("0"))
    hit_factor: Decimal = Field(ge=0, max_digits=8, decimal_places=4, default_factory=lambda: D4("0"))

    @validator("time", pre=True)
    def coerce_time_into_decimal(cls, v):
        return D2(v)

    @validator("hit_factor", pre=True)
    def coerce_hit_factor_into_decimal(cls, v):
        return D4(v)

    def calculate_hit_factor(self):
        return get_hf(**self.dict())
