# CLI

After installing, the `hitfactorpy` command should be added to `$PATH`.

```console
$ hitfactorpy --help
```

If not, run it as a python module:

```console
$ python -m hitfactorpy --help
```

## Command: `parse-match`

Parse a match report into JSON.

```console
$ hitfactorpy parse-match ./report.txt --json-indent 2
{
    "name": "Paul Bunyan USPSA - January 2023 NW01",
    "raw_date": "01/08/2023",
    "date": "2023-01-08T00:00:00",
    "match_level": 1,
    "competitors": [ 
# (output truncated)
```

## Command: `json-schema`

Output the JSONSchema used to build parsed results.

- Show usage:
  ```console
  $ hitfactorpy json-schema --help
  ```
- Show the default (`match-report`) JSONSchema:
  ```console
  $ hitfactorpy json-schema
  ```
- Show JSONSchema for _only_ the `stage` model and use a custom title:
  ```console
  $ hitfactorpy json-schema --model stage --title "My Custom-Titled Schema"
  ```
