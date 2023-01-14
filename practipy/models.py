from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .enums import MatchLevel, Scoring


@dataclass
class Competitor:
    first_name: str
    last_name: str


@dataclass
class Stage:
    name: str
    is_classifier: bool
    classifier_number: Optional[str]
    scoring: Scoring


@dataclass
class MatchReport:
    name: str
    raw_date: str
    date: datetime
    match_level: MatchLevel
    practiscore_id: str
    report_contents: str
    competitors: List[Competitor]
    stages: List[Stage]
