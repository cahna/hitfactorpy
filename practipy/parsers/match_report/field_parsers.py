import logging
import re
from datetime import datetime
from typing import Optional

from ...enums import Classification, Division, MatchLevel, PowerFactor, Scoring

_logger = logging.getLogger(__name__)


def parse_match_level(level_text: str) -> Optional[MatchLevel]:
    if "IV" in level_text:
        return MatchLevel.IV
    if "III" in level_text:
        return MatchLevel.III
    if "II" in level_text:
        return MatchLevel.II
    if "I" in level_text:
        return MatchLevel.I
    return None


MATCH_REPORT_DATE_FORMAT = "%m/%d/%Y"


def parse_match_date(date_text: str) -> Optional[datetime]:
    try:
        parsed_date = datetime.strptime(date_text, MATCH_REPORT_DATE_FORMAT)
        _logger.debug("match date found: %s", date_text)
        return parsed_date
    except ValueError:
        _logger.warning("failed to parse match date: %s", date_text)
        return None


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
            _logger.warning("unknown division %s", s.strip().lower())
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


def parse_member_number(s: str):
    return re.sub(r"[^0-9A-Z]", "", s.upper())


def parse_scoring(s: str):
    match s.strip().lower():
        case "comstock":
            return Scoring.COMSTOCK
        case "virginia":
            return Scoring.VIRGINIA
        case "fixed":
            return Scoring.FIXED_TIME
        case "chrono":
            return Scoring.CHRONO
        case _:
            _logger.warning("unknown scoring: %s", s)
            return Scoring.UNKNOWN


def parse_boolean(s: str):
    return (s or "").lower() == "yes"
