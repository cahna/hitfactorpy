import logging
import re
from datetime import datetime
from typing import Any, Optional

from ...enums import Classification, Division, MatchLevel, PowerFactor, Scoring

_logger = logging.getLogger(__name__)


def parse_match_level(level_text: str) -> Optional[MatchLevel]:
    if not level_text:
        return None
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
        return parsed_date
    except (ValueError, TypeError):
        _logger.debug("failed to parse match date: %s", date_text)
        return None


def _sanitize_string(s: Any) -> str:
    return (s if (s and isinstance(s, str)) else "").strip()


def parse_division(s: str) -> Division:
    match _sanitize_string(s).lower():
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
        case _ as unrecognized_value:
            _logger.debug("unknown division: %s", unrecognized_value)
            return Division.UNKNOWN


def parse_classification(s: str) -> Classification:
    match _sanitize_string(s).lower():
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
        case _ as unrecognized_value:
            _logger.debug("unknown classification: %s", unrecognized_value)
            return Classification.UNKNOWN


def parse_power_factor(s: str) -> PowerFactor:
    match _sanitize_string(s).lower():
        case "major":
            return PowerFactor.MAJOR
        case "minor":
            return PowerFactor.MINOR
        case _ as unrecognized_value:
            _logger.debug("unknown power factor: %s", unrecognized_value)
            return PowerFactor.UNKNOWN


def parse_power_factor_default_none(s: str | None) -> PowerFactor | None:
    if s and (parsed_power_factor := parse_power_factor(s)):
        if parsed_power_factor and parsed_power_factor != PowerFactor.UNKNOWN:
            return parsed_power_factor
    return None


def parse_member_number(s: str):
    return re.sub(r"[^0-9A-Z]", "", _sanitize_string(s).upper())


def parse_scoring(s: str):
    match _sanitize_string(s).lower():
        case "comstock":
            return Scoring.COMSTOCK
        case "virginia":
            return Scoring.VIRGINIA
        case "fixed":
            return Scoring.FIXED_TIME
        case "chrono":
            return Scoring.CHRONO
        case _ as unrecognized_value:
            _logger.debug("unknown scoring: %s", unrecognized_value)
            return Scoring.UNKNOWN


def parse_boolean(s: str):
    return _sanitize_string(s).lower() == "yes"
