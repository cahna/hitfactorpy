import pytest

from ..mock_data import match_reports


@pytest.mark.parametrize("match_report_file", [*match_reports.BY_FILENAME.keys()])
@pytest.mark.parametrize(
    "cmd_args",
    [
        pytest.param([], id="default"),
        pytest.param(["--parser=pandas"], id="opt-parser-pandas"),
        pytest.param(["--parser=strict"], id="opt-parser-strict"),
    ],
)
def test_cli_parse_match(match_report_file, cmd_args, cli_invoke, tmp_path):
    match_file = tmp_path / "test-match.txt"
    match_file.write_text(match_reports.BY_FILENAME[match_report_file])
    result = cli_invoke(["parse-match", str(match_file), *cmd_args])
    assert result.exit_code == 0
    assert result.stdout.lstrip().startswith("{")
    assert result.stdout.rstrip().endswith("}")
