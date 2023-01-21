from datetime import datetime

import pytest

from hitfactorpy.enums import Classification, Division, MatchLevel, PowerFactor, Scoring
from hitfactorpy.parsers.match_report import fields

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
        ("12252022", None),
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
        ("L10", Division.LIMITED_10),
        ("Ltd10", Division.LIMITED_10),
        ("LIMITED 10", Division.LIMITED_10),
        ("PROD", Division.PRODUCTION),
        ("Production", Division.PRODUCTION),
        ("SS", Division.SINGLE_STACK),
        ("Single Stack", Division.SINGLE_STACK),
        ("SINGLE STACK", Division.SINGLE_STACK),
        ("rev", Division.REVOLVER),
        ("Revo", Division.REVOLVER),
        ("revolver", Division.REVOLVER),
        ("", Division.UNKNOWN),
        (None, Division.UNKNOWN),
        ("X", Division.UNKNOWN),
    ],
)
def test_parse_division(test_input, expected):
    assert fields.parse_division(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # Happy path
        ("gm", Classification.GM),
        ("grandmaster", Classification.GM),
        ("g", Classification.GM),
        ("m", Classification.M),
        ("master", Classification.M),
        ("a", Classification.A),
        ("b", Classification.B),
        ("c", Classification.C),
        ("d", Classification.D),
        ("u", Classification.U),
        ("x", Classification.U),
        # Sad path
        ("", Classification.UNKNOWN),
        (None, Classification.UNKNOWN),
        ("y", Division.UNKNOWN),
    ],
)
def test_parse_classification(test_input, expected):
    assert fields.parse_classification(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("mAjOr", PowerFactor.MAJOR),
        ("minor", PowerFactor.MINOR),
        ("", PowerFactor.UNKNOWN),
        (None, PowerFactor.UNKNOWN),
        ("y", PowerFactor.UNKNOWN),
    ],
)
def test_parse_power_factor(test_input, expected):
    assert fields.parse_power_factor(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("TY123321", "TY123321"),
        ("A-1", "A1"),
        ("L1771no", "L1771NO"),
        (" B-    000.-", "B000"),
        ("FY.0  ", "FY0"),
        (None, ""),
        ("", ""),
        (0, ""),
        (["test"], ""),
    ],
)
def test_parse_member_number(test_input, expected):
    assert fields.parse_member_number(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("COMSTOCK", Scoring.COMSTOCK),
        ("Virginia", Scoring.VIRGINIA),
        ("fixed", Scoring.FIXED_TIME),
        ("chrono", Scoring.CHRONO),
        ("", Scoring.UNKNOWN),
        (None, Scoring.UNKNOWN),
        ("major", Scoring.UNKNOWN),
    ],
)
def test_parse_scoring(test_input, expected):
    assert fields.parse_scoring(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("yes", True),
        ("Yes", True),
        ("YES", True),
        ("yES", True),
        ("   yEs  ", True),
        ("no", False),
        (None, False),
        ("", False),
        (0, False),
        (["test"], False),
    ],
)
def test_parse_boolean(test_input, expected):
    assert fields.parse_boolean(test_input) == expected
