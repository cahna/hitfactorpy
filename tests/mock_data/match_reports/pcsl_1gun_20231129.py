import datetime

from pytest import approx

from hitfactorpy.enums import Classification, Division, PowerFactor, Scoring
from hitfactorpy.parsers.match_report.models import ParsedMatchReport


def assert_pcsl_match_report_1gun_20231129(report: ParsedMatchReport):
    """Assert the expected state of the 1-gun 20231129 report"""
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
    assert len(report.competitors) == 5
    assert report.stage_scores
    assert len(report.stage_scores) == 13

    # Verify a stage
    assert report.stages[0].name == "Surefire"
    assert report.stages[0].min_rounds == 30
    assert report.stages[0].max_points == 150
    assert report.stages[0].classifier is False
    assert report.stages[0].classifier_number in ["nan", "", None]
    assert report.stages[0].internal_id == 1
    assert report.stages[0].scoring_type == Scoring.COMSTOCK
    assert report.stages[0].number == 1
    assert report.stages[0].gun_type == "Pistol"

    # Verify a competitor
    assert report.competitors[0].internal_id == 1
    assert report.competitors[0].first_name == "Person"
    assert report.competitors[0].last_name == "A"
    assert report.competitors[0].classification == Classification.UNKNOWN
    assert report.competitors[0].division == Division.UNKNOWN
    assert report.competitors[0].member_number == "NUMBER1"
    assert report.competitors[0].power_factor == PowerFactor.MINOR
    assert report.competitors[0].dq is False
    assert report.competitors[0].reentry is False

    # Verify DQ'ed competitor
    assert report.competitors[4].dq is True

    # Verify a stage score with a DQ
    assert report.stage_scores[-1].stage_id == 3
    assert report.stage_scores[-1].competitor_id == 4
    assert report.stage_scores[-1].a == 9
    assert report.stage_scores[-1].b == 0
    assert report.stage_scores[-1].c == 5
    assert report.stage_scores[-1].d == 0
    assert report.stage_scores[-1].m == 0
    assert report.stage_scores[-1].ns == 0
    assert report.stage_scores[-1].npm == 0
    assert report.stage_scores[-1].procedural == 0
    assert report.stage_scores[-1].late_shot == 0
    assert report.stage_scores[-1].extra_shot == 0
    assert report.stage_scores[-1].extra_hit == 0
    assert report.stage_scores[-1].other_penalty == 0
    assert report.stage_scores[-1].t1 == approx(9.43)
    assert report.stage_scores[-1].t2 == approx(0)
    assert report.stage_scores[-1].t3 == approx(0)
    assert report.stage_scores[-1].t4 == approx(0)
    assert report.stage_scores[-1].t5 == approx(0)
    assert report.stage_scores[-1].time == approx(9.43)
    assert report.stage_scores[-1].raw_points == approx(60)
    assert report.stage_scores[-1].penalty_points == approx(0)
    assert report.stage_scores[-1].total_points == approx(60)
    assert report.stage_scores[-1].hit_factor == approx(0)
    assert report.stage_scores[-1].stage_points == approx(0)
    assert report.stage_scores[-1].stage_place == 4
    assert report.stage_scores[-1].dq is True
    assert report.stage_scores[-1].dnf is False
    assert report.stage_scores[-1].stage_power_factor is None

    # Verify DQ'ed competitor exists in competitors list, and was DQ'ed
    dqed_competitor = next((c for c in report.competitors if c.internal_id == 4), None)
    assert dqed_competitor
    assert dqed_competitor.dq is True


assert_match_report = assert_pcsl_match_report_1gun_20231129
