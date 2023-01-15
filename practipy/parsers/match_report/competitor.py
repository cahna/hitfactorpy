import logging
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import List, Optional

from ...enums import Classification, Division, PowerFactor
from ..csv_utils import parse_csv_row
from .field_parsers import parse_classification, parse_division, parse_member_number, parse_power_factor

logger = logging.getLogger(__name__)


@unique
class CompetitorAttributeColumn(int, Enum):
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
    expected_first_name_col = parsed_columns[CompetitorAttributeColumn.FIRST_NAME]
    if "first" not in expected_first_name_col.lower():
        logger.error("CSV column order mismatch(?). Expected 'FirstName', but found: %s", expected_first_name_col)
        check_failed = True
    # TODO: other checks, or just dynamically pick the values from the column name order?

    if fail_on_mismatch and check_failed:
        raise ValueError("expected parsed column order mismatch detected")


@dataclass(frozen=True)
class ParsedCompetitor:
    member_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    division: Optional[Division] = None
    classification: Optional[Classification] = None
    power_factor: Optional[PowerFactor] = None
    dq: bool = field(default_factory=lambda: False)


def parse_match_report_competitor_lines(
    competitor_lines: List[str], columns: Optional[List[str]] = None
) -> List[ParsedCompetitor]:
    if columns:
        check_competitor_columns(columns)
    competitors: List[ParsedCompetitor] = []
    for line in competitor_lines:
        row = parse_csv_row(line)
        competitors.append(
            ParsedCompetitor(
                member_number=parse_member_number(row[CompetitorAttributeColumn.MEMBER_NUM]),
                first_name=row[CompetitorAttributeColumn.FIRST_NAME].strip(),
                last_name=row[CompetitorAttributeColumn.LAST_NAME].strip(),
                division=parse_division(row[CompetitorAttributeColumn.DIVISION]),
                classification=parse_classification(row[CompetitorAttributeColumn.CLASS]),
                power_factor=parse_power_factor(row[CompetitorAttributeColumn.POWER_FACTOR]),
            )
        )
    return competitors
