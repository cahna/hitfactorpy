import logging
import re
from enum import Enum, unique
from typing import List, Optional

from ...csv_utils import parse_csv_row
from ..fields import parse_classification, parse_division, parse_member_number, parse_power_factor
from ..models import ParsedCompetitor

_logger = logging.getLogger(__name__)


@unique
class CompetitorColumn(int, Enum):
    """Expected column indices"""

    ID = 0
    MEMBER_NUM = 1
    FIRST_NAME = 2
    LAST_NAME = 3
    DQ_PISTOL = 4
    DQ_RIFLE = 5
    DQ_SHOTGUN = 6
    REENTRY = 7
    CLASS = 8
    DIVISION = 9
    POWER_FACTOR = 12


def check_competitor_columns(parsed_columns: List[str], fail_on_mismatch=False):
    check_failed = False
    expected_first_name_col = parsed_columns[CompetitorColumn.FIRST_NAME]
    if "first" not in expected_first_name_col.lower():
        _logger.error("CSV column order mismatch(?). Expected 'FirstName', but found: %s", expected_first_name_col)
        check_failed = True
    # TODO: other checks, or just dynamically pick the values from the column name order?

    if fail_on_mismatch and check_failed:
        raise ValueError("expected parsed column order mismatch detected")


def _is_dq(competitor_row: List[str]) -> bool:
    return "yes" in [
        competitor_row[CompetitorColumn.DQ_PISTOL].lower(),
        competitor_row[CompetitorColumn.DQ_RIFLE].lower(),
        competitor_row[CompetitorColumn.DQ_SHOTGUN].lower(),
    ]


def parse_match_report_competitor_column_lines(column_lines: List[str]) -> Optional[List[str]]:
    n_header_cols = len(column_lines)
    if n_header_cols == 0:
        _logger.debug("no lines found for column names")
        return None
    if n_header_cols > 1:
        _logger.error("expected only one header line, but found %d", n_header_cols)
    columns: Optional[List[str]] = parse_csv_row(column_lines[0])
    return columns


def parse_match_report_competitor_lines(
    competitor_lines: List[str], competitor_columns: Optional[List[str]] = None
) -> List[ParsedCompetitor]:
    if competitor_columns:
        check_competitor_columns(competitor_columns)
    competitors: List[ParsedCompetitor] = []
    for line in competitor_lines:
        row = parse_csv_row(line)
        competitor = ParsedCompetitor(
            internal_id=int(re.sub(r"[^0-9]", "", row[CompetitorColumn.ID].strip())),
            member_number=parse_member_number(row[CompetitorColumn.MEMBER_NUM]),
            first_name=row[CompetitorColumn.FIRST_NAME].strip(),
            last_name=row[CompetitorColumn.LAST_NAME].strip(),
            division=parse_division(row[CompetitorColumn.DIVISION]),
            classification=parse_classification(row[CompetitorColumn.CLASS]),
            power_factor=parse_power_factor(row[CompetitorColumn.POWER_FACTOR]),
            reentry=row[CompetitorColumn.REENTRY].lower() == "yes",
            dq=_is_dq(row),
        )
        competitors.append(competitor)
    return competitors
