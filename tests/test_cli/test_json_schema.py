from ..test_parsers_match_report.mock_data import EXAMPLE_REPORT


def test_json_schema(cli_invoke):
    result = cli_invoke(["json-schema"])
    assert result.exit_code == 0
    assert result.stdout.lstrip().startswith("{")
    assert result.stdout.rstrip().endswith("}")
