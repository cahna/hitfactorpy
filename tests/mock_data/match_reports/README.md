# Mock match reports for tests

The following pattern(s) *must* be followed for automatic discovery and testing. See `./__init__.py` for details.

## Add a match report for testing

1. Add the report text file to `tests/mock_data/match_reports` (ex: `report_foo.txt`)
  - The stem of the filename must conform to python source file naming requirements (rule of thumb: `^[a-z][_a-z0-9]*\.txt$`)
  - Sanitize competitor names
2. Add a corresponding python source file of the same name (ex: `report_foo.py`) that exports a function named `assert_match_report`
  - the exported function just be of type `Callable[[ParsedMatchReport], None]`
  - it should assert the expected state of the corresponding match report
