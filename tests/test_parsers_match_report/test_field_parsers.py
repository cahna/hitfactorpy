from datetime import datetime

import pytest

from practipy.enums import Division, MatchLevel
from practipy.parsers.match_report import fields

_levels = [i.name for i in MatchLevel]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # Happy paths
        *((lvl, MatchLevel[lvl]) for lvl in _levels),
        *((f"Level{lvl}", MatchLevel[lvl]) for lvl in _levels),
        *((f"l {lvl}", MatchLevel[lvl]) for lvl in _levels),
        # Sad paths
        ("", None),
        (None, None),
        ("X", None),
    ],
)
def test_parse_match_level(test_input, expected):
    assert fields.parse_match_level(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("12/25/2022", datetime(year=2022, month=12, day=25)),
        ("", None),
        ("//", None),
        ("99/99/9999", None),
        ("26/01/2023", None),
        ("2022/12/25", None),
        (None, None),
        (12252022, None),
        (12 / 25 / 2022, None),
    ],
)
def test_parse_match_date(test_input, expected):
    assert fields.parse_match_date(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("pcc", Division.PCC),
        ("PCC", Division.PCC),
        ("pIsTol CaLIbEr cARbInE", Division.PCC),
        ("open", Division.OPEN),
        ("LTD", Division.LIMITED),
        ("Limited", Division.LIMITED),
        ("Carry Optics", Division.CARRY_OPTICS),
        ("CO", Division.CARRY_OPTICS),
        ("", Division.UNKNOWN),
        (None, Division.UNKNOWN),
        ("X", Division.UNKNOWN),
    ],
)
def test_parse_division(test_input, expected):
    assert fields.parse_division(test_input) == expected
