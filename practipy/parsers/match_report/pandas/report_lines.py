from collections import defaultdict
from enum import Enum, unique

from ..models import ParsedMatchLines


@unique
class SectionPrefix(str, Enum):
    """Nothing works if these aren't consistent across reports. I'm assuming they are(?)"""

    INFO = "$INFO"
    COMPETITOR_HEADER = "D"
    COMPETITOR = "E"
    STAGE_HEADER = "F"
    STAGE = "G"
    STAGE_SCORE_HEADER = "H"
    STAGE_SCORE = "I"


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
        info=categorized_lines.get(SectionPrefix.INFO, []),
        competitor_columns=categorized_lines.get(SectionPrefix.COMPETITOR_HEADER, []),
        competitor=categorized_lines.get(SectionPrefix.COMPETITOR, []),
        stage_columns=categorized_lines.get(SectionPrefix.STAGE_HEADER, []),
        stage=categorized_lines.get(SectionPrefix.STAGE, []),
        # stage_score_columns=categorized_lines.get(SectionPrefix.STAGE_SCORE_HEADER, []),
        stage_score=categorized_lines.get(SectionPrefix.STAGE_SCORE, []),
    )
