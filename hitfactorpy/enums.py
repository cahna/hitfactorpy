from enum import Enum, unique
from typing import Literal


@unique
class Scoring(str, Enum):
    COMSTOCK = "comstock"
    VIRGINIA = "virginia"
    FIXED_TIME = "fixedTime"
    CHRONO = "chrono"
    UNKNOWN = "unknown"


ScoringLiteral = Literal["comstock", "virginia", "fixedTime", "chrono", "unknown"]


@unique
class Division(str, Enum):
    PCC = "pcc"
    OPEN = "open"
    LIMITED = "limited"
    CARRY_OPTICS = "carryOptics"
    LIMITED_10 = "limited10"
    PRODUCTION = "production"
    SINGLE_STACK = "singleStack"
    REVOLVER = "revolver"

    """
    Unknown (missing data or parsing failed)
    """
    UNKNOWN = "unknown"


@unique
class PowerFactor(str, Enum):
    MAJOR = "major"
    MINOR = "minor"

    """
    Unknown (missing data or parsing failed)
    """
    UNKNOWN = "unknown"


PowerFactorLiteral = Literal["major", "minor", "unknown"]


@unique
class Classification(str, Enum):
    GM = "GM"
    M = "M"
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    """
    Unclassified
    """
    U = "U"

    """
    Unknown (missing data or parsing failed)
    """
    UNKNOWN = "unknown"


@unique
class MatchLevel(int, Enum):
    I = 1  # noqa: E741
    II = 2
    III = 3
    IV = 4
