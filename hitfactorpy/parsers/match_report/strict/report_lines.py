import logging
from dataclasses import dataclass, field
from typing import List

from ..constants import MatchReportSectionPrefix

_logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ParsedMatchLines:
    info: List[str] = field(default_factory=list)
    competitor_columns: List[str] = field(default_factory=list)
    competitor: List[str] = field(default_factory=list)
    stage_columns: List[str] = field(default_factory=list)
    stage: List[str] = field(default_factory=list)
    stage_score_columns: List[str] = field(default_factory=list)
    stage_score: List[str] = field(default_factory=list)


REPORT_LINE_PREFIX_INFO = f"{MatchReportSectionPrefix.INFO.value} "
REPORT_LINE_PREFIX_COLUMNS_COMPETITORS = f"{MatchReportSectionPrefix.COMPETITOR_HEADER.value} "
REPORT_LINE_PREFIX_COMPETITOR = f"{MatchReportSectionPrefix.COMPETITOR.value} "
REPORT_LINE_PREFIX_COLUMNS_STAGE = f"{MatchReportSectionPrefix.STAGE_HEADER.value} "
REPORT_LINE_PREFIX_STAGE = f"{MatchReportSectionPrefix.STAGE.value} "
REPORT_LINE_PREFIX_COLUMNS_STAGE_SCORE = f"{MatchReportSectionPrefix.STAGE_SCORE_HEADER.value} "
REPORT_LINE_PREFIX_STAGE_SCORE = f"{MatchReportSectionPrefix.STAGE_SCORE.value} "


def parse_match_report_response_lines(response: str) -> ParsedMatchLines:
    """
    First step in parsing involves categorizing sections of the response text based on each line's prefix
    """
    info_lines: List[str] = []
    competitor_column_lines: List[str] = []
    competitor_lines: List[str] = []
    stage_lines: List[str] = []
    stage_score_column_lines: List[str] = []
    stage_score_lines: List[str] = []
    stage_column_lines: List[str] = []
    response_lines = response.splitlines()

    for line in response_lines:
        sanitized_line = line.strip()
        if sanitized_line.startswith(REPORT_LINE_PREFIX_INFO):
            info_lines.append(sanitized_line.partition(REPORT_LINE_PREFIX_INFO)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_COMPETITOR):
            competitor_lines.append(sanitized_line.partition(REPORT_LINE_PREFIX_COMPETITOR)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_STAGE):
            stage_lines.append(sanitized_line.partition(REPORT_LINE_PREFIX_STAGE)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_STAGE_SCORE):
            stage_score_lines.append(sanitized_line.partition(REPORT_LINE_PREFIX_STAGE_SCORE)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_COLUMNS_STAGE):
            stage_column_lines.append(sanitized_line.partition(REPORT_LINE_PREFIX_COLUMNS_STAGE)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_COLUMNS_COMPETITORS):
            competitor_column_lines.append(sanitized_line.partition(REPORT_LINE_PREFIX_COLUMNS_COMPETITORS)[-1])
        elif sanitized_line.startswith(REPORT_LINE_PREFIX_COLUMNS_STAGE_SCORE):
            stage_score_column_lines.append(sanitized_line.partition(REPORT_LINE_PREFIX_COLUMNS_STAGE_SCORE)[-1])
        else:
            _logger.warning("unrecognized line: %s", sanitized_line)

    return ParsedMatchLines(
        info=info_lines,
        stage_columns=stage_column_lines,
        stage=stage_lines,
        competitor_columns=competitor_column_lines,
        competitor=competitor_lines,
        stage_score_columns=stage_score_column_lines,
        stage_score=stage_score_lines,
    )
