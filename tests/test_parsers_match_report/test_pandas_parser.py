import pytest

from hitfactorpy.parsers.match_report.pandas import parse_match_report
from hitfactorpy.parsers.match_report.pandas.dataframe import load_match_report_dataframes

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


def test_load_match_report_dataframes():
    dataframes = load_match_report_dataframes(EXAMPLE_REPORT)
    assert not dataframes.competitors.empty
    assert not dataframes.stages.empty
    assert not dataframes.stage_scores.empty
