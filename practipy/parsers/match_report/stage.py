import logging
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import List, Optional

from ..csv_utils import parse_csv_row
from .field_parsers import parse_classification, parse_division, parse_member_number, parse_power_factor

logger = logging.getLogger(__name__)


@unique
class StageAttributeColumn(int, Enum):
    MIN_ROUNDS = 2
    MAX_POINTS = 3
    CLASSIFIER = 4
    CLASSIFIER_NUM = 5
    STAGE_NAME = 6
    SCORING = 7


def check_stage_columns(parsed_columns: List[str], fail_on_mismatch=False):
    check_failed = False
    expected_stage_name_col = parsed_columns[StageAttributeColumn.STAGE_NAME]
    if "name" not in expected_stage_name_col.lower():
        logger.error("CSV column order mismatch(?). Expected a stage name, but found: %s", expected_stage_name_col)
        check_failed = True
    # TODO: other checks, or just dynamically pick the values from the column name order?

    if fail_on_mismatch and check_failed:
        raise ValueError("expected parsed stage column order mismatch detected")


@dataclass(frozen=True)
class ParsedStage:
    name: Optional[str] = None
    min_rounds: Optional[int] = 0
    max_points: Optional[int] = 0
    # dq: bool = field(default_factory=lambda: False)


def parse_match_report_stage_column_lines(column_lines: List[str]) -> Optional[List[str]]:
    n_header_cols = len(column_lines)
    if n_header_cols == 0:
        logger.debug("no lines found for stage column names")
        return None
    if n_header_cols > 1:
        logger.warning("expected only one header line, but found %d", n_header_cols)
    columns: Optional[List[str]] = parse_csv_row(column_lines[0])
    return columns


def parse_match_report_stage_lines(
    stage_lines: List[str], stage_columns: Optional[List[str]] = None
) -> List[ParsedStage]:
    if stage_columns:
        check_stage_columns(stage_columns)
    stages: List[ParsedStage] = []
    for line in stage_lines:
        row = parse_csv_row(line)
        stage = ParsedStage(
            name=row[StageAttributeColumn.STAGE_NAME].strip(),
            min_rounds=row[StageAttributeColumn.MIN_ROUNDS],
            max_points=row[StageAttributeColumn.MAX_POINTS],
        )
        stages.append(stage)
    return stages
