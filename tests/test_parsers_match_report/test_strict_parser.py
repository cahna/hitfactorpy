from practipy.parsers.match_report.strict import parse_match_report

from .mock_data import EXAMPLE_REPORT


def test_parse_match_report():
    report = parse_match_report(EXAMPLE_REPORT)
    assert report
    assert report.name == "Paul Bunyan USPSA - January 2023 NW01"
    assert report.stages
    assert len(report.stages) == 7
    assert report.competitors
    assert len(report.competitors) == 72
    assert report.stage_scores
    assert len(report.stage_scores) == 494
