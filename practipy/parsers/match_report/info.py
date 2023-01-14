import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from ....enums import MatchLevel

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ParsedMatchInfo:
    name: Optional[str] = None
    raw_date: Optional[str] = None
    date: Optional[datetime] = None
    level: Optional[MatchLevel] = None


_MATCH_REPORT_PREFIX_NAME = "Match name:"
_MATCH_REPORT_PREFIX_DATE = "Match date:"
_MATCH_REPORT_PREFIX_LEVEL = "Match Level:"
_MATCH_REPORT_DATE_FORMAT = "%m/%d/%Y"


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


def parse_match_date(date_text: str) -> Optional[datetime]:
    try:
        parsed_date = datetime.strptime(date_text, _MATCH_REPORT_DATE_FORMAT)
        logger.debug("match date found: %s", date_text)
        return parsed_date
    except ValueError:
        logger.warning("failed to parse match date: %s", date_text)
        return None


def parse_match_report_info_lines(info_lines: List[str]) -> ParsedMatchInfo:
    name: Optional[str] = None
    raw_date: Optional[str] = None
    date: Optional[datetime] = None
    level: Optional[MatchLevel] = None
    for line in info_lines:
        if line.startswith(_MATCH_REPORT_PREFIX_NAME):
            name = line.partition(_MATCH_REPORT_PREFIX_NAME)[-1]
            logger.debug("match name found: %s", name)
        elif line.startswith(_MATCH_REPORT_PREFIX_DATE):
            raw_date = line.partition(_MATCH_REPORT_PREFIX_DATE)[-1]
            logger.debug("match date found: %s", raw_date)
            date = parse_match_date(raw_date)
        elif line.startswith(_MATCH_REPORT_PREFIX_LEVEL):
            level_text = line.partition(_MATCH_REPORT_PREFIX_LEVEL)[-1].upper()
            logger.debug("attempting to parse match level: %s", level_text)
            level = parse_match_level(level_text)
            logger.debug("parsed match level: %s", level)
    return ParsedMatchInfo(name=name, raw_date=raw_date, date=date, level=level)
