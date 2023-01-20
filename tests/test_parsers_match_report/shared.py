from pytest import approx

from hitfactorpy.enums import Classification, Division, PowerFactor, Scoring
from hitfactorpy.parsers.match_report.models import ParsedMatchReport


def assert_example_match_report(report: ParsedMatchReport):
    """Assert the expected state of the report after sucessful parsing"""
    assert report
    assert report.name == "Paul Bunyan USPSA - January 2023 NW01"
    assert report.stages
    assert len(report.stages) == 7
    assert report.competitors
    assert len(report.competitors) == 72
    assert report.stage_scores
    assert len(report.stage_scores) == 494

    # Verify a stage
    assert report.stages[0].name == "A New Dawn"
    assert report.stages[0].min_rounds == 32
    assert report.stages[0].max_points == 160
    assert report.stages[0].classifier is False
    assert report.stages[0].internal_id == 1
    assert report.stages[0].scoring_type == Scoring.COMSTOCK
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
    assert report.stage_scores[0].dq is False
    assert report.stage_scores[0].dnf is False

    # Verify a stage score with a DQ
    assert report.stage_scores[37].dq is True
    assert report.stage_scores[37].dnf is False
    assert report.stage_scores[37].competitor_id == 38

    # Verify a stage score with a DNF
    assert report.stage_scores[69].dnf is True
    assert report.stage_scores[69].dq is False
    assert report.stage_scores[69].competitor_id == 70
