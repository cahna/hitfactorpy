import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ...enums import MatchLevel

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MatchResponseLines:
    info: List[str] = field(default_factory=list)
    competitor: List[str] = field(default_factory=list)
    stage: List[str] = field(default_factory=list)
    stage_score: List[str] = field(default_factory=list)


def parse_match_report_response_lines(response: str) -> MatchResponseLines:
    categorized_lines = MatchResponseLines([], [], [], [])
    response_lines = response.splitlines()
    for line in response_lines:
        sanitized_line = line.strip()
        if sanitized_line.startswith("$INFO"):
            categorized_lines.info.append(sanitized_line)
        elif sanitized_line.startswith("E "):
            categorized_lines.competitor.append(sanitized_line)
        elif sanitized_line.startswith("G "):
            categorized_lines.stage.append(sanitized_line)
        elif sanitized_line.startswith("I "):
            categorized_lines.stage_score.append(sanitized_line)
    return categorized_lines


@dataclass(frozen=True)
class ParsedMatchInfo:
    name: Optional[str] = None
    raw_date: Optional[str] = None
    date: Optional[datetime] = None
    level: Optional[MatchLevel] = None


_MATCH_REPORT_PREFIX_NAME = "$INFO Match name:"
_MATCH_REPORT_PREFIX_DATE = "$INFO Match date:"
_MATCH_REPORT_PREFIX_LEVEL = "$INFO Match Level:"
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


def parse_match_report(report_text: str):
    report_lines = parse_match_report_response_lines(report_text)
    match_info = parse_match_report_info_lines(report_lines.info)
    return match_info
