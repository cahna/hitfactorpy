from datetime import datetime
from typing import List, Optional

from pydantic.dataclasses import dataclass

from ...enums import Classification, Division, MatchLevel, PowerFactor, Scoring


@dataclass(frozen=True)
class ParsedCompetitor:
    """Competitor info parsed from match report"""

    internal_id: int
    member_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    division: Optional[Division] = None
    classification: Optional[Classification] = None
    power_factor: Optional[PowerFactor] = None
    dq: bool = False
    reentry: bool = False


@dataclass(frozen=True)
class ParsedStage:
    """Stage info parsed from match report"""

    internal_id: int
    name: Optional[str] = None
    min_rounds: Optional[int] = 0
    max_points: Optional[int] = 0
    classifier: bool = False
    classifier_number: Optional[str] = None
    scoring_type: Scoring = Scoring.COMSTOCK


@dataclass(frozen=True)
class ParsedStageScore:
    """Stage score parsed from match report"""

    stage_id: Optional[int] = None
    competitor_id: Optional[int] = None
    dq: bool = False
    dnf: bool = False
    a: int = 0
    b: int = 0
    c: int = 0
    d: int = 0
    m: int = 0
    npm: int = 0
    ns: int = 0
    procedural: int = 0
    late_shot: int = 0
    extra_shot: int = 0
    extra_hit: int = 0
    other_penalty: int = 0
    t1: float = 0.0
    t2: float = 0.0
    t3: float = 0.0
    t4: float = 0.0
    t5: float = 0.0
    time: float = 0.0
    raw_points: Optional[float] = None
    penalty_points: Optional[float] = None
    total_points: Optional[float] = None
    hit_factor: Optional[float] = None
    stage_points: Optional[float] = None
    stage_place: Optional[int] = None
    stage_power_factor: Optional[PowerFactor] = None


@dataclass(frozen=True)
class ParsedMatchInfo:
    """Match info parsed from header of match report"""

    name: Optional[str] = None
    raw_date: Optional[str] = None
    date: Optional[datetime] = None
    match_level: Optional[MatchLevel] = None
    region: Optional[str] = None
    ps_product: Optional[str] = None
    ps_version: Optional[str] = None
    platform: Optional[str] = None
    club_name: Optional[str] = None
    club_code: Optional[str] = None


@dataclass(frozen=True)
class ParsedMatchReport(ParsedMatchInfo):
    """All data that could be parsed from the match report"""

    competitors: Optional[List[ParsedCompetitor]] = None
    stages: Optional[List[ParsedStage]] = None
    stage_scores: Optional[List[ParsedStageScore]] = None
