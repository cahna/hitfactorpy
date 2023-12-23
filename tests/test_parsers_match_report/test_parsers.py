import pytest

from hitfactorpy.parsers.match_report.pandas import parse_match_report as parse_match_report_pandas
from hitfactorpy.parsers.match_report.pandas.dataframe import load_match_report_dataframes
from hitfactorpy.parsers.match_report.strict import parse_match_report as parse_match_report_strict

from ..mock_data import match_reports


@pytest.mark.parametrize(
    "match_report_file,validate_report_fn",
    [*match_reports.VALIDATORS.items()],
)
@pytest.mark.parametrize("parser_fn", [parse_match_report_pandas, parse_match_report_strict])
def test_parse_match_report(match_report_file, validate_report_fn, parser_fn):
    file_contents = match_reports.BY_FILENAME[match_report_file]
    report = parser_fn(file_contents)
    assert report
    validate_report_fn(report)


@pytest.mark.parametrize(
    "test_input",
    [
        pytest.param("", id="empty-string"),
        "$PRACTISCORE",
        "$INFO",
        "$END",
        "$\nD",
        pytest.param("$PRACTISCORE \n$INFO \nZ \nA \nD \nE \nF \nG \nH \nI \n$END", id="empty-report-with-markers"),
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


@pytest.mark.parametrize("match_report_file", [*match_reports.BY_FILENAME.keys()])
def test_load_match_report_dataframes(match_report_file):
    dataframes = load_match_report_dataframes(match_reports.BY_FILENAME[match_report_file])
    assert not dataframes.competitors.empty
    assert not dataframes.stages.empty
    assert not dataframes.stage_scores.empty
