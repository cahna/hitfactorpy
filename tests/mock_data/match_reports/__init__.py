import importlib
from pathlib import Path
from typing import Callable, Dict

from hitfactorpy.parsers.match_report.models import ParsedMatchReport

AssertMatchReportCallable = Callable[[ParsedMatchReport], None]

DIRECTORY = Path(__file__).resolve().parent
REPORT_FILES = list(DIRECTORY.glob("*.txt"))
BY_FILENAME = {str(f).split("tests/mock_data/")[-1]: f.read_text() for f in REPORT_FILES}
VALIDATORS: Dict[str, AssertMatchReportCallable] = {
    fname: importlib.import_module(f".{Path(fname).stem}", package="tests.mock_data.match_reports").assert_match_report
    # fname: __import__(f".{Path(fname).stem}", globals(), locals(), [], 1).assert_match_report
    for fname in BY_FILENAME.keys()
}
