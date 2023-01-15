import logging

from ...enums import Classification, Division, PowerFactor

logger = logging.getLogger(__name__)


def parse_division(s: str) -> Division:
    match s.strip().lower():
        case "pcc" | "pistol caliber carbine":
            return Division.PCC
        case "open":
            return Division.OPEN
        case "ltd" | "limited":
            return Division.LIMITED
        case "carry optics" | "co":
            return Division.CARRY_OPTICS
        case "l10" | "ltd10" | "limited 10":
            return Division.LIMITED_10
        case "prod" | "production":
            return Division.PRODUCTION
        case "ss" | "single stack":
            return Division.SINGLE_STACK
        case "rev" | "revo" | "revolver":
            return Division.REVOLVER
        case _:
            logger.warning("unknown division %s", s.strip().lower())
            return Division.UNKNOWN


def parse_classification(s: str) -> Classification:
    match s.strip().lower():
        case "gm" | "grandmaster" | "g":
            return Classification.GM
        case "m" | "master":
            return Classification.M
        case "a":
            return Classification.A
        case "b":
            return Classification.B
        case "c":
            return Classification.C
        case "d":
            return Classification.D
        case "u" | "x":
            return Classification.U
        case _:
            return Classification.UNKNOWN


def parse_power_factor(s: str) -> PowerFactor:
    match s.strip().lower():
        case "major":
            return PowerFactor.MAJOR
        case "minor":
            return PowerFactor.MINOR
        case _:
            return PowerFactor.UNKNOWN
