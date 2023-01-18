from enum import Enum, unique
from io import StringIO
from typing import Any, Callable, List, Mapping

import pandas as pd
from pandas._typing import FilePath, ReadCsvBuffer

from ..fields import parse_boolean, parse_scoring
from ..models import ParsedStage


@unique
class StageColumnName(str, Enum):
    ID = "index"
    MIN_ROUNDS = "Minimum Rounds"
    MAX_POINTS = "Maximum Points"
    CLASSIFIER = "Classifier"
    CLASSIFIER_NUM = "Classifier_No"
    STAGE_NAME = "Stage_name"
    SCORING = "ScoringType"


CONVERTERS: Mapping[str, Callable[[str], Any]] = {
    StageColumnName.SCORING: parse_scoring,
    StageColumnName.CLASSIFIER: parse_boolean,
}


def read_stage_csv(filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str]):
    df = pd.read_csv(
        filepath_or_buffer,
        index_col="Number",
        converters=CONVERTERS,
    )
    return df


def parse_stage_info(stage_csv_text: str) -> List[ParsedStage]:
    df = read_stage_csv(StringIO(stage_csv_text))
    stages = [
        ParsedStage(
            internal_id=internal_id,
            name=stage_name,
            scoring_type=scoring,
            min_rounds=min_rounds,
            max_points=max_points,
        )
        for internal_id, stage_name, scoring, min_rounds, max_points in zip(
            df.index,
            df[StageColumnName.STAGE_NAME],
            df[StageColumnName.SCORING],
            df[StageColumnName.MIN_ROUNDS],
            df[StageColumnName.MAX_POINTS],
        )
    ]
    # TODO: how to handle this edge case?
    #             scoring_type=parse_scoring(row[StageColumn.SCORING])
    #             if len(row) > StageColumn.SCORING
    #             else Scoring.COMSTOCK,
    return stages
