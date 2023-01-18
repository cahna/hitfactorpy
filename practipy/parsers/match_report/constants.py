from enum import Enum, unique


@unique
class MatchReportSectionPrefix(str, Enum):
    INFO = "$INFO"
    COMPETITOR_HEADER = "D"
    COMPETITOR = "E"
    STAGE_HEADER = "F"
    STAGE = "G"
    STAGE_SCORE_HEADER = "H"
    STAGE_SCORE = "I"
