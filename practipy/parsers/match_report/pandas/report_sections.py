import logging
from collections import defaultdict
from dataclasses import dataclass

from ..constants import MatchReportSectionPrefix

_logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ParsedMatchReportSections:
    """Report split into sections by prefix (prefix is stripped)"""

    info: str
    competitors: str
    stages: str
    stage_scores: str


def parse_match_report_sections(response: str) -> ParsedMatchReportSections:
    """
    First step in parsing involves categorizing sections of the response text based on each line's prefix
    """
    response_lines = response.splitlines()
    categorized_lines = defaultdict(list)

    for line in response_lines:
        if not line.startswith("$END"):
            try:
                prefix, line_content = line.split(None, 1)
                categorized_lines[prefix].append(line_content)
            except ValueError:
                pass

    competitor_columns = categorized_lines.get(MatchReportSectionPrefix.COMPETITOR_HEADER, [])
    stage_columns = categorized_lines.get(MatchReportSectionPrefix.STAGE_HEADER, [])
    stage_score_columns = categorized_lines.get(MatchReportSectionPrefix.STAGE_SCORE_HEADER, [])

    if not competitor_columns:
        _logger.error("failed to parse competitor columns")
    if not stage_columns:
        _logger.error("failed to parse stage columns")
    if not stage_score_columns:
        _logger.error("failed to parse stage_score columns")

    return ParsedMatchReportSections(
        info="\n".join(categorized_lines.get(MatchReportSectionPrefix.INFO, [])),
        competitors=f"{competitor_columns[0]}\n"
        + "\n".join(categorized_lines.get(MatchReportSectionPrefix.COMPETITOR, [])),
        stages=f"{stage_columns[0]}\n" + "\n".join(categorized_lines.get(MatchReportSectionPrefix.STAGE, [])),
        stage_scores=f"{stage_score_columns[0]}\n"
        + "\n".join(categorized_lines.get(MatchReportSectionPrefix.STAGE_SCORE, [])),
    )
