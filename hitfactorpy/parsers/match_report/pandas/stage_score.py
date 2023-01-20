import logging
from enum import Enum, unique
from io import StringIO
from typing import Any, Callable, List, Mapping

import pandas as pd
from pandas._typing import FilePath, ReadCsvBuffer
from pandas.errors import EmptyDataError

from ..fields import parse_boolean, parse_power_factor
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
    STAGE_POWER_FACTOR = "Stage Power Factor"


CSV_CONVERTERS: Mapping[str, Callable[[str], Any]] = {
    StageScoreColumnName.DQ: parse_boolean,
    StageScoreColumnName.DNF: parse_boolean,
    StageScoreColumnName.STAGE_POWER_FACTOR: parse_power_factor,
}


def read_stage_scores_csv(filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str]):
    """Load a dataframe with stage scores as rows parsed from csv"""
    df = pd.read_csv(
        filepath_or_buffer,
        index_col=None,
        converters=CSV_CONVERTERS,
    )
    # df['hit_factor'] = (df['A'] * 5) # TODO
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
            dq=dq,
            dnf=dnf,
        )
        for (
            stage_id,
            competitor_id,
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
            dq,
            dnf,
        ) in zip(
            df[StageScoreColumnName.STAGE_ID],
            df[StageScoreColumnName.COMPETITOR_ID],
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
            df[StageScoreColumnName.DQ],
            df[StageScoreColumnName.DNF],
        )
    ]
    return stage_scores
