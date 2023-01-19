from enum import Enum, unique


@unique
class MatchReportSectionPrefix(str, Enum):
    PS = "$PRACTISCORE"
    INFO = "$INFO"
    COMPETITOR_HEADER = "D"
    COMPETITOR = "E"
    STAGE_HEADER = "F"
    STAGE = "G"
    STAGE_SCORE_HEADER = "H"
    STAGE_SCORE = "I"


@unique
class MatchReportInfoSectionFields(str, Enum):
    """Fields in the $INFO section that can be parsed via a single split on ':'"""

    MATCH_NAME = "Match name"
    MATCH_DATE = "Match date"
    MATCH_LEVEL = "Match Level"
    REGION = "Region"
    CLUB_NAME = "Club Name"
    CLUB_CODE = "Club Code"
    PS_PRODUCT = "PractiScore_Product"
    PS_VERSION = "PractiScore_Version"
