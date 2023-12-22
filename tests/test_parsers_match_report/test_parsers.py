import pytest

from hitfactorpy.parsers.match_report.pandas import parse_match_report as parse_match_report_pandas
from hitfactorpy.parsers.match_report.pandas.dataframe import load_match_report_dataframes
from hitfactorpy.parsers.match_report.strict import parse_match_report as parse_match_report_strict

from .mock_data import EXAMPLE_REPORT
from .shared import (
    assert_example_uspsa_match_report,
    assert_pcsl_match_report_1gun_20231129,
    assert_pcsl_match_report_2gun_20231129,
)


@pytest.mark.parametrize(
    "match_report_file,validate_report_fn",
    [
        ("uspsa_match_reports/20230108.txt", assert_example_uspsa_match_report),
        ("uspsa_match_reports/20230108.txt", assert_example_uspsa_match_report),
        ("pcsl_match_reports/2gun/20231129.txt", assert_pcsl_match_report_2gun_20231129),
        ("pcsl_match_reports/1gun/20231129.txt", assert_pcsl_match_report_1gun_20231129),
        ("pcsl_match_reports/2gun/20231129.txt", assert_pcsl_match_report_2gun_20231129),
        ("pcsl_match_reports/1gun/20231129.txt", assert_pcsl_match_report_1gun_20231129),
    ],
)
@pytest.mark.parametrize("parser_fn", [parse_match_report_pandas, parse_match_report_strict])
def test_parse_match_report(match_report_file, validate_report_fn, parser_fn, mock_data_file):
    mock_file_path = mock_data_file(match_report_file)
    with open(mock_file_path) as f:
        report = parser_fn(f.read())
    assert report
    validate_report_fn(report)


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
@pytest.mark.parametrize("parser_fn", [parse_match_report_pandas, parse_match_report_strict])
def test_parse_match_report_nothing_parsed(test_input, parser_fn):
    report = parser_fn(test_input)
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
