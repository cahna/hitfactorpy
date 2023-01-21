import pytest


def test_json_schema(cli_invoke):
    result = cli_invoke(["json-schema"])
    assert result.exit_code == 0
    assert result.stdout.lstrip().startswith("{")
    assert result.stdout.rstrip().endswith("}")


@pytest.mark.parametrize(
    "test_cli_args",
    [
        ["--model", "competitor"],
        ["--model", "stage"],
        ["--model", "stage-score"],
        ["--model", "competitor", "--title", "pytest-schema"],
    ],
)
def test_json_schema_options(test_cli_args, cli_invoke):
    result = cli_invoke(["json-schema", *test_cli_args])
    assert result.exit_code == 0
    assert result.stdout.lstrip().startswith("{")
    assert result.stdout.rstrip().endswith("}")
