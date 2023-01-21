from ..test_parsers_match_report.mock_data import EXAMPLE_REPORT


def test_parse_match_default(cli_invoke, tmp_path):
    match_file = tmp_path / "test-match.txt"
    match_file.write_text(EXAMPLE_REPORT)
    result = cli_invoke(["parse-match", str(match_file)])
    assert result.exit_code == 0
    assert result.stdout.lstrip().startswith("{")
    assert result.stdout.rstrip().endswith("}")


def test_parse_match_pandas(cli_invoke, tmp_path):
    match_file = tmp_path / "test-match1.txt"
    match_file.write_text(EXAMPLE_REPORT)
    result = cli_invoke(["parse-match", str(match_file), "--parser=pandas"])
    assert result.exit_code == 0
    assert result.stdout.lstrip().startswith("{")
    assert result.stdout.rstrip().endswith("}")


def test_parse_match_strict(cli_invoke, tmp_path):
    match_file = tmp_path / "test-match2.txt"
    match_file.write_text(EXAMPLE_REPORT)
    result = cli_invoke(["parse-match", str(match_file), "--parser=strict"])
    assert result.exit_code == 0
    assert result.stdout.lstrip().startswith("{")
    assert result.stdout.rstrip().endswith("}")
