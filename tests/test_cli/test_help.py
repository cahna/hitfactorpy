def test_help(cli_invoke):
    result = cli_invoke(["--help"])
    assert result.exit_code == 0
    assert result.stdout.lstrip().startswith("Usage:")
