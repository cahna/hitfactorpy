import csv
from typing import Any, Callable, Optional, TypeVar, Union

TCastReturn = TypeVar("TCastReturn")


def _safe_cast(
    value: Any, caster: Callable[[Any], TCastReturn], default: Optional[TCastReturn] = None
) -> Optional[TCastReturn]:
    try:
        return caster(value)
    except (ValueError, TypeError):
        return default


def parse_csv_row(row_string: str):
    """
    Parse a string containing one row of CSV data
    """
    values = list(csv.reader([row_string]))
    return values[0] if values else None


def parse_int_value(v: Optional[Union[str, int]]) -> Optional[int]:
    if isinstance(v, str) and v.isdigit():
        return _safe_cast(v, int)
    if isinstance(v, (int, float, complex)) and not isinstance(v, bool):
        return _safe_cast(v, int)
    return None


def parse_float_value(v: str | float | None) -> Optional[float]:
    if isinstance(v, str):
        return _safe_cast(v, float)
    if isinstance(v, (int, float, complex)) and not isinstance(v, bool):
        return _safe_cast(v, float)
    return None
