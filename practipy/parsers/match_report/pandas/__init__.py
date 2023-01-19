from ..match_info import parse_match_info
from ..models import ParsedMatchReport
from .competitor import parse_competitors
from .report_lines import parse_match_report_response_lines
from .stage import parse_stages
from .stage_score import parse_stage_scores


def parse_match_report(report_text: str) -> ParsedMatchReport:
    report_lines = parse_match_report_response_lines(report_text)
    match_info = parse_match_info(report_lines.info)
    competitor_csv = f"{report_lines.competitor_columns[0]}\n" + "\n".join(report_lines.competitor)
    competitors = parse_competitors(competitor_csv)
    stage_csv = f"{report_lines.stage_columns[0]}\n" + "\n".join(report_lines.stage)
    stages = parse_stages(stage_csv)
    stage_scores_csv = f"{report_lines.stage_score_columns[0]}\n" + "\n".join(report_lines.stage_score)
    stage_scores = parse_stage_scores(stage_scores_csv)
    return ParsedMatchReport(
        name=match_info.name,
        raw_date=match_info.raw_date,
        date=match_info.date,
        match_level=match_info.match_level,
        competitors=competitors,
        stages=stages,
        stage_scores=stage_scores,
    )
