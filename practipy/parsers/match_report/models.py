from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ...enums import Classification, Division, MatchLevel, PowerFactor, Scoring


@dataclass(frozen=True)
class ParsedCompetitor:
    internal_id: int
    member_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    division: Optional[Division] = None
    classification: Optional[Classification] = None
    power_factor: Optional[PowerFactor] = None
    dq: bool = field(default_factory=lambda: False)
    reentry: bool = field(default_factory=lambda: False)


@dataclass(frozen=True)
class ParsedStage:
    internal_id: int
    name: Optional[str] = None
    min_rounds: Optional[int] = 0
    max_points: Optional[int] = 0
    classifier: bool = field(default_factory=lambda: False)
    classifier_number: Optional[str] = None
    scoring_type: Scoring = Scoring.COMSTOCK


@dataclass(frozen=True)
class ParsedStageScore:
    competitor_id: Optional[int] = None
    stage_id: Optional[int] = None
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


@dataclass(frozen=True)
class ParsedMatchInfo:
    name: Optional[str] = None
    raw_date: Optional[str] = None
    date: Optional[datetime] = None
    match_level: Optional[MatchLevel] = None


@dataclass(frozen=True)
class ParsedMatchReport(ParsedMatchInfo):
    competitors: Optional[List[ParsedCompetitor]] = None
    stages: Optional[List[ParsedStage]] = None
    stage_scores: Optional[List[ParsedStageScore]] = None
