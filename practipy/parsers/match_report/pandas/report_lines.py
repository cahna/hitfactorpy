from collections import defaultdict

from ..constants import MatchReportSectionPrefix
from ..models import ParsedMatchLines


def parse_match_report_response_lines(response: str) -> ParsedMatchLines:
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

    return ParsedMatchLines(
        info=categorized_lines.get(MatchReportSectionPrefix.INFO, []),
        competitor_columns=categorized_lines.get(MatchReportSectionPrefix.COMPETITOR_HEADER, []),
        competitor=categorized_lines.get(MatchReportSectionPrefix.COMPETITOR, []),
        stage_columns=categorized_lines.get(MatchReportSectionPrefix.STAGE_HEADER, []),
        stage=categorized_lines.get(MatchReportSectionPrefix.STAGE, []),
        stage_score_columns=categorized_lines.get(MatchReportSectionPrefix.STAGE_SCORE_HEADER, []),
        stage_score=categorized_lines.get(MatchReportSectionPrefix.STAGE_SCORE, []),
    )
