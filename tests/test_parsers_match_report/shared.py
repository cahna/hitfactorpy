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


def assert_example_uspsa_match_report(report: ParsedMatchReport):
    """Assert the expected state of the report after sucessful parsing"""
    assert report
    assert report.name == "Paul Bunyan USPSA - January 2023 NW01"
    assert report.stages
    assert len(report.stages) == 7
    assert report.competitors
    assert len(report.competitors) == 72
    assert report.stage_scores
    assert len(report.stage_scores) == 494
    assert report.platform == "IOS"
    assert report.ps_product
    assert report.ps_version == "1.682"
    assert report.club_name == "PaulBunyan"
    assert report.club_code == "PB"

    # Verify a stage
    assert report.stages[0].name == "A New Dawn"
    assert report.stages[0].min_rounds == 32
    assert report.stages[0].max_points == 160
    assert report.stages[0].classifier is False
    assert report.stages[0].internal_id == 1
    assert report.stages[0].scoring_type == Scoring.COMSTOCK
    assert report.stages[0].number == 1
    assert report.stages[0].gun_type == "Pistol"

    assert report.stages[2].name == "CM 22-06 Blue's Don't Care"

    # Verify a classifier stage
    assert report.stages[2].classifier is True
    assert report.stages[2].classifier_number == "22-06"
    assert report.stages[2].internal_id == 3

    # Verify a competitor
    assert report.competitors[0].internal_id == 1
    assert report.competitors[0].first_name == "Emily"
    assert report.competitors[0].last_name == "Smith"
    assert report.competitors[0].classification == Classification.M
    assert report.competitors[0].division == Division.CARRY_OPTICS
    assert report.competitors[0].member_number == "L4898"
    assert report.competitors[0].power_factor == PowerFactor.MINOR
    assert report.competitors[0].dq is False
    assert report.competitors[0].reentry is False

    # Verify DQ'ed competitor
    assert report.competitors[37].dq is True
    assert report.competitors[70].dq is True

    # Verify weird/missing member numbers
    assert report.competitors[1].member_number == "TY104096"
    assert report.competitors[17].member_number == "L1770NO"
    assert report.competitors[26].member_number == ""
    assert report.competitors[60].member_number == "B49"

    # Verify a stage score
    assert report.stage_scores[0].stage_id == 1
    assert report.stage_scores[0].competitor_id == 1
    assert report.stage_scores[0].a == 27
    assert report.stage_scores[0].b == 0
    assert report.stage_scores[0].c == 5
    assert report.stage_scores[0].d == 0
    assert report.stage_scores[0].m == 0
    assert report.stage_scores[0].ns == 0
    assert report.stage_scores[0].npm == 0
    assert report.stage_scores[0].procedural == 0
    assert report.stage_scores[0].late_shot == 0
    assert report.stage_scores[0].extra_shot == 0
    assert report.stage_scores[0].extra_hit == 0
    assert report.stage_scores[0].other_penalty == 0
    assert report.stage_scores[0].t1 == approx(17.34)
    assert report.stage_scores[0].t2 == approx(0)
    assert report.stage_scores[0].t3 == approx(0)
    assert report.stage_scores[0].t4 == approx(0)
    assert report.stage_scores[0].t5 == approx(0)
    assert report.stage_scores[0].time == approx(17.34)
    assert report.stage_scores[0].raw_points == approx(150.0)
    assert report.stage_scores[0].penalty_points == approx(0)
    assert report.stage_scores[0].total_points == approx(150.0)
    assert report.stage_scores[0].hit_factor == approx(8.6505)
    assert report.stage_scores[0].stage_points == approx(160.0)
    assert report.stage_scores[0].stage_place == 1
    assert report.stage_scores[0].dq is False
    assert report.stage_scores[0].dnf is False
    assert report.stage_scores[0].stage_power_factor is None

    # Verify a stage score with a DQ
    assert report.stage_scores[37].dq is True
    assert report.stage_scores[37].dnf is False
    assert next(
        (c for c in report.competitors if c.internal_id == report.stage_scores[37].competitor_id), None
    ), "DQ'ed competitor not found in competitors list"

    # Verify a stage score with a DNF
    assert report.stage_scores[69].dnf is True
    assert report.stage_scores[69].dq is False
    assert report.stage_scores[69].competitor_id == 70
