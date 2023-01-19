from io import StringIO
from typing import NamedTuple

from pandas import DataFrame

from .competitor import read_competitors_csv
from .report_sections import parse_match_report_sections
from .stage import read_stages_csv
from .stage_score import read_stage_scores_csv


class MatchReportDataframes(NamedTuple):
    competitors: DataFrame
    stages: DataFrame
    stage_scores: DataFrame


def load_match_report_dataframes(report_text: str) -> MatchReportDataframes:
    """Parse each CSV section of the match report into dataframes"""
    sections = parse_match_report_sections(report_text)
    competitors = read_competitors_csv(StringIO(sections.competitors))
    stages = read_stages_csv(StringIO(sections.stages))
    stage_scores = read_stage_scores_csv(StringIO(sections.stage_scores))

    return MatchReportDataframes(competitors, stages, stage_scores)
