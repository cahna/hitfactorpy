from ..models import ParsedMatchLines

REPORT_LINE_PREFIX_INFO = "$INFO "
REPORT_LINE_PREFIX_COLUMNS_COMPETITORS = "D "
REPORT_LINE_PREFIX_COMPETITOR = "E "
REPORT_LINE_PREFIX_COLUMNS_STAGE = "F"
REPORT_LINE_PREFIX_STAGE = "G "
REPORT_LINE_PREFIX_STAGE_SCORE = "I "


def parse_match_report_response_lines(response: str) -> ParsedMatchLines:
    """
    First step in parsing involves categorizing sections of the response text based on each line's prefix
    """
    categorized_lines = ParsedMatchLines()
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
