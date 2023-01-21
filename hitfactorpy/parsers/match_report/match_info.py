import logging
from datetime import datetime
from typing import List, Optional

from ...enums import MatchLevel
from .constants import MatchReportInfoSectionFields
from .fields import parse_match_date, parse_match_level
from .models import ParsedMatchInfo

_logger = logging.getLogger(__name__)


MATCH_REPORT_PREFIX_NAME = f"{MatchReportInfoSectionFields.MATCH_NAME.value}:"
MATCH_REPORT_PREFIX_DATE = f"{MatchReportInfoSectionFields.MATCH_DATE.value}:"
MATCH_REPORT_PREFIX_LEVEL = f"{MatchReportInfoSectionFields.MATCH_LEVEL.value}:"


def parse_match_info(info_lines: List[str]) -> ParsedMatchInfo:
    name: Optional[str] = None
    raw_date: Optional[str] = None
    date: Optional[datetime] = None
    level: Optional[MatchLevel] = None
    for line in info_lines:
        if line.startswith(MATCH_REPORT_PREFIX_NAME):
            name = line.partition(MATCH_REPORT_PREFIX_NAME)[-1]
            _logger.debug("match name found: %s", name)
        elif line.startswith(MATCH_REPORT_PREFIX_DATE):
            raw_date = line.partition(MATCH_REPORT_PREFIX_DATE)[-1]
            _logger.debug("match date found: %s", raw_date)
            date = parse_match_date(raw_date)
        elif line.startswith(MATCH_REPORT_PREFIX_LEVEL):
            level_text = line.partition(MATCH_REPORT_PREFIX_LEVEL)[-1].upper()
            _logger.debug("attempting to parse match level: %s", level_text)
            level = parse_match_level(level_text)
            _logger.debug("parsed match level: %s", level)
    return ParsedMatchInfo(name=name, raw_date=raw_date, date=date, match_level=level)
