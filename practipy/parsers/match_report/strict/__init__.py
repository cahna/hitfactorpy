from ..match_info import parse_match_info
from ..models import ParsedMatchReport
from .competitor import parse_match_report_competitor_column_lines, parse_match_report_competitor_lines
from .report_lines import parse_match_report_response_lines
from .stage import parse_match_report_stage_column_lines, parse_match_report_stage_lines
from .stage_score import parse_match_report_stage_score_lines


def parse_match_report(report_text: str) -> ParsedMatchReport:
    report_lines = parse_match_report_response_lines(report_text)
    match_info = parse_match_info(report_lines.info)
    competitor_columns = parse_match_report_competitor_column_lines(report_lines.competitor_columns)
    competitors = parse_match_report_competitor_lines(report_lines.competitor, competitor_columns)
    stage_columns = parse_match_report_stage_column_lines(report_lines.stage_columns)
    stages = parse_match_report_stage_lines(report_lines.stage, stage_columns)
    stage_scores = parse_match_report_stage_score_lines(report_lines.stage_score)
    return ParsedMatchReport(
        name=match_info.name,
        raw_date=match_info.raw_date,
        date=match_info.date,
        match_level=match_info.match_level,
        competitors=competitors,
        stages=stages,
        stage_scores=stage_scores,
    )
