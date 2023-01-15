import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from practipy.enums import MatchLevel

from .competitor import (
    ParsedCompetitor,
    parse_match_report_competitor_column_lines,
    parse_match_report_competitor_lines,
)
from .info import parse_match_report_info_lines
from .stage import ParsedStage, parse_match_report_stage_column_lines, parse_match_report_stage_lines

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _MatchResponseLines:
    info: List[str] = field(default_factory=list)
    competitor: List[str] = field(default_factory=list)
    stage: List[str] = field(default_factory=list)
    stage_score: List[str] = field(default_factory=list)
    competitor_columns: List[str] = field(default_factory=list)
    stage_columns: List[str] = field(default_factory=list)


REPORT_LINE_PREFIX_INFO = "$INFO "
REPORT_LINE_PREFIX_COLUMNS_COMPETITORS = "D "
REPORT_LINE_PREFIX_COMPETITOR = "E "
REPORT_LINE_PREFIX_COLUMNS_STAGE = "F"
REPORT_LINE_PREFIX_STAGE = "G "
REPORT_LINE_PREFIX_STAGE_SCORE = "I "


def _parse_match_report_response_lines(response: str) -> _MatchResponseLines:
    categorized_lines = _MatchResponseLines()
    response_lines = response.splitlines()

    for line in response_lines:
        sanitized_line = line.strip()
        if sanitized_line.startswith(REPORT_LINE_PREFIX_INFO):
            categorized_lines.info.append(sanitized_line.partition(REPORT_LINE_PREFIX_INFO)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_COMPETITOR):
            categorized_lines.competitor.append(sanitized_line.partition(REPORT_LINE_PREFIX_COMPETITOR)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_STAGE):
            categorized_lines.stage.append(sanitized_line.partition(REPORT_LINE_PREFIX_STAGE)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_STAGE_SCORE):
            categorized_lines.stage_score.append(sanitized_line.partition(REPORT_LINE_PREFIX_STAGE_SCORE)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_COLUMNS_STAGE):
            categorized_lines.stage_columns.append(sanitized_line.partition(REPORT_LINE_PREFIX_COLUMNS_STAGE)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_COLUMNS_COMPETITORS):
            categorized_lines.competitor_columns.append(
                sanitized_line.partition(REPORT_LINE_PREFIX_COLUMNS_COMPETITORS)[-1]
            )

    return categorized_lines


@dataclass
class ParsedMatchReport:
    name: Optional[str] = None
    raw_date: Optional[str] = None
    date: Optional[datetime] = None
    match_level: Optional[MatchLevel] = None
    practiscore_id: Optional[str] = None
    report_contents: Optional[str] = None
    competitors: Optional[List[ParsedCompetitor]] = None
    stages: Optional[List[ParsedStage]] = None


def parse_match_report(report_text: str) -> ParsedMatchReport:
    report_lines = _parse_match_report_response_lines(report_text)
    match_info = parse_match_report_info_lines(report_lines.info)
    competitor_columns = parse_match_report_competitor_column_lines(report_lines.competitor_columns)
    competitors = parse_match_report_competitor_lines(report_lines.competitor, competitor_columns)
    stage_columns = parse_match_report_stage_column_lines(report_lines.stage_columns)
    stages = parse_match_report_stage_lines(report_lines.stage, stage_columns)
    return ParsedMatchReport(
        name=match_info.name,
        raw_date=match_info.raw_date,
        date=match_info.date,
        match_level=match_info.level,
        competitors=competitors,
        stages=stages,
    )
