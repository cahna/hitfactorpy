import json
from enum import Enum, unique
from pathlib import Path

import typer
from pydantic.json import pydantic_encoder

CLI_NAME = "hitfactorpy"

cli = typer.Typer()


@unique
class MatchParserOption(str, Enum):
    PANDAS = "pandas"
    STRICT = "strict"


@cli.command()
def parse_match(
    match_report_file: Path, json_indent: int | None = None, parser: MatchParserOption = MatchParserOption.PANDAS
):
    """
    Parse a match report file
    """
    if parser == MatchParserOption.PANDAS:
        from hitfactorpy.parsers.match_report.pandas import parse_match_report
    else:
        from hitfactorpy.parsers.match_report.strict import parse_match_report  # type:ignore

    with open(match_report_file, "r") as f:
        report_text = f.read()

    report = parse_match_report(report_text)
    typer.echo(json.dumps(report, indent=json_indent, default=pydantic_encoder))


if __name__ == "__main__":
    cli()
