from decimal import Decimal

from pydantic import BaseModel, Field, NonNegativeInt, root_validator, validator

from ..decimal_ import D2, D4
from ..enums import PowerFactor, Scoring
from ..utils import calculate_hit_factor


class UspsaStageScore(BaseModel):
    """
    Minimum attributes for a stage score report to be able to calculate hit_factor.
    If `hit_factor` is omitted, it will be calculated from the remaining values.
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
    def _coerce_time_into_decimal(cls, v):
        return D2(v)

    @root_validator(pre=True)
    def _coerce_hit_factor_to_decimal_or_calculate_if_unset(cls, values):
        hit_factor = values.get("hit_factor")
        return {
            **values,
            "hit_factor": calculate_hit_factor(**values) if hit_factor is None else D4(hit_factor),
        }

    @root_validator
    def _check_hit_factor_matches_calculated_hit_factor(cls, values):
        if (hit_factor := values.get("hit_factor")) != (calculated_hit_factor := calculate_hit_factor(**values)):
            raise ValueError(f"calculated hit factor mismatch: given={hit_factor}, calculated={calculated_hit_factor}")
        return values

    def calculate_hit_factor(self):
        return calculate_hit_factor(**self.dict())
