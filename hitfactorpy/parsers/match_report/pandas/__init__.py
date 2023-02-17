from ..match_info import parse_match_info
from ..models import ParsedMatchReport
from .competitor import parse_competitors
from .report_sections import parse_match_report_sections
from .stage import parse_stages
from .stage_score import parse_stage_scores


def parse_match_report(report_text: str) -> ParsedMatchReport:
    sections = parse_match_report_sections(report_text)
    match_info = parse_match_info(sections.info.split("\n"))
    competitors = parse_competitors(sections.competitors)
    stages = parse_stages(sections.stages)
    stage_scores = parse_stage_scores(sections.stage_scores)
    return ParsedMatchReport(
        name=match_info.name,
        raw_date=match_info.raw_date,
        date=match_info.date,
        match_level=match_info.match_level,
        platform=match_info.platform,
        ps_product=match_info.ps_product,
        ps_version=match_info.ps_version,
        club_code=match_info.club_code,
        club_name=match_info.club_name,
        region=match_info.region,
        competitors=competitors,
        stages=stages,
        stage_scores=stage_scores,
    )
