import json
from enum import Enum, unique
from pathlib import Path

import typer
from pydantic import schema_json_of
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


@unique
class JsonSchemaModelArgument(str, Enum):
    MATCH_REPORT = "match"


@cli.command()
def json_schema(
    model: JsonSchemaModelArgument = JsonSchemaModelArgument.MATCH_REPORT, title: str = "MatchReport Schema"
):
    """
    Dump the JSON Schema for a model
    """
    if model == JsonSchemaModelArgument.MATCH_REPORT:
        from hitfactorpy.parsers.match_report.models import ParsedMatchReport

        typer.echo(schema_json_of(ParsedMatchReport, title=title))


if __name__ == "__main__":
    cli()
