import logging
import re
from enum import Enum, unique
from typing import List, Optional

from ....enums import Scoring
from ...csv_utils import parse_csv_row, parse_int_value
from ..fields import parse_scoring
from ..models import ParsedStage

_logger = logging.getLogger(__name__)


@unique
class StageColumn(int, Enum):
    ID = 0
    MIN_ROUNDS = 2
    MAX_POINTS = 3
    CLASSIFIER = 4
    CLASSIFIER_NUM = 5
    STAGE_NAME = 6
    SCORING = 7


def check_stage_columns(parsed_columns: List[str], fail_on_mismatch=False):
    check_failed = False
    expected_stage_name_col = parsed_columns[StageColumn.STAGE_NAME]
    if "name" not in expected_stage_name_col.lower():
        _logger.error("CSV column order mismatch(?). Expected a stage name, but found: %s", expected_stage_name_col)
        check_failed = True
    # TODO: other checks, or just dynamically pick the values from the column name order?

    if fail_on_mismatch and check_failed:
        raise ValueError("expected parsed stage column order mismatch detected")


def parse_match_report_stage_column_lines(column_lines: List[str]) -> Optional[List[str]]:
    n_header_cols = len(column_lines)
    if n_header_cols == 0:
        _logger.debug("no lines found for stage column names")
        return None
    if n_header_cols > 1:
        _logger.warning("expected only one header line, but found %d", n_header_cols)
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
            internal_id=int(re.sub(r"[^0-9]", "", row[StageColumn.ID].strip())),
            name=row[StageColumn.STAGE_NAME].strip(),
            min_rounds=parse_int_value(row[StageColumn.MIN_ROUNDS]),
            max_points=parse_int_value(row[StageColumn.MAX_POINTS]),
            classifier=row[StageColumn.CLASSIFIER].strip().lower() == "yes",
            classifier_number=row[StageColumn.CLASSIFIER_NUM].strip(),
            scoring_type=parse_scoring(row[StageColumn.SCORING])
            if len(row) > StageColumn.SCORING
            else Scoring.COMSTOCK,
        )
        stages.append(stage)
    return stages
