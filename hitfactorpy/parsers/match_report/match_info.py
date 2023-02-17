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
MATCH_REPORT_PREFIX_REGION = f"{MatchReportInfoSectionFields.REGION.value}:"
MATCH_REPORT_PREFIX_CLUB_NAME = f"{MatchReportInfoSectionFields.CLUB_NAME.value}:"
MATCH_REPORT_PREFIX_CLUB_CODE = f"{MatchReportInfoSectionFields.CLUB_CODE.value}:"
MATCH_REPORT_PREFIX_PS_PRODUCT = f"{MatchReportInfoSectionFields.PS_PRODUCT.value}:"
MATCH_REPORT_PREFIX_PS_VERSION = f"{MatchReportInfoSectionFields.PS_VERSION.value}:"
MATCH_REPORT_PREFIX_PLATFORM = "PLATFORM "


def parse_match_info(info_lines: List[str]) -> ParsedMatchInfo:  # noqa: C901
    name: Optional[str] = None
    raw_date: Optional[str] = None
    date: Optional[datetime] = None
    level: Optional[MatchLevel] = None
    region: Optional[str] = None
    club_name: Optional[str] = None
    club_code: Optional[str] = None
    ps_product: Optional[str] = None
    ps_version: Optional[str] = None
    platform: Optional[str] = None
    for line in info_lines:
        if line.startswith(MATCH_REPORT_PREFIX_NAME):
            name = line.partition(MATCH_REPORT_PREFIX_NAME)[-1].strip()
            _logger.debug("match name found: %s", name)
        elif line.startswith(MATCH_REPORT_PREFIX_DATE):
            raw_date = line.partition(MATCH_REPORT_PREFIX_DATE)[-1].strip()
            _logger.debug("match date found: %s", raw_date)
            date = parse_match_date(raw_date)
        elif line.startswith(MATCH_REPORT_PREFIX_LEVEL):
            level_text = line.partition(MATCH_REPORT_PREFIX_LEVEL)[-1].strip().upper()
            _logger.debug("attempting to parse match level: %s", level_text)
            level = parse_match_level(level_text)
            _logger.debug("parsed match level: %s", level)
        elif line.startswith(MATCH_REPORT_PREFIX_REGION):
            region = line.partition(MATCH_REPORT_PREFIX_REGION)[-1].strip()
            _logger.debug("region found: %s", region)
        elif line.startswith(MATCH_REPORT_PREFIX_CLUB_NAME):
            club_name = line.partition(MATCH_REPORT_PREFIX_CLUB_NAME)[-1].strip()
            _logger.debug("club name found: %s", club_name)
        elif line.startswith(MATCH_REPORT_PREFIX_CLUB_CODE):
            club_code = line.partition(MATCH_REPORT_PREFIX_CLUB_CODE)[-1].strip()
            _logger.debug("club code found: %s", club_code)
        elif line.startswith(MATCH_REPORT_PREFIX_PS_PRODUCT):
            ps_product = line.partition(MATCH_REPORT_PREFIX_PS_PRODUCT)[-1].strip()
            _logger.debug("ps_product found: %s", ps_product)
        elif line.startswith(MATCH_REPORT_PREFIX_PS_VERSION):
            ps_version = line.partition(MATCH_REPORT_PREFIX_PS_VERSION)[-1].strip()
            _logger.debug("ps_version found: %s", ps_version)
        elif line.startswith(MATCH_REPORT_PREFIX_PLATFORM):
            platform = line.partition(MATCH_REPORT_PREFIX_PLATFORM)[-1].strip()
            _logger.debug("platform found: %s", platform)
    return ParsedMatchInfo(
        name=name,
        raw_date=raw_date,
        date=date,
        match_level=level,
        region=region,
        club_name=club_name,
        club_code=club_code,
        ps_product=ps_product,
        ps_version=ps_version,
        platform=platform,
    )
