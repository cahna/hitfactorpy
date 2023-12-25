import datetime

from pytest import approx

from hitfactorpy.enums import Classification, Division, PowerFactor, Scoring
from hitfactorpy.parsers.match_report.models import ParsedMatchReport


def assert_pcsl_match_report_2gun_20231129(report: ParsedMatchReport):
    """Assert the expected state of the 2-gun 20231129 report"""
    assert report
    assert report.name == "matchName"
    assert report.match_level == 1
    assert report.platform == "IOS"
    assert report.ps_product == "PractiScore (iOS)"
    assert report.ps_version == "1.682"
    assert report.club_name == "clubName"
    assert report.club_code == "clubCode"
    assert report.region == "USPSA"
    assert report.raw_date == "11/29/2023"
    assert report.date == datetime.datetime(2023, 11, 29, 0, 0)
    assert report.stages
    assert len(report.stages) == 3
    assert report.competitors
    assert len(report.competitors) == 3
    assert report.stage_scores
    assert len(report.stage_scores) == 8

    # Verify a stage
    assert report.stages[0].name == "Surefire"
    assert report.stages[0].min_rounds == 54
    assert report.stages[0].max_points == 270
    assert report.stages[0].classifier is False
    assert report.stages[0].classifier_number in ["nan", "", None]
    assert report.stages[0].internal_id == 1
    assert report.stages[0].scoring_type == Scoring.COMSTOCK
    assert report.stages[0].number == 1
    assert report.stages[0].gun_type == "Pistol"

    # Verify a competitor
    assert report.competitors[1].internal_id == 2
    assert report.competitors[1].first_name == "Person"
    assert report.competitors[1].last_name == "B"
    assert report.competitors[1].classification == Classification.UNKNOWN
    assert report.competitors[1].division == Division.UNKNOWN
    assert report.competitors[1].member_number == "NUMBER2"
    assert report.competitors[1].power_factor == PowerFactor.MINOR
    assert report.competitors[1].dq is False
    assert report.competitors[1].reentry is False

    # Verify no DQ'ed competitors exist in this report
    assert report.competitors[-1].dq is True

    # Verify a stage score
    assert report.stage_scores[1].stage_id == 1
    assert report.stage_scores[1].competitor_id == 2
    assert report.stage_scores[1].a == 45
    assert report.stage_scores[1].b == 0
    assert report.stage_scores[1].c == 9
    assert report.stage_scores[1].d == 0
    assert report.stage_scores[1].m == 0
    assert report.stage_scores[1].ns == 0
    assert report.stage_scores[1].npm == 0
    assert report.stage_scores[1].procedural == 0
    assert report.stage_scores[1].late_shot == 0
    assert report.stage_scores[1].extra_shot == 0
    assert report.stage_scores[1].extra_hit == 0
    assert report.stage_scores[1].other_penalty == 0
    assert report.stage_scores[1].t1 == approx(49.21)
    assert report.stage_scores[1].t2 == approx(0)
    assert report.stage_scores[1].t3 == approx(0)
    assert report.stage_scores[1].t4 == approx(0)
    assert report.stage_scores[1].t5 == approx(0)
    assert report.stage_scores[1].time == approx(49.21)
    assert report.stage_scores[1].raw_points == approx(252)
    assert report.stage_scores[1].penalty_points == approx(0)
    assert report.stage_scores[1].total_points == approx(252)
    assert report.stage_scores[1].hit_factor == approx(5.1209)
    assert report.stage_scores[1].stage_points == approx(248.82)
    assert report.stage_scores[1].stage_place == 2
    assert report.stage_scores[1].dq is False
    assert report.stage_scores[1].dnf is False
    assert report.stage_scores[1].stage_power_factor is None


assert_match_report = assert_pcsl_match_report_2gun_20231129
