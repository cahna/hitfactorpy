import logging
from enum import Enum, unique
from io import StringIO
from typing import Any, Callable, List, Mapping

import pandas as pd
from pandas._typing import FilePath, ReadCsvBuffer
from pandas.errors import EmptyDataError

from ..fields import parse_boolean, parse_classification, parse_division, parse_member_number, parse_power_factor
from ..models import ParsedCompetitor

_logger = logging.getLogger(__name__)


@unique
class CompetitorColumnName(str, Enum):
    """Known competitor column names. Also includes dataframe references and custom columns added to the dataframe."""

    ID = "index"
    MEMBER_NUM = "USPSA"
    FIRST_NAME = "FirstName"
    LAST_NAME = "LastName"
    DQ_PISTOL = "DQPistol"
    DQ_RIFLE = "DQRifle"
    DQ_SHOTGUN = "DQShotgun"
    REENTRY = "Reentry"
    CLASS = "Class"
    DIVISION = "Division"
    POWER_FACTOR = "Power Factor"

    # Below this line are custom columns added to the pandas dataframe
    IS_DQ = "is_dq"


CONVERTERS: Mapping[str, Callable[[str], Any]] = {
    CompetitorColumnName.MEMBER_NUM: parse_member_number,
    CompetitorColumnName.DIVISION: parse_division,
    CompetitorColumnName.CLASS: parse_classification,
    CompetitorColumnName.POWER_FACTOR: parse_power_factor,
    CompetitorColumnName.REENTRY: parse_boolean,
    CompetitorColumnName.DQ_PISTOL: parse_boolean,
    CompetitorColumnName.DQ_RIFLE: parse_boolean,
    CompetitorColumnName.DQ_SHOTGUN: parse_boolean,
}


def read_competitors_csv(filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str]):
    """Load a dataframe with competitor rows parsed from csv"""
    df = pd.read_csv(
        filepath_or_buffer,
        index_col="Comp",
        converters=CONVERTERS,
    )
    df[CompetitorColumnName.IS_DQ] = (
        df[CompetitorColumnName.DQ_PISTOL] | df[CompetitorColumnName.DQ_RIFLE] | df[CompetitorColumnName.DQ_SHOTGUN]
    )
    return df


def parse_competitors(competitor_csv_text: str) -> List[ParsedCompetitor]:
    """Parse CSV text into ParsedCompetitor objects. Uses pandas for parsing."""
    try:
        df = read_competitors_csv(StringIO(competitor_csv_text))
    except EmptyDataError:
        _logger.error("failed to parse competitors csv into dataframe")
        return []

    competitors = [
        ParsedCompetitor(
            internal_id=internal_id,
            member_number=member_number,
            first_name=first_name,
            last_name=last_name,
            division=division,
            classification=classification,
            power_factor=power_factor,
            reentry=reentry,
            dq=dq,
        )
        for internal_id, member_number, first_name, last_name, classification, division, power_factor, reentry, dq in zip(
            df.index,
            df[CompetitorColumnName.MEMBER_NUM],
            df[CompetitorColumnName.FIRST_NAME],
            df[CompetitorColumnName.LAST_NAME],
            df[CompetitorColumnName.CLASS],
            df[CompetitorColumnName.DIVISION],
            df[CompetitorColumnName.POWER_FACTOR],
            df[CompetitorColumnName.REENTRY],
            df[CompetitorColumnName.IS_DQ],
        )
    ]

    return competitors
