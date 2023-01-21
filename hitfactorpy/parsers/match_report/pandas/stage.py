import logging
from enum import Enum, unique
from io import StringIO
from typing import Any, Callable, List, Mapping

import pandas as pd
from pandas._typing import FilePath, ReadCsvBuffer
from pandas.errors import EmptyDataError

from ..fields import parse_boolean, parse_scoring
from ..models import ParsedStage

_logger = logging.getLogger(__name__)


@unique
class StageColumnName(str, Enum):
    """Known competitor column names. May also include dataframe references and custom columns added to the dataframe after parsing."""

    ID = "index"  # ex: used to reference `df.index`
    MIN_ROUNDS = "Minimum Rounds"
    MAX_POINTS = "Maximum Points"
    CLASSIFIER = "Classifier"
    CLASSIFIER_NUM = "Classifier_No"
    STAGE_NAME = "Stage_name"
    SCORING = "ScoringType"


CSV_CONVERTERS: Mapping[str, Callable[[str], Any]] = {
    StageColumnName.SCORING: parse_scoring,
    StageColumnName.CLASSIFIER: parse_boolean,
}


def read_stages_csv(filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str]):
    """Load a dataframe with stages parsed from csv"""
    df = pd.read_csv(
        filepath_or_buffer,
        index_col="Number",
        converters=CSV_CONVERTERS,
    )
    return df


def parse_stages(stage_csv_text: str) -> List[ParsedStage]:
    """Parse CSV text into ParsedStage objects. Uses pandas for parsing."""
    try:
        df = read_stages_csv(StringIO(stage_csv_text))
    except EmptyDataError:
        _logger.error("failed to parse stages csv into dataframe")
        return []

    stages = [
        ParsedStage(
            internal_id=internal_id,
            name=stage_name,
            scoring_type=scoring,
            min_rounds=min_rounds,
            max_points=max_points,
            classifier=classifier,
            classifier_number=classifier_number,
        )
        for internal_id, stage_name, scoring, min_rounds, max_points, classifier, classifier_number in zip(
            df.index,
            df[StageColumnName.STAGE_NAME],
            df[StageColumnName.SCORING],
            df[StageColumnName.MIN_ROUNDS],
            df[StageColumnName.MAX_POINTS],
            df[StageColumnName.CLASSIFIER],
            df[StageColumnName.CLASSIFIER_NUM],
        )
    ]
    # TODO: how to handle this edge case?
    #             scoring_type=parse_scoring(row[StageColumn.SCORING])
    #             if len(row) > StageColumn.SCORING
    #             else Scoring.COMSTOCK,
    return stages
