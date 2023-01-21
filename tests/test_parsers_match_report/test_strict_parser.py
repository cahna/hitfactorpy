import pytest

from hitfactorpy.parsers.match_report.strict import parse_match_report

from .mock_data import EXAMPLE_REPORT
from .shared import assert_example_match_report


def test_parse_match_report():
    assert (report := parse_match_report(EXAMPLE_REPORT))
    assert_example_match_report(report)


@pytest.mark.parametrize(
    "test_input",
    [
        "",
        "$PRACTISCORE",
        "$INFO",
        "$END",
        "$\nD",
        "$PRACTISCORE \n$INFO \nZ \nA \nD \nE \nF \nG \nH \nI \n$END" "",
    ],
)
def test_parse_match_report_nothing_parsed(test_input):
    report = parse_match_report(test_input)
    assert report
    assert report.name is None
    assert report.raw_date is None
    assert report.date is None
    assert report.match_level is None
    assert len(report.stages) == 0
    assert len(report.competitors) == 0
    assert len(report.stage_scores) == 0
