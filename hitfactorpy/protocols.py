from datetime import datetime
from typing import List, Optional, Protocol

from .enums import MatchLevel, Scoring


class CompetitorAttributes(Protocol):
    """
    Required attributes of a competitor object
    """

    first_name: str
    last_name: str


class StageAttributes(Protocol):
    """
    Required attributes of a stage object
    """

    name: str
    is_classifier: bool
    classifier_number: Optional[str]
    scoring: Scoring


class MatchAttributes(Protocol):
    """
    Required attributes of a stage object
    """

    name: str
    raw_date: str
    date: datetime
    match_level: MatchLevel
    practiscore_id: str
    report_contents: str
    competitors: List[CompetitorAttributes]
    stages: List[StageAttributes]
