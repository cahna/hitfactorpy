import logging
from enum import Enum, unique
from typing import List, Optional

from ....enums import PowerFactor
from ...csv_utils import parse_csv_row, parse_float_value, parse_int_value
from ..fields import parse_boolean, parse_power_factor, parse_power_factor_default_none
from ..models import ParsedStageScore

_logger = logging.getLogger(__name__)


@unique
class StageScoreColumn(int, Enum):
    """Expected column indices"""

    STAGE_ID = 1
    SHOOTER_ID = 2
    DQ = 3
    DNF = 4
    A = 5
    B = 6
    C = 7
    D = 8
    M = 9
    NS = 10
    PROC = 11
    DOUBLE_POPPERS = 12
    DOUBLE_POPPER_MISS = 13
    LATE_SHOT = 14
    EXTRA_SHOT = 15
    EXTRA_HIT = 16
    NPM = 17
    OTHER_PENALTY = 18
    PENALTY_POINTS = 19
    T1 = 20
    T2 = 21
    T3 = 22
    T4 = 23
    T5 = 24
    TIME = 25
    RAW_POINTS = 26
    TOTAL_POINTS = 27
    HIT_FACTOR = 28
    STAGE_POINTS = 29
    STAGE_PLACE = 30
    STAGE_POWER_FACTOR = 31


def check_stage_score_columns(parsed_columns: List[str], fail_on_mismatch=False):
    check_failed = False
    expected_stage_id_col = parsed_columns[StageScoreColumn.STAGE_ID]
    if "stage" not in expected_stage_id_col.lower():
        _logger.error("CSV column order mismatch(?). Expected a stage id, but found: %s", expected_stage_id_col)
        check_failed = True
    # TODO: other checks, or just dynamically pick the values from the column name order?

    if fail_on_mismatch and check_failed:
        raise ValueError("expected parsed stage score column order mismatch detected")


def parse_match_report_stage_score_lines(
    stage_lines: List[str], stage_columns: Optional[List[str]] = None
) -> List[ParsedStageScore]:
    if stage_columns:
        check_stage_score_columns(stage_columns)
    stages: List[ParsedStageScore] = []
    for line in stage_lines:
        row = parse_csv_row(line)
        stage = ParsedStageScore(
            stage_id=parse_int_value(row[StageScoreColumn.STAGE_ID].strip()),
            competitor_id=parse_int_value(row[StageScoreColumn.SHOOTER_ID].strip()),
            dq=parse_boolean(row[StageScoreColumn.DQ].strip()),
            dnf=parse_boolean(row[StageScoreColumn.DNF].strip()),
            a=parse_int_value(row[StageScoreColumn.A].strip()) or 0,
            b=parse_int_value(row[StageScoreColumn.B].strip()) or 0,
            c=parse_int_value(row[StageScoreColumn.C].strip()) or 0,
            d=parse_int_value(row[StageScoreColumn.D].strip()) or 0,
            m=parse_int_value(row[StageScoreColumn.M].strip()) or 0,
            npm=parse_int_value(row[StageScoreColumn.NPM].strip()) or 0,
            ns=parse_int_value(row[StageScoreColumn.NS].strip()) or 0,
            procedural=parse_int_value(row[StageScoreColumn.PROC].strip()) or 0,
            late_shot=parse_int_value(row[StageScoreColumn.LATE_SHOT].strip()) or 0,
            extra_shot=parse_int_value(row[StageScoreColumn.EXTRA_SHOT].strip()) or 0,
            extra_hit=parse_int_value(row[StageScoreColumn.EXTRA_HIT].strip()) or 0,
            other_penalty=parse_int_value(row[StageScoreColumn.OTHER_PENALTY].strip()) or 0,
            t1=parse_float_value(row[StageScoreColumn.T1].strip()) or 0.0,
            t2=parse_float_value(row[StageScoreColumn.T2].strip()) or 0.0,
            t3=parse_float_value(row[StageScoreColumn.T3].strip()) or 0.0,
            t4=parse_float_value(row[StageScoreColumn.T4].strip()) or 0.0,
            t5=parse_float_value(row[StageScoreColumn.T5].strip()) or 0.0,
            time=parse_float_value(row[StageScoreColumn.TIME].strip()) or 0.0,
            raw_points=parse_float_value(row[StageScoreColumn.RAW_POINTS].strip()),
            penalty_points=parse_float_value(row[StageScoreColumn.PENALTY_POINTS].strip()),
            total_points=parse_float_value(row[StageScoreColumn.TOTAL_POINTS].strip()),
            hit_factor=parse_float_value(row[StageScoreColumn.HIT_FACTOR].strip()),
            stage_points=parse_float_value(row[StageScoreColumn.STAGE_POINTS].strip()),
            stage_place=parse_int_value(row[StageScoreColumn.STAGE_PLACE].strip()),
            stage_power_factor=parse_power_factor_default_none(row[StageScoreColumn.STAGE_POWER_FACTOR].strip()),
        )
        stages.append(stage)
    return stages
