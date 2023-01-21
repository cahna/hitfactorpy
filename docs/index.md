# hitfactorpy

[![Main](https://github.com/cahna/hitfactorpy/actions/workflows/main.yaml/badge.svg)](https://github.com/cahna/hitfactorpy/actions/workflows/main.yaml)

Python tools for parsing and analyzing practical match reports.

## Status

**Work in progress...**

Documentation website: [https:/cahna.github.io/hitfactorpy](https:/cahna.github.io/hitfactorpy)

## Library usage

See parsers available in [`hitfactorpy.parsers.match_report`](https://github.com/cahna/hitfactorpy/tree/main/hitfactorpy/parsers/match_report) and examples in [repository's `tests` directory](https://github.com/cahna/hitfactorpy/tree/main/tests).

## CLI Usage

After installing, run the `hitfactorpy` command should be added to `$PATH`.

```console
$ hitfactorpy --help
```

Or:

<div class="termy">

```console
$ python -m hitfactorpy --help

Usage: hitfactorpy [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, ...
  --help                Show this message and exit.

Commands:
  json-schema  Dump the JSON Schema for a model  
  parse-match  Parse a match report file into JSON

```

</div>

### Command: `parse-match`

<div class="termy">

```console
$ hitfactorpy parse-match ./report.txt --json-indent 2
{
    "name": "Paul Bunyan USPSA - January 2023 NW01",
    "raw_date": "01/08/2023",
    "date": "2023-01-08T00:00:00",
    "match_level": 1,
    "competitors": [ 
# ...
```

</div>

### Command: `json-schema`

Default use:

```console
$ hitfactorpy json-schema
```

Output JSON Schema for a specific model and override the title:

<div class="termy">

```console
$ hitfactorpy json-schema --model stage --title "My Custom-Titled Schema"
{"title": "My Custom-Titled Schema", "$ref": "#/definitions/ParsedStage", "definitions": {"Scoring": {"title": "Scoring", "description": "An enumeration.", "enum": ["comstock", "virginia", "fixedTime", "chrono", "unknown"], "type": "string"}, "ParsedStage": {"title": "ParsedStage", "description": "Stage info parsed from match report", "type": "object", "properties": {"internal_id": {"title": "Internal Id", "type": "integer"}, "name": {"title": "Name", "type": "string"}, "min_rounds": {"title": "Min Rounds", "default": 0, "type": "integer"}, "max_points": {"title": "Max Points", "default": 0, "type": "integer"}, "classifier": {"title": "Classifier", "default": false, "type": "boolean"}, "classifier_number": {"title": "Classifier Number", "type": "string"}, "scoring_type": {"default": "comstock", "allOf": [{"$ref": "#/definitions/Scoring"}]}}, "required": ["internal_id"]}}}
```

</div>
