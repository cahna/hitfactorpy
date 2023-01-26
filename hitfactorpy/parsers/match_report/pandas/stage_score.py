import logging
from enum import Enum, unique
from io import StringIO
from typing import Any, Callable, List, Mapping

import pandas as pd
from pandas._typing import FilePath, ReadCsvBuffer
from pandas.errors import EmptyDataError

from ..fields import parse_boolean, parse_power_factor_default_none
from ..models import ParsedStageScore

_logger = logging.getLogger(__name__)


@unique
class StageScoreColumnName(str, Enum):
    """Known competitor column names. May also includes dataframe references and custom columns added to the dataframe after parsing."""

    STAGE_ID = "Stage"
    COMPETITOR_ID = "Comp"
    DQ = "DQ"
    DNF = "DNF"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    M = "Miss"
    NS = "No Shoot"
    PROC = "Procedural"
    DOUBLE_POPPERS = "Double Poppers"
    DOUBLE_POPPER_MISS = "Double Popper Miss"
    LATE_SHOT = "Late Shot"
    EXTRA_SHOT = "Extra Shot"
    EXTRA_HIT = "Extra Hit"
    NPM = "No Penalty Miss"
    OTHER_PENALTY = "Additional Penalty"
    PENALTY_POINTS = "Total Penalty"
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"
    T4 = "T4"
    T5 = "T5"
    TIME = "Time"
    RAW_POINTS = "Raw Points"
    TOTAL_POINTS = "Total Points"
    HIT_FACTOR = "Hit Factor"
    STAGE_POINTS = "Stage Points"
    STAGE_PLACE = "Stage Place"
    STAGE_POWER_FACTOR = "Stage Power Factor"


CSV_CONVERTERS: Mapping[str, Callable[[str], Any]] = {
    StageScoreColumnName.DQ: parse_boolean,
    StageScoreColumnName.DNF: parse_boolean,
    StageScoreColumnName.STAGE_POWER_FACTOR: parse_power_factor_default_none,
}


def read_stage_scores_csv(filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str]):
    """Load a dataframe with stage scores as rows parsed from csv"""
    df = pd.read_csv(
        filepath_or_buffer,
        index_col=None,
        converters=CSV_CONVERTERS,
    )
    return df


def parse_stage_scores(stage_scores_csv: str) -> List[ParsedStageScore]:
    """Parse CSV text into ParsedStageScore objects. Uses pandas for parsing."""
    try:
        df = read_stage_scores_csv(StringIO(stage_scores_csv))
    except EmptyDataError:
        _logger.error("failed to parse stage_scores csv into dataframe")
        return []

    stage_scores = [
        ParsedStageScore(
            stage_id=stage_id,
            competitor_id=competitor_id,
            dq=dq,
            dnf=dnf,
            a=a,
            b=b,
            c=c,
            d=d,
            m=m,
            npm=npm,
            ns=ns,
            procedural=procedural,
            late_shot=late_shot,
            extra_shot=extra_shot,
            extra_hit=extra_hit,
            other_penalty=other_penalty,
            t1=t1,
            t2=t2,
            t3=t3,
            t4=t4,
            t5=t5,
            time=time,
            raw_points=raw_points,
            penalty_points=penalty_points,
            total_points=total_points,
            hit_factor=hit_factor,
            stage_points=stage_points,
            stage_place=stage_place,
            stage_power_factor=stage_power_factor,
        )
        for (
            stage_id,
            competitor_id,
            dq,
            dnf,
            a,
            b,
            c,
            d,
            m,
            npm,
            ns,
            procedural,
            late_shot,
            extra_shot,
            extra_hit,
            other_penalty,
            t1,
            t2,
            t3,
            t4,
            t5,
            time,
            raw_points,
            penalty_points,
            total_points,
            hit_factor,
            stage_points,
            stage_place,
            stage_power_factor,
        ) in zip(
            df[StageScoreColumnName.STAGE_ID],
            df[StageScoreColumnName.COMPETITOR_ID],
            df[StageScoreColumnName.DQ],
            df[StageScoreColumnName.DNF],
            df[StageScoreColumnName.A],
            df[StageScoreColumnName.B],
            df[StageScoreColumnName.C],
            df[StageScoreColumnName.D],
            df[StageScoreColumnName.M],
            df[StageScoreColumnName.NPM],
            df[StageScoreColumnName.NS],
            df[StageScoreColumnName.PROC],
            df[StageScoreColumnName.LATE_SHOT],
            df[StageScoreColumnName.EXTRA_SHOT],
            df[StageScoreColumnName.EXTRA_HIT],
            df[StageScoreColumnName.OTHER_PENALTY],
            df[StageScoreColumnName.T1],
            df[StageScoreColumnName.T2],
            df[StageScoreColumnName.T3],
            df[StageScoreColumnName.T4],
            df[StageScoreColumnName.T5],
            df[StageScoreColumnName.TIME],
            df[StageScoreColumnName.RAW_POINTS],
            df[StageScoreColumnName.PENALTY_POINTS],
            df[StageScoreColumnName.TOTAL_POINTS],
            df[StageScoreColumnName.HIT_FACTOR],
            df[StageScoreColumnName.STAGE_POINTS],
            df[StageScoreColumnName.STAGE_PLACE],
            df[StageScoreColumnName.STAGE_POWER_FACTOR],
        )
    ]
    return stage_scores
