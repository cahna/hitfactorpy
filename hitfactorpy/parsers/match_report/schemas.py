from pydantic.dataclasses import dataclass as pydanticdataclass

from .models import ParsedCompetitor, ParsedMatchReport, ParsedStage, ParsedStageScore

Competitor = pydanticdataclass(ParsedCompetitor, frozen=True)

Stage = pydanticdataclass(ParsedStage, frozen=True)

StageScore = pydanticdataclass(ParsedStageScore, frozen=True)

MatchReport = pydanticdataclass(ParsedMatchReport, frozen=True)
