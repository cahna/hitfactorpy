import csv
from typing import Optional, Union


def parse_csv_row(row_string: str):
    """
    Parse a string containing one row of CSV data
    """
    values = list(csv.reader([row_string]))
    return values[0] if values else None


def parse_int_value(v: Optional[Union[str, int]]) -> Optional[int]:
    if isinstance(v, str) and v.isdigit():
        return int(v)
    if isinstance(v, (int, float, complex)) and not isinstance(v, bool):
        return int(v)
    return None


def parse_float_value(v: str | float | None) -> Optional[float]:
    if isinstance(v, str):
        # TODO: make better
        float(v)
    if isinstance(v, (int, float, complex)) and not isinstance(v, bool):
        return float(v)
    return None
