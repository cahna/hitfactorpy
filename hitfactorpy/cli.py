import json
from enum import Enum, unique
from pathlib import Path
from typing import Any, NamedTuple, Optional

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
    match_report_file: Path, json_indent: Optional[int] = None, parser: MatchParserOption = MatchParserOption.PANDAS
):
    """
    Parse a match report file into JSON
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
    COMPETITOR = "competitor"
    STAGE = "stage"
    STAGE_SCORE = "stage-score"


@cli.command()
def json_schema(model: JsonSchemaModelArgument = JsonSchemaModelArgument.MATCH_REPORT, title: Optional[str] = None):
    """
    Dump the JSON Schema for a model
    """
    from hitfactorpy.parsers.match_report import models

    class ModelConfig(NamedTuple):
        """A model and its default title"""

        model: Any
        title: str

    models_config = {
        JsonSchemaModelArgument.MATCH_REPORT: ModelConfig(models.ParsedMatchReport, "MatchReport Schema"),
        JsonSchemaModelArgument.COMPETITOR: ModelConfig(models.ParsedCompetitor, "Competitor Schema"),
        JsonSchemaModelArgument.STAGE: ModelConfig(models.ParsedStage, "Stage schema"),
        JsonSchemaModelArgument.STAGE_SCORE: ModelConfig(models.ParsedStageScore, "StageScore Schema"),
    }
    config = models_config[model]

    typer.echo(schema_json_of(config.model, title=title or config.title))


if __name__ == "__main__":
    cli()
