import logging
from typing import List, Optional

from ..csv_utils import parse_csv_row

logger = logging.getLogger(__name__)


def parse_match_report_column_lines(column_lines: List[str]) -> Optional[List[str]]:
    n_header_cols = len(column_lines)
    if n_header_cols == 0:
        logger.debug("no lines found for column names")
        return None
    if n_header_cols > 1:
        logger.error("expected only one header line, but found %d", n_header_cols)
    columns: Optional[List[str]] = parse_csv_row(column_lines[0])
    return columns
